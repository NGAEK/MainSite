"""Соответствие slug страницы «Учащимся» и пути на ngaek.by (после /index.php/ru/)."""

STUDENT_SOURCE_PATHS: dict[str, str] = {
    "grafik-uchebnogo-protsessa": "shortcode/dnevnoe-otdelenie/grafik-uchebnogo-protsessa",
    "proizvodstvennoe-obuchenie": "shortcode/dnevnoe-otdelenie/proizvodstvennoe-obuchenie",
    "grafik-prokhozhdeniya-uchebnykh-i-proizvodstvennykh-praktik": (
        "shortcode/dnevnoe-otdelenie/proizvodstvennoe-obuchenie/"
        "grafik-prokhozhdeniya-uchebnykh-i-proizvodstvennykh-praktik"
    ),
    "pamyatka-uchashchemusya": (
        "shortcode/dnevnoe-otdelenie/proizvodstvennoe-obuchenie/pamyatka-uchashchemusya"
    ),
    "obraztsy-dokumentov": "shortcode/dnevnoe-otdelenie/proizvodstvennoe-obuchenie/obraztsy-dokumentov",
    "kursovoe-i-diplomnoe-proektirovanie": "shortcode/dnevnoe-otdelenie/kursovoe-i-diplomnoe-proektirovanie",
    "normativnye-dokumenty": "shortcode/dnevnoe-otdelenie/normativnye-dokumenty",
    "raspredelenie-i-trudoustrojstvo-vypusknikov": (
        "shortcode/dnevnoe-otdelenie/raspredelenie-i-trudoustrojstvo-vypusknikov"
    ),
    "uchebnaya-programma-preddiplomnoj-praktiki": (
        "shortcode/zaochnoe-otdelenie/uchebnaya-programma-preddiplomnoj-praktiki"
    ),
    "grafik-uchebnogo-protsessa-zaochnogo-otdeleniya": (
        "shortcode/zaochnoe-otdelenie/grafik-uchebnogo-protsessa-zaochnogo-otdeleniya"
    ),
    "stoimost-obucheniya": "shortcode/stoimost-obucheniya",
    "vypusknikam": "shortcode/vypusknikam",
    "informatsiya-dlya-uchashchikhsya-prekrativshim-dosrochno-obrazovatelnye-otnosheniya-i-prokhodivshim-attestatsiyu-v-poryadke-eksternata": (
        "shortcode/informatsiya-dlya-uchashchikhsya-prekrativshim-dosrochno-obrazovatelnye-otnosheniya-"
        "i-prokhodivshim-attestatsiyu-v-poryadke-eksternata"
    ),
}

STUDENT_SLUGS = frozenset(STUDENT_SOURCE_PATHS.keys())
