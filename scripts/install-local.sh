#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="${PROJECT_DIR}/skills/workbench-app-development"

usage() {
  echo "Usage: $0 codex|claude|workbuddy|all"
}

if [[ $# -eq 1 && ( "$1" == "--help" || "$1" == "-h" ) ]]; then
  usage
  exit 0
fi

if [[ $# -ne 1 ]]; then
  usage >&2
  exit 2
fi

case "$1" in
  codex|claude|workbuddy|all)
    target="$1"
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac

"${PROJECT_DIR}/scripts/validate.sh"

install_client() {
  local client="$1"
  local target_root
  local target_dir

  case "${client}" in
    codex)
      target_root="${CODEX_HOME:-${HOME}/.codex}/skills"
      ;;
    claude)
      target_root="${HOME}/.claude/skills"
      ;;
    workbuddy)
      target_root="${HOME}/.workbuddy/skills"
      ;;
  esac

  target_dir="${target_root}/workbench-app-development"
  mkdir -p "${target_root}"
  cp -R "${SOURCE_DIR}/." "${target_dir}/"
  echo "Installed workbench-app-development for ${client} at ${target_dir}"
}

if [[ "${target}" == "all" ]]; then
  install_client codex
  install_client claude
  install_client workbuddy
else
  install_client "${target}"
fi
