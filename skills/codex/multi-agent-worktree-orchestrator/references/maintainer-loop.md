> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Maintainer Loop

## Maintainer Responsibilities

The maintainer owns:

- product and architecture issue decomposition;
- owner and dependency assignment;
- specialist dispatch and status tracking;
- independent Codex task creation and session-to-session communication;
- pull-request review;
- CI, merge, deployment, and cleanup coordination.

The maintainer does not implement specialist business features.

## Plan The Next Issue

1. Sync and inspect the main checkout without discarding local changes.
2. Read the current roadmap, open issues, open PRs, and recently merged work.
3. Validate the project manifest and worktree status.
4. Identify the highest-value unblocked delivery unit.
5. Assign one owner, owned paths, forbidden paths, acceptance criteria, and proof.
6. Create or refine the issue.
7. Record dependency order for cross-role work.

Do not dispatch from stale main or when the target worktree is dirty.

## Dispatch A Specialist

Before dispatch:

- confirm the issue exists;
- confirm the owner matches the manifest;
- discover the independent specialist task by title, project/worktree, and role;
- confirm the home branch is clean and can fast-forward;
- provide the exact issue branch;
- provide required verification and Draft PR requirements.

Generate a baseline prompt with `scripts/render_delegation.py`, add task-specific acceptance
criteria and security constraints, then send it with `send_message_to_thread`.

Require the specialist to:

- fetch and synchronize its home branch;
- create the exact issue branch from current remote base;
- stay within owned paths;
- implement and test;
- commit intentionally;
- push and create a Draft PR;
- report commit, PR URL, proof, and known risks.

## Track Progress

Prefer compact task/thread status reads. Do not repeatedly narrate unchanged status.
Intervene when:

- the specialist requests a contract decision;
- files move outside owned paths;
- tests reveal an upstream defect;
- the PR is ready for review;
- the task stalls on a permission or external-state problem.

Leave approval requests visible for the user when the platform requires user action.
Never replace a blocked or unavailable specialist task with a subagent.

## Review And Release

Follow `review-merge-deploy.md`. Findings lead; summaries follow. Send actionable feedback to
the same specialist Codex task and require an additional commit unless history rewriting was
explicitly approved.

## Close The Loop

After verified deployment:

1. Tell the specialist to return to its home branch.
2. Fetch/prune and fast-forward to current remote base.
3. Remove local and remote issue branches after confirming merge.
4. Verify the worktree is clean.
5. Refresh the issue graph before recommending the next task.
