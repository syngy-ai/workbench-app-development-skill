# Workbench App Development Skill

This repository is the editable source for the portable Agent Skill:

`workbench-app-development`

The skill guides Codex, Claude Code, and WorkBuddy when creating, extending, and deploying authenticated Syngy Workbench applications. All supported clients use the same canonical `SKILL.md`; the root README is installation and maintenance documentation for people, not the skill entry point.

## Compatibility

| Client | Personal skill directory | Install command |
| --- | --- | --- |
| Codex | `~/.codex/skills/workbench-app-development` | `./scripts/install-local.sh codex` |
| Claude Code | `~/.claude/skills/workbench-app-development` | `./scripts/install-local.sh claude` |
| WorkBuddy | `~/.workbuddy/skills/workbench-app-development` | `./scripts/install-local.sh workbuddy` |

Install for all three clients:

```bash
./scripts/install-local.sh all
```

The Codex destination respects `CODEX_HOME` when it is set. Claude Code and WorkBuddy use their standard directories under `HOME`.

After installation, start a new session or reload skills if the client does not detect the change immediately.

## Layout

- `skills/workbench-app-development/` — canonical portable skill package
- `skills/workbench-app-development/SKILL.md` — shared instructions and routing
- `skills/workbench-app-development/references/` — command contracts and acceptance scenarios
- `skills/workbench-app-development/agents/openai.yaml` — optional Codex UI metadata; other clients may ignore it
- `scripts/validate.sh` — validate the canonical package using the repository-local validator
- `scripts/install-local.sh` — install the package for one client or all clients
- `scripts/test.sh` — run repository unit and integration tests

## Validation and tests

Validate the skill package:

```bash
./scripts/validate.sh
```

Run all tests:

```bash
./scripts/test.sh
```

Installer tests use temporary home directories and do not write to the real `~/.codex/skills`, `~/.claude/skills`, or `~/.workbuddy/skills` directories.

## Development workflow

1. Edit files under `skills/workbench-app-development/`.
2. For behavior-changing edits, add or update a failing case in `references/acceptance-scenarios.md` before changing the skill.
3. Run `./scripts/test.sh` and `./scripts/validate.sh`.
4. Install the validated package with the appropriate client command or `./scripts/install-local.sh all`.
5. Start a new client session or reload its skill context before relying on the update.

Keep this repository as the source of truth. Avoid editing installed copies directly except for emergency inspection or rollback.
