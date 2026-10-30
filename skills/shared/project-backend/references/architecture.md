> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Backend architecture

## Boundaries

Keep Phoenix modules thin: authenticate/authorize the request, normalize
transport params, call a domain API, and translate the result into navigation,
JSON, or form feedback. New business rules, Ecto composition, cross-record
invariants, audits, and external-effect decisions belong under `[APPLICATION_MODULE].*`.

A context may delegate to focused query, command, policy, resolver, or service
modules when behavior is substantial. Expose a small intention-revealing API;
avoid making callers reproduce a transaction sequence or know which tables,
caches, and workers implement it. Do not create a service layer that only
renames a single stable context call.

Prefer return values such as `{:ok, value}` and `{:error, reason | changeset}`
for recoverable operations. Bang functions are appropriate only when the caller
explicitly treats failure as exceptional. Keep pure normalization/calculation
separate from database and network effects so it can be tested directly.

## Schemas and PostgreSQL prefixes

[PROJECT_NAME] uses one `[APPLICATION_MODULE].Repo` with multiple PostgreSQL schemas. Every new
table-owning Ecto schema uses `[APPLICATION_MODULE].Schema, :schema_atom`, backed by
`[APPLICATION_MODULE].DatabaseSchemas`; do not hardcode a prefix in each runtime query or
rely on `public`/the connection search path.

Use the domain's registered schema atom and migration folder. Cross-schema
associations still need clear ownership. Avoid pushing cross-domain joins into
LiveViews; keep them in a query/context boundary and select only the fields the
caller needs.

Changesets cast an explicit allowlist, validate domain requirements, and attach
named database constraints. Add database `NOT NULL`, unique, foreign-key, and
check constraints when correctness must survive concurrent or non-web writes.
For a migration, follow the `project-engineering` skill: migration versions
are global across all approved folders.

## Organization scope and authorization

Treat `organization_id`, actor, and compiled access as part of the query/mutation
contract, not optional filters to add at the end. Scope first, then search, sort,
count, preload, or aggregate. Never fetch a record globally by browser-provided
id and authorize only after displaying or mutating it.

Use the existing authorization registry/policy and
`[APPLICATION_MODULE].Authorization.QueryScope` when its organization/department/team/
project/self model fits. With no permitted scope, return an empty query or a
forbidden result. Hiding a route, button, or field is not a server authorization
check. Permission bit values in the registry are stable identifiers and must not
be renumbered.

Platform-global operations must have an explicit platform/system-admin boundary.
Do not accept `:system` or an authorization bypass from ordinary request params;
reserve it for trusted internal callers and make that trust visible at the call
site.

## Queries and transactions

- Build composable queries, select only needed fields, and preload deliberately.
- Use stable ordering for pagination and enforce maximum page sizes.
- Whitelist dynamic fields/sorts; never call `String.to_atom/1` on client data.
- Avoid per-row queries and loading whole tables to count, filter, or paginate.
- Use `Ecto.Multi` when writes, state transitions, audit/outbox records, or
  idempotency markers must commit together.
- Keep HTTP, object storage, email, and other slow external I/O outside DB
  transactions. Commit an intent/job atomically, then perform the external work.
- Design webhook and retryable command paths around stable provider/idempotency
  keys and safe replay. A retry must not duplicate domain effects.

## Error and observability contract

Log enough identifiers to diagnose an operation (domain, organization, record,
job/provider) without secrets, access tokens, raw credentials, or sensitive raw
payloads. Translate internal failures into stable errors at the web boundary.
Do not expose changeset internals, exceptions, SQL, or provider responses to end
users. Preserve the original cause in structured logs or job metadata where the
existing subsystem supports it.
