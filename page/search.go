package page

import (
	"bytes"
	"html/template"
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

	templates := []string{
		filepath.Join("templates", "header.html"),
		filepath.Join("templates", "search", "results.html"),
		filepath.Join("templates", "footer.html"),
	}

	tmpl, err := template.ParseFiles(templates...)
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

	var buf bytes.Buffer
	if err := tmpl.ExecuteTemplate(&buf, "results.html", data); err != nil {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	buf.WriteTo(w)
}
