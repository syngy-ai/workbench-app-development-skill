#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="${PROJECT_DIR}/skills/workbench-app-development"
VALIDATOR="/Users/nick/.codex/skills/.system/skill-creator/scripts/quick_validate.py"

if python3 -c 'import yaml' >/dev/null 2>&1; then
  python3 "${VALIDATOR}" "${SKILL_DIR}"
else
  uv run --with pyyaml python "${VALIDATOR}" "${SKILL_DIR}"
fi
