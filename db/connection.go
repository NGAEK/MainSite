package db

import (
	"database/sql"
	"fmt"
	"log"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

var DB *sql.DB

func InitDB(user, password, host string, port int, dbName string) {
	var connectionString string
	if password == "" {
		connectionString = fmt.Sprintf("%s@tcp(%s:%d)/%s?parseTime=true&charset=utf8mb4", user, host, port, dbName)
	} else {
		connectionString = fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?parseTime=true&charset=utf8mb4", user, password, host, port, dbName)
	}

	var err error
	DB, err = sql.Open("mysql", connectionString)
	if err != nil {
		log.Fatalf("Error opening database: %v", err)
	}

	// Устанавливаем параметры соединения
	DB.SetMaxOpenConns(25)
	DB.SetMaxIdleConns(25)
	DB.SetConnMaxLifetime(5 * time.Minute)

	err = DB.Ping()
	if err != nil {
		log.Fatalf("Error connecting to database: %v", err)
	}

	log.Println("Successfully connected to MySQL database")
}
