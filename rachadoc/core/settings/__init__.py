"""
Django settings for rachadoc project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import environ
from django.utils.translation import gettext_lazy as _
import os

env = environ.Env(
    LOCAL_BROKER_URL=(str, "redis://127.0.0.1/3"),
    LOCAL_CELERY_RESULT_BACKEND=(str, "redis://127.0.0.1/3"),
)
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="django-insecure--13fdqdnwt(6iktmydx%_%efzvv3i&=iyu(d+6q$0*si1u%gv+")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=False)

ALLOWED_HOSTS = [
    "https://rachadoc.com",
    "https://www.rachadoc.com",
    "https://rachadoc.vercel.app",
    "http://localhost:5173",
    "https://api.rachadoc.com",
    "http",
    "localhost",
]


# Application definition

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rosetta",
    "corsheaders",
    "django_extensions",
    "oauth2_provider",
    "rest_framework",
    "rest_framework_gis",
    "django_filters",
    "rules",
    "anymail",
    "django_celery_beat",
    "auditlog",
    "rachadoc.core",
    "rachadoc.accounts",
    "rachadoc.agendasetting",
    "rachadoc.clinic",
    "rachadoc.common",
    "rachadoc.events",
    "rachadoc.notification",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "rachadoc.core.urls"

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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": env.db(
        "DATABASE_DEFAULT_URL",
        default="postgresql://rachadoc:rachadoc@127.0.0.1:5432/rachadoc",
        engine="django.contrib.gis.db.backends.postgis",
    ),
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "fr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


LANGUAGES = [
    ("fr", _("French")),
]

LOCALE_PATHS = [
    f"{BASE_DIR}/accounts/locale",
    f"{BASE_DIR}/agendasetting/locale",
    f"{BASE_DIR}/clinic/locale",
    f"{BASE_DIR}/common/locale",
    f"{BASE_DIR}/events/locale",
    f"{BASE_DIR}/notification/locale",
    f"{BASE_DIR}/core/locale",
]

AUTHENTICATION_BACKENDS = (
    "rules.permissions.ObjectPermissionBackend",
    "django.contrib.auth.backends.ModelBackend",
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/"),
]

# Configure media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"

APPEND_SLASH = False

ASGI_APPLICATION = "core.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(env("REDIS_URL", default="127.0.0.1"), 6379)],
        },
    },
}

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = [
    "https://rachadoc.com",
    "https://www.rachadoc.com",
    "https://rachadoc.vercel.app",
    "http://localhost:5173",
    "https://api.rachadoc.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://rachadoc.com",
    "https://www.rachadoc.com",
    "https://rachadoc.vercel.app",
    "http://localhost:5173",
    "https://api.rachadoc.com",
]

EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@rachadoc.com"
SERVER_EMAIL = "root@rachadoc.com"

ANYMAIL = {
    "SENDINBLUE_API_KEY": env("SENDINBLUE_KEY", default=""),
}

AWS_USE_S3 = env("AWS_USE_S3", default=False)
if AWS_USE_S3:
    STORAGES = {
        "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
        "staticfiles": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"},
    }


from .api import *
from .business import *
from .celeryconf import *
from .celery_beat import *
from .aws import *
from .logging import *
