"""Дополняет messages.json ключами nav, accessibility (панель), js."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
p = ROOT / "static" / "locales" / "messages.json"
data = json.loads(p.read_text(encoding="utf-8"))

nav_add = {
    "history_pages": ("Страницы истории", "Старонкі гісторыі", "History pages"),
    "college_traditions": ("Традиции колледжа", "Традыцыі каледжа", "College traditions"),
    "our_achievements": ("Наши достижения", "Нашы дасягненні", "Our achievements"),
    "license_external": ("Лицензия ↗", "Ліцэнзія ↗", "License ↗"),
    "college_history": ("История колледжа", "Гісторыя каледжа", "College history"),
    "famous_graduates": ("Знаменитые выпускники", "Вядомыя выпускнікі", "Famous graduates"),
    "goals_and_tasks": ("Наши цель и задачи", "Нашы мэта і задачы", "Goals and objectives"),
    "press_about_us": ("Про нас говорят и пишут ↗", "Пра нас гавораць і пішуць ↗", "Press about us ↗"),
    "anticorruption": ("Антикоррупционная деятельность", "Антыкарупцыйная дзейнасць", "Anti-corruption"),
    "cookie_policy_nav": (
        "Положение о политике в отношении обработки cookie",
        "Палажэнне аб палітыцы ў дачыненні да апрацоўкі cookie",
        "Cookie processing policy",
    ),
    "edu_group_informatization": ("Информатизация", "Інфарматызацыя", "Informatization"),
    "edu_informatization": ("Информатизация", "Інфарматызацыя", "Informatization"),
    "edu_group_methodical": ("Методическая работа", "Метадычная работа", "Methodical work"),
    "edu_methodical_work": ("Методическая работа", "Метадычная работа", "Methodical work"),
    "edu_teaching_materials": (
        "Учебно-методические материалы",
        "Вучэбна-метадычныя матэрыялы",
        "Teaching materials",
    ),
    "edu_teacher_rules": (
        "Правила педагогических работников",
        "Правілы педагагічных работнікаў",
        "Rules for teaching staff",
    ),
    "edu_cycle_commissions": ("Цикловые комиссии", "Цыклавыя камісіі", "Cycle commissions"),
    "edu_qualification_plan": (
        "План повышения квалификации руководящих работников и специалистов",
        "План павышэння кваліфікацыі кіраўнікоў і спецыялістаў",
        "Staff qualification development plan",
    ),
    "edu_pedagogical_council_plan": (
        "План работы педагогического совета",
        "План работы педагагічнага савета",
        "Pedagogical council work plan",
    ),
    "edu_professional_development": ("Повышение квалификации", "Павышэнне кваліфікацыі", "Professional development"),
    "edu_legal_acts": ("Нормативно правовые акты", "Нарматыўна прававыя акты", "Legal acts"),
    "edu_group_adult": ("Дополнительное образование", "Дадатковая адукацыя", "Adult education"),
    "edu_adult_education": (
        "Дополнительное образование взрослых",
        "Дадатковая адукацыя дарослых",
        "Adult education",
    ),
    "edu_group_innovation": ("Инновационная деятельность", "Інавацыйная дзейнасць", "Innovation"),
    "edu_innovative_activity": (
        "Экспериментальная и инновационная деятельность",
        "Эксперыментальная і інавацыйная дзейнасць",
        "Experimental and innovative activity",
    ),
    "college_structure": ("Структура колледжа", "Структура каледжа", "College structure"),
    "site_map_nav": ("Карта сайта", "Карта сайта", "Site map"),
    "social_protection_phones": (
        "Справочник телефонов служб социальной защиты детей",
        "Даведнік тэлефонаў службаў сацыяльнай аховы дзяцей",
        "Child social protection phone directory",
    ),
    "interactive_map": ("Интерактивная карта", "Інтэрактыўная карта", "Interactive map"),
    "rating_portal_external": ("Портал рейтинговой оценки ↗", "Портал рэйтынгавай ацэнкі ↗", "Rating portal ↗"),
    "reference_phones": ("Телефоны справочных служб", "Тэлефоны даведачных службаў", "Directory service phones"),
}


def _tri(ru, by, en):
    return {"RU": ru, "BY": by, "EN": en}


for k, v in nav_add.items():
    data["nav"][k] = _tri(*v)

data["accessibility"] = {
    "panel_title": _tri("⚙️ Версия для слабовидящих", "⚙️ Версія для слабавідзячых", "⚙️ Low vision mode"),
    "close_panel": _tri("Закрыть панель настроек", "Закрыць панэль налад", "Close settings panel"),
    "font_size_label": _tri("Размер текста", "Памер тэксту", "Text size"),
    "font_decrease": _tri("Уменьшить шрифт", "Паменшыць шрыфт", "Decrease font"),
    "font_reset": _tri("Сбросить размер шрифта", "Скінуць памер шрыфту", "Reset font size"),
    "font_increase": _tri("Увеличить шрифт", "Павялічыць шрыфт", "Increase font"),
    "contrast_label": _tri("Цветовая схема и контрастность", "Колеравая схема і кантраснасць", "Color scheme and contrast"),
    "contrast_normal": _tri("Обычный", "Звычайны", "Normal"),
    "contrast_bw": _tri("Ч/Б", "Ч/Б", "B&W"),
    "contrast_yellow": _tri("◑ Жёлтый", "◑ Жоўты", "◑ Yellow"),
    "contrast_white": _tri("◑ Белый", "◑ Белы", "◑ White"),
    "contrast_blue": _tri("◑ Синий", "◑ Сіні", "◑ Blue"),
    "font_family_label": _tri("Гарнитура шрифта", "Гарнітура шрыфту", "Font family"),
    "font_default": _tri("Исходный", "Зыходны", "Default"),
    "other_label": _tri("Дополнительные параметры", "Дадатковыя параметры", "Additional options"),
    "hide_images": _tri("Скрыть изображения", "Схаваць выявы", "Hide images"),
    "hide_images_desc": _tri("Убирает все картинки", "Прыбірае ўсе выявы", "Removes all images"),
    "simplify": _tri("Упростить структуру", "Спростыць структуру", "Simplify layout"),
    "simplify_desc": _tri("Скрывает слайдеры и декор", "Хавае слайдеры і дэкор", "Hides sliders and decoration"),
    "keyboard_focus": _tri("Фокус-рамки", "Фокус-рамкі", "Focus outlines"),
    "keyboard_focus_desc": _tri(
        "Яркие рамки при Tab‑навигации", "Яркія рамкі пры Tab-навігацыі", "Bright outlines on Tab navigation"
    ),
    "line_height": _tri("Увеличить интерлиньяж", "Павялічыць міжрадковы інтэрвал", "Increase line spacing"),
    "line_height_desc": _tri(
        "Больший промежуток между строк", "Большы прамежак паміж радкамі", "More space between lines"
    ),
    "reset_all": _tri("Сбросить все настройки", "Скінуць усе налады", "Reset all settings"),
    "status_bar_label": _tri("Активные режимы доступности", "Актыўныя рэжымы даступнасці", "Active accessibility modes"),
    "status_bar_prefix": _tri("👁 Версия для слабовидящих:", "👁 Версія для слабавідзячых:", "👁 Low vision mode:"),
    "status_open_settings": _tri("Настройки ▲", "Налады ▲", "Settings ▲"),
    "status_text_scale": _tri("Текст:", "Тэкст:", "Text:"),
    "status_bw": _tri("Ч/Б", "Ч/Б", "B&W"),
    "status_black_yellow": _tri("Жёлтый контраст", "Жоўты кантраст", "Yellow contrast"),
    "status_black_white": _tri("Белый контраст", "Белы кантраст", "White contrast"),
    "status_dark_blue": _tri("Синий контраст", "Сіні кантраст", "Blue contrast"),
    "status_no_images": _tri("Без картинок", "Без выяў", "No images"),
    "status_simplified": _tri("Упрощённый вид", "Спрошаны выгляд", "Simplified view"),
    "status_keyboard": _tri("Яркий фокус", "Яркі фокус", "Strong focus"),
    "status_line_height": _tri("Увеличен интерлиньяж", "Павялічаны інтэрвал", "Increased line spacing"),
    "status_font_arial": _tri("Шрифт: Arial", "Шрыфт: Arial", "Font: Arial"),
    "status_font_verdana": _tri("Шрифт: Verdana", "Шрыфт: Verdana", "Font: Verdana"),
    "status_font_times": _tri("Шрифт: Times", "Шрыфт: Times", "Font: Times"),
}

data["js"] = {
    "close_menu": _tri("Закрыть меню", "Закрыць меню", "Close menu"),
    "clear_search": _tri("Очистить поиск", "Ачысціць пошук", "Clear search"),
}

if "phone_sample" not in data.get("teachers", {}):
    data["teachers"]["phone_sample"] = _tri(
        "+375-29-123-45-67", "+375-29-123-45-67", "+375-29-123-45-67"
    )

p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("Patched messages.json")
