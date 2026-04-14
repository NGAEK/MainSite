import logging

from db.connection import get_db

logger = logging.getLogger(__name__)


def ensure_admin_users_table() -> None:
    """Создает таблицу админ-пользователей, если она отсутствует."""
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS admin_users (
              id INT NOT NULL AUTO_INCREMENT,
              username VARCHAR(64) NOT NULL,
              password_hash VARCHAR(255) NOT NULL,
              is_active TINYINT(1) NOT NULL DEFAULT 1,
              created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
              updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
              PRIMARY KEY (id),
              UNIQUE KEY uq_admin_users_username (username)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
        )


def get_admin_user_by_username(username: str) -> dict | None:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            SELECT id, username, password_hash, is_active
            FROM admin_users
            WHERE username = %s
            LIMIT 1
            """,
            (username,),
        )
        row = c.fetchone()
    return row


def create_admin_user(username: str, password_hash: str) -> int:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            INSERT INTO admin_users (username, password_hash, is_active)
            VALUES (%s, %s, 1)
            """,
            (username, password_hash),
        )
        return c.lastrowid


def count_admin_users(active_only: bool = False) -> int:
    db = get_db()
    with db.cursor() as c:
        if active_only:
            c.execute("SELECT COUNT(*) AS total FROM admin_users WHERE is_active = 1")
        else:
            c.execute("SELECT COUNT(*) AS total FROM admin_users")
        row = c.fetchone()
    return int((row or {}).get("total") or 0)
