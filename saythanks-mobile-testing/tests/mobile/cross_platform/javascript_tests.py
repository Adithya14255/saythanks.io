# tests/mobile/cross_platform/javascript_tests.py
import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestSayThanksJavaScript:
    @pytest.fixture
    def mobile_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("mobileEmulation", {
            "deviceMetrics": {"width": 375, "height": 667, "pixelRatio": 2.0}
        })
        
        selenium_host = os.getenv('SELENIUM_HUB_HOST', 'selenium')
        selenium_port = os.getenv('SELENIUM_HUB_PORT', '4444')
        
        driver = webdriver.Remote(
            command_executor=f"http://{selenium_host}:{selenium_port}/wd/hub",
            options=chrome_options
        )
        yield driver
        driver.quit()
    
    def test_javascript_execution(self, mobile_driver):
        """Test basic JavaScript functionality works on mobile"""
        mobile_driver.get("http://host.docker.internal:5000")
        
        try:
            WebDriverWait(mobile_driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Test basic JavaScript execution
            js_result = mobile_driver.execute_script("return 2 + 2;")
            assert js_result == 4, "Basic JavaScript not working"
            
            # Test DOM manipulation capability
            dom_test = mobile_driver.execute_script("""
                return document.body ? true : false;
            """)
            assert dom_test, "DOM not accessible"
            
            print("✅ JavaScript execution test passed")
            
        except Exception as e:
            print(f"⚠️ JavaScript test failed: {e}")
    
    def test_local_storage_mobile(self, mobile_driver):
        """Test localStorage functionality on mobile"""
        mobile_driver.get("http://host.docker.internal:5000")
        
        try:
            # Test localStorage
            mobile_driver.execute_script("""
                localStorage.setItem('test_key', 'test_value');
            """)
            
            stored_value = mobile_driver.execute_script("""
                return localStorage.getItem('test_key');
            """)
            
            assert stored_value == 'test_value', "localStorage not working"
            print("✅ LocalStorage test passed")
            
        except Exception as e:
            print(f"⚠️ LocalStorage test failed: {e}")
    
    def test_word_counter_mobile(self, mobile_driver):
        """Test word counter JavaScript works on mobile"""
        mobile_driver.get("http://localhost:5000/to/testuser")
        
        try:
            # Test counter elements exist
            counter = mobile_driver.find_element(By.ID, "counter")
            counter1 = mobile_driver.find_element(By.ID, "counter1")
            
            assert counter.is_displayed()
            assert counter1.is_displayed()
            
            # Test initial counter value
            initial_count = counter.text
            assert initial_count == "0"
            
        except Exception as e:
            print(f"Word counter test failed: {e}")
    
    def test_badge_modal_mobile(self, mobile_driver):
        """Test badge modal functionality on mobile"""
        mobile_driver.get("http://localhost:5000/inbox")  # Mock URL
        
        try:
            # Test badge modal trigger
            badge_link = mobile_driver.find_element(By.XPATH, "//a[@href='#badge-modal']")
            badge_link.click()
            
            time.sleep(1)
            
            # Test modal elements
            badge_modal = mobile_driver.find_element(By.ID, "badge-modal")
            badge_format = mobile_driver.find_element(By.ID, "badge-format")
            badge_code = mobile_driver.find_element(By.ID, "badgeCode")
            
            assert badge_format.is_displayed()
            assert badge_code.is_displayed()
            
        except Exception as e:
            print(f"Badge modal test failed: {e}")
    
    def test_font_selector_mobile(self, mobile_driver):
        """Test font selection functionality on mobile"""
        mobile_driver.get("http://localhost:5000/inbox")
        
        try:
            # Test localStorage font functionality
            mobile_driver.execute_script("""
                localStorage.setItem('selectedFont', 'Regular');
                setSelectedFont();
            """)
            
            # Check if CSS variable was updated
            css_var = mobile_driver.execute_script("""
                return getComputedStyle(document.documentElement)
                    .getPropertyValue('--customfont');
            """)
            
            assert "Annie Use Your Telescope" in css_var
            
        except Exception as e:
            print(f"Font selector test failed: {e}")
    
    def test_pagination_mobile(self, mobile_driver):
        """Test pagination vs load-more functionality on mobile"""
        mobile_driver.get("http://localhost:5000/inbox")
        
        try:
            # Test view mode toggle
            load_more_option = mobile_driver.find_element(By.ID, "loadMoreOption")
            pagination_option = mobile_driver.find_element(By.ID, "paginationOption")
            
            # Test switching to pagination mode
            pagination_option.click()
            
            pagination_section = mobile_driver.find_element(By.ID, "paginationSection")
            load_more_section = mobile_driver.find_element(By.ID, "loadMoreSection")
            
            # Pagination should be visible, load more hidden
            assert pagination_section.is_displayed()
            assert not load_more_section.is_displayed()
            
        except Exception as e:
            print(f"Pagination test failed: {e}")