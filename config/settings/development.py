from .base import *  # noqa: F403 # Only to shutout linter ruff
from .base import (
    BASE_DIR,
    INSTALLED_APPS,
    MIDDLEWARE,
)

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

# INSTALLED_APPS += THIRD_PARTY_APPS

INSTALLED_APPS += [
    "debug_toolbar",
]


MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# SETTINGS OF DJANGO TOOLBAR
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]
