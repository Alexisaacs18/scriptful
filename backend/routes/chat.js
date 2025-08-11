const express = require('express');
const router = express.Router();
const axios = require('axios');
const Conversation = require('../models/Conversation');

// POST /api/chat - Send a chat message and get AI response
router.post('/', async (req, res) => {
  try {
    const { message, outputType = 'script', conversationId } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    let conversation;
    
    if (conversationId) {
      // Continue existing conversation
      conversation = await Conversation.findById(conversationId);
      if (!conversation) {
        return res.status(404).json({ error: 'Conversation not found' });
      }
    } else {
      // Create new conversation
      conversation = new Conversation({
        title: message.substring(0, 50) + '...',
        outputType
      });
    }

    // Add user message
    await conversation.addMessage('user', message);

    // Get AI response from AI service
    try {
      const aiResponse = await axios.post(`${process.env.AI_SERVICE_URL}/generate`, {
        prompt: message,
        outputType,
        conversationHistory: conversation.messages.slice(-10) // Last 10 messages for context
      });

      const aiContent = aiResponse.data.content || 'I apologize, but I encountered an error generating a response.';

      // Add AI response
      await conversation.addMessage('ai', aiContent);

      // Save conversation
      await conversation.save();

      res.json({
        conversationId: conversation._id,
        response: aiContent,
        conversation: conversation.getSummary()
      });

    } catch (aiError) {
      console.error('AI Service Error:', aiError);
      
      // Add error message
      await conversation.addMessage('ai', 'I apologize, but I encountered an error. Please try again.');
      await conversation.save();

      res.status(500).json({
        error: 'AI service unavailable',
        conversationId: conversation._id,
        response: 'I apologize, but I encountered an error. Please try again.',
        conversation: conversation.getSummary()
      });
    }

  } catch (error) {
    console.error('Chat route error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/chat/:conversationId - Get conversation messages
router.get('/:conversationId', async (req, res) => {
  try {
    const { conversationId } = req.params;
    
    const conversation = await Conversation.findById(conversationId);
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

module.exports = router;
