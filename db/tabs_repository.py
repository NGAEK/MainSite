from db.connection import get_db


def ensure_tabs_table() -> None:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS site_tabs (
              id              SERIAL PRIMARY KEY,
              slug            VARCHAR(120)  NOT NULL,
              title           VARCHAR(255)  NOT NULL,
              menu_title      VARCHAR(120)  NOT NULL,
              content_html    TEXT,
              sort_order      INT           NOT NULL DEFAULT 100,
              is_active       BOOLEAN       NOT NULL DEFAULT TRUE,
              open_in_new_tab BOOLEAN       NOT NULL DEFAULT FALSE,
              created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
              updated_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
              CONSTRAINT uq_site_tabs_slug UNIQUE (slug)
            )
            """
        )
        c.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_site_tabs_active_sort
              ON site_tabs (is_active, sort_order)
            """
        )


def search_tabs(query: str) -> list[dict]:
    db = get_db()
    with db.cursor() as c:
        like = f"%{query}%"
        c.execute(
            """
            SELECT id, slug, title, menu_title, content_html
            FROM site_tabs
            WHERE is_active = TRUE
              AND (
                title ILIKE %s
                OR menu_title ILIKE %s
                OR COALESCE(content_html, '') ILIKE %s
              )
            ORDER BY sort_order ASC, id ASC
            """,
            (like, like, like),
        )
        return c.fetchall()


def get_active_tabs() -> list[dict]:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            SELECT id, slug, title, menu_title, content_html, sort_order, is_active, open_in_new_tab
            FROM site_tabs
            WHERE is_active = TRUE
            ORDER BY sort_order ASC, id ASC
            """
        )
        return c.fetchall()


def get_all_tabs() -> list[dict]:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            SELECT id, slug, title, menu_title, content_html, sort_order, is_active, open_in_new_tab
            FROM site_tabs
            ORDER BY sort_order ASC, id ASC
            """
        )
        return c.fetchall()


def get_tab_by_slug(slug: str) -> dict | None:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            SELECT id, slug, title, menu_title, content_html, sort_order, is_active, open_in_new_tab
            FROM site_tabs
            WHERE slug = %s
            LIMIT 1
            """,
            (slug,),
        )
        return c.fetchone()


def create_tab(row: dict) -> int:
    """Создаёт вкладку; возвращает id новой записи."""
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            INSERT INTO site_tabs (slug, title, menu_title, content_html, sort_order, is_active, open_in_new_tab)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                row["slug"],
                row["title"],
                row["menu_title"],
                row.get("content_html"),
                row.get("sort_order", 100),
                bool(row.get("is_active", True)),
                bool(row.get("open_in_new_tab", False)),
            ),
        )
        return c.fetchone()["id"]


def update_tab(tab_id: int, row: dict) -> None:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            UPDATE site_tabs
            SET slug=%s, title=%s, menu_title=%s, content_html=%s,
                sort_order=%s, is_active=%s, open_in_new_tab=%s
            WHERE id=%s
            """,
            (
                row["slug"],
                row["title"],
                row["menu_title"],
                row.get("content_html"),
                row.get("sort_order", 100),
                bool(row.get("is_active", True)),
                bool(row.get("open_in_new_tab", False)),
                tab_id,
            ),
        )


def delete_tab(tab_id: int) -> bool:
    db = get_db()
    with db.cursor() as c:
        c.execute("DELETE FROM site_tabs WHERE id=%s", (tab_id,))
        return c.rowcount > 0
