import re
import traceback
import requests

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
    'or_or' : "Odia",
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
    "kok_Latn" :"Hindi",
    "tam_Tamil" : "Tamil",
    "mni_Meti":"English"
}

def languageDetection(content):
    try:
        # Replace newlines with spaces and strip extra whitespace
        clean_content = " ".join(content.split())


        IP = "http://15.206.70.131:6000/langDetect"
        payload = {"content": [clean_content]}


        response = requests.post(IP, json=payload, timeout=10)
        response.raise_for_status() # raise error if status != 200


        response_data = response.json()
        language = response_data
        print(f"Language : {language[0]}")
        return lang_code.get(language[0], "English")


    except Exception:
        traceback.print_exc()
        return "English"

def languageTranslator(content):
    # return content
    clean_content = " ".join(content.split())
    try:
        # IP = "http://10.226.42.111:5001/langDetect"
        # IP = "http://10.226.53.238:6000/langDetect"
        IP = "http://15.206.70.131:6000/langDetect"
        payload = {
                "content":[clean_content]
                }
        response = requests.post(IP, json=payload)
        response_data = response.json()
        
        if response_data[0]=='eng_Latn':
           return content

        # Trans_IP =  "http://10.226.53.238:6001/translate"
        # Trans_IP =  "http://10.226.33.176:5001/translate"
        Trans_IP = "http://15.206.70.131:6001/translate"
        payload2 = {
            "source_lang":response_data[0],"content":[clean_content]
                    }
        response2 = requests.post(Trans_IP, json=payload2)
        response_language = response2.json()
        print(f"Translated : {response_language[0]}")
        return response_language[0]
    except:
        print(f"Error for String {content}")
        return content

def process_large_text(data):
    
        # Split the words into chunks of 100 words each
        chunks = [' '.join(data[i:i + 100]) for i in range(0, len(data), 1000)]
        
        # Translate each chunk and store the results
        translated_chunks = []
        for chunk in chunks:
            # Translate the chunk
            data_output = languageTranslator(chunk.strip())
            
            # Check if the translation is empty or None
            if data_output == "" or data_output is None:
                translated_chunks.append(chunk)  # Use the original chunk
            else:
                translated_chunks.append(data_output)
        
        # Join the translated chunks back in order
        final_translation = ' '.join(translated_chunks)
        return {"translation": final_translation}

def is_punctuation(word):
    """Checks if a given word is a punctuation mark."""
    return word[0] in [".", ",", "?", "!", "|", "$", "#","-",":",";","&","^","%","+","*","(",")","[","]","{","}","/","=","_","@","-"]

def is_hindi_char(char):
   
    return '\u0900' <= char[0] <= '\u097F'

def is_english_char(char):
    return 'A' <= char[0] <= 'Z' or 'a' <= char <= 'z'

def is_kannada_char(char):
    return '\u0C80' <= char[0] <= '\u0CFF'

def is_assamese_char(char):
    return '\u0980' <= char[0] <= '\u09FF'
def is_tamil_char(char):
    return '\u0B80' <= char[0] <= '\u0BFF'

def is_malayalam_char(char):
    return '\u0D00' <= char[0] <= '\u0D7F'
def is_telugu_char(char):
    return '\u0C00' <= char[0] <= '\u0C7F'
def is_urdu_char(char):
    return '\u0600' <= char[0] <= '\u06FF'
def is_punjabi_char(char):
    return '\u0A00' <= char[0] <= '\u0A7F'
def is_gujarati_char(char):
    return '\u0A80' <= char[0] <= '\u0AFF'
def is_marathi_char(char):
    return '\u0900' <= char[0] <= '\u097F'
def is_odia_char(char):
    return '\u0B00' <= char[0] <= '\u0B7F'


def is_emoticon(text):
    """Check if a given string contains an emoticon."""
    for char in text:
        if (
            '\U0001F600' <= char <= '\U0001F64F'
            or '\U0001F300' <= char <= '\U0001F5FF'
            or '\U0001F680' <= char <= '\U0001F6FF'
            or '\U0001F900' <= char <= '\U0001F9FF'
            or '\U00002600' <= char <= '\U000026FF'
        ):
            return True
    return False


def detect_language(word):
    if is_hindi_char(word):
        return "Hindi"
    elif is_english_char(word):
        return "English"
    elif is_kannada_char(word):
        return "Kannada"
    elif is_assamese_char(word):
        return "Assamese"
    elif is_tamil_char(word):
        return "Tamil"
    elif is_malayalam_char(word):
        return "Malayalam"
    elif is_telugu_char(word):
        return "Telugu"
    elif is_urdu_char(word):
        return "Urdu"
    elif is_punjabi_char(word):
        return "Punjabi"
    elif is_gujarati_char(word):
        return "Gujrati"
    elif is_marathi_char(word):
        return "Marathi"
    elif is_odia_char(word):
        return "Odia"
    else:
        return "mixed"     

def language_finder(data):
    # return {"translation": data}
    """
    Detects languages in a given sentence and translates mixed language content
    to a single language.

    Args:
        data (str): The input sentence to be processed.

    Returns:
        dict: A dictionary containing the most dominant language and the translated sentence.
    """
    sentence = data
    words = sentence.split()
    current_sentence = ""
    current_language = None
    translated = ""
    languages = []

    if len(words) > 300:
        print("Length Is Big")
        # # data_output = languageIdentifier(data.strip())
        # data_output = languageTranslator(data.strip())
        # if data_output=="" or data_output is None:
        #     return {"translation": data}
        # return {"translation": data_output}
        result = process_large_text(words)
        return result

    for word in words:
        if word.startswith("http://") or is_emoticon(word) or is_punctuation(word) or word[0]=='#' or word[0]=='"' or word[0]=='@' or 'http' in word or word[0].isdigit() or "(" in word[0] or "'" in word[0]:
            # translated += word + " "
            continue

        detected_language = detect_language(word)
        if detected_language not in languages and detected_language != "mixed":
            languages.append(detected_language)

        if current_language is None:
            current_language = detected_language

        if detected_language == current_language:
            current_sentence += word + " "
        else:
            data_output = languageTranslator(current_sentence.strip())
            try:
                translated += data_output + " "
            except:
                pass
            current_sentence = word + " "
            current_language = detected_language

    if current_sentence:
        data_output = languageTranslator(current_sentence.strip())
        try:
            translated += data_output
        except:
            pass
    if translated=="" or translated is None:
        translated=data
    return {"translation": translated}

