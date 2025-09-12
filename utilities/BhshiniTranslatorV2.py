import traceback
import requests
import json

import requests
import traceback

language_code = {
    'hin_Latn' : "Hindi",
    'te_Latn' : "Telugu",
    'mr_Latn' : "Marathi",
    'ml_Latn' : "Malyalam",
    'as_Latn'  : "Assamese",
    'or_Latn' : "Odia",
    'nep_Latn' : "Nepali",
    'gu_Latn' : "Gujarati",
    'ta_Latn' : "Tamil",
    'ur_Latn' : "Urdu",
    'bn_Latn'  : "Bengali",
    'pa_Latn' : "Punjabi",
    'kn_Latn' : "Kannada",
    'ks_Latn' : "Hindi",
    'brx_Latn':"Hindi",
    "san_Latn":"Sanskrit",
    "mai_Latn":"Hindi",
    "mni_Latn" :"Bengali",
    'hi_Deva' : "Hindi",
    'te_Telu' : "Telugu",
    'mr_Deva' : "Marathi",
    'ml_Mlym' : "Malayalam",
    'as_Beng'  : "Assamese",
    'br_or'  : "Hindi",
    'or_Orya' : "Oriya",
    'ne_Deva' : "Nepali",
    "mai_Deva" : "Hindi",
    "pa_Guru" : "Punjabi",
    "gu_Gujr" : "Gujarati",
    "ta_Taml"  : "Tamil",
    "kn_Knda"  : "Kannada",
    "ks_Deva"  : "Hindi",
    "bn_Beng"  : "Bengali",
    "ur_Arab"  : "Urdu",
    "mni_ben_or" : "Manipuri Bengali",
    "mni_or" :"Manipuri",
    "sa_Deva" : "Sanskrit",
    "eng_Latn" :"English",
    "kok_deva" :"Konkani"
}

API_URL = "https://anuvaad-backend.bhashini.co.in/v1/pipeline"

# Common headers to mimic browser request
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://bhashini.gov.in",
    "Referer": "https://bhashini.gov.in/",
    "Connection": "keep-alive"
}

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

def LangDetectComplete(content):
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
        lang_prediction = data["output"][0]["langPrediction"][0]
        lang_code = lang_prediction["langCode"]
        script_code = lang_prediction["scriptCode"]
        joined_string = f"{lang_code}_{script_code}"
        # final_lang = language_code.get(joined_string,"English")
        final_lang = {"lang_code":lang_code,"script_code":script_code}
        return final_lang
    except:
        traceback.print_exc()
        final_lang = {"lang_code":"en","script_code":"Latn"}
        return final_lang
    


def detect_language(content):
    """Function to Detect Language of Text"""
    try:
        payload = {
            "inputData": {
                "input": [
                    {
                        "source": content
                    }
                ]
            },
            "pipelineTasks": [
                {
                    "taskType": "txt-lang-detection",
                    "config": {
                        "serviceId": "bhashini/indic-lang-detection-all"
                    }
                }
            ]
        }

        response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))
        data = response.json()

        # Extracting from correct response structure
        lang_prediction = data["pipelineResponse"][0]["output"][0]["langPrediction"][0]
        lang_code = lang_prediction["langCode"]
        script_code = lang_prediction["scriptCode"]

        final_lang = {"lang_code": lang_code, "script_code": script_code}
        return final_lang

    except Exception:
        traceback.print_exc()
        return {"lang_code": "en", "script_code": "Latn"}

def translation(content):
    try:
        # Detect language
        lang_detected = detect_language(content)
        lang_code = lang_detected['lang_code']
        script_code = lang_detected['script_code']

        print("Source Language:", lang_code)
        print("Source Script Code:", script_code)

        # Prepare Translation Payload
        url = "https://anuvaad-backend.bhashini.co.in/v1/pipeline"
        payload = {
            "inputData": {
                "input": [
                    {
                        "source": content
                    }
                ],
                "audio": []
            },
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": lang_code,
                            "targetLanguage": "en",
                            "sourceScriptCode": script_code,
                            "targetScriptCode": "Latn"
                        },
                        "serviceId": "ai4bharat/indictrans-v2-all-gpu--t4"
                    }
                }
            ]
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://bhashini.gov.in",
            "Referer": "https://bhashini.gov.in/",
            "Connection": "keep-alive"
        }

        # Make Translation Request
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            data = response.json()
            # Extract 'target' text from correct path
            target = data['pipelineResponse'][0]['output'][0]['target']
            return target
        else:
            print(f"Request failed with status code {response.status_code}")
            print(response.text)
            return content

    except Exception:
        traceback.print_exc()
        return content