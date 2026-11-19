import os

from .settings import *


def env_bool(name, default=False):
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def env_int(name, default):
    value = os.getenv(name)

    if value is None:
        return default

    return int(value)


DEBUG = False


SECRET_KEY = os.environ[
    "DJANGO_SECRET_KEY"
]


ALLOWED_HOSTS = env_list(
    "DJANGO_ALLOWED_HOSTS",
)


CSRF_TRUSTED_ORIGINS = env_list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
)


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv(
            "POSTGRES_DB",
            "rifttrace",
        ),
        "USER": os.getenv(
            "POSTGRES_USER",
            "rifttrace",
        ),
        "PASSWORD": os.environ[
            "POSTGRES_PASSWORD"
        ],
        "HOST": os.getenv(
            "POSTGRES_HOST",
            "db",
        ),
        "PORT": os.getenv(
            "POSTGRES_PORT",
            "5432",
        ),
        "CONN_MAX_AGE": 60,
    },
}


SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)


SECURE_SSL_REDIRECT = env_bool(
    "DJANGO_SECURE_SSL_REDIRECT",
    True,
)


SESSION_COOKIE_SECURE = env_bool(
    "DJANGO_SESSION_COOKIE_SECURE",
    True,
)


CSRF_COOKIE_SECURE = env_bool(
    "DJANGO_CSRF_COOKIE_SECURE",
    True,
)


SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_HTTPONLY = False


SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"

SECURE_REFERRER_POLICY = "same-origin"


SECURE_HSTS_SECONDS = env_int(
    "DJANGO_HSTS_SECONDS",
    31536000,
)


SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool(
    "DJANGO_HSTS_INCLUDE_SUBDOMAINS",
    True,
)


SECURE_HSTS_PRELOAD = env_bool(
    "DJANGO_HSTS_PRELOAD",
    False,
)


STATIC_ROOT = BASE_DIR / "staticfiles"


MIDDLEWARE = [
    MIDDLEWARE[0],
    "config.observability.RequestLoggingMiddleware",
    *MIDDLEWARE[1:],
]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "json": {
            "()": "config.observability.JsonFormatter",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },

    "root": {
        "handlers": [
            "console",
        ],
        "level": "INFO",
    },

    "loggers": {
        "django": {
            "handlers": [
                "console",
            ],
            "level": "INFO",
            "propagate": False,
        },

        "rifttrace.request": {
            "handlers": [
                "console",
            ],
            "level": "INFO",
            "propagate": False,
        },

        "rifttrace.health": {
            "handlers": [
                "console",
            ],
            "level": "INFO",
            "propagate": False,
        },
    },
}
