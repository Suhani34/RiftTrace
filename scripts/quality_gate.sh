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
echo " RiftTrace Complete Quality Gate"
echo "======================================"
echo


echo "[1/3] Backend quality"

"$ROOT_DIR/scripts/backend_quality_gate.sh"


echo
echo "[2/3] Simulation quality"

"$ROOT_DIR/scripts/simulation_quality_gate.sh"


echo
echo "[3/3] Frontend quality"

"$ROOT_DIR/scripts/frontend_quality_gate.sh"


echo
echo "======================================"
echo " All RiftTrace quality gates passed"
echo "======================================"
