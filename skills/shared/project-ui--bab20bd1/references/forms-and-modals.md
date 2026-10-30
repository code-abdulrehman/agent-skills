> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Forms, inputs, and modals

## Inputs and validation

Prefer `<.form>` with `to_form(changeset)` and
`<.input field={@form[:field]}>` for new LiveView forms. The core input supports
the established text, textarea, select, checkbox/toggle, currency, date/time,
inline, and specialized variants. Use a custom native input only when the shared
API cannot express the interaction.

Required indicators and placeholders are centralized in
`[WEB_MODULE].InputDefaults` and applied by both `CoreComponents.input/1` and
legacy `FormHelpers`:

- Pass `required` when native browser validation should also apply.
- A changeset-required field can receive the visual `*` automatically without
  changing browser submission behavior.
- Never type `*` or `(optional)` into new labels. Do not write “Optional …” in a
  placeholder. Select prompts such as “No project” can express an optional
  choice.
- Explicit placeholders win; otherwise the component derives one from the label
  or field name. Placeholderless input types stay placeholderless.
- `hide_label` is only for compact controls whose accessible name is supplied
  another way, such as `aria-label`.

Build a pristine initial changeset with `action == nil`. On `phx-change`, rebuild
from submitted params and set `action: :validate`. On a failed final save, use
the returned changeset/action so all relevant errors render. Put cross-field or
settings-driven failures on the correct field with `add_error/3`; do not collect
field errors in a detached paragraph.

Derive submit-disabled state from the same validation contract that produces
errors. Keep `phx-disable-with`, do not trust client validation at the context
boundary, and reset transient form state when a modal closes unless draft
persistence is an explicit requirement.

## Choose one modal lifecycle

This repository contains three modal mechanisms. Follow the target feature's
existing lifecycle; do not mix close/open events from different systems.

1. `[WEB_MODULE].LiveModal` is the application LiveView modal host. Parents call
   `open_modal/3`; content is a LiveComponent, closes through `close_modal/1` or
   the host's `"modal"` event, and commonly imports `close_x/1` and `footer/1`.
   Use it for parent-owned create/edit flows that already render the `live_modal`
   host. Pass an explicit footer spacer class such as `class="pt-6"`; its legacy
   default is intentionally large.
2. `<.modal>` from `CoreComponents` is a function component driven by `show`,
   `on_cancel`, and `show_modal/2`/`hide_modal/2` JS commands. It supplies dialog
   semantics, focus wrapping, Escape, and click-away behavior. Use it where the
   state already belongs to the current LiveView/template.
3. `[WEB_MODULE].ModalComponent` is a legacy patch-navigation wrapper. Preserve
   it on existing routes, but do not introduce it into a feature already using
   one of the other systems.

For `LiveModal` content, match nearby the relevant feature forms: a bounded scrollable
`.modal`, responsive padding, a clear heading, `<.form class="space-y-6">`,
responsive field grids, and full-width mobile buttons. Use the shared footer and
close control. A non-closable modal must be deliberate; its completion or escape
path must be clear.

After a successful mutation, close the modal, notify the parent with a specific
message, and refresh only the affected collection/cache. On failure, keep the
modal open with the returned form state. Do not reload the page to clear errors.

## Regression checks

- Open create and edit flows: no errors before interaction and no stale state
  after reopen.
- Submit empty/invalid data, then correct it: errors and disabled state update
  without a reload.
- Exercise Cancel, close button, Escape, and click-away according to `closable`.
- Confirm focus stays within the dialog and returns to a sensible trigger.
- Check narrow-screen scrolling, field spacing, sticky actions, and on-screen
  keyboard behavior.
