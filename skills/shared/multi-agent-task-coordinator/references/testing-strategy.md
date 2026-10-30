> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Testing strategy

Inspect nearby tests and run a relevant baseline before behavior edits. Add focused regressions for uncovered behavior, run them after each owned change, and report exact commands, counts, and failures. The lead coordinates integration checks for lifecycle, tenant/resource scope, historical assignment, report history, cache invalidation, workers, and cross-tenant denial. Run the full suite when requested and distinguish its failures from focused results.

Discover the active repository’s guarded test runner and dedicated local test configuration. Inspect aliases and scripts before invoking them; even a normal test command may perform setup or migrations. Use the project’s actual language/framework commands. Never point tests at staging or production.

The lead serializes database-dependent tests and compilation that share the same database or build output. Parallelize them only after proving isolation. Keep test execution separate from another session's active transaction. Run formatting on changed files, `git diff --check`, and relevant compilation after integration. The final report includes exact commands and actual results, including exclusions and unresolved failures.
