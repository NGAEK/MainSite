import psycopg2
import psycopg2.extras
import logging

logger = logging.getLogger(__name__)

_db_connection = None
_db_config: dict = {}  # Сохраняем конфигурацию для переподключения


def init_db(user, password, host, port, db_name):
    """Инициализирует подключение к базе данных PostgreSQL."""
    global _db_connection, _db_config

    _db_config = {
        'host': host,
        'port': int(port),
        'user': user,
        'dbname': db_name,
        'connect_timeout': 10,
        # cursor_factory на уровне соединения — все cursor() вернут RealDictRow (dict-подобные объекты)
        'cursor_factory': psycopg2.extras.RealDictCursor,
    }
    if password:
        _db_config['password'] = password

    try:
        _db_connection = _new_connection()
        logger.info("Successfully connected to PostgreSQL database")
        return _db_connection
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise


def _new_connection():
    """Создаёт новое соединение и включает autocommit."""
    conn = psycopg2.connect(**_db_config)
    conn.autocommit = True
    return conn


def get_db():
    """Возвращает рабочее подключение к БД, автоматически переподключаясь при обрыве."""
    global _db_connection

    if not _db_config:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    # Проверяем живость соединения
    if _db_connection is not None and not _db_connection.closed:
        try:
            with _db_connection.cursor() as cur:
                cur.execute("SELECT 1")
            return _db_connection
        except Exception as e:
            logger.warning(f"Database connection lost: {e}")
            _db_connection = None

    # Переподключение
    try:
        _db_connection = _new_connection()
        logger.info("Database reconnection successful")
        return _db_connection
    except Exception as e:
        logger.error(f"Failed to reconnect to database: {e}")
        raise


def is_db_alive() -> bool:
    """Проверяет доступность БД простым SELECT 1."""
    try:
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT 1 AS ok")
            row = cursor.fetchone()
            return bool(row and row.get("ok") == 1)
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


def get_table_names() -> list[str]:
    """Возвращает список таблиц текущей схемы (public)."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_type = 'BASE TABLE'
            ORDER BY table_name
            """
        )
        rows = cursor.fetchall()
    return [row["table_name"] for row in rows]


def close_connection():
    """Закрывает соединение с БД (вызывать при завершении приложения)."""
    global _db_connection
    if _db_connection and not _db_connection.closed:
        try:
            _db_connection.close()
            logger.info("Database connection closed")
        except Exception as e:
            logger.warning(f"Error closing database connection: {e}")
        finally:
            _db_connection = None
