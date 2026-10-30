# Compatibility and functionality

Only packages with present entrypoints, preserved support files, clear permissive license evidence or explicit source-maintainer redistribution authorization, passing available syntax checks, and no unresolved local links or security flags are exported. See `inventory.csv` for every distinct package and exclusion reason.

Exported static parser results: `{"javascript:passed": 19, "json:passed": 33, "python:passed": 219, "shell:passed": 31, "toml:passed": 3, "xml:passed": 96, "yaml:passed": 728}`.

Python AST, shell parse-only, Node parse-only, JSON, YAML, TOML, and XML checks were used where applicable. No copied workflow was executed. TypeScript, framework-specific languages, authenticated services, host plugins/MCP tools, production operations, and end-to-end behavior remain unverified. Environment dependencies are recorded per skill in `../catalog.json`; consult the skill for semantics. A catalog environment variable can be an optional setting rather than a requirement.

Project-dependent guidance resolves the current workspace and its conventions. GitHub workflows use current Git/CLI authentication. Distinct variants are retained with a directory suffix while their original sanitized skill identity remains in metadata. The installer chooses one deterministic variant per identity and skips installed identities.

Per-exported-skill parser results and environment hints are in `skill-validation.csv`; duplicate resolution is in `duplicates.csv`. The catalog contains 534 variants representing 478 distinct installable identities.

Orca adapters passed local guide retrieval only; operational orchestration remains unverified and needs the installed Orca runtime.
