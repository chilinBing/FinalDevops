@echo off
REM Build script for all Docker images (Windows)

echo Building all Docker images...

REM Build frontend
echo.
echo Building frontend image...
docker build -t inventory-frontend:latest -f frontend/Dockerfile .

REM Build backend
echo.
echo Building backend image...
docker build -t inventory-backend:latest -f backend/Dockerfile .

REM Build database
echo.
echo Building database image...
docker build -t inventory-database:latest -f database/Dockerfile database/

echo.
echo All images built successfully!

REM List images
echo.
echo Docker images:
docker images | findstr inventory

echo.
echo To run all services:
echo docker-compose -f docker-compose-microservices.yml up -d

pause
