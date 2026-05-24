"""
Генерация диаграмм для диплома (приложения А, Б, В).
Оформление: ч/б, шрифт Arial, подписи по ГОСТ 2.105 / СТБ 6.38 (иллюстрации в ПЗ).
Нотация: ER (логическая схема БД), UML 2.x (классы, варианты использования).
"""
from __future__ import annotations

import os
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont

# ГОСТ: иллюстрации в пояснительной записке — чёрные линии на белом фоне
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LINE_W = 2

# A4 альбомная ~ 297×210 мм при ~150 dpi
CANVAS_W = 2480
CANVAS_H = 1754
MARGIN = 80
CAPTION_H = 56


def _find_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\ARIAL.TTF",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size=size)
            except OSError:
                pass
    return ImageFont.load_default()


def _text_center(draw: ImageDraw.ImageDraw, xy: Tuple[int, int, int, int], text: str, font: ImageFont.ImageFont) -> None:
    x0, y0, x1, y1 = xy
    lines = text.split("\n")
    line_h = font.size + 4
    total_h = len(lines) * line_h
    y = y0 + (y1 - y0 - total_h) // 2
    for line in lines:
        tw = draw.textlength(line, font=font)
        draw.text((x0 + (x1 - x0 - tw) / 2, y), line, fill=BLACK, font=font)
        y += line_h


