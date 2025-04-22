package page

import (
	"html/template"
	"log"
	"net/http"
	"path/filepath"
)

func NotFoundHandler(w http.ResponseWriter, r *http.Request) {
	templates := []string{
		filepath.Join("templates", "header.html"),
		filepath.Join("templates", "errors", "404.html"),
		filepath.Join("templates", "footer.html"),
	}

	tmpl, err := template.ParseFiles(templates...)
	if err != nil {
		log.Printf("Ошибка загрузки шаблонов 404: %v (пути: %v)", err, templates)
		http.Error(w, "500 Internal Server Error", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusNotFound)

	data := struct {
		Title string
		Path  string
	}{
		Title: "Страница не найдена",
		Path:  r.URL.Path,
	}

	err = tmpl.ExecuteTemplate(w, "404.html", data)
	if err != nil {
		log.Printf("Ошибка рендеринга шаблона 404: %v", err)
		http.Error(w, "500 Internal Server Error", http.StatusInternalServerError)
	}
}
