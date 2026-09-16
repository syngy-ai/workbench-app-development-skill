---
name: workbench-app-development
description: Use when creating, extending, publishing, or redeploying Syngy Workbench apps, especially with octopus-cli, Taskboard, Arcubase, or Workbench authentication.
---

# Workbench App Development

## Core contract

Use only the official Workbench React scaffold and `octopus-cli` for creation/deployment. Every app keeps `@syngy/workbench-auth`; optional features are business clients, never authentication switches.

Inspect repository instructions and target first. Never scaffold a non-empty app. For existing apps, inspect `package.json` and the facade, infer features, preserve custom/uncommitted work, and add only a required official client using its package manager and current official contract.

| Requirement | Feature |
| --- | --- |
| Authenticated Workbench UI only | empty |
| Octopus conversations or digital employees | `octopus` |
| Tasks or projects | `taskboard` |
| Persisted, shared, queryable records | `arcubase` |

Local TypeScript objects and static fixtures do not imply Arcubase.

## Arcubase decision

When Arcubase is required, stop before writes: the developer explicitly chooses an existing or new App.

- Existing: list Apps; require an explicit ID when candidates are ambiguous; inspect schema and stable keys; generate typed project code.
- New: present tables, fields, relations, and access model. Create through `octopus-cli arcubase-admin` only after that choice, then generate typed code.

Never guess an ID, match by name alone, or silently create storage.
Before writing datetime row values or defining `serialnumber` fields, read [Arcubase runtime gotchas](references/arcubase-runtime-gotchas.md).

## Workflow

Read [command contracts](references/command-contracts.md) before scaffolding, Arcubase work, or deployment.

1. Scaffold a safe empty target or inspect the existing app.
2. Use the generated authenticated facade; do not add a token store or standalone login.
3. Run relevant tests and production build; require `dist/index.html`.
4. Before team-scoped discovery (including Arcubase App list) and every external write, run `octopus-cli auth whoami --json`; verify profile, host, account, and team. On mismatch, stop with a copyable correction.
5. Create at most one first remote Workbench project, and only after the build. If its response is uncertain, use `coding projects list/show` to resolve it before any retry. Never introduce or write a hidden local project-ID mapping file. Later deployments use an explicit project ID or an unambiguous exact list result.
6. Publish the built directory and boundedly watch its task: `queued`/`processing` continue; `failed` stops immediately with `errorMessage` and action; `active` plus `workbenchUrl` succeeds. Successful handoff reports exactly `projectId`, `taskId`, `status=active`, `workbenchUrl`, verified `profile`, `host`, `team`; never substitute Arcubase `appId` or deployment/version/environment fields.

Direct HTTP, `kubectl`, GitHub Actions, copied scaffold, alternate publish, and remote archive/delete are outside this skill.

Every stop or failure must state the proven reason and a directly copyable next action. For an unsupported CLI flag, run that exact command’s current `--help`; never try legacy or guessed aliases.

## Skill improvement

Change this skill only when explicitly requested. Read [acceptance scenarios](references/acceptance-scenarios.md), reproduce the concrete gap before editing, make the smallest correction, validate it, and rerun the failing and affected scenarios. Do not add speculative compatibility or a changelog.
