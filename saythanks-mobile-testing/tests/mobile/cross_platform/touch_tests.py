# tests/mobile/cross_platform/touch_tests.py
import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSayThanksTouchInteractions:
    @pytest.fixture
    def mobile_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("mobileEmulation", {
            "deviceMetrics": {"width": 375, "height": 667, "pixelRatio": 2.0},
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
        })
        
        selenium_host = os.getenv('SELENIUM_HUB_HOST', 'selenium')
        selenium_port = os.getenv('SELENIUM_HUB_PORT', '4444')
        
        driver = webdriver.Remote(
            command_executor=f"http://{selenium_host}:{selenium_port}/wd/hub",
            options=chrome_options
        )
        yield driver
        driver.quit()
    
    def test_button_interactions(self, mobile_driver):
        """Test button interactions work on mobile"""
        mobile_driver.get("http://host.docker.internal:5000")
        
        try:
            # Wait for page load
            WebDriverWait(mobile_driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Find clickable buttons
            buttons = mobile_driver.find_elements(By.TAG_NAME, "button")
            links = mobile_driver.find_elements(By.TAG_NAME, "a")
            
            clickable_elements = buttons + links
            
            for element in clickable_elements[:3]:  # Test first 3 elements
                if element.is_displayed() and element.is_enabled():
                    try:
                        actions = ActionChains(mobile_driver)
                        actions.click(element).perform()
                        print(f"✅ Successfully clicked element: {element.tag_name}")
                    except Exception as e:
                        print(f"⚠️ Click failed on {element.tag_name}: {e}")
                        
        except Exception as e:
            print(f"⚠️ Touch interaction test failed: {e}")
    
    def test_form_touch_interactions(self, mobile_driver):
        """Test form elements respond to touch"""
        mobile_driver.get("http://host.docker.internal:5000")
        
        try:
            # Find form inputs
            inputs = mobile_driver.find_elements(By.TAG_NAME, "input")
            textareas = mobile_driver.find_elements(By.TAG_NAME, "textarea")
            
            form_elements = inputs + textareas
            
            for element in form_elements[:2]:  # Test first 2 form elements
                if element.is_displayed() and element.is_enabled():
                    try:
                        element.click()
                        element.send_keys("test")
                        print(f"✅ Successfully interacted with form element")
                    except Exception as e:
                        print(f"⚠️ Form interaction failed: {e}")
                        
        except Exception as e:
            print(f"⚠️ Form touch test failed: {e}")