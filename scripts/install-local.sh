#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="${PROJECT_DIR}/skills/workbench-app-development"
TARGET_ROOT="${CODEX_HOME:-${HOME}/.codex}/skills"
TARGET_DIR="${TARGET_ROOT}/workbench-app-development"

"${PROJECT_DIR}/scripts/validate.sh"
mkdir -p "${TARGET_ROOT}"
cp -R "${SOURCE_DIR}/." "${TARGET_DIR}/"

echo "Installed workbench-app-development skill to ${TARGET_DIR}"
