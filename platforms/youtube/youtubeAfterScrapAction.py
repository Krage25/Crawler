from bs4 import BeautifulSoup
import requests
import threading
import json
import re
from datetime import datetime
from config.db_model import youtubePosts, scrappedPosts, scrappedPostsTest
import traceback
from requests_html import HTMLSession
import pytz
from utilities.LanguageTranslator import languageDetection
from utilities.LanguageTranslator import languageTranslator
from platforms.youtube.transcription import fetchTranscription
session = HTMLSession()
API_KEY = "0375133ace-e22a-4e05-9ee4-94a13b6741d8"
ID = "4d5a1f7239b6473aae5052ce94f4767c"
lang_code = {
    'hin_Latn' : "Hindi",
    'tel_Latn' : "Telugu",
    'mar_Latn' : "Marathi",
    'mal_Latn' : "Malayalam",
    'as_Latn'  : "Assamese",
    'ori_Latn' : "Odia",
    'nep_Latn' : "Nepali",
    'guj_Latn' : "Gujarati",
    'tam_Latn' : "Tamil",
    'urd_Latn' : "Urdu",
    'bn_Latn'  : "Bengali",
    'pan_Latn' : "Punjabi",
    'kan_Latn' : "Kannada",
    'br_Latn':"Hindi",
    "san_Latn":"Sanskrit",
    "mai_Latn":"Hindi",
    "mni_Latn" :"Bengali",
    'hin_or' : "Hindi",
    'tel_or' : "Telugu",
    'mar_or' : "Marathi",
    'ml_or' : "Malayalam",
    'as_or'  : "Assamese",
    'br_or'  : "Hindi",
    'or_or' : "Oriya",
    'nep_or' : "Nepali",
    "mai_or" : "Hindi",
    "pan_or" : "Punjabi",
    "guj_or" : "Gujarati",
    "ta_or"  : "Tamil",
    "kn_or"  : "Kannada",
    "bn_or"  : "Bengali",
    "ur_or"  : "Urdu",
    "mni_ben_or" : "Manipuri Bengali",
    "mni_or" :"Manipuri",
    "san_or" : "Sanskrit",
    "eng_Latn" :"English",
    "kok_Latn" :"Hindi"
}

