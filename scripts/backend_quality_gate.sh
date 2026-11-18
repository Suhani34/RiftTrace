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
echo " RiftTrace Backend Quality Gate"
echo "======================================"
echo


cd "$BACKEND_DIR"


echo "[1/4] Django system check"
python manage.py check


echo
echo "[2/4] Database system check"
python manage.py check \
    --database default


echo
echo "[3/4] Migration consistency"
python manage.py makemigrations \
    --check \
    --dry-run


echo
echo "[4/4] Backend test suite"
python manage.py test


echo
echo "======================================"
echo " Backend quality gate passed"
echo "======================================"
