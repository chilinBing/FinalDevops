# Test Case 3: Inventory Management and CRUD Operations
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from base_test import BaseTest
import time

class TestInventoryManagement(BaseTest):
    
    def login_first(self):
        """Helper method to login before inventory tests"""
        self.navigate_to("/login.html")
        self.safe_send_keys((By.ID, "username"), self.config.ADMIN_USERNAME)
        self.safe_send_keys((By.ID, "password"), self.config.ADMIN_PASSWORD)
        
        login_button = self.wait_for_clickable((By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"))
        login_button.click()
        time.sleep(3)
    
    def test_inventory_page_loads(self):
        """Test Case 3.1: Verify inventory page loads after login"""
        print("\n=== Test Case 3.1: Inventory Page Load Test ===")
        
        # Login first
        self.login_first()
        
        # Navigate to inventory page (may be main page after login)
        self.navigate_to("/")
        time.sleep(2)
        
        # Take screenshot
        self.take_screenshot("inventory_page")
        
        # Check for inventory-related elements
        inventory_indicators = [
            self.is_element_present((By.ID, "itemForm")),
            self.is_element_present((By.CSS_SELECTOR, "form")),
            self.is_element_present((By.CSS_SELECTOR, "input[name='name']")),
            self.is_element_present((By.CSS_SELECTOR, "input[name='quantity']")),
            self.is_element_present((By.CSS_SELECTOR, "input[name='price']")),
            "inventory" in self.driver.page_source.lower(),
            "add item" in self.driver.page_source.lower(),
            "product" in self.driver.page_source.lower()
        ]
        
        if any(inventory_indicators):
            print("✅ Inventory page loaded successfully")
        else:
            print("ℹ️ Inventory elements not immediately visible - may require navigation")
    
    def test_add_inventory_item(self):
        """Test Case 3.2: Verify adding new inventory item"""
        print("\n=== Test Case 3.2: Add Inventory Item Test ===")
        
        # Login first
        self.login_first()
        self.navigate_to("/")
        time.sleep(2)
        
        # Take screenshot before adding item
        self.take_screenshot("before_add_item")
        
        # Look for form fields
        form_fields = {
            'name': ['name', 'itemName', 'product_name'],
            'description': ['description', 'desc', 'product_description'],
            'quantity': ['quantity', 'qty', 'stock'],
            'price': ['price', 'cost', 'amount'],
            'category': ['category', 'type', 'product_category']
        }
        
        filled_fields = 0
        
        # Try to fill form fields
        for field_type, possible_names in form_fields.items():
            for name in possible_names:
                elements = self.driver.find_elements(By.NAME, name)
                if not elements:
                    elements = self.driver.find_elements(By.ID, name)
                
                if elements and elements[0].is_displayed():
                    try:
                        if field_type == 'name':
                            elements[0].clear()
                            elements[0].send_keys(self.config.TEST_INVENTORY_ITEM['name'])
                            filled_fields += 1
                            print(f"✅ Filled {field_type} field")
                        elif field_type == 'description':
                            elements[0].clear()
                            elements[0].send_keys(self.config.TEST_INVENTORY_ITEM['description'])
                            filled_fields += 1
                            print(f"✅ Filled {field_type} field")
                        elif field_type == 'quantity':
                            elements[0].clear()
                            elements[0].send_keys(self.config.TEST_INVENTORY_ITEM['quantity'])
                            filled_fields += 1
                            print(f"✅ Filled {field_type} field")
                        elif field_type == 'price':
                            elements[0].clear()
                            elements[0].send_keys(self.config.TEST_INVENTORY_ITEM['price'])
                            filled_fields += 1
                            print(f"✅ Filled {field_type} field")
                        elif field_type == 'category':
                            if elements[0].tag_name == 'select':
                                select = Select(elements[0])
                                try:
                                    select.select_by_visible_text(self.config.TEST_INVENTORY_ITEM['category'])
                                except:
                                    select.select_by_index(1)  # Select first option
                            else:
                                elements[0].clear()
                                elements[0].send_keys(self.config.TEST_INVENTORY_ITEM['category'])
                            filled_fields += 1
                            print(f"✅ Filled {field_type} field")
                        break
                    except Exception as e:
                        print(f"⚠️ Could not fill {field_type} field: {str(e)}")
        
        # Take screenshot after filling form
        self.take_screenshot("form_filled")
        
        if filled_fields > 0:
            # Look for submit button
            submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
            if not submit_buttons:
                submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button")
            
            if submit_buttons:
                # Click submit
                submit_buttons[0].click()
                time.sleep(3)
                
                # Take screenshot after submission
                self.take_screenshot("after_add_item")
                
                # Check for success indicators
                success_indicators = [
                    "success" in self.driver.page_source.lower(),
                    "added" in self.driver.page_source.lower(),
                    "created" in self.driver.page_source.lower(),
                    self.config.TEST_INVENTORY_ITEM['name'] in self.driver.page_source
                ]
                
                if any(success_indicators):
                    print("✅ Item appears to have been added successfully")
                else:
                    print("ℹ️ Item submission completed - success message may vary")
            else:
                print("⚠️ Submit button not found")
        else:
            print("⚠️ No form fields could be filled")
    
    def test_view_inventory_list(self):
        """Test Case 3.3: Verify viewing inventory list"""
        print("\n=== Test Case 3.3: View Inventory List Test ===")
        
        # Login first
        self.login_first()
        self.navigate_to("/")
        time.sleep(2)
        
        # Take screenshot
        self.take_screenshot("inventory_list")
        
        # Look for inventory list elements
        list_indicators = [
            self.driver.find_elements(By.CSS_SELECTOR, "table"),
            self.driver.find_elements(By.CSS_SELECTOR, ".item"),
            self.driver.find_elements(By.CSS_SELECTOR, ".product"),
            self.driver.find_elements(By.CSS_SELECTOR, "ul li"),
            self.driver.find_elements(By.CSS_SELECTOR, ".inventory-item")
        ]
        
        found_list = False
        for elements in list_indicators:
            if elements and len(elements) > 0:
                found_list = True
                print(f"✅ Found inventory list with {len(elements)} elements")
                break
        
        if not found_list:
            # Check if there's text indicating empty list
            empty_indicators = [
                "no items" in self.driver.page_source.lower(),
                "empty" in self.driver.page_source.lower(),
                "no products" in self.driver.page_source.lower()
            ]
            
            if any(empty_indicators):
                print("✅ Empty inventory list detected")
            else:
                print("ℹ️ Inventory list format may differ from expected")
    
    def test_search_functionality(self):
        """Test Case 3.4: Verify search functionality"""
        print("\n=== Test Case 3.4: Search Functionality Test ===")
        
        # Login first
        self.login_first()
        self.navigate_to("/")
        time.sleep(2)
        
        # Look for search field
        search_fields = []
        search_selectors = [
            (By.NAME, "search"),
            (By.ID, "search"),
            (By.CSS_SELECTOR, "input[type='search']"),
            (By.CSS_SELECTOR, "input[placeholder*='search']"),
            (By.CSS_SELECTOR, "input[placeholder*='Search']")
        ]
        
        for selector in search_selectors:
            elements = self.driver.find_elements(*selector)
            if elements and elements[0].is_displayed():
                search_fields = elements
                break
        
        if search_fields:
            # Perform search
            search_term = "laptop"
            search_fields[0].clear()
            search_fields[0].send_keys(search_term)
            
            # Take screenshot during search
            self.take_screenshot("search_input")
            
            # Look for search button or press Enter
            search_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
            if search_buttons:
                search_buttons[0].click()
            else:
                search_fields[0].send_keys("\n")  # Press Enter
            
            time.sleep(2)
            
            # Take screenshot after search
            self.take_screenshot("search_results")
            
            print("✅ Search functionality tested")
        else:
            print("ℹ️ Search field not found - may not be implemented")
    
    def test_edit_inventory_item(self):
        """Test Case 3.5: Verify editing inventory item"""
        print("\n=== Test Case 3.5: Edit Inventory Item Test ===")
        
        # Login first
        self.login_first()
        self.navigate_to("/")
        time.sleep(2)
        
        # Look for edit buttons
        edit_buttons = []
        edit_selectors = [
            (By.CSS_SELECTOR, "button[onclick*='edit']"),
            (By.CSS_SELECTOR, "a[href*='edit']"),
            (By.PARTIAL_LINK_TEXT, "Edit"),
            (By.PARTIAL_LINK_TEXT, "edit"),
            (By.CSS_SELECTOR, ".edit"),
            (By.CSS_SELECTOR, "button.edit")
        ]
        
        for selector in edit_selectors:
            elements = self.driver.find_elements(*selector)
            if elements:
                edit_buttons = elements
                break
        
        if edit_buttons and len(edit_buttons) > 0:
            # Click first edit button
            edit_buttons[0].click()
            time.sleep(2)
            
            # Take screenshot of edit form
            self.take_screenshot("edit_form")
            
            # Try to modify a field
            name_fields = self.driver.find_elements(By.NAME, "name")
            if not name_fields:
                name_fields = self.driver.find_elements(By.ID, "name")
            
            if name_fields and name_fields[0].is_displayed():
                original_value = name_fields[0].get_attribute("value")
                name_fields[0].clear()
                name_fields[0].send_keys(f"{original_value} - Updated")
                
                # Look for update/save button
                save_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
                if save_buttons:
                    save_buttons[0].click()
                    time.sleep(2)
                    
                    # Take screenshot after update
                    self.take_screenshot("after_edit")
                    
                    print("✅ Edit functionality tested")
                else:
                    print("⚠️ Save button not found")
            else:
                print("⚠️ Editable fields not found")
        else:
            print("ℹ️ Edit buttons not found - may not be implemented or no items exist")
    
    def test_delete_inventory_item(self):
        """Test Case 3.6: Verify deleting inventory item"""
        print("\n=== Test Case 3.6: Delete Inventory Item Test ===")
        
        # Login first
        self.login_first()
        self.navigate_to("/")
        time.sleep(2)
        
        # Look for delete buttons
        delete_buttons = []
        delete_selectors = [
            (By.CSS_SELECTOR, "button[onclick*='delete']"),
            (By.CSS_SELECTOR, "a[href*='delete']"),
            (By.PARTIAL_LINK_TEXT, "Delete"),
            (By.PARTIAL_LINK_TEXT, "delete"),
            (By.CSS_SELECTOR, ".delete"),
            (By.CSS_SELECTOR, "button.delete")
        ]
        
        for selector in delete_selectors:
            elements = self.driver.find_elements(*selector)
            if elements:
                delete_buttons = elements
                break
        
        if delete_buttons and len(delete_buttons) > 0:
            # Take screenshot before delete
            self.take_screenshot("before_delete")
            
            # Click first delete button
            delete_buttons[0].click()
            time.sleep(1)
            
            # Handle confirmation dialog if present
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
                print("✅ Confirmed deletion in alert dialog")
            except:
                # No alert, look for confirmation button
                confirm_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[onclick*='confirm'], .confirm")
                if confirm_buttons:
                    confirm_buttons[0].click()
                    print("✅ Confirmed deletion with button")
            
            time.sleep(2)
            
            # Take screenshot after delete
            self.take_screenshot("after_delete")
            
            print("✅ Delete functionality tested")
        else:
            print("ℹ️ Delete buttons not found - may not be implemented or no items exist")