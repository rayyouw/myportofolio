(function () {
    const themeToggle = document.getElementById('theme-toggle');
    const root = document.documentElement;

    function applyTheme(theme) {
        const isLight = theme === 'light';
        root.dataset.theme = isLight ? 'light' : 'dark';
        if (themeToggle) {
            themeToggle.textContent = isLight ? '☾ Dark' : '☀ Light';
            themeToggle.setAttribute('aria-label', `Switch to ${isLight ? 'dark' : 'light'} theme`);
        }
    }

    let currentTheme = root.dataset.theme === 'light' ? 'light' : 'dark';
    applyTheme(currentTheme);

    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(currentTheme);
            try {
                localStorage.setItem('portfolio-theme', currentTheme);
            } catch (error) {
                // The selected theme still applies for this page when storage is unavailable.
            }
        });
    }
})();
