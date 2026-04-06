"""One-off: add EN to messages.json (setdefault from RU + UI overrides). Run: python tools/fill_messages_en.py"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
p = ROOT / "static" / "locales" / "messages.json"
data = json.loads(p.read_text(encoding="utf-8"))


def walk(o):
    if isinstance(o, dict):
        if "RU" in o and "BY" in o:
            o.setdefault("EN", o["RU"])
        else:
            for v in o.values():
                walk(v)
    elif isinstance(o, list):
        for i in o:
            walk(i)


walk(data)
data["header"]["lang_en_aria"] = {"RU": "Английский язык", "BY": "Ангельская мова", "EN": "English"}

def set_en(cur, path, en_val):
    for k in path[:-1]:
        cur = cur[k]
    cur[path[-1]]["EN"] = en_val


set_en(data, ["404"], "Page not found")
for k, en in [
    ("site_title", "Novopolsky State Agrarian and Economic College"),
    ("logo_alt", "College logo"),
    ("partner_alt", "Partner"),
]:
    data["common"][k]["EN"] = en

header_map = {
    "title": "Novopolsky State Agrarian and Economic College",
    "subtitle": "Secondary specialized education institution",
    "search_placeholder": "Search news...",
    "search_aria": "Search news",
    "search_btn_aria": "Search",
    "lang_be_aria": "Belarusian",
    "lang_ru_aria": "Russian",
    "accessibility_aria": "Accessibility settings",
    "theme_aria": "Toggle theme",
}
for k, v in header_map.items():
    data["header"][k]["EN"] = v

nav_map = {
    "home": "Home",
    "about_college": "About the college",
    "history": "History",
    "administration": "Administration",
    "documents": "Documents",
    "vacancies": "Vacancies",
    "enrollee": "Applicants",
    "specialties": "Specialties",
    "admission_rules": "Admission rules",
    "open_doors": "Open day",
    "faq": "Q&A",
    "study": "Studies",
    "schedule": "Schedule",
    "e_learning": "E-learning",
    "library": "Library",
    "practice": "Internship",
    "news": "News",
    "gallery": "Gallery",
    "contacts": "Contacts",
}
for k, v in nav_map.items():
    data["nav"][k]["EN"] = v

news_block = {
    "title": "News",
    "search_results": "Search results",
    "found_count": "found",
    "prev_aria": "Previous news",
    "next_aria": "Next news",
    "back_to_news": "Back to all news",
    "read_more": "Read more",
    "no_results_title": "Nothing found",
    "no_results_text": "no news matched your query.",
    "show_all": "Show all news",
}
for k, v in news_block.items():
    data["news"][k]["EN"] = v

search_block = {
    "results_title": "Search results",
    "back_home": "Back to home",
    "found_news": "News found",
    "read_more": "Read more",
    "no_results_title": "Nothing found",
    "no_results_text": "no news matched your query.",
    "show_all_news": "Show all news",
    "news_alt": "News item",
}
for k, v in search_block.items():
    data["search"][k]["EN"] = v

errors_block = {
    "page_not_found": "Page not found",
    "page_not_found_text": "Sorry, the page does not exist.",
    "back_home": "Back to home",
}
for k, v in errors_block.items():
    data["errors"][k]["EN"] = v

news_detail_block = {"back_to_list": "Back to news list", "gallery_alt": "Gallery image"}
for k, v in news_detail_block.items():
    data["news_detail"][k]["EN"] = v

footer_en = {
    "about_college": "About the college",
    "enrollee": "Applicants",
    "student": "Students",
    "contacts": "Contacts",
    "history": "History",
    "administration": "Administration",
    "documents": "Documents",
    "vacancies": "Vacancies",
    "photo_gallery": "Photo gallery",
    "specialties": "Specialties",
    "admission_rules": "Admission rules",
    "open_doors": "Open day",
    "prep_courses": "Preparatory courses",
    "faq": "Q&A",
    "schedule": "Schedule",
    "e_learning": "E-learning",
    "library": "Library",
    "student_council": "Student council",
    "sport_sections": "Sports clubs",
    "address": "Minsk, Sverdlova st., 15",
    "work_hours": "Mon–Fri: 8:30 – 17:30",
    "copyright": "Novopolsky State Agrarian and Economic College. All rights reserved.",
}
for k, v in footer_en.items():
    data["footer"][k]["EN"] = v

acc = {
    "title": "Accessibility settings",
    "high_contrast": "High contrast",
    "large_text": "Large text",
    "dark_mode": "Dark mode",
    "reset": "Reset",
    "save": "Save",
}
for k, v in acc.items():
    data["accessibility"][k]["EN"] = v

hero_en = {
    "slide1_title": "Vocational education — a path to success",
    "slide1_subtitle": "Gain an in-demand profession",
    "slide1_alt": "Main college building",
    "slide2_title": "Modern training labs",
    "slide2_subtitle": "Equipped to current standards",
    "slide2_alt": "Training laboratories",
    "slide3_title": "Active student life",
    "slide3_subtitle": "Sports, creativity, and self-development",
    "slide3_alt": "Sports events",
    "prev_aria": "Previous slide",
    "next_aria": "Next slide",
}
for k, v in hero_en.items():
    data["hero"][k]["EN"] = v

spec_t = {
    "title": "Our specialties",
    "duration_years": "years",
    "duration_months": "mo.",
    "po_title": "Software for information technology",
    "po_duration": "3 years 10 mo.",
    "po_qualification": "Software technician",
    "po_description": "Training in development, testing, and maintenance of software.",
    "byx_title": "Accounting, analysis and control",
    "byx_duration": "2 years 10 mo.",
    "byx_qualification": "Accountant",
    "byx_description": "Training in accounting and financial analysis.",
    "ogu_title": "Hotel services organization",
    "ogu_duration": "2 years 10 mo.",
    "ogu_qualification": "Hotel services specialist",
    "ogu_description": "Training in organizing hotel services.",
    "do_title": "Documentation support for management",
    "do_duration": "2 years 10 mo.",
    "do_qualification": "Secretary",
    "do_description": "Training in documentation support.",
    "soc_rab_title": "Social work",
    "soc_rab_duration": "2 years 10 mo.",
    "soc_rab_qualification": "Social worker",
    "soc_rab_description": "Training in social work.",
    "accounting_title": "Accounting, analysis and control",
    "hotel_title": "Hotel services organization",
    "documentation_title": "Records management",
    "social_work_title": "Social work",
    "software_title": "Software and information technology",
}
for k, v in spec_t.items():
    data["specialties"][k]["EN"] = v

gallery_en = {
    "title": "Gallery",
    "slide1_caption": "Main college building",
    "slide2_caption": "Training laboratories",
    "slide3_caption": "Sports events",
    "slide4_caption": "Creative performances",
    "photo_alt": "College photo",
}
for k, v in gallery_en.items():
    data["gallery"][k]["EN"] = v

teachers_en = {
    "title": "Our administration",
    "admin_alt": "Administrator",
    "director_name": "Trus Nikolai Nikolaevich",
    "director_position": "College director",
    "deputy_edu_name": "Krumkach Tamara Nikolaevna",
    "deputy_edu_position": "Deputy director for academic affairs",
    "deputy_vosp_name": "Begun Lolita Mikhailovna",
    "deputy_vosp_position": "Deputy director for student affairs",
    "deputy_other_name": "Tereshko Svetlana Leonidovna",
    "deputy_other_position": "Deputy director",
}
for k, v in teachers_en.items():
    data["teachers"][k]["EN"] = v

ach_en = {
    "title": "Our achievements",
    "wins": "Wins in skills competitions",
    "employment": "Graduate employment",
    "teachers_count": "Qualified teaching staff",
    "years_work": "Years of successful work",
}
for k, v in ach_en.items():
    data["achievements"][k]["EN"] = v

contact_en = {
    "title": "Contacts",
    "address_title": "Address",
    "address_value": "220005, Minsk, Sverdlova st., 15",
    "phones_title": "Phones",
    "phone_reception": "Reception: +375 (17) 123-45-67",
    "phone_admission": "Admission office: +375 (17) 123-45-68",
    "email_title": "Email",
    "schedule_title": "Opening hours",
    "schedule_week": "Mon–Fri: 8:30 – 17:30",
    "schedule_sat": "Sat: 9:00 – 14:00",
    "schedule_sun": "Sun: closed",
    "feedback_title": "Feedback",
    "your_name": "Your name",
    "topic": "Subject",
    "message": "Message",
    "send": "Send message",
}
for k, v in contact_en.items():
    data["contact"][k]["EN"] = v

p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("Wrote", p)
