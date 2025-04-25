package page

import (
	"context"
	"html/template"
	"log"
	"net/http"
	"path/filepath"
	"src/db"
	"src/models"
	"strings"
)

func HomeHandler(w http.ResponseWriter, r *http.Request) {
	allNews, err := db.GetAllNews()
	if err != nil {
		log.Printf("Ошибка загрузки новостей: %v", err)
		http.Error(w, "500 Internal Server Error", http.StatusInternalServerError)
		return
	}

	query := strings.TrimSpace(r.URL.Query().Get("q"))
	log.Printf("Search query: '%s'", query)

	var filteredNews []models.News
	var isSearchResults bool

	if query != "" {
		isSearchResults = true
		dbResults, err := db.SearchNews(query)
		if err != nil {
			log.Printf("Ошибка поиска в БД: %v", err)
			// Если ошибка в БД, фильтруем локально
			query = strings.ToLower(query)
			for _, news := range allNews {
				if strings.Contains(strings.ToLower(news.Name), query) ||
					strings.Contains(strings.ToLower(news.Description), query) {
					filteredNews = append(filteredNews, news)
				}
			}
		} else {
			filteredNews = dbResults
		}
		log.Printf("Found %d results for query '%s'", len(filteredNews), query)
	} else {
		filteredNews = allNews
		isSearchResults = false
	}

	// Остальной код без изменений
	templates := []string{
		filepath.Join("templates", "header.html"),
		filepath.Join("templates", "index.html"),
		filepath.Join("templates", "footer.html"),
	}

	data := struct {
		NewsList        []models.News
		Query           string
		IsSearchResults bool
		SearchCount     int
	}{
		NewsList:        filteredNews,
		Query:           query,
		IsSearchResults: isSearchResults,
		SearchCount:     len(filteredNews),
	}

	tmpl, err := template.ParseFiles(templates...)
	if err != nil {
		log.Printf("Ошибка загрузки шаблонов: %v (пути: %v)", err, templates)
		http.Error(w, "500 Internal Server Error", http.StatusInternalServerError)
		return
	}

	err = tmpl.ExecuteTemplate(w, "index.html", data)
	if err != nil {
		log.Printf("Ошибка рендеринга шаблона: %v", err)
		http.Error(w, "500 Internal Server Error", http.StatusInternalServerError)
	}
}

func languageMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Определяем язык из cookie или параметра URL
		lang := r.URL.Query().Get("lang")
		if lang == "" {
			if cookie, err := r.Cookie("lang"); err == nil {
				lang = cookie.Value
			} else {
				lang = "ru" // язык по умолчанию
			}
		}

		// Сохраняем язык в контексте запроса
		ctx := context.WithValue(r.Context(), "lang", lang)
		next.ServeHTTP(w, r.WithContext(ctx))

		// Устанавливаем cookie
		http.SetCookie(w, &http.Cookie{
			Name:   "lang",
			Value:  lang,
			Path:   "/",
			MaxAge: 30 * 24 * 60 * 60, // 30 дней
		})
	})
}
