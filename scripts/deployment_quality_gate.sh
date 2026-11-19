#!/usr/bin/env bash

set -euo pipefail


ROOT_DIR="$(
    cd "$(
        dirname "${BASH_SOURCE[0]}"
    )/.."

    pwd
)"


BACKEND_DIR="$ROOT_DIR/backend"


echo
echo "======================================"
echo " RiftTrace Deployment Quality Gate"
echo "======================================"
echo


echo "[1/5] Production Python compilation"

cd "$BACKEND_DIR"

python -m compileall \
    -q \
    config \
    api


echo
echo "[2/5] Production Django check"

DJANGO_SETTINGS_MODULE=config.settings_prod \
DJANGO_SECRET_KEY=rifttrace-production-check-secret-key-12345678901234567890 \
DJANGO_ALLOWED_HOSTS=rifttrace.example.com \
DJANGO_CSRF_TRUSTED_ORIGINS=https://rifttrace.example.com \
POSTGRES_DB=rifttrace \
POSTGRES_USER=rifttrace \
POSTGRES_PASSWORD=deployment-check-password \
POSTGRES_HOST=127.0.0.1 \
POSTGRES_PORT=5432 \
DJANGO_SECURE_SSL_REDIRECT=true \
DJANGO_SESSION_COOKIE_SECURE=true \
DJANGO_CSRF_COOKIE_SECURE=true \
DJANGO_HSTS_SECONDS=31536000 \
python manage.py check \
    --deploy


echo
echo "[3/5] Migration consistency"

python manage.py makemigrations \
    --check \
    --dry-run


echo
echo "[4/5] Docker Compose validation"

cd "$ROOT_DIR"

RIFTTRACE_ENV_FILE=.env.prod.example \
docker compose \
    -f docker-compose.prod.yml \
    config \
    >/dev/null


echo
echo "[5/5] Secret-file protection"

if git ls-files \
    | grep -E \
        '(^|/)\.env\.prod$'
then
    echo
    echo ".env.prod is tracked by Git."
    exit 1
fi


echo
echo "======================================"
echo " Deployment quality gate passed"
echo "======================================"
