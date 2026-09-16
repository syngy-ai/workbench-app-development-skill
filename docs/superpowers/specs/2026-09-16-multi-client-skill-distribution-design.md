# Multi-client Skill Distribution Design

Date: 2026-09-16
Status: Approved for implementation planning

## Context

The repository currently maintains one `workbench-app-development` skill and installs it only into Codex's personal skill directory. The skill itself already follows the shared Agent Skills structure: a `SKILL.md` entry point plus optional `references/` and client metadata.

Codex, Claude Code, and WorkBuddy can all consume this core structure. Their meaningful difference for this project is where personal skills are installed. Codex also consumes the optional `agents/openai.yaml` metadata; the other clients may ignore that file.

## Goals

- Keep one canonical copy of the skill instructions and references.
- Support local installation for Codex, Claude Code, and WorkBuddy.
- Make the supported clients and installation commands clear in the repository README.
- Preserve the existing Codex installation behavior when the `codex` target is selected.
- Validate the package before writing to any client directory.
- Test target selection without modifying a developer's real personal skill directories.

## Non-goals

- Publishing to a marketplace or registry.
- Creating separate, independently maintained copies for each client.
- Adding client-specific behavior to the Workbench development workflow.
- Installing or configuring Codex, Claude Code, or WorkBuddy themselves.
- Automatically installing to every client when no target was requested.

## Architecture

The existing directory remains the single source of truth:

```text
skills/
└── workbench-app-development/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    └── references/
        ├── acceptance-scenarios.md
        └── command-contracts.md
```

No `.claude/`, `.workbuddy/`, or duplicate `.agents/` source trees will be added. The installer copies this canonical directory to the selected clients. Relative links inside `SKILL.md` therefore resolve the same way in every client.

## Installer interface

`scripts/install-local.sh` accepts exactly one target:

```text
./scripts/install-local.sh codex
./scripts/install-local.sh claude
./scripts/install-local.sh workbuddy
./scripts/install-local.sh all
```

`--help` prints usage and exits successfully. Missing or unknown targets print usage and exit non-zero before any filesystem write.

The destination mapping is:

| Target | Destination |
| --- | --- |
| `codex` | `${CODEX_HOME:-$HOME/.codex}/skills/workbench-app-development` |
| `claude` | `$HOME/.claude/skills/workbench-app-development` |
| `workbuddy` | `$HOME/.workbuddy/skills/workbench-app-development` |
| `all` | All three destinations above |

The script resolves and validates the source directory first, runs `scripts/validate.sh` once, and only then creates destination directories and copies files. Re-running the same target is supported and refreshes the installed files. It reports each completed destination explicitly.

## Validation and testability

The current validator contains a machine-specific absolute path into one Codex installation. That dependency must be removed so a clone of this repository can be validated outside the original machine.

Validation will remain a repository command:

```text
./scripts/validate.sh
```

It will validate the shared Agent Skills requirements that matter to all three clients: readable `SKILL.md`, valid YAML frontmatter, matching `name`, non-empty `description`, and required referenced files. Codex-only UI metadata remains optional and is checked only when present.

Installer tests will run with an isolated temporary home directory. They will verify:

- each individual target writes only to its mapped directory;
- `all` writes to all three mapped directories;
- no argument and an invalid argument perform no installation;
- validation failure prevents every destination write;
- the installed package includes `SKILL.md`, `references/`, and `agents/openai.yaml`;
- repeated installation succeeds and refreshes changed source files.

Tests must not read from or write to the developer's actual `~/.codex`, `~/.claude`, or `~/.workbuddy` directories.

## Documentation

The root README will describe the project as a portable Agent Skill instead of a Codex-only personal skill. It will include:

- a compatibility table for Codex, Claude Code, and WorkBuddy;
- the canonical source directory;
- one installation command per client plus the `all` command;
- the exact destination directories;
- validation and update instructions;
- a note that `agents/openai.yaml` is Codex metadata and does not create a second skill implementation.

## Acceptance criteria

The change is complete when:

1. One canonical `SKILL.md` remains under `skills/workbench-app-development/`.
2. The repository validator runs without a user-specific absolute path.
3. The installer supports `codex`, `claude`, `workbuddy`, and `all` with safe argument handling.
4. Automated tests prove target routing and failure behavior in temporary directories.
5. The README accurately documents all supported clients and commands.
6. The existing Workbench behavior acceptance scenarios remain unchanged and the skill still validates.
