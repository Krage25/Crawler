from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
from PIL import Image
from utility_functions import ipFinder
from utility_functions.chromeKiller import cleanup_chrome_processes
# Ensure the screenshot folder exists
screenshot_folder = r"static"
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)

def take_screenshot(data):

    # print(f"Taking screenshot of {url} with ID {inserted_id}")    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        screenshot_urls=[]
        for link in data:
            url = link['link']
            inserted_id = link['id']
        # Go to the URL
            driver.get(url)
            # Wait for the page to load completely
            time.sleep(6)

            # Save the full-page screenshot
            try:
                screenshot_path = os.path.join(screenshot_folder, f"{inserted_id}.png")
                driver.save_screenshot(screenshot_path)
            except:
                pass    
            # screenshot_urls=[]
            # Open the image and get its dimensions
            with Image.open(screenshot_path) as img:
                width, height = img.size
                print(f"Original image size: {width}x{height}")
                # Calculate the cropping box (left, upper, right, lower)
                left = 500
                upper = 0
                right = width - 700
                lower = height - 320
                # Crop the image
                cropped_img = img.crop((left, upper, right, lower))
                # Save the cropped image
                cropped_screenshot_path = os.path.join(screenshot_folder, f"{inserted_id}.png")
                cropped_img.save(cropped_screenshot_path)
                # print(f"Cropped screenshot saved to {cropped_screenshot_path}")
                # screenshot_url = f"{ipFinder()}/static/{inserted_id}.png"
                screenshot_url = f"http://10.226.54.111:5000/static/{inserted_id}.png"
                # print(screenshot_url)
                screenshot_urls.append(screenshot_url)

                # twitterPosts.update_one({"_id":ObjectId(inserted_id)})

    except Exception as e:
        print(f"Error taking screenshot: {e}")
        pass
    finally:
        driver.quit()
        # cleanup_chrome_processes()

    return screenshot_urls

# Usage example
# url = "https://www.example.com"
# inserted_id = "example_id"
# take_screenshot(url, inserted_id)
