"""
Генерация UML/ER-диаграмм для диплома (приложения А, Б, В).
На выходе — только графика диаграммы (без заголовков, примечаний и подписей «Рисунок …»).
Размер выхода — A4 @150 dpi; содержимое масштабируется на весь фон листа.
"""
from __future__ import annotations

import os
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LINE_W = 3

# A4 @150 dpi: ширина альбомного 1754 px, высота (длинная сторона) 1754 px
CANVAS_W = 1754
CANVAS_H = 1754
MARGIN = 24
ROW_GAP = 48
COL_GAP = 28
# Отступ от края листа после масштабирования (0 = на весь фон)
FIT_MARGIN = 0

FONT_CLASS_TITLE = 26
FONT_CLASS_BODY = 22
FONT_USE_CASE = 22
FONT_USE_CASE_SMALL = 20
FONT_ER_TITLE = 26
FONT_ER_BODY = 22


def _content_bbox(img: Image.Image) -> Tuple[int, int, int, int] | None:
    """Границы нарисованного (не белого) содержимого."""
    px = img.load()
    w, h = img.size
    min_x, min_y = w, h
    max_x, max_y = 0, 0
    found = False
    step = max(1, min(w, h) // 400)
    for y in range(0, h, step):
        for x in range(0, w, step):
            if px[x, y] != WHITE:
                found = True
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    if not found:
        return None
    pad = 8
    return (
        max(0, min_x - pad),
        max(0, min_y - pad),
        min(w, max_x + pad),
        min(h, max_y + pad),
    )


def _save_filled_canvas(img: Image.Image, out_path: str) -> None:
    """Масштабирует содержимое на весь фон CANVAS_W×CANVAS_H (ширина и высота)."""
    bbox = _content_bbox(img)
    if not bbox:
        fitted = img.resize((CANVAS_W, CANVAS_H), Image.Resampling.LANCZOS)
    else:
        crop = img.crop(bbox)
        target_w = max(1, CANVAS_W - 2 * FIT_MARGIN)
        target_h = max(1, CANVAS_H - 2 * FIT_MARGIN)
        scaled = crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
        if FIT_MARGIN == 0:
            fitted = scaled
        else:
            fitted = Image.new("RGB", (CANVAS_W, CANVAS_H), WHITE)
            fitted.paste(scaled, (FIT_MARGIN, FIT_MARGIN))
    if fitted.size != (CANVAS_W, CANVAS_H):
        fitted = fitted.resize((CANVAS_W, CANVAS_H), Image.Resampling.LANCZOS)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    fitted.save(out_path, "PNG", dpi=(150, 150))


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
    line_h = font.size + 6
    total_h = len(lines) * line_h
    y = y0 + (y1 - y0 - total_h) // 2
    for line in lines:
        tw = draw.textlength(line, font=font)
        draw.text((x0 + (x1 - x0 - tw) / 2, y), line, fill=BLACK, font=font)
        y += line_h


def _line(draw: ImageDraw.ImageDraw, a: Tuple[int, int], b: Tuple[int, int], *, dashed: bool = False) -> None:
    if not dashed:
        draw.line((*a, *b), fill=BLACK, width=LINE_W)
        return
    x0, y0, x1, y1 = a[0], a[1], b[0], b[1]
    length = int(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5)
    if length == 0:
        return
    dash, gap = 12, 8
    steps = length // (dash + gap)
    for i in range(steps + 1):
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
    size = 16
    p1 = (x1 - size * math.cos(ang - 0.4), y1 - size * math.sin(ang - 0.4))
    p2 = (x1 - size * math.cos(ang + 0.4), y1 - size * math.sin(ang + 0.4))
    draw.polygon([(x1, y1), p1, p2], outline=BLACK, fill=BLACK)


def _draw_actor(draw: ImageDraw.ImageDraw, cx: int, cy: int, label: str, font: ImageFont.ImageFont) -> Tuple[int, int]:
    r = 28
    draw.ellipse((cx - r, cy - 58 - r, cx + r, cy - 58 + r), outline=BLACK, width=LINE_W)
    draw.line((cx, cy - 58 + r, cx, cy + 12), fill=BLACK, width=LINE_W)
    draw.line((cx - 42, cy - 18, cx + 42, cy - 18), fill=BLACK, width=LINE_W)
    draw.line((cx, cy + 12, cx - 34, cy + 62), fill=BLACK, width=LINE_W)
    draw.line((cx, cy + 12, cx + 34, cy + 62), fill=BLACK, width=LINE_W)
    for i, ln in enumerate(label.split("\n")):
        tw = draw.textlength(ln, font=font)
        draw.text((cx - tw / 2, cy + 72 + i * (font.size + 4)), ln, fill=BLACK, font=font)
    return (cx, cy - 58)


def _draw_use_case(
    draw: ImageDraw.ImageDraw, cx: int, cy: int, w: int, h: int, text: str, font: ImageFont.ImageFont
) -> Tuple[int, int, int, int]:
    x0, y0 = cx - w // 2, cy - h // 2
    x1, y1 = cx + w // 2, cy + h // 2
    draw.ellipse((x0, y0, x1, y1), outline=BLACK, width=LINE_W)
    _text_center(draw, (x0 + 14, y0 + 10, x1 - 14, y1 - 10), text, font)
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
    pad = 12
    line_h = body_font.size + 6
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
    line_h = body_font.size + 8
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


def _class_row_height(
    specs: List[Tuple[int, int, str, List[str], List[str]]],
    *,
    title_font: ImageFont.ImageFont,
    body_font: ImageFont.ImageFont,
) -> int:
    pad = 12
    line_h = body_font.size + 6
    h_name = title_font.size + pad * 2
    max_h = 0
    for _x, _w, _name, attrs, methods in specs:
        h_attrs = max(line_h, len(attrs) * line_h + pad)
        h_methods = max(line_h, len(methods) * line_h + pad)
        max_h = max(max_h, h_name + h_attrs + h_methods)
    return max_h


def _draw_class_row(
    draw: ImageDraw.ImageDraw,
    y: int,
    specs: List[Tuple[int, int, str, List[str], List[str]]],
    *,
    title_font: ImageFont.ImageFont,
    body_font: ImageFont.ImageFont,
) -> Tuple[List[Tuple[int, int, int, int]], int]:
    boxes: List[Tuple[int, int, int, int]] = []
    row_bottom = y
    for x, w, name, attrs, methods in specs:
        box = _draw_uml_class(draw, x, y, w, name, attrs, methods, title_font=title_font, body_font=body_font)
        boxes.append(box)
        row_bottom = max(row_bottom, box[3])
    return boxes, row_bottom


def _spread_row_horizontally(
    specs: List[Tuple[int, int, str, List[str], List[str]]],
    *,
    left: int = MARGIN,
    right: int = CANVAS_W - MARGIN,
) -> List[Tuple[int, int, str, List[str], List[str]]]:
    """Равномерно распределяет блоки строки от левого до правого края."""
    if not specs:
        return specs
    n = len(specs)
    span = right - left
    gap = COL_GAP
    gaps_total = gap * max(0, n - 1)
    weights = [w for _x, w, *_ in specs]
    sum_w = max(1, sum(weights))
    scale = (span - gaps_total) / sum_w
    widths = [max(100, int(w * scale)) for w in weights]
    used = sum(widths) + gaps_total
    if used < span:
        widths[-1] += span - used
    elif used > span:
        overflow = used - span
        for i in range(n):
            cut = overflow // (n - i)
            widths[i] = max(90, widths[i] - cut)
            overflow -= cut
            if overflow <= 0:
                break
    out: List[Tuple[int, int, str, List[str], List[str]]] = []
    x = left
    for (_x, _w, name, attrs, methods), nw in zip(specs, widths):
        out.append((x, nw, name, attrs, methods))
        x += nw + gap
    return out


def _draw_class_rows_fill_canvas(
    draw: ImageDraw.ImageDraw,
    rows: List[List[Tuple[int, int, str, List[str], List[str]]]],
    *,
    title_font: ImageFont.ImageFont,
    body_font: ImageFont.ImageFont,
) -> List[Tuple[int, int, int, int]]:
    """Распределяет строки классов по всей высоте и ширине холста."""
    spread_rows = [_spread_row_horizontally(row) for row in rows]
    heights = [_class_row_height(row, title_font=title_font, body_font=body_font) for row in spread_rows]
    n = len(spread_rows)
    usable = CANVAS_H - 2 * MARGIN
    gaps = max(ROW_GAP, (usable - sum(heights)) // (n + 1))
    y = MARGIN + gaps
    all_boxes: List[Tuple[int, int, int, int]] = []
    for row_specs, rh in zip(spread_rows, heights):
        row_boxes, bottom = _draw_class_row(
            draw, y, row_specs, title_font=title_font, body_font=body_font
        )
        all_boxes.extend(row_boxes)
        y = bottom + gaps
    return all_boxes


def render_database_diagram(out_path: str) -> None:
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), WHITE)
    draw = ImageDraw.Draw(img)
    title_font = _find_font(FONT_ER_TITLE)
    body_font = _find_font(FONT_ER_BODY)

    col_w = (CANVAS_W - 2 * MARGIN - COL_GAP) // 2
    left_x = MARGIN
    right_x = MARGIN + col_w + COL_GAP

    left_specs = [
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
        ),
    ]
    right_specs = [
        (
            "admin_users",
            [
                "id : SERIAL (PK)",
                "username : VARCHAR(64) UNIQUE",
                "password_hash : VARCHAR(255)",
                "is_active : BOOLEAN",
                "created_at, updated_at : TIMESTAMPTZ",
            ],
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
            ],
        ),
    ]

    def entity_h(fields: list) -> int:
        pad = 14
        line_h = body_font.size + 8
        return title_font.size + pad * 2 + len(fields) * line_h + pad

    left_heights = [entity_h(f) for _n, f in left_specs]
    right_heights = [entity_h(f) for _n, f in right_specs]
    pages_h = entity_h(
        [
            "id : SERIAL (PK)",
            "slug : VARCHAR(120) UNIQUE",
            "title : VARCHAR(255)",
            "content_html : TEXT",
            "sort_order : INT",
            "is_active : BOOLEAN",
        ]
    )
    col_rows = max(len(left_specs), len(right_specs))
    col_block = sum(max(left_heights[i] if i < len(left_heights) else 0,
                        right_heights[i] if i < len(right_heights) else 0)
                    for i in range(col_rows))
    col_gaps = max(0, col_rows - 1) * ROW_GAP
    bottom_block = pages_h
    total_h = col_block + col_gaps + ROW_GAP + bottom_block
    usable_h = CANVAS_H - 2 * MARGIN
    extra = max(0, usable_h - total_h)
    v_gap = ROW_GAP + extra // (col_rows + 2)

    y_left = MARGIN
    y_right = MARGIN
    for i, (_name, fields) in enumerate(left_specs):
        box = _draw_er_entity(draw, left_x, y_left, col_w, _name, fields, title_font=title_font, body_font=body_font)
        y_left = box[3] + v_gap
    for i, (_name, fields) in enumerate(right_specs):
        box = _draw_er_entity(draw, right_x, y_right, col_w, _name, fields, title_font=title_font, body_font=body_font)
        y_right = box[3] + v_gap

    pages_y = max(y_left, y_right) + v_gap
    pages_w = col_w * 2 + COL_GAP
    pages_x = MARGIN
    _draw_er_entity(
        draw,
        pages_x,
        pages_y,
        pages_w,
        "site_pages",
        [
            "id : SERIAL (PK)",
            "slug : VARCHAR(120) UNIQUE",
            "title : VARCHAR(255)",
            "content_html : TEXT",
            "sort_order : INT",
            "is_active : BOOLEAN",
        ],
        title_font=title_font,
        body_font=body_font,
    )

    _save_filled_canvas(img, out_path)


