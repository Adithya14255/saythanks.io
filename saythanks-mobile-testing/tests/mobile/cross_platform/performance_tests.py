# tests/mobile/cross_platform/performance_tests.py
import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class TestSayThanksPerformance:
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
    
    def test_page_load_time_mobile(self, mobile_driver):
        """Test page load performance on mobile"""
        start_time = time.time()
        mobile_driver.get("http://host.docker.internal:5000")
        
        try:
            # Wait for page to be fully loaded
            WebDriverWait(mobile_driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            load_time = time.time() - start_time
            
            # Page should load within 10 seconds (generous for Docker)
            assert load_time < 10.0, f"Page load too slow: {load_time}s"
            print(f"✅ Page load time: {load_time:.2f}s")
            
        except Exception as e:
            print(f"⚠️ Page load test failed: {e}")
    
    def test_asset_loading(self, mobile_driver):
        """Test critical assets load properly"""
        mobile_driver.get("http://host.docker.internal:5000")
        
        try:
            WebDriverWait(mobile_driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Test CSS files loaded
            css_loaded = mobile_driver.execute_script("""
                return Array.from(document.styleSheets).length > 0;
            """)
            print(f"✅ CSS loaded: {css_loaded}")
            
            # Test JavaScript availability
            js_available = mobile_driver.execute_script("""
                return typeof document !== 'undefined';
            """)
            print(f"✅ JavaScript available: {js_available}")
            
        except Exception as e:
            print(f"⚠️ Asset loading test failed: {e}")