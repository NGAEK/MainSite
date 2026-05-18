(function () {
    'use strict';

    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mainNav       = document.getElementById('mainNav');
    const smartNav      = document.getElementById('smartNav');
    const mainHeader    = document.getElementById('mainHeader');

    if (!mobileMenuBtn || !mainNav) return;

    const MOBILE = () => window.innerWidth <= 768;

    /* ── Close button (fixed, top-left of nav area) ── */
    let closeBtn = document.getElementById('drawerCloseBtn');
    if (!closeBtn) {
        closeBtn = document.createElement('button');
        closeBtn.id   = 'drawerCloseBtn';
        closeBtn.type = 'button';
        closeBtn.setAttribute('aria-label', 'Закрыть меню');
        closeBtn.innerHTML = '<i class="fas fa-times"></i>';
        Object.assign(closeBtn.style, {
            display:        'none',
            alignItems:     'center',
            justifyContent: 'center',
            background:     'rgba(255,255,255,0.08)',
            border:         '1px solid rgba(255,255,255,0.13)',
            color:          'rgba(255,255,255,0.7)',
            cursor:         'pointer',
            fontFamily:     'var(--ff-body)',
            fontSize:       '1.1rem',
            width:          '38px',
            height:         '38px',
            borderRadius:   '10px',
            position:       'fixed',
            top:            '115px',
            left:           '12px',
            zIndex:         '99999',
            transition:     'background 0.15s, color 0.15s',
            border:         'none',
        });
        closeBtn.addEventListener('mouseenter', () => {
            closeBtn.style.background = 'rgba(255,255,255,0.2)';
            closeBtn.style.color = '#fff';
        });
        closeBtn.addEventListener('mouseleave', () => {
            closeBtn.style.background = 'rgba(255,255,255,0.08)';
            closeBtn.style.color = 'rgba(255,255,255,0.7)';
        });
        closeBtn.addEventListener('click', closeDrawer);
        document.body.appendChild(closeBtn);
    }

    /* ── Close drawer when clicking outside ── */
    function handleOutsideClick(e) {
        if (!MOBILE()) return;
        if (!mainNav.classList.contains('active')) return;
        if (mainNav.contains(e.target)) return;
        if (mobileMenuBtn.contains(e.target)) return;
        if (closeBtn.contains(e.target)) return;
        closeDrawer();
    }

    /* ── Open ── */
    function openDrawer() {
        if (!MOBILE()) return;
        closeBtn.style.display = 'flex';
        mainNav.classList.add('active');
        mobileMenuBtn.classList.add('active');
        document.body.style.overflow = 'hidden';
        mobileMenuBtn.setAttribute('aria-expanded', 'true');
        // Delay to avoid capturing the click that opened
        requestAnimationFrame(() => {
            document.addEventListener('click', handleOutsideClick);
        });
    }

    /* ── Close ── */
    function closeDrawer() {
        closeBtn.style.display = 'none';
        mainNav.classList.remove('active');
        mobileMenuBtn.classList.remove('active');
        document.body.style.overflow = '';
        mobileMenuBtn.setAttribute('aria-expanded', 'false');
        document.querySelectorAll('.main-nav > li.active')
            .forEach(li => li.classList.remove('active'));
        document.removeEventListener('click', handleOutsideClick);
    }

    /* ── Burger ── */
    mobileMenuBtn.setAttribute('aria-expanded', 'false');
    mobileMenuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        mainNav.classList.contains('active') ? closeDrawer() : openDrawer();
    });

    /* ── Escape → close ── */
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && mainNav.classList.contains('active')) {
            closeDrawer();
            mobileMenuBtn.focus();
        }
    });

    /* ── Dropdown accordion (только мобиль) ── */
    const navItems = document.querySelectorAll('.main-nav > li');

    navItems.forEach(item => {
        const link = item.querySelector(':scope > a');
        if (!link) return;

        link.addEventListener('click', e => {
            if (!MOBILE()) return;

            const hasDropdown = Boolean(item.querySelector('.dropdown-menu'));
            if (!hasDropdown) {
                closeDrawer();
                return;
            }

            e.preventDefault();

            const isOpen = item.classList.contains('active');
            navItems.forEach(other => {
                if (other !== item) other.classList.remove('active');
            });
            item.classList.toggle('active', !isOpen);
        });
    });

    /* ── Ссылки внутри дропдауна — закрываем ящик ── */
    mainNav.querySelectorAll('.dropdown-menu a').forEach(a => {
        a.addEventListener('click', () => {
            if (MOBILE()) closeDrawer();
        });
    });

    /* ── Resize → десктоп: сбрасываем всё ── */
    window.addEventListener('resize', () => {
        if (!MOBILE()) {
            closeDrawer();
            if (smartNav) smartNav.style.top = '';
        }
    });

    /* ── NAV SCROLL-HIDE ── */
    if (smartNav) {
        let lastY   = window.scrollY;
        let ticking = false;

        window.addEventListener('scroll', () => {
            if (ticking) return;
            ticking = true;
            requestAnimationFrame(() => {
                const y = window.scrollY;
                if (!mainNav.classList.contains('active')) {
                    smartNav.classList.toggle('nav-hidden', y > lastY && y > 150);
                }
                lastY   = y;
                ticking = false;
            });
        }, { passive: true });
    }

    /* ── DYNAMIC NAV TOP — только мобиль ── */
    function syncNavTop() {
        if (!mainHeader || !smartNav) return;
        if (!MOBILE()) {
            smartNav.style.top = '';
            return;
        }
        const h = mainHeader.getBoundingClientRect().height;
        smartNav.style.top = h + 'px';
    }

    const ro = window.ResizeObserver ? new ResizeObserver(syncNavTop) : null;
    if (ro && mainHeader) ro.observe(mainHeader);

    window.addEventListener('load', syncNavTop);
    syncNavTop();

    /* ══════════════════════════════════════════════════════════════
       SLIDER MODULE
       ══════════════════════════════════════════════════════════════ */

    /* ── 1. Hero Slider ── */
    (function initHeroSlider() {
        const slidesContainer = document.querySelector('.hero-slider .slides-container');
        const slides          = document.querySelectorAll('.hero-slider .slid');
        const prevBtn         = document.querySelector('.hero-slider .prev-btn');
        const nextBtn         = document.querySelector('.hero-slider .next-btn');
        const dots            = document.querySelectorAll('.hero-slider .slider-dot');

        if (!slidesContainer || !slides.length) return;

        let currentIndex = 0;
        let autoplayTimer = null;
        const AUTOPLAY_DELAY = 5000;

        function goToSlide(index) {
            if (index < 0) index = slides.length - 1;
            if (index >= slides.length) index = 0;
            currentIndex = index;

            slidesContainer.style.transform = 'translateX(-' + (currentIndex * 100) + '%)';

            dots.forEach(function(dot, i) {
                dot.classList.toggle('active', i === currentIndex);
            });
        }

        function prevSlide() { goToSlide(currentIndex - 1); }
        function nextSlide() { goToSlide(currentIndex + 1); }

        function startAutoplay() {
            stopAutoplay();
            autoplayTimer = setInterval(nextSlide, AUTOPLAY_DELAY);
        }

        function stopAutoplay() {
            if (autoplayTimer) {
                clearInterval(autoplayTimer);
                autoplayTimer = null;
            }
        }

        /* ── Events ── */
        if (prevBtn) prevBtn.addEventListener('click', function() { prevSlide(); startAutoplay(); });
        if (nextBtn) nextBtn.addEventListener('click', function() { nextSlide(); startAutoplay(); });

        dots.forEach(function(dot) {
            dot.addEventListener('click', function() {
                var idx = parseInt(this.getAttribute('data-slide'), 10);
                if (!isNaN(idx)) goToSlide(idx);
                startAutoplay();
            });
        });

        /* Pause on hover */
        var heroSlider = document.querySelector('.hero-slider');
        if (heroSlider) {
            heroSlider.addEventListener('mouseenter', stopAutoplay);
            heroSlider.addEventListener('mouseleave', startAutoplay);
        }

        /* ── Touch swipe for hero slider ── */
        var heroTouchStartX = 0;
        var heroTouchStartY = 0;
        var heroSwiped = false;

        if (heroSlider) {
            heroSlider.addEventListener('touchstart', function(e) {
                heroTouchStartX = e.changedTouches[0].screenX;
                heroTouchStartY = e.changedTouches[0].screenY;
                heroSwiped = false;
            }, { passive: true });

            heroSlider.addEventListener('touchmove', function(e) {
                if (heroSwiped) return;
                var dx = e.changedTouches[0].screenX - heroTouchStartX;
                var dy = e.changedTouches[0].screenY - heroTouchStartY;
                if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) {
                    heroSwiped = true;
                    if (dx < 0) {
                        nextSlide();
                    } else {
                        prevSlide();
                    }
                    startAutoplay();
                }
            }, { passive: true });
        }

        goToSlide(0);
        startAutoplay();
    })();