def _caption(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> None:
    tw = draw.textlength(text, font=font)
    x = (CANVAS_W - tw) / 2
    draw.text((x, CANVAS_H - CAPTION_H + 8), text, fill=BLACK, font=font)


def _line(draw: ImageDraw.ImageDraw, a: Tuple[int, int], b: Tuple[int, int], *, dashed: bool = False) -> None:
    if not dashed:
        draw.line((*a, *b), fill=BLACK, width=LINE_W)
        return
    x0, y0, x1, y1 = a[0], a[1], b[0], b[1]
    length = int(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5)
    if length == 0:
        return
    dash, gap = 10, 7
    steps = length // (dash + gap)
    for i in range(steps + 1):
        t0 = i / max(steps, 1)
        t1 = min(1.0, (i * (dash + gap) + dash) / length)
        sx = int(x0 + (x1 - x0) * (i * (dash + gap) / length))
        sy = int(y0 + (y1 - y0) * (i * (dash + gap) / length))
        ex = int(x0 + (x1 - x0) * t1)
        ey = int(y0 + (y1 - y0) * t1)
        draw.line((sx, sy, ex, ey), fill=BLACK, width=LINE_W)


def _arrow(draw: ImageDraw.ImageDraw, a: Tuple[int, int], b: Tuple[int, int], *, dashed: bool = False) -> None:
    _line(draw, a, b, dashed=dashed)
    import math

    x0, y0, x1, y1 = a[0], a[1], b[0], b[1]
    ang = math.atan2(y1 - y0, x1 - x0)
    size = 12
    p1 = (x1 - size * math.cos(ang - 0.4), y1 - size * math.sin(ang - 0.4))
    p2 = (x1 - size * math.cos(ang + 0.4), y1 - size * math.sin(ang + 0.4))
    draw.polygon([(x1, y1), p1, p2], outline=BLACK, fill=BLACK)


def _draw_actor(draw: ImageDraw.ImageDraw, cx: int, cy: int, label: str, font: ImageFont.ImageFont) -> Tuple[int, int]:
    """UML-актёр (человечек): круг + тело + подпись."""
    r = 22
    draw.ellipse((cx - r, cy - 50 - r, cx + r, cy - 50 + r), outline=BLACK, width=LINE_W)
    draw.line((cx, cy - 50 + r, cx, cy + 10), fill=BLACK, width=LINE_W)
    draw.line((cx - 35, cy - 20, cx + 35, cy - 20), fill=BLACK, width=LINE_W)
    draw.line((cx, cy + 10, cx - 28, cy + 55), fill=BLACK, width=LINE_W)
    draw.line((cx, cy + 10, cx + 28, cy + 55), fill=BLACK, width=LINE_W)
    for i, ln in enumerate(label.split("\n")):
        tw = draw.textlength(ln, font=font)
        draw.text((cx - tw / 2, cy + 65 + i * (font.size + 2)), ln, fill=BLACK, font=font)
    return (cx, cy - 50)


def _draw_use_case(draw: ImageDraw.ImageDraw, cx: int, cy: int, w: int, h: int, text: str, font: ImageFont.ImageFont) -> Tuple[int, int, int, int]:
    x0, y0 = cx - w // 2, cy - h // 2
    x1, y1 = cx + w // 2, cy + h // 2
    draw.ellipse((x0, y0, x1, y1), outline=BLACK, width=LINE_W)
    _text_center(draw, (x0 + 12, y0 + 8, x1 - 12, y1 - 8), text, font)
    return (x0, y0, x1, y1)


def _draw_uml_class(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    w: int,
    name: str,
    attrs: List[str],
    methods: List[str],
    *,
    title_font: ImageFont.ImageFont,
    body_font: ImageFont.ImageFont,
) -> Tuple[int, int, int, int]:
    pad = 10
    line_h = body_font.size + 5
    h_name = title_font.size + pad * 2
    h_attrs = max(line_h, len(attrs) * line_h + pad)
    h_methods = max(line_h, len(methods) * line_h + pad)
    h = h_name + h_attrs + h_methods
    x1, y1 = x + w, y + h

    draw.rectangle((x, y, x1, y1), outline=BLACK, width=LINE_W)
    draw.line((x, y + h_name, x1, y + h_name), fill=BLACK, width=LINE_W)
    draw.line((x, y + h_name + h_attrs, x1, y + h_name + h_attrs), fill=BLACK, width=LINE_W)

    tw = draw.textlength(name, font=title_font)
    draw.text((x + (w - tw) / 2, y + pad - 2), name, fill=BLACK, font=title_font)

    ay = y + h_name + pad - 4
    for a in attrs:
        draw.text((x + pad, ay), a, fill=BLACK, font=body_font)
        ay += line_h
    my = y + h_name + h_attrs + pad - 4
    for m in methods:
        draw.text((x + pad, my), m, fill=BLACK, font=body_font)
        my += line_h

    return (x, y, x1, y1)


def _draw_er_entity(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    w: int,
    entity: str,
    fields: List[str],
    *,
    title_font: ImageFont.ImageFont,
    body_font: ImageFont.ImageFont,
) -> Tuple[int, int, int, int]:
    pad = 14
    line_h = body_font.size + 6
    h_title = title_font.size + pad * 2
    h_body = len(fields) * line_h + pad
    h = h_title + h_body
    x1, y1 = x + w, y + h
    draw.rectangle((x, y, x1, y1), outline=BLACK, width=LINE_W)
    draw.line((x, y + h_title, x1, y + h_title), fill=BLACK, width=LINE_W)
    tw = draw.textlength(entity, font=title_font)
    draw.text((x + (w - tw) / 2, y + pad - 2), entity, fill=BLACK, font=title_font)
    fy = y + h_title + pad - 4
    for f in fields:
        draw.text((x + pad, fy), f, fill=BLACK, font=body_font)
        fy += line_h
    return (x, y, x1, y1)


def render_database_diagram(out_path: str) -> None:
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), WHITE)
    draw = ImageDraw.Draw(img)
    title_font = _find_font(22)
    body_font = _find_font(16)
    note_font = _find_font(15)

    draw.text(
        (MARGIN, 28),
        "Логическая схема базы данных (PostgreSQL, схема public)",
        fill=BLACK,
        font=title_font,
    )
    draw.text(
        (MARGIN, 58),
        "Связи между таблицами внешними ключами не заданы; целостность обеспечивается на уровне приложения.",
        fill=BLACK,
        font=note_font,
    )

    entities = [
        (
            "news",
            [
                "id : SERIAL (PK)",
                "name : VARCHAR(255)",
                "date : DATE",
                "description : TEXT",
                "name_be, name_en : VARCHAR(255)",
                "description_be, description_en : TEXT",
                "image_path : VARCHAR(255)",
            ],
            (MARGIN, 110, 720, 0),
        ),
        (
            "admin_users",
            [
                "id : SERIAL (PK)",
                "username : VARCHAR(64) UNIQUE",
                "password_hash : VARCHAR(255)",
                "is_active : BOOLEAN",
                "created_at, updated_at : TIMESTAMPTZ",
            ],
            (MARGIN + 780, 110, 720, 0),
        ),
        (
            "site_visits",
            [
                "id : BIGSERIAL (PK)",
                "visit_date : DATE",
                "visitor_key : CHAR(64)",
                "first_seen, last_seen : TIMESTAMP",
                "hits : INT",
                "UNIQUE (visit_date, visitor_key)",
            ],
            (MARGIN, 430, 720, 0),
        ),
        (
            "site_tabs",
            [
                "id : SERIAL (PK)",
                "slug : VARCHAR(120) UNIQUE",
                "title, menu_title : VARCHAR",
                "content_html : TEXT",
                "sort_order : INT",
                "is_active, open_in_new_tab : BOOLEAN",
                "created_at, updated_at : TIMESTAMPTZ",
            ],
            (MARGIN + 780, 380, 720, 0),
        ),
        (
            "site_pages",
            [
                "id : SERIAL (PK)",
                "slug : VARCHAR(120) UNIQUE",
                "title : VARCHAR(255)",
                "content_html : TEXT",
                "sort_order : INT",
                "is_active : BOOLEAN",
                "created_at, updated_at : TIMESTAMPTZ",
            ],
            (MARGIN, 750, 1520, 0),
        ),
    ]

    for name, fields, (x, y, w, _) in entities:
        _draw_er_entity(draw, x, y, w, name, fields, title_font=title_font, body_font=body_font)

    _caption(
        draw,
        "Рисунок А.1 – Диаграмма базы данных серверной части веб-сайта "
        "УО «Новопольский аграрно-экономический колледж»",
        _find_font(18),
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG", dpi=(150, 150))


def render_class_diagram(out_path: str) -> None:
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), WHITE)
    draw = ImageDraw.Draw(img)
    title_font = _find_font(17)
    body_font = _find_font(14)
    small = _find_font(13)

    draw.text((MARGIN, 24), "Диаграмма классов серверной части (фрагмент)", fill=BLACK, font=_find_font(22))

    boxes = []
    boxes.append(
        _draw_uml_class(
            draw, 60, 90, 340, "News",
            [
                "- id : int",
                "- name, description : str",
                "- name_be, name_en : str",
                "- date, image_path",
            ],
            [
                "+ localized_name(lang)",
                "+ localized_description(lang)",
                "+ formatted_date(lang)",
                "+ from_dict(data)",
            ],
            title_font=title_font, body_font=body_font,
        )
    )
    boxes.append(
        _draw_uml_class(
            draw, 450, 90, 360, "Config",
            ["- database : DatabaseConfig", "- server : ServerConfig", "- admin_api_key : str"],
            ["+ load_config(path)"],
            title_font=title_font, body_font=body_font,
        )
    )
    boxes.append(
        _draw_uml_class(
            draw, 860, 90, 320, "DatabaseConfig",
            ["- host, port, user", "- password, name"],
            [],
            title_font=title_font, body_font=body_font,
        )
    )
    boxes.append(
        _draw_uml_class(
            draw, 60, 400, 400, "«module» news_repository",
            [],
            [
                "+ get_all_news()",
                "+ get_news_by_id(id)",
                "+ search_news(q)",
                "+ insert_news(row)",
                "+ update_news_*()",
                "+ delete_news(id)",
            ],
            title_font=title_font, body_font=body_font,
        )
    )
    boxes.append(
        _draw_uml_class(
            draw, 500, 400, 380, "«module» db.connection",
            ["_db_connection", "_db_config"],
            ["+ init_db(...)", "+ get_db()", "+ is_db_alive()"],
            title_font=title_font, body_font=body_font,
        )
    )
    boxes.append(
        _draw_uml_class(
            draw, 930, 400, 420, "Flask Application",
            ["- app : Flask", "- config"],
            ["+ route handlers", "+ register_blueprint(api)"],
            title_font=title_font, body_font=body_font,
        )
    )
    boxes.append(
        _draw_uml_class(
            draw, 60, 720, 400, "«module» page handlers",
            [],
            [
                "home_handler()",
                "search_handler()",
                "news_detail_handler()",
                "site/student/applicant pages",
            ],
            title_font=title_font, body_font=body_font,
        )
    )
    boxes.append(
        _draw_uml_class(
            draw, 500, 720, 400, "ApiBlueprint /api/v1",
            [],
            [
                "auth/login",
                "CRUD /news, /pages, /tabs",
                "/files, /metrics/main",
            ],
            title_font=title_font, body_font=body_font,
        )
    )
    boxes.append(
        _draw_uml_class(
            draw, 960, 720, 390, "«module» api.security",
            [],
            [
                "validate_api_key()",
                "validate_admin_credentials()",
                "issue_access_token()",
            ],
            title_font=title_font, body_font=body_font,
        )
    )
    boxes.append(
        _draw_uml_class(
            draw, 1420, 90, 360, "«module» pages_repository",
            [],
            ["+ get_page_by_slug()", "+ create_page()", "+ search_pages()"],
            title_font=title_font, body_font=body_font,
        )
    )
    boxes.append(
        _draw_uml_class(
            draw, 1420, 400, 360, "«module» visitor_metrics",
            [],
            ["+ record_visit()", "+ get_user_metrics()"],
            title_font=title_font, body_font=body_font,
        )
    )

    def center(b):
        return ((b[0] + b[2]) // 2, (b[1] + b[3]) // 2)

    # Зависимости (пунктир со стрелкой — UML dependency)
    _arrow(draw, center(boxes[3]), center(boxes[0]), dashed=True)
    _arrow(draw, center(boxes[3]), center(boxes[4]), dashed=True)
    _arrow(draw, center(boxes[6]), center(boxes[3]), dashed=True)
    _arrow(draw, center(boxes[5]), center(boxes[1]), dashed=True)
    _arrow(draw, center(boxes[5]), center(boxes[6]), dashed=True)
    _arrow(draw, center(boxes[5]), center(boxes[7]), dashed=True)
    _arrow(draw, center(boxes[7]), center(boxes[3]), dashed=True)
    _arrow(draw, center(boxes[7]), center(boxes[8]), dashed=True)
    _arrow(draw, center(boxes[5]), center(boxes[4]), dashed=True)
    _arrow(draw, center(boxes[9]), center(boxes[4]), dashed=True)
    _arrow(draw, center(boxes[10]), center(boxes[4]), dashed=True)

    draw.text((60, 1080), "Примечание: репозитории tabs_repository, admin_users_repository "
              "аналогичны pages_repository.", fill=BLACK, font=small)

    _caption(
        draw,
        "Рисунок Б.1 – Диаграмма классов серверной части веб-сайта "
        "УО «Новопольский аграрно-экономический колледж»",
        _find_font(18),
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG", dpi=(150, 150))


def render_use_case_diagram(out_path: str) -> None:
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), WHITE)
    draw = ImageDraw.Draw(img)
    font = _find_font(15)
    small = _find_font(14)
    title_font = _find_font(22)

    draw.text((MARGIN, 24), "Диаграмма вариантов использования", fill=BLACK, font=title_font)

    # Граница системы (UML)
    sys_x, sys_y = 520, 95
    sys_w, sys_h = 1880, 1480
    draw.rectangle((sys_x, sys_y, sys_x + sys_w, sys_y + sys_h), outline=BLACK, width=LINE_W)
    _text_center(
        draw,
        (sys_x, sys_y + 8, sys_x + sys_w, sys_y + 48),
        "Серверная часть веб-сайта УО «Новопольский аграрно-экономический колледж»",
        font,
    )

    # Подсистемы
    web_y, api_y = sys_y + 60, sys_y + 780
    draw.rectangle((sys_x + 30, web_y, sys_x + sys_w - 30, api_y - 30), outline=BLACK, width=1)
    draw.rectangle((sys_x + 30, api_y, sys_x + sys_w - 30, sys_y + sys_h - 40), outline=BLACK, width=1)
    draw.text((sys_x + 50, web_y + 10), "Публичный веб-интерфейс (Flask + Jinja2)", fill=BLACK, font=small)
    draw.text((sys_x + 50, api_y + 10), "REST API администрирования (/api/v1)", fill=BLACK, font=small)

    actors = [
        ("Посетитель\nсайта", 200, 220),
        ("Абитуриент", 200, 480),
        ("Студент", 200, 700),
        ("Администратор", 200, 1180),
    ]
    actor_tops = []
    for label, ax, ay in actors:
        actor_tops.append(_draw_actor(draw, ax, ay, label, font))

    def uc(cx, cy, text, w=300, h=72):
        return _draw_use_case(draw, cx, cy, w, h, text, small)

    # Веб-прецеденты
    uc_web = [
        uc(sys_x + 280, web_y + 120, "Просмотр\nглавной страницы"),
        uc(sys_x + 620, web_y + 120, "Просмотр\nсписка новостей"),
        uc(sys_x + 960, web_y + 120, "Просмотр\nновости"),
        uc(sys_x + 280, web_y + 280, "Поиск\nинформации"),
        uc(sys_x + 620, web_y + 280, "Просмотр раздела\n«Абитуриенту»"),
        uc(sys_x + 960, web_y + 280, "Просмотр раздела\n«Студенту»"),
        uc(sys_x + 1300, web_y + 200, "Просмотр\nспециальностей"),
        uc(sys_x + 480, web_y + 440, "Переключение\nязыка (ru/be/en)"),
        uc(sys_x + 900, web_y + 440, "Просмотр служебных\nстраниц (контакты, privacy)"),
        uc(sys_x + 1320, web_y + 440, "Учёт посещений\n(метрики)"),
    ]

    # API-прецеденты
    uc_api = [
        uc(sys_x + 300, api_y + 120, "Авторизация\nадминистратора", w=320, h=78),
        uc(sys_x + 680, api_y + 120, "Управление\nновостями", w=320, h=78),
        uc(sys_x + 1060, api_y + 120, "Загрузка изображений\nновостей", w=340, h=78),
        uc(sys_x + 300, api_y + 300, "Управление\nстраницами", w=320, h=78),
        uc(sys_x + 680, api_y + 300, "Управление\nвкладками меню", w=320, h=78),
        uc(sys_x + 1060, api_y + 300, "Редактирование\nшаблонов страниц", w=340, h=78),
        uc(sys_x + 300, api_y + 480, "Управление файлами\nstatic", w=320, h=78),
        uc(sys_x + 680, api_y + 480, "Просмотр метрик\nи статуса системы", w=340, h=78),
    ]

    def link_actor(actor_idx, uc_box):
        ax, ay = actors[actor_idx][1], actor_tops[actor_idx][1]
        cx = (uc_box[0] + uc_box[2]) // 2
        cy = (uc_box[1] + uc_box[3]) // 2
        _line(draw, (ax + 60, ay), (uc_box[0], cy))

    # Связи актёров
    link_actor(0, uc_web[0])
    link_actor(0, uc_web[1])
    link_actor(0, uc_web[2])
    link_actor(0, uc_web[3])
    link_actor(0, uc_web[6])
    link_actor(0, uc_web[7])
    link_actor(0, uc_web[8])

    link_actor(1, uc_web[4])
    link_actor(2, uc_web[5])
    link_actor(3, uc_api[0])
    for j in range(1, len(uc_api)):
        link_actor(3, uc_api[j])

    # <<include>> Авторизация → Управление новостями
    a0 = ((uc_api[0][0] + uc_api[0][2]) // 2, (uc_api[0][1] + uc_api[0][3]) // 2)
    a1 = ((uc_api[1][0] + uc_api[1][2]) // 2, uc_api[1][1])
    _arrow(draw, a1, (a0[0], a0[1] + 30), dashed=True)
    tw = draw.textlength("<<включить>>", font=small)
    draw.text(((a0[0] + a1[0]) / 2 - tw / 2, (a0[1] + a1[1]) / 2 - 20), "<<включить>>", fill=BLACK, font=small)

    _caption(
        draw,
        "Рисунок В.1 – Диаграмма вариантов использования серверной части веб-сайта "
        "УО «Новопольский аграрно-экономический колледж»",
        _find_font(18),
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG", dpi=(150, 150))


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "diagrams")
    render_database_diagram(os.path.join(out, "appendix_A_database.png"))
    render_class_diagram(os.path.join(out, "appendix_B_classes.png"))
    render_use_case_diagram(os.path.join(out, "appendix_C_use_cases.png"))
    # Совместимость со старыми именами
    render_database_diagram(os.path.join(out, "uml_database_mainsite.png"))
    render_class_diagram(os.path.join(out, "uml_classes_mainsite.png"))
    render_use_case_diagram(os.path.join(out, "uml_usecases_mainsite.png"))
    print(f"Диаграммы сохранены в: {out}")


if __name__ == "__main__":
    main()
