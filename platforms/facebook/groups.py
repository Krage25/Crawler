import traceback
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.LanguageTranslator import languageDetection
import time
import random
import re
from datetime import datetime
from utilities.LanguageTranslator import languageTranslator
from platforms.facebook.videos import extract_video_content
from platforms.facebook.postParsing import callParserAPI


def random_delay():
    time.sleep(random.uniform(2, 5))


def extract_content(content):
    try:
        content_array = [word.strip() for word in content.split() if word.strip()]
        extracted_words = []

        for i in range(len(content_array) - 1, -1, -1):  
            word = content_array[i].strip()
            if word == "·" and len(content_array[i - 1]) == 1 and content_array[i - 1] != "·":
                print("Condition satisfied")
                print(f"Index Number : {i}")

                # Start from i+1 and go forward until you find "All"
                for j in range(i + 1, len(content_array)):
                    if content_array[j] == "All" or content_array[j]=="Follow" or content_array[j]=="Like" or content_array[j]=="comments":
                        break
                    extracted_words.append(content_array[j])
                break

        return ' '.join(extracted_words)
    except Exception as e:
        print(f"Error: {e}")
        return "n/a"

def groups(driver,keyword, sessionId, dataCount,links,username):
    final_results = []
    try:
        print("Initiated Group Scraping")
        # options = webdriver.ChromeOptions()
        # options.add_argument("--start-maximized")
        # options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        # driver = webdriver.Chrome(options=options)
        for l in links:
            driver.get(l)
            random_delay()
            wait = WebDriverWait(driver, 10)

            try:
                elements = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                clean_text = ""
                # if '/videos/' in l:
                #     clean_text = extract_video_content(elements.text)
                # else:
                #     clean_text = extract_content(elements.text)
                # print("After Cleaning -------------------------------------------------")
                # print(clean_text)

                # translated_content = languageTranslator(clean_text)

                # languageDetected = "English"
                # try:
                #     languageDetected = languageDetection(clean_text)
                # except:
                #     languageDetected="English"
                #     pass
                
                result = None
                try:
                    result = callParserAPI()
                    print("Mistral Response :",result)
                except:
                    pass

                title = "n/a"
                date_new = datetime.now()
                post_owner = "n/a"
                if result is not None:
                    title = result['title']
                    post_owner = result['publisher']
                    date_new = result['published_date']
                else:
                    continue
                print("Result :",result)


                final_results.append({
                "content":title,
                "rawContent":elements.text,
                "link": l,
                "hashtags":[keyword],
                # "videoLinks":"n/a",
                "postOwner":post_owner,
                "sessionId":sessionId,
                "keyword":keyword,
                # "translation":translated_content,
                # "languages":languageDetected,
                "datetime":date_new,
                "screenshotUrl": "n/a",
                "crawlTime": datetime.now(),
                "platform":"facebook",
                "username":username
            })
            except:
                pass
            
        driver.quit()
        return final_results
    except Exception as e:
        driver.quit()
        traceback.print_exc()