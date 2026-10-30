> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Multi-Agent Manifest Schema

The project source of truth is `.codex/multi-agent.toml`. Keep it project-specific and commit
it only after the user approves the topology.

## Top-Level Fields

```toml
version = 1

[project]
name = "project-name"
main_checkout = "/absolute/path/to/project"
remote = "origin"
base_branch = "main"
branch_prefix = "codex/"
communication_language = "English"

[coordination]
mode = "independent_codex_tasks"
hub_role = "main-maintainer"
allow_subagents = false

[maintainer]
id = "main-maintainer"
role_file = ".codex/roles/main-maintainer.md"
session_title = "project-name - main-maintainer"
worktree = "/absolute/path/to/project"
owned_paths = [".github/**", "docs/**", ".codex/**"]
forbidden_paths = ["src/**"]
verify = ["git diff --check"]
deploy_verify = []

[[specialists]]
id = "backend"
role_file = ".codex/roles/backend.md"
session_title = "project-name - backend"
purpose = "Own the application backend and data contracts."
worktree = "/absolute/path/to/project-backend"
home_branch = "codex/backend-home"
owned_paths = ["services/backend/**", "db/**"]
forbidden_paths = ["apps/frontend/**"]
verify = ["run backend tests", "git diff --check"]
user_visible_verify = []
depends_on = []

[shared_paths]
"packages/contracts/**" = "backend"
```

## Required Fields

`project` requires:

- `name`
- `main_checkout`
- `remote`
- `base_branch`
- `branch_prefix`

`coordination` requires:

- `mode = "independent_codex_tasks"`
- `hub_role` matching the maintainer ID
- `allow_subagents = false`

`maintainer` requires:

- `id`
- `role_file`
- `session_title`
- `worktree`
- `owned_paths`
- `verify`

Every `specialists` item requires:

- `id`
- `role_file`
- `session_title`
- `purpose`
- `worktree`
- `home_branch`
- `owned_paths`
- `verify`

## Optional Fields

- `communication_language`: issue, PR, and status language.
- `forbidden_paths`: explicit no-write boundaries.
- `user_visible_verify`: browser, API, device, or artifact proof.
- `depends_on`: role-level dependency hints.
- `deploy_verify`: production verification commands.
- `shared_paths`: glob-to-default-owner mapping.

## Validation Rules

- Use absolute, unique worktree paths.
- Use unique role IDs, session titles, and home branches.
- Keep owned path globs repository-relative.
- Do not assign overlapping owned paths to different roles.
- Resolve intentional shared paths through `shared_paths`.
- Assign a shared path owner that exists as maintainer or specialist.
- Keep verification commands non-empty.
- Do not store task IDs, secrets, tokens, credentials, or environment values here.
- Do not change coordination mode to a subagent workflow.

Run:

```bash
python3 <skill-dir>/scripts/validate_manifest.py .codex/multi-agent.toml
```

The validator catches structural errors and obvious path overlaps. It cannot prove semantic
ownership correctness; review the repository architecture before accepting a topology.
