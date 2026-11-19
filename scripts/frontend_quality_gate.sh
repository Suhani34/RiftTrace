#!/usr/bin/env bash

set -euo pipefail


ROOT_DIR="$(
    cd "$(
        dirname "${BASH_SOURCE[0]}"
    )/.."

    pwd
)"


FRONTEND_DIR="$ROOT_DIR/frontend"


echo
echo "======================================"
echo " RiftTrace Frontend Quality Gate"
echo "======================================"
echo


cd "$FRONTEND_DIR"


echo "[1/5] Direct backend URL check"

if grep -R -n \
    "http://127.0.0.1:8000" \
    src \
    --include="*.ts" \
    --include="*.tsx"
then
    echo
    echo "Direct backend URL found."
    exit 1
fi


echo
echo "[2/5] Router consistency"

if grep -R -n \
    "react-router-dom" \
    src \
    --include="*.ts" \
    --include="*.tsx"
then
    echo
    echo "react-router-dom usage found."
    exit 1
fi


echo
echo "[3/5] Editor temporary files"

TEMP_FILES="$(
    find src \
        -type f \
        \( \
            -name "*.swp" \
            -o -name "*.swo" \
            -o -name "*~" \
        \)
)"


if [ -n "$TEMP_FILES" ]; then
    echo "$TEMP_FILES"

    echo
    echo "Editor temporary files found."

    exit 1
fi


echo
echo "[4/5] ESLint"

npm run lint


echo
echo "[5/5] Production build"

npm run build


echo
echo "======================================"
echo " Frontend quality gate passed"
echo "======================================"
