> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Coordination rules

The lead maintains a single roadmap and records decisions with the affected interface, owner, reason, and validation. Each specialist reports: assignment, inspected files/functions, requested write files/functions, dependencies, completed changes, executed tests and results, failures, blockers, and handoff readiness. Send discoveries explicitly; separate agent contexts do not automatically share them.

Work in dependency waves. Allow parallel inspection and edits to distinct owned files. For a shared file, the lead selects one writer, waits for completion and focused verification, releases that ownership, then asks the next writer to re-read and patch the new version. The lead validates the combined behavior. If a writer or test process is still active after an interruption, wait for its atomic write or database transaction to finish and verify its stopped state before reassignment.

When a patch no longer matches or the file changed after inspection, stop and notify the lead. Do not replace the file wholesale or undo another agent's changes. The lead inspects the new state, decides ordering, and reassigns. If a test fails, record its exact command and failure; distinguish implementation defects, fixture defects, environmental failures, and unresolved product decisions using evidence.

Only the lead updates the ownership register, shared progress record, and final integration result. Agents may inspect them at any time. Report progress at handoff boundaries and after meaningful test checkpoints.
