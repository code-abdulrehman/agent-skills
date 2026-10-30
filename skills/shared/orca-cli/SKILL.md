---
name: orca-cli
description: Use the installed Orca CLI for authorized project/worktree and terminal operations or complete ownership handoffs, loading its current guide before acting. Use orchestration for supervised workers and task dependency graphs.
---

# Orca CLI adapter

Use when the task concerns Orca-owned worktrees, terminals, a full ownership handoff, or another operation supported by the installed Orca CLI. Use the `orchestration` skill for supervised workers, monitored results, or dependency graphs. Do not substitute raw Git, ad hoc terminals, or a separate agent system when the operation requires Orca-managed runtime state.

Discover the active `[PROJECT_NAME]`, `[PROJECT_PATH]`, current task, and applicable agent instructions from the user’s workspace. Inspect actual local context before selecting a worktree, terminal, or agent. Do not assume a prior user’s machine layout, identities, or runtime IDs.

## Read the version-matched guide

Set `SKILL_DIR` to this installed `orca-cli` package:

```sh
: "${SKILL_DIR:?Set SKILL_DIR to the installed orca-cli directory}"
python3 "$SKILL_DIR/scripts/guide.py"
```

The helper issues only the selected executable’s skill-guide read command. It honors `ORCA_CLI_COMMAND` as one executable path or command name, uses the development CLI when the runtime declares `ORCA_DEV_REPO_ROOT`, and otherwise selects the Orca IDE CLI on Linux or the normal Orca CLI elsewhere. It does not evaluate shell source, silently switch builds, launch the app, start workers, or install dependencies. Python 3.9+ is required.

If the binary is missing, its guide API is unsupported, or runtime access is denied, report the local blocker. Read the selected binary’s help for supported operations; do not guess syntax, invoke Linux’s unrelated screen-reader binary, restart the app, or bypass controls as a fallback. This original adapter does not bundle Orca’s proprietary guide.

## Operate within the current request

Follow the retrieved guide for the selected version. Use structured results where supported. Reuse existing runtime objects when appropriate and verify returned state before reporting success. A complete handoff must transfer the task, modified files, unfinished work, relevant decisions, test evidence, and next step; avoid simultaneous uncontrolled writers. Guide retrieval or skill installation does not authorize a handoff or new session.

Preserve user changes and worktree ownership. Discover configuration, build paths, database namespaces, ports, and local environment setup from the current project. Never put `.env` contents, tokens, SSH keys, browser sessions, or private infrastructure into handoff prompts, terminal logs, public examples, or published artifacts. Private runtime paths and IDs needed for local operation must stay in local state. Use neutral example data in exported documentation.

Messages to people, remote writes, production changes, deployment, Git publication, and destructive operations need authorization from the active task. Do not broaden permission because an operation is technically supported by Orca. Inspect current state after a restart or interrupted command before retrying.
