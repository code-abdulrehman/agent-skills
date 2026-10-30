#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
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


def run_git(worktree: Path, *args: str) -> tuple[int, str]:
    result = subprocess.run(
        ["git", "-C", str(worktree), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    output = result.stdout.strip() or result.stderr.strip()
    return result.returncode, output


def inspect(
    role_id: str,
    session_title: str,
    worktree_value: str,
) -> dict[str, Any]:
    worktree = Path(worktree_value)
    result: dict[str, Any] = {
        "role": role_id,
        "session_title": session_title,
        "worktree": str(worktree),
        "exists": worktree.is_dir(),
    }
    if not worktree.is_dir():
        result["healthy"] = False
        result["error"] = "worktree directory does not exist"
        return result

    branch_code, branch = run_git(worktree, "branch", "--show-current")
    head_code, head = run_git(worktree, "rev-parse", "HEAD")
    status_code, status = run_git(worktree, "status", "--short")
    upstream_code, upstream = run_git(
        worktree,
        "rev-parse",
        "--abbrev-ref",
        "--symbolic-full-name",
        "@{upstream}",
    )

    result.update(
        {
            "branch": branch if branch_code == 0 else None,
            "head": head if head_code == 0 else None,
            "upstream": upstream if upstream_code == 0 else None,
            "clean": status_code == 0 and status == "",
            "status": status,
            "healthy": branch_code == 0 and head_code == 0 and status_code == 0,
        }
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Report configured worktree state.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    try:
        with args.manifest.open("rb") as handle:
            data = tomllib.load(handle)
    except (FileNotFoundError, tomllib.TOMLDecodeError) as error:
        print(f"Cannot read manifest: {error}", file=sys.stderr)
        return 2

    roles = [data.get("maintainer", {})] + data.get("specialists", [])
    reports = [
        inspect(
            str(role.get("id", "unknown")),
            str(role.get("session_title", "")),
            str(role.get("worktree", "")),
        )
        for role in roles
        if isinstance(role, dict)
    ]

    if args.as_json:
        print(json.dumps(reports, indent=2))
    else:
        for report in reports:
            state = "clean" if report.get("clean") else "dirty"
            if not report.get("exists"):
                state = "missing"
            elif not report.get("healthy"):
                state = "invalid"
            print(
                f"{report['role']}: {state} "
                f"session={report.get('session_title') or '-'} "
                f"branch={report.get('branch') or '-'} "
                f"head={(report.get('head') or '-')[:12]} "
                f"upstream={report.get('upstream') or '-'} "
                f"worktree={report['worktree']}"
            )
            if report.get("status"):
                for line in str(report["status"]).splitlines():
                    print(f"  {line}")

    return 0 if all(
        report.get("healthy") and report.get("clean") for report in reports
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
