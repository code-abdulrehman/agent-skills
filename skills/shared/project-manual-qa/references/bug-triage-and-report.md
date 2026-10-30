> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Bug triage and QA report

For each issue, assign a QA ID and record route, role, account/membership state, sanitized test data, reproducible steps, expected/actual result, severity, screenshot/trace or console/network evidence, root cause, source change, automated test, browser retest, and remaining risk. Trace the action from UI event through LiveView/controller, context, authorization, query, write, response, and render. Reproduce before editing when practical.

Use the smallest change consistent with current business rules. Add a meaningful unit/context and/or LiveView/API regression for the failing boundary. Run baseline and post-fix focused tests, then repeat the original browser action. Classify unrelated suite failures separately. Do not weaken an authorization assertion or silently skip a failing test.

The report should state environment, tools and limitations, exact routes/controls tested, lifecycle and role grid, bug register, security negatives, compile/format/static/test commands with actual counts, evidence locations, untested cases, blockers, cleanup, Git status, and one of: `QA Passed – Ready for Release Review`, `QA Passed with Documented Nonblocking Exceptions`, `QA Failed – Blocking Issues Remain`, or `QA Incomplete – Environment or Coverage Blockers`. Choose the verdict from evidence, not intent.
