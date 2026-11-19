import os

from .settings import *


DEBUG = False


SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    (
        "rifttrace-ci-only-secret-key-"
        "not-for-production"
    ),
)


ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "testserver",
]


DATABASES = {
    "default": {
        "ENGINE":
            (
                "django.db.backends."
                "postgresql"
            ),

        "NAME":
            os.getenv(
                "POSTGRES_DB",
                "rifttrace_ci",
            ),

        "USER":
            os.getenv(
                "POSTGRES_USER",
                "rifttrace",
            ),

        "PASSWORD":
            os.getenv(
                "POSTGRES_PASSWORD",
                "rifttrace",
            ),

        "HOST":
            os.getenv(
                "POSTGRES_HOST",
                "127.0.0.1",
            ),

        "PORT":
            os.getenv(
                "POSTGRES_PORT",
                "5432",
            ),
    },
}


PASSWORD_HASHERS = [
    (
        "django.contrib.auth.hashers."
        "MD5PasswordHasher"
    ),
]


EMAIL_BACKEND = (
    "django.core.mail.backends."
    "locmem.EmailBackend"
)


SESSION_COOKIE_SECURE = False

CSRF_COOKIE_SECURE = False
