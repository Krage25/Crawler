import requests
import traceback

def detect_language(contents):
    url = "http://10.226.54.4:6000/langDetect"
    payload = {"content": contents}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()  # Expected: ["hi", "gu", ...]
    except requests.exceptions.RequestException as e:
        print(f"Language detection failed: {e}")
        return []

def translate_text_batch(contents, source_langs):
    url = "http://10.226.54.4:6001/translate"
    payload = {
        "content": contents,
        "source_lang": source_langs
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()  # Expected: list of translated strings
    except requests.exceptions.RequestException as e:
        print(f"Translation request failed: {e}")
        return []

def process_text_pipeline(texts):
    """
    Detects languages for input texts, translates them to English,
    and returns enriched data with language and translation.
    """
    try:
        detected_langs = detect_language(texts)
        print("Detected languages:", detected_langs)

        if not detected_langs or len(detected_langs) != len(texts):
            raise ValueError("Mismatch in detected language count and input count.")

        translations = translate_text_batch(texts, detected_langs)
        print("Translations:", translations)

        results = []
        for i, text in enumerate(texts):
            results.append({
                "content": text,
                "detectedLanguage": detected_langs[i],
                "translation": translations[i] if i < len(translations) else text
            })

        return results
    
    except Exception:
        traceback.print_exc()
        return [{"content": text, "detectedLanguage": None, "translation": text} for text in texts]
