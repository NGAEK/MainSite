import logging

from db.connection import get_db

logger = logging.getLogger(__name__)


def ensure_admin_users_table() -> None:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS admin_users (
              id            SERIAL PRIMARY KEY,
              username      VARCHAR(64)   NOT NULL,
              password_hash VARCHAR(255)  NOT NULL,
              is_active     BOOLEAN       NOT NULL DEFAULT TRUE,
              created_at    TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
              updated_at    TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
              CONSTRAINT uq_admin_users_username UNIQUE (username)
            )
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
        return c.fetchone()


def create_admin_user(username: str, password_hash: str) -> int:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            INSERT INTO admin_users (username, password_hash, is_active)
            VALUES (%s, %s, TRUE)
            RETURNING id
            """,
            (username, password_hash),
        )
        return c.fetchone()["id"]


def count_admin_users(active_only: bool = False) -> int:
    db = get_db()
    with db.cursor() as c:
        if active_only:
            c.execute("SELECT COUNT(*) AS total FROM admin_users WHERE is_active = TRUE")
        else:
            c.execute("SELECT COUNT(*) AS total FROM admin_users")
        row = c.fetchone()
    return int((row or {}).get("total") or 0)
