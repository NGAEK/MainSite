from db.connection import get_db


def ensure_pages_table() -> None:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS site_pages (
              id INT NOT NULL AUTO_INCREMENT,
              slug VARCHAR(120) NOT NULL,
              title VARCHAR(255) NOT NULL,
              content_html MEDIUMTEXT NULL,
              sort_order INT NOT NULL DEFAULT 100,
              is_active TINYINT(1) NOT NULL DEFAULT 1,
              created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
              updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
              PRIMARY KEY (id),
              UNIQUE KEY uq_site_pages_slug (slug),
              KEY idx_site_pages_active_sort (is_active, sort_order)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
        )


def get_all_pages() -> list[dict]:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            SELECT id, slug, title, content_html, sort_order, is_active
            FROM site_pages
            ORDER BY sort_order ASC, id ASC
            """
        )
        return c.fetchall()


def get_page_by_slug(slug: str) -> dict | None:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            SELECT id, slug, title, content_html, sort_order, is_active
            FROM site_pages
            WHERE slug=%s
            LIMIT 1
            """,
            (slug,),
        )
        return c.fetchone()


def create_page(row: dict) -> int:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            INSERT INTO site_pages (slug, title, content_html, sort_order, is_active)
            VALUES (%s,%s,%s,%s,%s)
            """,
            (
                row["slug"],
                row["title"],
                row.get("content_html") or "",
                row.get("sort_order", 100),
                1 if row.get("is_active", True) else 0,
            ),
        )
        return c.lastrowid


def update_page(page_id: int, row: dict) -> None:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            UPDATE site_pages
            SET slug=%s, title=%s, content_html=%s, sort_order=%s, is_active=%s
            WHERE id=%s
            """,
            (
                row["slug"],
                row["title"],
                row.get("content_html") or "",
                row.get("sort_order", 100),
                1 if row.get("is_active", True) else 0,
                page_id,
            ),
        )


def delete_page(page_id: int) -> bool:
    db = get_db()
    with db.cursor() as c:
        c.execute("DELETE FROM site_pages WHERE id=%s", (page_id,))
        return c.rowcount > 0
