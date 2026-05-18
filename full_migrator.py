"""
full_migrator.py — ПОЛНАЯ МИГРАЦИЯ: контент + навигация + бэкенд + файлы
Установка: pip install requests beautifulsoup4 lxml
Запуск: python full_migrator.py
"""
import requests
from bs4 import BeautifulSoup, Tag
import re
import os
from pathlib import Path
import hashlib
from urllib.parse import urljoin
import json
from typing import Optional, Dict, List, Any


class FullSiteMigrator:
    def __init__(self,
                 base_url: str = "http://www.ngaek.by",
                 project_root: str = ".",
                 images_dir: str = "static/images/migrated",
                 pages_dir: str = "templates/migrated"):
        """
        Args:
            base_url: URL старого сайта
            project_root: корень Flask-проекта (где app.py)
            images_dir: куда сохранять картинки (относительно project_root)
            pages_dir: куда сохранять HTML-шаблоны (относительно project_root)
        """
        self.base_url = base_url.rstrip('/')
        self.project_root = Path(project_root)
        self.images_dir = self.project_root / images_dir
        self.pages_dir = self.project_root / pages_dir
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.pages_dir.mkdir(parents=True, exist_ok=True)

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; SiteMigrator/1.0)'
        })

        # Список смигрированных страниц: {slug, title, url, nav_section}
        self.migrated_pages: List[Dict] = []

    # ═══════════════════════════════════════════════
    # ЗАГРУЗКА И ПАРСИНГ
    # ═══════════════════════════════════════════════
    def fetch_page(self, url: str) -> BeautifulSoup:
        """Загружает страницу Joomla"""
        full_url = url if url.startswith('http') else urljoin(self.base_url, url)
        print(f"  📄 Загрузка: {full_url}")
        resp = self.session.get(full_url, timeout=30)
        resp.encoding = 'utf-8'
        return BeautifulSoup(resp.text, 'lxml')

    def extract_title(self, soup: BeautifulSoup) -> str:
        """Извлекает заголовок страницы"""
        selectors = [
            '.entry-title',
            '.page-header h1',
            'h1.entry-title',
            '.item-page h1',
            'h1'
        ]
        for sel in selectors:
            el = soup.select_one(sel)
            if el:
                title = el.get_text(strip=True)
                if len(title) > 5:
                    return title
        return "untitled"

    def extract_breadcrumbs(self, soup: BeautifulSoup) -> List[str]:
        """Извлекает хлебные крошки"""
        crumbs = []
        bread_el = soup.select_one('.breadcrumb')
        if bread_el:
            for li in bread_el.find_all('li'):
                text = li.get_text(strip=True)
                if text and text not in ['/', '›']:
                    crumbs.append(text)
        return crumbs

    def extract_content(self, soup: BeautifulSoup) -> Optional[Tag]:
        """Извлекает контейнер с контентом"""
        selectors = [
            '.entry-content',
            '#sp-component .item-page',
            'article.item-page',
            '.item-page'
        ]
        for sel in selectors:
            content = soup.select_one(sel)
            if content:
                return content
        return None

    # ═══════════════════════════════════════════════
    # РАБОТА С ИЗОБРАЖЕНИЯМИ
    # ═══════════════════════════════════════════════
    def download_image(self, img_url: str) -> str:
        """Скачивает картинку, возвращает новый путь"""
        try:
            if not img_url or img_url.startswith('data:'):
                return img_url

            full_url = urljoin(self.base_url, img_url)

            resp = self.session.get(full_url, stream=True, timeout=30)
            if resp.status_code != 200:
                print(f"    ⚠️ HTTP {resp.status_code}: {img_url[:80]}")
                return img_url

            # Определяем расширение
            ext = img_url.split('.')[-1].split('?')[0].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'webp', 'gif', 'svg']:
                ext = 'jpg'

            # Уникальное имя файла
            content_hash = hashlib.md5(resp.content).hexdigest()[:12]
            filename = f"mig_{content_hash}.{ext}"

            filepath = self.images_dir / filename
            with open(filepath, 'wb') as f:
                f.write(resp.content)

            size_kb = len(resp.content) / 1024
            print(f"    ✅ {filename} ({size_kb:.1f} КБ)")

            return f"/static/images/migrated/{filename}"

        except Exception as e:
            print(f"    ❌ Ошибка: {e}")
            return img_url

    def process_images_in_content(self, content: Tag) -> None:
        """Скачивает все картинки в контенте и заменяет пути"""
        for img in content.find_all('img'):
            src = img.get('src', '')
            if src:
                new_src = self.download_image(src)
                img['src'] = new_src
                img.attrs = {
                    'src': new_src,
                    'alt': img.get('alt', ''),
                    'loading': 'lazy'
                }

    # ═══════════════════════════════════════════════
    # РАБОТА С ФАЙЛАМИ
    # ═══════════════════════════════════════════════
    def check_if_html_page(self, url: str) -> bool:
        """Проверяет, является ли URL HTML-страницей"""
        full_url = url if url.startswith('http') else urljoin(self.base_url, url)
        try:
            resp = self.session.head(full_url, timeout=10, allow_redirects=True)
            content_type = resp.headers.get('content-type', '').lower()
            return 'text/html' in content_type
        except Exception as e:
            print(f"    ⚠️ Ошибка проверки: {e}")
            return False

    def download_file(self, file_url: str, save_path: str = None) -> Optional[str]:
        """
        Скачивает файл (PDF, DOC, JPG и т.д.)

        Args:
            file_url: URL файла на старом сайте
            save_path: путь для сохранения (если None - сгенерирует автоматически)

        Returns:
            новый путь к файлу или None при ошибке
        """
        try:
            full_url = file_url if file_url.startswith('http') else urljoin(self.base_url, file_url)

            # Определяем расширение файла
            ext = file_url.split('.')[-1].split('?')[0].lower()
            if ext not in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', 'jpg', 'png', 'gif']:
                ext = 'file'

            # Генерируем уникальное имя файла
            content_hash = hashlib.md5(full_url.encode()).hexdigest()[:12]
            filename = f"file_{content_hash}.{ext}"

            # Определяем папку для сохранения
            if not save_path:
                if ext in ['pdf', 'doc', 'docx', 'xls', 'xlsx']:
                    file_dir = self.project_root / 'static' / 'documents' / 'migrated'
                elif ext in ['jpg', 'png', 'gif', 'jpeg']:
                    file_dir = self.images_dir
                else:
                    file_dir = self.project_root / 'static' / 'files' / 'migrated'

                file_dir.mkdir(parents=True, exist_ok=True)
                file_path = file_dir / filename
            else:
                file_path = Path(save_path)
                file_path.parent.mkdir(parents=True, exist_ok=True)

            # Скачиваем файл
            resp = self.session.get(full_url, stream=True, timeout=60)
            if resp.status_code != 200:
                print(f"    ⚠️ HTTP {resp.status_code}: {file_url}")
                return None

            # Сохраняем файл
            with open(file_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)

            size_kb = len(resp.content) / 1024
            print(f"    ✅ Файл сохранен: {filename} ({size_kb:.1f} КБ)")

            # Возвращаем относительный путь
            if 'documents' in str(file_path):
                return f"/static/documents/migrated/{filename}"
            elif 'images' in str(file_path):
                return f"/static/images/migrated/{filename}"
            else:
                return f"/static/files/migrated/{filename}"

        except Exception as e:
            print(f"    ❌ Ошибка скачивания файла: {e}")
            return None

    def process_file_links_in_content(self, content: Tag) -> None:
        """Обрабатывает ссылки на файлы в контенте"""
        file_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar']

        for a in content.find_all('a', href=True):
            href = a['href']
            if any(href.lower().endswith(ext) for ext in file_extensions):
                print(f"    📎 Найден файл: {href[:80]}")
                new_path = self.download_file(href)
                if new_path:
                    a['href'] = new_path
                    a['target'] = '_blank'

    # ═══════════════════════════════════════════════
    # ОЧИСТКА КОНТЕНТА
    # ═══════════════════════════════════════════════
    def clean_content(self, content: Tag) -> str:
        """
        Очищает контент от мусора Joomla
        """
        soup = BeautifulSoup(str(content), 'lxml')

        junk_selectors = [
            '#js_csc',
            '.socbuttons',
            '.soc_no',
            '.soc_yes',
            'script',
            'style',
            'noscript'
        ]
        for sel in junk_selectors:
            for junk in soup.select(sel):
                junk.decompose()

        for a in soup.find_all('a'):
            if not a.get_text(strip=True) and not a.find('img'):
                a.decompose()

        for tag in soup.find_all(True):
            allowed = []
            if tag.name == 'a':
                allowed = ['href', 'target', 'title']
            elif tag.name == 'img':
                allowed = ['src', 'alt', 'loading']
            elif tag.name in ['table', 'tr', 'td', 'th', 'tbody', 'thead']:
                allowed = []
            elif tag.name == 'td':
                allowed = ['colspan', 'rowspan']

            attrs_to_keep = {k: v for k, v in tag.attrs.items() if k in allowed}
            tag.attrs = attrs_to_keep

            if 'style' in tag.attrs:
                del tag.attrs['style']
            if 'class' in tag.attrs:
                del tag.attrs['class']
            if 'id' in tag.attrs and tag.name != 'a':
                del tag.attrs['id']

        for table in soup.find_all('table'):
            if not table.get('class'):
                wrapper = soup.new_tag('div')
                wrapper['style'] = 'overflow-x: auto; margin: 24px 0;'
                table.wrap(wrapper)

        return str(soup)

    # ═══════════════════════════════════════════════
    # ГЕНЕРАЦИЯ ШАБЛОНА
    # ═══════════════════════════════════════════════
    def generate_template(self, title: str, breadcrumbs: List[str], content_html: str) -> str:
        """Генерирует Jinja2-шаблон страницы"""

        bread_items = []
        if breadcrumbs:
            for i, crumb in enumerate(breadcrumbs):
                if i == len(breadcrumbs) - 1:
                    bread_items.append(f'<li><span aria-current="page">{crumb}</span></li>')
                else:
                    bread_items.append(f'<li><a href="{{{{ u(\'/\') }}}}">{crumb}</a></li>')

        bread_html = ''
        if bread_items:
            bread_html = f'''
<div class="breadcrumbs-wrap">
    <div class="container">
        <ul class="breadcrumbs">
            {"            ".join(bread_items)}
        </ul>
    </div>
</div>'''

        return f'''{{% extends "base.html" %}}
{{% from 'macros/url.html' import u %}}

{{% block content %}}
{bread_html}

<section class="static-page migrated-page">
    <div class="container static-page-inner">
        <h1 class="static-page-title">{title}</h1>
        
        <div class="static-page-body">
            {content_html}
        </div>
    </div>
</section>
{{% endblock %}}'''

    # ═══════════════════════════════════════════════
    # МИГРАЦИЯ СТРАНИЦЫ
    # ═══════════════════════════════════════════════
    def migrate_page(self, url: str, slug: Optional[str] = None,
                     nav_section: Optional[str] = None) -> Optional[Dict]:
        """
        Мигрирует одну страницу с поддержкой файлов
        """
        print(f"\n{'='*60}")
        print(f"🔄 Миграция: {url}")

        # Проверяем, что это HTML-страница
        if not self.check_if_html_page(url):
            print(f"  ⚠️ URL не является HTML-страницей (возможно файл). Пропускаем.")
            return None

        try:
            soup = self.fetch_page(url)
        except Exception as e:
            print(f"  ❌ Ошибка загрузки: {e}")
            return None

        title = self.extract_title(soup)
        breadcrumbs = self.extract_breadcrumbs(soup)
        content = self.extract_content(soup)

        if not content:
            print(f"  ❌ Контент не найден")
            return None

        print(f"  📝 Заголовок: {title}")
        print(f"  📂 Хлебные крошки: {' → '.join(breadcrumbs) if breadcrumbs else 'нет'}")

        # Обрабатываем ссылки на файлы
        print(f"  📎 Обработка ссылок на файлы...")
        self.process_file_links_in_content(content)

        # Скачиваем картинки
        print(f"  📸 Обработка изображений...")
        self.process_images_in_content(content)

        # Очищаем контент
        clean = self.clean_content(content)

        if not slug:
            slug = self._slugify(title)

        template = self.generate_template(title, breadcrumbs, clean)

        template_path = self.pages_dir / f"{slug}.html"
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template)

        print(f"  💾 Сохранено: {template_path}")

        page_info = {
            'slug': slug,
            'title': title,
            'url': url,
            'nav_section': nav_section,
            'breadcrumbs': breadcrumbs,
            'template_path': str(template_path)
        }
        self.migrated_pages.append(page_info)

        return page_info

    @staticmethod
    def _slugify(text: str) -> str:
        """Генерирует slug из заголовка"""
        translit = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
            'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
            'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
            'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts',
            'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
            'э': 'e', 'ю': 'yu', 'я': 'ya'
        }
        text = text.lower()
        text = ''.join(translit.get(c, c) for c in text)
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text).strip('-')
        return text or 'page'

    # ═══════════════════════════════════════════════
    # ДОБАВЛЕНИЕ МАРШРУТОВ
    # ═══════════════════════════════════════════════
    def add_route_to_app(self, slug: str, page_info: Dict) -> bool:
        """Добавляет маршрут в app.py"""
        app_path = self.project_root / 'app.py'
        if not app_path.exists():
            print(f"  ⚠️ app.py не найден")
            return False

        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if f"@app.route('/pages/{slug}')" in content:
            print(f"  ✅ Маршрут /pages/{slug} уже существует")
            return True

        route_code = f"""
@app.route('/pages/{slug}')
def page_{slug}():
    return render_template('migrated/{slug}.html')
"""
        insert_pos = content.find("if __name__ == '__main__':")
        if insert_pos == -1:
            insert_pos = len(content)

        new_content = content[:insert_pos] + route_code + "\n" + content[insert_pos:]

        backup_path = app_path.with_suffix('.py.bak')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)

        with open(app_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  ➕ Маршрут /pages/{slug} добавлен")
        return True

    # ═══════════════════════════════════════════════
    # СОХРАНЕНИЕ ОТЧЕТА
    # ═══════════════════════════════════════════════
    def save_report(self):
        """Сохраняет отчет о миграции"""
        report = {
            'base_url': self.base_url,
            'total_pages': len(self.migrated_pages),
            'pages': self.migrated_pages
        }

        report_path = self.pages_dir / 'migration_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n{'='*60}")
        print(f"📊 Отчет сохранен: {report_path}")
        print(f"📄 Всего страниц: {len(self.migrated_pages)}")

        print(f"\n{'Слаг':<30} {'Заголовок':<40}")
        print("-" * 70)
        for p in self.migrated_pages:
            print(f"{p['slug']:<30} {p['title'][:38]:<40}")


# ═══════════════════════════════════════════════
# ЗАПУСК
# ═══════════════════════════════════════════════
if __name__ == '__main__':

    PROJECT_ROOT = "."

    PAGES_TO_MIGRATE = [
        # КОНТАКТЫ И СЕТЕВАЯ ФОРМА
        {
            "url": "/index.php/ru/kabinet-proforientatsii",
            "slug": "kabinet-proforientatsii",
            "title": "Кабинет профориентации"
        },
        {
            "url": "/index.php/ru/kontakty",
            "slug": "kontakty",
            "title": "Контакты"
        },
    ]

    migrator = FullSiteMigrator(
        base_url="http://www.ngaek.by",
        project_root=PROJECT_ROOT,
        images_dir="static/images/migrated",
        pages_dir="templates/migrated"
    )

    for page_config in PAGES_TO_MIGRATE:
        result = migrator.migrate_page(
            url=page_config["url"],
            slug=page_config.get("slug"),
            nav_section=page_config.get("nav_section")
        )

        if result:
            migrator.add_route_to_app(result['slug'], result)

    migrator.save_report()

    print("\n✅ Миграция завершена!")
    print(f"📁 Шаблоны: templates/migrated/")
    print(f"🖼️ Картинки: static/images/migrated/")
    print(f"📎 Документы: static/documents/migrated/")