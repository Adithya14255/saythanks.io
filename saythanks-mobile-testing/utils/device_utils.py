import json
import os

def get_device_configurations():
    """
    Retrieve all device configurations.
    
    Returns:
        dict: A dictionary containing all device configurations.
    """
    # Docker environment path
    config_path = '/app/config/devices.json'
    if not os.path.exists(config_path):
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'devices.json')
    
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def get_mobile_devices():
    """
    Get mobile device configurations only.
    
    Returns:
        dict: Mobile device configurations.
    """
    devices = get_device_configurations()
    return devices.get('mobile_devices', {})

def get_tablet_devices():
    """
    Get tablet device configurations only.
    
    Returns:
        dict: Tablet device configurations.
    """
    devices = get_device_configurations()
    return devices.get('tablet_devices', {})

def get_chrome_mobile_options(device_name=None):
    """
    Get Chrome options for mobile emulation.
    
    Args:
        device_name (str): Name of device to emulate
        
    Returns:
        ChromeOptions: Configured Chrome options
    """
    from selenium.webdriver.chrome.options import Options
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    if device_name:
        devices = get_mobile_devices()
        if device_name in devices:
            device_config = devices[device_name]
            mobile_emulation = {
                "deviceMetrics": {
                    "width": device_config['width'],
                    "height": device_config['height'],
                    "pixelRatio": 2.0
                },
                "userAgent": device_config['user_agent']
            }
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    return chrome_options