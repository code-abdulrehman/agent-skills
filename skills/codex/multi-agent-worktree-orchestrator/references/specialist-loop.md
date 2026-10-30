> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Specialist Issue Loop

## Session Identity

Run as one independent, user-visible Codex task bound to the configured fixed worktree. Reuse
this same task across issues. Do not spawn subagents or steer another specialist task.

The maintainer is the authority for issue assignment, shared contracts, review, merge, and
cleanup. When thread tools and the maintainer thread ID are available, send blockers and
completion reports back to that maintainer task.

## Start Safely

1. Read repository guidance, the project manifest, and the configured project role file.
2. Confirm the current directory is the configured fixed worktree.
3. Run `git status --short --branch`.
4. Stop if unexplained changes exist.
5. Fetch/prune the configured remote.
6. Switch to the configured home branch and fast-forward from the remote base branch.
7. Create the exact issue branch supplied by the maintainer.

Never implement on the home branch.

## Confirm Scope

Read the issue and report:

- intended behavior;
- owned files likely to change;
- upstream contract or data dependencies;
- verification commands;
- any ambiguity that could force cross-owner edits.

Stop and escalate before editing when a required upstream contract is missing.

## Implement

- Follow existing repository patterns.
- Keep changes inside owned paths.
- Avoid unrelated refactors and dependencies.
- Add tests proportional to risk.
- Use fixtures or fakes for external systems unless live verification is explicitly required.
- Redact secrets and sensitive source material.

Do not modify another role's files as a convenience.

## Verify

Run every configured `verify` command. Run every applicable `user_visible_verify` command or
equivalent observable proof.

At minimum check:

- tests;
- formatting, lint, or type checking;
- `git diff --check`;
- changed-file scope;
- no secret or temporary artifact leakage.

## Publish

1. Review the final diff and status.
2. Stage only intended files.
3. Create one intentional commit or a small coherent series.
4. Push without force unless explicitly approved.
5. Create a Draft PR against the configured base branch.
6. Link the issue and include behavior, verification, risk, and screenshots or API proof.

Report:

- branch;
- commit SHA;
- Draft PR URL;
- verification results;
- known limitations;
- CI status.

Keep the final report in this specialist task. Also notify the maintainer task through
`send_message_to_thread` when that tool and thread ID are available.

## Address Review

Read all actionable maintainer comments. Make narrow fixes in the same worktree and branch.
Add a new commit by default; do not amend or force-push unless requested. Re-run relevant
verification and report the new head SHA.

## Cleanup After Merge

Only after the maintainer confirms merge:

1. Confirm the issue branch is clean.
2. Switch to the home branch.
3. Fetch/prune and fast-forward to current remote base.
4. Delete the merged local and remote issue branch.
5. Confirm final branch, HEAD, upstream, and clean status.

Do not begin another issue during cleanup.
Do not archive the task after cleanup; remain available for the next issue.