/* ══════════════════════════════════════════════════════════════
   THEME TOGGLE (DARK MODE)
   ══════════════════════════════════════════════════════════════ */
(function initThemeToggle() {
    const themeBtn = document.getElementById('themeToggle');
    if (!themeBtn) return;

    function applyDarkMode(enabled) {
        if (enabled) {
            document.body.classList.add('dark-mode');
            themeBtn.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            document.body.classList.remove('dark-mode');
            themeBtn.innerHTML = '<i class="fas fa-moon"></i>';
        }
        try {
            localStorage.setItem('darkMode', enabled ? 'true' : 'false');
        } catch(e) {}
    }

    // Sync initial state from localStorage
    try {
        const isDark = localStorage.getItem('darkMode') === 'true';
        applyDarkMode(isDark);
    } catch(e) {}

    themeBtn.addEventListener('click', function() {
        const isDark = document.body.classList.contains('dark-mode');
        applyDarkMode(!isDark);
    });
})();

/* ══════════════════════════════════════════════════════════════
   ACCESSIBILITY MODAL
   ══════════════════════════════════════════════════════════════ */
(function initAccessibilityModal() {
    const modal         = document.getElementById('accessibilityModal');
    const openBtn       = document.getElementById('accessibilityBtn');
    const closeBtn      = document.getElementById('closeModal');
    const saveBtn       = document.getElementById('saveAccessibility');
    const resetBtn      = document.getElementById('resetAccessibility');
    const highContrast  = document.getElementById('highContrastToggle');
    const largeText     = document.getElementById('largeTextToggle');
    const darkModeChk   = document.getElementById('darkModeToggle');

    if (!modal || !openBtn) return;

    function openModal() {
        // Load current settings into modal
        try {
            if (highContrast) highContrast.checked = localStorage.getItem('highContrast') === 'true';
            if (largeText) largeText.checked       = localStorage.getItem('largeText') === 'true';
            if (darkModeChk) darkModeChk.checked   = localStorage.getItem('darkMode') === 'true';
        } catch(e) {}

        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }

    function closeModalFn() {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }

    openBtn.addEventListener('click', openModal);

    if (closeBtn) closeBtn.addEventListener('click', closeModalFn);
    // Close modal when clicking on the dark backdrop (not on modal content)
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModalFn();
        }
    });

    // Close on Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.style.display !== 'none') {
            closeModalFn();
        }
    });

    // Save
    if (saveBtn) {
        saveBtn.addEventListener('click', function() {
            try {
                if (highContrast) localStorage.setItem('highContrast', highContrast.checked ? 'true' : 'false');
                if (largeText) localStorage.setItem('largeText', largeText.checked ? 'true' : 'false');
                if (darkModeChk) localStorage.setItem('darkMode', darkModeChk.checked ? 'true' : 'false');
            } catch(e) {}

            // Apply dark mode
            if (darkModeChk) {
                const themeBtn = document.getElementById('themeToggle');
                if (darkModeChk.checked) {
                    document.body.classList.add('dark-mode');
                    if (themeBtn) themeBtn.innerHTML = '<i class="fas fa-sun"></i>';
                } else {
                    document.body.classList.remove('dark-mode');
                    if (themeBtn) themeBtn.innerHTML = '<i class="fas fa-moon"></i>';
                }
            }

            // Apply high contrast
            if (highContrast) {
                document.body.classList.toggle('high-contrast', highContrast.checked);
            }

            // Apply large text
            if (largeText) {
                document.body.classList.toggle('large-text', largeText.checked);
            }

            closeModalFn();
        });
    }

    // Reset
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            try {
                if (highContrast) localStorage.removeItem('highContrast');
                if (largeText) localStorage.removeItem('largeText');
                localStorage.removeItem('darkMode');
            } catch(e) {}

            if (highContrast) highContrast.checked = false;
            if (largeText) largeText.checked = false;
            if (darkModeChk) darkModeChk.checked = false;

            document.body.classList.remove('high-contrast', 'large-text', 'dark-mode');

            const themeBtn = document.getElementById('themeToggle');
            if (themeBtn) themeBtn.innerHTML = '<i class="fas fa-moon"></i>';

            closeModalFn();
        });
    }

    // Apply saved settings on page load
    try {
        if (localStorage.getItem('highContrast') === 'true') {
            document.body.classList.add('high-contrast');
        }
        if (localStorage.getItem('largeText') === 'true') {
            document.body.classList.add('large-text');
        }
    } catch(e) {}
})();

