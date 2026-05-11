import os
from dataclasses import dataclass
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def _find_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    # Windows fonts typically available on the user's machine.
    candidates = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\ARIAL.TTF",
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size=size)
            except Exception:
                pass
    # Fallback (may not support Cyrillic perfectly, but will keep script functional).
    return ImageFont.load_default()


def _wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
    words = (text or "").split()
    if not words:
        return [""]

    lines: List[str] = []
    cur = words[0]
    for w in words[1:]:
        candidate = f"{cur} {w}"
        if draw.textlength(candidate, font=font) <= max_width:
            cur = candidate
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def _rounded_rect(draw: ImageDraw.ImageDraw, xy: Tuple[int, int, int, int], radius: int, width: int = 2) -> None:
    draw.rounded_rectangle(xy, radius=radius, outline=BLACK, width=width)


def _draw_box(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    w: int,
    h: int,
    title: str,
    lines: List[str],
    *,
    title_font: ImageFont.ImageFont,
    body_font: ImageFont.ImageFont,
    pad: int = 16,
) -> Tuple[int, int, int, int]:
    _rounded_rect(draw, (x, y, x + w, y + h), radius=16, width=2)

    # Title
    title_lines = [title] if len(title) < 60 else title[:57] + "…"
    cur_y = y + pad
    for tl in title_lines:
        tw = draw.textlength(tl, font=title_font)
        draw.text((x + w / 2 - tw / 2, cur_y), tl, fill=BLACK, font=title_font)
        cur_y += title_font.size + 6

    # Body
    body_max_width = w - pad * 2
    line_y = cur_y
    line_h = body_font.size + 4
    for ln in lines:
        wrapped = _wrap_text(draw, ln, body_font, max_width=body_max_width)
        for wl in wrapped:
            draw.text((x + pad, line_y), wl, fill=BLACK, font=body_font)
            line_y += line_h
        # Small gap between logical lines.
        line_y += 2

    return (x, y, x + w, y + h)


def _draw_center_line(
    draw: ImageDraw.ImageDraw,
    a: Tuple[int, int],
    b: Tuple[int, int],
    *,
    width: int = 2,
) -> None:
    draw.line((a[0], a[1], b[0], b[1]), fill=BLACK, width=width)


