//
//  Dark mode functionality
//

function toggleDarkMode() {
    const isDark = document.body.classList.toggle('dark-mode');
    const button = document.getElementById('darkModeBtn');

    // Change button test according to language
    if (isDark) {
        button.value = LANG === 'en' ? 'Light mode' : 'Ljust läge';
        localStorage.setItem('darkMode', 'enabled');
    } else {
        button.value = LANG === 'en' ? 'Dark mode' : 'Mörkt läge';
        localStorage.setItem('darkMode', 'disabled');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('darkModeBtn');
    const darkModeSetting = localStorage.getItem('darkMode');

    if (darkModeSetting === 'enabled') {
        document.body.classList.add('dark-mode');
        button.value = LANG === 'en' ? 'Light mode' : 'Ljust läge';
    }
});
