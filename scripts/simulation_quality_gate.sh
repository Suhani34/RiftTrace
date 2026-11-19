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
echo "=========================================="
echo " RiftTrace Simulation Engine Quality Gate"
echo "=========================================="
echo


echo "[1/8] Engine architecture"

python \
    "$ROOT_DIR/scripts/check_simulation_engine_architecture.py"


echo
echo "[2/8] Python compilation"

cd "$BACKEND_DIR"

python -m compileall \
    -q \
    simulation_engine \
    simulations


echo
echo "[3/8] Simulation engine tests"

python manage.py test \
    simulation_engine.tests \
    -v 2


echo
echo "[4/8] Simulation Django tests"

python manage.py test \
    simulations


echo
echo "[5/8] Identity propagation tests"

python manage.py test \
    identities


echo
echo "[6/8] ATT&CK mapping tests"

python manage.py test \
    attack_mapping


echo
echo "[7/8] Business-impact tests"

python manage.py test \
    business


echo
echo "[8/8] Full backend regression"

python manage.py test


echo
echo "=========================================="
echo " Simulation engine quality gate passed"
echo "=========================================="
