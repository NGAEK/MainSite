package page

import (
	"html/template"
	"log"
	"net/http"
	"path/filepath"
)

func SpecByx(w http.ResponseWriter, r *http.Request) {
	templates := []string{
		filepath.Join("templates", "header.html"),
		filepath.Join("templates", "specialization", "byx.html"),
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

func SpecPo(w http.ResponseWriter, r *http.Request) {
	templates := []string{
		filepath.Join("templates", "header.html"),
		filepath.Join("templates", "specialization", "po.html"),
		filepath.Join("templates", "footer.html"),
	}

	tmpl, err := template.ParseFiles(templates...)
	if err != nil {
		log.Printf("Ошибка загрузки шаблонов: %v (пути: %v)", err, templates)
		http.Error(w, "500 Internal Server Error", http.StatusInternalServerError)
		return
	}

	err = tmpl.ExecuteTemplate(w, "po.html", nil)
	if err != nil {
		log.Printf("Ошибка рендеринга шаблона: %v", err)
		http.Error(w, "500 Internal Server Error", http.StatusInternalServerError)
	}
}

func SpecOgu(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, "templates/specialization/ogu.html")
}

func SpecDo(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, "templates/specialization/do.html")
}

func SpecSocRab(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, "templates/specialization/soc_rab.html")
}
