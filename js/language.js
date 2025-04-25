function changeLanguage(lang) {
    const loader = document.createElement('div');
    loader.className = 'language-loader';
    loader.innerHTML = '<div class="loader-spinner"></div>';
    document.body.appendChild(loader);

    // Сохраняем язык и перезагружаем страницу
    const url = new URL(window.location.href);
    url.searchParams.set('lang', lang);
    window.location.href = url.toString();
}