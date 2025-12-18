#!/usr/bin/env python3
"""
Selenium Test Runner for Inventory Management System
Executes all test suites and generates comprehensive reports
"""

import pytest
import sys
import os
import time
from datetime import datetime

def create_screenshots_directory():
    """Create screenshots directory if it doesn't exist"""
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
        print("📁 Created screenshots directory")

def run_all_tests():
    """Run all Selenium test suites"""
    print("🧪 Starting Selenium Test Execution")
    print("=" * 50)
    
    # Create screenshots directory
    create_screenshots_directory()
    
    # Test configuration
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"test_report_{timestamp}.html"
    
    # Test files to run
    test_files = [
        "test_homepage.py",
        "test_authentication.py", 
        "test_inventory_management.py",
        "test_api_integration.py",
        "test_navigation_and_ui.py",
        "test_advanced_scenarios.py"
    ]
    
    print(f"📋 Test Files to Execute:")
    for i, test_file in enumerate(test_files, 1):
        print(f"   {i}. {test_file}")
    
    print(f"📊 Report will be saved as: {report_file}")
    print("=" * 50)
    
    # Pytest arguments
    pytest_args = [
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        f"--html={report_file}",  # HTML report
        "--self-contained-html",  # Embed CSS/JS in HTML
        "--capture=no",  # Don't capture stdout (show print statements)
    ]
    
    # Add test files
    pytest_args.extend(test_files)
    
    # Run tests
    start_time = time.time()
    exit_code = pytest.main(pytest_args)
    end_time = time.time()
    
    # Print summary
    print("=" * 50)
    print(f"🏁 Test Execution Completed")
    print(f"⏱️  Total Time: {end_time - start_time:.2f} seconds")
    print(f"📊 Report: {report_file}")
    print(f"📸 Screenshots: screenshots/ directory")
    
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed - check the report for details")
    
    return exit_code

def run_specific_test_suite(suite_name):
    """Run a specific test suite"""
    test_files = {
        "homepage": "test_homepage.py",
        "auth": "test_authentication.py",
        "inventory": "test_inventory_management.py", 
        "api": "test_api_integration.py",
        "navigation": "test_navigation_and_ui.py",
        "advanced": "test_advanced_scenarios.py"
    }
    
    if suite_name.lower() not in test_files:
        print(f"❌ Unknown test suite: {suite_name}")
        print(f"Available suites: {', '.join(test_files.keys())}")
        return 1
    
    test_file = test_files[suite_name.lower()]
    print(f"🧪 Running {suite_name} test suite: {test_file}")
    
    # Create screenshots directory
    create_screenshots_directory()
    
    # Run specific test
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"test_report_{suite_name}_{timestamp}.html"
    
    pytest_args = [
        "-v",
        "--tb=short",
        f"--html={report_file}",
        "--self-contained-html",
        "--capture=no",
        test_file
    ]
    
    exit_code = pytest.main(pytest_args)
    
    print(f"📊 Report saved as: {report_file}")
    return exit_code

if __name__ == "__main__":
    print("🚀 Selenium Test Runner for Inventory Management System")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        # Run specific test suite
        suite_name = sys.argv[1]
        exit_code = run_specific_test_suite(suite_name)
    else:
        # Run all tests
        exit_code = run_all_tests()
    
    sys.exit(exit_code)