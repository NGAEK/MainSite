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
    link.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
            e.preventDefault();
            item.classList.toggle('active');
        }
    });
});

// Tab Navigation
const tabBtns = document.querySelectorAll('.tab-btn');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons and tab contents
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked button
        btn.classList.add('active');
        
        // Show corresponding tab content
        const tabId = btn.getAttribute('data-tab');
        document.getElementById(tabId).classList.add('active');
    });
});

//hero-slider
document.addEventListener('DOMContentLoaded', function() {
    const slidesContainer = document.querySelector('.slides-container');
    const slides = document.querySelectorAll('.slid');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    const dots = document.querySelectorAll('.slider-dot');
    let currentIndex = 0;

    if (!slidesContainer || !slides.length || !prevBtn || !nextBtn) {
        return;
    }

    function showSlide(index) {
        slidesContainer.style.transform = `translateX(-${index * 100}%)`;
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % slides.length;
        showSlide(currentIndex);
        
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        showSlide(currentIndex);
    }

    prevBtn.addEventListener('click', prevSlide);
    nextBtn.addEventListener('click', nextSlide);

    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentIndex = index;
            showSlide(currentIndex);
        });
    });

    // Auto slide
    setInterval(nextSlide, 5000);
});

// Gallery Slider
const gallerySlider = document.getElementById('gallerySlider');
const sliderDots = document.querySelectorAll('.slider-dot');
let currentSlide = 0;

if (gallerySlider && sliderDots.length) {
    sliderDots.forEach(dot => {
        dot.addEventListener('click', () => {
            const slideIndex = parseInt(dot.getAttribute('data-slide'));
            currentSlide = slideIndex;
            updateSlider();
        });
    });

    setInterval(() => {
        currentSlide = (currentSlide + 1) % sliderDots.length;
        updateSlider();
    }, 5000);

    function updateSlider() {
        gallerySlider.scrollTo({
            left: currentSlide * gallerySlider.offsetWidth,
            behavior: 'smooth'
        });
        
        sliderDots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentSlide);
        });
    }
}

// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const darkModeToggle = document.getElementById('darkModeToggle');

if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        themeToggle.querySelector('i').classList.toggle('fa-moon');
        themeToggle.querySelector('i').classList.toggle('fa-sun');
        
        if (darkModeToggle) {
            darkModeToggle.checked = document.body.classList.contains('dark-mode');
        }
    });
}

if (darkModeToggle) {
    darkModeToggle.addEventListener('change', () => {
        document.body.classList.toggle('dark-mode', darkModeToggle.checked);
    });
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
    accessibilityBtn.addEventListener('click', () => {
        accessibilityModal.style.display = 'flex';
    });
}

if (closeModal && accessibilityModal) {
    closeModal.addEventListener('click', () => {
        accessibilityModal.style.display = 'none';
    });
}

if (highContrastToggle) {
    highContrastToggle.addEventListener('change', () => {
        document.body.classList.toggle('high-contrast', highContrastToggle.checked);
    });
}

if (largeTextToggle) {
    largeTextToggle.addEventListener('change', () => {
        document.body.classList.toggle('large-text', largeTextToggle.checked);
    });
}

if (resetAccessibility && highContrastToggle && largeTextToggle && darkModeToggle) {
    resetAccessibility.addEventListener('click', () => {
        document.body.classList.remove('high-contrast', 'large-text', 'dark-mode');
        highContrastToggle.checked = false;
        largeTextToggle.checked = false;
        darkModeToggle.checked = false;
    });
}

if (saveAccessibility && accessibilityModal && highContrastToggle && largeTextToggle) {
    saveAccessibility.addEventListener('click', () => {
        localStorage.setItem('highContrast', highContrastToggle.checked);
        localStorage.setItem('largeText', largeTextToggle.checked);
        localStorage.setItem('darkMode', darkModeToggle ? darkModeToggle.checked : false);
        accessibilityModal.style.display = 'none';
    });
}

window.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('highContrast') === 'true' && highContrastToggle) {
        document.body.classList.add('high-contrast');
        highContrastToggle.checked = true;
    }
    
    if (localStorage.getItem('largeText') === 'true' && largeTextToggle) {
        document.body.classList.add('large-text');
        largeTextToggle.checked = true;
    }
    
    if (localStorage.getItem('darkMode') === 'true' && darkModeToggle) {
        document.body.classList.add('dark-mode');
        darkModeToggle.checked = true;
        if (themeToggle) {
            const icon = themeToggle.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            }
        }
    }
});

if (accessibilityModal) {
    window.addEventListener('click', (e) => {
        if (e.target === accessibilityModal) {
            accessibilityModal.style.display = 'none';
        }
    });
}

// news slider
const newsGrid = document.querySelector('.news-grid');
const newsPrev = document.querySelector('.news-prev');
const newsNext = document.querySelector('.news-next');

if (newsGrid && newsPrev && newsNext) {
    newsNext.addEventListener('click', () => {
        const scrollAmount = newsGrid.clientWidth;
        newsGrid.scrollBy({
            left: scrollAmount,
            behavior: 'smooth'
        });
    });

    newsPrev.addEventListener('click', () => {
        const scrollAmount = newsGrid.clientWidth;
        newsGrid.scrollBy({
            left: -scrollAmount,
            behavior: 'smooth'
        });
    });

    const checkNewsButtons = () => {
        const scrollLeft = newsGrid.scrollLeft;
        const maxScroll = newsGrid.scrollWidth - newsGrid.clientWidth;
        
        newsPrev.disabled = scrollLeft === 0;
        newsNext.disabled = scrollLeft >= maxScroll - 1;
    };

    newsGrid.addEventListener('scroll', checkNewsButtons);
    window.addEventListener('resize', checkNewsButtons);
    checkNewsButtons();
}

const langButtons = document.querySelectorAll('.lang-btn');

langButtons.forEach(button => {
    button.addEventListener('click', () => {
        const lang = button.getAttribute('data-lang');
        changeLanguage(lang);
    });
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
        if (query) {
            const url = `/search?q=${encodeURIComponent(query)}&lang=${encodeURIComponent(lang)}`;
            window.location.href = url;
        }
    });
}
