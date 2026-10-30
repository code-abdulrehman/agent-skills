> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# File ownership

Use one writer per whole file. Function-level interests can be recorded, but do not permit simultaneous writes to different functions in one file because patch context, formatting, and imports can overlap.

The lead keeps a table in a local coordination record:

| File | Writer | Interested agents | State | Requested change |
|---|---|---|---|---|
| `lib/[APPLICATION_DIRECTORY]/projects/tasks.ex` | Agent B | Agent A, Agent C | Editing | Scoped task mutation |

States: `available`, `reserved`, `editing`, `verifying`, `blocked`. A specialist requests ownership with exact paths and intended functions. The lead checks all active reservations, grants exclusive ownership by native message, and updates the register before edits. The specialist confirms the latest file contents and current diff, then patches only owned files. On completion, the specialist sends changed paths, tests, and a release message. The lead reviews and marks the file available before another writer begins.

The register is evidence of the decision, not an atomic lock. Do not allow a separate uncontrolled session to write to the worktree. If an external writer is discovered, freeze new writes and arrange a safe handoff. Independent read-only review may continue.

Shared authorization modules, route hooks, member status interfaces, and cross-module fixtures need lead scheduling when multiple specialists request them. The lead resolves the API contract before downstream edits and runs integration tests after both sides land.
