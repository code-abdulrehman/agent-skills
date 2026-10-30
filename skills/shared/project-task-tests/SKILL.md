---
name: project-task-tests
description: "Add, repair, and run focused unit and integration regressions for the current project’s backend, LiveView, controller, worker, and frontend behavior."
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

# [PROJECT_NAME] Task Tests

Treat relevant test coverage and actual execution as part of completing each
[PROJECT_NAME] implementation task. Keep verification scoped to the behavior changed.

## Choose meaningful coverage

- Inspect the current diff, existing tests, fixtures, project rules, `mix.exs`,
  test configuration, and any relevant frontend scripts before choosing commands.
- Add or fix unit tests for changed domain rules, parsing, validation, or hooks,
  and integration tests for the affected controller, LiveView, context/database,
  worker, or external-client boundary. Reuse existing helpers and test adapters.
- Reproduce a reported bug before fixing it when practical. Include success and
  failure behavior, persisted effects, and permission/tenant denial cases when
  the changed behavior crosses those boundaries. Verify that rejected requests
  leave data unchanged; hiding a button is not an authorization assertion.
- Avoid duplicate cases or tests that merely mirror markup or implementation.
  Purely visual or reversible low-impact changes may use existing component and
  interaction checks instead of adding artificial unit/integration layers. State
  which test category is inapplicable and why.
- Preserve meaningful assertions when updating stale fixtures, canonical routes,
  or async helpers. Do not skip failures or weaken assertions to produce green output.

## Execute locally

- Confirm dedicated localhost test database and local service configuration
  before any setup or mutation. Never use Production/Staging databases, real
  users, live mail delivery, or live OAuth. Use the repository's guarded runner
  when available and appropriate; inspect its database restrictions first.
- Run the task's unit and integration files, then directly affected regressions.
  Run relevant formatting and compilation checks. Run frontend tests when the
  changed behavior includes a JavaScript hook or frontend state.
- Default to task-specific suites. Run the full project suite only when the user
  explicitly requests it. Do not expand into unrelated failing features.
- Investigate failures and fix task-related defects or test setup. Report
  unrelated failures and blocked checks with evidence. Respect excluded features
  and preserve existing developer changes.

## Completion evidence

Provide copyable commands from the correct checkout, required local services and
environment settings without secrets, exact test files/cases added or updated,
actual pass/fail/exclusion counts, and any limitations. Distinguish automated
local evidence from manual browser checks and live environment verification.
Never mark an unexecuted check as passed. Keep changes uncommitted unless the
current user request authorizes committing; tests do not authorize deployment.
