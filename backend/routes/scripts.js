const express = require('express');
const router = express.Router();
const Script = require('../models/Script');
const path = require('path');
const fs = require('fs').promises;

// GET /api/scripts - Get all scripts
router.get('/', async (req, res) => {
  try {
    const { page = 1, limit = 20, status, genre } = req.query;
    
    const query = {};
    if (status) {
      query.status = status;
    }
    if (genre) {
      query['metadata.genre'] = genre;
    }

    const scripts = await Script.find(query)
      .sort({ createdAt: -1 })
      .limit(limit * 1)
      .skip((page - 1) * limit)
      .select('-content') // Don't send full content in list
      .exec();

    const total = await Script.countDocuments(query);

    res.json({
      scripts,
      pagination: {
        currentPage: parseInt(page),
        totalPages: Math.ceil(total / limit),
        totalScripts: total,
        hasNext: page * limit < total,
        hasPrev: page > 1
      }
    });

  } catch (error) {
    console.error('Get scripts error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/scripts/:id - Get specific script
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    const script = await Script.findById(id);
    if (!script) {
      return res.status(404).json({ error: 'Script not found' });
    }

    res.json({ script });

  } catch (error) {
    console.error('Get script error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// PUT /api/scripts/:id - Update script metadata
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { title, genre, year, author } = req.body;
    
    const script = await Script.findById(id);
    if (!script) {
      return res.status(404).json({ error: 'Script not found' });
    }

    if (title !== undefined) {
      script.title = title;
    }
    
    if (genre !== undefined) {
      script.metadata.genre = genre;
    }
    
    if (year !== undefined) {
      script.metadata.year = parseInt(year);
    }
    
    if (author !== undefined) {
      script.metadata.author = author;
    }

    await script.save();

    res.json({
      message: 'Script updated successfully',
      script
    });

  } catch (error) {
    console.error('Update script error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// DELETE /api/scripts/:id - Delete script
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    const script = await Script.findById(id);
    if (!script) {
      return res.status(404).json({ error: 'Script not found' });
    }

    // Delete the file from disk
    try {
      await fs.unlink(script.filePath);
    } catch (unlinkError) {
      console.error('Error deleting file from disk:', unlinkError);
      // Continue with deletion even if file deletion fails
    }

    // Delete from database
    await Script.findByIdAndDelete(id);

    res.json({
      message: 'Script deleted successfully',
      scriptId: id
    });

  } catch (error) {
    console.error('Delete script error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/scripts/:id/download - Download script file
router.get('/:id/download', async (req, res) => {
  try {
    const { id } = req.params;
    
    const script = await Script.findById(id);
    if (!script) {
      return res.status(404).json({ error: 'Script not found' });
    }

    // Check if file exists
    try {
      await fs.access(script.filePath);
    } catch (error) {
      return res.status(404).json({ error: 'Script file not found on disk' });
    }

    res.download(script.filePath, script.originalName);

  } catch (error) {
    console.error('Download script error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/scripts/stats - Get script statistics
router.get('/stats', async (req, res) => {
  try {
    const stats = await Script.aggregate([
      {
        $group: {
          _id: null,
          totalScripts: { $sum: 1 },
          totalSize: { $sum: '$fileSize' },
          avgSize: { $avg: '$fileSize' },
          byStatus: {
            $push: {
              status: '$status',
              count: 1
            }
          },
          byGenre: {
            $push: {
              genre: '$metadata.genre',
              count: 1
            }
          }
        }
      }
    ]);

    if (stats.length === 0) {
      return res.json({
        totalScripts: 0,
        totalSize: 0,
        avgSize: 0,
        byStatus: {},
        byGenre: {}
      });
    }

    const stat = stats[0];
    
    // Process status counts
    const statusCounts = {};
    stat.byStatus.forEach(item => {
      statusCounts[item.status] = (statusCounts[item.status] || 0) + item.count;
    });

    // Process genre counts
    const genreCounts = {};
    stat.byGenre.forEach(item => {
      genreCounts[item.genre] = (genreCounts[item.genre] || 0) + item.count;
    });

    res.json({
      totalScripts: stat.totalScripts,
      totalSize: stat.totalSize,
      avgSize: Math.round(stat.avgSize),
      byStatus: statusCounts,
      byGenre: genreCounts
    });

  } catch (error) {
    console.error('Get script stats error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/scripts/search - Search scripts
router.get('/search', async (req, res) => {
  try {
    const { q, page = 1, limit = 20 } = req.query;
    
    if (!q) {
      return res.status(400).json({ error: 'Search query is required' });
    }

    const searchRegex = new RegExp(q, 'i');
    
    const scripts = await Script.find({
      $or: [
        { title: searchRegex },
        { content: searchRegex },
        { 'metadata.genre': searchRegex },
        { 'metadata.author': searchRegex }
      ]
    })
    .sort({ createdAt: -1 })
    .limit(limit * 1)
    .skip((page - 1) * limit)
    .select('-content')
    .exec();

    const total = await Script.countDocuments({
      $or: [
        { title: searchRegex },
        { content: searchRegex },
        { 'metadata.genre': searchRegex },
        { 'metadata.author': searchRegex }
      ]
    });

    res.json({
      scripts,
      pagination: {
        currentPage: parseInt(page),
        totalPages: Math.ceil(total / limit),
        totalScripts: total,
        hasNext: page * limit < total,
        hasPrev: page > 1
      }
    });

  } catch (error) {
    console.error('Search scripts error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
