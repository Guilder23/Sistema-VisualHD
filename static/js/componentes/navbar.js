document.addEventListener('DOMContentLoaded', function () {
    const notificacionesBtn = document.getElementById('notificacionesBtn');
    const notificacionesDropdown = document.getElementById('notificacionesDropdown');
    const usuarioBtn = document.getElementById('usuarioBtn');
    const usuarioDropdown = document.getElementById('usuarioDropdown');
    const darkModeToggle = document.getElementById('darkModeToggle');

    // Modo Oscuro
    function initDarkMode() {
        const savedMode = localStorage.getItem('darkMode');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

        if (savedMode === 'true' || (!savedMode && prefersDark)) {
            document.body.classList.add('dark-mode');
            updateDarkModeIcon(true);
        }
    }

    function toggleDarkMode() {
        document.body.classList.toggle('dark-mode');
        const isDarkMode = document.body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDarkMode);
        updateDarkModeIcon(isDarkMode);
    }

    function updateDarkModeIcon(isDarkMode) {
        if (darkModeToggle) {
            const icon = darkModeToggle.querySelector('i');
            if (icon) {
                icon.className = isDarkMode ? 'fas fa-sun' : 'fas fa-moon';
            }
        }
    }

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            toggleDarkMode();
        });
    }

    // Inicializar modo oscuro
    initDarkMode();

    if (notificacionesBtn && notificacionesDropdown) {
        notificacionesBtn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            usuarioDropdown?.classList.remove('show');
            notificacionesDropdown.classList.toggle('show');
        });
    }

    if (usuarioBtn && usuarioDropdown) {
        usuarioBtn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            notificacionesDropdown?.classList.remove('show');
            usuarioDropdown.classList.toggle('show');
        });
    }

    document.addEventListener('click', function () {
        notificacionesDropdown?.classList.remove('show');
        usuarioDropdown?.classList.remove('show');
    });
});
