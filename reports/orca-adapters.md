# Orca runtime adapters

`orchestration` and `orca-cli` are original collection adapters. They load version-matched documentation from the user’s installed Orca CLI. Vendor stubs and full runtime documentation are not redistributed; the original vendor packages remain excluded from the discovery inventory where license evidence was unresolved.

Both packages passed metadata and Python parsing, seven mocked behavior/safety checks, and actual local read-only guide retrieval. Tests confirmed explicit executable selection, Linux CLI disambiguation, development-build selection, no shell evaluation/fallback, rejected reference traversal, fixed read-only argument construction, and redacted failed-command output. No workers, tasks, messages, worktrees, browser sessions, remote actions, or app restarts were initiated.

Set `SKILL_DIR` to the installed package. The CLI is resolved from the new user’s own environment. A configured `ORCA_CLI_COMMAND` must name one executable, not a shell command expression. Missing or incompatible Orca installations remain a runtime prerequisite; the installer does not install Orca. Do not substitute other agent runtimes or leak private IDs/paths into public examples.

License revision: the collection’s original tooling/adapters and authorized local project-workflow adaptations now carry MIT licenses. Existing upstream licenses remain unchanged. See `../LICENSE-SCOPE.md` and the catalog for the current scope.
