> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Cache, PubSub, and background work

## Cache contract

Use `[APPLICATION_MODULE].Cache.KeyBuilder` and choose the narrowest correct scope:
global, user, organization, or user+organization. Resource names are stable
lowercase strings with underscores. Do not hand-build keys at call sites.

A cache loader under `lib/[APPLICATION_DIRECTORY]/cache/data/loaders/` should keep these paths
separate:

- `get/...`: cache-first via the established hybrid cache;
- `load_...`: fresh database/domain read only;
- `put/...` and `invalidate/...`: explicit consistency operations;
- `cache_key/...`: one canonical scoped key shape.

If the value participates in the aggregated current-user payload, updater/
invalidator flow, or admin cache inspector, update the corresponding
`cached_data.ex`, `updater.ex`, `invalidator.ex`, and `db_resolver.ex` contracts.
Fresh resolver output must have the same shape as the cached value.

Never populate or invalidate a successful value before its database transaction
commits. Prefer invalidation when reconstructing the value is safer than
patching a potentially stale aggregate. User-state updates are especially prone
to lost updates: reload the scoped state before caching when the socket/worker
may hold an older copy.

## PubSub

Publish only after the authoritative write succeeds. Topic names and payloads
must identify the correct scope without leaking data across organizations. A
subscriber treats PubSub as a refresh/invalidation signal unless the subsystem
explicitly guarantees durable delivery; it must be able to recover state from
the database/cache after missed or duplicate messages.

Keep handlers idempotent and avoid broadcasting full sensitive records when ids
or revisions are enough. Add subscription cleanup/monitoring where a long-lived
process owns subscriptions.

## Jobs and external effects

Use Oban or the domain's existing supervised workflow for retryable, slow, or
external work. Job args contain JSON-safe identifiers and immutable intent—not
Ecto structs, sockets, functions, plaintext secrets, or huge provider payloads.
Reload and reauthorize/revalidate the authoritative state at execution time when
the domain requires it.

Define the idempotency boundary before enabling retries. Store stable external
ids, command receipts, or attempt state where the existing subsystem does so.
Classify errors into retryable and terminal outcomes; cap retries and surface a
diagnosable terminal state. Do not retry validation/authorization failures as if
they were transient network errors.

Keep network/object-storage/email calls outside database transactions. When a DB
change and external effect must stay coordinated, atomically write an intent or
enqueue a job with the domain mutation, then let the worker perform the effect.

## Tests

Test cache hit, miss, invalidation/update after success, no cache mutation after
failure, and scope isolation. For jobs, test duplicate execution, retryable vs
terminal errors, stale/missing records, and redaction. For PubSub, verify the
right scope receives a refresh and another organization does not.
