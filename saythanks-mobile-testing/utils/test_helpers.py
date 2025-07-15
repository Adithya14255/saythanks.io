import time
import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def setup_test_environment():
    """Setup test environment with necessary configurations"""
    # Create reports directory
    os.makedirs("reports", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)
    
    print("Test environment setup completed")

def teardown_test_environment():
    """Clean up test environment after tests"""
    print("Test environment cleanup completed")

def log_test_results(test_name, result, device_name=None):
    """Log test results for reporting"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    device_info = f" on {device_name}" if device_name else ""
    status = "PASSED" if result else "FAILED"
    
    log_message = f"[{timestamp}] {test_name}{device_info}: {status}"
    print(log_message)
    
    # Write to log file
    log_file = "reports/test_execution.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_message + "\n")

def wait_for_element_to_be_visible(driver, locator, timeout=10):
    """
    Wait for a specific element to be visible on the screen
    
    :param driver: WebDriver instance
    :param locator: Tuple of (By, value) for element location
    :param timeout: Maximum time to wait in seconds
    :return: WebElement if found, None if timeout
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element
    except Exception as e:
        print(f"Element not visible after {timeout}s: {e}")
        return None

def wait_for_element_to_be_clickable(driver, locator, timeout=10):
    """
    Wait for element to be clickable
    
    :param driver: WebDriver instance
    :param locator: Tuple of (By, value) for element location
    :param timeout: Maximum time to wait in seconds
    :return: WebElement if clickable, None if timeout
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        return element
    except Exception as e:
        print(f"Element not clickable after {timeout}s: {e}")
        return None

def safe_click(driver, element, max_attempts=3):
    """
    Safely click an element with retry logic
    
    :param driver: WebDriver instance
    :param element: WebElement to click
    :param max_attempts: Maximum number of click attempts
    :return: Boolean indicating success
    """
    for attempt in range(max_attempts):
        try:
            # Scroll element into view
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            
            # Try to click
            element.click()
            return True
            
        except Exception as e:
            print(f"Click attempt {attempt + 1} failed: {e}")
            time.sleep(1)
    
    return False

def get_element_info(element):
    """
    Get detailed information about an element
    
    :param element: WebElement
    :return: Dictionary with element information
    """
    try:
        return {
            'tag_name': element.tag_name,
            'text': element.text,
            'size': element.size,
            'location': element.location,
            'is_displayed': element.is_displayed(),
            'is_enabled': element.is_enabled(),
            'attributes': {
                'id': element.get_attribute('id'),
                'class': element.get_attribute('class'),
                'href': element.get_attribute('href')
            }
        }
    except Exception as e:
        return {'error': str(e)}

def check_responsive_layout(driver, element, max_width):
    """
    Check if element respects responsive layout constraints
    
    :param driver: WebDriver instance
    :param element: WebElement to check
    :param max_width: Maximum allowed width
    :return: Boolean indicating if layout is responsive
    """
    try:
        element_width = element.size['width']
        viewport_width = driver.execute_script("return window.innerWidth")
        
        # Element should not exceed viewport or max_width
        is_responsive = element_width <= min(viewport_width, max_width)
        
        if not is_responsive:
            print(f"Layout issue: Element width {element_width}px exceeds limit {max_width}px")
        
        return is_responsive
        
    except Exception as e:
        print(f"Responsive layout check failed: {e}")
        return False

def simulate_mobile_swipe(driver, direction="left", distance=100):
    """
    Simulate mobile swipe gesture
    
    :param driver: WebDriver instance
    :param direction: Swipe direction ('left', 'right', 'up', 'down')
    :param distance: Distance to swipe in pixels
    """
    try:
        viewport_size = driver.get_window_size()
        start_x = viewport_size['width'] // 2
        start_y = viewport_size['height'] // 2
        
        if direction == "left":
            end_x = start_x - distance
            end_y = start_y
        elif direction == "right":
            end_x = start_x + distance
            end_y = start_y
        elif direction == "up":
            end_x = start_x
            end_y = start_y - distance
        elif direction == "down":
            end_x = start_x
            end_y = start_y + distance
        else:
            raise ValueError(f"Invalid swipe direction: {direction}")
        
        # Execute swipe using JavaScript touch events
        driver.execute_script(f"""
            var startX = {start_x};
            var startY = {start_y};
            var endX = {end_x};
            var endY = {end_y};
            
            var touchstart = new TouchEvent('touchstart', {{
                touches: [new Touch({{
                    identifier: 0,
                    target: document.body,
                    clientX: startX,
                    clientY: startY
                }})]
            }});
            
            var touchend = new TouchEvent('touchend', {{
                changedTouches: [new Touch({{
                    identifier: 0,
                    target: document.body,
                    clientX: endX,
                    clientY: endY
                }})]
            }});
            
            document.body.dispatchEvent(touchstart);
            setTimeout(() => document.body.dispatchEvent(touchend), 100);
        """)
        
        print(f"Simulated {direction} swipe from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        
    except Exception as e:
        print(f"Swipe simulation failed: {e}")