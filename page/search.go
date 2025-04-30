package page

import (
	"html/template"
	"log"
	"net/http"
	"path/filepath"
	"src/db"
	"src/models"
	"strings"
)

func SearchHandler(w http.ResponseWriter, r *http.Request) {
	query := strings.TrimSpace(r.URL.Query().Get("q"))
	if query == "" {
		http.Redirect(w, r, "/", http.StatusSeeOther)
		return
	}

	results, err := db.SearchNews(query)
	if err != nil {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	tmpl, err := template.ParseFiles(
		filepath.Join("templates", "header.html"),
		filepath.Join("templates", "search", "results.html"),
		filepath.Join("templates", "footer.html"),
	)
	if err != nil {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	data := struct {
		Title   string
		Query   string
		Results []models.News
	}{
		Title:   "Результаты поиска",
		Query:   query,
		Results: results,
	}

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	if err := tmpl.ExecuteTemplate(w, "results.html", data); err != nil {
		log.Printf("Error executing template: %v", err)
	}
}
