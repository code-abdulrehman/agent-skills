> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Browser test protocol

1. Verify worktree/branch, local server response, PostgreSQL and Redis readiness, test runner, mail adapter, and browser integration. Record browser name/version and headed/headless features actually available. Do not invent tool commands.
2. Use a fresh named profile/context for each role and origin. Keep `localhost` and `127.0.0.1` distinct; cookies do not cross those hosts. Never import the user's browser profile or reveal cookies, tokens, passwords, OTPs, or private reasons.
3. Create or reuse only dedicated local QA accounts and organizations. Inspect local mail capture or test adapter before invitation/OTP actions. Skip external OAuth without a configured sandbox identity. Record any unavailable identity as blocked.
4. In the visible browser, navigate the real route, inspect populated/empty/error states, click every in-scope control, test keyboard focus and modal behavior, and inspect desktop/tablet/mobile viewports. Capture sanitized screenshots when they prove a defect or result.
   For Phoenix LiveView workflows, wait for `[data-phx-main].phx-connected` before interacting and again after navigation. After a click navigates, first wait for a destination-specific control: the previous page's connected element can otherwise satisfy the check before navigation finishes. A rendered initial HTML page does not establish that event handlers are connected.
5. In headless automation, repeat high-risk paths with isolated contexts: valid role, restricted role, stale session, forged resource ID, and cross-tenant ID. Check response status, redirects, LiveView behavior, console errors, network failures, and persisted state. Expected 403/401 denials are successful security checks when no data leaks or mutations occur.
6. For each action, record route, role/status, control name, steps, expected/actual, HTTP or LiveView result, screenshot/trace path, and retest status. Never equate source inspection, HTTP-only probes, or an automated Phoenix test with visible browser verification.
7. If a browser control tool is absent, use only installed approved local alternatives. Report exactly which visible/headless capabilities remain unavailable; continue safe HTTP, LiveView, and source tests while seeking the missing capability or identity.
   For the installed global fallback, read the helper usage below. Use a separate temporary Chrome profile and CDP port for each role; a new tab shares its profile's cookies. Never connect this helper to a person's normal Chrome profile.
8. Use temporary local profiles and bounded test data. Clean up only data created during this run and only through reversible supported local paths; keep evidence needed for reproduction. Do not delete shared or pre-existing data.

## Local CDP fallback

Discover installed Chrome and an unused local CDP port first. The operator must start Chrome with a dedicated temporary `--user-data-dir` and loopback debugging port for this role. Keep that profile and port separate from other QA roles and the person's browser. The helper does not create an isolated browser context: `--dedicated-profile` confirms this prerequisite. The helper opens one tab and closes only that tab in `finally`, including action failures. It leaves the browser process/profile intact for subsequent same-role runs; its cookies persist until the operator removes that temporary profile. Close only browser processes and profiles created for this QA run after preserving necessary evidence.

If a dedicated headless browser stalls on input or screenshots while backgrounded, record the failure and retry its launch with `--disable-background-timer-throttling --disable-renderer-backgrounding --disable-backgrounding-occluded-windows`. Record the actual launch settings and rerun the original action; a timeout remains unverified until the action succeeds.

Run from any checkout with a Node version providing native `fetch` and `WebSocket` (Node 22 or later):

```bash
node "$HOME/.codex/skills/project-manual-qa/scripts/local_cdp_qa.mjs" \
  <role-CDP-port> <actions.json> --dedicated-profile
```

Use a trusted local JSON action array. The script caps a run at 200 actions and approximately two minutes, individual waits at 20 seconds, pauses at five seconds, and connection/cleanup requests at five seconds. Browser commands also have timeouts. An action failure returns nonzero with its zero-based index; raw page errors, expressions and private values are withheld. Successful completion means the supplied actions/assertions ran; inspect `browserDiagnostics` separately and judge each status against the intended result. A cleanup failure also returns nonzero.

Supported actions:

