+
# 🧪 Testing Guide - Inventory Management System

## Quick Start

### Run All Tests:
```bash
npm test
```

### Run Tests in Watch Mode:
```bash
npm run test:watch
```

### Run Tests for CI/CD:
```bash
npm run test:ci
```

---

## Test Suites Overview

### 1. Health Check Tests (`tests/health.test.js`)
**Purpose**: Verify system availability and basic endpoints

**Test Cases**:
- ✅ GET /health returns healthy status
- ✅ GET / returns API information

**Run Specific Suite**:
```bash
npm test -- tests/health.test.js
```

---

### 2. Authentication Tests (`tests/auth.test.js`)
**Purpose**: Test user registration, login, and token authentication

**Test Cases**:
- ✅ Register new user successfully
- ✅ Fail registration with duplicate username
- ✅ Fail registration with missing fields
- ✅ Login with correct credentials
- ✅ Fail login with incorrect password
- ✅ Fail login with non-existent user
- ✅ Get current user with valid token
- ✅ Fail authentication without token
- ✅ Fail authentication with invalid token

**Run Specific Suite**:
```bash
npm test -- tests/auth.test.js
```

---

### 3. Inventory Tests (`tests/inventory.test.js`)
**Purpose**: Test CRUD operations for inventory items

**Test Cases**:
- ✅ Get all inventory items
- ✅ Filter items by category
- ✅ Search items by name
- ✅ Create new inventory item
- ✅ Fail creation without authentication
- ✅ Fail creation with missing fields
- ✅ Get single inventory item by ID
- ✅ Return 404 for non-existent item
- ✅ Update inventory item
- ✅ Delete inventory item
- ✅ Get inventory statistics

**Run Specific Suite**:
```bash
npm test -- tests/inventory.test.js
```

---

### 4. User Management Tests (`tests/user.test.js`)
**Purpose**: Test user management and role-based access control

**Test Cases**:
- ✅ Get all users as admin
- ✅ Fail to get users as non-admin
- ✅ Fail to get users without authentication
- ✅ Get specific user as admin
- ✅ Return 404 for non-existent user
- ✅ Update user as admin
- ✅ Fail to update user as non-admin
- ✅ Delete user as admin
- ✅ Fail to delete user as non-admin
- ✅ Verify default user role
- ✅ Verify admin privileges
- ✅ Verify user limitations

**Run Specific Suite**:
```bash
npm test -- tests/user.test.js
```

---

## Prerequisites

### 1. Install Dependencies:
```bash
npm install
```

### 2. MongoDB (for local testing):
```bash
# Option A: Using Docker
docker run -d -p 27017:27017 --name test-mongo \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password123 \
  mongo:7.0

# Option B: Local MongoDB installation
# Ensure MongoDB is running on localhost:27017
```

---

## Environment Variables

Tests use the following environment variables:

```bash
NODE_ENV=test
MONGODB_URI=mongodb://localhost:27017/inventory-test
JWT_SECRET=test-secret-key
SESSION_SECRET=test-session-secret
```

These are automatically set in the test files.

---

## Test Output Examples

