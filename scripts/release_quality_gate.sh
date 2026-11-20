#!/usr/bin/env bash

set -euo pipefail


ROOT_DIR="$(
    cd "$(
        dirname "${BASH_SOURCE[0]}"
    )/.."

    pwd
)"


echo
echo "======================================"
echo " RiftTrace v1.0 Release Quality Gate"
echo "======================================"
echo


VERSION_FILE="$ROOT_DIR/VERSION"


echo "[1/6] Release version"

if [ ! -f "$VERSION_FILE" ]; then
    echo "VERSION file is missing."
    exit 1
fi


VERSION="$(
    tr -d '[:space:]' \
        < "$VERSION_FILE"
)"


if [ "$VERSION" != "1.0.0" ]; then
    echo "Expected version 1.0.0."
    echo "Found: $VERSION"
    exit 1
fi


echo "Version: $VERSION"


echo
echo "[2/6] Frontend package version"

cd "$ROOT_DIR/frontend"


FRONTEND_VERSION="$(
    node -p \
        "require('./package.json').version"
)"


if [ "$FRONTEND_VERSION" != "$VERSION" ]; then
    echo "Frontend version mismatch."
    echo "VERSION: $VERSION"
    echo "Frontend: $FRONTEND_VERSION"
    exit 1
fi


echo "Frontend version: $FRONTEND_VERSION"


echo
echo "[3/6] Required documentation"

REQUIRED_FILES=(
    "README.md"
    "CHANGELOG.md"
    "docs/architecture.md"
    "docs/research-positioning.md"
    "docs/demo-guide.md"
    "docs/portfolio-summary.md"
    "docs/release-v1.0.0.md"
    "docs/release-checklist.md"
    "docs/testing-and-ci.md"
    "docs/production-deployment.md"
)


for file in "${REQUIRED_FILES[@]}"; do
    if [
        ! -f "$ROOT_DIR/$file"
    ]; then
        echo "Missing required file:"
        echo "$file"
        exit 1
    fi
done


echo "Required documentation found."


echo
echo "[4/6] Tracked-secret check"

cd "$ROOT_DIR"


if git ls-files \
    | grep -E \
        '(^|/)\.env$|(^|/)\.env\.prod$'
then
    echo
    echo "A real environment file is tracked."
    exit 1
fi


echo "No tracked real environment files."


echo
echo "[5/6] Git whitespace check"

git diff --check


echo
echo "[6/6] Complete quality gate"

"$ROOT_DIR/scripts/quality_gate.sh"


echo
echo "======================================"
echo " RiftTrace v1.0 release gate passed"
echo "======================================"
