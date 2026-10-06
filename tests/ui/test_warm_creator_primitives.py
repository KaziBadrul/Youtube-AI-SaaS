"""Automated tests for T004 Warm Creator tokens, themes, and accessible primitives."""
import hashlib
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault(
    "ALPHA_SECRET_KEY",
    "synthetic-test-only-0123456789-abcdefghijklmnopqrstuvwxyz-ABCDEFGHIJKLMNOPQRSTUVWXYZ",
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.template.loader import render_to_string

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_DIR = BASE_DIR / "static" / "alpha"
TEMPLATES_DIR = BASE_DIR / "templates" / "alpha" / "components"
SCREENSHOTS_DIR = BASE_DIR / "tests" / "ui" / "screenshots"

BRAVE_PATH = Path("/Applications/Brave Browser.app/Contents/MacOS/Brave Browser")


def relative_luminance(hex_color: str) -> float:
    """Calculate WCAG 2.2 relative luminance for a given hex color."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

    def adjust(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)


def contrast_ratio(hex1: str, hex2: str) -> float:
    """Calculate WCAG 2.2 contrast ratio between two colors."""
    l1 = relative_luminance(hex1)
    l2 = relative_luminance(hex2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def parse_theme_tokens_from_css(css_text: str) -> dict[str, dict[str, str]]:
    """Dynamically parse CSS variable tokens from design.css for Light and Dark themes."""
    tokens: dict[str, dict[str, str]] = {"light": {}, "dark": {}}

    # Extract :root / [data-theme="light"]
    light_match = re.search(r"(?::root|\[data-theme=[\"']?light[\"']?\])[^{]*\{([^}]+)\}", css_text)
    if light_match:
        for line in light_match.group(1).splitlines():
            line = line.strip()
            if line.startswith("--") and ":" in line:
                k, v = line.split(":", 1)
                tokens["light"][k.strip()] = v.split(";")[0].strip()

    # Extract [data-theme="dark"]
    dark_match = re.search(r"\[data-theme=[\"']?dark[\"']?\]\s*\{([^}]+)\}", css_text)
    if dark_match:
        for line in dark_match.group(1).splitlines():
            line = line.strip()
            if line.startswith("--") and ":" in line:
                k, v = line.split(":", 1)
                tokens["dark"][k.strip()] = v.split(";")[0].strip()

    return tokens


def parse_system_media_tokens_from_css(css_text: str) -> dict[str, str]:
    """Parse CSS variable tokens defined in @media (prefers-color-scheme: dark)."""
    match = re.search(r"@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)\s*\{([^@]+)\}", css_text)
    if not match:
        return {}
    body = match.group(1)
    rule_match = re.search(r"(?:\[data-theme=[\"']?system[\"']?\]|:root)[^{]*\{([^}]+)\}", body)
    if not rule_match:
        return {}
    tokens = {}
    for line in rule_match.group(1).splitlines():
        line = line.strip()
        if line.startswith("--") and ":" in line:
            k, v = line.split(":", 1)
            tokens[k.strip()] = v.split(";")[0].strip()
    return tokens


class ContrastTokenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.css_path = STATIC_DIR / "design.css"
        cls.assertTrue(cls, cls.css_path.exists(), "design.css must exist")
        cls.css_content = cls.css_path.read_text()
        cls.tokens = parse_theme_tokens_from_css(cls.css_content)

    def test_light_theme_contrast_meets_wcag_aa(self) -> None:
        """Verify dynamically parsed Light theme tokens satisfy WCAG 2.2 AA."""
        t = self.tokens["light"]
        self.assertIn("--canvas", t)
        self.assertIn("--text-primary", t)

        canvas = t["--canvas"]

        # Text contrast: >= 4.5:1
        r_primary = contrast_ratio(canvas, t["--text-primary"])
        self.assertGreaterEqual(r_primary, 4.5, f"Light primary text ratio {r_primary:.2f} < 4.5")

        r_secondary = contrast_ratio(canvas, t["--text-secondary"])
        self.assertGreaterEqual(r_secondary, 4.5, f"Light secondary text ratio {r_secondary:.2f} < 4.5")

        r_muted = contrast_ratio(canvas, t["--text-muted"])
        self.assertGreaterEqual(r_muted, 4.5, f"Light muted text ratio {r_muted:.2f} < 4.5")

        # Action primary text: >= 4.5:1
        r_action = contrast_ratio(t["--action-primary"], t["--action-primary-text"])
        self.assertGreaterEqual(r_action, 4.5, f"Light action text ratio {r_action:.2f} < 4.5")

        # Control border / focus ring contrast: >= 3:1 (WCAG 2.2 SC 1.4.11 non-text contrast)
        r_border = contrast_ratio(canvas, t["--action-secondary-border"])
        self.assertGreaterEqual(r_border, 3.0, f"Light secondary control border ratio {r_border:.2f} < 3.0")

        r_ctrl = contrast_ratio(canvas, t["--control-border"])
        self.assertGreaterEqual(r_ctrl, 3.0, f"Light control border ratio {r_ctrl:.2f} < 3.0")

        r_ctrl_elevated = contrast_ratio(t["--surface-elevated"], t["--control-border"])
        self.assertGreaterEqual(r_ctrl_elevated, 3.0, f"Light control border on elevated surface {r_ctrl_elevated:.2f} < 3.0")

        r_focus = contrast_ratio(canvas, t["--focus-ring"])
        self.assertGreaterEqual(r_focus, 3.0, f"Light focus ring ratio {r_focus:.2f} < 3.0")

        # Status text contrast: >= 4.5:1
        self.assertGreaterEqual(contrast_ratio(t["--status-success-bg"], t["--status-success-text"]), 4.5)
        self.assertGreaterEqual(contrast_ratio(t["--status-warning-bg"], t["--status-warning-text"]), 4.5)
        self.assertGreaterEqual(contrast_ratio(t["--status-error-bg"], t["--status-error-text"]), 4.5)

    def test_dark_theme_contrast_meets_wcag_aa(self) -> None:
        """Verify dynamically parsed Dark theme tokens satisfy WCAG 2.2 AA."""
        t = self.tokens["dark"]
        self.assertIn("--canvas", t)
        self.assertIn("--text-primary", t)

        canvas = t["--canvas"]

        # Text contrast: >= 4.5:1
        r_primary = contrast_ratio(canvas, t["--text-primary"])
        self.assertGreaterEqual(r_primary, 4.5, f"Dark primary text ratio {r_primary:.2f} < 4.5")

        r_secondary = contrast_ratio(canvas, t["--text-secondary"])
        self.assertGreaterEqual(r_secondary, 4.5, f"Dark secondary text ratio {r_secondary:.2f} < 4.5")

        r_muted = contrast_ratio(canvas, t["--text-muted"])
        self.assertGreaterEqual(r_muted, 4.5, f"Dark muted text ratio {r_muted:.2f} < 4.5")

        # Elevated surface vs primary text
        r_elevated = contrast_ratio(t["--surface-elevated"], t["--text-primary"])
        self.assertGreaterEqual(r_elevated, 4.5, f"Dark elevated surface text ratio {r_elevated:.2f} < 4.5")

        # Action primary text: >= 4.5:1
        r_action = contrast_ratio(t["--action-primary"], t["--action-primary-text"])
        self.assertGreaterEqual(r_action, 4.5, f"Dark action text ratio {r_action:.2f} < 4.5")

        # Control border / focus ring contrast: >= 3:1 (WCAG 2.2 SC 1.4.11 non-text contrast)
        r_border = contrast_ratio(canvas, t["--action-secondary-border"])
        self.assertGreaterEqual(r_border, 3.0, f"Dark secondary control border ratio {r_border:.2f} < 3.0")

        r_ctrl = contrast_ratio(canvas, t["--control-border"])
        self.assertGreaterEqual(r_ctrl, 3.0, f"Dark control border ratio {r_ctrl:.2f} < 3.0")

        r_ctrl_elevated = contrast_ratio(t["--surface-elevated"], t["--control-border"])
        self.assertGreaterEqual(r_ctrl_elevated, 3.0, f"Dark control border on elevated surface {r_ctrl_elevated:.2f} < 3.0")

        r_focus = contrast_ratio(canvas, t["--focus-ring"])
        self.assertGreaterEqual(r_focus, 3.0, f"Dark focus ring ratio {r_focus:.2f} < 3.0")

        # Status text contrast: >= 4.5:1
        self.assertGreaterEqual(contrast_ratio(t["--status-success-bg"], t["--status-success-text"]), 4.5)
        self.assertGreaterEqual(contrast_ratio(t["--status-warning-bg"], t["--status-warning-text"]), 4.5)
        self.assertGreaterEqual(contrast_ratio(t["--status-error-bg"], t["--status-error-text"]), 4.5)

    def test_system_media_dark_mode_tokens(self) -> None:
        """Verify @media (prefers-color-scheme: dark) defines tokens matching dark theme exactly."""
        sys_tokens = parse_system_media_tokens_from_css(self.css_content)
        dark_tokens = self.tokens["dark"]
        self.assertGreater(len(sys_tokens), 0, "@media (prefers-color-scheme: dark) block must exist in design.css")

        # Critical tokens in the system dark media query must match dark theme tokens
        for key in [
            "--canvas",
            "--text-primary",
            "--text-secondary",
            "--surface-elevated",
            "--action-primary",
            "--action-secondary-border",
            "--control-border",
            "--focus-ring",
        ]:
            self.assertEqual(
                sys_tokens.get(key),
                dark_tokens.get(key),
                f"System token {key} in prefers-color-scheme media query does not match dark theme token",
            )


class DesignCssAntiPatternTests(unittest.TestCase):
    def setUp(self) -> None:
        self.css_path = STATIC_DIR / "design.css"
        self.assertTrue(self.css_path.exists(), "design.css must exist")
        self.css_content = self.css_path.read_text()

    def test_no_forbidden_ai_anti_patterns(self) -> None:
        """Verify absence of gradients, glows, glassmorphism, and pill-shaped extremes."""
        # No linear gradients or radial gradients
        self.assertNotIn("linear-gradient", self.css_content.lower())
        self.assertNotIn("radial-gradient", self.css_content.lower())

        # No glassmorphism backdrop-filter
        self.assertNotIn("backdrop-filter", self.css_content.lower())

        # No pill-shaped border radius (9999px or 50px)
        self.assertNotIn("9999px", self.css_content)
        self.assertNotIn("50px", self.css_content)

        # Radii are restrained (max <= 16px)
        radius_matches = re.findall(r"--radius-[a-z]+:\s*(\d+)px", self.css_content)
        for r in radius_matches:
            self.assertLessEqual(int(r), 16, f"Radius {r}px exceeds restrained guideline")

    def test_reduced_motion_overrides_exist(self) -> None:
        """Verify prefers-reduced-motion media query suppresses animations and transitions."""
        self.assertIn("prefers-reduced-motion", self.css_content)
        self.assertIn("transition-duration", self.css_content)
        self.assertIn("animation-duration", self.css_content)

    def test_visible_focus_ring_is_defined(self) -> None:
        """Verify visible focus ring is specified with focus-visible."""
        self.assertIn(":focus-visible", self.css_content)
        self.assertIn("--focus-ring", self.css_content)

    def test_form_control_primitive_defined(self) -> None:
        """Verify .form-input primitive is defined in design.css with --control-border."""
        self.assertIn(".form-input", self.css_content)
        self.assertIn("var(--control-border)", self.css_content)


class AccessibleComponentTemplateTests(unittest.TestCase):
    def test_button_template_rendering(self) -> None:
        """Verify button.html renders accessible semantic button with role/label."""
        rendered = render_to_string(
            "alpha/components/button.html",
            {"label": "Create Video", "variant": "primary", "id": "btn-create"},
        )
        self.assertIn("<button", rendered)
        self.assertIn('type="button"', rendered)
        self.assertIn('class="btn btn-primary"', rendered)
        self.assertIn('id="btn-create"', rendered)
        self.assertIn("Create Video", rendered)

    def test_disabled_button_accessibility(self) -> None:
        """Verify disabled button sets disabled and aria-disabled='true'."""
        rendered = render_to_string(
            "alpha/components/button.html",
            {"label": "Disabled Action", "disabled": True},
        )
        self.assertIn("disabled", rendered)
        self.assertIn('aria-disabled="true"', rendered)

    def test_dialog_template_accessibility(self) -> None:
        """Verify dialog.html places role='dialog' and aria-modal='true' on the modal box."""
        rendered = render_to_string(
            "alpha/components/dialog.html",
            {"id": "test-dialog", "title": "Delete Scene", "body": "Are you sure?"},
        )
        self.assertIn('class="dialog-backdrop"', rendered)
        self.assertIn('class="dialog-modal"', rendered)
        self.assertIn('role="dialog"', rendered)
        self.assertIn('aria-modal="true"', rendered)
        self.assertIn('aria-labelledby="test-dialog-title"', rendered)
        self.assertIn('aria-hidden="true"', rendered)
        self.assertIn("Delete Scene", rendered)
        self.assertIn("data-dialog-close", rendered)

    def test_disclosure_template_accessibility(self) -> None:
        """Verify disclosure.html sets aria-expanded and aria-controls on the trigger button."""
        rendered = render_to_string(
            "alpha/components/disclosure.html",
            {"id": "disc-test", "title": "See More", "content": "Hidden content"},
        )
        self.assertIn('class="disclosure"', rendered)
        self.assertIn('class="disclosure-summary"', rendered)
        self.assertIn('aria-expanded="false"', rendered)
        self.assertIn('aria-controls="disc-test-content"', rendered)
        self.assertIn("See More", rendered)
        # Verify the outer container div does NOT have aria-expanded
        self.assertNotIn('<div id="disc-test" class="disclosure" aria-expanded', rendered)

    def test_theme_selector_template_accessibility(self) -> None:
        """Verify theme_selector.html provides radiogroup with light, dark, and system."""
        rendered = render_to_string("alpha/components/theme_selector.html", {})
        self.assertIn('role="radiogroup"', rendered)
        self.assertIn('data-theme-value="light"', rendered)
        self.assertIn('data-theme-value="dark"', rendered)
        self.assertIn('data-theme-value="system"', rendered)


class ClientScriptBehaviorTests(unittest.TestCase):
    def test_theme_script_semantics(self) -> None:
        """Verify theme.js supports light, dark, system, localStorage, and input preservation."""
        theme_js = (STATIC_DIR / "theme.js").read_text()
        self.assertIn("alpha_theme", theme_js)
        self.assertIn("localStorage", theme_js)
        self.assertIn("prefers-color-scheme", theme_js)
        self.assertIn("data-theme", theme_js)
        self.assertIn("window.AlphaTheme", theme_js)

    def test_components_script_semantics(self) -> None:
        """Verify components.js implements Escape dismissal, Tab focus trap, and focus restoration."""
        comp_js = (STATIC_DIR / "components.js").read_text()
        self.assertIn("Escape", comp_js)
        self.assertIn("Tab", comp_js)
        self.assertIn("previousActiveElement", comp_js)
        self.assertIn("focus()", comp_js)
        self.assertIn("aria-expanded", comp_js)
        self.assertIn("window.AlphaComponents", comp_js)


class BrowserRuntimeBehaviorTests(unittest.TestCase):
    """Automated in-browser runtime testing via headless Brave."""

    def _build_test_page_html(self, preseed_storage_js: str = "") -> str:
        css = (STATIC_DIR / "design.css").read_text()
        theme_js = (STATIC_DIR / "theme.js").read_text()
        comp_js = (STATIC_DIR / "components.js").read_text()

        html = render_to_string("alpha/components/showcase.html", {})
        html = html.replace('<link rel="stylesheet" href="/static/alpha/design.css">', f"<style>{css}</style>")
        
        preseed_tag = f"<script>{preseed_storage_js}</script>" if preseed_storage_js else ""
        html = html.replace('<script src="/static/alpha/theme.js"></script>', f"{preseed_tag}<script>{theme_js}</script>")
        html = html.replace('<script src="/static/alpha/components.js"></script>', f"<script>{comp_js}</script>")

        return html

    def test_browser_interactive_contracts(self) -> None:
        """
        Verify in-browser interactive contracts:
        1. Theme switching across dark, light, and system modes while preserving input value, focus, and radio state.
        2. localStorage persistence of user theme choices.
        3. Disclosure expand/collapse toggling aria-expanded, aria-hidden, and .expanded.
        4. Modal dialog open, Tab / Shift+Tab focus trap wrapping, and Escape dismissal with focus restoration.
        """
        if not BRAVE_PATH.exists():
            self.skipTest("Brave browser not installed for headless browser testing")

        test_harness_script = """
<script>
window.addEventListener("DOMContentLoaded", function() {
  const testResults = { passed: true, errors: [] };
  function assert(cond, msg) {
    if (!cond) {
      testResults.passed = false;
      testResults.errors.push(msg);
    }
  }

  try {
    // 1. Theme switching test with form input preservation
    const input = document.getElementById("sample-input");
    input.value = "Preserved test prompt 12345";
    input.focus();
    assert(document.activeElement === input, "Input should have focus before switching theme");

    // Switch to Dark
    const darkBtn = document.querySelector('.theme-option[data-theme-value="dark"]');
    assert(darkBtn !== null, "Dark theme button should exist in theme selector");
    darkBtn.click();
    assert(document.documentElement.getAttribute("data-theme") === "dark", "Theme attribute must switch to dark");
    assert(localStorage.getItem("alpha_theme") === "dark", "localStorage must persist dark theme");
    assert(darkBtn.getAttribute("aria-checked") === "true", "Dark button aria-checked must be true");
    assert(darkBtn.classList.contains("active"), "Dark button must have active class");
    assert(input.value === "Preserved test prompt 12345", "Form input value must be preserved after dark switch");
    assert(document.activeElement === input, "Form input focus must be preserved after dark switch");

    // Switch to Light
    const lightBtn = document.querySelector('.theme-option[data-theme-value="light"]');
    lightBtn.click();
    assert(document.documentElement.getAttribute("data-theme") === "light", "Theme attribute must switch to light");
    assert(localStorage.getItem("alpha_theme") === "light", "localStorage must persist light theme");
    assert(lightBtn.getAttribute("aria-checked") === "true", "Light button aria-checked must be true");
    assert(lightBtn.classList.contains("active"), "Light button must have active class");
    assert(input.value === "Preserved test prompt 12345", "Form input value must be preserved after light switch");
    assert(document.activeElement === input, "Form input focus must be preserved after light switch");

    // Switch to System
    const sysBtn = document.querySelector('.theme-option[data-theme-value="system"]');
    assert(sysBtn !== null, "System theme button should exist in theme selector");
    sysBtn.click();
    assert(document.documentElement.getAttribute("data-theme") === "system", "Theme attribute must switch to system");
    assert(localStorage.getItem("alpha_theme") === "system", "localStorage must persist system theme");
    assert(sysBtn.getAttribute("aria-checked") === "true", "System button aria-checked must be true");
    assert(sysBtn.classList.contains("active"), "System button must have active class");
    assert(input.value === "Preserved test prompt 12345", "Form input value must be preserved after system switch");
    assert(document.activeElement === input, "Form input focus must be preserved after system switch");

    // 2. Disclosure expand and collapse behavior
    const discSummary = document.querySelector("#settings-disclosure .disclosure-summary");
    const discContent = document.getElementById("settings-disclosure-content");
    const discContainer = document.getElementById("settings-disclosure");
    assert(discSummary !== null, "Disclosure summary button must exist");
    assert(discSummary.getAttribute("aria-expanded") === "false", "Disclosure initially aria-expanded false");
    assert(discContent.getAttribute("aria-hidden") === "true", "Disclosure content initially hidden");
    assert(!discContainer.classList.contains("expanded"), "Disclosure container initially not expanded");

    discSummary.click();
    assert(discSummary.getAttribute("aria-expanded") === "true", "Disclosure aria-expanded true on click");
    assert(discContent.getAttribute("aria-hidden") === "false", "Disclosure content visible on click");
    assert(discContainer.classList.contains("expanded"), "Disclosure container has class expanded");

    discSummary.click();
    assert(discSummary.getAttribute("aria-expanded") === "false", "Disclosure aria-expanded false on collapse");
    assert(discContent.getAttribute("aria-hidden") === "true", "Disclosure content hidden on collapse");
    assert(!discContainer.classList.contains("expanded"), "Disclosure container expanded class removed");

    // 3. Dialog open, Tab focus trap, and Escape dismissal
    const openBtn = document.querySelector('[data-dialog-open="demo-dialog"]');
    const dialog = document.getElementById("demo-dialog");
    assert(openBtn !== null, "Dialog trigger button must exist");
    assert(dialog.getAttribute("aria-hidden") === "true", "Dialog initially hidden");

    openBtn.focus();
    assert(document.activeElement === openBtn, "Trigger button focused before dialog open");
    openBtn.click();

    assert(dialog.getAttribute("aria-hidden") === "false", "Dialog opened aria-hidden false");
    assert(dialog.classList.contains("open"), "Dialog backdrop has open class");
    assert(dialog.contains(document.activeElement), "Focus must enter inside dialog");

    const focusables = dialog.querySelectorAll("button:not([disabled]), [href], input:not([disabled])");
    const firstFocusable = focusables[0];
    const lastFocusable = focusables[focusables.length - 1];

    // Forward Tab wrap
    lastFocusable.focus();
    assert(document.activeElement === lastFocusable, "Last focusable focused");
    document.dispatchEvent(new KeyboardEvent("keydown", { key: "Tab", bubbles: true }));
    assert(document.activeElement === firstFocusable, "Tab from last element must wrap to first element");

    // Backward Shift+Tab wrap
    firstFocusable.focus();
    assert(document.activeElement === firstFocusable, "First focusable focused");
    document.dispatchEvent(new KeyboardEvent("keydown", { key: "Tab", shiftKey: true, bubbles: true }));
    assert(document.activeElement === lastFocusable, "Shift+Tab from first element must wrap to last element");

    // Escape closes dialog and restores focus to openBtn
    document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
    assert(dialog.getAttribute("aria-hidden") === "true", "Dialog closed after Escape key");
    assert(!dialog.classList.contains("open"), "Dialog open class removed after Escape");
    assert(document.activeElement === openBtn, "Focus restored to openBtn after Escape dismissal");

  } catch (err) {
    testResults.passed = false;
    testResults.errors.push("Exception: " + err.message);
  }

  const resDiv = document.createElement("div");
  resDiv.id = "browser-test-results";
  resDiv.setAttribute("data-passed", testResults.passed ? "true" : "false");
  resDiv.setAttribute("data-errors", JSON.stringify(testResults.errors));
  resDiv.textContent = JSON.stringify(testResults);
  document.body.appendChild(resDiv);
});
</script>
"""
        html_content = self._build_test_page_html().replace("</body>", f"{test_harness_script}</body>")

        with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=False) as tf:
            tf.write(html_content)
            tf.flush()
            temp_html = Path(tf.name)

        try:
            cmd = [
                str(BRAVE_PATH),
                "--headless",
                "--disable-gpu",
                "--dump-dom",
                f"file://{temp_html}",
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            self.assertEqual(res.returncode, 0, f"Brave process failed: {res.stderr}")

            match_passed = re.search(r'data-passed="([^"]+)"', res.stdout)
            match_errors = re.search(r'data-errors="([^"]+)"', res.stdout)

            self.assertIsNotNone(match_passed, "Browser test harness div not found in dumped DOM")
            passed = match_passed.group(1) == "true"
            errors = json.loads(match_errors.group(1).replace("&quot;", '"')) if match_errors else []

            self.assertTrue(passed, f"Browser interactive test failures: {errors}")
            self.assertEqual(len(errors), 0, f"Encountered browser errors: {errors}")
        finally:
            if temp_html.exists():
                temp_html.unlink()

    def test_theme_preference_persistence_restoration(self) -> None:
        """
        Verify that a theme preference stored in localStorage is correctly restored on page init,
        preventing regressions where localStorage is written but never read back (Mutation 2 guard).
        """
        if not BRAVE_PATH.exists():
            self.skipTest("Brave browser not installed for headless browser testing")

        test_harness_script = """
<script>
window.addEventListener("DOMContentLoaded", function() {
  const testResults = { passed: true, errors: [] };
  function assert(cond, msg) {
    if (!cond) {
      testResults.passed = false;
      testResults.errors.push(msg);
    }
  }

  try {
    // Check restored theme attribute matches localStorage value
    const themeAttr = document.documentElement.getAttribute("data-theme");
    assert(themeAttr === "dark", "Theme should restore to dark from pre-seeded localStorage, got: " + themeAttr);

    const darkOpt = document.querySelector('.theme-option[data-theme-value="dark"]');
    assert(darkOpt !== null, "Dark option must exist");
    assert(darkOpt.getAttribute("aria-checked") === "true", "Restored dark option aria-checked must be true");
    assert(darkOpt.classList.contains("active"), "Restored dark option must have active class");

  } catch (err) {
    testResults.passed = false;
    testResults.errors.push("Exception: " + err.message);
  }

  const resDiv = document.createElement("div");
  resDiv.id = "persistence-restore-results";
  resDiv.setAttribute("data-passed", testResults.passed ? "true" : "false");
  resDiv.setAttribute("data-errors", JSON.stringify(testResults.errors));
  document.body.appendChild(resDiv);
});
</script>
"""
        preseed_js = "try { localStorage.setItem('alpha_theme', 'dark'); } catch(e) {}"
        html_content = self._build_test_page_html(preseed_storage_js=preseed_js).replace(
            "</body>", f"{test_harness_script}</body>"
        )

        with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=False) as tf:
            tf.write(html_content)
            tf.flush()
            temp_html = Path(tf.name)

        try:
            cmd = [
                str(BRAVE_PATH),
                "--headless",
                "--disable-gpu",
                "--dump-dom",
                f"file://{temp_html}",
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            self.assertEqual(res.returncode, 0, f"Brave process failed: {res.stderr}")

            match_passed = re.search(r'data-passed="([^"]+)"', res.stdout)
            match_errors = re.search(r'data-errors="([^"]+)"', res.stdout)

            self.assertIsNotNone(match_passed, "Persistence restore test div not found in dumped DOM")
            passed = match_passed.group(1) == "true"
            errors = json.loads(match_errors.group(1).replace("&quot;", '"')) if match_errors else []

            self.assertTrue(passed, f"Theme persistence restoration failures: {errors}")
            self.assertEqual(len(errors), 0, f"Encountered persistence restore errors: {errors}")
        finally:
            if temp_html.exists():
                temp_html.unlink()


class ScreenshotVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    def _render_showcase_html(self, theme: str) -> str:
        """Render self-contained showcase HTML string with inlined CSS, scripts, and explicit data-theme."""
        css_content = (STATIC_DIR / "design.css").read_text()
        theme_js = (STATIC_DIR / "theme.js").read_text()
        comp_js = (STATIC_DIR / "components.js").read_text()

        html = render_to_string("alpha/components/showcase.html", {})
        html = html.replace(
            '<link rel="stylesheet" href="/static/alpha/design.css">',
            f"<style>{css_content}</style>",
        )
        html = html.replace(
            '<script src="/static/alpha/theme.js"></script>',
            f"<script>{theme_js}</script>",
        )
        html = html.replace(
            '<script src="/static/alpha/components.js"></script>',
            f"<script>{comp_js}</script>",
        )
        # Set explicit data-theme on <html>
        html = html.replace(
            '<html lang="en">',
            f'<html lang="en" data-theme="{theme}">',
        )
        return html

    def _capture_screenshot(self, html_content: str, output_png: Path, width: int, height: int) -> bool:
        if not BRAVE_PATH.exists():
            return False

        with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=False) as tf:
            tf.write(html_content)
            tf.flush()
            temp_html = Path(tf.name)

        try:
            cmd = [
                str(BRAVE_PATH),
                "--headless",
                f"--screenshot={output_png}",
                f"--window-size={width},{height}",
                f"file://{temp_html}",
            ]
            subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            return output_png.exists() and output_png.stat().st_size > 1000
        finally:
            if temp_html.exists():
                temp_html.unlink()

    def test_generate_desktop_and_mobile_screenshots(self) -> None:
        """
        Generate component screenshots in both Light and Dark themes for:
        - Desktop (1280x800)
        - Mobile (390x844)
        And assert light and dark screenshots are visually distinct (different hashes).
        """
        if not BRAVE_PATH.exists():
            self.skipTest("Brave browser not installed for headless screenshot generation")

        shots = [
            ("light", 1280, 800, SCREENSHOTS_DIR / "desktop_light.png"),
            ("dark", 1280, 800, SCREENSHOTS_DIR / "desktop_dark.png"),
            ("light", 390, 844, SCREENSHOTS_DIR / "mobile_light.png"),
            ("dark", 390, 844, SCREENSHOTS_DIR / "mobile_dark.png"),
        ]

        hashes = {}
        for theme, w, h, path in shots:
            html = self._render_showcase_html(theme)
            success = self._capture_screenshot(html, path, w, h)
            self.assertTrue(success, f"Failed to generate screenshot for {path.name}")
            # Verify PNG signature
            with open(path, "rb") as f:
                content = f.read()
                self.assertEqual(content[:8], b"\x89PNG\r\n\x1a\n", f"{path.name} is not a valid PNG")
                hashes[f"{path.name}"] = hashlib.sha256(content).hexdigest()

        # Verify Light and Dark screenshots are distinct (Issue 1)
        self.assertNotEqual(
            hashes["desktop_light.png"],
            hashes["desktop_dark.png"],
            "Desktop light and dark screenshots must not be identical",
        )
        self.assertNotEqual(
            hashes["mobile_light.png"],
            hashes["mobile_dark.png"],
            "Mobile light and dark screenshots must not be identical",
        )


if __name__ == "__main__":
    unittest.main()
