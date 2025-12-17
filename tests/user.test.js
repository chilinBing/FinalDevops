const request = require('supertest');
const mongoose = require('mongoose');

// Mock environment variables
process.env.NODE_ENV = 'test';
process.env.MONGODB_URI = 'mongodb://admin:password123@localhost:27017/inventory-test?authSource=admin';
process.env.JWT_SECRET = 'test-secret-key';
process.env.SESSION_SECRET = 'test-session-secret';

const app = require('../server-enhanced');
const User = require('../models/User');

describe('User Management API Tests', () => {
  let adminToken;
  let userToken;
  let adminId;

  beforeAll(async () => {
    // Connect to test database
    if (mongoose.connection.readyState === 0) {
      try {
        await mongoose.connect(process.env.MONGODB_URI, {
          serverSelectionTimeoutMS: 5000, // 5 second timeout
        });
        console.log('Connected to MongoDB for testing');
      } catch (error) {
        console.error('MongoDB connection failed:', error.message);
        throw error;
      }
    }
  }, 10000); // 10 second timeout

  afterAll(async () => {
    // Clean up and close connection
    await User.deleteMany({});
    await mongoose.connection.close();
  });

  beforeEach(async () => {
    // Clear users before each test
    await User.deleteMany({});

    // Create admin user
    const admin = new User({
      username: 'admin',
      email: 'admin@example.com',
      password: 'admin123',
      role: 'admin'
    });
    await admin.save();
    
    const adminLogin = await request(app)
      .post('/api/auth/login')
      .send({
        username: 'admin',
        password: 'admin123'
      });
    adminToken = adminLogin.body.token;
    adminId = adminLogin.body.user.id;

    // Create regular user
    const userResponse = await request(app)
      .post('/api/auth/register')
      .send({
        username: 'user',
        email: 'user@example.com',
        password: 'user123'
      });
    userToken = userResponse.body.token;
  });

  describe('GET /api/users', () => {
    it('should get all users as admin', async () => {
      const response = await request(app)
        .get('/api/users')
        .set('Authorization', `Bearer ${adminToken}`);

      expect(response.status).toBe(200);
      expect(Array.isArray(response.body)).toBe(true);
      expect(response.body.length).toBeGreaterThanOrEqual(2);
    });

    it('should fail for non-admin users', async () => {
      const response = await request(app)
        .get('/api/users')
        .set('Authorization', `Bearer ${userToken}`);

      expect(response.status).toBe(403);
      expect(response.body).toHaveProperty('error');
    });

    it('should fail without authentication', async () => {
      const response = await request(app)
        .get('/api/users');

      expect(response.status).toBe(401);
    });
  });

  describe('GET /api/users/:id', () => {
    it('should get a specific user as admin', async () => {
      const users = await User.find({});
      const userId = users[0]._id;

      const response = await request(app)
        .get(`/api/users/${userId}`)
        .set('Authorization', `Bearer ${adminToken}`);

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('_id');
    });

    it('should return 404 for non-existent user', async () => {
      const fakeId = new mongoose.Types.ObjectId();
      const response = await request(app)
        .get(`/api/users/${fakeId}`)
        .set('Authorization', `Bearer ${adminToken}`);

      expect(response.status).toBe(404);
    });
  });

  describe('PUT /api/users/:id', () => {
    it('should update user as admin', async () => {
      const users = await User.find({ username: 'user' });
      const userId = users[0]._id;

      const response = await request(app)
        .put(`/api/users/${userId}`)
        .set('Authorization', `Bearer ${adminToken}`)
        .send({
          fullName: 'Updated Name',
          email: 'updated@example.com'
        });

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('fullName', 'Updated Name');
    });

    it('should fail for non-admin users', async () => {
      const users = await User.find({ username: 'admin' });
      const userId = users[0]._id;

      const response = await request(app)
        .put(`/api/users/${userId}`)
        .set('Authorization', `Bearer ${userToken}`)
        .send({ fullName: 'Hacker' });

      expect(response.status).toBe(403);
    });
  });

  describe('DELETE /api/users/:id', () => {
    it('should delete user as admin', async () => {
      const users = await User.find({ username: 'user' });
      const userId = users[0]._id;

      const response = await request(app)
        .delete(`/api/users/${userId}`)
        .set('Authorization', `Bearer ${adminToken}`);

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('message');

      // Verify user is deleted
      const deletedUser = await User.findById(userId);
      expect(deletedUser).toBeNull();
    });

    it('should fail for non-admin users', async () => {
      const response = await request(app)
        .delete(`/api/users/${adminId}`)
        .set('Authorization', `Bearer ${userToken}`);

      expect(response.status).toBe(403);
    });
  });

  describe('User Role Tests', () => {
    it('should create user with default role', async () => {
      const response = await request(app)
        .post('/api/auth/register')
        .send({
          username: 'newuser',
          email: 'newuser@example.com',
          password: 'password123'
        });

      expect(response.status).toBe(201);
      expect(response.body.user).toHaveProperty('role', 'user');
    });

    it('should verify admin role has elevated privileges', async () => {
      const response = await request(app)
        .get('/api/users')
        .set('Authorization', `Bearer ${adminToken}`);

      expect(response.status).toBe(200);
    });

    it('should verify user role has limited privileges', async () => {
      const response = await request(app)
        .get('/api/users')
        .set('Authorization', `Bearer ${userToken}`);

      expect(response.status).toBe(403);
    });
  });
});
