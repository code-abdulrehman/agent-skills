# Portable project workflows

Local project workflows were added at the source maintainer’s explicit request, after removing the original project identity and assumptions. The new packages carry individual redistribution-authorization notices; the existing third-party orchestrator retains its MIT license. No unrelated third-party package was reclassified.

| Skill | Collection path | Files |
| --- | --- | ---: |
| elixir-fastloop | `skills/shared/elixir-fastloop` | 5 |
| multi-agent-task-coordinator | `skills/shared/multi-agent-task-coordinator` | 7 |
| multi-agent-worktree-orchestrator | `skills/codex/multi-agent-worktree-orchestrator` | 21 |
| project-components | `skills/shared/project-components` | 2 |
| project-manual-qa | `skills/shared/project-manual-qa` | 7 |
| project-task-tests | `skills/shared/project-task-tests` | 2 |
| project-backend | `skills/shared/project-backend` | 6 |
| project-engineering | `skills/shared/project-engineering` | 2 |
| project-ui | `skills/shared/project-ui` | 6 |
| project-engineering | `skills/shared/project-engineering--e4c1a999` | 2 |
| project-ui | `skills/shared/project-ui--bab20bd1` | 6 |
| github-commit-push-pr | `skills/shared/github-commit-push-pr` | 2 |

All 12 packages (68 files) passed targeted identity/path/credential inspection, frontmatter and YAML checks, relative-reference and support-file checks, and applicable Python, Node, shell, and TOML parsers. A mocked diagnostic test verified that raw environment values, process paths, and process arguments are omitted while process IDs and configured-setting names remain available. No browser session, database, external service, build workflow, or production resource was exercised.

The agent resolves `[PROJECT_NAME]`, `[PROJECT_PATH]`, `[APPLICATION_MODULE]`, and `[WEB_MODULE]` from the active workspace; these are not executable literals. Shell commands use validated environment variables. The issue-specific coordinator now discovers the approved task instead of requiring a historical ticket, worktree, or phase plan. Domain policies, custom schema registries, helpers, warning systems, and UI contracts are conditional examples that must be verified in the current project. Elixir/Phoenix implementation rules remain framework-specific.

Runtime manifests, delegation prompts, test output, and screenshots may contain the new user’s project details because they support local work. Keep those artifacts local and review/redact them before sharing. Do not publish runtime credentials or private paths. Installation remains non-overwriting and skips an already installed metadata identity.

License revision: the collection’s original tooling/adapters and authorized local project-workflow adaptations now carry MIT licenses. Existing upstream licenses remain unchanged. See `../LICENSE-SCOPE.md` and the catalog for the current scope.