/* ══════════════════════════════════════════════════════════════
   LANGUAGE SWITCHER
   ══════════════════════════════════════════════════════════════ */
(function initLanguageSwitcher() {
    const langBtns = document.querySelectorAll('.lang-btn');
    if (!langBtns.length) return;

    langBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var lang = this.getAttribute('data-lang');
            if (!lang) return;

            // Show loader
            var loader = document.createElement('div');
            loader.className = 'language-loader';
            loader.innerHTML = '<div class="loader-spinner"></div>';
            document.body.appendChild(loader);

            var url = new URL(window.location.href);
            url.searchParams.set('lang', lang);
            window.location.href = url.toString();
        });
    });
})();


    /* ── 2. Gallery Slider (dot navigation + arrows) ── */
    (function initGallerySlider() {
        var gallerySlider = document.getElementById('gallerySlider');
        var galleryDots   = document.querySelectorAll('#sliderNav .slider-dot');
        var prevBtn       = document.querySelector('.gallery-prev-btn');
        var nextBtn       = document.querySelector('.gallery-next-btn');

        if (!gallerySlider || !galleryDots.length) return;

        function goToGallerySlide(index) {
            var slides = gallerySlider.children;
            if (index < 0) index = slides.length - 1;
            if (index >= slides.length) index = 0;
            var slide = slides[index];
            if (slide) {
                slide.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' });
            }
            galleryDots.forEach(function(d) { d.classList.remove('active'); });
            galleryDots[index].classList.add('active');
        }

        galleryDots.forEach(function(dot) {
            dot.addEventListener('click', function() {
                var idx = parseInt(this.getAttribute('data-slide'), 10);
                if (isNaN(idx)) return;
                goToGallerySlide(idx);
            });
        });

        if (prevBtn) {
            prevBtn.addEventListener('click', function() {
                var activeIndex = 0;
                galleryDots.forEach(function(dot, i) {
                    if (dot.classList.contains('active')) activeIndex = i;
                });
                goToGallerySlide(activeIndex - 1);
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', function() {
                var activeIndex = 0;
                galleryDots.forEach(function(dot, i) {
                    if (dot.classList.contains('active')) activeIndex = i;
                });
                goToGallerySlide(activeIndex + 1);
            });
        }

        /* Update active dot on scroll */
        gallerySlider.addEventListener('scroll', function() {
            var scrollLeft = gallerySlider.scrollLeft;
            var slideWidth = gallerySlider.offsetWidth;
            if (!slideWidth) return;

            var activeIndex = Math.round(scrollLeft / slideWidth);

            galleryDots.forEach(function(dot, i) {
                dot.classList.toggle('active', i === activeIndex);
            });
        });

        /* ── Touch swipe for gallery slider ── */
        var galleryTouchStartX = 0;
        var galleryTouchStartY = 0;
        var gallerySwiped = false;

        gallerySlider.addEventListener('touchstart', function(e) {
            galleryTouchStartX = e.changedTouches[0].screenX;
            galleryTouchStartY = e.changedTouches[0].screenY;
            gallerySwiped = false;
        }, { passive: true });

        gallerySlider.addEventListener('touchmove', function(e) {
            if (gallerySwiped) return;
            var dx = e.changedTouches[0].screenX - galleryTouchStartX;
            var dy = e.changedTouches[0].screenY - galleryTouchStartY;
            if (Math.abs(dx) > 30 && Math.abs(dx) > Math.abs(dy)) {
                gallerySwiped = true;
                var activeIndex = 0;
                galleryDots.forEach(function(dot, i) {
                    if (dot.classList.contains('active')) activeIndex = i;
                });
                if (dx < 0) {
                    goToGallerySlide(activeIndex + 1);
                } else {
                    goToGallerySlide(activeIndex - 1);
                }
            }
        }, { passive: true });
    })();

    /* ── 3. News Slider (prev/next scroll) ── */
    (function initNewsSlider() {
        const newsGrid   = document.querySelector('.news-grid');
        const newsPrev   = document.querySelector('.news-prev');
        const newsNext   = document.querySelector('.news-next');

        if (!newsGrid || !newsPrev || !newsNext) return;

        var card = newsGrid.querySelector('.news-card');
        if (!card) return;
        var cardStyle = window.getComputedStyle(card);
        var cardWidth = card.offsetWidth + parseFloat(cardStyle.marginLeft) + parseFloat(cardStyle.marginRight);

        function updateButtons() {
            var maxScroll = newsGrid.scrollWidth - newsGrid.clientWidth;
            newsPrev.disabled = newsGrid.scrollLeft <= 0;
            newsNext.disabled = newsGrid.scrollLeft >= maxScroll - 1;
        }

        newsPrev.addEventListener('click', function() {
            newsGrid.scrollBy({ left: -cardWidth, behavior: 'smooth' });
            setTimeout(updateButtons, 350);
        });

        newsNext.addEventListener('click', function() {
            newsGrid.scrollBy({ left: cardWidth, behavior: 'smooth' });
            setTimeout(updateButtons, 350);
        });

        newsGrid.addEventListener('scroll', updateButtons);
        updateButtons();
    })();

})();