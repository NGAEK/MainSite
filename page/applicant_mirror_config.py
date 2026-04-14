"""Раздел «Абитуриентам»: пути на ngaek.by (после /index.php/ru/)."""

# Читаемые slug в URL нашего сайта -> путь на старом Joomla
APPLICANT_SOURCE_PATHS: dict[str, str] = {
    "spetsialnosti": "2013-01-31-07-20-51/spetsialnosti",
    "kontrolnye-tsifry-priema": "2013-01-31-07-20-51/ygfcyjgvhj",
    "tselevaya-podgotovka": "2013-01-31-07-20-51/2019-07-08-21-41-01",
    "prokhodnye-bally": "2013-01-31-07-20-51/svodnaya-tablitsa-rezultatov-vstupitelnoj-kompanii",
    "stoimost-obucheniya": "2013-01-31-07-20-51/stoimost-obucheniya",
    "sroki-vstupitelnoj-kampanii": "2013-01-31-07-20-51/sroki-priema-dokumentov",
    "dokumenty-dlya-postupleniya": "2013-01-31-07-20-51/dokumenty-neobkhodimye-dlya-postupleniya",
    "normativnye-pravovye-dokumenty": "2013-01-31-07-20-51/normativnye-pravovye-dokumenty",
    "chasto-zadavaemye-voprosy": "2013-01-31-07-20-51/chasto-zadavaemye-voprosy",
    "goryachaya-liniya": "2013-01-31-07-20-51/goryachaya-liniya",
    "konsultatsionnyj-punkt": "2013-01-31-07-20-51/konsultatsionnyj-punkt-dlya-abiturientov",
    "trudoustrojstvo": "2013-01-31-07-20-51/trudoustrojstvo",
    "obshchezhitie": "2013-01-31-07-20-51/2023-02-05-21-24-57",
    "organizatsiya-pitaniya": "2013-01-31-07-20-51/organizatsiya-pitaniya-uchashchikhsya",
}

APPLICANT_SLUGS = frozenset(APPLICANT_SOURCE_PATHS.keys())
