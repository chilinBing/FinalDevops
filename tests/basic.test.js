// Mock environment variables first
process.env.NODE_ENV = 'test';
process.env.JWT_SECRET = 'test-secret-key';
process.env.SESSION_SECRET = 'test-session-secret';

// Basic test to verify Jest is working
describe('Basic Tests', () => {
  it('should pass a simple test', () => {
    expect(1 + 1).toBe(2);
  });

  it('should verify environment variables', () => {
    expect(process.env.NODE_ENV).toBe('test');
  });

  it('should have required environment variables', () => {
    expect(process.env.JWT_SECRET).toBeDefined();
    expect(process.env.SESSION_SECRET).toBeDefined();
  });
});