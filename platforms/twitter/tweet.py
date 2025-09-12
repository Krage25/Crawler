from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException,TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime
from time import sleep
import traceback
import pytz
from selenium.webdriver.support.ui import WebDriverWait

class Tweet:
    def __init__(self,
            driver: webdriver.Chrome,
            Ad: list
    ):
        self.driver = driver
        self.Ad = Ad
        while True:
            try:
                self.tweet = self.__get_first_tweet()
                self.__remove_pinned()
                self.tweet_url, self.retweet = self.__get_tweet_url()
                self.tweet_date = self.__get_tweet_date()
                self.tweet_text = self.__get_tweet_text()
                self.tweet_lang = self.__get_tweet_lang()
                self.tweet_num_likes = self.__get_tweet_num_likes()
                self.tweet_num_retweet = self.__get_tweet_num_retweet()
                self.tweet_num_reply = self.__get_tweet_num_reply()
                self.tweet_post_owner = self.__get_tweet_post_owner()
                self.tweet_username = self.__get_tweet_user_name()
            
            except TypeError:
                self.Ad.append(self.tweet)
                sleep(1)
                driver.execute_script("arguments[0].scrollIntoView();", self.tweet)
                continue

            except Exception:
                print(traceback.format_exc())
                sleep(1)
                pass
            break

        self.__delete_tweet()

    
    def get_url(self) -> str:
        return self.tweet_url
    
    def get_date(self) -> str:
        return self.tweet_date
    
    def get_text(self) -> str:
        return self.tweet_text
    
    def get_lang(self) -> str:
        return self.tweet_lang
    
    def get_num_likes(self) -> str:
        return self.tweet_num_likes
    
    def get_num_retweet(self) -> str:
        return self.tweet_num_retweet

    def get_num_reply(self) -> str:
        return self.tweet_num_reply
    def get_post_owner(self) -> str:
        return self.tweet_post_owner
    def get_tweet_username(self)-> str:
        return self.tweet_username
    

    def __get_first_tweet(self) -> WebElement:
        while True:
            try:
                tweets = self.driver.find_elements(By.CSS_SELECTOR, "article[data-testid='tweet']")
                if len(tweets) <=0:
                    break
                for tweet in tweets:
                    if tweet not in self.Ad:
                        return tweet
                    else:
                        break
            except IndexError:
                sleep(0.5)
                continue
        return None
    
    def __remove_pinned(self):
        while True:
            try:
                if self.tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="socialContext"]').get_attribute("innerText") == "Pinned":
                # if WebDriverWait(self.tweet, 10).until(lambda d: d.find_element(By.CSS_SELECTOR, 'div[data-testid="socialContext"]')).get_attribute("innerText") == "Pinned":
                    print("Skipping pinned...")
                    pass
                
            except NoSuchElementException:
                pass
                return

            except StaleElementReferenceException:
                sleep(1)
                pass
            except StaleElementReferenceException:
                sleep(1)
                pass

            break
    # def __remove_pinned(self):
    #     while True:
    #         try:
    #             if not self.tweet:
    #                 break  # or return

    #             # Attempt to find the 'socialContext' within the tweet
    #             social_context_elem = WebDriverWait(self.driver, 10).until(
    #                 lambda d: self.tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="socialContext"]')
    #             )

    #             if social_context_elem.get_attribute("innerText") == "Pinned":
    #                 print("Skipping pinned tweet...")
    #                 # Handle the pinned tweet as needed
    #                 break  # exit loop after handling
    #             else:
    #                 break  # Not pinned, exit loop

    #         except (NoSuchElementException, TimeoutException):
    #             # Element not found => not pinned
    #             break

    #         except StaleElementReferenceException:
    #             # Wait a bit and retry in case DOM updated
    #             sleep(1)
    #             continue


    def __get_tweet_url(self) -> tuple[str, bool]:
        urls = self.tweet.find_elements(By.CSS_SELECTOR, "a")

        if urls[0].get_attribute("href") == urls[1].get_attribute("href"):
            url = urls[3].get_attribute("href")
            re_tweet = False
        else:
            url = urls[4].get_attribute("href")
            re_tweet = True

        return url, re_tweet

    def __get_tweet_date(self) -> str:
        try:
            datetime_str = self.tweet.find_element(By.CSS_SELECTOR, "time").get_attribute("datetime")
            date_time_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            utc_date_time_obj = date_time_obj.replace(tzinfo=pytz.utc)
            ist_tz = pytz.timezone("Asia/Kolkata")
            ist_date_time_obj = utc_date_time_obj.astimezone(ist_tz)
            return ist_date_time_obj.strftime('%d/%m/%Y %H:%M:%S')
        except NoSuchElementException:
            return ""

    def __get_tweet_text(self) -> str:
        try:
            element = self.tweet.find_element(
                By.CSS_SELECTOR, "div[data-testid='tweetText']")
            return element.get_attribute("innerText")
        except NoSuchElementException:
            return ""

    def __get_tweet_lang(self) -> str:
        try:
            video_elements = self.tweet.find_elements(By.TAG_NAME, 'video')
            if video_elements:
                video_url = video_elements[0].get_attribute('poster')
                if video_url:
                    return video_url
                else:
                    return "n/a"
            else:
                return "n/a"
        except Exception as e:
            print(f"Error in __get_Video-Image: {e}")
            return "n/a"
    
    def __get_tweet_post_owner(self) -> str:
        try:
            element = self.tweet.find_element(By.CSS_SELECTOR,"span[class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']")
            return element.text
        except NoSuchElementException:
            return ""
       
    def __get_tweet_user_name(self) -> str:
        try:
            element = self.tweet.find_element(By.CSS_SELECTOR,"a[class='css-175oi2r r-1wbh5a2 r-dnmrzs r-1ny4l3l r-1loqt21']")
            username = str(element.get_attribute('href'))
            return username
        except NoSuchElementException:
            return ""
        
    def __get_tweet_num_likes(self):
        return self.tweet.find_element(By.CSS_SELECTOR, "button[data-testid='like']").get_attribute("innerText")

    def __get_tweet_num_retweet(self):
        return self.tweet.find_element(By.CSS_SELECTOR, "button[data-testid='retweet']").get_attribute("innerText")
    
    def __get_tweet_num_reply(self):
        return self.tweet.find_element(By.CSS_SELECTOR, "button[data-testid='reply']").get_attribute("innerText")


    # def __delete_tweet(self):
    #     self.driver.execute_script("""
    #         var element = arguments[0];
    #         element.parentNode.removeChild(element);
    #         """, self.tweet)

    def __delete_tweet(self):
        if self.tweet:
            self.driver.execute_script("""
                var element = arguments[0];
                if (element && element.parentNode) {
                    element.parentNode.removeChild(element);
                }
            """, self.tweet)
        else:
            print("Tweet element not found, skipping delete.")
