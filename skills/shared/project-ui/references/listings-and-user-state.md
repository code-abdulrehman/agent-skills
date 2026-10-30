> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Listings, search, filters, and persisted UI state

## Search/filter pipeline

Treat a listing as one pipeline:

`actor + organization scope -> search/filter -> safe sort -> count/page -> preload -> render`

Apply authorization before returning rows or totals. Search across an explicit
set of fields, normalize whitespace/case deliberately, escape wildcard behavior
when literal matching is intended, and keep a stable secondary sort so paging
does not duplicate or skip rows. Map browser-provided sort columns, directions,
statuses, and actions through a finite whitelist or the shared safe helpers;
never call `String.to_atom/1` on client data.

Use `[WEB_MODULE].Shared.NewPaginationAndFilteration.search_sort_bar/1` and
`new_pagination_component/1` when the surrounding listing already uses that
contract. Preserve its event names and assigns. The class groups search and
filters responsively through the `ToolbarWrap` hook; do not insert a wrapper that
changes its measured control layout.

For popovers/selectors whose result set can grow, use
`[WEB_MODULE].Live.Shared.PaginatedList`. Its fetch callback receives
`(search, page, page_size)` and returns `{:ok, %{rows: rows, total: total}}`; it
must enforce authorization and organization scoping. Pass only plain values to
async tasks, drop superseded responses, and expose loading/error/retry states.

Any search or filter change resets to page one while keeping the chosen page
size. A clear-search action must use the same query path as search and restore a
valid total/window. Avoid N+1 queries and unbounded option loads.

## Decide where state lives

Use the URL for shareable/navigation state: search terms, selected filters,
sort, page, date range, and tabs when a bookmark should reproduce the view.
Normalize through `handle_params/3` and `push_patch`; an explicit URL always wins
over a saved preference.

Use `PreferredFilter` for an established listing preference such as page size or
the reports filter contract. Preserve its existing type key and merge behavior;
do not create a competing preference store.

Use `[APPLICATION_MODULE].UserStates` only for small, JSON-safe UI preferences that should
survive reloads for one user in one organization, such as drawer state,
page-scoped accordion/tab state, or scroll position. Never store domain records,
secrets, authorization decisions, unsanitized markup, or large result sets there.

User-state rules:

- A row is scoped by both `user_id` and `organization_id`; never read or write it
  by user alone when organization context exists.
- Page-scoped values live in `ModalAndTabsState.modal_params` under a stable path
  and string key. Read with `page_param/4`, providing a safe default, and write
  with `put_page_param/5` so sibling values are merged rather than replaced.
- Use the socket's assigned `:user_state`, falling back to
  `current_user_data.user_state` only where the established page does so.
- After a successful update, keep `socket.assigns.user_state`,
  `current_user_data.user_state`, and the scoped cache coherent. Reload before a
  cache write when the socket copy may be stale; otherwise one preference update
  can undo another.
- Skip no-op writes. Handle missing/legacy map values with defaults, and do not
  crash page rendering because preference persistence failed.

## Empty results and testing

Keep a way to distinguish the unfiltered total from the filtered result when the
UI needs different empty copy. Test URL precedence, clear/reset, filter changes
from later pages, stable ordering, no-result text, refresh/restoration, and two
organizations for the same user. For database-backed pagination, verify the
query actually uses `LIMIT`/`OFFSET` (or the project's cursor contract), not an
in-memory slice after an unbounded fetch.
