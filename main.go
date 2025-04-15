package main

import (
	"github.com/gorilla/mux"
	"log"
	"net/http"
	"src/config"
	"src/db"
)

func main() {
	cfg, err := config.LoadConfig("config.yml")
	if err != nil {
		log.Fatalf("Ошибка загрузки конфигурации: %v", err)
	}

	db.InitDB(cfg.Database.User, cfg.Database.Password, cfg.Database.Host,
		cfg.Database.Port, cfg.Database.Name)

	r := mux.NewRouter()

	fs := http.FileServer(http.Dir("static"))
	r.PathPrefix("/static/").Handler(http.StripPrefix("/static/", fs))

	jsFs := http.FileServer(http.Dir("js"))
	r.PathPrefix("/js/").Handler(http.StripPrefix("/js/", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/javascript")
		jsFs.ServeHTTP(w, r)
	})))

	RoutersLoad(r)

	log.Printf("Сервер запущен на http://localhost%s", cfg.Server.Port)
	if err := http.ListenAndServe(cfg.Server.Port, r); err != nil {
		log.Fatal(err)
	}
}
