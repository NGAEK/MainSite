package main

import (
	"github.com/gorilla/mux"
	"net/http"
	"src/db"
	"src/page"
	"strconv"
)

func RoutersLoad(r *mux.Router) {
	r.HandleFunc("/", page.HomeHandler)
	r.HandleFunc("/search", page.SearchHandler)
	r.HandleFunc("/news/{id:[0-9]+}", func(w http.ResponseWriter, r *http.Request) {
		vars := mux.Vars(r)
		id := vars["id"]

		exists, err := db.NewsExists(id)
		if err != nil {
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		}

		if !exists {
			page.NotFoundHandler(w, r)
			return
		}

		newsID, _ := strconv.Atoi(id)
		page.NewsDetailHandler(w, r, newsID)
	})
	r.HandleFunc("/spec/byx", page.SpecByx)
	r.HandleFunc("/spec/do", page.SpecDo)
	r.HandleFunc("/spec/ogu", page.SpecOgu)
	r.HandleFunc("/spec/po", page.SpecPo)
	r.HandleFunc("/spec/soc_rab", page.SpecSocRab)
}
