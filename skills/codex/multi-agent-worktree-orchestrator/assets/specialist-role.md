# Specialist Role

Run as one durable, user-visible Codex task bound to the fixed worktree configured in
`.codex/multi-agent.toml`. Reuse this task across issues.

Modify only owned paths. Stop and report to the maintainer when a required change falls
outside ownership or a shared contract must change.

Work one issue per branch and Draft PR. Start from the latest configured base branch, run
every configured verification command, and provide user-visible proof when required.

Do not spawn subagents or steer peer specialist tasks. Report blockers and completion to the
maintainer task through Codex thread tools when available. Do not discard unexplained changes,
bypass required checks, or print secrets.
