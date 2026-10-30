> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Components, tables, and states

## Component ownership

`[WEB_MODULE].CoreComponents` is a globally imported API. It currently owns
generic primitives such as `<.modal>`, `<.input>`, `<.table>`, labels, errors,
buttons, and user entries. A change to an attr default or rendered DOM can affect
unrelated pages, hooks, and tests. Preserve current call sites and defaults;
make new behavior opt-in unless the task intentionally requires a global change.

`[WEB_MODULE].LiveHelpers` is also broadly imported and contains older shared
presentation helpers, including `empty_state_base/1`. Focused reusable
LiveComponents/function components live under `lib/[WEB_DIRECTORY]/live/shared/`.
Search there and in the nearest feature's `components/` directory before adding
markup or a new module.

Promote a component to shared code only when its API is domain-neutral, at least
two real consumers need the same behavior, and ownership/lifecycle are clear.
Keep feature-specific copy, permissions, queries, and events with the feature.

## Table selection

Use the table pattern that matches the data and the surrounding feature:

- `<.table>` from `CoreComponents` is the generic small-table primitive and
  supports lists or LiveStreams, `row_id`, `row_click`, column slots, and action
  slots.
- `[WEB_MODULE].Live.Shared.ResponsiveColumnsTable` renders semantic desktop
  tables and stacked mobile cards. Use it when the same data must remain usable
  on narrow screens; provide one cell slot for every declared column.
- Existing admin pages often use explicit semantic table markup plus shared
  `<.actions>`. Match a nearby admin screen when its badges, mobile cards, and
  row actions form the established product language.
- A feature-specific virtualized table is a specialized virtualized, fixed-layout grid with strict
  scroll-performance invariants. Do not copy its structure or SCSS for ordinary
  tables. When changing it, preserve row/header height variables, shallow CSS
  selectors, stable `<colgroup>` widths, sticky offsets, and reduced-motion
  behavior.

For result sets that can grow, page at the database boundary. Do not fetch the
entire authorized set and use `Enum.slice/3` merely to render one page. Use a
stable deterministic order, compute the filtered total, preload in the query
layer, and prevent per-row database calls.

Keep real `<table>`, `<thead>`, `<th scope>`, `<tbody>`, and `<td>` semantics on
desktop table surfaces. Row actions need an accessible label; icon-only actions
need a title or `aria-label`. Ensure menus are not clipped by an ancestor's
overflow rules.

## Empty, loading, and error states

Choose state UI by intent:

- `empty_state_base/1` is the large, two-column onboarding/education state. It
  supports a tour/video area, eyebrow, headline, body, CTA slot, and dismissal.
  Use it when explaining how to start a feature, not for every empty table.
- `[WEB_MODULE].Live.Shared.PaginatedList.empty_state/1` is the compact state for
  selectors and bounded lists.
- A filtered table can use a small local message such as “No … match your
  filters,” ideally with a clear-filters action when filters are active.

Do not render empty UI until loading has completed. Distinguish:

1. no records exist yet — explain the value and offer an authorized creation CTA;
2. records exist but none match — mention search/filters and offer reset;
3. data failed to load — show an error and safe retry, not an empty state;
4. access excludes all rows — never imply that hidden records exist.

Hide CTAs the actor cannot perform. Keep empty-state wording specific to the
current scope and preserve the surrounding page's spacing on mobile and desktop.
