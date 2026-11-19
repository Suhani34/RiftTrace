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
echo " RiftTrace Backend CI"
echo "======================================"
echo


cd "$BACKEND_DIR"


echo "[1/6] Django system check"

python manage.py check


echo
echo "[2/6] Database system check"

python manage.py check \
    --database default


echo
echo "[3/6] Migration consistency"

python manage.py makemigrations \
    --check \
    --dry-run


echo
echo "[4/6] Simulation architecture"

python \
    "$ROOT_DIR/scripts/check_simulation_engine_architecture.py"


echo
echo "[5/6] Full backend test suite"

coverage erase

coverage run \
    manage.py test


echo
echo "[6/6] Coverage report"

coverage report

coverage xml \
    -o coverage.xml


echo
echo "======================================"
echo " Backend CI passed"
echo "======================================"
