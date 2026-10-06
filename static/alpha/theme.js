/**
 * Theme Manager for Warm Creator Design System
 * Supports Light, Dark, and System preferences.
 * Persists user choice in localStorage.
 * Updates data-theme attribute on <html> without losing form input, selection, or focus.
 */

(function () {
  'use strict';

  var STORAGE_KEY = 'alpha_theme';
  var VALID_THEMES = ['light', 'dark', 'system'];

  function getStoredTheme() {
    try {
      var stored = localStorage.getItem(STORAGE_KEY);
      if (stored && VALID_THEMES.indexOf(stored) !== -1) {
        return stored;
      }
    } catch (e) {
      // localStorage may be disabled or restricted
    }

    var explicitAttr = document.documentElement.getAttribute('data-theme');
    if (explicitAttr && VALID_THEMES.indexOf(explicitAttr) !== -1 && explicitAttr !== 'system') {
      return explicitAttr;
    }

    return 'system';
  }

  function applyTheme(theme) {
    if (VALID_THEMES.indexOf(theme) === -1) {
      theme = 'system';
    }

    var root = document.documentElement;
    root.setAttribute('data-theme', theme);

    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (e) {}

    updateThemeSelectorControls(theme);
  }

  function updateThemeSelectorControls(theme) {
    var selectors = document.querySelectorAll('.theme-selector');
    selectors.forEach(function (sel) {
      var options = sel.querySelectorAll('.theme-option');
      options.forEach(function (opt) {
        var optVal = opt.getAttribute('data-theme-value');
        var isActive = optVal === theme;
        opt.setAttribute('aria-checked', isActive ? 'true' : 'false');
        if (isActive) {
          opt.classList.add('active');
        } else {
          opt.classList.remove('active');
        }
      });
    });
  }

  function initTheme() {
    var initial = getStoredTheme();
    applyTheme(initial);

    // Watch for OS preference changes when in 'system' mode
    if (window.matchMedia) {
      var mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      var handler = function () {
        if (getStoredTheme() === 'system') {
          // Do not mutate user focus or inputs; just ensure root stays system
          document.documentElement.setAttribute('data-theme', 'system');
        }
      };
      if (mediaQuery.addEventListener) {
        mediaQuery.addEventListener('change', handler);
      } else if (mediaQuery.addListener) {
        mediaQuery.addListener(handler);
      }
    }

    // Attach click handlers to theme-option buttons
    document.addEventListener('click', function (event) {
      var target = event.target.closest('.theme-option');
      if (target) {
        var themeVal = target.getAttribute('data-theme-value');
        if (themeVal) {
          applyTheme(themeVal);
        }
      }
    });
  }

  // Expose API for testing and programmatic switching
  window.AlphaTheme = {
    get: getStoredTheme,
    set: applyTheme,
    init: initTheme,
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
  } else {
    initTheme();
  }
})();
