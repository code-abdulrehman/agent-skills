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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a multi-agent worktree manifest.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument(
        "--check-worktrees",
        action="store_true",
        help="Require configured worktree directories to exist.",
    )
    return parser.parse_args()


def expect_table(parent: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be a TOML table")
        return {}
    return value


def expect_string(table: dict[str, Any], key: str, prefix: str, errors: list[str]) -> str:
    value = table.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{prefix}.{key} must be a non-empty string")
        return ""
    return value.strip()


def expect_strings(
    table: dict[str, Any],
    key: str,
    prefix: str,
    errors: list[str],
    *,
    required: bool,
) -> list[str]:
    value = table.get(key)
    if value is None and not required:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        errors.append(f"{prefix}.{key} must be an array of non-empty strings")
        return []
    if required and not value:
        errors.append(f"{prefix}.{key} must not be empty")
    return [item.strip() for item in value]


def pattern_root(pattern: str) -> str:
    clean = pattern.replace("\\", "/").removeprefix("./").strip("/")
    wildcard_positions = [clean.find(char) for char in "*?[" if char in clean]
    if wildcard_positions:
        clean = clean[: min(wildcard_positions)]
    return clean.rstrip("/")


def patterns_overlap(left: str, right: str) -> bool:
    left_root = pattern_root(left)
    right_root = pattern_root(right)
    if not left_root or not right_root:
        return False
    return (
        left_root == right_root
        or left_root.startswith(right_root + "/")
        or right_root.startswith(left_root + "/")
    )


def shared_path_resolves_overlap(
    left: str,
    right: str,
    left_id: str,
    right_id: str,
    shared_paths: dict[str, Any],
) -> bool:
    left_root = pattern_root(left)
    right_root = pattern_root(right)
    overlap_root = left_root if len(left_root) >= len(right_root) else right_root
    for shared_pattern, owner in shared_paths.items():
        if owner not in (left_id, right_id):
            continue
        shared_root = pattern_root(shared_pattern)
        if shared_root and (
            overlap_root == shared_root
            or overlap_root.startswith(shared_root + "/")
        ):
            return True
    return False


def find_cycle(graph: dict[str, list[str]]) -> list[str]:
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> list[str]:
        if node in visiting:
            start = stack.index(node)
            return stack[start:] + [node]
        if node in visited:
            return []
        visiting.add(node)
        stack.append(node)
        for dependency in graph.get(node, []):
            cycle = visit(dependency)
            if cycle:
                return cycle
        stack.pop()
        visiting.remove(node)
        visited.add(node)
        return []

    for node in graph:
        cycle = visit(node)
        if cycle:
            return cycle
    return []


def main() -> int:
    args = parse_args()
    try:
        with args.manifest.open("rb") as handle:
            data = tomllib.load(handle)
    except FileNotFoundError:
        print(f"Manifest not found: {args.manifest}", file=sys.stderr)
        return 2
    except tomllib.TOMLDecodeError as error:
        print(f"Invalid TOML: {error}", file=sys.stderr)
        return 2

    errors: list[str] = []
    if data.get("version") != 1:
        errors.append("version must equal 1")

    project = expect_table(data, "project", errors)
    for key in ("name", "main_checkout", "remote", "base_branch", "branch_prefix"):
        expect_string(project, key, "project", errors)

    main_checkout = project.get("main_checkout")
    if isinstance(main_checkout, str) and not Path(main_checkout).is_absolute():
        errors.append("project.main_checkout must be an absolute path")

    coordination = expect_table(data, "coordination", errors)
    coordination_mode = expect_string(
        coordination, "mode", "coordination", errors
    )
    hub_role = expect_string(coordination, "hub_role", "coordination", errors)
    if coordination_mode and coordination_mode != "independent_codex_tasks":
        errors.append("coordination.mode must equal 'independent_codex_tasks'")
    if coordination.get("allow_subagents") is not False:
        errors.append("coordination.allow_subagents must equal false")

    maintainer = expect_table(data, "maintainer", errors)
    maintainer_id = expect_string(maintainer, "id", "maintainer", errors)
    maintainer_role_file = expect_string(
        maintainer, "role_file", "maintainer", errors
    )
    if maintainer_role_file and (
        Path(maintainer_role_file).is_absolute()
        or ".." in Path(maintainer_role_file).parts
    ):
        errors.append("maintainer.role_file must be repository-relative")
    maintainer_session_title = expect_string(
        maintainer, "session_title", "maintainer", errors
    )
    if maintainer_id and hub_role and hub_role != maintainer_id:
        errors.append("coordination.hub_role must match maintainer.id")
    maintainer_worktree = expect_string(
        maintainer, "worktree", "maintainer", errors
    )
    if maintainer_worktree and not Path(maintainer_worktree).is_absolute():
        errors.append("maintainer.worktree must be an absolute path")
    expect_strings(maintainer, "owned_paths", "maintainer", errors, required=True)
    expect_strings(maintainer, "forbidden_paths", "maintainer", errors, required=False)
    expect_strings(maintainer, "verify", "maintainer", errors, required=True)
    expect_strings(maintainer, "deploy_verify", "maintainer", errors, required=False)

    specialists_value = data.get("specialists")
    if not isinstance(specialists_value, list) or not specialists_value:
        errors.append("specialists must contain at least one table")
        specialists: list[dict[str, Any]] = []
    else:
        specialists = [
            item for item in specialists_value if isinstance(item, dict)
        ]
        if len(specialists) != len(specialists_value):
            errors.append("every specialists item must be a TOML table")

    roles: list[dict[str, Any]] = []
    if maintainer:
        roles.append({"kind": "maintainer", **maintainer})

    role_ids: set[str] = set()
    role_files: set[str] = set()
    session_titles: set[str] = set()
    worktrees: set[str] = set()
    home_branches: set[str] = set()
    graph: dict[str, list[str]] = {}

    if maintainer_id:
        role_ids.add(maintainer_id)
    if maintainer_role_file:
        role_files.add(maintainer_role_file)
    if maintainer_session_title:
        session_titles.add(maintainer_session_title)
    if maintainer_worktree:
        worktrees.add(maintainer_worktree)

    for index, specialist in enumerate(specialists):
        prefix = f"specialists[{index}]"
        role_id = expect_string(specialist, "id", prefix, errors)
        role_file = expect_string(specialist, "role_file", prefix, errors)
        if role_file and (
            Path(role_file).is_absolute() or ".." in Path(role_file).parts
        ):
            errors.append(f"{prefix}.role_file must be repository-relative")
        session_title = expect_string(
            specialist, "session_title", prefix, errors
        )
        expect_string(specialist, "purpose", prefix, errors)
        worktree = expect_string(specialist, "worktree", prefix, errors)
        home_branch = expect_string(specialist, "home_branch", prefix, errors)
        expect_strings(specialist, "owned_paths", prefix, errors, required=True)
        expect_strings(specialist, "forbidden_paths", prefix, errors, required=False)
        expect_strings(specialist, "verify", prefix, errors, required=True)
        expect_strings(specialist, "user_visible_verify", prefix, errors, required=False)
        dependencies = expect_strings(specialist, "depends_on", prefix, errors, required=False)

        if role_id in role_ids:
            errors.append(f"duplicate role id: {role_id}")
        role_ids.add(role_id)
        if role_file in role_files:
            errors.append(f"duplicate role file: {role_file}")
        role_files.add(role_file)
        if session_title in session_titles:
            errors.append(f"duplicate session title: {session_title}")
        session_titles.add(session_title)
        if worktree:
            if not Path(worktree).is_absolute():
                errors.append(f"{prefix}.worktree must be an absolute path")
            if worktree in worktrees:
                errors.append(f"duplicate worktree path: {worktree}")
            worktrees.add(worktree)
        if home_branch in home_branches:
            errors.append(f"duplicate home branch: {home_branch}")
        home_branches.add(home_branch)
        graph[role_id] = dependencies
        roles.append({"kind": "specialist", **specialist})

    for role_id, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in role_ids:
                errors.append(f"{role_id} depends on unknown role: {dependency}")
            if dependency == role_id:
                errors.append(f"{role_id} cannot depend on itself")

    cycle = find_cycle(graph)
    if cycle:
        errors.append("role dependency cycle: " + " -> ".join(cycle))

    shared_paths = data.get("shared_paths", {})
    if not isinstance(shared_paths, dict):
        errors.append("shared_paths must be a TOML table")
        shared_paths = {}
    else:
        for pattern, owner in shared_paths.items():
            if not isinstance(pattern, str) or not pattern.strip():
                errors.append("shared_paths keys must be non-empty path patterns")
            if not isinstance(owner, str) or owner not in role_ids:
                errors.append(f"shared path {pattern!r} has unknown owner {owner!r}")

    for left_index, left in enumerate(roles):
        left_id = str(left.get("id", f"role-{left_index}"))
        left_owned = left.get("owned_paths", [])
        left_forbidden = left.get("forbidden_paths", [])
        for owned in left_owned:
            for forbidden in left_forbidden:
                if patterns_overlap(owned, forbidden):
                    errors.append(
                        f"{left_id} owns {owned!r} but also forbids overlapping {forbidden!r}"
                    )
        for right in roles[left_index + 1 :]:
            right_id = str(right.get("id", "unknown"))
            for left_pattern in left_owned:
                for right_pattern in right.get("owned_paths", []):
                    if patterns_overlap(
                        left_pattern, right_pattern
                    ) and not shared_path_resolves_overlap(
                        left_pattern,
                        right_pattern,
                        left_id,
                        right_id,
                        shared_paths,
                    ):
                        errors.append(
                            f"owned path overlap: {left_id}:{left_pattern} and "
                            f"{right_id}:{right_pattern}"
                        )

    if args.check_worktrees:
        for worktree in sorted(worktrees):
            if not Path(worktree).is_dir():
                errors.append(f"worktree directory does not exist: {worktree}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        f"OK: {args.manifest} defines {len(role_ids)} roles, "
        f"{len(specialists)} independent specialist task(s), and "
        f"{len(shared_paths)} shared paths."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
