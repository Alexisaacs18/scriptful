# 🎬 Scriptful - AI Movie Script Generator

A powerful AI-powered application that generates movie scripts, outlines, and provides creative writing assistance using OpenAI's GPT models.

## ✨ Features

- **🎭 Script Scene Generation**: Create cinematic scenes with dialogue and action
- **📋 Movie Outline Creation**: Generate complete 3-act movie structures
- **💬 AI Chat Interface**: Interactive conversations about movie ideas and writing
- **🎨 Modern UI**: Beautiful, responsive chatbot interface
- **🧠 AI Training**: Uses extensive screenplay training data for quality output
- **🚀 Real-time Generation**: Instant AI-powered content creation

## 🏗️ Architecture

```
Scriptful/
├── ai-service/          # Python Flask AI service
├── backend/             # Node.js Express API
├── frontend/            # React frontend (Vite)
├── training/            # AI training data (screenplays)
├── scripts/             # Sample scripts
└── simple_app.html      # Standalone HTML interface
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/scriptful.git
   cd scriptful
   ```

2. **Set up AI Service**
   ```bash
   cd ai-service
   pip install -r requirements.txt
   # Add your OpenAI API key to app.py
   python app.py
   ```

3. **Set up Backend**
   ```bash
   cd backend
   npm install
   npm start
   ```

4. **Set up Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5001
   - AI Service: http://localhost:8001
   - Standalone: Open `simple_app.html` in browser

## 🔧 Configuration

### Environment Variables
Create `.env` files in each service directory:

**AI Service (.env)**
```env
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
PORT=8001
```

**Backend (.env)**
```env
PORT=5001
MONGODB_URI=mongodb://localhost:27017/script_db
NODE_ENV=development
```

## 📚 API Endpoints

### AI Service (Port 8001)
- `GET /health` - Service health check
- `POST /generate` - Generate scripts/outlines
- `POST /train` - Add training data
- `GET /scripts` - List training scripts

### Backend API (Port 5001)
- `GET /health` - API health check
- `POST /api/chat` - AI chat endpoint
- `GET /api/scripts` - List scripts
- `POST /api/train` - Training endpoint

## 🎭 Training Data

The AI service includes 29+ high-quality screenplay files covering:
- **Sample Scripts**: Pulp Fiction, Good Will Hunting, Inglorious Basterds
- **Dialogue Patterns**: Tarantino-style, emotional monologues, natural conversations
- **Character Development**: Backstory reveals, transformation moments
- **Plot Structures**: Tension building, plot twists, pacing examples
- **Visual Storytelling**: Cinematic descriptions and scene elements

## 🛠️ Development

### Running in Development Mode
```bash
# AI Service
cd ai-service && python app.py

# Backend
cd backend && npm run dev

# Frontend
cd frontend && npm run dev
```

### Docker Support
```bash
docker-compose up --build
```

## 📱 Usage

1. **Choose Generation Type**: Script Scene, Movie Outline, or AI Chat
2. **Enter Your Prompt**: Describe what you want to create
3. **Generate Content**: AI processes your request and generates content
4. **View Results**: Generated content appears in the chat interface

## 🔒 Security

- OpenAI API key should be kept secure
- CORS configured for development
- Rate limiting implemented on API endpoints
- Input validation and sanitization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models
- Training data from various screenplay sources
- Open source community for libraries and tools

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/scriptful/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/scriptful/discussions)
- **Wiki**: [Project Wiki](https://github.com/yourusername/scriptful/wiki)

---

**Made with ❤️ for the creative writing community**
