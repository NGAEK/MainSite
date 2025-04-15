package main

import (
	"github.com/gorilla/mux"
	"src/page"
)

func RoutersLoad(r *mux.Router) {
	r.HandleFunc("/", page.HomeHandler)
	r.HandleFunc("/spec/byx", page.SpecByx)
	r.HandleFunc("/spec/do", page.SpecDo)
	r.HandleFunc("/spec/ogu", page.SpecOgu)
	r.HandleFunc("/spec/po", page.SpecPo)
	r.HandleFunc("/spec/soc_rab", page.SpecSocRab)
}