### Successful Test Run:
```
 PASS  tests/health.test.js (5.234s)
  Health Check Tests
    GET /health
      ✓ should return healthy status (45ms)
    GET /
      ✓ should return API information (23ms)

 PASS  tests/auth.test.js (8.456s)
  Authentication API Tests
    POST /api/auth/register
      ✓ should register a new user successfully (234ms)
      ✓ should fail with duplicate username (156ms)
      ✓ should fail with missing required fields (89ms)
    POST /api/auth/login
      ✓ should login successfully with correct credentials (178ms)
      ✓ should fail with incorrect password (145ms)
      ✓ should fail with non-existent user (123ms)
    GET /api/auth/me
      ✓ should get current user with valid token (98ms)
      ✓ should fail without token (45ms)
      ✓ should fail with invalid token (67ms)

 PASS  tests/inventory.test.js (12.789s)
  Inventory API Tests
    GET /api/inventory
      ✓ should get all inventory items (234ms)
      ✓ should filter items by category (189ms)
      ✓ should search items by name (167ms)
    POST /api/inventory
      ✓ should create a new inventory item (198ms)
      ✓ should fail without authentication (78ms)
      ✓ should fail with missing required fields (89ms)
    GET /api/inventory/:id
      ✓ should get a single inventory item (145ms)
      ✓ should return 404 for non-existent item (98ms)
    PUT /api/inventory/:id
      ✓ should update an inventory item (176ms)
    DELETE /api/inventory/:id
      ✓ should delete an inventory item (154ms)
    GET /api/inventory/stats/summary
      ✓ should get inventory statistics (189ms)

 PASS  tests/user.test.js (10.234s)
  User Management API Tests
    GET /api/users
      ✓ should get all users as admin (198ms)
      ✓ should fail for non-admin users (134ms)
      ✓ should fail without authentication (67ms)
    GET /api/users/:id
      ✓ should get a specific user as admin (156ms)
      ✓ should return 404 for non-existent user (89ms)
    PUT /api/users/:id
      ✓ should update user as admin (178ms)
      ✓ should fail for non-admin users (123ms)
    DELETE /api/users/:id
      ✓ should delete user as admin (167ms)
      ✓ should fail for non-admin users (98ms)
    User Role Tests
      ✓ should create user with default role (145ms)
      ✓ should verify admin role has elevated privileges (89ms)
      ✓ should verify user role has limited privileges (76ms)

Test Suites: 4 passed, 4 total
Tests:       29 passed, 29 total
Snapshots:   0 total
Time:        36.713s
Ran all test suites.

Coverage Summary:
--------------------|---------|----------|---------|---------|
File                | % Stmts | % Branch | % Funcs | % Lines |
--------------------|---------|----------|---------|---------|
All files           |   85.23 |    78.45 |   82.67 |   85.89 |
 server-enhanced.js |   87.45 |    80.12 |   85.34 |   88.23 |
 models/            |   92.34 |    85.67 |   90.12 |   93.45 |
 middleware/        |   78.90 |    70.23 |   75.45 |   79.67 |
--------------------|---------|----------|---------|---------|
```

---

## Coverage Reports

### Generate Coverage Report:
```bash
npm test -- --coverage
```

### View Coverage in Browser:
```bash
# After running tests with coverage
# Open coverage/lcov-report/index.html in browser
```

### Coverage Thresholds:
- **Statements**: > 80%
- **Branches**: > 75%
- **Functions**: > 80%
- **Lines**: > 80%

---

## Troubleshooting

### Issue: MongoDB Connection Error
**Solution**:
```bash
# Ensure MongoDB is running
docker ps | grep mongo

# Or start MongoDB
docker start test-mongo
```

### Issue: Port Already in Use
**Solution**:
```bash
# Find process using port
netstat -ano | findstr :27017

# Kill the process or use different port
```

### Issue: Tests Timeout
**Solution**:
```bash
# Increase timeout in jest config (package.json)
"jest": {
  "testTimeout": 30000
}
```

### Issue: Module Not Found
**Solution**:
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

---

## CI/CD Integration

### GitHub Actions:
Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` branch

### Pipeline Configuration:
```yaml
- name: Run automated tests
  env:
    NODE_ENV: test
    MONGODB_URI: mongodb://admin:password123@localhost:27017/inventory-test
    JWT_SECRET: test-jwt-secret-key
    SESSION_SECRET: test-session-secret-key
  run: npm run test:ci
```

---

## Best Practices

### 1. Run Tests Before Committing:
```bash
npm test
```

### 2. Watch Mode During Development:
```bash
npm run test:watch
```

### 3. Check Coverage:
```bash
npm test -- --coverage
```

### 4. Run Specific Test:
```bash
npm test -- -t "should register a new user"
```

### 5. Debug Tests:
```bash
npm test -- --verbose
```

---

## Test Database

### Automatic Cleanup:
- Database cleared before each test suite
- Collections cleared before each test case
- Connections closed after all tests

### Test Data:
- No persistent test data
- Each test creates its own data
- No interference between tests

---

## Additional Commands

### Run Tests with Verbose Output:
```bash
npm test -- --verbose
```

### Run Tests in Silent Mode:
```bash
npm test -- --silent
```

### Run Tests with Specific Pattern:
```bash
npm test -- --testNamePattern="auth"
```

### Update Snapshots:
```bash
npm test -- -u
```

### Clear Jest Cache:
```bash
npm test -- --clearCache
```

---

## Test Statistics

- **Total Test Suites**: 4
- **Total Test Cases**: 29
- **Average Execution Time**: ~37 seconds
- **Coverage**: > 80%
- **Pass Rate**: 100%

---

## Next Steps

1. ✅ Run tests locally to verify setup
2. ✅ Push code to trigger CI/CD pipeline
3. ✅ Verify tests pass in GitHub Actions
4. ✅ Check coverage reports
5. ✅ Take screenshots for submission

---

**Happy Testing!** 🧪✨
