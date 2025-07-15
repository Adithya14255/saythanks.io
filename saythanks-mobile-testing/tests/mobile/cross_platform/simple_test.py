import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time

def test_selenium_connection():
    """Simple test to verify Selenium connection works"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    selenium_host = os.getenv('SELENIUM_HUB_HOST', 'selenium')
    selenium_port = os.getenv('SELENIUM_HUB_PORT', '4444')
    
    print("Connecting to Selenium at {}:{}".format(selenium_host, selenium_port))
    
    # For Selenium 3.x - use desired_capabilities
    capabilities = {
        'browserName': 'chrome',
        'chromeOptions': {
            'args': ['--headless', '--no-sandbox', '--disable-dev-shm-usage']
        }
    }
    
    driver = webdriver.Remote(
        command_executor="http://{}:{}/wd/hub".format(selenium_host, selenium_port),
        desired_capabilities=capabilities
    )
    
    try:
        # Test basic functionality
        driver.get("https://www.google.com")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        assert "Google" in driver.title
        print("✅ Selenium connection successful!")
        
    finally:
        driver.quit()

def test_mobile_viewport():
    """Test mobile viewport emulation"""
    selenium_host = os.getenv('SELENIUM_HUB_HOST', 'selenium')
    selenium_port = os.getenv('SELENIUM_HUB_PORT', '4444')
    
    # Mobile emulation for Selenium 3.x
    capabilities = {
        'browserName': 'chrome',
        'chromeOptions': {
            'args': ['--headless', '--no-sandbox', '--disable-dev-shm-usage'],
            'mobileEmulation': {
                'deviceMetrics': {'width': 375, 'height': 667, 'pixelRatio': 2.0},
                'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
            }
        }
    }
    
    driver = webdriver.Remote(
        command_executor="http://{}:{}/wd/hub".format(selenium_host, selenium_port),
        desired_capabilities=capabilities
    )
    
    try:
        driver.get("https://www.google.com")
        
        # Check viewport size
        viewport_width = driver.execute_script("return window.innerWidth")
        assert viewport_width == 375
        
        print("✅ Mobile viewport test successful!")
        
    finally:
        driver.quit()

def test_saythanks_mobile():
    """Test SayThanks.io mobile responsiveness"""
    selenium_host = os.getenv('SELENIUM_HUB_HOST', 'selenium')
    selenium_port = os.getenv('SELENIUM_HUB_PORT', '4444')
    
    # iPhone 6/7/8 viewport
    capabilities = {
        'browserName': 'chrome',
        'chromeOptions': {
            'args': ['--headless', '--no-sandbox', '--disable-dev-shm-usage'],
            'mobileEmulation': {
                'deviceMetrics': {'width': 375, 'height': 667, 'pixelRatio': 2.0},
                'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
            }
        }
    }
    
    driver = webdriver.Remote(
        command_executor="http://{}:{}/wd/hub".format(selenium_host, selenium_port),
        desired_capabilities=capabilities
    )
    
    try:
        # Test SayThanks.io
        driver.get("https://saythanks.io")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Basic checks
        assert "Say Thanks" in driver.title
        
        # Check if page is responsive
        viewport_width = driver.execute_script("return window.innerWidth")
        assert viewport_width == 375
        
        print("✅ SayThanks.io mobile test successful!")
        
    finally:
        driver.quit()

def run_all_tests(self):
    """Run complete test suite"""
    self.log("🚀 Starting SayThanks.io Mobile Testing Suite...", "green")
    
    # Create reports directory
    if not os.path.exists("reports"):
        os.makedirs("reports")
    
    # Wait for services
    self.log("Waiting for services to be ready...", "yellow")
    if not self.wait_for_services():
        self.log("💥 Failed to connect to required services. Exiting.", "red")
        sys.exit(1)
    
    # Additional wait for stability
    time.sleep(5)
    
    # Define test suites to run (start with simple connection test)
    test_suites = [
        ("tests/mobile/cross_platform/simple_test.py", "Connection Tests"),
        ("tests/mobile/cross_platform/responsive_tests.py", "Responsive Layout Tests"),
        ("tests/mobile/cross_platform/touch_tests.py", "Touch Interaction Tests"),
        ("tests/mobile/cross_platform/content_tests.py", "Content Adaptation Tests"),
        ("tests/mobile/cross_platform/javascript_tests.py", "JavaScript Functionality Tests"),
        ("tests/mobile/cross_platform/performance_tests.py", "Performance Tests"),
        ("tests/mobile/cross_platform/browser_tests.py", "Cross-Browser Tests")
    ]
    
    # Run each test suite
    for test_path, description in test_suites:
        self.run_test_suite(test_path, description)
    
    # Generate reports
    self.generate_summary_report()
    
    # Final status
    if self.results["summary"]["failed_suites"] == 0:
        self.log("🎉 All tests passed!", "green")
        sys.exit(0)
    else:
        self.log("💥 {} test suite(s) failed. Check output for details.".format(self.results['summary']['failed_suites']), "red")
        sys.exit(1)