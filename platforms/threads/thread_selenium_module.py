from bs4 import BeautifulSoup
from seleniumwire import webdriver
import requests
# from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
# from db_model import youtube
from datetime import datetime
# from scrapYoutubeVideo import scrapYoutubeVideo
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from platforms.threads.extractMetadata import extractMetadata
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config.db_model import proxyIP, isProxy
import random
import traceback
from utilities.proxyParser import parse_proxy_url
def getProxyIP():
    try:
        # Step 1: Check useProxy value from isProxy
        checkProxy = isProxy.find_one({'platform': 'threads'})
        print(checkProxy)

        if checkProxy and checkProxy.get('useProxy') == "false":
            return None

        # Step 2: Randomly select one document from proxyIP
        proxies = list(proxyIP.find())
        if not proxies:
            return None
        selected = random.choice(proxies)
        return selected['ip']
    except Exception:
        traceback.print_exc()
        return None
    
def chromeDriverWithoutProxy():
    print("Not Using Proxies")
    # Set up Chrome options for normal usage (without proxy)
    options = webdriver.ChromeOptions()

    # Adding basic options for Chrome
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # Start the WebDriver without proxy
    driver = webdriver.Chrome(options=options)
    print(driver)
    return driver
def chromeDriverWithProxy(IP):
    if IP:
        username, password, proxy_host, proxy_port = parse_proxy_url(IP)
        proxy_url = f"https://{username}:{password}@{proxy_host}:{proxy_port}"
        print(f"Using Proxy: {proxy_url}")
    else:
        print("Not Using Proxy")
        proxy_url = None

    options = webdriver.ChromeOptions()
    seleniumwire_options = {}

    if proxy_url:
        seleniumwire_options = {
        'port': 8895,
        'verify_ssl': False,
        'proxy': {
            'http': proxy_url,
            'https': proxy_url,
            'no_proxy': 'localhost,127.0.0.1'
            }
            }

    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )

    driver = webdriver.Chrome(options=options, seleniumwire_options=seleniumwire_options)
    print(driver)
    return driver


def threadScrapper(keyword, sessionId, dataCount,username):
    try:
        IP = getProxyIP()
        if IP!=None:
            print(f"Using Proxy : {IP}")
            driver = chromeDriverWithProxy(IP) 
        else:
            print("Not Using Proxy IP")
            driver = chromeDriverWithoutProxy()
        # driver=webdriver.Chrome()
        url="https://www.threads.net"
        driver.get(url)
        driver.get(f"https://www.threads.net/search?q={keyword}&serp_type=default&filter=recent")
 
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.x1i10hfl'))
        )

        link_elements = driver.find_elements(By.CSS_SELECTOR, 'a.x1i10hfl')

        p_links=[]
        for link_element in link_elements:
            if len(p_links)>=dataCount:
                break
            href_value = link_element.get_attribute("href")
            if "/post/" in href_value:
                p_links.append(href_value)
        print(len(p_links))
        results = extractMetadata(p_links,driver, sessionId, keyword,username)
        driver.quit()
        return results
    except Exception as e:
        return f"Crawling Failed For Keyword {keyword} : {e}", 500



