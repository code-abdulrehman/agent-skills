---
name: multi-agent-task-coordinator
description: Coordinate an approved task in the current project across agents with explicit file ownership, dependency waves, safe handoffs, integration review, and isolated testing. Use only when parallel agent work is requested or authorized.
---

# Multi-agent task coordination

Determine `[PROJECT_NAME]`, `[PROJECT_PATH]`, the approved task, and acceptance criteria from the active workspace and current request. These are documentation placeholders; resolve real values each time. Use the Git root when applicable, inspect the actual project structure, and read its available agent instructions and workflow rules. Discover task specifications and test commands from the current project; do not assume an issue number, pre-existing worktree, report, module namespace, or directory from another project.

Use this workflow when parallel agents are authorized and a lead coordinates bounded implementation tasks. The lead owns the roadmap, shared decisions, file ownership, integration review, test scheduling, and final report. Specialists report inspected files, requested write paths, dependencies, changes, tests, and blockers. The lead resolves conflicting decisions.

For independent durable sessions/worktrees, use the installed `multi-agent-worktree-orchestrator` instead of silently substituting in-thread subagents. For native subagents, first discover the actual available tools and limits. If the required tools are unavailable, prepare explicit handoff prompts without claiming an agent was started. A skill installation does not authorize spawning agents or creating sessions.

## Establish the current contract

Read [task-requirements.md](references/task-requirements.md) to extract the approved scope, policy, dependencies, and acceptance evidence. Historical tests and reports are evidence to compare with current source, not permission to change business policy. The membership/resource examples in that reference apply only if the current task has those approved requirements.

Before assigning writers, verify previous writers have stopped or handed off. Current-tree controls do not control a separate session. Coordinate a safe pause with its owner when necessary; never kill unrelated processes. Preserve all uncommitted work. Read [handoff-protocol.md](references/handoff-protocol.md).

## Delegate in dependency waves

- Decompose the approved task using the current architecture: for example, domain contracts, transport/UI, external integration, and QA. The project’s boundaries determine workstreams; do not create fictional features or apply a stale P0/phase plan.
- Require a declared file list before edits. Grant one writer per whole file. Serialize shared interfaces through the lead; parallelize only independent paths and runtime resources. Read [coordination-rules.md](references/coordination-rules.md) and [file-ownership.md](references/file-ownership.md).
- Each writer re-reads the latest file immediately before patching and preserves unrelated changes. The ownership register documents a grant; it is not an atomic lock. If ownership cannot be enforced, serialize work.
- Keep one local coordination record for decisions and results. Use the available messaging mechanism for handoffs. Review each specialist’s output before integration.
- Discover real test/build commands and shared services. Isolate or serialize database-dependent tests, compilers, ports, and generated outputs. Read [testing-strategy.md](references/testing-strategy.md).

## Portable examples and private runtime state

Use `[PROJECT_NAME]` and `[PROJECT_PATH]` in public prose. For executable commands, validate variables and quote paths:

```sh
: "${PROJECT_PATH:?Set PROJECT_PATH to the verified active workspace}"
cd "$PROJECT_PATH"
```

Inspect the project’s toolchain/configuration to find its module names and runtime services. Do not copy desktop paths, account mappings, real task/session IDs, credentials, customer data, or private endpoints into prompts or public artifacts. Keep required runtime manifests and evidence local with restrictive permissions; use mock data in distributable examples. Never copy a local `.env` into the public collection.

## Scope and stop conditions

Task authorization and the current project’s instructions govern allowed actions. Coordination alone does not authorize commits, pushes, merges, PR writes, deployments, destructive data changes, production access, new business policy, or uncontrolled migration changes. Continue authorized implementation without redundant approval, and stop only the affected transition when required authorization or a policy decision is missing. Preserve source history, existing migrations, and user work. If another writer’s state is uncertain, continue read-only preparation until safe ownership is established.
