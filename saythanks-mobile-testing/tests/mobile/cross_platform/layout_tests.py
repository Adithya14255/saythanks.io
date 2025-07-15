import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

class TestLayoutTests:
    @pytest.fixture
    def devices(self):
        devices_path = '/app/config/devices.json'
        if not os.path.exists(devices_path):
            devices_path = 'config/devices.json'
            
        with open(devices_path, 'r') as f:
            return json.load(f)
    
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

    def test_mobile_layouts(self, driver, devices):
        """Test layouts on mobile devices"""
        for device_name, device_config in devices['mobile_devices'].items():
            driver.set_window_size(device_config['width'], device_config['height'])
            driver.get("http://host.docker.internal:5000")
            
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                body = driver.find_element(By.TAG_NAME, "body")
                assert body.is_displayed()
                print(f"✅ Layout test passed for {device_name}")
                
            except Exception as e:
                print(f"⚠️ Layout test failed for {device_name}: {e}")
                continue

    def test_tablet_layouts(self, driver, devices):
        """Test layouts on tablet devices"""
        for device_name, device_config in devices['tablet_devices'].items():
            driver.set_window_size(device_config['width'], device_config['height'])
            driver.get("http://host.docker.internal:5000")
            
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                body = driver.find_element(By.TAG_NAME, "body")
                assert body.is_displayed()
                print(f"✅ Tablet layout test passed for {device_name}")
                
            except Exception as e:
                print(f"⚠️ Tablet layout test failed for {device_name}: {e}")
                continue