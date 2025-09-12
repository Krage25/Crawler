import traceback
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utilities.LanguageTranslator import languageTranslator
from utilities.LanguageTranslator import languageDetection

def extract_reddit_data(link,driver, sessionId, keyword,username):
    print(link)
    final_results = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
            "DNT": "1",  # Do Not Track
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1"
        }
        # link = "https://old.reddit.com/r/BJPSupremacy/comments/1h0w2vj/sambhal_police_have_released_pictures_of_muslim/"
        response = requests.get(link, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch page: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        
        content = "Not Available"
        try:
            topic = soup.find("a", class_="title")
            content = topic.text.strip()
        except:
            pass
        
        comments = 0
        try:
            comments_divs = soup.find_all("div", class_="md")
            comments = [div.text.strip() for div in comments_divs if div.text.strip()]
        except:
            pass
        
        likes = 0
        try:
            likes = soup.find('div',class_="score likes").text.strip()
        except:
            pass
        
        imageLink = "n/a"
        try:
            imageLink = soup.find('meta', property='og:image')['content']
            # image = soup.find('img', class_="preview")
            # if image and 'src' in image.attrs:
            #     imageLink = image['src']
        except:
            pass
        
        datetime_ = datetime.now()  
        try:
            time_tag = soup.find('time')
            if time_tag and 'datetime' in time_tag.attrs:
                datetime_value = time_tag['datetime']
                print("Datetime value:", datetime_value)
                # datetime = datetime.fromisoformat(datetime_value)
                datetime_ = datetime.fromisoformat(datetime_value)
                # datetime_ = datetime.strptime(datetime_value, '%Y-%m-%dT%H:%M:%S%z')
                
            else:
                print("Time tag or 'datetime' attribute not found.")
        except:
            pass
        
        postOwner = "Not Available"
        try:
            # postOwner = soup.find('a',class_='author may-blank id-t2_4b577xjv').text.strip()
            p_tag = soup.find('p', class_='tagline')
            a_tag = p_tag.find('a') if p_tag else None
            postOwner = a_tag.text
        except:
            pass

        translation = content
        try:
            response_data = languageTranslator(content)
            translation = response_data.json()
            print(f"Language Translation : {translation}")
        except:
                 pass
        
        languageDetected = "English"
        try:
            languageDetected= languageDetection(content)
        except:
            pass
        
        redditName = "Not Available"
        try:
            span_tag = soup.find('span', class_='hover pagename redditname')
            a_tag = span_tag.find('a') if span_tag else None
            redditName = a_tag.text
        except:
            pass
        
        final_results.append({
                    "content":content,
                    "link": link,
                    "imageLink":imageLink,
                    "postOwner":postOwner,
                    "sessionId":sessionId,
                    "keyword":keyword,
                    "likes":likes,
                    "comments":comments,
                    "platform":"reddit",
                    "datetime":datetime_,
                    "status":1,
                    "translation":translation,
                    "languages":languageDetected,
                    "translation":translation,
                    "reddit":redditName,
                    "crawlTime":datetime.now(),
                    "user":username
                    })
        return final_results
    except Exception as e:
        traceback.print_exc()



