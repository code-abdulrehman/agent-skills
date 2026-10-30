---
name: project-backend
description: "Design and change the current Elixir/Phoenix project’s contexts, Ecto schemas and queries, transactions, authorization, caches, workers, and admin settings after discovering its existing architecture."
metadata:
  short-description: "[PROJECT_NAME] backend architecture conventions"
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

# [PROJECT_NAME] Backend

Keep domain behavior explicit, organization-scoped, testable, and independent
from the LiveView/controller that invokes it.

## Discover before designing

Trace the full current path: route/controller or LiveView, context/service,
schemas and prefixes, authorization policy/query scope, cache loader/invalidation,
workers/external clients, and focused tests. Check for an existing command,
query, resolver, or context API before adding a parallel path.

Do not infer architecture from a single legacy module. Prefer the conventions in
the nearest actively maintained domain, especially where it already encodes
authorization, audit, retry, or cache behavior.

## Load relevant guidance

- For module boundaries, Ecto schemas/prefixes, queries, authorization,
  transactions, and external side effects, read
  [references/architecture.md](references/architecture.md).
- For platform settings, organization settings, admin CRUD, typed resolution,
  status/lifecycle, seeds, and audit behavior, read
  [references/admin-settings.md](references/admin-settings.md).
- For cache keys/loaders, invalidation, PubSub, background work, and consistency,
  read [references/cache-and-jobs.md](references/cache-and-jobs.md).

If the task creates or changes a migration, also read
the installed `project-engineering` skill and follow its global migration-version rule.

## Required outcomes

- Web modules translate params and render results; context/service APIs own
  business validation, scoped queries, mutations, and side-effect decisions.
- Every data access path makes actor and organization scope explicit when the
  domain is not truly platform-global.
- Public APIs return intentional success/error shapes. Do not rescue broad
  exceptions into success or silently discard invariant failures.
- Database constraints back up changeset validation for uniqueness, references,
  and invariants subject to concurrency.
- Untrusted strings never become atoms or executable code. Secrets and raw
  provider payloads are redacted from logs and user-visible errors.
- Tests cover the domain boundary and negative authorization/organization case,
  not only the happy-path LiveView event.

## Verification

Run focused context/service/schema tests, then affected web or worker tests.
Format changed Elixir and HEEx files and run `git diff --check`. Run broader
compile/test checks in proportion to the shared surface; report build-lock,
database-capacity, or external-service limitations explicitly.
