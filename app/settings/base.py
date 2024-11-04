import contextlib
from os import environ
from os.path import join

from django.urls import reverse_lazy

from docs.markdown import CustomHtmlFormatter

from .helpers import BASE_DIR

# Security

SECRET_KEY = environ.get("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = []
ALLOWED_HOSTS += environ.get("ALLOWED_HOSTS", "").split(",")

CSRF_TRUSTED_ORIGINS = []
CSRF_TRUSTED_ORIGINS += environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")


# Application definition

INSTALLED_APPS = [
    "dal",
    "dal_select2",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",
    "authentication",
    "docs",
    "markdownx",
    "storages",
    "taggit",
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

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            join(BASE_DIR, "templates"),
        ],
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


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": environ.get("RDS_HOSTNAME"),
        "PORT": environ.get("RDS_PORT"),
        "NAME": environ.get("RDS_DB_NAME"),
        "USER": environ.get("RDS_USERNAME"),
        "PASSWORD": environ.get("RDS_PASSWORD"),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Email

DEFAULT_FROM_EMAIL = "Django <no_reply@example.com>"
EMAIL_HOST = environ.get("EMAIL_HOST")
EMAIL_PORT = environ.get("EMAIL_PORT")
EMAIL_HOST_USER = environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False


# Authentication

AUTH_PASSWORD_VALIDATORS = [{
    "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
}, {
    "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
}, {
    "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
}, {
    "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
}]

AUTH_USER_MODEL = "authentication.User"

LOGIN_URL = reverse_lazy("login")
LOGIN_REDIRECT_URL = LOGOUT_REDIRECT_URL = "/"


# Internationalization

LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", "English"),
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# AWS

AWS_ACCESS_KEY_ID = environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = environ.get("AWS_S3_REGION_NAME")


# Storages

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "default_acl": "private",
            "location": "",
            "querystring_auth": True,
            "file_overwrite": False,
            "gzip": False,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "default_acl": "public-read",
            "location": "static",
            "querystring_auth": False,
            "file_overwrite": True,
            "gzip": True,
            "object_parameters": {
                "CacheControl": "max-age=86400",
            },
        },
    },
}


# Static

STATICFILES_DIRS = [join(BASE_DIR, "static")]
STATIC_URL = "/static/"


# Media

MEDIA_ROOT = join(BASE_DIR, "public/media")
MEDIA_URL = "/media/"


# File Storage

FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 99


# Data Upload

DATA_UPLOAD_MAX_MEMORY_SIZE = None


# Markdownx

MARKDOWNX_MARKDOWN_EXTENSIONS = [
    "markdown.extensions.extra",
    "markdown.extensions.admonition",
    "markdown.extensions.codehilite",
]

MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS = {
    "markdown.extensions.codehilite": {
        "css_class": "highlight",
        "use_pygments": True,
        "pygments_formatter": CustomHtmlFormatter,
    },
}


# Sentry - if its installed and we have a dsn in the environment

if environ.get("SENTRY_DSN"):
    with contextlib.suppress(ImportError):
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration

        sentry_sdk.init(
            dsn=environ.get("SENTRY_DSN"),
            integrations=[DjangoIntegration()],
            send_default_pii=True,
        )
