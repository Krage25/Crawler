from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
# from db_model import youtube
from datetime import datetime
# from scrapYoutubeVideo import scrapYoutubeVideo
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from platforms.youtube.youtubeAfterScrapAction import scrapYoutubeVideo
import threading
from selenium.webdriver.chrome.options import Options
import random
from config.db_model import scrappedPosts
import traceback
# import undetected_chromedriver as uc
from selenium import webdriver as uc
from config.db_model import proxyIP, isProxy,twitterTokens
import platform
import tempfile
import os
from config.WebDriver.withProxy import open_driver_with_proxy
from config.WebDriver.withoutProxy import open_driver_non_proxy
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"
]

user_agent = random.choice(user_agents)

def removeDuplicateLinks(links):
    try:
       
        existing_links = set(doc["link"] for doc in scrappedPosts.find({"link": {"$in": links}}, {"link": 1}))
        unique_links = [link for link in links if link not in existing_links]
        return unique_links

    except Exception as e:
        print(f"Error: {e}")
        return []
    
def getProxyIP():
    try:
        # Step 1: Check useProxy value from isProxy
        checkProxy = isProxy.find_one({'platform': 'youtube'})
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
def getUserProfile():
    try:
        profiles = list(twitterTokens.find())
        if not profiles:
            return None
        # random_a = random.choice(profiles)
        # print(random_a)
        return profiles
    except Exception as e:
        print(e)

def youtube_selenium_module(keyword, sessionId, dataCount,username):
    os.system("pkill -f chrome || true")
    try:
    #     print(datetime.now())
    #     system = platform.system()
    #     print(f"Operating System : {system}")
    #     # chrome_options = Options()
    #     # chrome_options.add_argument('--headless')
    #     # chrome_options.add_argument('--header="Referer: https://www.google.com"')
    #     # chrome_options.add_argument('--header="Accept-Language: en-US,en;q=0.9"')
    #     # chrome_options.add_argument('--header="Accept-Encoding: gzip, deflate, br"')
    #     # driver=webdriver.Chrome(options=chrome_options)
    #     # url="https://www.youtube.com"
    #     # driver.get(url)
    #     profile_id = "server1"
    #     options = uc.ChromeOptions()
    #     # options.add_argument('--headless') 
    #     if system == "Windows":
    #         print("Its Windows Nothing to Worry, Thanks to Bill Gates")
    #         # options.add_argument(f"--user-data-dir=C:\\chrome_profiles\\profile_{profile_id}")
    #     elif system == "Linux":
    #         print("Added Profile in Linux")
    #         # user_data_dir = tempfile.mkdtemp()
    #         # options.add_argument(f"--user-data-dir=/tmp/udc_profile_{user_data_dir}")
    #         user_data_dir = tempfile.mkdtemp(prefix="udc_profile_")
    #         options.add_argument(f"--user-data-dir={user_data_dir}")
    #     else:
    #         raise RuntimeError(f"Unsupported OS: {system}")
    #     options.add_argument('--disable-blink-features=AutomationControlled')  # Hide automation
    #     options.add_argument('--window-size=1920,1080')
    #     options.add_argument('--disable-gpu')
    #     options.add_argument('--no-sandbox')
    #     options.add_argument('--disable-dev-shm-usage')
    #     options.add_argument("--disable-infobars")
    #     options.add_argument("--lang=en-US")
    #     options.add_argument("--headless=new")
    #     # options.add_argument(f'--proxy-server={rotating_ip}')

    #     # Optional: set a realistic user agent
    #     options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    #                         "AppleWebKit/537.36 (KHTML, like Gecko) "
    #                         "Chrome/123.0.0.0 Safari/537.36")

    #     # Launch undetected Chrome
    #     driver = uc.Chrome(options=options)

    # # Enable headers using CDP
    #     driver.execute_cdp_cmd('Network.enable', {})
    #     driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
    #         'headers': {
    #             'Referer': 'https://www.google.com',
    #             'Accept-Language': 'en-US,en;q=0.9',
    #             'Accept-Encoding': 'gzip, deflate, br',
    #         }
    #     })
        profiles = getUserProfile()
        random_profile = random.choice(profiles)
        
        # log.warning(f"Account Using For Crawling :{random_profile['username']} ")

        IP = getProxyIP()
        if IP:
            driver = open_driver_with_proxy(False, random_profile['user_agent'], IP)
        else:
            print("Not using Proxy")
            driver = open_driver_non_proxy(False, random_profile['user_agent'])

    # Visit YouTube
        driver.get("https://www.youtube.com")
        print(driver.title)
        try:
            cookiesAccept = driver.find_element(By.XPATH,'//*[@id="content"]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')
            if cookiesAccept:
                cookiesAccept.click()
        except:
            pass

        time.sleep(5)
        selectLang = driver.find_element(By.XPATH,'//*[@id="subtitle"]')
        time.sleep(3)
        selectLang.click()
        searchBox= driver.find_element(By.NAME,'search_query')
        searchBox.send_keys(f"{keyword}")
        searchBox.send_keys(Keys.ENTER)
        current_url = driver.current_url
        new_url = current_url +  "&sp=CAI%253D"
        driver.get(new_url)

        #--------Scrolling Scripts-----------
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "contents")))

        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        dataCountScrap = (dataCount // 100 + 1) * 3
        scrollCount=0
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while scrollCount<dataCountScrap :
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(4)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height
            scrollCount=scrollCount+1

        content = driver.page_source
        soup = BeautifulSoup(content,'lxml')
        
        videoLinks= soup.find_all('a',attrs={'id': 'thumbnail'})
        driver.quit()
    
        v_links = []
        max_shorts_links = 25

        total_links = 0
        shorts_links_count = 0
        counter = 0
        for links in videoLinks:
            if total_links >= dataCount:
                break

            href = links.get('href')
            if href:
                if '/shorts/' in href:
                    if shorts_links_count < max_shorts_links:
                        v_links.append("https://www.youtube.com" + href)
                        shorts_links_count += 1
                        total_links += 1
                else:
                    v_links.append("https://www.youtube.com" + href)
                    total_links += 1
                counter=counter+1

        uniqueLinks = removeDuplicateLinks(v_links)
        print(f"Before Removing Duplicate Links : {len(v_links)} ")
        print(f"After Removing Duplicate Links : {len(uniqueLinks)} ")

        # youtube_data =[]
        # for link in uniqueLinks:
        #     scrapYoutubeVideo(link, sessionId,keyword)

        IP = getProxyIP()
        if IP==None:
            print("Not using Proxy")
        else:
            print(f"Using Proxy Server : {IP}")
        
        youtube_data = []
        for link in uniqueLinks:
            result = scrapYoutubeVideo(link, sessionId, keyword, username,IP)
            if result:  
                youtube_data.extend(result)

        return youtube_data
        def process_links(links):
            for link in links:
                scrapYoutubeVideo(link, sessionId,keyword)

        def split_list(lst, n):
            k, m = divmod(len(lst), n)
            return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

        parts = split_list(uniqueLinks, 5)
    except:
        traceback.print_exc()
        return 

    