@dataclass(frozen=True)
class Node:
    name: str
    x: int
    y: int
    w: int
    h: int

    @property
    def center(self) -> Tuple[int, int]:
        return (self.x + self.w // 2, self.y + self.h // 2)

    @property
    def top_center(self) -> Tuple[int, int]:
        return (self.x + self.w // 2, self.y)


def render_class_diagram(out_path: str) -> None:
    img = Image.new("RGB", (2000, 1400), WHITE)
    draw = ImageDraw.Draw(img)

    title_font = _find_font(26)
    body_font = _find_font(18)

    draw.text((100, 20), "Диаграмма классов (упрощённо)", fill=BLACK, font=title_font)

    nodes = [
        Node("Flask app", 60, 80, 750, 250),
        Node("Web handlers", 60, 370, 750, 260),
        Node("Admin API", 860, 80, 620, 280),
        Node("Security", 860, 400, 380, 220),
        Node("FileService", 1260, 400, 220, 220),
        Node("Repositories", 860, 660, 620, 270),
        Node("News model", 1260, 950, 220, 200),
        Node("DB connection", 860, 950, 380, 200),
    ]

    # Boxes
    _draw_box(
        draw,
        nodes[0].x,
        nodes[0].y,
        nodes[0].w,
        nodes[0].h,
        "Flask-приложение (app.py)",
        [
            "Веб-роуты: /, /search, /news/<id>, /spec/*, /students/*, /applicants/*, /pages/*",
            "after_request: collect_site_user_metrics → visitor_metrics_repository",
            "register_blueprint: api_bp (/api/v1)",
        ],
        title_font=body_font,
        body_font=body_font,
    )

    _draw_box(
        draw,
        nodes[1].x,
        nodes[1].y,
        nodes[1].w,
        nodes[1].h,
        "Обработчики страниц",
        [
            "main_page.home_handler",
            "search_page.search_handler",
            "news_detail_page.news_detail_handler",
            "spec_page.spec_*",
            "site_pages.* (managed/зеркала)",
            "student_pages.* (зеркала)",
            "applicant_pages.* (зеркала)",
            "notfound_page.not_found_handler",
        ],
        title_font=body_font,
        body_font=body_font,
    )

    _draw_box(
        draw,
        nodes[2].x,
        nodes[2].y,
        nodes[2].w,
        nodes[2].h,
        "Admin API Blueprint /api/v1",
        [
            "Auth: POST /auth/login",
            "Health/metrics: /health, /metrics/main, /system/status",
            "Новости: /news (GET/POST/PUT/PATCH/DELETE)",
            "Вложения: POST /media/news-image",
            "Контент: /tabs, /pages, /page-templates/*, /files",
        ],
        title_font=body_font,
        body_font=body_font,
    )

    _draw_box(
        draw,
        nodes[3].x,
        nodes[3].y,
        nodes[3].w,
        nodes[3].h,
        "Security (api/security.py)",
        ["validate_api_key", "validate_admin_credentials", "issue_access_token", "validate_access_token"],
        title_font=body_font,
        body_font=body_font,
    )

    _draw_box(
        draw,
        nodes[4].x,
        nodes[4].y,
        nodes[4].w,
        nodes[4].h,
        "FileService",
        ["scopes: content / locales / css / templates", "list_dir / read_text / write_text / delete_file"],
        title_font=body_font,
        body_font=body_font,
    )

    _draw_box(
        draw,
        nodes[5].x,
        nodes[5].y,
        nodes[5].w,
        nodes[5].h,
        "Репозитории БД",
        [
            "news_repository (CRUD + search + News→dict)",
            "admin_users_repository (login)",
            "tabs_repository (site_tabs)",
            "pages_repository (site_pages)",
            "visitor_metrics_repository (site_visits)",
        ],
        title_font=body_font,
        body_font=body_font,
    )

    _draw_box(
        draw,
        nodes[7].x,
        nodes[7].y,
        nodes[7].w,
        nodes[7].h,
        "DB connection (db/connection.py)",
        ["init_db", "get_db", "is_db_alive", "get_table_names"],
        title_font=body_font,
        body_font=body_font,
    )

    _draw_box(
        draw,
        nodes[6].x,
        nodes[6].y,
        nodes[6].w,
        nodes[6].h,
        "Модель News",
        ["models/news.py: News (localized поля, формат даты)", "News.from_dict()"],
        title_font=body_font,
        body_font=body_font,
    )

    # Edges
    _draw_center_line(draw, nodes[0].center, nodes[1].center)
    _draw_center_line(draw, nodes[0].center, nodes[2].center)
    _draw_center_line(draw, nodes[0].center, nodes[5].center)  # after_request → VisitorMetricsRepository (subset of repos)
    _draw_center_line(draw, nodes[2].center, nodes[3].center)
    _draw_center_line(draw, nodes[2].center, nodes[4].center)
    _draw_center_line(draw, nodes[2].center, nodes[5].center)
    _draw_center_line(draw, nodes[5].center, nodes[7].center)
    _draw_center_line(draw, nodes[5].center, nodes[6].center)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")


def render_database_diagram(out_path: str) -> None:
    img = Image.new("RGB", (2000, 1400), WHITE)
    draw = ImageDraw.Draw(img)

    title_font = _find_font(26)
    body_font = _find_font(18)

    draw.text((100, 20), "Схема БД (упрощённо, 5 таблиц)", fill=BLACK, font=title_font)
    draw.text((100, 60), "Внешних ключей (FK) нет.", fill=BLACK, font=body_font)

    boxes = [
        (
            "news",
            [
                "id (PK, AUTO_INCREMENT)",
                "name",
                "date",
                "description",
                "name_be",
                "name_en",
                "description_be",
                "description_en",
                "image_path",
            ],
            (90, 140, 820, 340),
        ),
        (
            "admin_users",
            [
                "id (PK, AUTO_INCREMENT)",
                "username (UNIQUE)",
                "password_hash",
                "is_active",
                "created_at",
                "updated_at",
            ],
            (1030, 140, 860, 240),
        ),
        (
            "site_visits",
            [
                "id (PK, AUTO_INCREMENT)",
                "visit_date",
                "visitor_key",
                "first_seen",
                "last_seen",
                "hits",
                "UNIQUE(visit_date, visitor_key)",
            ],
            (90, 510, 820, 320),
        ),
        (
            "site_tabs",
            [
                "id (PK, AUTO_INCREMENT)",
                "slug (UNIQUE)",
                "title",
                "menu_title",
                "content_html",
                "sort_order",
                "is_active",
                "open_in_new_tab",
                "created_at",
                "updated_at",
            ],
            (1030, 420, 860, 420),
        ),
        (
            "site_pages",
            [
                "id (PK, AUTO_INCREMENT)",
                "slug (UNIQUE)",
                "title",
                "content_html",
                "sort_order",
                "is_active",
                "created_at",
                "updated_at",
            ],
            (90, 870, 1800, 380),
        ),
    ]

    for title, lines, (x, y, w, h) in boxes:
        _draw_box(
            draw,
            x,
            y,
            w,
            h,
            title,
            lines,
            title_font=body_font,
            body_font=body_font,
            pad=20,
        )

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")


def render_use_case_diagram(out_path: str) -> None:
    img = Image.new("RGB", (2000, 1400), WHITE)
    draw = ImageDraw.Draw(img)

    title_font = _find_font(26)
    body_font = _find_font(18)
    small_font = _find_font(16)

    draw.text((100, 20), "Варианты использования (Use Case, упрощённо)", fill=BLACK, font=title_font)

    # System boundary
    sys_x, sys_y, sys_w, sys_h = 780, 110, 1180, 1200
    _rounded_rect(draw, (sys_x, sys_y, sys_x + sys_w, sys_y + sys_h), radius=22, width=2)
    draw.text((sys_x + sys_w / 2 - draw.textlength("MainSite", font=title_font) / 2, sys_y + 18), "MainSite", fill=BLACK, font=title_font)

    # Subsystems
    site_x, site_y, site_w, site_h = sys_x + 40, sys_y + 80, sys_w - 80, 520
    admin_x, admin_y, admin_w, admin_h = sys_x + 40, sys_y + 630, sys_w - 80, 520
    _rounded_rect(draw, (site_x, site_y, site_x + site_w, site_y + site_h), radius=18, width=2)
    _rounded_rect(draw, (admin_x, admin_y, admin_x + admin_w, admin_y + admin_h), radius=18, width=2)
    draw.text((site_x + site_w / 2 - draw.textlength("Веб-сайт", font=body_font) / 2, site_y + 12), "Веб-сайт", fill=BLACK, font=body_font)
    draw.text(
        (admin_x + admin_w / 2 - draw.textlength("Admin API (/api/v1)", font=body_font) / 2, admin_y + 12),
        "Admin API (/api/v1)",
        fill=BLACK,
        font=body_font,
    )

    # Actors
    actors = [
        ("Посетитель сайта\n(аноним.)", 90, 220),
        ("Студент", 90, 480),
        ("Абитуриент", 90, 740),
        ("Администратор\nвнешней админки", 90, 1000),
    ]
    for name, ax, ay in actors:
        # Actor circle approximation using rounded rectangle
        _rounded_rect(draw, (ax, ay, ax + 220, ay + 120), radius=60, width=2)
        draw.text((ax + 110 - draw.textlength(name.split("\n")[0], font=small_font) / 2, ay + 18), name.split("\n")[0], fill=BLACK, font=small_font)
        if "\n" in name:
            draw.text((ax + 110 - draw.textlength(name.split("\n")[1], font=small_font) / 2, ay + 58), name.split("\n")[1], fill=BLACK, font=small_font)

    # Use cases as rounded-rect "ovals"
    # Website
    uc_site = [
        ("Просмотр главной\n(лента новостей)", site_x + 30, site_y + 90),
        ("Поиск новостей", site_x + 30, site_y + 200),
        ("Просмотр новости", site_x + 30, site_y + 310),
        ("Просмотр spec/*", site_x + 420, site_y + 90),
        ("Просмотр студентов", site_x + 420, site_y + 200),
        ("Просмотр абитуриентов", site_x + 420, site_y + 310),
        ("Просмотр статических страниц", site_x + 220, site_y + 420),
    ]
    for label, ux, uy in uc_site:
        _rounded_rect(draw, (ux, uy, ux + 360, uy + 90), radius=45, width=2)
        for i, part in enumerate(label.split("\n")):
            draw.text((ux + 180 - draw.textlength(part, font=small_font) / 2, uy + 18 + i * 36), part, fill=BLACK, font=small_font)

    # Admin API
    uc_admin = [
        ("Логин и получение\ntoken (POST /auth/login)", admin_x + 30, admin_y + 90),
        ("CRUD новостей (/news)", admin_x + 30, admin_y + 210),
        ("Загрузка изображения\nновостей (/media/news-image)", admin_x + 30, admin_y + 330),
        ("CRUD вкладок (/tabs)", admin_x + 430, admin_y + 90),
        ("CRUD страниц (/pages)", admin_x + 430, admin_y + 210),
        ("Управление\npage-templates", admin_x + 430, admin_y + 330),
        # Два последних блока ставим ниже, чтобы не вылезать за правую границу холста.
        ("Управление файлами\n(/files)", admin_x + 30, admin_y + 430),
        ("Health/metrics\n(/health,/metrics/main,/system/status)", admin_x + 430, admin_y + 430),
    ]
    for label, ux, uy in uc_admin:
        _rounded_rect(draw, (ux, uy, ux + 420, uy + 90), radius=45, width=2)
        parts = label.split("\n")
        for i, part in enumerate(parts[:2]):
            # Keep only up to 2 lines to avoid clutter.
            draw.text((ux + 210 - draw.textlength(part, font=small_font) / 2, uy + 18 + i * 36), part, fill=BLACK, font=small_font)

    # Connections (simple straight lines)
    # Anonymous → main/search/news/spec/static
    _draw_center_line(draw, (actors[0][1] + 220, actors[0][2] + 60), (site_x + 30 + 170, site_y + 90 + 45))
    _draw_center_line(draw, (actors[0][1] + 220, actors[0][2] + 60), (site_x + 30 + 170, site_y + 200 + 45))
    _draw_center_line(draw, (actors[0][1] + 220, actors[0][2] + 60), (site_x + 30 + 170, site_y + 310 + 45))
    _draw_center_line(draw, (actors[0][1] + 220, actors[0][2] + 60), (site_x + 420 + 170, site_y + 90 + 45))
    _draw_center_line(draw, (actors[0][1] + 220, actors[0][2] + 60), (site_x + 220 + 250, site_y + 420 + 45))

    # Student → students
    _draw_center_line(draw, (actors[1][1] + 220, actors[1][2] + 60), (site_x + 420 + 170, site_y + 200 + 45))
    # Applicant → applicants
    _draw_center_line(draw, (actors[2][1] + 220, actors[2][2] + 60), (site_x + 420 + 170, site_y + 310 + 45))
    # Admin → login + CRUD
    _draw_center_line(draw, (actors[3][1] + 220, actors[3][2] + 60), (admin_x + 30 + 200, admin_y + 90 + 45))
    _draw_center_line(draw, (actors[3][1] + 220, actors[3][2] + 60), (admin_x + 30 + 200, admin_y + 210 + 45))
    _draw_center_line(draw, (actors[3][1] + 220, actors[3][2] + 60), (admin_x + 30 + 200, admin_y + 330 + 45))
    _draw_center_line(draw, (actors[3][1] + 220, actors[3][2] + 60), (admin_x + 430 + 210, admin_y + 90 + 45))

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")


def main() -> None:
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(repo_root, "diagrams")

    render_class_diagram(os.path.join(out_dir, "uml_classes_mainsite.png"))
    render_database_diagram(os.path.join(out_dir, "uml_database_mainsite.png"))
    render_use_case_diagram(os.path.join(out_dir, "uml_usecases_mainsite.png"))

    print(f"PNG diagrams generated into: {out_dir}")


if __name__ == "__main__":
    main()

