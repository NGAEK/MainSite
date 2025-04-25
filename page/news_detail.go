package page

import (
	"github.com/gorilla/mux"
	"html/template"
	"log"
	"net/http"
	"path/filepath"
	"src/db"
	"src/models"
	"strconv"
)

func NewsDetailHandler(w http.ResponseWriter, r *http.Request, id int) {
	idStr := mux.Vars(r)["id"]
	id, err := strconv.Atoi(idStr)
	if err != nil {
		http.Error(w, "Invalid news ID", http.StatusBadRequest)
		return
	}

	news, err := db.GetNewsByID(id)
	if err != nil {
		http.Error(w, "News not found", http.StatusNotFound)
		return
	}

	// Получаем параметр запроса q, если он есть в URL
	query := r.URL.Query().Get("q")

	// Подготавливаем данные для передачи в шаблон
	data := struct {
		News  models.News
		Query string // Добавляем поле Query для хранения поискового запроса
	}{
		News:  news,
		Query: query, // Записываем поисковый запрос в структуру данных
	}

	templates := []string{
		filepath.Join("templates", "header.html"),
		filepath.Join("templates", "news_detail.html"),
		filepath.Join("templates", "footer.html"),
	}

	tmpl, err := template.ParseFiles(templates...)
	if err != nil {
		log.Printf("Ошибка загрузки шаблонов: %v", err)
		http.Error(w, "500 Internal Server Error", http.StatusInternalServerError)
		return
	}

	// Передаем данные в шаблон
	err = tmpl.ExecuteTemplate(w, "news_detail.html", data)
	if err != nil {
		log.Printf("Ошибка рендеринга шаблона: %v", err)
		http.Error(w, "500 Internal Server Error", http.StatusInternalServerError)
	}
}
