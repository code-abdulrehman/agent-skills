---
name: project-ui
description: "Create or change the current Phoenix project’s LiveView/HEEx UI, shared components, forms, tables, modals, responsive layouts, filters, pagination, and persisted UI preferences."
metadata:
  short-description: "[PROJECT_NAME] UI architecture and design rules"
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

# [PROJECT_NAME] UI

Build UI that looks and behaves like the surrounding [PROJECT_NAME] product and
reuses its established LiveView contracts.

## Start with the existing surface

Before editing, inspect the target LiveView/component, its template, adjacent
screens, tests, hooks, and styles. Search by component tag and event name, not
only by filename. Confirm which helpers are already imported through
`[WEB_MODULE]`; do not add aliases/imports that are already supplied.

Choose the smallest existing abstraction whose behavior matches the feature.
Do not generalize a feature-local component merely because another page has
similar markup. Conversely, do not copy a shared component's markup into a new
page just to make minor style changes.

## Load relevant guidance

- For `CoreComponents`, shared components, table selection, responsive design,
  actions, and empty states, read
  [references/components-and-states.md](references/components-and-states.md).
- For forms, inputs, validation, and any modal implementation, read
  [references/forms-and-modals.md](references/forms-and-modals.md).
- For search bars, filters, sorting, pagination, URL state, `PreferredFilter`,
  or `UserStates`, read
  [references/listings-and-user-state.md](references/listings-and-user-state.md).

Read more than one reference when the feature crosses those concerns.

## Cross-cutting requirements

- Use verified `~p` routes and LiveView navigation primitives. Preserve query
  parameters that are part of the current view contract.
- Keep all authorization and organization scoping on the server; conditional
  rendering only improves the interface.
- Reuse the existing color, spacing, button, badge, typography, focus, and
  breakpoint conventions near the target surface.
- Keep DOM ids stable and unique. Hooks, streams, `phx-target`, focus handling,
  and tests depend on them.
- Every control needs an accessible name. Preserve keyboard interaction, focus
  containment, Escape/click-away behavior, disabled states, and useful loading
  feedback.
- Make the disconnected render safe. Do not assume an async result, hook, or
  client event already ran.
- Do not introduce browser-only business rules, executable database content,
  or client-generated atoms.

## Verification

Run focused LiveView/component tests and `mix format` on changed `.ex`/`.heex`
files, then `git diff --check`. For meaningful layout or interaction changes,
inspect both a narrow and wide viewport and exercise empty, loading, error, and
populated states where applicable.
