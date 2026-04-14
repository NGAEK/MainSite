import hashlib
from datetime import datetime

from db.connection import get_db


def ensure_site_visits_table() -> None:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS site_visits (
              id BIGINT NOT NULL AUTO_INCREMENT,
              visit_date DATE NOT NULL,
              visitor_key CHAR(64) NOT NULL,
              first_seen DATETIME NOT NULL,
              last_seen DATETIME NOT NULL,
              hits INT NOT NULL DEFAULT 1,
              PRIMARY KEY (id),
              UNIQUE KEY uq_site_visits_date_visitor (visit_date, visitor_key),
              KEY idx_site_visits_visit_date (visit_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
        )


def build_visitor_key(ip: str, user_agent: str) -> str:
    raw = f"{ip or ''}|{user_agent or ''}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def record_visit(visitor_key: str, at: datetime | None = None) -> None:
    now = at or datetime.utcnow()
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            INSERT INTO site_visits (visit_date, visitor_key, first_seen, last_seen, hits)
            VALUES (%s, %s, %s, %s, 1)
            ON DUPLICATE KEY UPDATE
              last_seen = VALUES(last_seen),
              hits = hits + 1
            """,
            (now.date(), visitor_key, now, now),
        )


def get_user_metrics() -> dict:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            SELECT COUNT(DISTINCT visitor_key) AS total
            FROM site_visits
            WHERE visit_date = CURDATE()
            """
        )
        today = int((c.fetchone() or {}).get("total") or 0)

        c.execute(
            """
            SELECT COUNT(DISTINCT visitor_key) AS total
            FROM site_visits
            WHERE YEAR(visit_date) = YEAR(CURDATE())
              AND MONTH(visit_date) = MONTH(CURDATE())
            """
        )
        month = int((c.fetchone() or {}).get("total") or 0)

        c.execute(
            """
            SELECT COUNT(DISTINCT visitor_key) AS total
            FROM site_visits
            WHERE YEAR(visit_date) = YEAR(CURDATE())
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
