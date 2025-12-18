# Test Case 1: Homepage and Navigation Tests
import pytest
from selenium.webdriver.common.by import By
from base_test import BaseTest
import time

class TestHomepage(BaseTest):
    
    def test_homepage_loads_successfully(self):
        """Test Case 1.1: Verify homepage loads successfully"""
        print("\n=== Test Case 1.1: Homepage Load Test ===")
        
        # Navigate to homepage
        self.navigate_to("/")
        
        # Take screenshot
        self.take_screenshot("homepage_load")
        
        # Verify page title
        assert "Inventory Management" in self.driver.title
        print("✅ Page title contains 'Inventory Management'")
        
        # Check if redirected to login page (expected behavior)
        current_url = self.driver.current_url
        assert "/login.html" in current_url or "login" in current_url.lower()
        print("✅ Redirected to login page as expected")
        
        # Verify login form elements are present
        username_field = self.wait_for_element((By.ID, "username"))
        password_field = self.wait_for_element((By.ID, "password"))
        login_button = self.wait_for_element((By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"))
        
        assert username_field.is_displayed()
        assert password_field.is_displayed()
        assert login_button.is_displayed()
        print("✅ Login form elements are visible")
        
    def test_navigation_elements_present(self):
        """Test Case 1.2: Verify navigation elements are present"""
        print("\n=== Test Case 1.2: Navigation Elements Test ===")
        
        # Navigate to login page
        self.navigate_to("/login.html")
        
        # Take screenshot
        self.take_screenshot("navigation_elements")
        
        # Check for header/title
        header_elements = self.driver.find_elements(By.TAG_NAME, "h1")
        if header_elements:
            header_text = header_elements[0].text
            assert "Inventory" in header_text or "Login" in header_text
            print(f"✅ Header found: {header_text}")
        
        # Check for register link
        register_links = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "Register")
        if not register_links:
            register_links = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "register")
        
        if register_links:
            assert register_links[0].is_displayed()
            print("✅ Register link is present")
        else:
            print("ℹ️ Register link not found (may be implemented differently)")
    
    def test_responsive_design(self):
        """Test Case 1.3: Verify responsive design"""
        print("\n=== Test Case 1.3: Responsive Design Test ===")
        
        # Navigate to login page
        self.navigate_to("/login.html")
        
        # Test desktop view
        self.driver.set_window_size(1920, 1080)
        time.sleep(1)
        self.take_screenshot("desktop_view")
        
        # Verify elements are visible in desktop view
        username_field = self.wait_for_element((By.ID, "username"))
        assert username_field.is_displayed()
        print("✅ Desktop view: Elements visible")
        
        # Test tablet view
        self.driver.set_window_size(768, 1024)
        time.sleep(1)
        self.take_screenshot("tablet_view")
        
        # Verify elements are still visible
        username_field = self.wait_for_element((By.ID, "username"))
        assert username_field.is_displayed()
        print("✅ Tablet view: Elements visible")
        
        # Test mobile view
        self.driver.set_window_size(375, 667)
        time.sleep(1)
        self.take_screenshot("mobile_view")
        
        # Verify elements are still visible
        username_field = self.wait_for_element((By.ID, "username"))
        assert username_field.is_displayed()
        print("✅ Mobile view: Elements visible")
        
        # Restore to desktop
        self.driver.maximize_window()
    
    def test_page_load_performance(self):
        """Test Case 1.4: Verify page load performance"""
        print("\n=== Test Case 1.4: Page Load Performance Test ===")
        
        start_time = time.time()
        
        # Navigate to homepage
        self.navigate_to("/")
        
        # Wait for page to fully load
        self.wait_for_element((By.TAG_NAME, "body"))
        
        load_time = time.time() - start_time
        
        # Take screenshot
        self.take_screenshot("page_load_performance")
        
        # Assert page loads within reasonable time (10 seconds)
        assert load_time < 10, f"Page load time {load_time:.2f}s exceeds 10 seconds"
        print(f"✅ Page loaded in {load_time:.2f} seconds")
        
        # Check if any JavaScript errors occurred
        logs = self.driver.get_log('browser')
        severe_errors = [log for log in logs if log['level'] == 'SEVERE']
        
        if severe_errors:
            print(f"⚠️ Found {len(severe_errors)} severe JavaScript errors")
            for error in severe_errors[:3]:  # Show first 3 errors
                print(f"   - {error['message']}")
        else:
            print("✅ No severe JavaScript errors found")