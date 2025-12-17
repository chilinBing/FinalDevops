# 🐳 Docker Microservices Setup

## 📋 Architecture Overview

This project uses a **3-tier microservices architecture**:

```
┌─────────────────┐
│    Frontend     │  (Nginx - Port 80)
│  Static Files   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Backend     │  (Node.js - Port 3000)
│   REST API      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Database     │  (MongoDB - Port 27017)
│   Data Storage  │
└─────────────────┘
```

## 📁 Directory Structure

```
inventory-management-system/
├── frontend/
│   ├── Dockerfile              # Frontend container config
│   ├── nginx.conf              # Nginx configuration
│   └── .dockerignore           # Frontend ignore file
├── backend/
│   ├── Dockerfile              # Backend container config
│   └── .dockerignore           # Backend ignore file
├── database/
│   ├── Dockerfile              # Database container config
│   ├── init-mongo.js           # DB initialization script
│   └── mongod.conf             # MongoDB configuration
├── docker-compose-microservices.yml  # Multi-service orchestration
├── build-all.sh                # Build script (Linux/Mac)
└── build-all.bat               # Build script (Windows)
```

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose -f docker-compose-microservices.yml up --build -d

# View logs
docker-compose -f docker-compose-microservices.yml logs -f

# Stop all services
docker-compose -f docker-compose-microservices.yml down

# Stop and remove volumes (clean slate)
docker-compose -f docker-compose-microservices.yml down -v
```

### Option 2: Build Individual Images

**Windows:**
```bash
build-all.bat
```

**Linux/Mac:**
```bash
chmod +x build-all.sh
./build-all.sh
```

### Option 3: Manual Build

```bash
# Build frontend
docker build -t inventory-frontend:latest -f frontend/Dockerfile .

# Build backend
docker build -t inventory-backend:latest -f backend/Dockerfile .

# Build database
docker build -t inventory-database:latest -f database/Dockerfile database/
```

## 🔍 Verify Deployment

### Check Running Containers

```bash
docker ps
```

Expected output:
```
CONTAINER ID   IMAGE                  STATUS                    PORTS
xxxxx          inventory-frontend     Up (healthy)              0.0.0.0:80->80/tcp
xxxxx          inventory-backend      Up (healthy)              0.0.0.0:3000->3000/tcp
xxxxx          inventory-database     Up (healthy)              0.0.0.0:27017->27017/tcp
```

### Check Container Health

```bash
# Check all services
docker-compose -f docker-compose-microservices.yml ps

# Check specific service health
docker inspect inventory-frontend --format='{{.State.Health.Status}}'
docker inspect inventory-backend --format='{{.State.Health.Status}}'
docker inspect inventory-database --format='{{.State.Health.Status}}'
```

### Test Services

```bash
# Test frontend
curl http://localhost/

# Test backend health
curl http://localhost:3000/health

# Test backend API
curl http://localhost/api/inventory

