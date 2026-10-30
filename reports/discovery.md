# Discovery coverage and duplicate resolution

Discovery inspected accessible home directories (including hidden agent configuration, projects, downloaded collections, plugin caches, and symlink registrations), macOS application resources, shared Application Support locations, shared user directories, shared package locations, and resolved agent executable bundles. Both ripgrep and native filesystem discovery were used. Skill entrypoints and recognized standalone command/agent registrations were inventoried; arbitrary documents mentioning skills were not accepted.

Large dependency/build caches, virtual environments, version-manager dependency trees, backups, OS data, private mail/message/photo stores, application sandboxes, logs, and unrelated operating-system files were excluded. Relevant global agent package locations inside otherwise excluded version-manager trees were checked separately. These boundaries can hide unconventional installations. Permissions were respected and no controls were bypassed. Eight permission/I/O messages occurred during broad discovery; complete machine coverage cannot be guaranteed. Source paths and raw diagnostics are kept only in the restricted audit workspace.

Content hashes covering relative file paths, file content, and executable status were used to collapse identical packages. The first stable, license-eligible identical source was preferred. Materially different versions remain distinct. Directory suffixes prevent collisions; metadata retains the sanitized identity. The installer selects one deterministic variant per identity and never replaces an existing installation.

Found 10394 skill occurrences, 565 standalone commands, and 17 agent definitions: 10976 total occurrences, 1955 distinct packages, 9021 redundant occurrences. Exported 532 skill variants.

| Ecosystem | Discovered occurrences | Exported variants |
| --- | ---: | ---: |
| application-bundled | 47 | 1 |
| claude-code | 123 | 31 |
| codex | 1569 | 95 |
| cursor | 95 | 56 |
| gemini | 60 | 35 |
| harness | 2 | 1 |
| openclaw | 1 | 0 |
| opencode | 4 | 2 |
| shared | 9075 | 300 |

All exclusions are listed in inventory.csv. An excluded package can have several overlapping reasons. Missing/unclear redistribution evidence alone excludes a package; source licenses were not invented. No source installations were intentionally changed. Live marketplace updates were observed while auditing, so point-in-time hashes and availability could change externally.

Later project-workflow additions are described in `project-skills.md`; the ecosystem table above records the initial export, and `summary.json` contains the current counts. Original discovery and duplicate counts are unchanged.