proxies = {
    # 'http': 'http://4w67ctv8.pr.thordata.net:9999:td-customer-KeWcX6mfg6ad-sessid-alldl4bm2wlwgeu417-sesstime-10:doEopvf3xrpu',  
    'https': 'https://td-customer-KeWcX6mfg6ad:doEopvf3xrpu@4w67ctv8.pr.thordata.net:9999',
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.119 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/",
    "Upgrade-Insecure-Requests": "1",
}
def scrapYoutubeVideo(link, sessionId, keyword,username,IP):
    final_data =[]
    try:
        print(link)
        try:
            if IP:
                print("Using Proxy IP")
                response = requests.get(link, proxies={'https': IP}, timeout=25)
            else:
                my_ip = requests.get('https://api.ipify.org').text
                print(f"My Public IP (non-proxy): {my_ip}")
                response = requests.get(link, timeout=25, headers=headers)
        except:
            print("Request timed out. Try again later or handle the retry logic.")
            return "Crawling Failed",500
              
        soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), 'lxml') 
     
        allSpan = soup.find_all('span') 
        thumbnail_element = soup.find('meta', property='og:image')
        thumbnail = thumbnail_element.get('content', None) if thumbnail_element else None
        
        pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')
        description_matches = pattern.findall(str(soup))
        description = description_matches[0].replace('\\n', '\n') if description_matches else None
        
        channel_subscribers = "none"
        try:
            data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)  
            data_json = json.loads(data)
        except:
            pass

        try:
            if 'contents' in data_json:
                videoSecondaryInfoRenderer = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']
                channel_subscribers = videoSecondaryInfoRenderer['owner']['videoOwnerRenderer']['subscriberCountText']['accessibility']['accessibilityData']['label']
        except:
            pass

        title_element = soup.find('meta', property='og:title')
        video_title = title_element['content'] if title_element else None
        
        checkDuration = soup.find('span', class_='ytp-time-duration')
        duration = checkDuration.text if checkDuration else "na"
        
        channel_name = "none"
        try:
            channel_tag = soup.find('link', itemprop='name')
            channel_name = channel_tag['content']
        except:
            pass
        
        views_element = soup.find('meta', itemprop='interactionCount')
        views_count = views_element['content'] if views_element else None
        
        try:
            date_published = soup.find("meta", itemprop="datePublished")['content']
        except:
            pass
    
        hashtags = ', '.join([meta.attrs.get("content") for meta in soup.find_all("meta", {"property": "og:video:tag"})])
        
        final_transcription = "none"
        try:
            final_transcription= fetchTranscription(link)
        except:
            pass

        # try:
        #     for script in soup.find_all('script'):
        #         if 'captions' in script.text:
        #             start = script.text.find('"captionTracks":')
        #             end = script.text.find(',"audioTracks"')
        #             if start != -1 and end != -1:
        #                 captions_json = script.text[start:end]
        #                 start = captions_json.find('[')
        #                 end = captions_json.find(']')
        #                 if start != -1 and end != -1:
        #                     captions_json = captions_json[start:end+1]
        #                     break

        #     captions_data = json.loads(captions_json)
        #     transcription_url = None
        #     for caption in captions_data:
        #         if 'baseUrl' in caption:
        #             transcription_url = caption['baseUrl']
        #             if 'languageCode' in caption and caption['languageCode'] == 'en':
        #                 break
        #     if not transcription_url:
        #         print("No transcription URL found.")
        #         return
        #     response = requests.get(transcription_url)
        #     if response.status_code != 200:
        #         print("Failed to retrieve transcription.")
        #         return

        #     transcript_soup = BeautifulSoup(response.content, 'lxml')
        #     transcript_text = [text.get_text() for text in transcript_soup.find_all('text')]

        #     if transcript_text:
        #         final_transcription = "".join(transcript_text)
        # except:
        #     pass

        channel_subscribers = channel_subscribers if channel_subscribers is not None else "Not available"
        Translation = None

        langauageDetected = None
        def translate_part(text, part_index, results):
            global langauageDetected
            # translation = languageIdentifier(text)
            translation = languageTranslator(text)
            # data = translation['language']
            langauageDetected = data
            results[part_index] = translation['translation']

        if final_transcription != "none":
            length = len(final_transcription)
            part_size = length // 3
            parts = [
                final_transcription[:part_size],
                final_transcription[part_size:2*part_size],
                final_transcription[2*part_size:]
            ]

            results = {}
            threads = []

            for i in range(3):
                thread = threading.Thread(target=translate_part, args=(parts[i], i, results))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            if all(i in results for i in range(3)):
                Translation = ''.join(results[i] for i in range(3))
            else:
                print("Translation results are incomplete.")
                Translation = "none"
        else:
            Translation = final_transcription
        language_detected = "English"
        try:
            language_detected = languageDetection(video_title)
        except:
            language_detected="English"
            pass
        
       
        title = "none"
        try:
            title_ = languageTranslator(video_title)
            if title_ is None:
                title = "none"
            else:
                title = title_['translation']
        except:
            traceback.print_exc()
            pass

        print(f"Test Title :{title} ")
        
        desc = "none"
        try:
            lang_data = languageTranslator(description)
            if lang_data is None:
                desc = "none"
            else:
                desc = lang_data['translation']
        except:
            traceback.print_exc()
            pass
        print(f"Test :{desc}")

        if Translation=="none":
            Translation=title

        content = [{'title': video_title, 'translation': title}, {"description": description, "translation": desc}, {"transcription": final_transcription, "translation": Translation}]
        
        datePublished = "none"
        try:
            date_obj = datetime.fromisoformat(date_published)
            datePublished = date_obj.astimezone(pytz.utc)
        except:
            pass

        final_data.append({
            "datetime": datePublished,
            "thumbnail": thumbnail,
            "videoDuration": duration,
            "postOwner": channel_name,
            "channelSubscribers": channel_subscribers,
            "views": views_count,
            # "translation": Translation,
            "languages": language_detected,
            'hashtags': hashtags,
            "datetime": datetime.now(),
            "link": link,
            "sessionId": sessionId,
            "platform": "youtube",
            "keyword": keyword,
            "content": content,
            # "metadata":title+description+Translation+desc+final_transcription,
            "crawlTime":datetime.now(),
            "screenshotUrl": thumbnail,
            "status":1,  
            "username":username,
            "text":Translation
        })
        return final_data
        
    except Exception as e: 
        traceback.print_exc()
        return []
