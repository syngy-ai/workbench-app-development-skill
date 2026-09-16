# Multi-client Skill Distribution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the canonical `workbench-app-development` Agent Skill installable and verifiable for Codex, Claude Code, and WorkBuddy without duplicating its source.

**Architecture:** Keep `skills/workbench-app-development/` as the only skill package. Add repository-local Python validation, a target-aware Bash installer, and standard-library integration tests that run against temporary home directories. Document each supported client and command in the root README.

**Tech Stack:** Bash, Python 3 standard library, `unittest`, Agent Skills `SKILL.md` format.

---

## File map

- Create `scripts/validate_skill.py`: validate the repository's portable Agent Skills package without referring to an installed Codex copy.
- Modify `scripts/validate.sh`: call the repository-local validator.
- Modify `scripts/install-local.sh`: parse the client target, validate once, and copy the canonical package to mapped destinations.
- Create `scripts/test.sh`: run every repository test with one command.
- Create `tests/test_validate_skill.py`: exercise valid and invalid skill packages.
- Create `tests/test_install_local.py`: exercise client routing, no-write failures, package completeness, and refresh behavior in temporary homes.
- Create `tests/test_readme.py`: ensure published installation examples remain aligned with the installer interface.
- Modify `README.md`: describe the portable package, supported clients, installation, validation, testing, and update workflow.

### Task 1: Portable skill validation

**Files:**
- Create: `tests/test_validate_skill.py`
- Create: `scripts/validate_skill.py`
- Modify: `scripts/validate.sh`

- [ ] **Step 1: Write validator tests against temporary package copies**

Create `tests/test_validate_skill.py` with tests that copy `skills/workbench-app-development` into a temporary directory and invoke `scripts/validate_skill.py`. Cover a valid package, a frontmatter name that does not match the directory, a missing description, a missing `references/command-contracts.md`, and incomplete optional `agents/openai.yaml` metadata.

The subprocess helper must capture output and assert both exit status and an actionable error fragment. No test may modify the canonical skill directory.

- [ ] **Step 2: Run the validator tests to verify RED**

Run:

```bash
python3 -m unittest tests.test_validate_skill -v
```

Expected: FAIL because `scripts/validate_skill.py` does not exist.

- [ ] **Step 3: Implement the repository-local validator**

Create `scripts/validate_skill.py` using only the Python standard library. It must:

- accept exactly one skill directory argument;
- require a readable `SKILL.md` beginning with a closed YAML frontmatter block;
- extract one-line `name` and `description` scalars used by this repository;
- require the name to match the parent directory and the Agent Skills naming pattern;
- enforce a non-empty description of at most 1024 characters;
- require `references/acceptance-scenarios.md` and `references/command-contracts.md`;
- when `agents/openai.yaml` exists, require `interface`, `display_name`, `short_description`, and `default_prompt` keys;
- print `Skill is valid: <path>` on success and `Validation error: <reason>` to stderr on failure.

Modify `scripts/validate.sh` to resolve `PROJECT_DIR`, set `SKILL_DIR`, and run:

```bash
python3 "${PROJECT_DIR}/scripts/validate_skill.py" "${SKILL_DIR}"
```

This removes the `/Users/nick/.../quick_validate.py` dependency.

- [ ] **Step 4: Run validator tests and the public validation command**

Run:

```bash
python3 -m unittest tests.test_validate_skill -v
./scripts/validate.sh
```

Expected: all validator tests pass and the command prints `Skill is valid` for the canonical package.

- [ ] **Step 5: Commit the portable validator**

```bash
git add scripts/validate.sh scripts/validate_skill.py tests/test_validate_skill.py
git commit -m "test: add portable skill validation"
```

### Task 2: Target-aware local installation

**Files:**
- Create: `tests/test_install_local.py`
- Modify: `scripts/install-local.sh`

- [ ] **Step 1: Write installer integration tests**

Create `tests/test_install_local.py` with a helper that runs the installer under a per-test temporary `HOME`, removes `CODEX_HOME` from the subprocess environment, and inspects only that temporary directory.

Test these mappings independently:

```text
codex     -> $HOME/.codex/skills/workbench-app-development
claude    -> $HOME/.claude/skills/workbench-app-development
workbuddy -> $HOME/.workbuddy/skills/workbench-app-development
all       -> all three destinations
```

Also verify that:

