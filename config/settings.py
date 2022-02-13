"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path

import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="8*na@u$t-m*0agt!jk=m&x@3q827ha*_8p)m!&jhi_er90zt")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool, default=True) is True

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    cast=lambda allowed_hosts: [host.strip() for host in allowed_hosts.split(",")],
    default="127.0.0.1,localhost",
)

APPEND_SLASH = False


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_yasg",
    "rest_framework",
    "userservice.apps.UserserviceConfig",
    "feedservice.apps.FeedserviceConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASE_URL = config(
    "DATABASE_URL",
    default="postgresql://postgres:postgres@localhost:5433/rss_db",
)
# set db connection requests to 600 seconds to enable persistent connections
DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=0)}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Base User
AUTH_USER_MODEL = "userservice.User"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "PAGE_SIZE": 20,
    "DEFAULT_PAGINATION_CLASS": "utils.helpers.CustomPagination",
}


SIMPLE_JWT = {"ACCESS_TOKEN_LIFETIME": timedelta(minutes=5000), "REFRESH_TOKEN_LIFETIME": timedelta(days=1)}

REDIS_CONNECTION_URL = config("REDIS_URL", default="redis://localhost:6379/1")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CONNECTION_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


# Celery Config
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = CELERY_RESULT_BACKEND = CELERY_REDIS_SCHEDULER_URL = REDIS_CONNECTION_URL
CELERY_REDIS_SCHEDULER_KEY_PREFIX = "tasks:meta:"
CELERY_BEAT_SCHEDULER = "redbeat.RedBeatScheduler"
CELERY_BEAT_MAX_LOOP_INTERVAL = 2
CELERY_MAX_RETRY = config("CELERY_MAX_RETRY", default=3)
CELERY_RETRY_DELAY = config("CELERY_RETRY_DELAY", default=5)
CELERY_ALWAYS_EAGER = config("CELERY_ALWAYS_EAGER", cast=bool, default=False)


# SMTP Configs
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="smtp.ethereal.email")
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587)
EMAIL_FROM = config("EMAIL_FROM", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", default=False)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "sql.log",
        },
    },
    "loggers": {
        "django.db": {
            "level": "INFO",
            "handlers": ["file"],
        },
        "django.request": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
    },
}

# Swagger Docs Config
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {"api_key": {"type": "apiKey", "name": "authorization", "in": "header"}},
    "USE_SESSION_AUTH": False,
    "DOC_EXPANSION": "full",
}
