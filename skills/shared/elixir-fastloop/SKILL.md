---
name: elixir-fastloop
description: "Diagnose and improve Elixir/Phoenix compile and test feedback in the current workspace, with cooperative build locking, measured CPU limits, warm builds, and explicitly isolated test databases."
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

# Codex Elixir Fastloop — do not delete caches to gain CPU speed

**Outcome:** Minimize the time from an edit to a trustworthy result on the current machine. Measure available CPU, memory pressure, and competing work before choosing concurrency; do not assume a particular CPU model, operating system, core count, or RAM size.

## Trigger and initial triage

1. Identify the Git worktree path (`git rev-parse --show-toplevel`), confirm app root with `mix.exs`, Elixir/OTP version, active Phoenix server, current test DB name and current `MIX_ENV`/`ERL_FLAGS`/`MIX_BUILD_ROOT`/`MIX_BUILD_PATH`/`MIX_DEPS_PATH`.
2. Distinguish **cold dependency compilation**, **project incremental recompilation**, **test file loading**, **DB/test startup**, **slow test execution**, and **a compilation lock wait**. Count test *cases* vs test *files*: 600 cases does not imply 600 parallelizable modules.
3. Check CPU/memory pressure and active beam processes (`python3 "$FASTMIX" doctor --cwd "$PROJECT_PATH"`; Activity Monitor for real memory pressure). Do **not** delete a PID lock, `mix.lock`, `_build`, `deps`, or kill BEAM processes just to dismiss lock messages. First check actual process ownership with `ps -p PID -o pid,ppid,etime,%cpu,command`.
4. IMPORTANT: Mix 1.19+ already has an OS compilation lock (`MIX_OS_CONCURRENCY_LOCK` must remain enabled). A wait indicates conflicting builds sharing a path; solve **ownership and scheduling**, never switch lock off. Git worktrees isolate checkout trees but may still share `MIX_BUILD_ROOT`, `MIX_DEPS_PATH`, PostgreSQL databases and ports.
5. Use the active project’s available ownership/scheduling workflow. The wrapper’s coordination is cooperative and applies only to processes using the same configured lock state.

## Fast diagnostic before editing optimization flags

Run from the exact worktree needing optimization:

```bash
FASTMIX="${SKILL_DIR:?Set SKILL_DIR to the installed elixir-fastloop directory}/scripts/fastmix.py"
python3 "$FASTMIX" doctor --cwd "$PWD"
# AFTER a small code change, profile before another tool has already recompiled it:
python3 "$FASTMIX" profile --cwd "$PWD" --schedulers 5
MIX_ENV=test mix xref graph --label compile-connected --format stats --no-compile
MIX_ENV=test mix xref graph --label compile --sink lib/path/to/changed.ex --only-nodes --no-compile
```

The xref commands read the existing compile manifest without starting another compile. Check fanout before editing shared macros or schemas; a file with hundreds of compile dependents can turn a small edit into a large rebuild. Watch for generated routes, config changes, `@external_resource`, expensive `__mix_recompile__?/0`, changing OTP/Elixir versions or build paths. Never introduce `mix clean` or `--force` into the normal edit/test loop. `mix xref trace lib/...ex` gives a reason for compile-time dependencies. Profile/test output is evidence; a guess about hundreds of recompiles is not.

For a large incremental rebuild or a scheduler benchmark, read `references/why-recompile.md` before changing compilation settings.

## Choose the smallest setup that satisfies the task

Before running setup, check whether `deps`, `_build/test`, and `assets/node_modules` already exist. A warm test loop needs only the focused `fastmix test` command below. Do not rerun `mix setup`, `npm install`, or `mix deps.get` for every code edit. Preserve build caches across Codex sessions and worktree restarts.

### Cold setup when only tests are needed

After a deliberate cache reset, fetch dependencies in the test environment and build that environment once:

```bash
FASTMIX="${SKILL_DIR:?Set SKILL_DIR to the installed elixir-fastloop directory}/scripts/fastmix.py"
MIX_ENV=test mix deps.get
python3 "$FASTMIX" compile --cwd "$PWD" --schedulers 5 --deps-partitions 2
```

Inspect the active project’s setup and test aliases before running them. Setup can compile another environment, mutate a database, or build assets; choose only the verified steps needed for the task. Measure partition behavior on the actual machine.

### Cold setup when the dev app and assets are needed

Compare the active project’s Makefile and Mix aliases for duplicated setup. Use the smallest approved path that prepares the required environment. Do not assume `mix setup`, `make setup`, or `mix test` is free of database side effects. Dev and test are separate build environments.

On a genuinely cold checkout, npm installation and asset building can run alongside the dependency fetch/dev compile because they use different outputs. Keep only one Mix compiler in a worktree at a time and use a modest scheduler count on a shared Mac. Do not start another full setup or erase caches to benchmark the change. Compare end-to-end times only under similar machine load.

## Code/test loop (no repeated redundant compile)

**Every agent that starts Mix commands must use the wrapper**, or native Mix locks may still force waits. Commands run in one worktree at a time with a cooperative global slot cap. `compile` uses an exclusive per-worktree lock; `test` auto-compiles when known source inputs change and runs `mix test --no-compile` only after a verified successful warm test build. The warm check compares file metadata first, then hashes content if metadata differs; it never skips a changed source file solely because size or modification time matches.

