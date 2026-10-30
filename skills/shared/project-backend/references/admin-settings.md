> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Admin and settings architecture

## Choose the setting scope

Before adding a setting, decide who owns it and who may change it:

- Platform/system setting: one value or definition for the installation. Use
  the platform infrastructure schema and the existing admin context/service.
- Organization setting: scoped by `organization_id`, with explicit inheritance
  from a platform default when the domain supports it.
- User setting: scoped by user and organization. UI-only preferences may belong
  in `UserStates` or `PreferredFilter`; business policy does not.
- App/integration setting: use the integration/app domain's existing credential,
  capability, or setting model. Never put secrets in generic global settings.

Do not add a second source of truth. Inspect `AdminGlobalSettings`, domain
resolvers such as `Integrations.RetentionSettings`, organization settings, and
existing seed paths before selecting storage.

## Treat values as typed contracts

`AdminGlobalSetting.value` is stored as a string, but consumers must not scatter
parsing and fallback logic. A domain resolver/service owns:

- accepted type, range, enum, or structured format;
- behavior for missing, inactive, malformed, or legacy values;
- safe application default;
- inheritance/override precedence;
- cache policy and change side effects.

The admin form and domain service validate the same contract; the service is the
authority. Do not use partial integer parses (`Integer.parse/1` with ignored
remainder) unless suffixes are explicitly valid. Keep setting slugs stable and
unique; changing a slug is a data migration/API compatibility decision.

Prefer a feature-specific facade (for example retention settings) when a value
has business effects, rather than calling `AdminGlobalSettings.get_*` from many
consumers. It should return a useful effective value and, when needed, its source
or revision so workers can make deterministic decisions.

## Admin UI and mutation flow

Admin routes are not a substitute for domain authorization. Keep the route's
existing platform-admin gate and enforce authorization again in sensitive
services when they can be called outside that route. Validate ids and params,
return controlled errors, and never turn a browser value into a new atom.

Use the existing lifecycle vocabulary when present (`active`, `disabled`,
`archived`) and prefer reversible activation/deactivation to deletion. A delete
needs explicit domain semantics for references, history, cache cleanup, and
audit. Preserve stable rows that other code addresses by slug.

After success, refresh the bounded list and invalidate/update relevant caches.
On failure, keep the submitted form and show field-level errors. For admin tables,
modals, filters, and actions, also follow the `project-ui` skill.

## Seeds, history, and runtime changes

Seeds must be idempotent and safe to rerun. Insert missing system definitions,
but do not overwrite admin-edited values, content, or active state unless the
task explicitly defines a forced upgrade. Schema belongs in migrations; default
definitions belong in the established seed path.

Audit security, retention, billing/quota, credential, destructive lifecycle,
and other operationally meaningful changes using the domain's existing audit
mechanism. Record actor, scope, before/after or revision, reason where required,
and outcome—without secrets.

When a worker's behavior depends on a mutable setting, decide explicitly whether
it resolves the latest value at execution time or snapshots a value/revision at
enqueue/start time. Preserve active-run cutoffs and other invariants already
documented by the domain.

## Tests

Cover missing/malformed values, boundary values, disabled/inherited state,
unauthorized actors, concurrent uniqueness where relevant, safe seed reruns, and
cache invalidation. A LiveView save test alone is insufficient for a setting
that controls backend behavior.
