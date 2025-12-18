# Selenium Test Configuration
import os
from dotenv import load_dotenv

load_dotenv()

class TestConfig:
    # Application URLs
    BASE_URL = os.getenv('BASE_URL', 'http://localhost')
    PRODUCTION_URL = os.getenv('PRODUCTION_URL', 'http://4.144.249.110')
    API_BASE_URL = f"{BASE_URL}/api"
    
    # Test Credentials
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    TEST_USER_USERNAME = os.getenv('TEST_USER_USERNAME', 'testuser')
    TEST_USER_PASSWORD = os.getenv('TEST_USER_PASSWORD', 'test123')
    TEST_USER_EMAIL = os.getenv('TEST_USER_EMAIL', 'test@example.com')
    
    # Browser Configuration
    BROWSER = os.getenv('BROWSER', 'chrome')  # chrome, firefox, edge
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
    
    # Test Data
    TEST_INVENTORY_ITEM = {
        'name': 'Test Laptop',
        'description': 'Selenium Test Item - Dell XPS 15',
        'quantity': '5',
        'price': '1299.99',
        'category': 'Electronics',
        'sku': 'TEST-LAPTOP-001'
    }
    
    # Timeouts
    SHORT_WAIT = 5
    MEDIUM_WAIT = 10
    LONG_WAIT = 20