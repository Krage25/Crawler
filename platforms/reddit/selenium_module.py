from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
import traceback
from platforms.reddit.utilities.checkLogin import checkLogin
from platforms.reddit.extract_reddit_data import extract_reddit_data
from pathlib import Path
# Path to your exported cookies file
COOKIE_FILE = Path("platforms") / "reddit" / "www.reddit.com.json"

# If you need it as a string (for opening files, etc.)
cookie_file_path = str(COOKIE_FILE)

# Initialize Selenium WebDriver

# def reddit_main(keyword, sessionId, dataCount,username):
#     # keyword = "sambhal violence"
#     try:
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless=new')  # Use new headless mode
#         options.add_argument('--headless=new')  # Use the newer headless mode
#         options.add_argument('--disable-gpu')
#         options.add_argument('--window-size=1920,1080')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_argument('--start-maximized')
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         options.add_experimental_option('useAutomationExtension', False)

#         # Optionally, set a custom user-agent
#         options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                             "AppleWebKit/537.36 (KHTML, like Gecko) "
#                             "Chrome/122.0.0.0 Safari/537.36")
#         options.add_argument('--disable-dev-shm-usage')
#         driver = webdriver.Chrome(options=options)

#         # Open Reddit login page
#         driver.get("https://old.reddit.com/")
#         time.sleep(2)  

#         # Load cookies from the file
#         with open(COOKIE_FILE, "r") as file:
#             cookies = json.load(file)

#         # Add cookies to the browser session
#         for cookie in cookies:
#             # Remove fields not accepted by Selenium
#             cookie.pop("sameSite", None)
#             cookie.pop("priority", None)
#             driver.add_cookie(cookie)

#         # Refresh the page to apply cookies
#         driver.refresh()
#         driver.get(f"https://old.reddit.com/search?q={keyword}&restrict_sr=&sort=new&t=all")

#         checkLogin(driver)
        
#         allLinks = driver.find_elements(By.TAG_NAME, "a")
        
#         final_links = set()
#         for l in allLinks:
#             if len(final_links)>20:
#                 break
#             link = l.get_attribute("href") 
#             if link and "/comments" in link: 
#                 final_links.add(link)
        
        

#         results = []
#         for l in list(final_links):
#            results.extend(extract_reddit_data(l,driver, sessionId, keyword,username))

#         driver.quit()
#         return results
#     except Exception as e:
#         print(e)
#         traceback.print_exc()
#     finally:
#         driver.quit()
def reddit_main(keyword, sessionId, dataCount, username):
    import time
    import json
    import traceback
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/122.0.0.0 Safari/537.36")

        driver = webdriver.Chrome(options=options)

        # Initial page to load cookies
        driver.get("https://old.reddit.com/")
        time.sleep(2)

        with open(COOKIE_FILE, "r") as file:
            cookies = json.load(file)

        for cookie in cookies:
            cookie.pop("sameSite", None)
            cookie.pop("priority", None)
            driver.add_cookie(cookie)

        driver.refresh()
        time.sleep(2)

        base_url = f"https://old.reddit.com/search?q={keyword}&restrict_sr=&sort=new&t=all"
        current_url = base_url
        final_links = set()

        counter = 1
        while len(final_links) < dataCount and current_url:
            if counter>=3:
                break
            driver.get(current_url)
            print(f"Current URL: {current_url}")
            time.sleep(2)

            # checkLogin(driver) 

            try:
                # Wait until posts appear
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-result"))
                )
            except:
                print("No search results loaded.")
                break

            all_links = driver.find_elements(By.TAG_NAME, "a")
            for a in all_links:
                href = a.get_attribute("href")
                if href and "/comments/" in href:
                    final_links.add(href)
                    if len(final_links) >= dataCount:
                        break

            print(f"Collected so far: {len(final_links)} links")

            # Pagination
            try:
                footer = driver.find_elements(By.TAG_NAME,'footer')
                
                if len(footer)>1:
                    footer = footer[1]
                else:
                    footer = footer[0]
                next_button = footer.find_element(By.TAG_NAME,'a')
                # next_button = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/footer/div/span/a")
                current_url = next_button.get_attribute("href")
                print("Next Page : ", current_url)
            except:
                print("No more pages available.")
                break
            counter+=1

        print(f"✅ Total {len(final_links)} links collected.")

        results = []
        for link in list(final_links):
            results.extend(extract_reddit_data(link, driver, sessionId, keyword, username))

        return results

    except Exception as e:
        print("❌ Error:", e)
        traceback.print_exc()
    finally:
        driver.quit()

