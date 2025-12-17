const request = require('supertest');

// Mock environment variables
process.env.NODE_ENV = 'test';
process.env.MONGODB_URI = 'mongodb://localhost:27017/inventory-test';
process.env.JWT_SECRET = 'test-secret-key';
process.env.SESSION_SECRET = 'test-session-secret';

const app = require('../server-enhanced');

describe('Health Check Tests', () => {
  describe('GET /health', () => {
    it('should return healthy status', async () => {
      const response = await request(app).get('/health');

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('status', 'healthy');
      expect(response.body).toHaveProperty('timestamp');
    });
  });

  describe('GET /', () => {
    it('should return API information', async () => {
      const response = await request(app).get('/');

      expect(response.status).toBe(200);
    });
  });
});
