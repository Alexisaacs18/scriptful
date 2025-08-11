#!/bin/bash

echo "🔧 Setting up AI Movie Script Chatbot for development..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ and try again."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ and try again."
    exit 1
fi

# Check if MongoDB is installed
if ! command -v mongod &> /dev/null; then
    echo "⚠️  MongoDB is not installed. Please install MongoDB or use Docker."
    echo "   For macOS: brew install mongodb-community"
    echo "   For Ubuntu: sudo apt-get install mongodb"
fi

echo "📦 Installing dependencies..."

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
npm install
cd ..

# Install AI service dependencies
echo "Installing AI service dependencies..."
cd ai-service
pip3 install -r requirements.txt
cd ..

echo ""
echo "✅ Dependencies installed successfully!"
echo ""
echo "🚀 To start development servers:"
echo ""
echo "1. Start MongoDB (if installed locally):"
echo "   mongod --dbpath ./data/db"
echo ""
echo "2. Start Backend (in new terminal):"
echo "   cd backend && npm run dev"
echo ""
echo "3. Start AI Service (in new terminal):"
echo "   cd ai-service && python3 app.py"
echo ""
echo "4. Start Frontend (in new terminal):"
echo "   cd frontend && npm run dev"
echo ""
echo "🌐 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:5000"
echo "   AI Service: http://localhost:8000"
echo ""
echo "📝 Note: Make sure to copy env.example files to .env and configure them properly."
