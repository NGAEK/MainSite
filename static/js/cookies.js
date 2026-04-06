(function () {
    var KEY = 'ngaek_cookie_consent';
    var banner = document.getElementById('cookie-banner');
    if (!banner) return;

    function hide() {
        banner.classList.add('cookie-banner--hidden');
        banner.setAttribute('aria-hidden', 'true');
    }

    try {
        if (localStorage.getItem(KEY) === '1') {
            hide();
            return;
        }
    } catch (e) {
        /* ignore */
    }

    banner.setAttribute('aria-hidden', 'false');
    var accept = document.getElementById('cookie-accept');
    if (accept) {
        accept.addEventListener('click', function () {
            try {
                localStorage.setItem(KEY, '1');
            } catch (e) {
                /* ignore */
            }
            hide();
        });
    }
})();
