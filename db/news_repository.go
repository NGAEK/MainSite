package db

import (
	"log"
	"src/models"
)

func GetAllNews() ([]models.News, error) {
	rows, err := DB.Query("SELECT id, name, date, description, image_path FROM news ORDER BY date DESC")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var newsList []models.News
	for rows.Next() {
		var n models.News
		err := rows.Scan(&n.ID, &n.Name, &n.Date, &n.Description, &n.ImagePath)
		if err != nil {
			log.Println(err)
			continue
		}
		newsList = append(newsList, n)
	}

	return newsList, nil
}

func GetNewsByID(id int) (models.News, error) {
	var n models.News
	err := DB.QueryRow("SELECT id, name, date, description, image_path FROM news WHERE id = ?", id).
		Scan(&n.ID, &n.Name, &n.Date, &n.Description, &n.ImagePath)

	return n, err
}