# Test database connection
docker exec -it inventory-database mongosh -u admin -p password123 --authenticationDatabase admin
```

## 📊 Service Details

### Frontend Service
- **Image**: inventory-frontend
- **Base**: nginx:alpine
- **Port**: 80
- **Purpose**: Serves static HTML/CSS/JS files
- **Features**:
  - Gzip compression
  - Security headers
  - API proxy to backend
  - Health check endpoint

### Backend Service
- **Image**: inventory-backend
- **Base**: node:18-alpine
- **Port**: 3000
- **Purpose**: REST API with authentication
- **Features**:
  - JWT authentication
  - User management
  - Inventory CRUD operations
  - MongoDB integration
  - Health checks

### Database Service
- **Image**: inventory-database
- **Base**: mongo:7.0
- **Port**: 27017
- **Purpose**: Data persistence
- **Features**:
  - Authentication enabled
  - Automatic initialization
  - Sample data included
  - Indexes for performance
  - Persistent volumes

## 🔐 Default Credentials

### MongoDB
- **Root Username**: admin
- **Root Password**: password123
- **Database**: inventory

### Application
- **Admin Username**: admin
- **Admin Password**: admin123
- **Role**: admin

## 🌐 Access URLs

- **Frontend**: http://localhost
- **Backend API**: http://localhost:3000
- **Backend Health**: http://localhost:3000/health
- **Login Page**: http://localhost/login.html
- **Register Page**: http://localhost/register.html

## 📸 Screenshots for Submission

### 1. Docker Images
```bash
docker images | grep inventory
```

### 2. Running Containers
```bash
docker ps
```

### 3. Docker Compose Status
```bash
docker-compose -f docker-compose-microservices.yml ps
```

### 4. Container Logs
```bash
docker-compose -f docker-compose-microservices.yml logs
```

### 5. Network Inspection
```bash
docker network inspect inventory-network
```

## 🛠️ Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs inventory-frontend
docker logs inventory-backend
docker logs inventory-database

# Check health status
docker inspect inventory-backend --format='{{json .State.Health}}'
```

### Port Already in Use

```bash
# Windows
netstat -ano | findstr :80
netstat -ano | findstr :3000
netstat -ano | findstr :27017

# Linux/Mac
lsof -i :80
lsof -i :3000
lsof -i :27017
```

### Database Connection Issues

```bash
# Access MongoDB shell
docker exec -it inventory-database mongosh -u admin -p password123 --authenticationDatabase admin

# Check database
use inventory
show collections
db.inventoryitems.find().pretty()
```

### Reset Everything

```bash
# Stop and remove all containers, networks, and volumes
docker-compose -f docker-compose-microservices.yml down -v

# Remove images
docker rmi inventory-frontend inventory-backend inventory-database

# Rebuild from scratch
docker-compose -f docker-compose-microservices.yml up --build -d
```

## 📦 Volume Management

### List Volumes
```bash
docker volume ls | grep inventory
```

### Backup Database
```bash
docker exec inventory-database mongodump --username admin --password password123 --authenticationDatabase admin --db inventory --out /backup
docker cp inventory-database:/backup ./backup
```

### Restore Database
```bash
docker cp ./backup inventory-database:/backup
docker exec inventory-database mongorestore --username admin --password password123 --authenticationDatabase admin --db inventory /backup/inventory
```

## 🎯 Production Deployment

For production deployment to Docker Hub:

```bash
# Tag images
docker tag inventory-frontend:latest yourusername/inventory-frontend:latest
docker tag inventory-backend:latest yourusername/inventory-backend:latest
docker tag inventory-database:latest yourusername/inventory-database:latest

# Push to Docker Hub
docker push yourusername/inventory-frontend:latest
docker push yourusername/inventory-backend:latest
docker push yourusername/inventory-database:latest
```

## ✅ Verification Checklist

- [ ] All three Dockerfiles created
- [ ] Docker Compose file configured
- [ ] All images build successfully
- [ ] All containers start and show "healthy" status
- [ ] Frontend accessible at http://localhost
- [ ] Backend API responds at http://localhost:3000/health
- [ ] Database accepts connections
- [ ] Services can communicate with each other
- [ ] Data persists after container restart
- [ ] Screenshots taken for submission

## 🎓 Submission Requirements

For **Section A: Containerization (10 Marks)**:

1. ✅ **Separate Dockerfiles** (4 marks)
   - frontend/Dockerfile
   - backend/Dockerfile
   - database/Dockerfile

2. ✅ **Docker Compose** (4 marks)
   - docker-compose-microservices.yml
   - All services configured
   - Network setup
   - Volume persistence

3. ✅ **Screenshots** (2 marks)
   - `docker images` output
   - `docker ps` output showing all 3 containers
   - `docker-compose ps` output
   - Application running in browser

---

**🎉 All Docker requirements completed!**
