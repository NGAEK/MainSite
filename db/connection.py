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


def is_db_alive() -> bool:
    """Проверяет доступность БД простым ping-запросом."""
    try:
        db = get_db()
        db.ping(reconnect=True)
        with db.cursor() as cursor:
            cursor.execute("SELECT 1 AS ok")
            row = cursor.fetchone()
            return bool(row and row.get("ok") == 1)
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


def get_table_names() -> list[str]:
    """Возвращает список таблиц текущей схемы."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        rows = cursor.fetchall()
    names = []
    for row in rows:
        if not row:
            continue
        names.append(next(iter(row.values())))
    return sorted(names)

