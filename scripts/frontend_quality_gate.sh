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


echo "[1/7] Direct backend URL check"

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
echo "[2/7] Router consistency"

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
echo "[3/7] Editor temporary files"

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
echo "[4/7] Focused or skipped tests"

if grep -R -nE \
    '\.(only|skip)\(' \
    src \
    --include="*.test.ts" \
    --include="*.test.tsx"
then
    echo
    echo "Focused or skipped tests found."
    exit 1
fi


echo
echo "[5/7] Frontend tests"

npm test


echo
echo "[6/7] ESLint"

npm run lint


echo
echo "[7/7] Production build"

npm run build


echo
echo "======================================"
echo " Frontend quality gate passed"
echo "======================================"
