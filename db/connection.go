package db

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/go-sql-driver/mysql"
)

var DB *sql.DB

func InitDB(user, password, host string, port int, dbName string) {
	// Формируем строку подключения с учетом пустого пароля
	var connectionString string
	if password == "" {
		connectionString = fmt.Sprintf("%s@tcp(%s:%d)/%s?parseTime=true", user, host, port, dbName)
	} else {
		connectionString = fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?parseTime=true", user, password, host, port, dbName)
	}

	var err error
	DB, err = sql.Open("mysql", connectionString)
	if err != nil {
		log.Fatal(err)
	}

	err = DB.Ping()
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Successfully connected to MySQL database")
}