| `op` | Fields | Notes |
| --- | --- | --- |
| `httpBasic` | `origin`, `usernameEnv`, `passwordEnv` | Optional; configure once before navigation. Origin must be explicit local HTTP(S), without path, query, fragment or URL credentials. Credentials are read from environment variables and supplied only to Basic Auth challenges at that exact origin. |
| `navigate` | `url` | Explicit navigation requires local HTTP(S), without URL credentials. Waits for the new document's load event. |
| `navigateCurrentOrg` | strict path `suffix`, optional plain object `query` | Derives `/a/<account>/o/<organization>` from the current local page. Query values may be strings, finite numbers, booleans or null (serialized as `null`); arrays/nested objects are rejected. Encodes keys/values with `URLSearchParams`; retains the current origin and omits queries from diagnostics. |
| `waitFor` | `selector`, optional `timeoutMs` | Waits for an element; use it after actions that change the page or navigate. |
| `fill` | `selector`, `valueEnv` or public `value` | Read every private input, including passwords and OTPs, from an environment variable. Password fields require `valueEnv`. Never place credentials in action files or command arguments. |
| `click` | `selector`, optional `defer` | Calls the DOM click method and rejects disabled targets. `defer: true` schedules the click so a following explicit `handleDialog` can resolve a synchronous native dialog. Wait for the resulting UI condition after a deferred click. It does not prove native pointer, keyboard, focus, or visual behavior. |
| `handleDialog` | explicit boolean `accept`, optional `ifPresent`, `timeoutMs` | Accepts or dismisses a native JS dialog via CDP. By default waits for a dialog; `ifPresent: true` immediately skips when none is currently open. Does not expose or accept prompt text. |
| `key` | `key`, optional `shift` | Dispatches Tab, Escape, Enter, ArrowUp or ArrowDown through CDP; combine with explicit focus assertions and visible browser observations. |
| `assert` | `expression` | Executes trusted JavaScript and requires a truthy result. Assertions can have side effects; review them before running. |
| `viewport` | `width`, `height`, optional `mobile`, `scale` | Uses CDP viewport emulation; verify actual layout in a visible browser. |
| `screenshot` | new `path`, optional `redactSelectors` array | Writes a new PNG with mode 0600; refuses to overwrite existing evidence. Hides inputs, textareas, selects, editable elements and `[data-private]`, plus supplied selectors. |
| `pause` | optional `ms` | Short bounded delay; prefer an explicit condition. |

The JSON report uses an allowlist: control index/tag/type/disabled state and route words from known static paths. It omits values, text, titles, labels, DOM IDs/names, URL queries/fragments and dynamic route segments. Console errors and exceptions are reported by category without their messages. HTTP 400+ statuses and failed network requests are recorded with redacted paths; expected denials can be successful checks. This report cannot establish persisted effects or identify controls by human labels; record those observations separately using sanitized evidence.

For organization report filters, keep the suffix as a path and pass query parameters separately: `{"op":"navigateCurrentOrg","suffix":"/reports","query":{"period":"last_30_days","page":1}}`. The suffix cannot contain `?`, `#`, a hostname or URL credentials. Omitted or empty `query` clears the previous query. Query encoding cannot change the origin, path or fragment; query values remain absent from snapshots and navigation/network diagnostics. Use public filter values only in action files, never credentials or private tokens.

Bounded diagnostics also record main-frame navigation, document response statuses and redirects using redacted static paths, without evaluating page JavaScript. Native JS dialogs are recorded by type only, without message, URL or prompt contents. They are never dismissed automatically. A dialog can block `Runtime.evaluate`; inspect failure diagnostics, then explicitly place `handleDialog` in the reproduction. For a click that synchronously opens a dialog, use `{"op":"click","selector":"<verified selector>","defer":true}` followed by `{"op":"handleDialog","accept":false}` (or `true` when the scenario requires acceptance). A normal click waits for its JavaScript to finish and cannot advance past a blocking synchronous dialog. Diagnostic output is capped at 200 entries.

The helper restricts its debugger connection and explicit navigation URLs to loopback hosts. It is not a network sandbox: redirects, page resources, click handlers and assertion JavaScript may contact other origins. Inspect the app's local configuration and trusted actions before running. Use an externally enforced network restriction if the task requires no external requests.

For platform administrator Basic Auth, place `httpBasic` before the protected `navigate`. For example, use `{"op":"httpBasic","origin":"http://127.0.0.1:4002","usernameEnv":"QA_PLATFORM_USERNAME","passwordEnv":"QA_PLATFORM_PASSWORD"}` with the actual discovered local origin. Set those environment variables through the approved local credential procedure without printing their contents. The helper uses CDP Fetch authentication interception; it never sets a global Authorization header. Ordinary paused requests continue unchanged. It cancels proxy, non-Basic, repeated and other-origin challenges, and disables Fetch interception before closing its own tab in `finally`. Diagnostic categories contain no credential values or challenge messages.

Chrome can cache HTTP authentication in the role's profile. Start a fresh temporary profile for checks that must prove missing or incorrect credentials; disabling Fetch or closing a tab does not clear that cache. A platform Basic Auth credential also does not establish an employee application session. Keep these checks and identities explicit.

Screenshots still require deliberate review: private reasons and identities in ordinary page text are not automatically detected. Hide them with `redactSelectors` before capture and inspect the image before sharing. Never include raw screenshot pixels, page dumps, cookies, console messages or trace data in a report without checking them for secrets.
