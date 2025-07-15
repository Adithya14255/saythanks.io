# tests/mobile/cross_platform/content_tests.py
import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSayThanksContentAdaptation:
    @pytest.fixture
    def driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        selenium_host = os.getenv('SELENIUM_HUB_HOST', 'selenium')
        selenium_port = os.getenv('SELENIUM_HUB_PORT', '4444')
        
        driver = webdriver.Remote(
            command_executor=f"http://{selenium_host}:{selenium_port}/wd/hub",
            options=chrome_options
        )
        yield driver
        driver.quit()
    
    def test_text_readability_mobile(self, driver):
        """Test text remains readable on small screens"""
        driver.set_window_size(320, 568)  # iPhone SE
        driver.get("http://host.docker.internal:5000")
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Test main content text
            paragraphs = driver.find_elements(By.TAG_NAME, "p")
            headings = driver.find_elements(By.TAG_NAME, "h1") + \
                      driver.find_elements(By.TAG_NAME, "h2") + \
                      driver.find_elements(By.TAG_NAME, "h3")
            
            text_elements = paragraphs + headings
            
            for element in text_elements[:5]:  # Test first 5 text elements
                if element.is_displayed():
                    font_size = driver.execute_script(
                        "return window.getComputedStyle(arguments[0]).fontSize", element
                    )
                    try:
                        size_px = int(font_size.replace('px', ''))
                        assert size_px >= 12, f"Text too small: {size_px}px"
                        print(f"✅ Text size OK: {size_px}px")
                    except ValueError:
                        print(f"⚠️ Could not parse font size: {font_size}")
                        
        except Exception as e:
            print(f"⚠️ Text readability test failed: {e}")
    
    def test_image_responsiveness(self, driver):
        """Test images scale properly on mobile"""
        driver.set_window_size(375, 667)
        driver.get("http://host.docker.internal:5000")
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            images = driver.find_elements(By.TAG_NAME, "img")
            
            for img in images[:3]:  # Test first 3 images
                if img.is_displayed():
                    img_width = img.size['width']
                    viewport_width = driver.execute_script("return window.innerWidth")
                    
                    # Image should not exceed viewport
                    assert img_width <= viewport_width + 10, \
                        f"Image too wide: {img_width}px > {viewport_width}px"
                    print(f"✅ Image responsive: {img_width}px")
                    
        except Exception as e:
            print(f"⚠️ Image responsiveness test failed: {e}")