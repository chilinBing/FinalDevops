const request = require('supertest');
const mongoose = require('mongoose');

// Mock environment variables
process.env.NODE_ENV = 'test';
process.env.MONGODB_URI = 'mongodb://localhost:27017/inventory-test';
process.env.JWT_SECRET = 'test-secret-key';
process.env.SESSION_SECRET = 'test-session-secret';

const app = require('../server-enhanced');
const User = require('../models/User');
const InventoryItem = require('../models/InventoryItem');

describe('Inventory API Tests', () => {
  let token;
  let userId;

  beforeAll(async () => {
    // Connect to test database
    if (mongoose.connection.readyState === 0) {
      await mongoose.connect(process.env.MONGODB_URI);
    }
  });

  afterAll(async () => {
    // Clean up and close connection
    await InventoryItem.deleteMany({});
    await User.deleteMany({});
    await mongoose.connection.close();
  });

  beforeEach(async () => {
    // Clear data before each test
    await InventoryItem.deleteMany({});
    await User.deleteMany({});

    // Create a test user and get token
    const response = await request(app)
      .post('/api/auth/register')
      .send({
        username: 'testuser',
        email: 'test@example.com',
        password: 'password123'
      });
    token = response.body.token;
    userId = response.body.user.id;
  });

  describe('GET /api/inventory', () => {
    it('should get all inventory items', async () => {
      // Create test items
      await InventoryItem.create([
        { name: 'Item 1', quantity: 10, price: 100, category: 'Electronics', createdBy: userId },
        { name: 'Item 2', quantity: 20, price: 200, category: 'Furniture', createdBy: userId }
      ]);

      const response = await request(app)
        .get('/api/inventory')
        .set('Authorization', `Bearer ${token}`);

      expect(response.status).toBe(200);
      expect(Array.isArray(response.body)).toBe(true);
      expect(response.body).toHaveLength(2);
    });

    it('should filter items by category', async () => {
      await InventoryItem.create([
        { name: 'Item 1', quantity: 10, price: 100, category: 'Electronics', createdBy: userId },
        { name: 'Item 2', quantity: 20, price: 200, category: 'Furniture', createdBy: userId }
      ]);

      const response = await request(app)
        .get('/api/inventory?category=Electronics')
        .set('Authorization', `Bearer ${token}`);

      expect(response.status).toBe(200);
      expect(response.body).toHaveLength(1);
      expect(response.body[0].category).toBe('Electronics');
    });

    it('should search items by name', async () => {
      await InventoryItem.create([
        { name: 'Laptop', quantity: 10, price: 1000, category: 'Electronics', createdBy: userId },
        { name: 'Chair', quantity: 20, price: 200, category: 'Furniture', createdBy: userId }
      ]);

      const response = await request(app)
        .get('/api/inventory?search=Laptop')
        .set('Authorization', `Bearer ${token}`);

      expect(response.status).toBe(200);
      expect(response.body).toHaveLength(1);
      expect(response.body[0].name).toBe('Laptop');
    });
  });

  describe('POST /api/inventory', () => {
    it('should create a new inventory item', async () => {
      const newItem = {
        name: 'Test Item',
        quantity: 50,
        price: 99.99,
        category: 'Electronics',
        sku: 'TEST-001',
        description: 'Test description'
      };

      const response = await request(app)
        .post('/api/inventory')
        .set('Authorization', `Bearer ${token}`)
        .send(newItem);

      expect(response.status).toBe(201);
      expect(response.body).toHaveProperty('name', 'Test Item');
      expect(response.body).toHaveProperty('quantity', 50);
    });

    it('should fail without authentication', async () => {
      const newItem = {
        name: 'Test Item',
        quantity: 50,
        price: 99.99
      };

      const response = await request(app)
        .post('/api/inventory')
        .send(newItem);

      expect(response.status).toBe(401);
    });

    it('should fail with missing required fields', async () => {
      const response = await request(app)
        .post('/api/inventory')
        .set('Authorization', `Bearer ${token}`)
        .send({ name: 'Test Item' });

      expect(response.status).toBe(400);
    });
  });

  describe('GET /api/inventory/:id', () => {
    it('should get a single inventory item', async () => {
      const item = await InventoryItem.create({
        name: 'Test Item',
        quantity: 10,
        price: 100,
        category: 'Electronics',
        createdBy: userId
      });

      const response = await request(app)
        .get(`/api/inventory/${item._id}`)
        .set('Authorization', `Bearer ${token}`);

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('name', 'Test Item');
    });

    it('should return 404 for non-existent item', async () => {
      const fakeId = new mongoose.Types.ObjectId();
      const response = await request(app)
        .get(`/api/inventory/${fakeId}`)
        .set('Authorization', `Bearer ${token}`);

      expect(response.status).toBe(404);
    });
  });

  describe('PUT /api/inventory/:id', () => {
    it('should update an inventory item', async () => {
      const item = await InventoryItem.create({
        name: 'Test Item',
        quantity: 10,
        price: 100,
        category: 'Electronics',
        createdBy: userId
      });

      const response = await request(app)
        .put(`/api/inventory/${item._id}`)
        .set('Authorization', `Bearer ${token}`)
        .send({ quantity: 20, price: 150 });

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('quantity', 20);
      expect(response.body).toHaveProperty('price', 150);
    });
  });

  describe('DELETE /api/inventory/:id', () => {
    it('should delete an inventory item', async () => {
      const item = await InventoryItem.create({
        name: 'Test Item',
        quantity: 10,
        price: 100,
        category: 'Electronics',
        createdBy: userId
      });

      const response = await request(app)
        .delete(`/api/inventory/${item._id}`)
        .set('Authorization', `Bearer ${token}`);

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('message');

      // Verify item is deleted
      const deletedItem = await InventoryItem.findById(item._id);
      expect(deletedItem).toBeNull();
    });
  });

  describe('GET /api/inventory/stats/summary', () => {
    it('should get inventory statistics', async () => {
      await InventoryItem.create([
        { name: 'Item 1', quantity: 10, price: 100, category: 'Electronics', createdBy: userId },
        { name: 'Item 2', quantity: 20, price: 200, category: 'Furniture', createdBy: userId },
        { name: 'Item 3', quantity: 5, price: 50, category: 'Electronics', createdBy: userId }
      ]);

      const response = await request(app)
        .get('/api/inventory/stats/summary')
        .set('Authorization', `Bearer ${token}`);

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('totalItems');
      expect(response.body).toHaveProperty('totalValue');
      expect(response.body).toHaveProperty('categories');
    });
  });
});
