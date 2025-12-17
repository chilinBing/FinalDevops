#!/bin/bash

# Build script for all Docker images

echo "🏗️ Building all Docker images..."

# Build frontend
echo "📦 Building frontend image..."
docker build -t inventory-frontend:latest -f frontend/Dockerfile .

# Build backend
echo "📦 Building backend image..."
docker build -t inventory-backend:latest -f backend/Dockerfile .

# Build database
echo "📦 Building database image..."
docker build -t inventory-database:latest -f database/Dockerfile database/

echo "✅ All images built successfully!"

# List images
echo ""
echo "📊 Docker images:"
docker images | grep inventory

echo ""
echo "🚀 To run all services:"
echo "docker-compose -f docker-compose-microservices.yml up -d"
