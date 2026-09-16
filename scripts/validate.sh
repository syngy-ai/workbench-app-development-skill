#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="${PROJECT_DIR}/skills/workbench-app-development"

python3 "${PROJECT_DIR}/scripts/validate_skill.py" "${SKILL_DIR}"
