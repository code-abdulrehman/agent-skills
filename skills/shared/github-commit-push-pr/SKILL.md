---
name: github-commit-push-pr
description: Inspect and verify changes, make scoped commits, push with the correct GitHub identity, create or update draft pull requests, and review PR diffs and CI using local Git and gh. Use for requested Git/GitHub publication or review workflows; never merge.
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

# Git and GitHub workflows

Use local `git` for repository operations and local `gh` for GitHub operations.
Do not silently substitute a connected GitHub integration: it can authenticate as
a different account and create a PR under that identity. If local tools or
credentials are unavailable, report the blocker before making remote writes.
Run only the phases authorized by the current request. Inspection, review, or
installing this skill does not authorize commits, pushes, or PR changes.

## Inspect and preserve the workspace

- Establish the actual repository root, worktree, branch, HEAD, upstream and
  fetch/push remotes. Read applicable `AGENTS.md`, `AGENTS.local.md` and project
  rules. Honor the user's chosen checkout; do not create a worktree implicitly.
- Inspect `git status --short --branch`, `git worktree list`, unstaged and staged
  diffs, and untracked paths. Identify task-owned files and existing user work.
  If a Git operation is already in progress, inspect it before starting another.
- Inspect remote URLs locally and redact embedded credentials before displaying
  them. Do not assume `origin`, its fetch URL, its push URL and the PR base all
  identify the same repository. Check URL rewrites and explicit push URLs.
- Preserve unrelated edits, staged files, exports and backups. Never reset,
  clean, stash, switch away from dirty work, or overwrite another agent's files
  as an automatic preparation step. Do not print or commit tokens, passwords,
  `.env` files or private-key contents. Key paths and public fingerprints suffice.

## Verify identity before every remote write

Determine account selection from the active repository and the current authenticated environment. There is no fixed machine-specific account mapping. Inspect effective Git and SSH configuration and use standard GitHub CLI authentication. When explicit overrides are needed, obtain `GITHUB_USERNAME`, `GITHUB_SSH_HOST`, `SSH_KEY_PATH`, and `GIT_AUTHOR_EMAIL` from the user’s current environment; validate required settings without printing secrets.

1. Resolve the intended account from the requested repository, remote owner/name
   and user intent. An organization name, shell alias, key filename or commit
   email is not a GitHub login. Do not assume `[GITHUB_USERNAME]` is the authenticated
   username. If the intended account remains ambiguous, ask which account to use
   while continuing read-only work.
2. Inspect effective commit identity (`git var GIT_AUTHOR_IDENT` and
   `git var GIT_COMMITTER_IDENT`) and relevant config origins. Inspect effective
   SSH settings with `ssh -G` for the actual push host/alias and user, including
   `HostName`, `IdentityFile`, `IdentitiesOnly` and any proxy. Account for
   `core.sshCommand`, `GIT_SSH_COMMAND` and `GIT_SSH` overrides. Show only relevant
   nonsecret settings; do not dump credential helpers or environment values.
3. Authenticate to the resolved GitHub SSH host using `ssh -T` with batch mode
   and a bounded connection timeout. Verify the returned GitHub username and
   successful-authentication greeting. GitHub normally returns exit **1** for
   successful SSH authentication because it provides no shell; exit code alone
   is insufficient. Preserve host-key verification. Use exactly the same SSH
   settings/key selection for this probe and the actual Git operation.
4. Independently run `gh auth status --hostname "$github_host"` and
   `gh api --hostname "$github_host" user --jq .login`. Detect the presence of
   `GH_TOKEN`, `GITHUB_TOKEN`, enterprise token overrides, `GH_HOST` and
   `GH_CONFIG_DIR` without printing credential values. Environment credentials
   can override the account selected by `gh auth switch`.
5. Verify access to the intended repository through both transports:
   `git ls-remote "$verified_push_url" HEAD` using the verified SSH settings,
   and `gh api --method GET --hostname "$github_host" "repos/$repo"`.
   Inspect the canonical `full_name` and permissions. SSH's greeting proves
   account identity, not repository access; `ls-remote` proves read access, not
   push permission. Require push permission for the actual head repository and
   verify access to the PR base separately when using a fork.
6. Require the SSH username and CLI API login to match the intended account;
   if different accounts are deliberately required, obtain an explicit user
   instruction for that separation. Summarize repository, branch, commit email,
   SSH login and CLI login before the first write. Recheck identity/access before
   subsequent writes, especially after any switch or environment change.

For HTTPS remotes, SSH checks do not establish Git's HTTPS credential identity.
Verify that Git uses the same confirmed CLI account, for example through a
per-command `gh auth git-credential` helper, or use an authorized SSH transport
with the verified key. Do not silently rewrite remotes or global configuration.

