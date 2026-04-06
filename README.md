# 🎓 Сайт колледжа — дипломный проект

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)
![GitHub last commit](https://img.shields.io/github/last-commit/NGAEK/MainSite)

Профессиональный веб-сайт для образовательного учреждения, разработанный как дипломный проект на **Python** и **Flask**. Сайт предоставляет полный спектр функционала для студентов, абитуриентов и администрации колледжа.

## ✨ Особенности

- Современный интерфейс с адаптивным дизайном
- Новостная система колледжа
- **Локализация RU/BY/EN** — файл `static/locales/messages.json` (ключи `RU`, `BY`, `EN`; русский по умолчанию). Скрипт дополнения EN: `python tools/fill_messages_en.py`
- Переключение языка через cookie и параметр `?lang=ru` / `?lang=be` / `?lang=en`
- **Новости** хранят тексты на трёх языках: поля `name`/`description` (RU), `name_be`/`description_be`, `name_en`/`description_en` в таблице `news`. Для существующей БД выполните `migrations/001_news_i18n.sql`
- Страницы специальностей (ПО, бухучёт, гостиничный сервис, документоведение, социальная работа)
- Поиск по новостям
- Настройки доступности (контраст, шрифт, тёмная тема)

## 🛠 Технологии

- **Backend:** Python 3, Flask
- **База данных:** MySQL
- **Frontend:** HTML5, CSS3, JavaScript
- **Шаблоны:** Jinja2
- **Локализация:** JSON (RU/BY) в одном файле

## 🚀 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/NGAEK/MainSite.git
cd MainSite
```

### 2. Виртуальное окружение и зависимости (Python)

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt
```

### 3. Настройка базы данных MySQL

Для подключения к MySQL 8 с `caching_sha2_password` нужен пакет **cryptography** — он уже в `requirements.txt`. Если ошибка остаётся:

```bash
pip install cryptography
```

**Создание пользователя MySQL** (локально или по SSH на сервер):

```bash
# Подключиться к MySQL (локально или после ssh user@server):
mysql -u root -p
```

В консоли MySQL выполните:

```sql
-- Создать базу (если ещё нет)
CREATE DATABASE IF NOT EXISTS ngaek CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Вариант 1: пользователь с caching_sha2_password (нужен pip install cryptography)
CREATE USER 'ngaek_user'@'localhost' IDENTIFIED BY 'ваш_пароль';
GRANT ALL PRIVILEGES ON ngaek.* TO 'ngaek_user'@'localhost';
FLUSH PRIVILEGES;

-- Вариант 2: пользователь с mysql_native_password (без cryptography)
CREATE USER 'ngaek_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'ваш_пароль';
GRANT ALL PRIVILEGES ON ngaek.* TO 'ngaek_user'@'localhost';
FLUSH PRIVILEGES;
```

Если подключаетесь к MySQL **по SSH** (MySQL на другом хосте):

1. Подключитесь по SSH: `ssh user@хост_сервера`
2. На сервере выполните: `mysql -u root -p` и команды выше.
3. Для доступа с вашей машины создайте пользователя с доступом с любого хоста (или с IP приложения):

```sql
CREATE USER 'ngaek_user'@'%' IDENTIFIED WITH mysql_native_password BY 'ваш_пароль';
GRANT ALL PRIVILEGES ON ngaek.* TO 'ngaek_user'@'%';
FLUSH PRIVILEGES;
```

Импорт дампа:

```bash
mysql -u root -p < ngaek.sql
# или с указанием базы:
mysql -u root -p ngaek < ngaek.sql
```

### 4. Конфигурация

Создайте или отредактируйте `config.yml`:

```yaml
database:
  host: "127.0.0.1"
  port: 3306
  user: "test"
  password: "test"
  name: "ngaek"
server:
  port: "8080"
```

### 5. Запуск сервера

```bash
python app.py
```

Откройте в браузере: **http://localhost:8080**

### API для внешней админки

Префикс **`/api/v1`**. Проверка без БД: **`GET /api/v1/health`**.

Остальные методы новостей требуют заголовок **`X-API-Key`** с секретом из `config.yml` → `admin_api.key` или переменной окружения **`NGAEK_ADMIN_API_KEY`** (имеет приоритет). Если ключ не задан, ответ **503** с текстом `api_not_configured`.

| Метод | Путь | Назначение |
|--------|------|------------|
| `GET` | `/api/v1/news` | Список новостей (все поля, включая переводы) |
| `GET` | `/api/v1/news/<id>` | Одна новость |
| `POST` | `/api/v1/news` | Создание: JSON с обязательными `name`, `description`, `date` (YYYY-MM-DD); опционально `name_be`, `name_en`, `description_be`, `description_en`, `image_path` |
| `PUT` | `/api/v1/news/<id>` | Полная замена (те же поля, что POST) |
| `PATCH` | `/api/v1/news/<id>` | Частичное обновление допустимых полей |
| `DELETE` | `/api/v1/news/<id>` | Удаление (**204** при успехе) |

Пример создания:

```bash
curl -s -X POST "http://localhost:8080/api/v1/news" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ВАШ_КЛЮЧ" \
  -d "{\"name\":\"Заголовок\",\"description\":\"Текст\",\"date\":\"2025-06-01\",\"name_en\":\"Title\",\"description_en\":\"Text\"}"
```

Ответы об ошибках в JSON: `{"error": {"code": "...", "message": "..."}}`.

Тесты без поднятого MySQL: `python -m pytest tests/ -q`

## 📁 Структура проекта

- `app.py` — точка входа, маршруты, локализация (`messages.json`), `hreflang`, регистрация API
- `api/` — JSON API для админ-сервиса (`X-API-Key`)
- `page/` — обработчики страниц (главная, новости, поиск, специальности, 404)
- `templates/` — Jinja2-шаблоны с переменной `t` (переводы)
- `static/` — CSS, изображения, **`static/js/`** (`script.js`, `search.js`; URL `/static/js/...`)
- `static/locales/messages.json` — тексты `RU` / `BY` / `EN`
- `config.yml` — БД, порт, `admin_api.key`, блок **`site`** (ГРИС, `admin_email`, ссылка «Одно окно»). Публичные страницы: **`/privacy`**, **`/one-window`**, **`/sitemap`**
- `tests/` — pytest (локализация новостей, hreflang URL, API-ключ)

## 📝 Лицензия

Проект распространяется под лицензией MIT.

- **Автор:** Дятлик А.Ю., Журавлёв А.Ю., Бокарев Р.
- **Год:** 2025–2026
- **Колледж:** НГАЭК

💻 Разработано с увлечением к образованию!
