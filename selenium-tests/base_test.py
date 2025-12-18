# Base Test Class for Selenium Tests
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config import TestConfig
import time
import requests

class BaseTest:
    def setup_method(self):
        """Setup method called before each test"""
        self.config = TestConfig()
        self.driver = self.get_driver()
        self.wait = WebDriverWait(self.driver, self.config.IMPLICIT_WAIT)
        
        # Set timeouts
        self.driver.implicitly_wait(self.config.IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(self.config.PAGE_LOAD_TIMEOUT)
        
        # Maximize window
        self.driver.maximize_window()
        
    def teardown_method(self):
        """Teardown method called after each test"""
        if hasattr(self, 'driver'):
            self.driver.quit()
    
    def get_driver(self):
        """Initialize and return WebDriver based on configuration"""
        browser = self.config.BROWSER.lower()
        
        if browser == 'chrome':
            options = webdriver.ChromeOptions()
            if self.config.HEADLESS:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            
            try:
                # Try with webdriver-manager first
                service = ChromeService(ChromeDriverManager().install())
                return webdriver.Chrome(service=service, options=options)
            except Exception as e:
                print(f"⚠️ WebDriver Manager failed: {e}")
                try:
                    # Try without service (use system PATH)
                    return webdriver.Chrome(options=options)
                except Exception as e2:
                    print(f"⚠️ System Chrome failed: {e2}")
                    raise Exception("Chrome WebDriver setup failed. Please install Chrome and ensure it's in PATH.")
            
        elif browser == 'firefox':
            options = webdriver.FirefoxOptions()
            if self.config.HEADLESS:
                options.add_argument('--headless')
            service = FirefoxService(GeckoDriverManager().install())
            return webdriver.Firefox(service=service, options=options)
            
        elif browser == 'edge':
            options = webdriver.EdgeOptions()
            if self.config.HEADLESS:
                options.add_argument('--headless')
            service = EdgeService(EdgeChromiumDriverManager().install())
            return webdriver.Edge(service=service, options=options)
            
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    def navigate_to(self, path=""):
        """Navigate to a specific path"""
        url = f"{self.config.BASE_URL}{path}"
        print(f"Navigating to: {url}")
        self.driver.get(url)
        time.sleep(2)  # Allow page to load
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present and visible"""
        if timeout is None:
            timeout = self.config.MEDIUM_WAIT
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def wait_for_clickable(self, locator, timeout=None):
        """Wait for element to be clickable"""
        if timeout is None:
            timeout = self.config.MEDIUM_WAIT
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    def safe_click(self, locator):
        """Safely click an element"""
        element = self.wait_for_clickable(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
        element.click()
    
    def safe_send_keys(self, locator, text):
        """Safely send keys to an element"""
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)
    
    def is_element_present(self, locator):
        """Check if element is present"""
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False
    
    def get_element_text(self, locator):
        """Get text from element"""
        element = self.wait_for_element(locator)
        return element.text
    
    def take_screenshot(self, name):
        """Take screenshot with given name"""
        timestamp = int(time.time())
        filename = f"screenshots/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"Screenshot saved: {filename}")
        return filename
    
    def check_api_health(self):
        """Check if API is healthy"""
        try:
            response = requests.get(f"{self.config.BASE_URL}/health", timeout=10)
            return response.status_code == 200 and response.json().get('status') == 'healthy'
        except:
            return False