> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Independent Codex Session Coordination

## Required Topology

Run the workflow as separate user-visible Codex tasks:

- one maintainer task;
- one long-running task per specialist;
- one fixed Git worktree per specialist task.

These are peer Codex sessions coordinated by the maintainer. They are not subagents spawned
inside the maintainer turn. Never use subagent spawn, wait, steer, or close tools as a
substitute for this topology.

## Discover Sessions

Use `list_threads` before creation or dispatch. Use a search query when the current host
accepts it; otherwise inspect a bounded recent list. Match a specialist by:

1. configured `session_title`;
2. configured worktree or saved project;
3. role identity reported by the task.

Use `read_thread` only when the summary is insufficient. Do not trust title alone when two
projects can use the same role name.

Identify the current maintainer task from its active status, worktree, title, and role before
passing its thread ID to specialist initialization prompts. If it cannot be identified
reliably, omit the callback ID and let the maintainer read the specialist task.

## Create Sessions

Call `create_thread` only after the user explicitly authorizes creating independent Codex
tasks. First call `list_projects` and match each fixed worktree to a saved project.

Create the task directly in that saved project with a local environment. Do not ask Codex to
create another managed worktree around an already fixed worktree. If no saved project matches
the configured path, stop and ask the user to add/open that worktree as a Codex project.

Initialize the task with the rendered `init` prompt. Then:

1. rename it to the configured `session_title`;
2. pin it when the user wants the durable team visible;
3. wait for its read-only initialization report;
4. verify role, worktree, branch, upstream, ownership, and clean status.

Do not create one task per issue. Reuse the role task for every later issue.

## Communication Protocol

The maintainer is the routing hub:

- Maintainer -> specialist: `send_message_to_thread`.
- Specialist -> maintainer: report in its task and, when given the maintainer thread ID and
  thread tools are callable, send blockers or completion back with `send_message_to_thread`.
- Specialist -> specialist: do not steer peers directly. Report the dependency to the
  maintainer, who makes the decision and forwards an authoritative message.

Every dispatch message includes issue/PR URL, exact branch, owned and forbidden paths,
acceptance criteria, verification, required proof, dependency state, and reporting format.

## Follow Progress

Prefer compact `wait_threads` snapshots when callable. Keep each task's returned cursor and
use it as `afterCursor` on the next wait. When `wait_threads` is unavailable, use bounded
`read_thread` checks only at meaningful transitions.

Do not poll repeatedly, narrate unchanged state, or hide approval and user-input requests.
Read deeper history only for a decision, failure, review claim, or conflicting instruction.

## Steering And Lifecycle

Send scope corrections, contract decisions, review fixes, and post-merge cleanup to the same
specialist task. Never create a replacement task merely because the current issue changed.

Archive a specialist task only when the role is retired, the project topology changes, or the
user explicitly requests archival. Merging one issue is not a reason to archive it.

## Permissions

Each independent task has its own runtime permission state. This skill does not bypass
approvals or promise that a project config can suppress host-required confirmation. Leave
approval requests attached to the originating task for the user.

## Tool Unavailable Fallback

If independent-thread tools are unavailable:

1. render the complete init, dispatch, review, or cleanup prompt;
2. report the intended task title and worktree;
3. ask the user to deliver or open it manually;
4. continue only maintainer-owned work.

Never fall back to subagents and never claim session communication occurred.
