from db.connection import get_db


def ensure_tabs_table() -> None:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS site_tabs (
              id INT NOT NULL AUTO_INCREMENT,
              slug VARCHAR(120) NOT NULL,
              title VARCHAR(255) NOT NULL,
              menu_title VARCHAR(120) NOT NULL,
              content_html MEDIUMTEXT NULL,
              sort_order INT NOT NULL DEFAULT 100,
              is_active TINYINT(1) NOT NULL DEFAULT 1,
              open_in_new_tab TINYINT(1) NOT NULL DEFAULT 0,
              created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
              updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
              PRIMARY KEY (id),
              UNIQUE KEY uq_site_tabs_slug (slug),
              KEY idx_site_tabs_active_sort (is_active, sort_order)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
        )


def get_active_tabs() -> list[dict]:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            SELECT id, slug, title, menu_title, content_html, sort_order, is_active, open_in_new_tab
            FROM site_tabs
            WHERE is_active = 1
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
            WHERE slug=%s
            LIMIT 1
            """,
            (slug,),
        )
        return c.fetchone()


def create_tab(row: dict) -> int:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            INSERT INTO site_tabs (slug, title, menu_title, content_html, sort_order, is_active, open_in_new_tab)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                row["slug"],
                row["title"],
                row["menu_title"],
                row.get("content_html"),
                row.get("sort_order", 100),
                1 if row.get("is_active", True) else 0,
                1 if row.get("open_in_new_tab", False) else 0,
            ),
        )
        return c.lastrowid


def update_tab(tab_id: int, row: dict) -> None:
    db = get_db()
    with db.cursor() as c:
        c.execute(
            """
            UPDATE site_tabs
            SET slug=%s, title=%s, menu_title=%s, content_html=%s, sort_order=%s, is_active=%s, open_in_new_tab=%s
            WHERE id=%s
            """,
            (
                row["slug"],
                row["title"],
                row["menu_title"],
                row.get("content_html"),
                row.get("sort_order", 100),
                1 if row.get("is_active", True) else 0,
                1 if row.get("open_in_new_tab", False) else 0,
                tab_id,
            ),
        )


def delete_tab(tab_id: int) -> bool:
    db = get_db()
    with db.cursor() as c:
        c.execute("DELETE FROM site_tabs WHERE id=%s", (tab_id,))
        return c.rowcount > 0
