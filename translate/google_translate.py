import json
import time
import urllib.parse
import urllib.request
from threading import Lock

_translation_cache = {}
_cache_lock = Lock()
_last_request_time = 0
_request_lock = Lock()


def translate_text(source, source_lang, target_lang):
    """Переводит текст с помощью Google Translate API"""
    global _translation_cache, _last_request_time
    
    # Проверяем кэш
    cache_key = f"{source_lang}{target_lang}{source}"
    with _cache_lock:
        if cache_key in _translation_cache:
            return _translation_cache[cache_key]
    
    # Ограничение запросов (1 запрос в секунду)
    with _request_lock:
        elapsed = time.time() - _last_request_time
        if elapsed < 1.0:
            time.sleep(1.0 - elapsed)
        _last_request_time = time.time()
    
    # Кодируем текст для URL
    encoded_source = urllib.parse.quote(source)
    url = (f"https://translate.googleapis.com/translate_a/single?"
           f"client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={encoded_source}")
    
    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                raise Exception(f"Translate API returned status: {response.status}")
            
            body = response.read().decode('utf-8')
            
            if '<title>Error 400 (Bad Request)' in body:
                raise Exception("Bad request to translate API")
            
            result = json.loads(body)
            
            if not result or len(result) == 0:
                raise Exception("Empty response from translate API")
            
            translated_text = ""
            if isinstance(result[0], list):
                for item in result[0]:
                    if isinstance(item, list) and len(item) > 0:
                        if isinstance(item[0], str):
                            translated_text += item[0]
            
            if not translated_text:
                raise Exception("No translation found in response")
            
            # Сохраняем в кэш
            with _cache_lock:
                _translation_cache[cache_key] = translated_text
            
            return translated_text
    
    except Exception as e:
        raise Exception(f"Error translating text: {e}")

