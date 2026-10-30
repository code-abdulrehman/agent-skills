> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Review, Merge, Deploy, And Cleanup

## Review The Pull Request

Inspect:

- issue acceptance criteria;
- changed files and ownership boundaries;
- behavior, edge cases, privacy, security, and compatibility;
- test quality and missing proof;
- migrations, API contracts, generated outputs, and deployment impact;
- PR body, issue linkage, Draft status, and commit scope.

Run independent verification without taking over specialist-owned implementation. Send every
business-code fix back to the original specialist Codex task.

Report findings first, ordered by severity with file and line references. Send blocking fixes
to the original specialist task. Do not silently patch specialist business code from main.

## Handle Review Fixes

Require:

- narrow changes for each finding;
- no unrelated refactor;
- new commit by default;
- repeated relevant tests;
- updated PR head and CI.

Re-review the actual fix diff, not only the specialist's summary.

## Merge Gate

Merge only when:

- no blocking findings remain;
- changed files match ownership;
- required local proof passes;
- all required CI checks completed successfully;
- the PR targets the configured base branch;
- migrations and compatibility risks are understood;
- the PR is ready rather than Draft.

Use the repository's configured merge strategy. Do not bypass branch protection.

## Deployment Verification

After merge:

1. Fast-forward the main checkout without touching unrelated local files.
2. Confirm the main CI run uses the merge SHA.
3. Wait for the configured deployment workflow.
4. Execute `maintainer.deploy_verify`.
5. Verify the deployed revision and each affected service or user-visible workflow.

A successful workflow alone is insufficient when production proof is available.

For a no-runtime-change PR, still confirm the deployment policy behaved as intended. Record
unnecessary rebuilds as separate CI/CD optimization work rather than mixing fixes into the
feature PR.

## Cleanup

Send a cleanup instruction with `send_message_to_thread` to the original specialist task:

- verify clean issue branch;
- switch to configured home branch;
- fetch/prune;
- fast-forward to deployed main;
- delete merged local and remote branches;
- report branch, HEAD, upstream, and status.

If branch deletion fails because a worktree still uses it, first switch that worktree to its
home branch. Never force-remove a worktree containing unexplained changes.

Keep the specialist task open after issue cleanup. Archive it only when the role is retired or
the user explicitly requests archival.
