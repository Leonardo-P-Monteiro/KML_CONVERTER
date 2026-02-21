from .base import *  # noqa: I001 F403
from decouple import config
from .base import (
    BASE_DIR,
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost")

# DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}
