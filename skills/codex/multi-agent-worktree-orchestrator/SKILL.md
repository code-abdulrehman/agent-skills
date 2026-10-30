---
name: multi-agent-worktree-orchestrator
description: Analyze, recommend, bootstrap, audit, and operate maintainer-led software development across multiple independent, user-visible Codex tasks/sessions, each bound to a fixed Git worktree and explicit path ownership. Use when Codex should coordinate durable specialist sessions through thread tools for issue dispatch, PR review, CI, deployment, and cleanup. This workflow intentionally does not use in-thread subagents for project implementation.
---

## Resolve the active project first

`[PROJECT_NAME]`, `[PROJECT_PATH]`, `[APPLICATION_MODULE]`, and `[WEB_MODULE]` are documentation placeholders. Determine their real values from the active workspace every time this skill is invoked; never treat them as literal commands, identifiers, or directory names. Use `git rev-parse --show-toplevel` when inside Git, otherwise the user-selected workspace. For an umbrella project, identify the actual application before editing. Inspect `mix.exs`, configuration, source modules, and applicable `AGENTS.md`/local instructions to find the application module, web namespace, test runner, schema conventions, and real paths. Do not derive a module name merely by capitalizing a directory name.

Use runtime variables in executable commands: set `PROJECT_PATH` to the verified workspace, `PROJECT_NAME` to its discovered name, `SKILL_DIR` to this installed skill, and `SKILLS_ROOT` to its containing installation directory. Validate required settings without printing secret values:

```sh
: "${PROJECT_PATH:?Set PROJECT_PATH to the verified active workspace}"
: "${SKILL_DIR:?Set SKILL_DIR to this installed skill directory}"
cd "$PROJECT_PATH"
```

The framework examples below describe possible implementations, not facts about another project. Resolve every named module, component, route, directory, service, feature, setup alias, and role against current source before using it. If a helper, registry, schema system, preference store, modal implementation, or warning engine is absent, retain the underlying behavior through the project’s existing equivalent; do not create the old architecture just to satisfy an example. Apply framework-specific rules only when that framework is actually used. Unrelated architectures require their own established implementation and test commands.

Find companion skills by metadata name in the active agent’s installed skill directories; do not assume `.codex/skills` exists in the project. Read project-owned documentation only when it is present, then verify it against source. Do not create missing policy from an old sample.

Keep actual local paths, task/session IDs, identity mappings, tokens, private URLs, environment values, and customer data out of public reports, examples, screenshots, generated prompts, and committed coordination files. Store runtime manifests and audit evidence locally with restrictive permissions; publish only reviewed, neutral examples. A task’s existing authorization and current project instructions take precedence over sample workflow approval defaults.

# Multi-Agent Worktree Orchestrator

Use one maintainer-controlled delivery protocol across projects. Keep project-specific
roles, paths, commands, language, and deployment checks in `.codex/multi-agent.toml`.
Never hardcode a framework, service name, repository path, or host in this skill.

## Use Independent Codex Sessions

This skill means multiple durable Codex tasks/sessions, not a parent turn spawning subagents.

- Keep the current task as the maintainer session.
- Give every specialist one separate, user-visible Codex task.
- Bind every specialist task to its configured fixed worktree.
- Use Codex thread tools to discover, create, message, read, wait for, rename, pin, and archive tasks.
- Route cross-specialist decisions through the maintainer session.
- Never call subagent spawn/delegate tools for implementation, review fixes, tests, or status checks governed by this skill.

## Route The Request

1. Locate the repository root and `.codex/multi-agent.toml`.
2. Select exactly one primary mode:
   - **Discover**: no manifest exists, or the user asks whether multi-agent helps.
   - **Bootstrap**: the user approved a proposed topology and wants it materialized.
   - **Maintain**: plan work, create/refine issues, dispatch specialists, or choose the next issue.
   - **Specialize**: execute one issue inside one owned worktree.
   - **Release**: review a PR, resolve feedback, merge, deploy, or clean worktrees.
   - **Audit**: validate ownership, worktree state, configuration drift, or workflow health.
3. Read only the reference files required by that mode:

| Mode | Read |
| --- | --- |
| Discover | `references/discovery-and-recommendation.md` |
| Bootstrap | `references/bootstrap.md`, `references/manifest-schema.md`, `references/thread-coordination.md` |
| Maintain | `references/maintainer-loop.md`, `references/dependency-rules.md`, `references/thread-coordination.md` |
| Specialize | `references/specialist-loop.md`, `references/thread-coordination.md` |
| Release | `references/review-merge-deploy.md`, `references/thread-coordination.md` |
| Audit | `references/manifest-schema.md`, then the reference for the failing stage |

