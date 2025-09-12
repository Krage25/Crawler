from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from platforms.youtube.transcription import fetchTranscription
from datetime import datetime
from utilities.LangDetect import LangDetect
from utilities.LanguageTranslator import languageTranslator
from config.db_model import scrappedPosts, youtubeTokens
import traceback
import time

def getToken():
    """Fetch a valid token from MongoDB"""
    try:
        token = youtubeTokens.find_one({"hasCapacity": "true"})
        if token:
            return token['authKey']
        else:
            raise Exception("No valid API key left in MongoDB")
    except:
        traceback.print_exc()

def markTokenExhausted(api_key):
    """Mark the given API key as exhausted in MongoDB"""
    youtubeTokens.update_one(
        {"authKey": api_key},
        {"$set": {"hasCapacity": "false"}}
    )

def build_youtube_client(api_key):
    return build("youtube", "v3", developerKey=api_key)

def youtube_search_with_comments(query: str, total_results: int = 100, max_comments: int = 20):
    results = []
    next_page_token = None
    api_key = getToken()
    youtube = build_youtube_client(api_key)

    while len(results) < total_results:
        try:
            max_fetch = min(50, total_results - len(results))

            search_response = youtube.search().list(
                q=query,
                part="id,snippet",
                type="video",
                maxResults=max_fetch,
                order="date",
                pageToken=next_page_token
            ).execute()

            for item in search_response.get("items", []):
                video_id = item["id"]["videoId"]

                # Get video details
                video_response = youtube.videos().list(
                    part="snippet,statistics,contentDetails",
                    id=video_id
                ).execute()

                if not video_response["items"]:
                    continue
                video_info = video_response["items"][0]
                thumbnail_url = video_info["snippet"]["thumbnails"]["high"]["url"]
                
                transcription_ = video_info["snippet"]["description"]
                try:
                    transcription_ = fetchTranscription(f"https://www.youtube.com/watch?v={video_id}")
                except:
                    pass

                languageDetection = LangDetect(transcription_)
                titleTranslation = languageTranslator(video_info["snippet"]["title"])
                descTranslation = languageTranslator(video_info["snippet"]["description"])
                transcriptionTranslation = languageTranslator(transcription_)
                content = [
                    {"title": video_info["snippet"]["title"], "translation": titleTranslation},
                    {"description": video_info["snippet"]["description"], "translation": descTranslation},
                    {"transcription": transcription_, "translation": transcriptionTranslation}
                ]
                video_data = {
                    "videoId": video_id,
                    "title": video_info["snippet"]["title"],
                    "description": video_info["snippet"]["description"],
                    "postOwner": video_info["snippet"]["channelTitle"],
                    "datePublished": video_info["snippet"]["publishedAt"],
                    "hashtags": video_info["snippet"].get("tags", []),
                    "duration": video_info["contentDetails"]["duration"],
                    "views": video_info["statistics"].get("viewCount"),
                    "likes": video_info["statistics"].get("likeCount"),
                    "commentCount": video_info["statistics"].get("commentCount"),
                    "comments": [],
                    "content": content,
                    "languages": languageDetection,
                    "link": f"https://www.youtube.com/watch?v={video_id}",
                    "crawlTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "screenshotUrl": thumbnail_url
                }

                # Fetch top-level comments
                try:
                    comments_response = youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        maxResults=max_comments,
                        textFormat="plainText"
                    ).execute()

                    for c in comments_response.get("items", []):
                        top_comment = c["snippet"]["topLevelComment"]["snippet"]
                        video_data["comments"].append({
                            "author": top_comment["authorDisplayName"],
                            "text": top_comment["textDisplay"],
                            "publishedAt": top_comment["publishedAt"],
                            "likeCount": top_comment["likeCount"]
                        })
                except Exception:
                    video_data["comments"] = ["Comments disabled or unavailable"]

                results.append(video_data)

            # Update page token for next loop
            next_page_token = search_response.get("nextPageToken")
            if not next_page_token:
                break  

        except HttpError as e:
            if e.resp.status == 403 and ("quotaExceeded" in str(e) or "RESOURCE_EXHAUSTED" in str(e)):
                print(f"🚨 Quota exhausted for key: {api_key}")
                markTokenExhausted(api_key)
                api_key = getToken()       
                youtube = build_youtube_client(api_key)  
                time.sleep(1)  
                continue
            else:
                traceback.print_exc()
                break

    # Insert into DB at the end
    if results:
        scrappedPosts.insert_many(results, ordered=False)
    return results


# Example usage
data = youtube_search_with_comments("Modi Vote Chor", total_results=500, max_comments=10)
print(f"Fetched {len(data)} videos")
