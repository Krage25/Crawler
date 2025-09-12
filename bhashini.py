import json
import requests
from collections import defaultdict
import traceback
import time

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "PostmanRuntime/7.36.3",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

API_URL = "https://anuvaad-backend.bhashini.co.in/v1/pipeline"


def post_with_retries(payload, max_retries=5, delay=2):
    """POST request with retry logic."""
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
            print(f"Attempt {attempt}: Status {response.status_code}")
            if response.ok:
                return response
            else:
                print("Non-OK response, retrying...")
                time.sleep(delay * attempt)
        except requests.exceptions.RequestException as e:
            print(f"Request failed on attempt {attempt}: {e}")
            time.sleep(delay * attempt)
    raise RuntimeError(f"Failed after {max_retries} attempts")


def batch_language_detection(data, batch_size=50):
    """Detect languages in given data array and add 'langCode' and 'scriptCode' keys."""
    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    for batch in chunks(data, batch_size):
        contents = [{"source": item["content"]} for item in batch]
        payload = {
            "inputData": {"input": contents},
            "pipelineTasks": [
                {
                    "taskType": "txt-lang-detection",
                    "config": {
                        "serviceId": "bhashini/indic-lang-detection-all"
                    }
                }
            ]
        }

        response = post_with_retries(payload)
        result = response.json()
        outputs = result["pipelineResponse"][0]["output"]
        for item, output in zip(batch, outputs):
            lang_info = output["langPrediction"][0]
            item["langCode"] = lang_info["langCode"]
            item["scriptCode"] = lang_info["scriptCode"]

    return data


def batch_translation(data, target_lang="en", target_script="Latn"):
    """Translate grouped data per source language."""
    lang_groups = defaultdict(list)
    for item in data:
        key = (item["langCode"], item["scriptCode"])
        lang_groups[key].append(item)

    for (source_lang, source_script), items in lang_groups.items():
        contents = [{"source": item["content"]} for item in items]

        payload = {
            "inputData": {
                "input": contents,
                "audio": []
            },
            "pipelineTasks": [
                {
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": source_lang,
                            "targetLanguage": target_lang,
                            "sourceScriptCode": source_script,
                            "targetScriptCode": target_script
                        },
                        "serviceId": "ai4bharat/indictrans-v2-all-gpu--t4"
                    }
                }
            ]
        }

        response = post_with_retries(payload)
        result = response.json()
        translations = result["pipelineResponse"][0]["output"]
        for item, translation in zip(items, translations):
            item["translated"] = translation["target"]

    return data


def process_text_pipeline(data_array):
    """Process data through detection and translation pipeline with error handling."""
    try:
        detected = batch_language_detection(data_array)
        translated = batch_translation(detected)

        for i in range(len(data_array)):
            data_array[i]["detectedLanguage"] = detected[i]["langCode"]
            data_array[i]["translation"] = detected[i].get("translated", data_array[i]["content"])

        return data_array
    except Exception:
        traceback.print_exc()
        return data_array
