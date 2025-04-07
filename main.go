package main

import (
	"net/http"
	"net/url"
)

func main() {
	request := http.Request{
		Method: "GET",
		URL: &url.URL{
			Scheme: "http",
			Host:   "localhost:8080",
			Path:   "/",
		},
	}
}
