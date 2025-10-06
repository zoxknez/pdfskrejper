// Theme Management
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'dark';
        console.log('🎨 ThemeManager initialized with theme:', this.currentTheme);
        this.applyTheme(this.currentTheme);
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        this.currentTheme = theme;
        
        console.log('🎨 Theme applied:', theme);
        
        // Update toggle button icon
        const themeIcon = document.getElementById('themeIcon');
        if (themeIcon) {
            if (theme === 'dark') {
                themeIcon.className = 'bi bi-sun-fill';
            } else {
                themeIcon.className = 'bi bi-moon-fill';
            }
        }
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        console.log('🎨 Toggling theme from', this.currentTheme, 'to', newTheme);
        this.applyTheme(newTheme);
    }
}

// Initialize theme manager
const themeManager = new ThemeManager();

// Add event listener when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎨 Theme: Setting up event listeners');
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function(e) {
            e.preventDefault();
            themeManager.toggleTheme();
        });
        console.log('🎨 Theme toggle button found and configured');
    } else {
        console.warn('⚠️ Theme toggle button not found');
    }
});
