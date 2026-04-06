/** Дублирует changeLanguage из script.js; подключайте только один вариант переключения языка. */
function changeLanguage(lang) {
    const loader = document.createElement('div');
    loader.className = 'language-loader';
    loader.innerHTML = '<div class="loader-spinner"></div>';
    document.body.appendChild(loader);

    const url = new URL(window.location.href);
    url.searchParams.set('lang', lang);
    window.location.href = url.toString();
}