```bash
FASTMIX="${SKILL_DIR:?Set SKILL_DIR to the installed elixir-fastloop directory}/scripts/fastmix.py"
python3 "$FASTMIX" compile --cwd "$PWD" --schedulers 5
python3 "$FASTMIX" test --cwd "$PWD" --schedulers 3 --max-cases 3 --max-requires 3 -- test/my_feature_test.exs
python3 "$FASTMIX" test --cwd "$PWD" -- --failed
# Initial --stale run can run the whole suite; later it narrows test files:
python3 "$FASTMIX" test --cwd "$PWD" -- --stale
```

Use Python 3.10 or newer. In an asdf worktree without a selected Python version, choose an installed version for the command with `ASDF_PYTHON_VERSION` rather than changing the project's `.tool-versions`.

For a single focused test in a project whose `config/test.exs` builds its database name from `MIX_TEST_PARTITION`, use `test --test-db-suffix <unique digits> -- <test file>` after checking the effective database name. This sets the variable for that test run without enabling ExUnit shards. Keep the suffix unique across active worktrees; the wrapper checks only for the variable's presence in config, not the resulting database name.

`--max-cases` schedules async **test modules**, not individual test cases within a module. `--max-requires` controls concurrent test-file loading/compilation. Keep `use ExUnit.Case, async: true` only for tests safe under concurrency. `--trace` and `--slowest` change concurrency: benchmark ordinary invocations separately. `test --no-compile` is for fast LOCAL feedback, not a substitute for standard CI/integration builds; external generators and custom compilers may invalidate cache outside the watch set.

When **dependencies** actually need recompilation, Elixir 1.19+ can compile independent dependencies across OS processes:

```bash
python3 "$FASTMIX" compile --cwd "$PWD" --schedulers 3 --deps-partitions 2
```

Compare 1 vs 2 vs 3 dependency partitions and 3/4/5/6 Erlang schedulers on THIS machine; 30–50 workers are not a reasonable first experiment. Do not configure partitions globally for language servers/Orca.

## Full suite: partition only after database isolation is verified

1. Check existing `config/test.exs`. Each concurrently running worktree must use a unique **worktree suffix**, and each ExUnit partition a unique **partition suffix**. Example template in `references/database-isolation.md`. This is a reviewed project configuration change; do not silently modify it.
2. Create and migrate the two partition databases **explicitly**, in the `test` environment, using the same suffixes. Never share a mutable Postgres test database between worktrees. Never point test commands at production or development databases.
3. Run the **dry run** first:

```bash
python3 "$FASTMIX" shards --cwd "$PWD" --partitions 2
```

4. Only after the developer confirms correct DB isolation and pre-creates/migrates test DBs:

```bash
python3 "$FASTMIX" shards --cwd "$PWD" --partitions 2 --schedulers 3 \
  --max-cases 2 --max-requires 2 --execute --db-reviewed
```

The wrapper compiles once, then starts two `mix test --no-compile --partitions 2` processes and logs results separately. The partitioner distributes TEST FILES round-robin, not individual cases or runtime-balanced jobs. Different worktrees need their own DB suffix, not just `MIX_TEST_PARTITION=1/2`. The wrapper does not create databases or migrations and refuses shards without explicit confirmation. Its config check only detects marker text, so manually confirm the effective database names before using `--db-reviewed`. If startup overhead or memory pressure makes two partitions slower, use a single `mix test` process with async cases instead.

## Worktree/Orca and resource safety

- Orca is the multi-agent UI, not a CPU scheduler. Give each **feature implementation** its own worktree, with its own local `_build` and per-worktree test database. One agent owns the Mix write/compile phase per worktree; other readers can keep coding in other worktrees.
- The fastmix script coordinates Mac CPU slots with the earlier `aco.py run` tool when they use the same default state directory and slot count. It does not stop bare `mix` commands from running; instruct every agent to use it. Its locking is cooperative, not CPU pinning, process memory isolation or security sandboxing.
- Start with 2 global heavy-job slots: compilation weight 2, test weight 1. Don't run several Phoenix servers on the same port; never run DB schema migrations concurrently on the same database.
- Keep the warm `_build/test` cache for active or resumable worktrees. **Do not use automatic seven-day deletion of `_build` on any worktree that may resume**: that forces expensive cold compilations. Prefer age+last-used+disk-pressure-aware retention, typically 30+ days for build artifacts unless manually approved. `mix clean` and deleting dependency trees are diagnostic last resorts.
- If a PID-lock wait repeats for 10–30 minutes, gather exact PID, command, build paths, mix debug output and profile first; do not forcibly terminate unknown work.
- After local fast tests pass, have an integration owner run the standard `MIX_ENV=test mix test` (compilation enabled) and CI. The warm stamp watches common project inputs, **not every possible custom codegen or external environment change**. If caches might be stale, use standard Mix compile/test to validate before merging.

## Agent response format

Summarize root cause (measured vs hypothetical), worktree/build path ownership, parallelism settings, focused tests, compile profile observations, database/port isolation, PID diagnosis, timing comparisons, risks and which steps require permission. Prefer the smallest experiment with the highest expected wall-clock benefit. If the full suite is taking 30 minutes, do not run it repeatedly while investigating without user approval.

Diagnostic output omits raw environment values, full process command lines, and wrapper command arguments. Compiler/test subprocess output can still contain project data; keep it local and review/redact it before sharing. The process IDs remain available for local ownership checks.
