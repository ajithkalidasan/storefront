from .common import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-fay#fyga$&7j@$1dy-z*whqw)v2319rc^-l6mpr@xwp8pm!ow&"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
if DEBUG:
    MIDDLEWARE += ["silk.middleware.SilkyMiddleware",]