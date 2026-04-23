const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mainNav = document.getElementById('mainNav');

if (mobileMenuBtn && mainNav) {
    mobileMenuBtn.addEventListener('click', () => {
        mainNav.classList.toggle('active');
        mobileMenuBtn.classList.toggle('active');
    });
}

// Dropdown Menu Handling
const navItems = document.querySelectorAll('.main-nav > li');
navItems.forEach(item => {
    const link = item.querySelector('a');
    if (!link) return;
    link.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
            const hasDropdown = Boolean(item.querySelector('.dropdown-menu'));
            if (!hasDropdown) return;
            e.preventDefault();
            item.classList.toggle('active');
        }
    });
});

// Tab Navigation
const tabBtns = document.querySelectorAll('.tab-btn');
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        const tabId = btn.getAttribute('data-tab');
        document.getElementById(tabId).classList.add('active');
    });
});

// hero-slider
document.addEventListener('DOMContentLoaded', function() {
    const slidesContainer = document.querySelector('.slides-container');
    const slides = document.querySelectorAll('.slid');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    const dots = document.querySelectorAll('.slider-dot');
    let currentIndex = 0;

    if (!slidesContainer || !slides.length || !prevBtn || !nextBtn) return;

    function showSlide(index) {
        slidesContainer.style.transform = `translateX(-${index * 100}%)`;
        dots.forEach((dot, i) => dot.classList.toggle('active', i === index));
    }

    prevBtn.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        showSlide(currentIndex);
    });
    nextBtn.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % slides.length;
        showSlide(currentIndex);
    });
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => { currentIndex = index; showSlide(currentIndex); });
    });
    setInterval(() => { currentIndex = (currentIndex + 1) % slides.length; showSlide(currentIndex); }, 5000);
});

// Gallery Slider
const gallerySlider = document.getElementById('gallerySlider');
const sliderDots = document.querySelectorAll('.slider-dot');
let currentSlide = 0;

if (gallerySlider && sliderDots.length) {
    sliderDots.forEach(dot => {
        dot.addEventListener('click', () => {
            currentSlide = parseInt(dot.getAttribute('data-slide'));
            updateSlider();
        });
    });
    setInterval(() => { currentSlide = (currentSlide + 1) % sliderDots.length; updateSlider(); }, 5000);
    function updateSlider() {
        gallerySlider.scrollTo({ left: currentSlide * gallerySlider.offsetWidth, behavior: 'smooth' });
        sliderDots.forEach((dot, index) => dot.classList.toggle('active', index === currentSlide));
    }
}

// ─── Theme Toggle ───────────────────────────────────────────────
function applyTheme(isDark) {
    document.body.classList.toggle('dark-mode', isDark);
    const toggle = document.getElementById('themeToggle');
    if (toggle) {
        const icon = toggle.querySelector('i');
        if (icon) { icon.classList.toggle('fa-moon', !isDark); icon.classList.toggle('fa-sun', isDark); }
    }
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) darkModeToggle.checked = isDark;
    localStorage.setItem('darkMode', isDark ? 'true' : 'false');
}

const themeToggle = document.getElementById('themeToggle');
const darkModeToggle = document.getElementById('darkModeToggle');

if (themeToggle) {
    themeToggle.addEventListener('click', () => applyTheme(!document.body.classList.contains('dark-mode')));
}
if (darkModeToggle) {
    darkModeToggle.addEventListener('change', () => applyTheme(darkModeToggle.checked));
}

// Accessibility Modal
const accessibilityBtn = document.getElementById('accessibilityBtn');
const accessibilityModal = document.getElementById('accessibilityModal');
const closeModal = document.getElementById('closeModal');
const highContrastToggle = document.getElementById('highContrastToggle');
const largeTextToggle = document.getElementById('largeTextToggle');
const resetAccessibility = document.getElementById('resetAccessibility');
const saveAccessibility = document.getElementById('saveAccessibility');

