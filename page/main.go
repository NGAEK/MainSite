package page

import (
	"html/template"
	"log"
	"net/http"
	"path/filepath"
)

func HomeHandler(w http.ResponseWriter, r *http.Request) {
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

	err = tmpl.ExecuteTemplate(w, "index.html", nil)
	if err != nil {
		log.Printf("Ошибка рендеринга шаблона: %v", err)
		http.Error(w, "500 Internal Server Error", http.StatusInternalServerError)
	}
}
