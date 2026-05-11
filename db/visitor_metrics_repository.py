import hashlib
from datetime import datetime

from db.connection import get_db


def ensure_site_visits_table() -> None:
    """Создаёт таблицу site_visits если она ещё не существует (идемпотентно)."""
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS site_visits (
              id           BIGSERIAL PRIMARY KEY,
              visit_date   DATE         NOT NULL,
              visitor_key  CHAR(64)     NOT NULL,
              first_seen   TIMESTAMP    NOT NULL,
              last_seen    TIMESTAMP    NOT NULL,
              hits         INT          NOT NULL DEFAULT 1,
              CONSTRAINT uq_site_visits_date_visitor UNIQUE (visit_date, visitor_key)
            )
            """
        )
        c.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_site_visits_visit_date
              ON site_visits (visit_date)
            """
        )


def build_visitor_key(ip: str, user_agent: str) -> str:
    raw = f"{ip or ''}|{user_agent or ''}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def record_visit(visitor_key: str, at: datetime | None = None) -> None:
    """Записывает посещение: создаёт новую запись или обновляет счётчик хитов."""
    now = at or datetime.utcnow()
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            INSERT INTO site_visits (visit_date, visitor_key, first_seen, last_seen, hits)
            VALUES (%s, %s, %s, %s, 1)
            ON CONFLICT (visit_date, visitor_key) DO UPDATE
              SET last_seen = EXCLUDED.last_seen,
                  hits      = site_visits.hits + 1
            """,
            (now.date(), visitor_key, now, now),
        )


def get_user_metrics() -> dict:
    """Возвращает метрики уникальных посетителей за сегодня, месяц, год и всего."""
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            SELECT COUNT(DISTINCT visitor_key) AS total
            FROM site_visits
            WHERE visit_date = CURRENT_DATE
            """
        )
        today = int((c.fetchone() or {}).get("total") or 0)

        c.execute(
            """
            SELECT COUNT(DISTINCT visitor_key) AS total
            FROM site_visits
            WHERE EXTRACT(YEAR  FROM visit_date) = EXTRACT(YEAR  FROM CURRENT_DATE)
              AND EXTRACT(MONTH FROM visit_date) = EXTRACT(MONTH FROM CURRENT_DATE)
            """
        )
        month = int((c.fetchone() or {}).get("total") or 0)

        c.execute(
            """
            SELECT COUNT(DISTINCT visitor_key) AS total
            FROM site_visits
            WHERE EXTRACT(YEAR FROM visit_date) = EXTRACT(YEAR FROM CURRENT_DATE)
            """
        )
        year = int((c.fetchone() or {}).get("total") or 0)

        c.execute(
            """
            SELECT COUNT(DISTINCT visitor_key) AS total
            FROM site_visits
            """
        )
        total = int((c.fetchone() or {}).get("total") or 0)

    return {
        "users_today": today,
        "users_month": month,
        "users_year": year,
        "users_total": total,
    }
