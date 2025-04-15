package main

import (
	"github.com/gorilla/mux"
	"log"
	"net/http"
)

func main() {
	r := mux.NewRouter()

	fs := http.FileServer(http.Dir("static"))
	r.PathPrefix("/static/").Handler(http.StripPrefix("/static/", fs))

	jsFs := http.FileServer(http.Dir("js"))
	r.PathPrefix("/js/").Handler(http.StripPrefix("/js/", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/javascript")
		jsFs.ServeHTTP(w, r)
	})))

	RoutersLoad(r)

	log.Println("Сервер запущен на http://localhost:8081")
	if err := http.ListenAndServe(":8081", r); err != nil {
		log.Fatal(err)
	}
}