if (accessibilityBtn && accessibilityModal) {
    accessibilityBtn.addEventListener('click', () => { accessibilityModal.style.display = 'flex'; });
}
if (closeModal && accessibilityModal) {
    closeModal.addEventListener('click', () => { accessibilityModal.style.display = 'none'; });
}
if (highContrastToggle) {
    highContrastToggle.addEventListener('change', () => {
        document.body.classList.toggle('high-contrast', highContrastToggle.checked);
        localStorage.setItem('highContrast', highContrastToggle.checked);
    });
}
if (largeTextToggle) {
    largeTextToggle.addEventListener('change', () => {
        document.body.classList.toggle('large-text', largeTextToggle.checked);
        localStorage.setItem('largeText', largeTextToggle.checked);
    });
}
if (resetAccessibility) {
    resetAccessibility.addEventListener('click', () => {
        document.body.classList.remove('high-contrast', 'large-text', 'dark-mode');
        if (highContrastToggle) highContrastToggle.checked = false;
        if (largeTextToggle) largeTextToggle.checked = false;
        if (darkModeToggle) darkModeToggle.checked = false;
        localStorage.setItem('highContrast', 'false');
        localStorage.setItem('largeText', 'false');
        localStorage.setItem('darkMode', 'false');
        const icon = themeToggle ? themeToggle.querySelector('i') : null;
        if (icon) { icon.classList.add('fa-moon'); icon.classList.remove('fa-sun'); }
    });
}
if (saveAccessibility && accessibilityModal) {
    saveAccessibility.addEventListener('click', () => {
        if (highContrastToggle) localStorage.setItem('highContrast', highContrastToggle.checked);
        if (largeTextToggle) localStorage.setItem('largeText', largeTextToggle.checked);
        if (darkModeToggle) localStorage.setItem('darkMode', darkModeToggle.checked);
        accessibilityModal.style.display = 'none';
    });
}

// Restore preferences on load (dark mode applied early via base.html inline script)
window.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('highContrast') === 'true' && highContrastToggle) {
        document.body.classList.add('high-contrast');
        highContrastToggle.checked = true;
    }
    if (localStorage.getItem('largeText') === 'true' && largeTextToggle) {
        document.body.classList.add('large-text');
        largeTextToggle.checked = true;
    }
    if (localStorage.getItem('darkMode') === 'true') {
        // body class already set by inline script; just sync toggles
        if (darkModeToggle) darkModeToggle.checked = true;
        const icon = themeToggle ? themeToggle.querySelector('i') : null;
        if (icon) { icon.classList.remove('fa-moon'); icon.classList.add('fa-sun'); }
    }
});

if (accessibilityModal) {
    window.addEventListener('click', (e) => { if (e.target === accessibilityModal) accessibilityModal.style.display = 'none'; });
}

// News slider
const newsGrid = document.querySelector('.news-grid');
const newsPrev = document.querySelector('.news-prev');
const newsNext = document.querySelector('.news-next');

if (newsGrid && newsPrev && newsNext) {
    newsNext.addEventListener('click', () => newsGrid.scrollBy({ left: newsGrid.clientWidth, behavior: 'smooth' }));
    newsPrev.addEventListener('click', () => newsGrid.scrollBy({ left: -newsGrid.clientWidth, behavior: 'smooth' }));
    const checkNewsButtons = () => {
        newsPrev.disabled = newsGrid.scrollLeft === 0;
        newsNext.disabled = newsGrid.scrollLeft >= newsGrid.scrollWidth - newsGrid.clientWidth - 1;
    };
    newsGrid.addEventListener('scroll', checkNewsButtons);
    window.addEventListener('resize', checkNewsButtons);
    checkNewsButtons();
}

const langButtons = document.querySelectorAll('.lang-btn');
langButtons.forEach(button => {
    button.addEventListener('click', () => changeLanguage(button.getAttribute('data-lang')));
});

function changeLanguage(lang) {
    const url = new URL(window.location.href);
    url.searchParams.set('lang', lang);
    window.location.href = url.toString();
}

const searchForm = document.querySelector('.search-form');
if (searchForm) {
    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const queryInput = searchForm.querySelector('input[name="q"]');
        const langInput = searchForm.querySelector('input[name="lang"]');
        const query = queryInput ? queryInput.value.trim() : '';
        const lang = langInput ? langInput.value : (new URL(window.location.href).searchParams.get('lang') || 'ru');
        if (query) window.location.href = `/search?q=${encodeURIComponent(query)}&lang=${encodeURIComponent(lang)}`;
    });
}

const mainHeader = document.getElementById('mainHeader');
const smartNav = document.getElementById('smartNav');
let lastScrollY = window.scrollY;

// Функция, которая точно ставит меню под логотип
function adjustNavPosition() {
    if (mainHeader && smartNav) {
        const headerHeight = mainHeader.offsetHeight;
        smartNav.style.top = headerHeight + 'px';
    }
}

window.addEventListener('scroll', () => {
    const currentScrollY = window.scrollY;

    if (smartNav) {
        // Если крутим вниз и проехали больше 150px — прячем только меню
        if (currentScrollY > lastScrollY && currentScrollY > 150) {
            smartNav.classList.add('nav-hidden');
        } 
        // Если крутим вверх — возвращаем меню на место
        else {
            smartNav.classList.remove('nav-hidden');
        }
    }
    lastScrollY = currentScrollY;
}, { passive: true });

// Подстраиваем позиции при загрузке и ресайзе
window.addEventListener('resize', adjustNavPosition);
window.addEventListener('load', adjustNavPosition);