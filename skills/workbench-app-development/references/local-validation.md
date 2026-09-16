# Local Validation Contract

Use local development against the selected Workbench environment before building or publishing. This is an acceptance stage, not proof that deployment may proceed.

## Prepare the local environment

Inspect `package.json`, the package-manager lockfile, generated facade, and declared scripts. Use only scripts and flags supported by the current project or their current `--help`; do not assume `npm test`, fixed routes, or a fixed port.

Run `octopus-cli auth whoami --json` before team-scoped discovery or any external write. Confirm the intended profile, host, account, and team. For the current official npm scaffold, start local development with the selected team:

```bash
WORKBENCH_REQUIRED_TEAM_ID=<teamId> npm run dev
```

Use the equivalent declared command for another package manager. Record the actual local URL. With no local Workbench session, a protected business route should enter the scaffold's supported dev login/JCode flow and return to that route after authorization; do not add an application-owned token store or login panel.

When an Arcubase-enabled scaffold declares `arcubase:codegen`, inspect its help first:

```bash
npm run arcubase:codegen -- --help
```

The current local JCode contract is:

```bash
npm run arcubase:codegen -- --app-id <appId> --team-id <teamId> --out src/arcubase
```

`--team-id` selects the Workbench team used for local authorization. Do not pass `--web-url`; the current codegen rejects it. If current help differs, use the documented current flags and update no command by guesswork. An environment with Arcubase admin credentials may instead use the `arcubase-admin dev sdk-gen` contract documented in [command contracts](command-contracts.md).

## Prove the real integration

Validate the routes and controls actually implemented by the app, not fixed example routes.

- Every app proves the authenticated viewer and selected team come from the intended Workbench environment.
- Each selected backend feature supplies visible state through its official client; static fixtures and local TypeScript objects are not integration evidence.
- Arcubase views render real backend rows from the selected App, or a true empty state and zero-derived counts when it returns no rows.
- Arcubase queries and actions use the generated typed ingress clients. Permission-sensitive controls use generated `can()` checks.
- A visible primary command must perform its named behavior, surface loading/backend errors, and refresh affected backend state after success; otherwise omit or disable it.

Use source evidence plus runtime evidence. SDK files or schema metadata alone prove only generation, not that the visible UI is connected.

## Protect real data

Real-environment validation is read-only by default. Implementing create/update behavior does not by itself authorize exercising it against real records.

Before a validation write, obtain authorization for the exact App and operation, rerun `octopus-cli auth whoami --json`, and use an approved test record or clearly identified test-data strategy. Never silently edit existing business records, create sample rows, or delete cleanup data. Apply [Arcubase runtime gotchas](arcubase-runtime-gotchas.md) to approved datetime or serial-number writes and read back the first write.

## Human acceptance gate

After agent-side validation, report:

- the local URL and how to complete or reuse JCode login;
- verified profile, host, account, and team;
- selected features and Arcubase `appId` when applicable;
- real-data evidence, exercised controls, and any skipped writes;
- unresolved errors or incomplete behavior.

Keep the dev server available while the environment supports it; otherwise give the exact restart command. Stop before the production build and remote project creation until the developer tests the app and explicitly approves publishing. If they reject it, iterate locally and present the same evidence again.

An original request that includes build, deploy, or publish authorizes the eventual goal but does not waive this checkpoint. Continue unattended only when the developer explicitly waives interactive local acceptance. Record that waiver and still complete agent-side local validation before building.
