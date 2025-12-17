// MongoDB initialization script
// This script runs when the MongoDB container starts for the first time

print('Starting MongoDB initialization...');

// Switch to the inventory database
db = db.getSiblingDB('inventory');

// Create a user for the inventory database
db.createUser({
  user: 'inventoryuser',
  pwd: 'inventorypass',
  roles: [
    {
      role: 'readWrite',
      db: 'inventory'
    }
  ]
});

print('Created inventory database user');

// Create collections with validation
db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['username', 'email', 'password'],
      properties: {
        username: {
          bsonType: 'string',
          description: 'Username must be a string and is required'
        },
        email: {
          bsonType: 'string',
          pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$',
          description: 'Email must be a valid email address'
        },
        password: {
          bsonType: 'string',
          description: 'Password must be a string and is required'
        },
        role: {
          enum: ['user', 'admin'],
          description: 'Role must be either user or admin'
        }
      }
    }
  }
});

db.createCollection('inventoryitems', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['name', 'quantity', 'price', 'category'],
      properties: {
        name: {
          bsonType: 'string',
          description: 'Name must be a string and is required'
        },
        quantity: {
          bsonType: 'number',
          minimum: 0,
          description: 'Quantity must be a non-negative number'
        },
        price: {
          bsonType: 'number',
          minimum: 0,
          description: 'Price must be a non-negative number'
        },
        category: {
          bsonType: 'string',
          description: 'Category must be a string and is required'
        }
      }
    }
  }
});

print('Created collections with validation');

// Create indexes for better performance
db.users.createIndex({ 'username': 1 }, { unique: true });
db.users.createIndex({ 'email': 1 }, { unique: true });
db.inventoryitems.createIndex({ 'name': 1 });
db.inventoryitems.createIndex({ 'category': 1 });
db.inventoryitems.createIndex({ 'sku': 1 }, { unique: true, sparse: true });
db.inventoryitems.createIndex({ 'createdAt': -1 });

print('Created indexes');

// Insert sample data
db.inventoryitems.insertMany([
  {
    name: 'Laptop Computer',
    description: 'High-performance laptop for development work',
    quantity: 15,
    price: 999.99,
    category: 'Electronics',
    sku: 'ELEC-LAP-001',
    supplier: 'Tech Supplies Inc',
    location: 'Warehouse A',
    minStockLevel: 5,
    createdAt: new Date(),
    updatedAt: new Date()
  },
  {
    name: 'Office Chair',
    description: 'Ergonomic office chair with lumbar support',
    quantity: 8,
    price: 299.99,
    category: 'Furniture',
    sku: 'FURN-CHR-001',
    supplier: 'Office Furniture Co',
    location: 'Warehouse B',
    minStockLevel: 3,
    createdAt: new Date(),
    updatedAt: new Date()
  },
  {
    name: 'Wireless Mouse',
    description: 'Bluetooth wireless mouse with precision tracking',
    quantity: 25,
    price: 49.99,
    category: 'Electronics',
    sku: 'ELEC-MOU-001',
    supplier: 'Tech Supplies Inc',
    location: 'Warehouse A',
    minStockLevel: 10,
    createdAt: new Date(),
    updatedAt: new Date()
  },
  {
    name: 'Programming Book',
    description: 'Complete guide to modern JavaScript development',
    quantity: 12,
    price: 39.99,
    category: 'Books',
    sku: 'BOOK-PRG-001',
    supplier: 'Book Distributors',
    location: 'Warehouse C',
    minStockLevel: 5,
    createdAt: new Date(),
    updatedAt: new Date()
  },
  {
    name: 'Desk Lamp',
    description: 'LED desk lamp with adjustable brightness',
    quantity: 20,
    price: 34.99,
    category: 'Electronics',
    sku: 'ELEC-LMP-001',
    supplier: 'Lighting Solutions',
    location: 'Warehouse A',
    minStockLevel: 8,
    createdAt: new Date(),
    updatedAt: new Date()
  }
]);

print('Inserted sample inventory data');

// Get collection stats
print('Database initialization completed!');
print('Collections created: ' + db.getCollectionNames().join(', '));
print('Sample items count: ' + db.inventoryitems.countDocuments());
print('Users collection ready for authentication');
