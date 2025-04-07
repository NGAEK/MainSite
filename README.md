🎓 Сайт колледжа - Дипломный проект

![GitHub go.mod Go version](https://img.shields.io/github/go-mod/go-version/NGAEK/MainSite)

![GitHub last commit](https://img.shields.io/github/last-commit/NGAEK/MainSite)


Профессиональный веб-сайт для образовательного учреждения, разработанный как дипломный проект. Сайт предоставляет полный спектр функционала для студентов, абитуриентов и администрации колледжа.
✨ Особенности

    Современный интерфейс с адаптивным дизайном

    Расписание занятий с возможностью редактирования

    Новостная система колледжа

    Административная панель для управления контентом

🛠 Технологии

![Go](https://img.shields.io/badge/-Go-00ADD8?logo=go&logoColor=white)
![MySQL](https://img.shields.io/badge/-MySQL-4479A1?logo=mysql&logoColor=white)
![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/-HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/-CSS3-1572B6?logo=css3&logoColor=white)

🚀 Установка и запуск

    Клонируйте репозиторий:
    git clone https://github.com/yourusername/college-website.git
    cd college-website

Настройте базу данных MySQL:

    mysql -u root -p < database/schema.sql

Настройте конфигурацию в файле config.yaml:

    database:
    host: "localhost"
    port: 3306
    user: "youruser"
    password: "yourpassword"
    name: "college_db"
    server:
    port: ":8080"

Запустите сервер:
    
    go run main.go

Откройте в браузере:

    http://localhost:8081

📝 Лицензия

Этот проект распространяется под лицензией MIT.

    Автор: Дятлик А.Ю.
    Год: 2025-2026
    Колледж: НГАЭК

💻 Разработано с passion для образования!