const express = require('express');
const router = express.Router();
const Conversation = require('../models/Conversation');

// GET /api/conversations - Get all conversations
router.get('/', async (req, res) => {
  try {
    const { page = 1, limit = 20, outputType } = req.query;
    
    const query = {};
    if (outputType) {
      query.outputType = outputType;
    }

    const conversations = await Conversation.find(query)
      .sort({ updatedAt: -1 })
      .limit(limit * 1)
      .skip((page - 1) * limit)
      .exec();

    const total = await Conversation.countDocuments(query);

    res.json({
      conversations: conversations.map(conv => conv.getSummary()),
      pagination: {
        currentPage: parseInt(page),
        totalPages: Math.ceil(total / limit),
        totalConversations: total,
        hasNext: page * limit < total,
        hasPrev: page > 1
      }
    });

  } catch (error) {
    console.error('Get conversations error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/conversations/:id - Get specific conversation
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    const conversation = await Conversation.findById(id);
    if (!conversation) {
      return res.status(404).json({ error: 'Conversation not found' });
    }

    res.json({
      conversation: conversation.getSummary(),
      messages: conversation.messages
    });

  } catch (error) {
    console.error('Get conversation error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// PUT /api/conversations/:id - Update conversation (e.g., title)
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { title, outputType } = req.body;
    
    const conversation = await Conversation.findById(id);
    if (!conversation) {
      return res.status(404).json({ error: 'Conversation not found' });
    }

    if (title !== undefined) {
      conversation.title = title;
    }
    
    if (outputType !== undefined) {
      conversation.outputType = outputType;
    }

    await conversation.save();

    res.json({
      message: 'Conversation updated successfully',
      conversation: conversation.getSummary()
    });

  } catch (error) {
    console.error('Update conversation error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// DELETE /api/conversations/:id - Delete conversation
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    const conversation = await Conversation.findByIdAndDelete(id);
    if (!conversation) {
      return res.status(404).json({ error: 'Conversation not found' });
    }

    res.json({
      message: 'Conversation deleted successfully',
      conversationId: id
    });

  } catch (error) {
    console.error('Delete conversation error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// POST /api/conversations/:id/messages - Add message to conversation
router.post('/:id/messages', async (req, res) => {
  try {
    const { id } = req.params;
    const { type, content } = req.body;
    
    if (!type || !content) {
      return res.status(400).json({ error: 'Type and content are required' });
    }

    if (!['user', 'ai'].includes(type)) {
      return res.status(400).json({ error: 'Type must be either "user" or "ai"' });
    }

    const conversation = await Conversation.findById(id);
    if (!conversation) {
      return res.status(404).json({ error: 'Conversation not found' });
    }

    await conversation.addMessage(type, content);

    res.json({
      message: 'Message added successfully',
      conversation: conversation.getSummary()
    });

  } catch (error) {
    console.error('Add message error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/conversations/search - Search conversations
router.get('/search', async (req, res) => {
  try {
    const { q, page = 1, limit = 20 } = req.query;
    
    if (!q) {
      return res.status(400).json({ error: 'Search query is required' });
    }

    const searchRegex = new RegExp(q, 'i');
    
    const conversations = await Conversation.find({
      $or: [
        { title: searchRegex },
        { 'messages.content': searchRegex }
      ]
    })
    .sort({ updatedAt: -1 })
    .limit(limit * 1)
    .skip((page - 1) * limit)
    .exec();

    const total = await Conversation.countDocuments({
      $or: [
        { title: searchRegex },
        { 'messages.content': searchRegex }
      ]
    });

    res.json({
      conversations: conversations.map(conv => conv.getSummary()),
      pagination: {
        currentPage: parseInt(page),
        totalPages: Math.ceil(total / limit),
        totalConversations: total,
        hasNext: page * limit < total,
        hasPrev: page > 1
      }
    });

  } catch (error) {
    console.error('Search conversations error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
