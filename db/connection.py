import pymysql
from pymysql.err import InterfaceError
import logging

logger = logging.getLogger(__name__)

_db_connection = None
_db_config = {}  # Сохраняем конфигурацию для переподключения


def init_db(user, password, host, port, db_name):
    """Инициализирует подключение к базе данных MySQL"""
    global _db_connection, _db_config
    
    # Сохраняем конфигурацию для будущих переподключений
    _db_config = {
        'host': host,
        'port': port,
        'user': user,
        'database': db_name,
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
        'autocommit': True,
        'connect_timeout': 10,  # Таймаут подключения
        'read_timeout': 30,     # Таймаут чтения
        'write_timeout': 30     # Таймаут записи
    }
    
    # Добавляем пароль только если он есть
    if password:
        _db_config['password'] = password
    
    try:
        _db_connection = pymysql.connect(**_db_config)
        logger.info("Successfully connected to MySQL database")
        return _db_connection
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise


def get_db():
    """Возвращает рабочее подключение к базе данных, автоматически переподключаясь при обрыве"""
    global _db_connection
    
    if _db_config is None or not _db_config:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    
    try:
        # Проверяем, существует ли соединение и живо ли оно
        if _db_connection is not None:
            # Пытаемся выполнить ping для проверки соединения
            _db_connection.ping(reconnect=True)
            return _db_connection
    except (AttributeError, InterfaceError, Exception) as e:
        logger.warning(f"Database connection lost, reconnecting: {e}")
        _db_connection = None
    
    # Создаём новое соединение
    try:
        _db_connection = pymysql.connect(**_db_config)
        logger.info("Database reconnection successful")
        return _db_connection
    except Exception as e:
        logger.error(f"Failed to reconnect to database: {e}")
        raise


def is_db_alive() -> bool:
    """Проверяет доступность БД простым ping-запросом."""
    try:
        db = get_db()  # Используем get_db вместо прямого доступа к _db_connection
        with db.cursor() as cursor:
            cursor.execute("SELECT 1 AS ok")
            row = cursor.fetchone()
            return bool(row and row.get("ok") == 1)
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


def get_table_names() -> list[str]:
    """Возвращает список таблиц текущей схемы."""
    db = get_db()  # Используем get_db вместо прямого доступа
    with db.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        rows = cursor.fetchall()
    names = []
    for row in rows:
        if not row:
            continue
        names.append(next(iter(row.values())))
    return sorted(names)


def close_connection():
    """Закрывает соединение с БД (вызывать при завершении приложения)"""
    global _db_connection
    if _db_connection:
        try:
            _db_connection.close()
            logger.info("Database connection closed")
        except Exception as e:
            logger.warning(f"Error closing database connection: {e}")
        finally:
            _db_connection = None