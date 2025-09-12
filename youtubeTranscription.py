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

# Example usage:
result = fetch_kome_transcript("https://www.youtube.com/shorts/YapVVJVdNc4++3", True)
print(result)