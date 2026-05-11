from db.connection import get_db


def ensure_pages_table() -> None:
    """Создаёт таблицу site_pages если она ещё не существует (идемпотентно)."""
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS site_pages (
              id           SERIAL PRIMARY KEY,
              slug         VARCHAR(120)  NOT NULL,
              title        VARCHAR(255)  NOT NULL,
              content_html TEXT,
              sort_order   INT           NOT NULL DEFAULT 100,
              is_active    BOOLEAN       NOT NULL DEFAULT TRUE,
              created_at   TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
              updated_at   TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
              CONSTRAINT uq_site_pages_slug UNIQUE (slug)
            )
            """
        )
        c.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_site_pages_active_sort
              ON site_pages (is_active, sort_order)
            """
        )


def search_pages(query: str) -> list[dict]:
    """Поиск по заголовку и содержимому активных страниц (ILIKE — без учёта регистра)."""
    db = get_db()
    with db.cursor() as c:
        like = f"%{query}%"
        c.execute(
            """
            SELECT id, slug, title, content_html
            FROM site_pages
            WHERE is_active = TRUE
              AND (title ILIKE %s OR content_html ILIKE %s)
            ORDER BY sort_order ASC, id ASC
            """,
            (like, like),
        )
        return c.fetchall()


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
            WHERE slug = %s
            LIMIT 1
            """,
            (slug,),
        )
        return c.fetchone()


def create_page(row: dict) -> int:
    """Создаёт страницу; возвращает id новой записи."""
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            INSERT INTO site_pages (slug, title, content_html, sort_order, is_active)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                row["slug"],
                row["title"],
                row.get("content_html") or "",
                row.get("sort_order", 100),
                bool(row.get("is_active", True)),
            ),
        )
        return c.fetchone()["id"]


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
                bool(row.get("is_active", True)),
                page_id,
            ),
        )


def delete_page(page_id: int) -> bool:
    db = get_db()
    with db.cursor() as c:
        c.execute("DELETE FROM site_pages WHERE id=%s", (page_id,))
        return c.rowcount > 0
