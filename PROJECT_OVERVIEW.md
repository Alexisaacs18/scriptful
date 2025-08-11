# AI Movie Script Chatbot - Project Overview

## 🎯 Project Description

The AI Movie Script Chatbot is a comprehensive system that generates movie scripts, outlines, and dialogue using artificial intelligence. It features a modern React.js frontend, a robust Node.js Express backend, and a Python-based AI service that can be trained on uploaded movie scripts.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   AI Service    │
│   (React.js)    │◄──►│  (Node.js)      │◄──►│   (Python)      │
│   Port: 3000    │    │   Port: 5000    │    │   Port: 8000    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │    MongoDB      │
                       │   Port: 27017   │
                       └─────────────────┘
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Prerequisites:**
   - Docker and Docker Compose installed
   - Git

2. **Clone and Start:**
   ```bash
   cd Script_Full
   ./start.sh
   ```

3. **Access the Application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - AI Service: http://localhost:8000

### Option 2: Local Development

1. **Prerequisites:**
   - Node.js 18+
   - Python 3.9+
   - MongoDB (optional, can use Docker)

2. **Setup:**
   ```bash
   cd Script_Full
   ./dev-setup.sh
   ```

3. **Start Services:**
   ```bash
   # Terminal 1: MongoDB (if local)
   mongod --dbpath ./data/db
   
   # Terminal 2: Backend
   cd backend && npm run dev
   
   # Terminal 3: AI Service
   cd ai-service && python3 app.py
   
   # Terminal 4: Frontend
   cd frontend && npm run dev
   ```

## 📁 Project Structure

```
Script_Full/
├── frontend/                 # React.js application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── contexts/        # React contexts
│   │   ├── App.jsx         # Main app component
│   │   └── main.jsx        # Entry point
│   ├── package.json
│   ├── tailwind.config.js   # Tailwind CSS config
│   └── Dockerfile
├── backend/                  # Node.js Express server
│   ├── routes/              # API route handlers
│   ├── models/              # MongoDB models
│   ├── server.js            # Main server file
│   ├── package.json
│   └── Dockerfile
├── ai-service/              # Python AI service
│   ├── app.py              # Flask application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile
├── scripts/                 # Training data and scripts
│   └── sample_script.txt    # Example training script
├── docker-compose.yml       # Docker orchestration
├── start.sh                 # Docker startup script
├── dev-setup.sh            # Local development setup
├── README.md               # Main documentation
└── PROJECT_OVERVIEW.md     # This file
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
NODE_ENV=development
PORT=5000
MONGODB_URI=mongodb://admin:password123@localhost:27017/script_db?authSource=admin
AI_SERVICE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

#### AI Service (.env)
```bash
FLASK_ENV=development
FLASK_APP=app.py
PORT=8000
MODEL_PATH=./models
TRAINING_DATA_PATH=./scripts
```

## 📡 API Endpoints

### Backend API (Port 5000)

#### Chat
- `POST /api/chat` - Send chat message and get AI response
- `GET /api/chat/:conversationId` - Get conversation messages

#### Training
- `POST /api/train` - Upload and process training script
- `GET /api/train/status/:scriptId` - Get training status

#### Conversations
- `GET /api/conversations` - List all conversations
- `GET /api/conversations/:id` - Get specific conversation
- `PUT /api/conversations/:id` - Update conversation
- `DELETE /api/conversations/:id` - Delete conversation
- `GET /api/conversations/search` - Search conversations

#### Scripts
- `GET /api/scripts` - List all training scripts
- `GET /api/scripts/:id` - Get specific script
- `PUT /api/scripts/:id` - Update script metadata
- `DELETE /api/scripts/:id` - Delete script
- `GET /api/scripts/:id/download` - Download script file
- `GET /api/scripts/stats` - Get script statistics
- `GET /api/scripts/search` - Search scripts

### AI Service (Port 8000)

- `GET /health` - Health check
- `POST /generate` - Generate script or outline
- `POST /train` - Train model with new data
- `GET /scripts` - List training scripts
- `GET /scripts/:id` - Get specific training script

## 🎨 Frontend Features

- **Modern Chat Interface**: Similar to ChatGPT/Claude
- **Dark/Light Mode**: Toggle between themes
- **Output Selection**: Choose between script scenes or movie outlines
- **File Upload**: Upload new scripts for training
- **Conversation Management**: Clear conversations and export scripts
- **Responsive Design**: Works on desktop and mobile
- **Real-time Chat**: Interactive conversation with AI

## 🔒 Security Features

- **CORS Protection**: Configured for specific origins
- **Rate Limiting**: 100 requests per 15 minutes per IP
- **Input Validation**: Sanitized file uploads and API inputs
- **Helmet.js**: Security headers and protection
- **File Type Restrictions**: Only allowed script formats

## 📊 Database Schema

### Conversation Model
```javascript
{
  title: String,
  messages: [{
    type: 'user' | 'ai',
    content: String,
    timestamp: Date
  }],
  outputType: 'script' | 'outline',
  createdAt: Date,
  updatedAt: Date
}
```

### Script Model
```javascript
{
  title: String,
  filename: String,
  originalName: String,
  filePath: String,
  fileSize: Number,
  mimeType: String,
  content: String,
  status: 'pending' | 'processing' | 'trained' | 'error',
  trainingData: {
    scenes: [String],
    characters: [String],
    dialogue: [String],
    descriptions: [String]
  },
  metadata: {
    genre: String,
    length: String,
    year: Number,
    author: String
  },
  createdAt: Date,
  updatedAt: Date
}
```

## 🚀 Deployment

### Production Docker Compose
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables for Production
- Set `NODE_ENV=production`
- Use strong JWT secrets
- Configure proper MongoDB authentication
- Set up reverse proxy (nginx)
- Enable HTTPS

## 🧪 Testing

### Frontend
```bash
cd frontend
npm run test
```

### Backend
```bash
cd backend
npm test
```

### AI Service
```bash
cd ai-service
python -m pytest tests/
```

## 📈 Monitoring and Logging

- **Health Checks**: All services have health endpoints
- **Structured Logging**: Morgan for HTTP requests, custom for business logic
- **Error Handling**: Comprehensive error handling with proper HTTP status codes
- **Performance**: Compression middleware, rate limiting

## 🔄 Development Workflow

1. **Feature Development**: Create feature branch from main
2. **Local Testing**: Use dev-setup.sh for local development
3. **Docker Testing**: Use start.sh for Docker testing
4. **Code Review**: Submit pull request
5. **Deployment**: Merge to main triggers production deployment

## 🐛 Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure ports 3000, 5000, 8000, and 27017 are available
2. **MongoDB Connection**: Check MongoDB is running and credentials are correct
3. **File Permissions**: Ensure scripts directory is writable
4. **Dependencies**: Run `npm install` and `pip install -r requirements.txt`

### Logs
```bash
# Docker logs
docker-compose logs -f [service_name]

# Local logs
# Check console output for each service
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Check service health endpoints
4. Review logs for error details

---

**Happy Script Writing! 🎬✨**
