from pathlib import Path
from config.environment import load_config

BASE_DIR = Path(__file__).resolve().parent.parent
RUNTIME = load_config()
SECRET_KEY = RUNTIME.secret_key
DEBUG = False
ALLOWED_HOSTS = list(RUNTIME.allowed_hosts)
ALPHA_PROVIDERS_ENABLED = RUNTIME.providers_enabled
INSTALLED_APPS = ["django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions", "django.contrib.staticfiles", "alpha.apps.AlphaConfig"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware", "django.contrib.sessions.middleware.SessionMiddleware", "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [BASE_DIR / "templates"], "APP_DIRS": True, "OPTIONS": {"context_processors": ["django.template.context_processors.request", "django.contrib.auth.context_processors.auth"]}}]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "private" / "alpha.sqlite3", "ATOMIC_REQUESTS": False}}
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static" / "alpha"]
STATIC_ROOT = BASE_DIR / "public-static"
# Private database/media/scratch have no URL routes; persistence comes in T002.
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = RUNTIME.profile == "invited-alpha"
CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE
SECURE_SSL_REDIRECT = SESSION_COOKIE_SECURE
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
# No trust of forwarded scheme headers until gateway configuration is authorized.
TIME_ZONE = "Asia/Dhaka"
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
