# 📸 Screenshot Checklist for Final Exam Submission

## Overview
This document provides a complete checklist of all screenshots needed for the final exam submission, organized by section.

---

## 📋 SECTION A: CONTAINERIZATION (3 Screenshots)

### Screenshot 1: Docker Images
**Command**:
```bash
docker images
```

**What to Show**:
- ✅ midlab-frontend image (~81.3MB)
- ✅ midlab-backend image (~232MB)
- ✅ midlab-database image (~1.13GB)
- ✅ Image IDs and creation dates
- ✅ All three images clearly visible

**Alternative Command**:
```bash
docker images | findstr midlab
```

---

### Screenshot 2: Running Containers
**Command**:
```bash
docker ps
```

**What to Show**:
- ✅ inventory-frontend container (Status: Up, Healthy)
- ✅ inventory-backend container (Status: Up, Healthy)
- ✅ inventory-database container (Status: Up, Healthy)
- ✅ Port mappings (80:80, 3000:3000, 27017:27017)
- ✅ Container names and IDs

**Alternative Command**:
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

---

### Screenshot 3: Docker Compose Status
**Command**:
```bash
docker-compose -f docker-compose-microservices.yml ps
```

**What to Show**:
- ✅ All three services listed
- ✅ State: Up
- ✅ Ports mapped correctly
- ✅ Service names visible

**Alternative - Application Running**:
- Open browser to `http://localhost`
- Show the login page or main dashboard
- Demonstrate the application is accessible

---

## 📋 SECTION B: CI/CD AUTOMATION (4 Screenshots)

### Screenshot 4: GitHub Actions Workflow Overview
**Location**: GitHub Repository → Actions Tab

**What to Show**:
- ✅ Recent workflow runs
- ✅ All stages showing green checkmarks
- ✅ Workflow name: "CI/CD Pipeline"
- ✅ Trigger: Push to main/develop
- ✅ Successful completion status

**Steps**:
1. Go to your GitHub repository
2. Click on "Actions" tab
3. Click on the most recent workflow run
4. Take screenshot showing all stages passed

---

### Screenshot 5: Test Results with Coverage
**Command**:
```bash
npm test
```

**What to Show**:
- ✅ All 4 test suites passed
- ✅ 29 tests passed
- ✅ Coverage summary table
- ✅ Coverage percentages (>80%)
- ✅ Execution time
- ✅ No failed tests

**Alternative - GitHub Actions**:
- In the workflow run, click on "Test" stage
- Expand the "Run automated tests" step
- Show the test output with coverage

---

### Screenshot 6: Docker Hub Images
**Location**: https://hub.docker.com

**What to Show**:
- ✅ Repository: faizanazam/inventory-management
- ✅ Multiple tags (latest, commit SHA)
- ✅ Image sizes
- ✅ Push dates/times
- ✅ Pull command visible

**Steps**:
1. Log in to Docker Hub
2. Navigate to your repository
3. Click on "Tags" tab
4. Show multiple tagged images

---

### Screenshot 7: CI/CD Pipeline Stages
**Location**: GitHub Actions → Workflow Run Details

**What to Show**:
- ✅ Test stage (completed successfully)
- ✅ Build and Push stage (completed successfully)
- ✅ Deploy to AKS stage (completed successfully)
- ✅ Execution times for each stage
- ✅ Green checkmarks for all stages

**Steps**:
1. Open the workflow run
2. Show the visual pipeline diagram
3. Ensure all stages are green

---

## 📋 SECTION C: KUBERNETES ON AZURE (6 Screenshots)

### Screenshot 8: Kubectl Get Pods
**Command**:
```bash
kubectl get pods -n inventory-system
```

**What to Show**:
- ✅ All pods in "Running" state
- ✅ Ready status (e.g., 1/1, 2/2)
- ✅ No restarts or minimal restarts
- ✅ Pod names visible
- ✅ Age of pods

**Alternative with More Details**:
```bash
kubectl get pods -n inventory-system -o wide
```

---

### Screenshot 9: Kubectl Get Services
**Command**:
```bash
kubectl get services -n inventory-system
```

**What to Show**:
- ✅ Service names
- ✅ Service types (LoadBalancer, ClusterIP)
- ✅ External IP address (for LoadBalancer)
- ✅ Ports (80:30XXX, 3000:30XXX)
- ✅ Age of services

**Alternative**:
```bash
kubectl get svc -n inventory-system
```

---

### Screenshot 10: Kubectl Get All
**Command**:
```bash
kubectl get all -n inventory-system
```

**What to Show**:
- ✅ All resources (pods, services, deployments, replicasets)
- ✅ Everything in healthy state
- ✅ Deployment status (e.g., 1/1 ready)
- ✅ Service endpoints
- ✅ Complete overview of the namespace

---

### Screenshot 11: Application on Public IP - Login Page
**URL**: http://4.144.249.110/login.html

**What to Show**:
- ✅ Login page fully loaded
- ✅ URL bar showing public IP
- ✅ Login form visible
- ✅ "Inventory Management System" title
- ✅ No errors in browser console (optional)

**Steps**:
1. Open browser
2. Navigate to http://4.144.249.110/login.html
3. Ensure page loads completely
4. Take screenshot

---

### Screenshot 12: Application - Main Dashboard
**URL**: http://4.144.249.110

**What to Show**:
- ✅ Main inventory dashboard
- ✅ Logged in (after using credentials)
- ✅ Inventory items displayed
- ✅ Navigation working
- ✅ URL showing public IP