## Enforce Invariants

- Use one issue, one issue branch, and one pull request per delivery unit.
- Allow only one active writer for an owned path at a time.
- Assign every shared path one default owner.
- Keep the maintainer out of specialist business implementation.
- Keep every long-running role in exactly one independent Codex task.
- Reuse the same specialist task across issues; do not create one task per issue.
- Do not replace a specialist task with a subagent.
- Start issue branches from the configured base branch after fetching the remote.
- Never discard, reset, stash, or overwrite dirty worktree changes without explicit approval.
- Do not let one specialist repair another specialist's owned files.
- Sequence contract and data ownership changes before dependent implementations.
- Do not merge with unresolved blocking review findings or pending/failing required checks.
- Verify user-visible behavior with the configured proof, not static checks alone.
- After merge, return the specialist to its home branch, fast-forward it, and remove the issue branch.
- Do not print secrets, raw credentials, private prompts, or sensitive source material.

## Require Topology Approval

In Discover mode, inspect the repository read-only and recommend either:

- single-agent development, or
- one maintainer plus one to four long-running specialists.

Explain each proposed role using repository evidence. Present owned paths, forbidden paths,
verification commands, shared-path ownership, dependency order, worktree locations, and
proposed Codex task titles, plus unresolved overlaps.

Ask the user to accept, adjust, reduce, or reject the topology. Do not create configuration,
worktrees, branches, tasks, or role files before approval. If a user-input tool is available,
ask one concise approval question; otherwise ask in plain text.

Topology approval does not imply permission for destructive Git operations or Codex task
creation. Obtain explicit task-creation approval before calling `create_thread`.

## Use The Manifest As Source Of Truth

After bootstrap, read `.codex/multi-agent.toml` before dispatching or editing. Validate it:

```bash
python3 <skill-dir>/scripts/validate_manifest.py .codex/multi-agent.toml
```

Inspect current worktree state:

```bash
python3 <skill-dir>/scripts/status_report.py .codex/multi-agent.toml
```

Generate a delegation prompt when useful:

```bash
python3 <skill-dir>/scripts/render_delegation.py \
  .codex/multi-agent.toml \
  --role <role-id> \
  --issue <issue-number> \
  --branch <issue-branch>
```

Generate the initial specialist-session prompt with:

```bash
python3 <skill-dir>/scripts/render_delegation.py \
  .codex/multi-agent.toml \
  --role <role-id> \
  --mode init \
  --maintainer-thread-id <thread-id>
```

Use `scripts/inspect_repository.sh <repo-root>` during read-only discovery. Treat script
output as evidence, not as a complete architecture analysis.

## Coordinate Through Durable State

Use these as distinct layers:

- Project manifest: role topology and policy.
- Project role files: durable instructions read by independent tasks.
- Fixed worktrees: file and Git isolation.
- Independent Codex tasks/threads: long-lived role context and communication.
- Issues: approved work orders and acceptance criteria.
- Pull requests: reviewable implementation results.
- CI and deployment checks: release gates.

Discover and reuse existing specialist tasks by title, worktree, and role before creating
anything. Create a user-owned task only after explicit approval. Dispatch with
`send_message_to_thread`; follow progress with compact thread status tools; send review fixes
and cleanup back to the same task.

If thread tools are unavailable, render the exact prompt for manual delivery and stop that
transition. Do not spawn a subagent, claim dispatch, or silently execute specialist work in
the maintainer task.

## Apply The Delivery State Machine

Track each issue through:

```text
planned -> dispatched -> draft_pr -> review_changes
        -> ci_passed -> merged -> deployed -> cleaned
```

Do not skip a state merely because the code appears correct. Report the current state,
evidence, blocker, owner, and next permitted transition.

## Stop And Escalate

Stop the affected workstream and ask the maintainer or user when:

- owned path patterns overlap without an explicit shared-path owner;
- the required contract or data model is missing;
- a worktree is dirty with unexplained changes;
- a specialist must edit another specialist's files;
- required tests, CI, deployment access, or production proof are unavailable;
- task creation, branch deletion, force push, or another consequential action lacks approval.

Continue independent workstreams when their ownership and dependencies remain valid.
