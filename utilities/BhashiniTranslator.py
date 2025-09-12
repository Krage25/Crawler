import requests
import traceback
# from LanguageDetectionAndTranslation.IP import home, office, sundaram
import re
from utilities.LangDetect import LangDetect


lang_code = {
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
    'hin_Deva' : "Hindi",
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

model_select_Eng_To_Native = {
    # 'hin_Latn' : "641d1d6592a6a31751ff1f49",
    'hi_Latn':"6568524900d64169e2f8f3de",
    'brx_Latn':"6568524900d64169e2f8f3de",
    'te_Latn' : "63b2837886369150cb004368",
    'mr_Latn' : "641d1d7c8ecee6735a1b37c3",
    'ml_Latn' : "641d1c6c8ecee6735a1b36d1",
    'as_Latn'  : "641d1cc98ecee6735a1b371e",
    'br_Latn'  : "641d1c738ecee6735a1b36d6",
    'or_Latn' : "641d1dd98ecee6735a1b380c",
    'nep_Latn' : "641d1cf58ecee6735a1b3749",
    # 'kas_Latn' : "641d1d258ecee6735a1b377a",
    'ks_Latn' : "6568524900d64169e2f8f3de",

    'mni_Latn' : "641d1d2a8ecee6735a1b377e",
    'gu_Latn' : "63b286efff7cd87a3f7e1031",
    'snd_Latn' : "641d1d3092a6a31751ff1f1f",
    'ta_Latn' : "641d1caa92a6a31751ff1eb6",
    'kn_Latn' : "641d1c788ecee6735a1b36db",
    'ur_Latn' : "641d1c778ecee6735a1b36da",
    'mai_Latn' : "641d1d6f8ecee6735a1b37b7",
    'bn_Latn'  : "641d1d818ecee6735a1b37c7",
    'pa_Latn' : "63b2883aff7cd87a3f7e104a",
    'doi_Latn' : "641d1db68ecee6735a1b37ee",
    'san_Latn' : "641d1cc98ecee6735a1b371d",
    'eng_Latn' : "6568524900d64169e2f8f3de",
    'kok_Latn' : "641d1d6592a6a31751ff1f49"
}

model_select_Native_To_English = {
    'hi_Deva' : "6568531600d64169e2f8f3e5",
    'te_Telu' : "641d1ca98ecee6735a1b3707",
    'mr_Deva' : "640cab922bd49460ce02ffd3",
    'ml_Mlym' : "641d1d1392a6a31751ff1f05",
    'as_Beng'  : "641d1d1a92a6a31751ff1f0c",
    'br_or'  : "63b286b286369150cb004369",
    'or_Orya' : "641d1d058ecee6735a1b375c",
    'ne_Deva' : "63b286b286369150cb004369",
    "mai_Deva" : "6568531600d64169e2f8f3e5",
    "pa_Guru" : "641d1d8392a6a31751ff1f63",
    "gu_Gujr" : "641d1c9392a6a31751ff1ea0",
    "ta_Taml"  : "641d1d2d92a6a31751ff1f1d",
    "kn_Knda"  : "641d1d6392a6a31751ff1f48",
    "bn_Beng"  : "641d1d3e8ecee6735a1b3793",
    "ur_Arab"  : "641d1d9a8ecee6735a1b37d9",
    "mni_ben_or" : "641d1d1b8ecee6735a1b3770",
    "mni_or" :"641d1d108ecee6735a1b3766",
    "sa_Deva" : "6568531600d64169e2f8f3e5",
    # "san_or" : "641d1d1d92a6a31751ff1f0f",
    "mr_or" :"641d1cc792a6a31751ff1ed4",
    "ks_Arab" : "63b286b286369150cb004369",
    "kok_Deva" :"6568531600d64169e2f8f3e5",
    "sd_Arab" :"6568531600d64169e2f8f3e5",
    "doi_or" :"6568531600d64169e2f8f3e5"
}


def NativeToEnglish(lang,content):
    try:    
        url = "https://tts.bhashini.ai/v1/translate"
        payload = {
        "inputLanguage": lang,
        "inputText": content,
        "outputLanguage": "English"
        }
        response = requests.post(url, json=payload)
        response_data = response.text
        return response_data
    except Exception as e:
        traceback.print_exc()

def BhashiniAPICall(data,id):
    url = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/compute"
    payload = {
    "modelId": id,
    "task": "translation",
    "input": [
        {
            "source": data
        }
    ],
    "userId": "4d5a1f7239b6473aae5052ce94f4767c",
    "ulcaApiKey" : "0375133ace-e22a-4e05-9ee4-94a13b6741d8"
    }
    response = requests.post(url, json=payload)
    response_data = response.json()
    return response_data['output'][0]['target']

# def LanguageDetect(content):
#     cleaned_text = re.sub(r'#\w+', '', content)
#     cleaned_content =  cleaned_text.strip()
#     payload = {
#        "content":cleaned_content
#             }
#     url = "http://10.226.53.238:6000/langDetect"
#     response = requests.post(url, json=payload)
#     response_data = response.json()
#     languageDetected =  selectLang(response_data)
#     print(languageDetected)
#     return languageDetected

def checkLangauge(content):
    english_pattern = re.compile(r'[a-zA-Z0-9\s,.!?\'\"-]+')
    devanagari_pattern = re.compile(r'[\u0900-\u097F\s]+')
    english_text = ' '.join(english_pattern.findall(content))
    devanagari_text = ' '.join(devanagari_pattern.findall(content))

def languageIdentifier(content):
    try:
        languageDetected = LangDetect(content)
        print("Language Detected : ",languageDetected)
    except:
        pass
    try:
       if languageDetected=='en_Latn':
            return content  
       if languageDetected[-4:] == "Latn":
            # modelId = model_select_Eng_To_Native.get(languageDetected,"Model Not Found")
            modelId = "6568524900d64169e2f8f3de"
            output =   BhashiniAPICall(content,modelId)
            data = languageIdentifier(output)
            if data:
                return data
            translated_content = "none"
            if languageDetected in lang_code:
                language = lang_code[languageDetected]
                output2 = NativeToEnglish(language, output)
                translated_content = "none"
                if output2 is not None:
                    translated_content=output2
            if languageDetected=='en_Latn':
                translated_content=content
                return  translated_content 
                
            return translated_content
       else:
            modelId = model_select_Native_To_English.get(languageDetected,"Model Not Found")
            output_ =  BhashiniAPICall(content,modelId)
            print("Output Non Latn :",output_)
            # translated_content ="none"
            # if output is not None:
            #     translated_content = output
            # language = lang_code.get(languageDetected,"Model Not Found")
            return output_
    except Exception as e:
       print("Error Happened")
       traceback.print_exc()
       return content