def render_class_diagram(out_path: str) -> None:
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), WHITE)
    draw = ImageDraw.Draw(img)
    title_font = _find_font(FONT_CLASS_TITLE)
    body_font = _find_font(FONT_CLASS_BODY)

    row1 = [
        (40, 300, "News", ["- id : int", "- name, description : str", "- name_be, name_en : str", "- date, image_path"],
         ["+ localized_name(lang)", "+ localized_description(lang)", "+ formatted_date(lang)", "+ from_dict(data)"]),
        (370, 320, "Config", ["- database : DatabaseConfig", "- server : ServerConfig", "- admin_api_key : str"],
         ["+ load_config(path)"]),
        (720, 300, "DatabaseConfig", ["- host, port, user", "- password, name"], []),
        (1060, 340, "«module» pages_repository", [],
         ["+ get_page_by_slug()", "+ create_page()", "+ search_pages()"]),
        (1420, 300, "«module» visitor_metrics", [], ["+ record_visit()", "+ get_user_metrics()"]),
    ]
    row2 = [
        (40, 360, "«module» news_repository", [],
         ["+ get_all_news()", "+ get_news_by_id(id)", "+ search_news(q)", "+ insert_news(row)",
          "+ update_news_*()", "+ delete_news(id)"]),
        (430, 340, "«module» db.connection", ["_db_connection", "_db_config"],
         ["+ init_db(...)", "+ get_db()", "+ is_db_alive()"]),
        (800, 380, "Flask Application", ["- app : Flask", "- config"],
         ["+ route handlers", "+ register_blueprint(api)"]),
        (1210, 360, "«module» api.security", [],
         ["validate_api_key()", "validate_admin_credentials()", "issue_access_token()"]),
    ]
    row3 = [
        (40, 400, "«module» page handlers", [],
         ["home_handler()", "search_handler()", "news_detail_handler()", "site/student/applicant pages"]),
        (470, 400, "ApiBlueprint /api/v1", [],
         ["auth/login", "CRUD /news, /pages, /tabs", "/files, /metrics/main"]),
    ]
    boxes = _draw_class_rows_fill_canvas(
        draw, [row1, row2, row3], title_font=title_font, body_font=body_font
    )

    def center(b):
        return ((b[0] + b[2]) // 2, (b[1] + b[3]) // 2)

    _arrow(draw, center(boxes[5]), center(boxes[0]), dashed=True)
    _arrow(draw, center(boxes[5]), center(boxes[6]), dashed=True)
    _arrow(draw, center(boxes[9]), center(boxes[5]), dashed=True)
    _arrow(draw, center(boxes[7]), center(boxes[1]), dashed=True)
    _arrow(draw, center(boxes[7]), center(boxes[9]), dashed=True)
    _arrow(draw, center(boxes[7]), center(boxes[8]), dashed=True)
    _arrow(draw, center(boxes[8]), center(boxes[5]), dashed=True)
    _arrow(draw, center(boxes[8]), center(boxes[3]), dashed=True)
    _arrow(draw, center(boxes[7]), center(boxes[6]), dashed=True)
    _arrow(draw, center(boxes[3]), center(boxes[6]), dashed=True)
    _arrow(draw, center(boxes[4]), center(boxes[6]), dashed=True)

    _save_filled_canvas(img, out_path)


def render_use_case_diagram(out_path: str) -> None:
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), WHITE)
    draw = ImageDraw.Draw(img)
    font = _find_font(FONT_USE_CASE)
    small = _find_font(FONT_USE_CASE_SMALL)

    sys_x, sys_y = MARGIN + 96, MARGIN
    sys_w = CANVAS_W - sys_x - MARGIN
    sys_h = CANVAS_H - 2 * MARGIN
    draw.rectangle((sys_x, sys_y, sys_x + sys_w, sys_y + sys_h), outline=BLACK, width=LINE_W)

    split_y = sys_y + sys_h // 2
    inner_pad = 16
    web_y = sys_y + inner_pad
    web_h = split_y - web_y - inner_pad
    api_y = split_y + inner_pad
    api_h = sys_y + sys_h - inner_pad - api_y

    draw.rectangle((sys_x + inner_pad, web_y, sys_x + sys_w - inner_pad, web_y + web_h), outline=BLACK, width=LINE_W)
    draw.rectangle((sys_x + inner_pad, api_y, sys_x + sys_w - inner_pad, api_y + api_h), outline=BLACK, width=LINE_W)
    draw.text((sys_x + inner_pad + 8, web_y + 8), "Публичный веб-интерфейс (Flask + Jinja2)", fill=BLACK, font=small)
    draw.text((sys_x + inner_pad + 8, api_y + 8), "REST API администрирования (/api/v1)", fill=BLACK, font=small)

    user_cy = web_y + web_h // 2
    admin_cy = api_y + api_h // 2
    actor_x = MARGIN + 36

    user_top = _draw_actor(draw, actor_x, user_cy, "Пользователь", font)
    admin_top = _draw_actor(draw, actor_x, admin_cy, "Администратор", font)

    def uc(cx, cy, text, w=340, h=108):
        return _draw_use_case(draw, cx, cy, w, h, text, small)

    def web_frac(fy: float) -> int:
        return web_y + int(web_h * fy)

    def api_frac(fy: float) -> int:
        return api_y + int(api_h * fy)

    inner_x = sys_x + inner_pad
    inner_w = sys_w - 2 * inner_pad
    uc_w = max(300, (inner_w - COL_GAP * 3) // 4)
    uc_h = 108

    uc_web: list = []
    for row_frac, labels in (
        (0.2, ["Просмотр\nглавной страницы", "Просмотр\nсписка новостей", "Просмотр\nновости", "Просмотр\nспециальностей"]),
        (0.5, ["Поиск\nинформации", "Просмотр раздела\n«Абитуриенту»", "Просмотр раздела\n«Студенту»", "Переключение\nязыка (ru/be/en)"]),
        (0.8, ["Просмотр служебных\nстраниц"]),
    ):
        cols = len(labels)
        step = inner_w // (cols + 1)
        cy = web_frac(row_frac)
        for i, text in enumerate(labels):
            uc_web.append(uc(inner_x + step * (i + 1), cy, text, w=uc_w, h=uc_h))

    uc_api: list = []
    api_uc_w = max(320, (inner_w - COL_GAP * 2) // 3)
    api_uc_h = 112
    for row_frac, labels in (
        (0.18, ["Авторизация\nадминистратора", "Управление\nновостями", "Загрузка изображений\nновостей"]),
        (0.48, ["Управление\nстраницами", "Управление\nвкладками меню", "Редактирование\nшаблонов"]),
        (0.78, ["Управление файлами\nstatic", "Просмотр метрик\nи статуса"]),
    ):
        cols = len(labels)
        step = inner_w // (cols + 1)
        cy = api_frac(row_frac)
        for i, text in enumerate(labels):
            uc_api.append(uc(inner_x + step * (i + 1), cy, text, w=api_uc_w, h=api_uc_h))

    def link_actor(actor_top_y: int, uc_box: Tuple[int, int, int, int]) -> None:
        cy = (uc_box[1] + uc_box[3]) // 2
        _line(draw, (actor_x + 72, actor_top_y), (uc_box[0], cy))

    for box in uc_web:
        link_actor(user_top[1], box)
    for box in uc_api:
        link_actor(admin_top[1], box)

    a0 = ((uc_api[0][0] + uc_api[0][2]) // 2, (uc_api[0][1] + uc_api[0][3]) // 2)
    a1 = ((uc_api[1][0] + uc_api[1][2]) // 2, uc_api[1][1])
    _arrow(draw, a1, (a0[0], a0[1] + 28), dashed=True)
    tw = draw.textlength("<<включить>>", font=small)
    draw.text(((a0[0] + a1[0]) / 2 - tw / 2, (a0[1] + a1[1]) / 2 - 20), "<<включить>>", fill=BLACK, font=small)

    _save_filled_canvas(img, out_path)


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "diagrams")
    render_database_diagram(os.path.join(out, "appendix_A_database.png"))
    render_class_diagram(os.path.join(out, "appendix_B_classes.png"))
    render_use_case_diagram(os.path.join(out, "appendix_C_use_cases.png"))
    render_database_diagram(os.path.join(out, "uml_database_mainsite.png"))
    render_class_diagram(os.path.join(out, "uml_classes_mainsite.png"))
    render_use_case_diagram(os.path.join(out, "uml_usecases_mainsite.png"))
    print(f"Диаграммы сохранены в: {out}")


if __name__ == "__main__":
    main()