**Steps**:
1. Login with credentials (admin/admin123)
2. Navigate to main dashboard
3. Show inventory items
4. Take screenshot

---

### Screenshot 13: Health Check Endpoint
**URL**: http://4.144.249.110/health

**What to Show**:
- ✅ JSON response with "status": "healthy"
- ✅ Timestamp
- ✅ URL showing /health endpoint
- ✅ HTTP 200 status

**Alternative - Using curl**:
```bash
curl http://4.144.249.110/health
```

---

## 📋 BONUS SCREENSHOTS (Optional but Recommended)

### Bonus 1: Azure Portal - AKS Cluster
**Location**: Azure Portal → Kubernetes Services

**What to Show**:
- ✅ Cluster name: inventory-aks
- ✅ Resource group: inventory-rg-sea
- ✅ Region: Southeast Asia
- ✅ Status: Running
- ✅ Node count and size

---

### Bonus 2: Coverage Report (Codecov)
**Location**: Codecov Dashboard (if configured)

**What to Show**:
- ✅ Overall coverage percentage
- ✅ Coverage trends
- ✅ File-by-file coverage
- ✅ Recent commits

---

### Bonus 3: Docker Compose Logs
**Command**:
```bash
docker-compose -f docker-compose-microservices.yml logs --tail=50
```

**What to Show**:
- ✅ Logs from all three services
- ✅ No error messages
- ✅ Successful startup messages
- ✅ Health check confirmations

---

### Bonus 4: Network Inspection
**Command**:
```bash
docker network inspect midlab_inventory-network
```

**What to Show**:
- ✅ Network configuration
- ✅ All three containers connected
- ✅ IP addresses assigned
- ✅ Subnet configuration

---

## 📝 Screenshot Organization

### Recommended File Naming:
```
Section-A/
├── 01-docker-images.png
├── 02-docker-containers-running.png
└── 03-docker-compose-status.png

Section-B/
├── 04-github-actions-workflow.png
├── 05-test-results-coverage.png
├── 06-docker-hub-images.png
└── 07-cicd-pipeline-stages.png

Section-C/
├── 08-kubectl-get-pods.png
├── 09-kubectl-get-services.png
├── 10-kubectl-get-all.png
├── 11-app-login-page.png
├── 12-app-dashboard.png
└── 13-health-check.png

Bonus/
├── azure-aks-cluster.png
├── codecov-coverage.png
├── docker-logs.png
└── network-inspection.png
```

---

## ✅ Pre-Screenshot Checklist

### Before Taking Screenshots:

#### For Section A:
- [ ] Run `docker-compose -f docker-compose-microservices.yml up -d`
- [ ] Wait for all containers to be healthy
- [ ] Verify with `docker ps`

#### For Section B:
- [ ] Push code to GitHub to trigger pipeline
- [ ] Wait for pipeline to complete
- [ ] Run `npm test` locally
- [ ] Verify Docker Hub has images

#### For Section C:
- [ ] Verify AKS cluster is running
- [ ] Check pods are in Running state
- [ ] Verify public IP is accessible
- [ ] Test login functionality

---

## 🎯 Quality Guidelines

### Screenshot Quality:
- ✅ High resolution (at least 1920x1080)
- ✅ Clear and readable text
- ✅ No sensitive information visible
- ✅ Proper cropping (remove unnecessary parts)
- ✅ Consistent format (PNG or JPG)

### What to Avoid:
- ❌ Blurry or low-resolution images
- ❌ Screenshots with personal information
- ❌ Partial or cut-off content
- ❌ Dark mode (if text is hard to read)
- ❌ Multiple screenshots for same requirement

---

## 📊 Screenshot Summary

| Section | Required | Bonus | Total |
|---------|----------|-------|-------|
| A | 3 | 2 | 5 |
| B | 4 | 1 | 5 |
| C | 6 | 1 | 7 |
| **Total** | **13** | **4** | **17** |

---

## 🚀 Quick Commands Reference

### Start Everything:
```bash
# Start Docker containers
docker-compose -f docker-compose-microservices.yml up -d

# Run tests
npm test

# Check Kubernetes
kubectl get all -n inventory-system
```

### Verify Everything:
```bash
# Docker
docker ps
docker images

# Tests
npm test

# Kubernetes
kubectl get pods -n inventory-system
kubectl get svc -n inventory-system

# Application
curl http://4.144.249.110/health
```

---

## 📝 Final Checklist

Before submission, ensure you have:

- [ ] All 13 required screenshots
- [ ] Screenshots are properly named
- [ ] Screenshots are organized by section
- [ ] All screenshots are clear and readable
- [ ] No sensitive information in screenshots
- [ ] Bonus screenshots (optional)
- [ ] Screenshot summary document

---

## 🎓 Submission Format

### Recommended Structure:
```
Final-Exam-Submission/
├── Code/
│   └── [All source code files]
├── Documentation/
│   ├── SECTION-A-COMPLETED.md
│   ├── SECTION-B-COMPLETED.md
│   └── FINAL-COMPLETION-SUMMARY.md
├── Screenshots/
│   ├── Section-A/
│   ├── Section-B/
│   └── Section-C/
└── README.md
```

---

**Good luck with your screenshots!** 📸✨

**Remember**: Quality over quantity. Make sure each screenshot clearly demonstrates the required functionality.
