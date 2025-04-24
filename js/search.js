document.addEventListener('DOMContentLoaded', function() {
    // Обработка поисковой формы
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="q"]');

        // Добавляем кнопку очистки
        const clearBtn = document.createElement('button');
        clearBtn.type = 'button';
        clearBtn.className = 'clear-search';
        clearBtn.innerHTML = '<i class="fas fa-times"></i>';
        clearBtn.style.display = 'none';
        clearBtn.setAttribute('aria-label', 'Очистить поиск');

        clearBtn.addEventListener('click', function() {
            searchInput.value = '';
            clearBtn.style.display = 'none';
            searchInput.focus();
        });

        searchForm.insertBefore(clearBtn, searchForm.querySelector('button[type="submit"]'));

        searchInput.addEventListener('input', function() {
            clearBtn.style.display = this.value ? 'block' : 'none';
        });

        // Фокус на поле поиска если есть параметр q
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('q')) {
            searchInput.value = urlParams.get('q');
            if (searchInput.value) {
                clearBtn.style.display = 'block';
            }
        }
    }
});