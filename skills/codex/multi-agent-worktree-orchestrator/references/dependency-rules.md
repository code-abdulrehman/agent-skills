> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Dependency And Parallelism Rules

## Split By Delivery Boundary

Create the smallest independently reviewable issues that preserve a coherent user outcome.
Do not split work merely to keep every specialist busy.

For cross-role changes, prefer this order:

```text
architecture decision
-> contract or data model
-> provider/domain implementation
-> application orchestration and persistence
-> user interface consumer
-> deployment or migration
```

Skip stages that do not apply, but never let a consumer invent an upstream contract.

## Parallelize Only When Safe

Two issues may run in parallel when:

- their owned paths do not overlap;
- neither depends on an unstable output from the other;
- each has independent verification;
- merging either first will not invalidate the other.

Serialize when:

- both modify a shared contract or schema;
- a data migration defines fields consumed by another role;
- generated code must follow an upstream specification;
- both change the same deployment or configuration surface;
- product behavior is still undecided.

## Assign Shared Paths

Give every shared path one default owner. Other specialists may read it, but must request a
separate owner-coordinated issue when it must change.

Common shared surfaces include:

- API contracts;
- database schemas and migrations;
- generated clients;
- authentication policy;
- deployment manifests;
- cross-application design tokens.

## Build An Issue Dependency Graph

For each issue record:

- owner;
- owned paths;
- acceptance criteria;
- required proof;
- upstream issues;
- downstream consumers;
- whether it can run in parallel;
- expected branch name.

Do not dispatch a blocked issue. A downstream specialist may perform read-only discovery while
waiting, but must not implement against guessed fields or behavior.

## Replan After Every Merge

After merge and deployment:

1. Refresh open issues and PRs.
2. Re-evaluate dependencies against current main.
3. Confirm specialist worktrees are clean.
4. Choose the highest-value unblocked issue.
5. Avoid automatically continuing an outdated roadmap sequence.
