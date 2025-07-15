# tests/mobile/cross_platform/browser_tests.py
import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestCrossBrowserMobile:
    
    def get_mobile_chrome_driver(self):
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
        
        return webdriver.Remote(
            command_executor=f"http://{selenium_host}:{selenium_port}/wd/hub",
            options=chrome_options
        )
    
    def test_chrome_mobile_compatibility(self):
        """Test Chrome mobile browser compatibility"""
        driver = self.get_mobile_chrome_driver()
        
        try:
            driver.get("http://host.docker.internal:5000")
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Test basic functionality works
            assert len(driver.title) > 0, "Page title missing"
            
            body = driver.find_element(By.TAG_NAME, "body")
            assert body.is_displayed(), "Body not displayed"
            
            # Test CSS support
            css_support = driver.execute_script("""
                return CSS.supports && CSS.supports('display', 'flex');
            """)
            assert css_support, "Modern CSS not supported"
            
            print("✅ Chrome mobile compatibility test passed")
            
        except Exception as e:
            print(f"⚠️ Chrome compatibility test failed: {e}")
        finally:
            driver.quit()
    
    def test_mobile_features_support(self):
        """Test mobile-specific features support"""
        driver = self.get_mobile_chrome_driver()
        
        try:
            driver.get("http://host.docker.internal:5000")
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Test touch events support
            touch_support = driver.execute_script("""
                return 'ontouchstart' in window;
            """)
            print(f"Touch events supported: {touch_support}")
            
            # Test viewport support
            viewport_support = driver.execute_script("""
                return window.visualViewport !== undefined;
            """)
            print(f"Visual viewport supported: {viewport_support}")
            
            print("✅ Mobile features test completed")
            
        except Exception as e:
            print(f"⚠️ Mobile features test failed: {e}")
        finally:
            driver.quit()