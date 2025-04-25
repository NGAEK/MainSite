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

func SearchNews(query string) ([]models.News, error) {
	query = "%" + query + "%"

	rows, err := DB.Query(`
        SELECT id, name, date, description, image_path 
        FROM news 
        WHERE name LIKE ? OR description LIKE ?
        ORDER BY date DESC`,
		query, query)

	defer rows.Close()

	var results []models.News
	for rows.Next() {
		var n models.News
		err := rows.Scan(&n.ID, &n.Name, &n.Date, &n.Description, &n.ImagePath)
		if err != nil {
			log.Printf("Error scanning news row: %v", err)
			continue
		}
		results = append(results, n)
	}

	if err = rows.Err(); err != nil {
		log.Printf("Rows error: %v", err)
		return nil, err
	}

	return results, nil
}

func GetNewsByID(id int) (models.News, error) {
	var n models.News
	err := DB.QueryRow("SELECT id, name, date, description, image_path FROM news WHERE id = ?", id).
		Scan(&n.ID, &n.Name, &n.Date, &n.Description, &n.ImagePath)

	return n, err
}

func NewsExists(id string) (bool, error) {
	var exists bool
	query := "SELECT EXISTS(SELECT 1 FROM news WHERE id = ?)"

	err := DB.QueryRow(query, id).Scan(&exists)
	if err != nil {
		log.Printf("Ошибка при проверке существования новости: %v", err)
		return false, err
	}

	return exists, nil
}
