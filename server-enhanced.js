const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config();

const User = require('./models/User');
const InventoryItem = require('./models/InventoryItem');
const { authenticate, isAdmin, generateToken } = require('./middleware/auth');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

// MongoDB Connection
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/inventory';

const mongoOptions = {
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000,
};

const connectDB = async () => {
  try {
    await mongoose.connect(MONGODB_URI, mongoOptions);
    console.log('✅ Connected to MongoDB successfully');
    console.log(`📍 Database: ${mongoose.connection.name}`);
    console.log(`🔗 Host: ${mongoose.connection.host}:${mongoose.connection.port}`);
    
    // Create default admin user if none exists
    const adminExists = await User.findOne({ role: 'admin' });
    if (!adminExists) {
      const admin = new User({
        username: 'admin',
        email: 'admin@inventory.com',
        password: 'admin123',
        role: 'admin'
      });
      await admin.save();
      console.log('👤 Default admin user created (username: admin, password: admin123)');
    }
  } catch (error) {
    console.error('❌ MongoDB connection error:', error.message);
    console.log('🔄 Retrying connection in 5 seconds...');
    setTimeout(connectDB, 5000);
  }
};

mongoose.connection.on('connected', () => {
  console.log('🟢 Mongoose connected to MongoDB');
});

mongoose.connection.on('error', (err) => {
  console.error('🔴 Mongoose connection error:', err);
});

mongoose.connection.on('disconnected', () => {
  console.log('🟡 Mongoose disconnected from MongoDB');
});

process.on('SIGINT', async () => {
  await mongoose.connection.close();
  console.log('🔴 MongoDB connection closed through app termination');
  process.exit(0);
});

connectDB();

// ==================== AUTHENTICATION ROUTES ====================

// Register new user
app.post('/api/auth/register', async (req, res) => {
  try {
    const { username, email, password } = req.body;
    
    // Validation
    if (!username || !email || !password) {
      return res.status(400).json({ error: 'All fields are required' });
    }
    
    // Check if user already exists
    const existingUser = await User.findOne({ $or: [{ email }, { username }] });
    if (existingUser) {
      return res.status(400).json({ error: 'User already exists' });
    }
    
    // Create new user
    const user = new User({ username, email, password });
    await user.save();
    
    // Generate token
    const token = generateToken(user._id);
    
    res.status(201).json({
      message: 'User registered successfully',
      token,
      user: {
        id: user._id,
        username: user.username,
        email: user.email,
        role: user.role
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Login user
app.post('/api/auth/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    
    // Validation
    if (!username || !password) {
      return res.status(400).json({ error: 'Username and password are required' });
    }
    
    // Find user
    const user = await User.findOne({ username });
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    // Check password
    const isMatch = await user.comparePassword(password);
    if (!isMatch) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    // Generate token
    const token = generateToken(user._id);
    
    res.json({
      message: 'Login successful',
      token,
      user: {
        id: user._id,
        username: user.username,
        email: user.email,
        role: user.role
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get current user
app.get('/api/auth/me', authenticate, async (req, res) => {
  res.json({
    user: {
      id: req.user._id,
      username: req.user.username,
      email: req.user.email,
      role: req.user.role
    }
  });
});

// ==================== USER MANAGEMENT ROUTES (Admin Only) ====================

// Get all users
app.get('/api/users', authenticate, isAdmin, async (req, res) => {
  try {
    const users = await User.find().select('-password');
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Delete user
app.delete('/api/users/:id', authenticate, isAdmin, async (req, res) => {
  try {
    const user = await User.findByIdAndDelete(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json({ message: 'User deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ==================== INVENTORY ROUTES ====================

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    database: mongoose.connection.readyState === 1 ? 'Connected' : 'Disconnected'
  });
});

// Get all inventory items (requires authentication)
app.get('/api/inventory', authenticate, async (req, res) => {
  try {
    const { category, search, lowStock } = req.query;
    let query = {};
    
    if (category) {
      query.category = category;
    }
    
    if (search) {
      query.$or = [
        { name: { $regex: search, $options: 'i' } },
        { description: { $regex: search, $options: 'i' } }
      ];
    }
    
    if (lowStock === 'true') {
      query.$expr = { $lt: ['$quantity', '$minStockLevel'] };
    }
    
    const items = await InventoryItem.find(query)
      .populate('createdBy', 'username')
      .populate('updatedBy', 'username')
      .sort({ createdAt: -1 });
    
    res.json(items);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get single inventory item
app.get('/api/inventory/:id', authenticate, async (req, res) => {
  try {
    const item = await InventoryItem.findById(req.params.id)
      .populate('createdBy', 'username')
      .populate('updatedBy', 'username');
    
    if (!item) {
      return res.status(404).json({ error: 'Item not found' });
    }
    res.json(item);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Create new inventory item
app.post('/api/inventory', authenticate, async (req, res) => {
  try {
    const itemData = {
      ...req.body,
      createdBy: req.user._id,
      updatedBy: req.user._id
    };
    
    const newItem = new InventoryItem(itemData);
    const savedItem = await newItem.save();
    
    const populatedItem = await InventoryItem.findById(savedItem._id)
      .populate('createdBy', 'username')
      .populate('updatedBy', 'username');
    
    res.status(201).json(populatedItem);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Update inventory item
app.put('/api/inventory/:id', authenticate, async (req, res) => {
  try {
    const updateData = {
      ...req.body,
      updatedBy: req.user._id,
      updatedAt: Date.now()
    };
    
    const updatedItem = await InventoryItem.findByIdAndUpdate(
      req.params.id,
      updateData,
      { new: true, runValidators: true }
    ).populate('createdBy', 'username')
     .populate('updatedBy', 'username');
    
    if (!updatedItem) {
      return res.status(404).json({ error: 'Item not found' });
    }
    res.json(updatedItem);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Delete inventory item
app.delete('/api/inventory/:id', authenticate, async (req, res) => {
  try {
    const deletedItem = await InventoryItem.findByIdAndDelete(req.params.id);
    if (!deletedItem) {
      return res.status(404).json({ error: 'Item not found' });
    }
    res.json({ message: 'Item deleted successfully', item: deletedItem });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get inventory statistics
app.get('/api/inventory/stats/summary', authenticate, async (req, res) => {
  try {
    const totalItems = await InventoryItem.countDocuments();
    const lowStockItems = await InventoryItem.countDocuments({
      $expr: { $lt: ['$quantity', '$minStockLevel'] }
    });
    
    const totalValue = await InventoryItem.aggregate([
      {
        $group: {
          _id: null,
          total: { $sum: { $multiply: ['$quantity', '$price'] } }
        }
      }
    ]);
    
    const categories = await InventoryItem.distinct('category');
    
    res.json({
      totalItems,
      lowStockItems,
      totalValue: totalValue[0]?.total || 0,
      categories: categories.length
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Start server only if not in test mode
if (process.env.NODE_ENV !== 'test') {
  app.listen(PORT, () => {
    console.log(`✅ Server running on port ${PORT}`);
    console.log(`🌐 Application: http://localhost:${PORT}`);
    console.log(`🔗 API: http://localhost:${PORT}/api`);
    console.log(`📊 Environment: ${process.env.NODE_ENV || 'development'}`);
  });
}

// Export app for testing
module.exports = app;
