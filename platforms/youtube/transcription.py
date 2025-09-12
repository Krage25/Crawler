import requests
from bs4 import BeautifulSoup
import traceback
def fetchTranscription(url):
   try:
       # URL to post to
       site = "https://youtubetotranscript.com/transcript"

       # Payload with the YouTube URL
       print(url)
       payload = {
           "youtube_url": url
       }

       # Headers to look like a real browser
       headers = {
           "Content-Type": "application/x-www-form-urlencoded",
           "Origin": "https://youtubetotranscript.com",
           "Referer": "https://youtubetotranscript.com/",
           "User-Agent": (
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
               "AppleWebKit/537.36 (KHTML, like Gecko) "
               "Chrome/138.0.0.0 Safari/537.36"
           ),
       }

       # Make the POST request
       response = requests.post(site, data=payload, headers=headers)
       print(response.status_code)
       # Save the HTML for inspection
       # with open("transcript_page.html", "w", encoding="utf-8") as f:
       #     f.write(response.text)

       # Parse the HTML with BeautifulSoup
       soup = BeautifulSoup(response.text, "html.parser")

       # Find the transcript div
       transcript_div = soup.find("div", id="transcript")

       # Initialize variable
       transcript_text = ""

       if transcript_div:
           # Find all transcript segments
           segments = transcript_div.find_all("span", class_="transcript-segment")
          
           # Extract and join text
           transcript_text = " ".join(
               segment.get_text(strip=True)
               for segment in segments
           )
           print("Transcription Fetched")
           # Print for verification
           return transcript_text
           # print(transcript_text)
       else:
           print("Transcript div not found. Check transcript_page.html for debugging.")
   except:
       return ""
  

import requests
import traceback

def fetch_kome_transcript(video_input: str, format: bool = True) -> str:
   """
   Fetch transcription from Kome.ai transcript API.
   Sends browser-like headers for authenticity.
   """
   try:
       # video_id = extract_video_id(video_input)

       url = "https://kome.ai/api/transcript"
       payload = {
           "video_id": video_input,
           "format": format
       }

       headers = {
           "accept": "application/json, text/plain, */*",
           "accept-encoding": "gzip, deflate, br, zstd",
           "accept-language": "en-US,en;q=0.9",
           "content-type": "application/json",
           "origin": "https://kome.ai",
           "referer": "https://kome.ai/tools/youtube-transcript-generator",
           "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
           "sec-ch-ua-mobile": "?0",
           "sec-ch-ua-platform": '"Windows"',
           "sec-fetch-dest": "empty",
           "sec-fetch-mode": "cors",
           "sec-fetch-site": "same-origin",
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
       }

       response = requests.post(url, json=payload, headers=headers)

       if response.status_code == 200:
           data = response.json()
           return data.get("transcript", "").strip()
       else:
           return f"❌ Error {response.status_code}: {response.text}"

   except Exception:
       traceback.print_exc()
       return "❌ Exception occurred while fetching transcript."


# Now transcript_text variable contains the full transcript

