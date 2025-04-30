package db

import (
	"database/sql"
	"log"
	"src/models"
)

// GetAllNews возвращает все новости из базы данных
func GetAllNews() ([]models.News, error) {
	rows, err := DB.Query(`
        SELECT id, name, date, description, image_path 
        FROM news 
        ORDER BY date DESC`)
	if err != nil {
		log.Printf("Error getting all news: %v", err)
		return nil, err
	}
	defer rows.Close()

	var newsList []models.News
	for rows.Next() {
		var n models.News
		err := rows.Scan(&n.ID, &n.Name, &n.Date, &n.Description, &n.ImagePath)
		if err != nil {
			log.Printf("Error scanning news row: %v", err)
			continue
		}
		newsList = append(newsList, n)
	}

	if err = rows.Err(); err != nil {
		log.Printf("Rows error: %v", err)
		return nil, err
	}

	return newsList, nil
}

// SearchNews выполняет поиск новостей по запросу
func SearchNews(query string) ([]models.News, error) {
	searchQuery := "%" + query + "%"

	rows, err := DB.Query(`
        SELECT id, name, date, description, image_path 
        FROM news 
        WHERE name LIKE ? OR description LIKE ?
        ORDER BY date DESC`,
		searchQuery, searchQuery)
	if err != nil {
		log.Printf("Error searching news: %v", err)
		return nil, err
	}
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

// GetNewsByID возвращает новость по ID
func GetNewsByID(id int) (models.News, error) {
	var n models.News
	err := DB.QueryRow(`
        SELECT id, name, date, description, image_path 
        FROM news 
        WHERE id = ?`, id).
		Scan(&n.ID, &n.Name, &n.Date, &n.Description, &n.ImagePath)

	if err != nil {
		if err == sql.ErrNoRows {
			return models.News{}, nil
		}
		log.Printf("Error getting news by ID: %v", err)
		return models.News{}, err
	}
	return n, nil
}

// NewsExists проверяет существование новости по ID
func NewsExists(id string) (bool, error) {
	var exists bool
	err := DB.QueryRow("SELECT EXISTS(SELECT 1 FROM news WHERE id = ?)", id).Scan(&exists)
	if err != nil {
		log.Printf("Error checking news existence: %v", err)
		return false, err
	}
	return exists, nil
}
