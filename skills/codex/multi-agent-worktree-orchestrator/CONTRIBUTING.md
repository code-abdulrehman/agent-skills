# Contributing

Thanks for helping improve Multi-Agent Worktree Orchestrator.

## Before Opening A Pull Request

1. Keep changes framework- and repository-agnostic.
2. Preserve the independent Codex task model; do not replace specialist tasks with
   in-thread subagents.
3. Keep consequential operations approval-gated.
4. Do not add real credentials, task IDs, hostnames, private prompts, or personal paths to
   examples and fixtures.
5. Update the relevant reference documentation when behavior changes.

## Local Checks

Run these checks from the repository root:

```bash
python3 scripts/validate_manifest.py assets/multi-agent.toml
python3 scripts/render_delegation.py assets/multi-agent.toml \
  --role component-owner \
  --mode init
python3 scripts/render_delegation.py assets/multi-agent.toml \
  --role component-owner \
  --issue 123 \
  --branch codex/issue-123-component-owner
bash -n scripts/inspect_repository.sh
python3 -m compileall -q scripts
git diff --check
```

`status_report.py` requires a manifest whose worktree paths point to real Git worktrees, so
test it with a temporary fixture or a real project manifest.

## Pull Requests

Keep pull requests focused and explain:

- the behavior being changed;
- why the change belongs in the generic skill rather than project configuration;
- the checks run;
- any compatibility or safety implications.
