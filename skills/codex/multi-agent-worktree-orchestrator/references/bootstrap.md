> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Bootstrap An Approved Topology

## Preconditions

Require:

- an explicit user-approved topology;
- an identified repository root and base branch;
- a clean understanding of existing worktrees and uncommitted changes;
- proposed absolute worktree paths;
- no unresolved ownership overlaps.

Topology approval permits configuration generation. Creating or deleting worktrees and
creating independent user-owned Codex tasks still requires explicit user intent.

## Materialize Project Configuration

1. Copy `assets/multi-agent.toml` to `.codex/multi-agent.toml`.
2. Replace every placeholder using the approved topology.
3. Run `scripts/validate_manifest.py`.
4. Create or update project role files under `.codex/roles/`.
5. Add concise ownership and workflow rules to the repository's agent guidance.
6. Generate a project collaboration document only when the repository keeps development docs.

Do not copy project-specific examples from another repository.

## Generate Role Files

Create one maintainer role file and one role file per approved specialist. Each file must
define:

- role purpose;
- fixed worktree when applicable;
- owned and forbidden paths;
- shared-path escalation rule;
- verification and user-visible proof;
- one-issue/branch/PR workflow;
- security and secret handling.

These are plain role instructions for independent Codex tasks, not custom-agent TOML files.
Do not put task-specific issue numbers in long-lived role files.

## Create Fixed Worktrees

Before each worktree operation:

1. Run `git status --short --branch` in the main checkout.
2. Run `git worktree list --porcelain`.
3. Fetch the configured remote.
4. Verify the proposed home branch is unused.
5. Verify the target directory does not contain user files.

Create a stable home branch from the configured remote base branch. The home branch exists
only to keep the fixed worktree attached; never use it as an issue PR branch.

Do not delete or repurpose existing worktrees without explicit approval.

## Connect Codex Tasks

Use one independent, long-running, user-visible Codex task per specialist worktree. Do not use
subagents. Create tasks only when explicitly requested by the user.

Before creating:

1. Use `list_threads` to avoid duplicate role tasks.
2. Use `list_projects` and match every fixed worktree to a saved Codex project.
3. Stop if a worktree is not available as a saved project; do not create a nested managed
   worktree as a substitute.
4. Render the role's `init` prompt with the maintainer thread ID when available.
5. Call `create_thread` with that saved project and a local environment.
6. Rename the result to the configured `session_title`.
7. Pin it when the user wants the durable team visible.

Initialize each task read-only:

- read project guidance and its configured role file;
- inspect branch, upstream, and status;
- report owned paths and verification commands;
- recommend a next issue but do not implement it.

Do not store host-specific thread IDs in the committed manifest. Discover sessions by title,
project/worktree, and role. Reuse each specialist task across issues.

## Bootstrap Verification

Verify:

- manifest validation passes;
- every approved role has one project role file;
- every specialist has one independent Codex task with the configured title;
- each task reports the configured fixed worktree and role;
- worktree paths and home branches match the manifest;
- every worktree is clean and based on the intended base SHA;
- no owned path has multiple writers;
- no secrets or host credentials were written;
- no business implementation was introduced during bootstrap.
- no subagent was spawned as a substitute for an independent task.
