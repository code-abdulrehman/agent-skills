---
name: project-engineering
description: "Change the current Phoenix project’s migrations, platform infrastructure, admin CRUD, seeds, and warning or notification infrastructure using its verified conventions."
metadata:
  short-description: "[PROJECT_NAME] platform and migration conventions"
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

# [PROJECT_NAME] engineering conventions

Use this skill for platform-infrastructure and migration work in the [PROJECT_NAME]
repository. It captures constraints that are easy to miss from generic Phoenix
conventions. Use `project-ui` for general interface work and
`project-backend` for general domain architecture.

## Migration workflow

Discover whether the project uses standard Ecto migration paths, multiple configured paths, or a custom migrator. Inspect its configured migration discovery before creating a version. A version must be unique across every path that the actual runner combines.

Before creating or renaming a migration:

1. Inspect the active project’s Mix aliases, migration configuration, and any custom migration runner.
2. Check for duplicate 14-digit versions across the entire `priv/repo/migrations` tree.
3. Use `mix ecto.gen.migration change_name --prefix <approved_prefix>`; the
   project alias rejects `--migrations-path`.
4. Confirm the generated version is unique globally.
5. Run `mix format` and `git diff --check`.

Do not manually copy a timestamp from another migration. A filename such as
20260909000000 is a version, not a timezone-aware date, and Ecto rejects the
same version even when the files are in different folders.

If the migration is new and unapplied, resolve a collision by changing only
the new migration to a unique version. Do not rename an existing migration that
may already have been applied in another environment.

Applied production migrations, including original CREATE TABLE files, are
immutable. This is a live product: change existing tables with safe, uniquely
versioned, forward-only migrations, backward-compatible rollouts and verified
rollback/recovery plans. Never reset, truncate, recreate or destructively modify
shared, staging or production data during routine implementation/verification.
Destructive diagnostics require an explicitly owned disposable database.

## Platform database and seeds

Platform-wide configuration belongs in the platform/system database and must
use the repository/schema conventions already present in the project. Keep
cross-database joins out of UI code; use a context/service boundary.

For system-defined warning rows, use an idempotent warning-only seed path when
the migration is intentionally schema-only. A seed must preserve admin-edited
content and status on reruns. Do not create per-user warning rows.

## Admin UI workflow

Before adding an admin page or modal, inspect existing Platform/System Admin
pages for authorization, route setup, table markup, modal lifecycle, and form
feedback. Reuse:

- core `<.form>` and `<.input>` components;
- the shared modal and `<.footer>` for modal actions;
- existing table/header/border/badge/toggle styles;
- shared `<.actions>` for row actions;
- existing verified `~p` routes and query/cache invalidation.

Server-side authorization is required even when the frontend route is hidden.
Do not introduce destructive delete actions when active/inactive state is the
existing safe lifecycle pattern.

## Warning system

Warnings have two separate sources:

- Database definition: slug, title, sanitized description, type, active state,
  priority, and safe action data.
- Application condition: a registered server-side evaluator keyed by slug.

Global warnings are returned when active. Conditional warnings are returned only
when their evaluator returns true. `active = false` always wins. Missing
definitions or evaluator failures must be logged safely and skipped, not exposed
as raw errors to users.

Use the existing applicable-warning service and evaluation context. Do not
duplicate conditional logic in the browser or React/UI layer, and do not add a
second banner component.

Actions must be structured data only. Registered actions use a whitelisted
application-side key; internal and external routes must pass safe URL checks.
Never put JavaScript, `eval`, `Function`, or executable strings in the database.

Rich descriptions must use the existing Quill/input and sanitizer pipeline.
Sanitize both at persistence and render/preview boundaries; never render raw
database HTML.

## Delivery checks

Use focused tests for the changed context/component, then run formatting and
diff checks. Compile/test output affected by a held Mix build lock, exhausted
database connections, or another unrelated process must be reported explicitly.
