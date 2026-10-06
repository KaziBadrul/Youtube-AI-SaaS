/**
 * Accessible UI Component Behaviors
 * Manages disclosure toggles and accessible modal dialog focus traps.
 */

(function () {
  'use strict';

  var activeDialog = null;
  var previousActiveElement = null;

  // Accessible Disclosures
  function initDisclosures() {
    document.addEventListener('click', function (event) {
      var summary = event.target.closest('.disclosure-summary');
      if (!summary) return;

      var disclosure = summary.closest('.disclosure');
      if (!disclosure) return;

      var isExpanded = summary.getAttribute('aria-expanded') === 'true';
      var newExpanded = !isExpanded;

      summary.setAttribute('aria-expanded', newExpanded ? 'true' : 'false');

      var content = disclosure.querySelector('.disclosure-content');
      if (content) {
        content.setAttribute('aria-hidden', newExpanded ? 'false' : 'true');
      }

      if (newExpanded) {
        disclosure.classList.add('expanded');
      } else {
        disclosure.classList.remove('expanded');
      }
    });
  }

  // Accessible Dialog Focus Trap and Restoration
  function openDialog(dialogId) {
    var backdrop = document.getElementById(dialogId);
    if (!backdrop) return;

    previousActiveElement = document.activeElement;
    activeDialog = backdrop;

    backdrop.setAttribute('aria-hidden', 'false');
    backdrop.classList.add('open');

    // Focus first focusable element inside dialog or the dialog modal itself
    var focusable = backdrop.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    if (focusable.length > 0) {
      focusable[0].focus();
    }
  }

  function closeDialog(dialogId) {
    var backdrop = dialogId ? document.getElementById(dialogId) : activeDialog;
    if (!backdrop) return;

    backdrop.setAttribute('aria-hidden', 'true');
    backdrop.classList.remove('open');
    activeDialog = null;

    if (previousActiveElement && typeof previousActiveElement.focus === 'function') {
      previousActiveElement.focus();
      previousActiveElement = null;
    }
  }

  function initDialogs() {
    // Open triggers
    document.addEventListener('click', function (event) {
      var openBtn = event.target.closest('[data-dialog-open]');
      if (openBtn) {
        var targetId = openBtn.getAttribute('data-dialog-open');
        openDialog(targetId);
        return;
      }

      // Close triggers
      var closeBtn = event.target.closest('[data-dialog-close]');
      if (closeBtn) {
        var dialogBackdrop = closeBtn.closest('.dialog-backdrop');
        if (dialogBackdrop) {
          closeDialog(dialogBackdrop.id);
        }
        return;
      }

      // Backdrop click closes
      if (event.target.classList.contains('dialog-backdrop')) {
        closeDialog(event.target.id);
      }
    });

    // Keyboard navigation: Escape key to close, Tab to cycle focus inside dialog
    document.addEventListener('keydown', function (event) {
      if (!activeDialog) return;

      if (event.key === 'Escape' || event.key === 'Esc') {
        event.preventDefault();
        closeDialog();
        return;
      }

      if (event.key === 'Tab') {
        var focusables = activeDialog.querySelectorAll(
          'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
        );
        if (focusables.length === 0) return;

        var first = focusables[0];
        var last = focusables[focusables.length - 1];

        if (event.shiftKey) {
          if (document.activeElement === first) {
            event.preventDefault();
            last.focus();
          }
        } else {
          if (document.activeElement === last) {
            event.preventDefault();
            first.focus();
          }
        }
      }
    });
  }

  // Public API
  window.AlphaComponents = {
    openDialog: openDialog,
    closeDialog: closeDialog,
    init: function () {
      initDisclosures();
      initDialogs();
    },
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', window.AlphaComponents.init);
  } else {
    window.AlphaComponents.init();
  }
})();
