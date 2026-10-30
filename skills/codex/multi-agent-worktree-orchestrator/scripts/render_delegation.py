#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Any

if sys.version_info < (3, 11):
    for candidate in ("python3.14", "python3.13", "python3.12", "python3.11"):
        executable = shutil.which(candidate)
        if executable:
            os.execv(executable, [executable, *sys.argv])
    print("Python 3.11 or newer is required.", file=sys.stderr)
    raise SystemExit(2)

try:
    import tomllib
except ModuleNotFoundError:
    print("Python 3.11 or newer is required.", file=sys.stderr)
    raise SystemExit(2)


def bullet_lines(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values) if values else "- none"


def find_role(data: dict[str, Any], role_id: str) -> dict[str, Any] | None:
    candidates = [data.get("maintainer", {})] + data.get("specialists", [])
    for role in candidates:
        if isinstance(role, dict) and role.get("id") == role_id:
            return role
    return None


def maintainer_reporting(maintainer_thread_id: str | None) -> str:
    if not maintainer_thread_id:
        return (
            "Keep the report in this Codex task. The maintainer will read it "
            "through thread tools."
        )
    return (
        "Also send blockers and completion to the maintainer Codex task with "
        f"`send_message_to_thread` using thread ID {maintainer_thread_id} when "
        "that tool is callable."
    )


def init_prompt(
    project: dict[str, Any],
    role: dict[str, Any],
    maintainer_thread_id: str | None,
) -> str:
    return f"""Initialize the independent Codex task titled:
{role['session_title']}

You are the long-running {role['id']} specialist for {project['name']}. This is a separate,
user-visible Codex task, not a subagent. Reuse this task for future issues and do not spawn
subagents or steer peer specialist tasks.

Work only in the fixed worktree:
{role['worktree']}

Perform read-only initialization:
1. Read repository guidance, .codex/multi-agent.toml, and {role['role_file']}.
2. Confirm the current directory is the configured worktree.
3. Report the current branch, HEAD, upstream, and git status.
4. Report your owned paths, forbidden paths, verification, and dependencies.
5. Stop if the worktree is dirty or the role configuration conflicts.
6. Do not edit files, create a branch, commit, push, open a PR, or begin an issue.

{maintainer_reporting(maintainer_thread_id)}
End by confirming that you are ready for maintainer dispatch."""


def start_prompt(
    project: dict[str, Any],
    role: dict[str, Any],
    issue: str,
    branch: str,
    maintainer_thread_id: str | None,
) -> str:
    forbidden = role.get("forbidden_paths", [])
    visible = role.get("user_visible_verify", [])
    language = project.get("communication_language", "the project's default language")
    return f"""Continue in the existing independent Codex task:
{role['session_title']}

You are the {role['id']} specialist for {project['name']}. Do not spawn subagents or steer
peer specialist tasks.

Work only in the fixed worktree:
{role['worktree']}

Start issue #{issue} on branch:
{branch}

Before editing:
1. Read the repository guidance, project manifest, and {role['role_file']}.
2. Confirm the worktree is clean.
3. Fetch/prune {project['remote']}.
4. Switch to {role.get('home_branch', project['base_branch'])}.
5. Fast-forward from {project['remote']}/{project['base_branch']}.
6. Create the exact issue branch above.

Owned paths:
{bullet_lines(role.get('owned_paths', []))}

Forbidden paths:
{bullet_lines(forbidden)}

Verification:
{bullet_lines(role.get('verify', []))}

User-visible proof:
{bullet_lines(visible)}

If a required change falls outside owned paths, stop and ask the maintainer to coordinate it.
Implement, test, commit, push, and create a Draft PR against {project['base_branch']}.
Link issue #{issue}. Use {language} for human-facing status, commit, issue, and PR text.
Report the branch, commit SHA, Draft PR URL, verification, CI state, and known risks.
{maintainer_reporting(maintainer_thread_id)}
Do not print secrets or discard unexplained worktree changes."""


def cleanup_prompt(
    project: dict[str, Any],
    role: dict[str, Any],
    branch: str,
    maintainer_thread_id: str | None,
) -> str:
    return f"""Continue in the existing independent Codex task:
{role['session_title']}

The issue branch {branch} has been merged.

In the fixed worktree {role['worktree']}:
1. Confirm the issue branch has no uncommitted changes.
2. Switch to {role.get('home_branch', project['base_branch'])}.
3. Fetch/prune {project['remote']}.
4. Fast-forward to {project['remote']}/{project['base_branch']}.
5. Delete the merged local and remote issue branch after confirming merge.
6. Do not edit code, create a commit, or begin another issue.

Report the final branch, HEAD, upstream, worktree status, and branch cleanup result.
{maintainer_reporting(maintainer_thread_id)}
Keep this Codex task open for the next maintainer dispatch."""


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a specialist delegation prompt.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--role", required=True)
    parser.add_argument(
        "--mode", choices=("init", "start", "cleanup"), default="start"
    )
    parser.add_argument("--issue")
    parser.add_argument("--branch")
    parser.add_argument("--maintainer-thread-id")
    args = parser.parse_args()

    try:
        with args.manifest.open("rb") as handle:
            data = tomllib.load(handle)
    except (FileNotFoundError, tomllib.TOMLDecodeError) as error:
        print(f"Cannot read manifest: {error}", file=sys.stderr)
        return 2

    project = data.get("project", {})
    role = find_role(data, args.role)
    if role is None:
        print(f"Unknown role: {args.role}", file=sys.stderr)
        return 2

    if args.mode == "init":
        print(init_prompt(project, role, args.maintainer_thread_id))
    elif args.mode == "start":
        if not args.issue:
            print("--issue is required in start mode", file=sys.stderr)
            return 2
        branch = args.branch or (
            f"{project.get('branch_prefix', 'codex/')}issue-{args.issue}-{args.role}"
        )
        print(
            start_prompt(
                project,
                role,
                args.issue,
                branch,
                args.maintainer_thread_id,
            )
        )
    else:
        if not args.branch:
            print("--branch is required in cleanup mode", file=sys.stderr)
            return 2
        print(
            cleanup_prompt(
                project,
                role,
                args.branch,
                args.maintainer_thread_id,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