- `--help` succeeds without creating a client directory;
- no argument, an extra argument, and an unknown target fail without creating a client directory;
- deleting `SKILL.md` from a temporary project copy makes installation fail before any write;
- installed output contains `SKILL.md`, both reference files, and `agents/openai.yaml`;
- changing a source file in a temporary project copy and reinstalling refreshes the installed file.

- [ ] **Step 2: Run installer tests to verify RED**

Run:

```bash
python3 -m unittest tests.test_install_local -v
```

Expected: FAIL because the current installer ignores client targets and only installs into the Codex directory.

- [ ] **Step 3: Implement target parsing and destination routing**

Update `scripts/install-local.sh` to:

1. Resolve `PROJECT_DIR` and `SOURCE_DIR`.
2. Print a usage function containing `codex|claude|workbuddy|all`.
3. Handle `--help` and `-h` before validation or writes.
4. Reject missing, extra, or unknown arguments with exit code 2.
5. Run `scripts/validate.sh` exactly once before creating any destination.
6. Map `codex` through `${CODEX_HOME:-${HOME}/.codex}` and map the other clients through `$HOME`.
7. Copy the canonical package contents into every selected destination.
8. Print one `Installed workbench-app-development for <client> at <path>` line per destination.

Keep the copy operation idempotent and scoped to the exact `workbench-app-development` destination.

- [ ] **Step 4: Run installer and validator tests**

Run:

```bash
python3 -m unittest tests.test_validate_skill tests.test_install_local -v
```

Expected: every test passes; all test writes remain under temporary directories.

- [ ] **Step 5: Commit the multi-client installer**

```bash
git add scripts/install-local.sh tests/test_install_local.py
git commit -m "feat: install skill for multiple clients"
```

### Task 3: User documentation and unified test entry point

**Files:**
- Create: `tests/test_readme.py`
- Create: `scripts/test.sh`
- Modify: `README.md`

- [ ] **Step 1: Write the documentation contract test**

Create `tests/test_readme.py` to read `README.md` and require these exact public commands:

```text
./scripts/install-local.sh codex
./scripts/install-local.sh claude
./scripts/install-local.sh workbuddy
./scripts/install-local.sh all
./scripts/validate.sh
./scripts/test.sh
```

Also require the README to name `~/.codex/skills`, `~/.claude/skills`, and `~/.workbuddy/skills`.

- [ ] **Step 2: Run the documentation test to verify RED**

Run:

```bash
python3 -m unittest tests.test_readme -v
```

Expected: FAIL because the README currently documents only the Codex installation workflow.

- [ ] **Step 3: Rewrite the README for the shared package**

Update `README.md` with:

- a portable Agent Skill overview;
- a compatibility table for Codex, Claude Code, and WorkBuddy;
- the canonical package layout;
- separate installation commands plus `all`;
- exact destination paths;
- a note that `agents/openai.yaml` is optional Codex metadata;
- validation, test, update, and development workflow commands.

Do not tell tools to load the root README as instructions; state that clients discover the installed `SKILL.md`.

- [ ] **Step 4: Add and run the unified test command**

Create executable `scripts/test.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_DIR}"
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Run:

```bash
./scripts/test.sh
./scripts/validate.sh
```

Expected: every unit and integration test passes; skill validation succeeds.

- [ ] **Step 5: Commit documentation and test entry point**

```bash
git add README.md scripts/test.sh tests/test_readme.py
git commit -m "docs: document multi-client skill installation"
```

### Task 4: Final regression verification and delivery

**Files:**
- Verify: all changed files
- Verify unchanged: `skills/workbench-app-development/SKILL.md`
- Verify unchanged: `skills/workbench-app-development/references/acceptance-scenarios.md`

- [ ] **Step 1: Run complete automated verification**

Run:

```bash
./scripts/test.sh
./scripts/validate.sh
git diff --check origin/main...HEAD
```

Expected: all tests pass, validation succeeds, and `git diff --check` emits no output.

- [ ] **Step 2: Confirm the canonical skill content did not drift**

Run:

```bash
git diff --exit-code origin/main...HEAD -- \
  skills/workbench-app-development/SKILL.md \
  skills/workbench-app-development/references/acceptance-scenarios.md
```

Expected: exit code 0 and no output.

- [ ] **Step 3: Review repository state and commits**

Run:

```bash
git status --short --branch
git log --oneline origin/main..HEAD
```

Expected: a clean `main` branch ahead of `origin/main` only by the plan and implementation commits.

- [ ] **Step 4: Push after local verification**

Run:

```bash
git push origin main
git fetch origin main --quiet
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
```

Expected: push succeeds and local `HEAD` equals `origin/main`.
