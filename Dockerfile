FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.4.29 /uv /bin/uv

ARG ENVIRONMENT=prod

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONPATH=/app
ENV APP_MODULE=app.asgi:app
ENV WORKER_CLASS=app.asgi.DjangoUvicornWorker
ENV DJANGO_MANAGEPY_MIGRATE=on
ENV DJANGO_MANAGEPY_COLLECTSTATIC=on
ENV DJANGO_SETTINGS_MODULE=app.settings
ENV SECRET_KEY='***** change me *****'
ENV ALLOWED_HOSTS=*
ENV CSRF_TRUSTED_ORIGINS=http://*
ENV RDS_HOSTNAME=db
ENV RDS_PORT=5432
ENV RDS_DB_NAME=postgres
ENV RDS_USERNAME=postgres
ENV RDS_PASSWORD=password
ENV EMAIL_HOST=mail
ENV EMAIL_PORT=1025
ENV EMAIL_HOST_USER=user
ENV EMAIL_HOST_PASSWORD=password

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync \
    --frozen \
    --no-install-project \
    $(if [ "$ENVIRONMENT" = "prod" ]; then echo "--no-group dev"; fi)

ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
    --frozen \
    $(if [ "$ENVIRONMENT" = "prod" ]; then echo "--no-group dev"; fi)

ENV PATH="/app/.venv/bin:$PATH"

CMD ["/app/start.sh"]