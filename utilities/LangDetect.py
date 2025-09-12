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

def LangDetect(content):
    content = trim_to_30_words(content)
    try:
        payload = {
        "modelId": "667fbf02de2e324c2eba1968",
        "task": "txt-lang-detection",
        "input": [
            {
            "source": content
            }
        ],
        "userId": ""
        }
        response = requests.post(
            "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/compute",
            json=payload
        )
        data = response.json()
        print(data)
        lang_prediction = data["output"][0]["langPrediction"][0]
        lang_code = lang_prediction["langCode"]
        script_code = lang_prediction["scriptCode"]
        joined_string = f"{lang_code}_{script_code}"
        print("Language Detected in Lang Func : ",joined_string)
        return joined_string
    except:
        traceback.print_exc()
        return "eng_Latn"
    

