// Language Management
class LanguageManager {
    constructor() {
        this.currentLang = localStorage.getItem('language') || 'sr';
        this.translations = {};
        console.log('🌍 LanguageManager initialized with language:', this.currentLang);
        this.loadTranslations();
    }

    async loadTranslations() {
        try {
            console.log('🌍 Loading translations for:', this.currentLang);
            const cacheBust = Date.now();
            const response = await fetch(`/static/locales/${this.currentLang}.json?v=${cacheBust}`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            this.translations = await response.json();
            console.log('🌍 Translations loaded:', Object.keys(this.translations));
            this.applyTranslations();
        } catch (error) {
            console.error('❌ Error loading translations:', error);
        }
    }

    applyTranslations() {
        console.log('🌍 Applying translations...');
        let translatedCount = 0;
        
        // Update text content
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.getNestedTranslation(key);
            if (translation) {
                // Check if translation is an object (error case)
                if (typeof translation === 'object') {
                    console.error('❌ Translation is object for key:', key, translation);
                    return;
                }
                element.textContent = translation;
                translatedCount++;
            } else {
                console.warn('⚠️ Translation not found for key:', key);
            }
        });

        // Update placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            const translation = this.getNestedTranslation(key);
            if (translation) {
                element.placeholder = translation;
                translatedCount++;
            }
        });

        // Update button values
        document.querySelectorAll('[data-i18n-value]').forEach(element => {
            const key = element.getAttribute('data-i18n-value');
            const translation = this.getNestedTranslation(key);
            if (translation) {
                element.value = translation;
                translatedCount++;
            }
        });

        // Update option elements in select dropdowns
        document.querySelectorAll('option[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.getNestedTranslation(key);
            if (translation) {
                element.textContent = translation;
                translatedCount++;
            }
        });

        // Update language flag icon
        const langFlag = document.getElementById('langFlag');
        if (langFlag) {
            langFlag.textContent = this.currentLang === 'sr' ? 'SRB' : 'EN';
        }
        
        console.log(`🌍 Applied ${translatedCount} translations`);
    }

    getNestedTranslation(key) {
        return key.split('.').reduce((obj, k) => obj?.[k], this.translations);
    }

    async switchLanguage(lang) {
        console.log('🌍 Switching language from', this.currentLang, 'to', lang);
        this.currentLang = lang;
        localStorage.setItem('language', lang);
        await this.loadTranslations();
    }
}

// Initialize language manager
const languageManager = new LanguageManager();

// Add event listener when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('🌍 Language: Setting up event listeners');
    const langToggle = document.getElementById('langToggle');
    if (langToggle) {
        langToggle.addEventListener('click', function(e) {
            e.preventDefault();
            const newLang = languageManager.currentLang === 'sr' ? 'en' : 'sr';
            languageManager.switchLanguage(newLang);
        });
        console.log('🌍 Language toggle button found and configured');
    } else {
        console.warn('⚠️ Language toggle button not found');
    }
});
