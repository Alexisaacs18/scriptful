#!/bin/bash

echo "🚀 Starting AI Movie Script Chatbot..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install it and try again."
    exit 1
fi

echo "📦 Building and starting services..."
docker-compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 10

# Check service health
echo "🔍 Checking service health..."

# Check MongoDB
if curl -s http://localhost:27017 > /dev/null; then
    echo "✅ MongoDB is running"
else
    echo "❌ MongoDB is not accessible"
fi

# Check Backend
if curl -s http://localhost:5000/health > /dev/null; then
    echo "✅ Backend API is running"
else
    echo "❌ Backend API is not accessible"
fi

# Check AI Service
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ AI Service is running"
else
    echo "❌ AI Service is not accessible"
fi

# Check Frontend
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is running"
else
    echo "❌ Frontend is not accessible"
fi

echo ""
echo "🎬 AI Movie Script Chatbot is ready!"
echo ""
echo "🌐 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:5000"
echo "   AI Service: http://localhost:8000"
echo ""
echo "📚 API Documentation:"
echo "   Health Check: http://localhost:5000/health"
echo "   Chat: POST http://localhost:5000/api/chat"
echo "   Train: POST http://localhost:5000/api/train"
echo "   Conversations: GET http://localhost:5000/api/conversations"
echo "   Scripts: GET http://localhost:5000/api/scripts"
echo ""
echo "🛑 To stop the services, run: docker-compose down"
echo "📊 To view logs, run: docker-compose logs -f"
