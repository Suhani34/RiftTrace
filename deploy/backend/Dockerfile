FROM python:3.12-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app


RUN apt-get update \
    && apt-get install -y \
        --no-install-recommends \
        gcc \
        libpq-dev \
    && rm -rf \
        /var/lib/apt/lists/*


COPY backend/requirements.txt \
    /tmp/requirements.txt

COPY backend/requirements-prod.txt \
    /tmp/requirements-prod.txt


RUN pip install \
        --no-cache-dir \
        --upgrade pip \
    && pip install \
        --no-cache-dir \
        -r /tmp/requirements-prod.txt


COPY backend/ /app/


RUN addgroup \
        --system \
        rifttrace \
    && adduser \
        --system \
        --ingroup rifttrace \
        rifttrace \
    && chown \
        -R \
        rifttrace:rifttrace \
        /app


USER rifttrace


EXPOSE 8000


CMD ["gunicorn", "config.wsgi:application", "--bind=0.0.0.0:8000", "--workers=2", "--timeout=60", "--graceful-timeout=30", "--error-logfile=-", "--capture-output"]
