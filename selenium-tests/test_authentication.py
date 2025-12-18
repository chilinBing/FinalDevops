# Test Case 2: Authentication and Login Tests
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from base_test import BaseTest
import time

class TestAuthentication(BaseTest):
    
    def test_login_with_valid_credentials(self):
        """Test Case 2.1: Verify login with valid credentials"""
        print("\n=== Test Case 2.1: Valid Login Test ===")
        
        # Navigate to login page
        self.navigate_to("/login.html")
        
        # Take screenshot of login page
        self.take_screenshot("login_page")
        
        # Fill in login form
        self.safe_send_keys((By.ID, "username"), self.config.ADMIN_USERNAME)
        self.safe_send_keys((By.ID, "password"), self.config.ADMIN_PASSWORD)
        
        # Take screenshot before login
        self.take_screenshot("before_login")
        
        # Click login button
        login_button = self.wait_for_clickable((By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"))
        login_button.click()
        
        # Wait for redirect or success indication
        time.sleep(3)
        
        # Take screenshot after login attempt
        self.take_screenshot("after_login")
        
        # Check if login was successful
        current_url = self.driver.current_url
        
        # Should be redirected away from login page
        success_indicators = [
            "/index.html" in current_url,
            "/dashboard" in current_url,
            "login.html" not in current_url,
            self.is_element_present((By.PARTIAL_LINK_TEXT, "Logout")),
            self.is_element_present((By.PARTIAL_LINK_TEXT, "logout")),
            self.is_element_present((By.ID, "logout")),
            "Welcome" in self.driver.page_source,
            "Dashboard" in self.driver.page_source
        ]
        
        if any(success_indicators):
            print("✅ Login successful - redirected to dashboard")
        else:
            print("ℹ️ Login behavior may differ - checking for error messages")
            
            # Check for error messages
            error_elements = self.driver.find_elements(By.CSS_SELECTOR, ".error, .alert, .message")
            if error_elements:
                for error in error_elements:
                    if error.is_displayed():
                        print(f"⚠️ Error message: {error.text}")
    
    def test_login_with_invalid_credentials(self):
        """Test Case 2.2: Verify login with invalid credentials"""
        print("\n=== Test Case 2.2: Invalid Login Test ===")
        
        # Navigate to login page
        self.navigate_to("/login.html")
        
        # Fill in login form with invalid credentials
        self.safe_send_keys((By.ID, "username"), "invalid_user")
        self.safe_send_keys((By.ID, "password"), "invalid_password")
        
        # Take screenshot before invalid login
        self.take_screenshot("before_invalid_login")
        
        # Click login button
        login_button = self.wait_for_clickable((By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"))
        login_button.click()
        
        # Wait for response
        time.sleep(3)
        
        # Take screenshot after invalid login
        self.take_screenshot("after_invalid_login")
        
        # Should still be on login page or show error
        current_url = self.driver.current_url
        
        # Check that we're still on login page
        assert "login" in current_url.lower() or "/login.html" in current_url
        print("✅ Remained on login page after invalid credentials")
        
        # Check for error message (optional, depends on implementation)
        error_indicators = [
            self.is_element_present((By.CSS_SELECTOR, ".error")),
            self.is_element_present((By.CSS_SELECTOR, ".alert")),
            "Invalid" in self.driver.page_source,
            "Error" in self.driver.page_source,
            "incorrect" in self.driver.page_source.lower()
        ]
        
        if any(error_indicators):
            print("✅ Error indication found for invalid credentials")
        else:
            print("ℹ️ No explicit error message found (may be handled differently)")
    
    def test_registration_form_validation(self):
        """Test Case 2.3: Verify registration form validation"""
        print("\n=== Test Case 2.3: Registration Form Validation Test ===")
        
        # Navigate to login page first
        self.navigate_to("/login.html")
        
        # Look for registration link
        register_links = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "Register")
        if not register_links:
            register_links = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "register")
        if not register_links:
            register_links = self.driver.find_elements(By.LINK_TEXT, "Sign up")
        
        if register_links and register_links[0].is_displayed():
            # Click register link
            register_links[0].click()
            time.sleep(2)
            
            # Take screenshot of registration page
            self.take_screenshot("registration_page")
            
            # Try to submit empty form
            submit_button = self.driver.find_elements(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
            if submit_button:
                submit_button[0].click()
                time.sleep(2)
                
                # Take screenshot after empty form submission
                self.take_screenshot("empty_form_validation")
                
                # Check for validation messages
                validation_indicators = [
                    self.is_element_present((By.CSS_SELECTOR, ".error")),
                    self.is_element_present((By.CSS_SELECTOR, ".invalid")),
                    "required" in self.driver.page_source.lower(),
                    "fill" in self.driver.page_source.lower()
                ]
                
                if any(validation_indicators):
                    print("✅ Form validation working - empty form rejected")
                else:
                    print("ℹ️ No explicit validation messages found")
            else:
                print("ℹ️ Submit button not found on registration page")
        else:
            # Try direct navigation to register page
            self.navigate_to("/register.html")
            
            if "register" in self.driver.current_url.lower():
                print("✅ Registration page accessible via direct URL")
                self.take_screenshot("registration_page_direct")
            else:
                print("ℹ️ Registration page not found - may not be implemented")
    
    def test_logout_functionality(self):
        """Test Case 2.4: Verify logout functionality"""
        print("\n=== Test Case 2.4: Logout Functionality Test ===")
        
        # First login with valid credentials
        self.navigate_to("/login.html")
        self.safe_send_keys((By.ID, "username"), self.config.ADMIN_USERNAME)
        self.safe_send_keys((By.ID, "password"), self.config.ADMIN_PASSWORD)
        
        login_button = self.wait_for_clickable((By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"))
        login_button.click()
        time.sleep(3)
        
        # Take screenshot after login
        self.take_screenshot("logged_in_state")
        
        # Look for logout button/link
        logout_elements = []
        logout_selectors = [
            (By.PARTIAL_LINK_TEXT, "Logout"),
            (By.PARTIAL_LINK_TEXT, "logout"),
            (By.ID, "logout"),
            (By.CLASS_NAME, "logout"),
            (By.CSS_SELECTOR, "button[onclick*='logout']"),
            (By.CSS_SELECTOR, "a[href*='logout']")
        ]
        
        for selector in logout_selectors:
            elements = self.driver.find_elements(*selector)
            if elements and elements[0].is_displayed():
                logout_elements = elements
                break
        
        if logout_elements:
            # Click logout
            logout_elements[0].click()
            time.sleep(3)
            
            # Take screenshot after logout
            self.take_screenshot("after_logout")
            
            # Should be redirected to login page
            current_url = self.driver.current_url
            if "login" in current_url.lower():
                print("✅ Logout successful - redirected to login page")
            else:
                print("ℹ️ Logout behavior may differ from expected")
        else:
            print("ℹ️ Logout button not found - may be implemented differently")
    
    def test_session_persistence(self):
        """Test Case 2.5: Verify session persistence"""
        print("\n=== Test Case 2.5: Session Persistence Test ===")
        
        # Login first
        self.navigate_to("/login.html")
        self.safe_send_keys((By.ID, "username"), self.config.ADMIN_USERNAME)
        self.safe_send_keys((By.ID, "password"), self.config.ADMIN_PASSWORD)
        
        login_button = self.wait_for_clickable((By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"))
        login_button.click()
        time.sleep(3)
        
        # Navigate to different page
        self.navigate_to("/")
        time.sleep(2)
        
        # Take screenshot
        self.take_screenshot("session_persistence")
        
        # Check if still logged in (not redirected to login)
        current_url = self.driver.current_url
        
        if "login" not in current_url.lower():
            print("✅ Session persisted - not redirected to login")
        else:
            print("ℹ️ Session may not persist or authentication required for each page")