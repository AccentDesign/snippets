FROM        accent/python-uvicorn-gunicorn:3.11-slim as base

ARG         ENVIRONMENT=production

WORKDIR     /app

COPY        ./pyproject.toml ./poetry.lock ./

RUN         pip install poetry \
            && poetry config virtualenvs.create false \
            && poetry install $(test "$ENVIRONMENT" = production && echo "--only main") --no-interaction --no-ansi \
            && rm -rf /root/.cache/pypoetry

FROM        base as final

ENV         PYTHONDONTWRITEBYTECODE=1
ENV         PYTHONFAULTHANDLER=1
ENV         PYTHONPATH=/app
ENV         APP_MODULE=app.asgi:app
ENV         WORKER_CLASS=app.asgi.DjangoUvicornWorker
ENV         DJANGO_MANAGEPY_MIGRATE=on
ENV         DJANGO_MANAGEPY_COLLECTSTATIC=on
ENV         DJANGO_SETTINGS_MODULE=app.settings
ENV         SECRET_KEY='***** change me *****'
ENV         ALLOWED_HOSTS=*
ENV         CSRF_TRUSTED_ORIGINS=http://*
ENV         RDS_HOSTNAME=db
ENV         RDS_PORT=5432
ENV         RDS_DB_NAME=postgres
ENV         RDS_USERNAME=postgres
ENV         RDS_PASSWORD=password
ENV         EMAIL_HOST=mail
ENV         EMAIL_PORT=1025
ENV         EMAIL_HOST_USER=user
ENV         EMAIL_HOST_PASSWORD=password

WORKDIR     /app

COPY        . .
