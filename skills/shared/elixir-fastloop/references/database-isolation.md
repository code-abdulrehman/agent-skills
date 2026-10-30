> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# PostgreSQL database isolation — REVIEW BEFORE APPLYING

A Git worktree is **not** a database namespace. Even when every feature has its own `_build`, the default Phoenix name `app_test#{System.get_env("MIX_TEST_PARTITION")}` will collide if two worktrees execute the same partition number against the same Postgres instance.

For a project with a test Repo already configured with SQL Sandbox, adapt its **existing** `config/test.exs` configuration to include both suffixes. Example only — replace `:your_app`, `YourApp.Repo` and `your_app_test`, and preserve all existing settings and secrets:

```elixir
worktree_id = System.get_env("ACO_TEST_DB_SUFFIX")
partition_id = System.get_env("MIX_TEST_PARTITION")

# Keep the existing database for plain Mix / final CI, while wrapper-driven
# worktrees use unique test DBs. Non-partitioned fastloop tests use shard 1.
test_database =
  if worktree_id do
    "your_app_test_#{worktree_id}_#{partition_id || "1"}"
  else
    "your_app_test#{partition_id}"
  end

config :your_app, YourApp.Repo,
  database: test_database,
  pool: Ecto.Adapters.SQL.Sandbox,
  pool_size: 5
```

The wrapper generates the worktree ID deterministically from its absolute checkout path. For two partitions its environments are `ACO_TEST_DB_SUFFIX=<same8chars>` and `MIX_TEST_PARTITION=1` or `2`. **This template is not installed or edited by the script.** The non-partitioned `fastmix test` uses test database shard `1`, so you only need to prepare the two named shard databases for fastloop runs. Plain `MIX_ENV=test mix test` retains the original database name for conventional integration tests.

Before running `fastmix shards --execute --db-reviewed`, the developer must inspect the actual resulting database names, review `DATABASE_URL` overrides, confirm the credentials only allow *test* database access, and create/migrate each DB in isolation. If the project uses `mix ecto.setup` aliases that reset/drop databases, **do not blindly run them**; inspect aliases first. Example one partition at a time using the exact suffix printed by `fastmix shards`:

```bash
# Replace XXXXXXXX with the printed worktree ID. Review what these aliases do first!
ACO_TEST_DB_SUFFIX=XXXXXXXX MIX_TEST_PARTITION=1 MIX_ENV=test mix ecto.create
ACO_TEST_DB_SUFFIX=XXXXXXXX MIX_TEST_PARTITION=1 MIX_ENV=test mix ecto.migrate
ACO_TEST_DB_SUFFIX=XXXXXXXX MIX_TEST_PARTITION=2 MIX_ENV=test mix ecto.create
ACO_TEST_DB_SUFFIX=XXXXXXXX MIX_TEST_PARTITION=2 MIX_ENV=test mix ecto.migrate
```

Do not run the above against production/development endpoints. Consider creating a dedicated local Postgres role with access limited to test databases. If a project uses another adapter or does not have transaction-isolated tests, investigate that adapter's supported concurrency first. `--partitions` splits **test files** among BEAM processes; it may increase RAM use, database connections and startup cost. Start with 2, not 5–50.

Official: https://hexdocs.pm/mix/Mix.Tasks.Test.html ; https://phoenix.hexdocs.pm/testing.html ; https://ecto-sql.hexdocs.pm/Ecto.Adapters.SQL.Sandbox.html
