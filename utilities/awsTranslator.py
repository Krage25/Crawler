import requests
import traceback

def trim_to_30_words(text):
    """
    Trim the input text to the first 30 words.
    """
    # Split the text into a list of words
    words = text.split()
    # Take the first 30 words
    trimmed_words = words[:30]
    # Join them back into a string
    trimmed_text = ' '.join(trimmed_words)    
    return trimmed_text


def detect_language(text: str) -> str:
    url = "http://15.206.70.131:6000/langDetect"
    payload = {"content": [text]}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an error if request fails
        response_data = response.json()  # Parse JSON response
        return response_data[0] if response_data else None
    except Exception as e:
        print(f"Error: {e}")
        return None