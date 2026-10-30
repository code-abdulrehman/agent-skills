> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Repository Discovery And Agent Recommendation

## Purpose

Decide whether long-running multi-agent development will reduce delivery time without
creating excessive merge and coordination cost. Perform this phase read-only.

## Discovery Checklist

Inspect:

- repository and workspace manifests;
- top-level applications, services, packages, infrastructure, and documentation;
- API contracts, schemas, database migrations, and generated code;
- test entry points and component-specific quality gates;
- CI workflows, deployment units, and production verification scripts;
- existing `AGENTS.md`, custom agents, ownership files, and worktrees;
- recent changes or issues when available.

Run `scripts/inspect_repository.sh <repo-root>` for a baseline inventory. Follow up with
targeted reads; do not infer ownership from directory names alone.

## Decide Whether Multi-Agent Helps

Recommend a long-running specialist only when most of these are true:

- The role has a stable write surface.
- Its work can be reviewed as an independent PR.
- It has an independent verification command or observable proof.
- It has recurring work, not one temporary task.
- Its dependencies can be expressed through contracts or ordered issues.
- Parallel work rarely edits the same files.

Recommend single-agent development when:

- most changes converge on one directory or a few shared files;
- tests and releases cannot be validated independently;
- the repository is small or highly cross-cutting;
- proposed roles would have little recurring work;
- coordination and merge cost exceeds likely parallelism.

Do not split only by programming language. Prefer boundaries based on product ownership,
service responsibility, data ownership, deployment units, or stable interfaces.

## Topology Limits

Default to:

- exactly one maintainer;
- one to four specialists;
- exactly one default owner for every shared path.

Recommend more roles only when the repository contains independently operated subsystems and
the user explicitly accepts the extra coordination cost.

## Candidate Role Shape

For every proposed role, provide:

```yaml
id: stable-role-id
purpose: concise responsibility
owned_paths:
  - path/**
forbidden_paths:
  - other/path/**
verification:
  - command
shared_path_policy:
  path/**: default-owner
depends_on:
  - another-role
reason:
  - repository evidence
confidence: high | medium | low
```

Do not recommend a role with no owned paths or no verification strategy.

## Recommendation Output

Present:

1. Multi-agent recommendation: yes or no.
2. Proposed maintainer and specialists.
3. Evidence for every role.
4. Owned, forbidden, and shared paths.
5. Verification and user-visible proof.
6. Cross-role dependency order.
7. Proposed absolute worktree paths, home branches, and durable Codex task titles.
8. Session communication plan: maintainer hub, specialist reporting, and task reuse.
9. Risks, path overlaps, and unresolved decisions.

Then ask the user to choose:

1. Accept the recommendation.
2. Adjust roles or ownership.
3. Use fewer agents.
4. Keep single-agent development.

Do not materialize anything until the choice is explicit.

State explicitly that the proposal uses independent user-visible Codex tasks, not subagents.
Ask separately for permission before creating those tasks.
