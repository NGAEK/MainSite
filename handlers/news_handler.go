package handlers

import (
	"html/template"
	"log"
	"net/http"
	"src/db"
	"strconv"
)

func NewsDetailHandler(w http.ResponseWriter, r *http.Request) {
	// Извлекаем ID из URL
	idStr := r.URL.Path[len("/news/"):]
	id, err := strconv.Atoi(idStr)
	if err != nil {
		http.Error(w, "Invalid news ID", http.StatusBadRequest)
		return
	}

	// Проверяем существование новости
	exists, err := db.NewsExists(idStr)
	if err != nil {
		log.Printf("Error checking news existence: %v", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	if !exists {
		http.Error(w, "News not found", http.StatusNotFound)
		return
	}

	// Получаем новость из БД
	news, err := db.GetNewsByID(id)
	if err != nil {
		log.Printf("Error getting news: %v", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	// Проверяем, что новость не пустая
	if news.ID == 0 {
		http.Error(w, "News not found", http.StatusNotFound)
		return
	}

	// Подготавливаем шаблоны
	tmpl, err := template.ParseFiles(
		"templates/base.html",
		"templates/header.html",
		"templates/news_detail.html",
		"templates/footer.html",
	)
	if err != nil {
		log.Printf("Template parsing error: %v", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}

	// Рендерим шаблон
	err = tmpl.ExecuteTemplate(w, "base", news)
	if err != nil {
		log.Printf("Template execution error: %v", err)
		// Не отправляем повторно заголовок ошибки
	}
}
