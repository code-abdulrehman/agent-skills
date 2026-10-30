#!/usr/bin/env bash
set -eu

root="${1:-.}"
root="$(cd "${root}" && pwd)"

printf 'repository_root=%s\n' "${root}"

if git -C "${root}" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf 'git_branch=%s\n' "$(git -C "${root}" branch --show-current)"
  printf 'git_head=%s\n' "$(git -C "${root}" rev-parse HEAD)"
  printf 'git_status_begin\n'
  git -C "${root}" status --short --branch
  printf 'git_status_end\n'
  printf 'git_worktrees_begin\n'
  git -C "${root}" worktree list --porcelain
  printf 'git_worktrees_end\n'
else
  printf 'git_repository=false\n'
fi

printf 'top_level_begin\n'
find "${root}" -mindepth 1 -maxdepth 1 \
  ! -name .git \
  ! -name node_modules \
  ! -name .venv \
  -print | sort
printf 'top_level_end\n'

printf 'architecture_files_begin\n'
find "${root}" -maxdepth 4 \
  \( -type d \( \
    -name .git -o \
    -name node_modules -o \
    -name vendor -o \
    -name .venv -o \
    -name dist -o \
    -name build -o \
    -name target -o \
    -name coverage \
  \) -prune \) -o \
  \( -type f \( \
    -name AGENTS.md -o \
    -name package.json -o \
    -name pnpm-workspace.yaml -o \
    -name go.mod -o \
    -name pyproject.toml -o \
    -name Cargo.toml -o \
    -name pom.xml -o \
    -name build.gradle -o \
    -name build.gradle.kts -o \
    -name Dockerfile -o \
    -name docker-compose.yml -o \
    -name docker-compose.yaml -o \
    -name compose.yml -o \
    -name compose.yaml \
  \) -print \) | sort
printf 'architecture_files_end\n'

printf 'ci_files_begin\n'
find "${root}/.github/workflows" -maxdepth 1 -type f -print 2>/dev/null | sort || true
find "${root}/.gitlab" -maxdepth 2 -type f -print 2>/dev/null | sort || true
printf 'ci_files_end\n'

printf 'test_surfaces_begin\n'
find "${root}" -maxdepth 4 \
  \( -type d \( \
    -name .git -o \
    -name node_modules -o \
    -name vendor -o \
    -name .venv -o \
    -name dist -o \
    -name build -o \
    -name target -o \
    -name coverage \
  \) -prune \) -o \
  \( -type d \( \
    -name test -o \
    -name tests -o \
    -name __tests__ -o \
    -name spec -o \
    -name e2e \
  \) -print \) | sort
printf 'test_surfaces_end\n'
