"""
Соответствие путей в messages.json (например applicants.pages.dokumenty_postupleniya)
реальным URL сайта — по тем же маршрутам, что в header.html / footer.
"""
from __future__ import annotations

# --- applicants.pages.* → /applicants/<slug> (кроме специальности → /specialties) ---
_APPLICANTS_PAGE_SLUG: dict[str, str] = {
    "spetsialnosti": "/specialties",
    "kontrolnye_tsifry": "kontrolnye-tsifry-priema",
    "tselevaya_podgotovka": "tselevaya-podgotovka",
    "prokhodnye_bally": "prokhodnye-bally",
    "stoimost_obucheniya": "stoimost-obucheniya",
    "sroki_kampanii": "sroki-vstupitelnoj-kampanii",
    "dokumenty_postupleniya": "dokumenty-dlya-postupleniya",
    "normativnye_dokumenty": "normativnye-pravovye-dokumenty",
    "chasto_voprosy": "chasto-zadavaemye-voprosy",
    "goryachaya_liniya": "goryachaya-liniya",
    "konsultatsionnyj_punkt": "konsultatsionnyj-punkt",
    "trudoustrojstvo": "trudoustrojstvo",
    "obshchezhitie": "obshchezhitie",
    "organizatsiya_pitaniya": "organizatsiya-pitaniya",
}

# --- students.pages.* → /students/<slug> ---
_STUDENTS_PAGE_SLUG: dict[str, str] = {
    "grafik_uchebnogo_protsessa": "grafik-uchebnogo-protsessa",
    "proizvodstvennoe_obuchenie": "proizvodstvennoe-obuchenie",
    "grafik_praktik": "grafik-prokhozhdeniya-uchebnykh-i-proizvodstvennykh-praktik",
    "pamyatka_uchashchemusya": "pamyatka-uchashchemusya",
    "obraztsy_dokumentov": "obraztsy-dokumentov",
    "kursovoe_diplomnoe": "kursovoe-i-diplomnoe-proektirovanie",
    "normativnye_dokumenty": "normativnye-dokumenty",
    "raspredelenie_vypusknikov": "raspredelenie-i-trudoustrojstvo-vypusknikov",
    "programma_preddiplomnoj_praktiki": "uchebnaya-programma-preddiplomnoj-praktiki",
    "grafik_zaochnogo": "grafik-uchebnogo-protsessa-zaochnogo-otdeleniya",
    "stoimost_obucheniya": "stoimost-obucheniya",
    "vypusknikam": "vypusknikam",
    "informatsiya_eksternat": (
        "informatsiya-dlya-uchashchikhsya-prekrativshim-dosrochno-obrazovatelnye-otnosheniya-"
        "i-prokhodivshim-attestatsiyu-v-poryadke-eksternata"
    ),
}

# --- nav.* (подписи меню) → URL ---
_NAV_ROUTES: dict[str, tuple[str, str]] = {
    "home": ("/", ""),
    "news": ("/news", ""),
    "specialties": ("/specialties", ""),
    "documents": ("/applicants/dokumenty-dlya-postupleniya", ""),
    "admission_documents": ("/applicants/dokumenty-dlya-postupleniya", ""),
    "admission_quotas": ("/applicants/kontrolnye-tsifry-priema", ""),
    "passing_scores": ("/applicants/prokhodnye-bally", ""),
    "tuition_fees": ("/applicants/stoimost-obucheniya", ""),
    "students": ("/students", ""),
    "students_section": ("/students", ""),
    "students_production_training": ("/students/proizvodstvennoe-obuchenie", ""),
    "students_practice_schedule": (
        "/students/grafik-prokhozhdeniya-uchebnykh-i-proizvodstvennykh-praktik",
        "",
    ),
    "students_memo": ("/students/pamyatka-uchashchemusya", ""),
    "students_documents_samples": ("/students/obraztsy-dokumentov", ""),
    "enrollee": ("/applicants", ""),
    "enrollee_section": ("/applicants", ""),
    "ideology": ("/pages/ideology", ""),
    "ideology_main": ("/pages/ideology-main", ""),
    "ideology_events": ("/pages/ideology-events", ""),
    "ideology_prevention": ("/pages/ideology-prevention", ""),
    "career_guidance": ("/pages/proforientation", ""),
    "career_video": ("/pages/proforientation-video", ""),
    "career_principles": ("/pages/proforientation-principles", ""),
    "inclusive_education": ("/pages/inclusive-education", ""),
    "inclusive_main": ("/pages/inclusive-main", ""),
    "inclusive_regional_map": ("/pages/inclusive-regional-map", ""),
    "inclusive_for_parents": ("/pages/inclusive-for-parents", ""),
    "one_window": ("/one-window", ""),
    "one_window_procedures": ("/one-window", ""),
    "one_window_management": ("/pages/one-window-management", ""),
    "one_window_citizens_schedule": ("/pages/one-window-citizens-schedule", ""),
    "one_window_acts": ("/pages/one-window-acts", ""),
    "contacts": ("/contacts", ""),
    "network_form": ("/pages/network", ""),
    "network_about": ("/pages/network", ""),
    "network_partners": ("/pages/network", ""),
    "faq": ("/applicants/chasto-zadavaemye-voprosy", ""),
}

