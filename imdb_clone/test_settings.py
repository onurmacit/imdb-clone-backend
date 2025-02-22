from .settings import *  # noqa: F403, F401

import os

SECRET_KEY = "django-test-key-123-for-ci"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test_imdb",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
        "TEST": {
            "NAME": "test_imdb",
        },
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "memory://")

DEBUG = os.getenv("DEBUG", "True") == "True"
