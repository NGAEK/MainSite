package handlers

import (
	"html/template"
	"log"
	"net/http"
	"src/db"
	"src/models"
	"strconv"
)

func HomeHandler(w http.ResponseWriter, r *http.Request) {
	newsList, err := db.GetAllNews()
	if err != nil {
		log.Println(err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	tmpl := template.Must(template.ParseFiles(
		"templates/base.html",
		"templates/header.html",
		"templates/footer.html",
		"templates/index.html",
	))

	data := struct {
		NewsList []models.News
	}{
		NewsList: newsList,
	}

	err = tmpl.ExecuteTemplate(w, "base", data)
	if err != nil {
		log.Println(err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
	}
}

func NewsDetailHandler(w http.ResponseWriter, r *http.Request) {
	idStr := r.URL.Path[len("/news/"):]
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

	tmpl := template.Must(template.ParseFiles(
		"templates/base.html",
		"templates/header.html",
		"templates/footer.html",
		"templates/news_detail.html",
	))

	err = tmpl.ExecuteTemplate(w, "base", news)
	if err != nil {
		log.Println(err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
	}
}
