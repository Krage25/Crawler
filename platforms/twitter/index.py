from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utilities.logger import Logger
from platforms.twitter.tweet import Tweet
from selenium.webdriver.common.by import By
import time
from seleniumwire import webdriver as wire_webdriver
from datetime import datetime
from bson import ObjectId
from selenium.common.exceptions import InvalidSessionIdException
from threading import Timer
from config.db_model import twitterTokens
import random
import traceback
from config.db_model import proxyIP,isProxy
from seleniumwire import webdriver
from config.db_model import scrappedPosts
import json
from utilities.proxyParser import parse_proxy_url
import platform
import tempfile
from platforms.twitter.without_proxy import open_driver_non_proxy
from platforms.twitter.withProxy import open_driver_with_proxy
from utilities.LanguageDetectionComplete import LangDetectComplete
from utilities.BhashiniTranslator import languageIdentifier
from utilities.BhshiniTranslatorV2 import translation
from urllib.parse import quote
from bhashini import batch_language_detection, batch_translation, process_text_pipeline
from utilities.LanguageTranslator import languageDetection, languageTranslator
from updateSession import updateSessionData


log = Logger()
screenshot_folder = r"C:\Users\azad\OneDrive\Desktop\Git\decoy-backend\Images"
keywordUsed = None
lookedOnTop = True
timeout_occurred = False

def convertKeyword(key):
    try:
        print(key)
    except:
        pass

def is_hindi_char(char):
    return '\u0900' <= char[0] <= '\u097F'
def extract_id_from_url(url):
    return url.split('/')[-1].split('.')[0]

# def getUserProfile():
#     try:
#         profiles =  list(twitterTokens.find({"server":"1"}))
#         return profiles 
#     except Exception as e:
#         print(e)

def translateKeyword(keyword_):
    try:
       received_keyword = languageTranslator(keyword_)
       return received_keyword
    except:
        return keyword_


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

def main(keyword, sessionId, dataCount, username):
    try:
        translatedKeyword = translateKeyword(keyword)
        newKeyword = f"{keyword} {translatedKeyword}"
        # url = f"https://x.com/search?q={keyword}&src=recent_search_click&f=live"
        # url = f"https://x.com/search?q={keyword}&src=recent_search_click"
        encoded_keyword = quote(newKeyword)
        url = f"https://x.com/search?q={encoded_keyword}&src=recent_search_click&f=live"
        log.warning("Loading configurations...")

        profiles = getUserProfile()
        random_profile = random.choice(profiles)
        
        log.warning(f"Account Using For Crawling :{random_profile['username']} ")

        IP = getProxyIP()
        if IP:
            driver = open_driver_with_proxy(True, random_profile['user_agent'], IP)
        else:
            driver = open_driver_non_proxy(True, random_profile['user_agent'])

        print(f"Auth Token : {random_profile['token']}")
        driver.get("https://twitter.com/")
        time.sleep(2)
        set_token(driver, random_profile['token'])
        driver.get("https://twitter.com/")
        log.warning("Starting...")
        
        final_data = profile_search(driver, url, sessionId, keyword, dataCount, username, random_profile['_id'])
        
        return final_data
        
    except Exception  as e:
        traceback.print_exc()
        log.error("Twitter token expired") 
        driver.quit()
    except Exception as e:
        log.error(f"Unexpected error: {str(e)}")
        raise e
    
    
# def stop_loop(driver, sessionId, objectId, keyUsed, platform):
#     global timeout_occurred
#     updateSessionData(objectId, sessionId, keyUsed, platform)
#     timeout_occurred = True

def updateTokenCollection(objectId):
    try:
        result = twitterTokens.update_one(
            {"_id": ObjectId(objectId)},
            {"$set": {"status": -1}}
        )
        if result.modified_count == 1:
            print(f"Token with ID {objectId} updated to status -1.")
        else:
            print(f"No document updated. Check if the ID {objectId} exists.")
    except Exception as e:
        print(f"Error updating token: {e}")