Inspect any user-defined identity-switching helper before invoking it; it may change shared configuration. Prefer scoped settings over global changes, then repeat both
authentication checks. A mismatch, expired authentication, insufficient access,
unknown host key or uncertain transport identity blocks remote writes. Report
expected versus observed identity without exposing credentials. Do not log in,
upload SSH keys, replace credentials or change global Git/SSH settings as an
automatic workaround. Never print tokens with `gh auth token` or `--show-token`.

## Verify and commit only the requested changes

- Review source and tests before choosing checks. Use actual project commands
  for relevant tests, linting, formatting, static analysis and required hooks.
  Use existing Elixir fast-loop/test skills when appropriate and available.
- Record commands, source checkpoint, exit codes and actual results. Preserve
  logs locally with secrets redacted. Pending, skipped, blocked and unrun checks
  are not passes. Support inherited-failure claims with comparable evidence.
  Fix confirmed task regressions without weakening assertions or bypassing hooks.
  If source changes, rerun affected checks; avoid duplicate expensive suites.
- Inspect secret exposure, authorization, data changes and missing regression
  coverage in the intended diff. Respect artifact exclusions: keep ad-hoc QA
  captures, temporary scripts, logs and extra task reports local. Include
  permanent tests and required generated contracts only within task scope.
- Confirm the effective author/committer identity before committing. Reconcile
  its email with the verified repository identity and user intent; email alone does not
  prove authentication. Do not amend or rewrite old commits to fix identity
  without explicit authorization.
- Stage explicit paths or reviewed hunks; never use broad `git add .`, `git add -A`
  or force-add ignored artifacts. Review `git diff --cached`, its path list and
  `git diff --cached --check` before each commit. Do not include or unstage
  unrelated pre-staged work; resolve index ownership before committing.
- Split large changes into coherent groups with clear messages describing the
  behavior and purpose. Inspect each resulting commit and the complete diff
  against the intended base. Preserve excluded local work.

## Push and create or update a PR

- Re-run the identity gate before pushing. Confirm the destination repository,
  branch/refspec and upstream; inspect local commits ahead/behind the remote.
  Push only the requested branch. Prevent implicit tag publication, for example
  with `--no-follow-tags`; do not use `--all`, `--mirror` or tag pushes implicitly.
  Keep repository hooks enabled and inspect the final exit status and remote SHA.
- Fetching is read-only remote access. Do not use `git pull` as an update shortcut
  because it may merge. Rebase only within explicitly authorized scope and never
  rewrite published history without explicit permission. A rejected push is a
  reason to inspect divergence, not to retry with force.
- Before creating **or updating** a PR, query existing PRs for the branch:

  ```sh
  gh pr list --repo "$base_repo" --head "$branch" --state all \
    --json number,url,state,isDraft,baseRefName,headRefName,headRepository,headRepositoryOwner
  ```

  Set these variables from verified context. `gh pr list --head` accepts a branch
  name, not `owner:branch`; disambiguate results by head repository/owner and base.
  Update the matching open PR rather than creating a duplicate. Inspect closed
  or merged matches and the remaining diff before deciding a new PR is warranted.
- Read the PR template and existing human-written description. Prepare a clear
  problem/behavior summary, scope, executed tests with results, and known
  limitations. Preserve useful existing content when updating it. Write exact
  multiline text to a temporary body file and use `--body-file`; keep it local.
- Recheck CLI identity immediately before a PR write. Create **draft** PRs by
  default using explicit repository, base and already-pushed head:

  ```sh
  gh pr create --repo "$base_repo" --base "$base" --head "$branch" \
    --draft --title "$title" --body-file "$body_file"
  ```

  This example is for a same-repository head. For forks, verify the correct head
  repository and supported CLI syntax first; never let `gh` implicitly fork or
  push to another repository. Even `gh pr create --dry-run` can push changes.
  Omit `--draft` only when the user explicitly requests ready for review. For an
  existing PR, preserve draft/ready status unless the user requests changing it.
- Verify the resulting PR URL, author, draft state, base, head repository, branch
  and SHA, and remote changed-file list against the reviewed commit scope. Report
  commit groups, push result, check results, known limitations and remaining WIP.

## Review a PR when requested

Use `gh pr view`, `gh pr diff`, `gh pr checks` and relevant workflow logs to review
the actual PR head, changed code and CI results. Check correctness, regressions,
security and authorization risks, secrets, data integrity, and missing tests.
Tie findings to files/lines and evidence; distinguish failures from untested
risks. Review is read-only unless posting a review/comment or changing the PR
was explicitly requested. Re-run the identity gate before any such write.

## Hard limits

- **Never merge PRs, locally or remotely.** Never run `gh pr merge`, `git merge`,
  a merge-capable pull, a merge API operation, or enable auto-merge. Leave merging
  to the user even after approval or green CI.
- **Never force-push or rewrite published history without explicit permission.**
  This includes `--force-with-lease`, rebasing published commits and amending
  published commits. Permission to push or create a PR alone is insufficient.
- Do not deploy, publish tags, change branch protection, or perform unrelated
  account/repository administration as part of this workflow.
