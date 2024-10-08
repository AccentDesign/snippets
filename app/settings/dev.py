import sys
from os import environ

# Security

DEBUG = True


# database

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


# auth

AUTH_PASSWORD_VALIDATORS = []


# storage

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detail": {
            "format": (
                "%(levelname)s %(asctime)s %(pathname)s:%(lineno)s "
                "[%(funcName)s] %(message)s"
            )
        }
    },
    "handlers": {
        "stdout": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "detail",
            "stream": sys.stdout,
        }
    },
    "loggers": {
        "django": {
            "handlers": ["stdout"],
            "level": "INFO",
        }
    },
}
