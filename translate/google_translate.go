package translate

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"strings"
	"sync"
	"time"
)

var (
	translationCache = struct {
		sync.RWMutex
		m map[string]string
	}{m: make(map[string]string)}
	lastRequest time.Time
	requestLock sync.Mutex
)

func encodeURI(s string) string {
	return url.QueryEscape(s)
}

func TranslateText(source, sourceLang, targetLang string) (string, error) {
	// Проверяем кэш
	cacheKey := sourceLang + targetLang + source
	translationCache.RLock()
	if cached, exists := translationCache.m[cacheKey]; exists {
		translationCache.RUnlock()
		return cached, nil
	}
	translationCache.RUnlock()

	// Ограничение запросов (1 запрос в секунду)
	requestLock.Lock()
	elapsed := time.Since(lastRequest)
	if elapsed < time.Second {
		time.Sleep(time.Second - elapsed)
	}
	lastRequest = time.Now()
	requestLock.Unlock()

	encodedSource := encodeURI(source)
	url := "https://translate.googleapis.com/translate_a/single?client=gtx&sl=" +
		sourceLang + "&tl=" + targetLang + "&dt=t&q=" + encodedSource

	resp, err := http.Get(url)
	if err != nil {
		return "", fmt.Errorf("error connecting to translate API: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("translate API returned status: %s", resp.Status)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("error reading response: %v", err)
	}

	if strings.Contains(string(body), `<title>Error 400 (Bad Request)`) {
		return "", errors.New("bad request to translate API")
	}

	var result []interface{}
	if err := json.Unmarshal(body, &result); err != nil {
		return "", fmt.Errorf("error parsing response: %v", err)
	}

	if len(result) == 0 {
		return "", errors.New("empty response from translate API")
	}

	var translatedText strings.Builder
	if slice, ok := result[0].([]interface{}); ok {
		for _, item := range slice {
			if pair, ok := item.([]interface{}); ok && len(pair) > 0 {
				if text, ok := pair[0].(string); ok {
					translatedText.WriteString(text)
				}
			}
		}
	}

	if translatedText.Len() == 0 {
		return "", errors.New("no translation found in response")
	}

	// Сохраняем в кэш
	translationCache.Lock()
	translationCache.m[cacheKey] = translatedText.String()
	translationCache.Unlock()

	return translatedText.String(), nil
}
