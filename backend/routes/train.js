const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const fs = require('fs').promises;
const axios = require('axios');
const Script = require('../models/Script');

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: async (req, file, cb) => {
    const uploadDir = path.join(__dirname, '../scripts');
    try {
      await fs.mkdir(uploadDir, { recursive: true });
      cb(null, uploadDir);
    } catch (error) {
      cb(error);
    }
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({
  storage,
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB limit
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['.txt', '.pdf', '.doc', '.docx'];
    const ext = path.extname(file.originalname).toLowerCase();
    
    if (allowedTypes.includes(ext)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type. Only .txt, .pdf, .doc, .docx files are allowed.'));
    }
  }
});

// POST /api/train - Upload and process a training script
router.post('/', upload.single('script'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const { title, genre, year, author } = req.body;
    
    // Read file content
    let content;
    try {
      content = await fs.readFile(req.file.path, 'utf8');
    } catch (error) {
      // Handle binary files (PDF, DOC, DOCX) - for now, just store placeholder
      content = `[Binary file content - ${req.file.mimetype}]`;
    }

    // Create script document
    const script = new Script({
      title: title || path.parse(req.file.originalname).name,
      filename: req.file.filename,
      originalName: req.file.originalname,
      filePath: req.file.path,
      fileSize: req.file.size,
      mimeType: req.file.mimetype,
      content,
      metadata: {
        genre: genre || 'Unknown',
        year: year ? parseInt(year) : null,
        author: author || 'Unknown'
      }
    });

    await script.save();

    // Send to AI service for processing
    try {
      await axios.post(`${process.env.AI_SERVICE_URL}/train`, {
        scriptId: script._id,
        content,
        metadata: script.metadata
      });

      // Update status to processing
      await script.updateStatus('processing');

      res.json({
        message: 'Script uploaded successfully and sent for training',
        script: {
          id: script._id,
          title: script.title,
          status: script.status,
          filename: script.filename
        }
      });

    } catch (aiError) {
      console.error('AI Service Training Error:', aiError);
      
      // Update status to error
      await script.updateStatus('error');
      
      res.status(500).json({
        error: 'Script uploaded but training failed',
        script: {
          id: script._id,
          title: script.title,
          status: script.status,
          filename: script.filename
        }
      });
    }

  } catch (error) {
    console.error('Training route error:', error);
    
    // Clean up uploaded file if error occurred
    if (req.file) {
      try {
        await fs.unlink(req.file.path);
      } catch (unlinkError) {
        console.error('Error deleting uploaded file:', unlinkError);
      }
    }
    
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/train/status/:scriptId - Get training status
router.get('/status/:scriptId', async (req, res) => {
  try {
    const { scriptId } = req.params;
    
    const script = await Script.findById(scriptId);
    if (!script) {
      return res.status(404).json({ error: 'Script not found' });
    }

    res.json({
      scriptId: script._id,
      title: script.title,
      status: script.status,
      trainingData: script.trainingData,
      createdAt: script.createdAt,
      updatedAt: script.updatedAt
    });

  } catch (error) {
    console.error('Get training status error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Error handling middleware for multer
router.use((error, req, res, next) => {
  if (error instanceof multer.MulterError) {
    if (error.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({ error: 'File too large. Maximum size is 10MB.' });
    }
  }
  
  if (error.message.includes('Invalid file type')) {
    return res.status(400).json({ error: error.message });
  }
  
  next(error);
});

module.exports = router;
