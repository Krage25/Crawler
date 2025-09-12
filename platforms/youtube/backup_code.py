from bs4 import BeautifulSoup
import requests
import threading
import json
import re
from datetime import datetime
from db_model import youtubePosts, scrappedPosts, scrappedPostsTest
import traceback
from requests_html import HTMLSession
from Youtube_Scrapper.bhasini import languageDetection
from LanguageDetectionAndTranslation.INDICLLDModel import languageIdentifier
import pytz
from LanguageDetectionAndTranslation.INDICLLDModel import LanguageDetect
from LanguageTranslator import language_finder

# session = HTMLSession()
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

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
}

proxies = {
    # 'http': 'http://4w67ctv8.pr.thordata.net:9999:td-customer-KeWcX6mfg6ad-sessid-alldl4bm2wlwgeu417-sesstime-10:doEopvf3xrpu',  
    'https': 'https://td-customer-KeWcX6mfg6ad:doEopvf3xrpu@4w67ctv8.pr.thordata.net:9999',
}


def scrapYoutubeVideo(link, sessionId, keyword):
    try:
        print(link)
        response = requests.get(link, headers=headers, proxies=proxies)
        response.raise_for_status()
        soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), 'lxml') 
        allSpan = soup.find_all('span') 
        thumbnail = "n/a"
        try:
            thumbnail_element = soup.find('meta', property='og:image')
            thumbnail = thumbnail_element.get('content', None) if thumbnail_element else None
        except:
            traceback.print_exc()
        
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
        # channel_name = soup.find("span", itemprop="author").next.next['content']
        
        views_element = soup.find('meta', itemprop='interactionCount')
        views_count = views_element['content'] if views_element else None
        
        
        try:
            date_published = soup.find("meta", itemprop="datePublished")['content']
        except:
            pass
    
        hashtags = ', '.join([meta.attrs.get("content") for meta in soup.find_all("meta", {"property": "og:video:tag"})])
        
        final_transcription = "none"
        try:
            for script in soup.find_all('script'):
                if 'captions' in script.text:
                    start = script.text.find('"captionTracks":')
                    end = script.text.find(',"audioTracks"')
                    if start != -1 and end != -1:
                        captions_json = script.text[start:end]
                        start = captions_json.find('[')
                        end = captions_json.find(']')
                        if start != -1 and end != -1:
                            captions_json = captions_json[start:end+1]
                            break

            captions_data = json.loads(captions_json)
            transcription_url = None
            for caption in captions_data:
                if 'baseUrl' in caption:
                    transcription_url = caption['baseUrl']
                    if 'languageCode' in caption and caption['languageCode'] == 'en':
                        break

            if not transcription_url:
                print("No transcription URL found.")
                return

            response = requests.get(transcription_url)
            if response.status_code != 200:
                print("Failed to retrieve transcription.")
                return

            transcript_soup = BeautifulSoup(response.content, 'lxml')
            transcript_text = [text.get_text() for text in transcript_soup.find_all('text')]

            if transcript_text:
                final_transcription = "".join(transcript_text)
        except:
            pass

        channel_subscribers = channel_subscribers if channel_subscribers is not None else "Not available"
        Translation = None

        langauageDetected = None
        def translate_part(text, part_index, results):
            global langauageDetected
            # translation = languageIdentifier(text)
            translation = language_finder(text)
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

        # language_detected = LanguageDetect(video_title)
        # final_lang_detect = lang_code.get(language_detected,"English")

       
        title = "none"
        # try:
        #     title_ = language_finder(video_title)
        #     if title_ is None:
        #         title = "none"
        #     else:
        #         title = title_['translation']
        # except:
        #     traceback.print_exc()
        #     pass
        
        desc = "none"
        # try:
        #     lang_data = language_finder(description)
        #     # print(f"Scrapper : {lang_data['language']}")
        #     if lang_data is None:
        #         desc = "none"
        #     else:
        #         desc = lang_data['translation']
        # except:
        #     traceback.print_exc()
        #     pass
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

        print(f"thumbnail : {thumbnail}")
        print(f"postOwner : {channel_name}")
        print(f"Ttitle : {title}")

        scrappedPosts.insert_one({
            "datetime": datePublished,
            "thumbnail": thumbnail,
            "videoDuration": duration,
            "postOwner": channel_name,
            "channelSubscribers": channel_subscribers,
            "views": views_count,
            # "translation": Translation,
            # "languages": final_lang_detect,
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
            
        })

        return {"status": "success"}
        
    except Exception as e: 
        traceback.print_exc()
        print(f"Error: {str(e)}")
        return {"status": "error", "message": str(e)}
