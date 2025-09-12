import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config.db_model import threadPosts,scrappedPosts
import time 
import re
from datetime import datetime
from selenium import webdriver
# from db_model import threadPosts
from utilities.LanguageTranslator import languageDetection
from utilities.LanguageTranslator import languageTranslator
import traceback


def extractMetadata(links, driver,sessionId, keyword,username):
    final_data=[]
    try:
        for link in links:
            
            
            driver.get(link)
            wait = WebDriverWait(driver, 10)
           

            owner = ""
            try:
                span_element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[4]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div[1]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div/span/div/span/div/a/span/span')))   
                owner = span_element.text
            except Exception as e:
                pass

            content =""
            try:
                spans = driver.find_elements(By.CSS_SELECTOR, 'div.x1a6qonq.x6ikm8r.x10wlt62.xj0a0fe.x126k92a.x6prxxf.x7r5mf7 span')
                span_texts = [span.text for span in spans]
                content = ' '.join(span_texts)
            except Exception as e:
                pass

            likes = "0"
            try:
                likes_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="barcelona-page-layout"]/div[1]/div[1]/div[1]/div[1]/div/div/div/div[2]/div[3]/div/div[3]/div/div[1]/div/div/span/div/span')))
                likes = likes_element.text
            except Exception as e:
                pass

            # Extract image URL
            img_element = "n/a"
            try:
                img_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.x1ey2m1c.xds687c.xl1xv1r.x10l6tqk.x17qophe.x13vifvy')))        
                img_element = img_element.get_attribute('src')
            except Exception as e:
                pass

            # Detect language
            languagedetected = "English"
            try:
                languagedetected =languageDetection(content)
                
            except Exception as e:
                pass

            # Translate language
            lang_translation = ""
            try:
                lang_translation = languageTranslator(content)
            except Exception as e:
                lang_translation=content
                pass

            # Extract datetime
            datetime_value = "null"
            try:
                time_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'time')))
                datetime_value = time_element.get_attribute('datetime')
                datetime_value = datetime.fromisoformat(datetime_value[:-1])
            except Exception as e:
                pass
            
            try:
                hashtags = re.findall(r'#\s*([\w]+)', content)
            except:
                pass
            
            print(f"Content : {content}")
            if content=="":
                return
            final_data.append({
                "link":links,
                "content" : content,
                "likes":likes,
                "imageLink":img_element,
                "platform":"threads",
                "sessionId":sessionId,
                "keyword": keyword,
                "languages": languagedetected,
                "translation":lang_translation,
                "datetime":datetime_value,
                "postOwner":owner,
                "hashtags":hashtags,
                "crawlTime":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user":username
            })
            
        return final_data
    except Exception as e:
        traceback.print_exc()
        return f"Crawling Failed For Keyword {keyword} : {e}", 500
        
    
