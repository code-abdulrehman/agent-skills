---
name: project-manual-qa
description: "Perform focused browser QA for the current project using available browser tools, isolated local test identities, role and tenant checks, sanitized evidence, and targeted regressions."
---

## Resolve the active project first

`[PROJECT_NAME]`, `[PROJECT_PATH]`, `[APPLICATION_MODULE]`, and `[WEB_MODULE]` are documentation placeholders. Determine their real values from the active workspace every time this skill is invoked; never treat them as literal commands, identifiers, or directory names. Use `git rev-parse --show-toplevel` when inside Git, otherwise the user-selected workspace. For an umbrella project, identify the actual application before editing. Inspect `mix.exs`, configuration, source modules, and applicable `AGENTS.md`/local instructions to find the application module, web namespace, test runner, schema conventions, and real paths. Do not derive a module name merely by capitalizing a directory name.

Use runtime variables in executable commands: set `PROJECT_PATH` to the verified workspace, `PROJECT_NAME` to its discovered name, `SKILL_DIR` to this installed skill, and `SKILLS_ROOT` to its containing installation directory. Validate required settings without printing secret values:

```sh
: "${PROJECT_PATH:?Set PROJECT_PATH to the verified active workspace}"
: "${SKILL_DIR:?Set SKILL_DIR to this installed skill directory}"
cd "$PROJECT_PATH"
```

The framework examples below describe possible implementations, not facts about another project. Resolve every named module, component, route, directory, service, feature, setup alias, and role against current source before using it. If a helper, registry, schema system, preference store, modal implementation, or warning engine is absent, retain the underlying behavior through the project’s existing equivalent; do not create the old architecture just to satisfy an example. Apply framework-specific rules only when that framework is actually used. Unrelated architectures require their own established implementation and test commands.

Find companion skills by metadata name in the active agent’s installed skill directories; do not assume `.codex/skills` exists in the project. Read project-owned documentation only when it is present, then verify it against source. Do not create missing policy from an old sample.

Keep actual local paths, task/session IDs, identity mappings, tokens, private URLs, environment values, and customer data out of public reports, examples, screenshots, generated prompts, and committed coordination files. Store runtime manifests and audit evidence locally with restrictive permissions; publish only reviewed, neutral examples. A task’s existing authorization and current project instructions take precedence over sample workflow approval defaults.

# [PROJECT_NAME] manual QA

Use this skill for a focused workflow or a full browser regression. The scope is set by the user's task; do not claim full coverage from a smoke test. Start in the requested checkout, read its `AGENTS.md`, `.codex/rules.md`, and `docs/git-worktree-workflow.md`, and preserve all local changes. Discover the actual app URL, startup command, test runner, browser tools, and service state before acting. Prefer an existing running server. Inspect test configuration before database work. Never use production or staging data, real email delivery, or live OAuth credentials for QA.

## Browser setup and execution

Read [browser-test-protocol.md](references/browser-test-protocol.md) before browser work. Discover current Orca/Codex browser tools first; use an existing repository browser runner or a locally installed browser automation fallback only when supported. Record which operations were actually possible. Use a visible browser for visual, responsive, keyboard, modal, and navigation checks; use isolated headless contexts for repeatable role and negative checks. Never borrow a person's browser cookies or report secrets. Set up dedicated local test identities and organizations through existing fixtures or authorized local flows; isolate each role's browser context. The bundled CDP fallback requires a dedicated temporary browser profile and debugging port per role, shares that profile's cookies, and closes its own tab after every run. Review its trusted actions, output limits and screenshot redactions in the protocol before invoking it.

Inventory actual controls and routes at runtime. For each important action, record role, account and membership state, input, expected result, observed UI, persisted effect, network/console result, viewport, and evidence path. Use [lifecycle-and-role-matrix.md](references/lifecycle-and-role-matrix.md) for lifecycle, permissions, multi-organization, historical data, and applicable team assignment cases. A visible or disabled button alone is not proof that the server denies forged requests.

## Bug loop and verification

Use [bug-triage-and-report.md](references/bug-triage-and-report.md) to reproduce, capture sanitized evidence, trace UI to authorization and storage, apply the smallest safe fix, run focused context and LiveView/API tests, and repeat the browser action. Read `project-task-tests` plus relevant UI/backend skills before code changes. Classify each result as passed, failed, fixed and browser retested, blocked, or not tested. Separate browser evidence from automated test evidence. Do not mark a fix browser verified until its original interaction was repeated.

Coordinate shared test databases and Mix build outputs. Use the repository's guarded test runner only after inspecting it; isolate or serialize PostgreSQL and Redis test work. Check formatting, `git diff --check`, test results, and Git status. Preserve all unrelated files. Never stage, commit, push, merge, reset, clean, or deploy unless the active user request explicitly authorizes it. Seek approval before migrations, destructive data changes, new business rules, or production/staging access.

## Invocation

For a focused run: `Use $project-manual-qa to verify <workflow> in <worktree>.` For a broad run: `Use $project-manual-qa for a regression of the approved task across lifecycle, roles, resources, and reports.` In the final report, list exact executable test commands, browser capabilities used, evidence, uncovered cases, blockers, and a verdict that matches actual coverage.
