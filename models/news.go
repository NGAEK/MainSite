package models

import "time"

type News struct {
	ID          int
	Name        string
	Date        time.Time
	Description string
	ImagePath   string
}

func (n News) FormattedDate() string {
	return n.Date.Format("02 January 2006")
}
