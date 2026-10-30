> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Compilation triage checklist

## Separate the stages

- **Lock wait:** Another `mix` process may be compiling the same build path. Inspect PID and `MIX_BUILD_ROOT`/`MIX_BUILD_PATH`; native Mix OS locking prevents races. Never set `MIX_OS_CONCURRENCY_LOCK=0` to speed it up.
- **Cold dependency build:** Happens after cleaning `deps` / `_build`, changing toolchain or dependencies or switching build roots. Elixir 1.19 introduced `MIX_OS_DEPS_COMPILE_PARTITION_COUNT`; start 2 and measure memory usage.
- **Large incremental recompilation:** After a successful test build, analyze dependencies with `MIX_ENV=test mix xref graph --label compile-connected --format stats --no-compile` and `MIX_ENV=test mix xref graph --label compile --sink lib/file.ex --only-nodes --no-compile`. `mix xref trace lib/file.ex --no-compile` explains why. Files with high incoming compile dependencies should be changed sparingly. Common suspects include compile-time macro usage, `@external_resource`, expensive `__mix_recompile__?/0`, changing compilation flags and generated code.
- **Slow compile of individual file:** After editing the file, run the skill's `profile` command before another agent recompiles it. That command holds the worktree lock while profiling `mix compile.elixir`. Do not `mix clean` just to obtain a profile unless explicitly approved and you can afford a cold rebuild.
- **Test-file startup:** ExUnit loads test files in parallel; `--max-requires` controls concurrency. `--no-compile` skips application compilation but not test-file loading.
- **Slow test execution:** `mix test --slowest-modules 15` reports slow modules but changes normal test concurrency. Compare wall time of ordinary tests separately. If many tests are `async: false`, this serialization may dominate. Review Ecto SQL Sandbox and shared state before enabling `async: true`.

## Benchmark protocol

Baseline from same worktree and matching `MIX_ENV=test` and dependencies:

1. Time no-op compile / first targeted test / second targeted test separately.
2. Profile a real task edit before any agent auto-compiles it. Do not make an artificial broad change just to benchmark compilation.
3. Test schedulers 3, 4, 5, 6 (with background load controlled); avoid assuming more schedulers equals faster.
4. Run one full ExUnit process with selected `--max-cases` values, then two shards only after verifying DB isolation. Record elapsed time and all failures.
5. Compare timings at *similar system state* (memory pressure, disk free and thermal conditions). If two shards are slower, leave partitioning disabled.
6. Keep a lightweight log of results: changed source module count, compiled file count, compilation elapsed, test startup, tests elapsed, result and CPU/memory pressure.

## Important developer facts

- Erlang BEAM `+S` controls schedulers, not OS threads pinned to physical cores.
- 600 **test assertions/cases** don't reveal how many test files, modules, async groups or integration dependencies exist.
- Recompiling the *entire* app every time is unusual on current Mix unless compile dependencies, config/toolchain switches or caches explain it.
- Do not delete `.mix`, `mix.lock` or known PID marker files without understanding actual ownership; `mix.lock` pins dependencies, it is not a stale PID file.
- Elixir 1.20 has more compiler enhancements but upgrading a large existing app requires compatibility checks and benchmarks, not automatic version replacement.

Sources: https://elixir-lang.org/blog/2025/10/16/elixir-v1-19-0-released/ ; https://elixir-lang.org/blog/2026/06/03/elixir-v1-20-0-released/ ; https://mix.hexdocs.pm/Mix.Tasks.Compile.Elixir.html ; https://mix.hexdocs.pm/Mix.Tasks.Xref.html