# --- footer.* → осмысленные разделы (в футере сейчас href="#", для поиска даём реальные URL) ---
_FOOTER_ROUTES: dict[str, tuple[str, str]] = {
    "about_college": ("/", ""),
    "enrollee": ("/applicants", ""),
    "student": ("/students", ""),
    "contacts": ("/contacts", ""),
    "history": ("/pages/istoriya", ""),
    "administration": ("/", "administration"),
    "documents": ("/applicants/dokumenty-dlya-postupleniya", ""),
    "vacancies": ("/", ""),
    "photo_gallery": ("/", ""),
    "specialties": ("/specialties", ""),
    "admission_rules": ("/applicants/normativnye-pravovye-dokumenty", ""),
    "open_doors": ("/applicants", ""),
    "prep_courses": ("/applicants", ""),
    "faq": ("/applicants/chasto-zadavaemye-voprosy", ""),
    "schedule": ("/students/grafik-uchebnogo-protsessa", ""),
    "e_learning": ("/students", ""),
    "library": ("/students", ""),
    "student_council": ("/students", ""),
    "sport_sections": ("/students", ""),
    "address": ("/", "contact"),
    "work_hours": ("/", "contact"),
    "copyright": ("/", ""),
    "legal_links_title": ("/privacy", ""),
    "link_privacy": ("/privacy", ""),
    "link_one_window": ("/one-window", ""),
    "link_sitemap": ("/sitemap", ""),
    "link_admin_site": ("/", ""),
    "link_cookies": ("/cookies", ""),
}

# Корневой ключ → (path, fragment) если нет более точного правила
_ROOT_FALLBACK: dict[str, tuple[str, str]] = {
    "teachers": ("/", "administration"),
    "contact": ("/", "contact"),
    "achievements": ("/", ""),
    "gallery": ("/", ""),
    "hero": ("/", ""),
    "specialties": ("/specialties", ""),
    "students": ("/students", ""),
    "applicants": ("/applicants", ""),
    "footer": ("/", ""),
    "header": ("/", ""),
    "nav": ("/", ""),
    "common": ("/", ""),
    "cookies": ("/cookies", ""),
    "404": ("/", ""),
    "errors": ("/", ""),
    "accessibility": ("/", ""),
    "breadcrumbs": ("/", ""),
    "news": ("/news", ""),
    "search": ("/search", ""),
    "news_detail": ("/news", ""),
    "legal": ("/privacy", ""),
}


def resolve_locale_key_path(key_path: str) -> tuple[str, str]:
    """
    По ключу вида applicants.pages.dokumenty_postupleniya возвращает (url_path, fragment).
    url_path начинается с / и готов к href_with_lang.
    """
    parts = key_path.split(".")
    if not parts:
        return ("/", "")

    root = parts[0]

    if root == "applicants" and len(parts) == 2:
        return ("/applicants", "")
    if root == "students" and len(parts) == 2:
        return ("/students", "")

    if root == "applicants" and len(parts) >= 3 and parts[1] == "pages":
        page_key = parts[2]
        target = _APPLICANTS_PAGE_SLUG.get(page_key)
        if target:
            if target.startswith("/"):
                return (target, "")
            return (f"/applicants/{target}", "")

    if root == "students" and len(parts) >= 3 and parts[1] == "pages":
        page_key = parts[2]
        slug = _STUDENTS_PAGE_SLUG.get(page_key)
        if slug:
            return (f"/students/{slug}", "")

    if root == "nav" and len(parts) >= 2:
        sub = parts[1]
        hit = _NAV_ROUTES.get(sub)
        if hit:
            return hit

    if root == "footer" and len(parts) >= 2:
        hit = _FOOTER_ROUTES.get(parts[1])
        if hit:
            return hit

    if root == "pages" and len(parts) > 1:
        tail = ".".join(parts[1:]).lower()
        if "contact" in tail:
            return ("/contacts", "")
        if "privacy" in tail:
            return ("/privacy", "")
        if "cookie" in tail:
            return ("/cookies", "")
        if "specialt" in tail or "spec" in tail:
            return ("/specialties", "")
        if "sitemap" in tail:
            return ("/sitemap", "")
        if "one_window" in tail or "one-window" in tail:
            return ("/one-window", "")
        return ("/", "")

    return _ROOT_FALLBACK.get(root, ("/", ""))
