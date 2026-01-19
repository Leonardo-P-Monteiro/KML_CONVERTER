from .base import *  # noqa: F403
from .base import BASE_DIR, MIDDLEWARE, THIRD_PARTY_APPS  # Only to shutout linter ruff

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

# DEVELOPMENT-SPECIFIC APPS
THIRD_PARTY_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
