package page

import (
	"html/template"
	"log"
	"net/http"
	"path/filepath"
	"src/db"
	"src/models" // Добавляем импорт models
)

func HomeHandler(w http.ResponseWriter, r *http.Request) {
	newsList, err := db.GetAllNews()
	if err != nil {
		log.Printf("Ошибка загрузки новостей: %v", err)
		http.Error(w, "500 Internal Server Error", http.StatusInternalServerError)
		return
	}

	templates := []string{
		filepath.Join("templates", "header.html"),
		filepath.Join("templates", "index.html"),
		filepath.Join("templates", "footer.html"),
	}

	tmpl, err := template.ParseFiles(templates...)
	if err != nil {
		log.Printf("Ошибка загрузки шаблонов: %v (пути: %v)", err, templates)
		http.Error(w, "500 Internal Server Error", http.StatusInternalServerError)
		return
	}

	data := struct {
		NewsList []models.News // Меняем db.News на models.News
	}{
		NewsList: newsList,
	}

	err = tmpl.ExecuteTemplate(w, "index.html", data)
	if err != nil {
		log.Printf("Ошибка рендеринга шаблона: %v", err)
		http.Error(w, "500 Internal Server Error", http.StatusInternalServerError)
	}
}
