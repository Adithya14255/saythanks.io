import os
from datetime import datetime
from PIL import Image, ImageChops

def create_screenshot_directory(directory="reports/screenshots"):
    """
    Creates a directory for storing screenshots if it does not already exist.
    
    :param directory: The directory path to create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def take_screenshot(driver, test_name, device_name=None):
    """
    Takes a screenshot and saves it with a descriptive name.
    
    :param driver: The WebDriver instance
    :param test_name: Name of the test
    :param device_name: Name of the device being tested
    :return: Path to the saved screenshot
    """
    # Create screenshots directory
    screenshot_dir = "reports/screenshots"
    create_screenshot_directory(screenshot_dir)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    device_suffix = f"_{device_name}" if device_name else ""
    filename = f"{test_name}{device_suffix}_{timestamp}.png"
    filepath = os.path.join(screenshot_dir, filename)
    
    # Take screenshot
    driver.save_screenshot(filepath)
    return filepath

def capture_element_screenshot(driver, element, test_name, device_name=None):
    """
    Captures a screenshot of a specific element.
    
    :param driver: The WebDriver instance
    :param element: The WebElement to capture
    :param test_name: Name of the test
    :param device_name: Name of the device being tested
    :return: Path to the saved screenshot
    """
    # Take full page screenshot first
    full_screenshot_path = take_screenshot(driver, f"{test_name}_full", device_name)
    
    # Get element location and size
    location = element.location
    size = element.size
    
    # Open and crop the image
    image = Image.open(full_screenshot_path)
    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = top + size['height']
    
    cropped_image = image.crop((left, top, right, bottom))
    
    # Save cropped image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    device_suffix = f"_{device_name}" if device_name else ""
    filename = f"{test_name}_element{device_suffix}_{timestamp}.png"
    screenshot_dir = "reports/screenshots"
    filepath = os.path.join(screenshot_dir, filename)
    
    cropped_image.save(filepath)
    
    # Clean up full screenshot
    os.remove(full_screenshot_path)
    
    return filepath

def compare_screenshots(screenshot1_path, screenshot2_path, threshold=0.1):
    """
    Compare two screenshots and return similarity.
    
    :param screenshot1_path: Path to first screenshot
    :param screenshot2_path: Path to second screenshot
    :param threshold: Similarity threshold (0.0 to 1.0)
    :return: Boolean indicating if images are similar
    """
    try:
        image1 = Image.open(screenshot1_path)
        image2 = Image.open(screenshot2_path)
        
        # Resize images to same size if different
        if image1.size != image2.size:
            image2 = image2.resize(image1.size)
        
        # Calculate difference
        diff = ImageChops.difference(image1, image2)
        stat = diff.histogram()
        
        # Calculate similarity percentage
        total_pixels = image1.size[0] * image1.size[1]
        different_pixels = sum(stat[256:])
        similarity = 1 - (different_pixels / total_pixels)
        
        return similarity >= (1 - threshold)
        
    except Exception as e:
        print(f"Screenshot comparison failed: {e}")
        return False