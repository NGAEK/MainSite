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

func NewsDetailHandler(w http.ResponseWriter, r *http.Request) {
	// Получаем ID из URL
	vars := mux.Vars(r)
	idStr := vars["id"]

	id, err := strconv.Atoi(idStr)
	if err != nil {
		http.Error(w, "Некорректный ID новости", http.StatusBadRequest)
		return
	}

	news, err := db.GetNewsByID(id)
	if err != nil {
		http.Error(w, "Новость не найдена", http.StatusNotFound)
		return
	}

	if news == (models.News{}) {
		http.Error(w, "Новость не найдена", http.StatusNotFound)
		return
	}

	query := r.URL.Query().Get("q")

	data := struct {
		News  models.News
		Query string
	}{
		News:  news,
		Query: query,
	}

	templates := []string{
		filepath.Join("templates", "header.html"),
		filepath.Join("templates", "news_detail.html"),
		filepath.Join("templates", "footer.html"),
	}

	tmpl := template.New("news_detail.html").Funcs(template.FuncMap{
		"safeHTML": func(s string) template.HTML {
			return template.HTML(s)
		},
	})

	tmpl, err = tmpl.ParseFiles(templates...)
	if err != nil {
		log.Printf("Ошибка загрузки шаблонов: %v", err)
		http.Error(w, "500 Внутренняя ошибка сервера", http.StatusInternalServerError)
		return
	}

	err = tmpl.ExecuteTemplate(w, "news_detail.html", data)
	if err != nil {
		log.Printf("Ошибка рендеринга: %v", err)
	}
}
