
// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mainNav = document.getElementById('mainNav');

mobileMenuBtn.addEventListener('click', () => {
    mainNav.classList.toggle('active');
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

// Gallery Slider
const gallerySlider = document.getElementById('gallerySlider');
const sliderDots = document.querySelectorAll('.slider-dot');
let currentSlide = 0;

// Set up dot navigation
sliderDots.forEach(dot => {
    dot.addEventListener('click', () => {
        const slideIndex = parseInt(dot.getAttribute('data-slide'));
        currentSlide = slideIndex;
        updateSlider();
    });
});

// Auto slide change
setInterval(() => {
    currentSlide = (currentSlide + 1) % sliderDots.length;
    updateSlider();
}, 5000);

function updateSlider() {
    gallerySlider.scrollTo({
        left: currentSlide * gallerySlider.offsetWidth,
        behavior: 'smooth'
    });
    
    // Update dots
    sliderDots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentSlide);
    });
}

// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const darkModeToggle = document.getElementById('darkModeToggle');

themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    themeToggle.querySelector('i').classList.toggle('fa-moon');
    themeToggle.querySelector('i').classList.toggle('fa-sun');
    
    // Update checkbox if in modal
    darkModeToggle.checked = document.body.classList.contains('dark-mode');
});

darkModeToggle.addEventListener('change', () => {
    document.body.classList.toggle('dark-mode', darkModeToggle.checked);
});

// Accessibility Modal
const accessibilityBtn = document.getElementById('accessibilityBtn');
const accessibilityModal = document.getElementById('accessibilityModal');
const closeModal = document.getElementById('closeModal');
const highContrastToggle = document.getElementById('highContrastToggle');
const largeTextToggle = document.getElementById('largeTextToggle');
const resetAccessibility = document.getElementById('resetAccessibility');
const saveAccessibility = document.getElementById('saveAccessibility');

accessibilityBtn.addEventListener('click', () => {
    accessibilityModal.style.display = 'flex';
});

closeModal.addEventListener('click', () => {
    accessibilityModal.style.display = 'none';
});

// High contrast mode
highContrastToggle.addEventListener('change', () => {
    document.body.classList.toggle('high-contrast', highContrastToggle.checked);
});

// Large text mode
largeTextToggle.addEventListener('change', () => {
    document.body.classList.toggle('large-text', largeTextToggle.checked);
});

// Reset accessibility settings
resetAccessibility.addEventListener('click', () => {
    document.body.classList.remove('high-contrast', 'large-text', 'dark-mode');
    highContrastToggle.checked = false;
    largeTextToggle.checked = false;
    darkModeToggle.checked = false;
});

// Save accessibility settings (could be extended to save to localStorage)
saveAccessibility.addEventListener('click', () => {
    localStorage.setItem('highContrast', highContrastToggle.checked);
    localStorage.setItem('largeText', largeTextToggle.checked);
    localStorage.setItem('darkMode', darkModeToggle.checked);
    accessibilityModal.style.display = 'none';
});

// Load saved settings
window.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('highContrast') === 'true') {
        document.body.classList.add('high-contrast');
        highContrastToggle.checked = true;
    }
    
    if (localStorage.getItem('largeText') === 'true') {
        document.body.classList.add('large-text');
        largeTextToggle.checked = true;
    }
    
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
        darkModeToggle.checked = true;
        themeToggle.querySelector('i').classList.remove('fa-moon');
        themeToggle.querySelector('i').classList.add('fa-sun');
    }
});

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === accessibilityModal) {
        accessibilityModal.style.display = 'none';
    }
});

// news slider
const newsGrid = document.querySelector('.news-grid');
const newsPrev = document.querySelector('.news-prev');
const newsNext = document.querySelector('.news-next');

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

// Disable buttons when at start/end
const checkNewsButtons = () => {
    const scrollLeft = newsGrid.scrollLeft;
    const maxScroll = newsGrid.scrollWidth - newsGrid.clientWidth;
    
    newsPrev.disabled = scrollLeft === 0;
    newsNext.disabled = scrollLeft >= maxScroll - 1;
};

newsGrid.addEventListener('scroll', checkNewsButtons);
window.addEventListener('resize', checkNewsButtons);
checkNewsButtons();