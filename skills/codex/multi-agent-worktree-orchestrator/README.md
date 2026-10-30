# Multi-Agent Worktree Orchestrator

A Codex skill for maintainer-led software delivery across independent, long-running Codex
tasks. Each specialist works in a fixed Git worktree with explicit path ownership, while a
maintainer coordinates issues, pull requests, CI, deployment, and cleanup.

This skill deliberately uses separate user-visible Codex tasks instead of in-thread
subagents for project implementation.

## What It Provides

- Repository discovery and a single-agent versus multi-agent recommendation
- An approval-gated topology bootstrap workflow
- A project manifest at `.codex/multi-agent.toml`
- Fixed worktree and path-ownership rules
- Durable maintainer and specialist task coordination
- Issue, branch, pull request, CI, deployment, and cleanup state transitions
- Manifest validation, worktree status reporting, and delegation prompt generation

## Requirements

- Codex with local skill support
- Git
- Python 3.11 or newer for the helper scripts
- Codex task/thread tools for automatic cross-task coordination

When task/thread tools are unavailable, the skill can still generate delegation prompts for
manual delivery. It will not silently replace an independent task with a subagent.

## Installation

Install this package using the collection’s root `install.py` and its `--skill multi-agent-worktree-orchestrator` option. Set `SKILL_DIR` to the resulting installation directory.

Restart Codex if the skill is not detected immediately.

## Usage

Invoke the skill from a Codex task:

```text
Use $multi-agent-worktree-orchestrator to inspect this repository and recommend
whether a fixed-worktree multi-agent topology would help.
```

The discovery phase is read-only. The skill asks for topology approval before creating
configuration or worktrees, and it requires separate explicit approval before creating
user-visible Codex tasks.

After bootstrap, the project manifest is the source of truth:

```bash
python3 "${SKILL_DIR:?Set SKILL_DIR to this installed skill}"/scripts/validate_manifest.py \
  .codex/multi-agent.toml

python3 "${SKILL_DIR:?Set SKILL_DIR to this installed skill}"/scripts/status_report.py \
  .codex/multi-agent.toml
```

Generate a specialist initialization prompt:

```bash
python3 "${SKILL_DIR:?Set SKILL_DIR to this installed skill}"/scripts/render_delegation.py \
  .codex/multi-agent.toml \
  --role backend \
  --mode init \
  --maintainer-thread-id <thread-id>
```

Generate an issue dispatch prompt:

```bash
python3 "${SKILL_DIR:?Set SKILL_DIR to this installed skill}"/scripts/render_delegation.py \
  .codex/multi-agent.toml \
  --role backend \
  --issue 123 \
  --branch codex/issue-123-backend
```

## Delivery Model

```text
planned -> dispatched -> draft_pr -> review_changes
        -> ci_passed -> merged -> deployed -> cleaned
```

The skill enforces one issue, one branch, and one pull request per delivery unit. It also
requires one active writer per owned path, a default owner for shared paths, current CI
evidence, and user-visible verification where applicable.

## Repository Layout

```text
SKILL.md                  Core routing and invariants
agents/openai.yaml        Codex skill metadata
assets/                   Manifest and role templates
references/               Mode-specific operating procedures
scripts/                  Validation and prompt-generation helpers
```

## Security

Do not commit secrets, credentials, private prompts, task IDs, or sensitive source material
to a project manifest. Review generated prompts before sharing them outside the intended
Codex tasks.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports and focused pull requests are welcome.

## License

MIT. See [LICENSE](LICENSE).
