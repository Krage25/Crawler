from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
from platforms.facebook.groups import groups
import traceback



def facebook_selenium_module(links, keyword, sessionId, dataCount, username):
    try:
        cookies_list = [
            {"name": "c_user", "value": "61561495122513"},
            {"name": "xs", "value": "43%3Ad-nvHNNunhqpVA%3A2%3A1744172017%3A-1%3A-1"}
        ]

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        # options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

        driver = webdriver.Chrome(options=options)

        driver.get("https://facebook.com/")
        time.sleep(5)  

        for cookie in cookies_list:
            driver.add_cookie(cookie)

        try:
            driver.get("https://facebook.com/")
        except:
            return "Invalid Token, Kindly Update Latest Token in DB",401
        time.sleep(5)  

        results = groups(driver,keyword, sessionId, dataCount,links,username)
        return results
    except Exception as e:
        traceback.print_exc()
    finally:
        driver.quit()


