import logging
from db.connection import get_db
from models.news import News
from datetime import datetime

logger = logging.getLogger(__name__)


def get_all_news():
    """Возвращает все новости из базы данных"""
    try:
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, date, description, image_path 
                FROM news 
                ORDER BY date DESC
            """)
            results = cursor.fetchall()
            
            news_list = []
            for row in results:
                news = News.from_dict(row)
                news_list.append(news)
            
            return news_list
    except Exception as e:
        logger.error(f"Error getting all news: {e}")
        raise


def search_news(query):
    """Выполняет поиск новостей по запросу"""
    try:
        db = get_db()
        with db.cursor() as cursor:
            search_query = f"%{query}%"
            cursor.execute("""
                SELECT id, name, date, description, image_path 
                FROM news 
                WHERE name LIKE %s OR description LIKE %s
                ORDER BY date DESC
            """, (search_query, search_query))
            
            results = cursor.fetchall()
            
            news_list = []
            for row in results:
                news = News.from_dict(row)
                news_list.append(news)
            
            return news_list
    except Exception as e:
        logger.error(f"Error searching news: {e}")
        raise


def get_news_by_id(news_id):
    """Возвращает новость по ID"""
    try:
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, date, description, image_path 
                FROM news 
                WHERE id = %s
            """, (news_id,))
            
            row = cursor.fetchone()
            if row:
                return News.from_dict(row)
            return None
    except Exception as e:
        logger.error(f"Error getting news by ID: {e}")
        raise


def news_exists(news_id):
    """Проверяет существование новости по ID"""
    try:
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT EXISTS(SELECT 1 FROM news WHERE id = %s) as exists_flag", (news_id,))
            result = cursor.fetchone()
            return bool(result['exists_flag']) if result else False
    except Exception as e:
        logger.error(f"Error checking news existence: {e}")
        raise

