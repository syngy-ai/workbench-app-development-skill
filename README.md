# Workbench App Development Skill

This project is the editable source for the personal Codex skill:

`workbench-app-development`

The installed personal skill currently lives at:

`~/.codex/skills/workbench-app-development`

## Layout

- `skills/workbench-app-development/` - skill source files
- `skills/workbench-app-development/SKILL.md` - main routing and workflow instructions
- `skills/workbench-app-development/references/` - detailed command contracts and acceptance scenarios
- `scripts/validate.sh` - validate the local skill package
- `scripts/install-local.sh` - copy this project version into the personal global skill directory

## Iteration Workflow

1. Edit files under `skills/workbench-app-development/`.
2. Run `./scripts/validate.sh`.
3. For behavior-changing edits, use the scenarios in `references/acceptance-scenarios.md` before installing.
4. Run `./scripts/install-local.sh`.
5. Start a new Codex task or reload skill context before relying on the updated installed skill.

Keep this project as the source of truth. Avoid editing `~/.codex/skills/workbench-app-development` directly except for emergency rollback or inspection.
