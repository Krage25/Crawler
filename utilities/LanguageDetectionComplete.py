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
        final_lang = language_code.get(joined_string,"English")
        return final_lang
    except:
        traceback.print_exc()
        return "English"
    

