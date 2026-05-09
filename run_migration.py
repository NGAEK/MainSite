"""
run_migration.py — запуск миграции с прогресс-баром
"""
import sys
import time
from full_migrator import FullSiteMigrator


def print_progress_bar(current, total, prefix='', suffix='', length=50):
    """Красивый прогресс-бар в терминале"""
    percent = int(100 * (current / total))
    filled = int(length * current / total)
    bar = '█' * filled + '░' * (length - filled)

    # Цвета
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    if percent < 30:
        color = '\033[91m'  # Красный
    elif percent < 70:
        color = YELLOW
    else:
        color = GREEN

    sys.stdout.write(f'\r{prefix} |{color}{bar}{RESET}| {percent}% {suffix}')
    sys.stdout.flush()


def print_header(text):
    """Красивый заголовок"""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}")


def print_result(success, total, time_elapsed):
    """Итоговая статистика"""
    print(f"\n{'=' * 60}")
    print(f"  📊 РЕЗУЛЬТАТЫ МИГРАЦИИ")
    print(f"{'=' * 60}")
    print(f"  ✅ Успешно:     {success}/{total}")
    print(f"  ❌ С ошибками:  {total - success}/{total}")
    print(f"  ⏱️  Время:       {time_elapsed:.1f} сек")
    print(f"  📁 Шаблоны:     templates/migrated/")
    print(f"  🖼️  Картинки:    static/images/migrated/")
    print(f"{'=' * 60}\n")


# ═══════════════════════════════════════════════
# НАСТРОЙКИ
# ═══════════════════════════════════════════════
PAGES_TO_MIGRATE = [
    {"url": "/index.php/ru/course/stranitsy-istorii", "slug": "stranitsy-istorii", "name": "Страницы истории"},
    {"url": "/index.php/ru/course/traditsii-kolledzha", "slug": "traditsii-kolledzha", "name": "Традиции колледжа"},
    {"url": "/index.php/ru/course/nashi-dostizheniya", "slug": "nashi-dostizheniya", "name": "Наши достижения"},
    {"url": "/index.php/ru/course/istoriya", "slug": "istoriya", "name": "История"},
    {"url": "/index.php/ru/course/znamenitye-vypuskniki", "slug": "znamenitye-vypuskniki",
     "name": "Знаменитые выпускники"},
    {"url": "/index.php/ru/course/nashi-tsel-i-zadachi", "slug": "nashi-tsel-i-zadachi", "name": "Наши цель и задачи"},
    {"url": "/index.php/ru/course/antikorruptsionnaya-deyatelnost", "slug": "antikorruptsionnaya-deyatelnost",
     "name": "Антикоррупционная деятельность"},
    {"url": "/index.php/ru/course/polozhenie-o-politike-v-otnoshenii-obrabotki-cookie",
     "slug": "polozhenie-o-politike-cookie", "name": "Политика cookie"},
]

# ═══════════════════════════════════════════════
# ЗАПУСК
# ═══════════════════════════════════════════════
print_header("🚀 ЗАПУСК МИГРАЦИИ КОНТЕНТА")

migrator = FullSiteMigrator(
    base_url="http://www.ngaek.by",
    project_root=".",
    images_dir="static/images/migrated",
    pages_dir="templates/migrated"
)

total = len(PAGES_TO_MIGRATE)
success = 0
failed_pages = []
start_time = time.time()

# Начальный прогресс
print_progress_bar(0, total, prefix='Прогресс:', suffix='Начинаем...')

for i, page in enumerate(PAGES_TO_MIGRATE):
    # Обновляем прогресс-бар
    print_progress_bar(i, total, prefix='Прогресс:', suffix=f'Миграция: {page["name"]}')

    try:
        result = migrator.migrate_page(
            url=page["url"],
            slug=page["slug"]
        )

        if result:
            success += 1
        else:
            failed_pages.append(page)

    except Exception as e:
        print(f"\n  ❌ Ошибка в {page['name']}: {e}")
        failed_pages.append(page)

    # Небольшая пауза чтобы не нагружать сервер
    time.sleep(0.5)

# Финальный прогресс-бар
print_progress_bar(total, total, prefix='Прогресс:', suffix='Завершено!')

# Сохраняем отчет
migrator.save_report()

# Время выполнения
elapsed = time.time() - start_time

# Выводим результаты
print_result(success, total, elapsed)

# Если были ошибки — показываем
if failed_pages:
    print("  ⚠️  НЕ УДАЛОСЬ МИГРИРОВАТЬ:")
    for fp in failed_pages:
        print(f"     - {fp['name']} ({fp['url']})")
    print()

print("  📝 ДАЛЬНЕЙШИЕ ШАГИ:")
print("     1. Проверьте шаблоны: templates/migrated/")
print("     2. Проверьте картинки: static/images/migrated/")
print("     3. Добавьте ссылки в header.html")
print("     4. Обновите страницу в браузере\n")

# Звуковой сигнал (опционально)
print('\a')  # Звуковой сигнал о завершении