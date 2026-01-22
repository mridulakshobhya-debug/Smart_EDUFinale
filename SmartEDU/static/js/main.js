/**
 * SmartEDU Pro - Main Application JavaScript
 * Professional UI interactions and functionality
 */

// ==================== Theme Management ====================
class SmartThemeManager {
    constructor() {
        this.storageKey = 'smartedu-theme';
        this.htmlElement = document.documentElement;
        this.init();
    }

    init() {
        this.loadTheme();
        this.setupEventListeners();
    }

    loadTheme() {
        const saved = localStorage.getItem(this.storageKey);
        const isDark = saved ? saved === 'dark' : this.prefersDark();
        this.setTheme(isDark ? 'dark' : 'light', false);
    }

    prefersDark() {
        return window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    setTheme(theme, notify = true) {
        this.htmlElement.setAttribute('data-theme', theme);
        if (typeof document.body !== 'undefined') {
            document.body.setAttribute('data-theme', theme);
        }
        localStorage.setItem(this.storageKey, theme);
        this.updateAllToggleIcons();
        
        if (notify) {
            this.showNotification(theme);
        }
    }

    toggleTheme() {
        const current = this.htmlElement.getAttribute('data-theme') || 'light';
        const next = current === 'light' ? 'dark' : 'light';
        this.setTheme(next, true);
    }

    setupEventListeners() {
        // Find all theme toggle buttons (main and navbar)
        const toggleButtons = document.querySelectorAll('#themeToggle, .theme-toggle-btn');
        toggleButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.toggleTheme();
                this.updateAllToggleIcons();
            });
        });
    }
    
    updateAllToggleIcons() {
        // Update all toggle button icons
        const theme = this.htmlElement.getAttribute('data-theme') || 'light';
        const toggleButtons = document.querySelectorAll('#themeToggle, .theme-toggle-btn');
        
        toggleButtons.forEach(button => {
            const icon = button.querySelector('.theme-icon');
            const sunIcon = button.querySelector('.sun-icon');
            const moonIcon = button.querySelector('.moon-icon');
            
            // For navbar-style button (emoji icon)
            if (icon && !sunIcon && !moonIcon) {
                icon.textContent = theme === 'dark' ? '☀️' : '🌙';
            }
            // For base-style button (SVG icons)
            else if (sunIcon && moonIcon) {
                if (theme === 'dark') {
                    sunIcon.style.opacity = '1';
                    sunIcon.style.display = 'block';
                    moonIcon.style.opacity = '0';
                    moonIcon.style.display = 'none';
                } else {
                    sunIcon.style.opacity = '0';
                    sunIcon.style.display = 'none';
                    moonIcon.style.opacity = '1';
                    moonIcon.style.display = 'block';
                }
            }
        });
    }

    showNotification(theme) {
        const message = theme === 'light' ? '☀️ Light Mode' : '🌙 Dark Mode';
        const notification = document.createElement('div');
        notification.className = 'theme-notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: 600;
            z-index: 9999;
            animation: slideInRight 0.3s ease-out;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        `;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 2000);
    }
}

// Initialize theme manager when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new SmartThemeManager();
    });
} else {
    new SmartThemeManager();
}

// ==================== Navigation ====================
function setupNavigation() {
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.style.display = 'none';
            });
        }
    });

    // Dropdown toggles
    document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            const menu = this.nextElementSibling;
            if (menu && menu.classList.contains('dropdown-menu')) {
                const isVisible = menu.style.display === 'block';
                // Close all other dropdowns
                document.querySelectorAll('.dropdown-menu').forEach(m => {
                    m.style.display = 'none';
                });
                // Toggle this dropdown
                menu.style.display = isVisible ? 'none' : 'block';
            }
        });
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupNavigation);
} else {
    setupNavigation();
}

// ==================== Smooth Scroll ====================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#' && document.querySelector(href)) {
            e.preventDefault();
            document.querySelector(href).scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// ==================== Modal Notifications ====================
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button class="alert-close" onclick="this.parentElement.remove();">×</button>
    `;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        z-index: 9999;
        animation: slideInRight 0.3s ease-out;
    `;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// ==================== Button Interactions ====================
function setupButtonInteractions() {
    document.querySelectorAll('.btn, button').forEach(btn => {
        btn.addEventListener('click', function() {
            // Add ripple effect
            const ripple = document.createElement('span');
            ripple.style.cssText = `
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.6);
                transform: scale(0);
                animation: ripple 0.6s ease-out;
                pointer-events: none;
            `;
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupButtonInteractions);
} else {
    setupButtonInteractions();
}

// ==================== Form Validation ====================
function setupFormValidation() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            this.querySelectorAll('input[required], textarea[required], select[required]').forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#ef4444';
                } else {
                    field.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Please fill in all required fields', 'warning');
            }
        });
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupFormValidation);
} else {
    setupFormValidation();
}

// ==================== Animations ====================
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ==================== Utility Functions ====================
window.SmartEDU = {
    showNotification,
    ThemeManager: SmartThemeManager,
    
    /**
     * Format date to readable format
     */
    formatDate(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },
    
    /**
     * Copy text to clipboard
     */
    copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copied to clipboard!', 'success');
        });
    },
    
    /**
     * Get URL parameter
     */
    getUrlParam(param) {
        const params = new URLSearchParams(window.location.search);
        return params.get(param);
    }
};

console.log('SmartEDU Pro - JavaScript initialized ✅');
