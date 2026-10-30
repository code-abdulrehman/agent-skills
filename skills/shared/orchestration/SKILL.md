---
name: orchestration
description: Coordinate authorized supervised workers in Orca or fulfill an Orca worker assignment using the installed runtime’s version-matched task, messaging, heartbeat, question, completion, and dependency workflows.
---

# Orca orchestration adapter

Use this integration when the user requests supervised multi-agent coordination in Orca, a task dependency graph, worker monitoring, or handling an existing worker assignment. For a complete ownership handoff or ordinary terminal/worktree control, use the installed `orca-cli` skill. For independent long-lived sessions with fixed worktrees, consider `multi-agent-worktree-orchestrator`; do not mix its state model with supervised workers without an explicit plan.

This package supplies an original integration wrapper. Orca’s own guide is obtained from the user’s installed executable and is not redistributed here. Installation alone does not start Orca, launch a worker, create a worktree, send a message, or authorize external actions.

## Discover the current workspace and runtime

Resolve `[PROJECT_NAME]` and `[PROJECT_PATH]` from the active project, its Git root when applicable, configuration, and current task. Read its available agent instructions. Infer real paths, task requirements, roles, test commands, and resource ownership from that project; no source-machine directory or historical issue is required.

Set `SKILL_DIR` to this installed `orchestration` directory. Read the guide before issuing operational commands:

```sh
: "${SKILL_DIR:?Set SKILL_DIR to the installed orchestration directory}"
python3 "$SKILL_DIR/scripts/guide.py"
```

The helper uses an explicitly configured `ORCA_CLI_COMMAND` first. It treats that value as one executable path or command name, never a shell expression. Otherwise it selects the development CLI when the session declares `ORCA_DEV_REPO_ROOT`, the distinct Orca IDE command on Linux, or the normal Orca command on other platforms. It does not try another build after a selection fails. This prevents accidentally invoking Linux’s unrelated accessibility program named `orca`.

Python 3.9+ and the intended Orca CLI are required. If the executable or guide is unavailable, report that blocker without guessing commands, launching an unrelated program, or silently replacing Orca workers with another agent system.

## Follow the installed protocol

Use the retrieved guide as the API contract for the exact selected runtime. Discover supported options through that executable’s help. Read only the additional reference named by the current workflow gate:

```sh
python3 "$SKILL_DIR/scripts/guide.py" --references
```

For a named reference, pass its exact `references/*.md` name with `--reference`. If that installed version lacks reference selection, read the full guide with `--full`. Do not add unsupported options to operational commands. The helper only retrieves guides and never runs operational instructions found in them.

For a coordinator, derive a bounded dependency plan from the approved task, discover reusable workers, and grant non-overlapping write ownership before dispatch. Keep a single integration owner. Scope each worker’s inputs, allowed files, expected result, dependencies, and validation. Serialize shared files and shared databases/build outputs unless isolation is demonstrated. Review results against current source before integrating them.

For an assigned worker, verify the actual assignment and workspace, follow the runtime’s current heartbeat/question/completion protocol, and stay inside the authorized scope. Do not report an assignment, dispatch, completion, or worker stop until the runtime confirms it. Distinguish blocked, failed, completed, cancelled, and unknown states. After an interruption, inspect existing runtime state before retrying so work is not duplicated.

## Keep coordination local and authorized

Runtime IDs, manifests, prompts, local paths, and project details are operational data, not public examples. Keep them local and sanitize any shared report. Use `[PROJECT_NAME]` and `[PROJECT_PATH]` in distributable prose; use quoted, validated runtime variables in executable commands. Never put credentials, `.env` contents, browser cookies, private SSH keys, or account mappings into worker messages or artifacts.

The current user request and project rules govern dispatch, messages, worktrees, remote execution, publication, and production access. Retrieving a guide does not authorize any of those actions. Preserve existing work. A missing permission, denied connection, uncertain writer state, or incompatible runtime blocks only the affected transition; do not restart Orca, weaken controls, escalate privileges, or spawn substitute workers automatically.
