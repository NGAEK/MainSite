import logging
from db.connection import get_db
from models.news import News

logger = logging.getLogger(__name__)

_NEWS_COLUMNS = (
    "id, name, date, description, name_be, name_en, "
    "description_be, description_en, image_path"
)


def get_all_news():
    """Возвращает все новости из базы данных."""
    try:
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT {_NEWS_COLUMNS}
                FROM news
                ORDER BY date DESC
                """
            )
            return [News.from_dict(row) for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Error getting all news: {e}")
        raise


def search_news(query):
    """Поиск новостей по всем языковым полям."""
    try:
        db = get_db()
        with db.cursor() as cursor:
            search_query = f"%{query}%"
            cursor.execute(
                f"""
                SELECT {_NEWS_COLUMNS}
                FROM news
                WHERE name LIKE %s OR description LIKE %s
                   OR name_be LIKE %s OR name_en LIKE %s
                   OR description_be LIKE %s OR description_en LIKE %s
                ORDER BY date DESC
                """,
                (search_query,) * 6,
            )
            return [News.from_dict(row) for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Error searching news: {e}")
        raise


def get_news_by_id(news_id):
    """Возвращает новость по ID."""
    try:
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT {_NEWS_COLUMNS}
                FROM news
                WHERE id = %s
                """,
                (news_id,),
            )
            row = cursor.fetchone()
            if row:
                return News.from_dict(row)
            return None
    except Exception as e:
        logger.error(f"Error getting news by ID: {e}")
        raise


def news_exists(news_id):
    """Проверяет существование новости по ID."""
    try:
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM news WHERE id = %s) as exists_flag",
                (news_id,),
            )
            result = cursor.fetchone()
            return bool(result["exists_flag"]) if result else False
    except Exception as e:
        logger.error(f"Error checking news existence: {e}")
        raise


def _date_iso(val):
    if val is None:
        return None
    if hasattr(val, "strftime"):
        return val.strftime("%Y-%m-%d")
    return str(val)


def news_to_dict(news: News) -> dict:
    """Сериализация новости для JSON API."""
    return {
        "id": news.id,
        "name": news.name,
        "date": _date_iso(news.date),
        "description": news.description,
        "name_be": news.name_be,
        "name_en": news.name_en,
        "description_be": news.description_be,
        "description_en": news.description_en,
        "image_path": news.image_path,
    }


_PATCH_KEYS = frozenset(
    {
        "name",
        "description",
        "name_be",
        "name_en",
        "description_be",
        "description_en",
        "image_path",
        "date",
    }
)


def insert_news(row: dict) -> int:
    """Создаёт новость; возвращает id."""
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            INSERT INTO news (
              `name`, `date`, `description`, `name_be`, `name_en`,
              `description_be`, `description_en`, `image_path`
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                row["name"],
                row["date"],
                row["description"],
                row.get("name_be"),
                row.get("name_en"),
                row.get("description_be"),
                row.get("description_en"),
                row.get("image_path"),
            ),
        )
        return c.lastrowid


def update_news_full(news_id: int, row: dict) -> None:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            UPDATE news SET
              `name`=%s, `date`=%s, `description`=%s,
              `name_be`=%s, `name_en`=%s, `description_be`=%s, `description_en`=%s, `image_path`=%s
            WHERE id=%s
            """,
            (
                row["name"],
                row["date"],
                row["description"],
                row.get("name_be"),
                row.get("name_en"),
                row.get("description_be"),
                row.get("description_en"),
                row.get("image_path"),
                news_id,
            ),
        )


def update_news_partial(news_id: int, patch: dict) -> None:
    keys = [k for k in patch if k in _PATCH_KEYS]
    if not keys:
        return
    assignments = ", ".join(f"`{k}`=%s" for k in keys)
    values = [patch[k] for k in keys]
    values.append(news_id)
    sql = f"UPDATE news SET {assignments} WHERE id=%s"
    db = get_db()
    with db.cursor() as c:
        c.execute(sql, values)


def delete_news(news_id: int) -> bool:
    db = get_db()
    with db.cursor() as c:
        c.execute("DELETE FROM news WHERE id=%s", (news_id,))
        return c.rowcount > 0