def profile_search(driver, url, sessionId, keyUsed, dataCount,username_,account):
    global lookedOnTop
    global timeout_occurred
    # time.sleep(5)
    data=[]
    try:
        
        num = dataCount
        driver.get(url)
        time.sleep(15)
        try:
            notfound = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[2]/a')
            if notfound:
                driver.quit()
                return
        except Exception:
            pass
        log.warning("Fetching...")

        current_url = driver.current_url
        updateTokenCollection(account)
        if current_url.startswith('https://x.com/i/flow/login?redirect'):
            driver.quit()

        Ad = []
        results = []
        
        try:
            while len(results) < num:
                # time.sleep(1)
                if timeout_occurred:
                    log.warning("Exited loop due to timeout.")
                    break
                tweet = Tweet(driver, Ad)
                try:
                    emptypage = driver.find_element(By.TAG_NAME,'article')
                    if emptypage is None:
                        break
                except:
                    pass
                try:
                    resetBtnFound = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div/button')

                except Exception:
                    pass
                try:
                   isTweetAvailable =  tweet.__get_first_tweet()
                   print(f"Tweet Available : {isTweetAvailable}")
                   if isTweetAvailable:
                       pass
                   else:
                       break
                except:
                    pass

                source_link = tweet.get_url()
                date = tweet.get_date()
                content = tweet.get_text()
                langauge = tweet.get_lang()
                likes = tweet.get_num_likes()
                retweets = tweet.get_num_retweet()
                replies = tweet.get_num_reply()
                postOwner = tweet.get_post_owner()
                username = tweet.get_tweet_username()

                if timeout_occurred:
                    log.warning("Exited loop due to timeout.")
                    break
                try:
                    datePublished = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
                except Exception:
                    datePublished = None
                
                # # Language Detection
                # try:
                #     languageDetected = languageDetection(content)
                # except:
                #     pass
                # # languageDetected = LangDetectComplete(content)
                
                # translated_data = content
                # try:
                #     translated_data = languageTranslator(content)
                    
                # except:
                #     translated_data = content

                data.append({
                    "link": source_link,
                    "content": content,
                    "datetime": datePublished.strftime("%Y-%m-%d %H:%M:%S"),
                    "retweets": retweets,
                    # "languages": languageDetected,
                    "likes": likes,
                    "retweets": retweets,
                    "replies": replies,
                    "platform": "twitter",
                    "sessionId": sessionId,
                    "keyword": keyUsed,
                    "postOwner": postOwner,
                    "useHandle": username,
                    # "translation": translated_data,
                    "mediaPresent": langauge,
                    "metadata": content,
                    "crawlTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status":1,
                    "screenshotUrl":langauge,
                    "user":username_,
                    # "text":translated_data
                    # "text" : translated_data
                })
                results.append({"link": source_link})
            # scrappedPosts.insert_many(data, ordered=False)
            # data = process_text_pipeline(data)
        except TimeoutError:
            log.warning("Exited loop due to timeout.")
            driver.quit()
        finally:
            driver.quit()
            # result = process_text_pipeline(data)            
            return data

    except Exception as e:
        traceback.print_exc()
        return data
    except Exception as e:
        return  f"Server error: {e}", 500
    finally:
        with open("results.txt", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        driver.quit()   

def getProxyIP():
    try:
        # Step 1: Check useProxy value from isProxy
        checkProxy = isProxy.find_one({'platform': 'twitter'})
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


# def open_driver_non_proxy(headless: bool, agent: str) -> webdriver.Chrome:
#     try:
#         system = platform.system()
#         options = Options()
#         log.warning("Not Using Proxy IP")
#         if system == "Windows":
#             log.success("Its Windows Nothing to Worry, Thanks to Bill Gates")
#         elif system == "Linux":
#             print("Added Profile in Linux")
#             user_data_dir = tempfile.mkdtemp(prefix="udc_profile_")
#             options.add_argument(f"--user-data-dir={user_data_dir}")
#         else:
#             raise RuntimeError(f"Unsupported OS: {system}")
#         options.add_argument('--log-level=3')
#         options.add_argument('ignore-certificate-errors')
#         options.add_experimental_option('excludeSwitches', ['enable-logging'])
#         if headless:
#             options.add_argument('--headless')
#         options.add_argument(f"user-agent={agent}")
        
#         # Add these lines to fix the user data directory issue
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_argument(f'--user-data-dir=/tmp/chrome-data-{time.time()}')
        
#         # If running on AWS, these additional options may help
#         options.add_argument('--disable-gpu')
#         options.add_argument('--disable-extensions')
#         options.add_argument('--disable-software-rasterizer')

#         seleniumwire_options = {
#             'proxy':{
#                 'no_proxy':'localhost,127.0.0.1'
#             }
#         }
#         # import os
#         # os.system('pkill -f chrom || true')
#         return wire_webdriver.Chrome(options=options,seleniumwire_options=seleniumwire_options)
#         return webdriver.Chrome(options=options)
#     except:
#         traceback.print_exc()
#         raise Exception
# def open_driver_with_proxy(headless: bool, agent: str, proxy_ip: str) -> webdriver.Chrome:
#     try:
#         # Parse proxy components
#         username, password, proxy_host, proxy_port = parse_proxy_url(proxy_ip)
#         proxy_url = f"http://{username}:{password}@{proxy_host}:{proxy_port}"
#         print(f"Using Proxy: {proxy_url}")
#         system = platform.system()
#         # Chrome options setup
#         options = Options()
#         if system == "Windows":
#             print("Its Windows Nothing to Worry, Thanks to Bill Gates")
#             # options.add_argument(f"--user-data-dir=C:\\chrome_profiles\\profile_{profile_id}")
#         elif system == "Linux":
#             print("Added Profile in Linux")
#             # user_data_dir = tempfile.mkdtemp()
#             # options.add_argument(f"--user-data-dir=/tmp/udc_profile_{user_data_dir}")
#             user_data_dir = tempfile.mkdtemp(prefix="udc_profile_")
#             options.add_argument(f"--user-data-dir={user_data_dir}")
#         else:
#             raise RuntimeError(f"Unsupported OS: {system}")
#         options.add_argument('--log-level=3')
#         options.add_argument('ignore-certificate-errors')
#         options.add_experimental_option('excludeSwitches', ['enable-logging'])
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_argument(f'--user-data-dir=/tmp/chrome-data-{time.time()}')
#         options.add_argument('--disable-gpu')
#         options.add_argument('--disable-extensions')
#         options.add_argument('--disable-software-rasterizer')
#         options.add_argument('--start-maximized')
#         options.add_argument('--window-size=1920,1080')
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         options.add_experimental_option('useAutomationExtension', False)
#         options.add_argument(f"user-agent={agent}")
#         if headless:
#             options.add_argument('--headless')

#         # Proxy settings
#         seleniumwire_options = {
#         'port': 8885,
#         'verify_ssl': False,
#         'proxy': {
#             'http': proxy_url,
#             'https': proxy_url,
#             'no_proxy': 'localhost,127.0.0.1'
#             }
#             }

#         # Return configured driver
#         return webdriver.Chrome(options=options, seleniumwire_options=seleniumwire_options)
#     except:
#         traceback.print_exc()
#         raise Exception("Failed to initialize Chrome WebDriver with proxy")
def set_token(driver: webdriver.Chrome, token: str) -> None:
    script = f"""
        let date = new Date();
        date.setTime(date.getTime() + (7*24*60*60*1000));
        let expires = "; expires=" + date.toUTCString();
        document.cookie = "auth_token={token}"  + expires + "; path=/";
    """
    driver.execute_script(script)

# def set_token(driver, token: str):
#     # Make sure you are on twitter.com so domain matches
#     driver.get("https://twitter.com/")
#     time.sleep(3)
    
#     driver.add_cookie({
#         'name': 'auth_token',
#         'value': token,
#         'domain': '.twitter.com',
#         'path': '/',
#         'secure': True,
#         'httpOnly': True,
#     })

# def load_conf() -> dict:
#     with open(r"Twitter_Scrapper/files/conf.json", "r") as file:
#         return json.loads(file.read())
