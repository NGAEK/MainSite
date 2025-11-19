import pymysql
import logging

logger = logging.getLogger(__name__)

_db_connection = None


def init_db(user, password, host, port, db_name):
    """Инициализирует подключение к базе данных MySQL"""
    global _db_connection
    
    try:
        if password:
            _db_connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=db_name,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
        else:
            _db_connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                database=db_name,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
        
        logger.info("Successfully connected to MySQL database")
        return _db_connection
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise


def get_db():
    """Возвращает текущее подключение к базе данных"""
    if _db_connection is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _db_connection

