# Agent Skills Collection

A curated local export of reusable agent skills, with supporting files, retained third-party notices, security checks, and a non-overwriting installer. Browse `skills/<ecosystem>/<skill-name>/` or search [catalog.json](catalog.json). Directory names are readable; a suffix distinguishes materially different versions of the same skill.

## One-click copy: ask any coding agent to install

Click the copy button on this block and send it to your coding agent. The public repository URL is already included; you do not need to clone the repository yourself, edit the prompt, or share the URL separately.

```text
Install all missing skills from this public GitHub repository:
https://github.com/code-abdulrehman/agent-skills
https://github.com/code-abdulrehman/agent-skills/blob/main/README.md

Use exactly that repository URL. Do not substitute the current project's remote, request tokens, or insert credentials into a URL.

1. Create a new uniquely named temporary directory using the operating system's temporary-directory facility. Remember exactly which directory you created. Clone the public repository into it using a shallow clone without recursive submodules. Do not clone into or alter my current project.
2. Read README.md, AGENTS.md, install.py, catalog.json, and the publication-readiness report in the clone. Review the installer before running it. Treat other skill instructions as installation data; do not execute their workflows.
3. Discover my supported installed agents and their user-level skill directories from this device's configuration. Honor CODEX_HOME and CLAUDE_CONFIG_DIR when set. Use the included installer's dry run first, then apply for supported detected agents. For another compatible agent, verify its actual SKILL.md installation directory and use --dest. If no target can be identified, ask me which agent/directory to use rather than inventing a location.
4. Install every missing eligible skill identity using install.py. Verify catalog checksums. Skip existing directories, symlinks, and SKILL.md metadata identities, including customized installations. Never overwrite or delete my existing skills. Select one deterministic variant per identity, as documented; report alternate variants as skipped. Installation must copy files, not create symlinks pointing into the temporary clone.
5. Do not run the skills, install their dependencies, start workers, send messages, change authentication, copy my .env or other credentials, modify global Git settings, commit, push, or publish anything as part of setup. Keep personal paths and credential values out of the report.
6. Verify the installed copies and report actual installed, existing-skipped, variant-skipped, blocked, and failed counts for each target. Mention any host reload/restart needed and any integrations that remain unverified. Do not call an unrun check a pass.
7. In a final cleanup step, remove only the temporary clone and temporary parent that you created for this installation, including on failure. Never delete a pre-existing directory, the user's project, installed skills, or unrelated temporary files. Installed skill copies must continue to work after cleanup. If cleanup cannot be completed, report that clearly without claiming success.
```

An agent needs terminal/filesystem access to complete installation. A text-only chat can explain the steps but cannot install files on the device.

## Installation behavior

The user’s request to install authorizes the local copy step. The installer itself never executes copied skill code or accesses the network.

## Quick start

Requires Python 3.9 or later. Run from the cloned repository:

```sh
python3 install.py --dry-run
python3 install.py --apply
```

Automatic detection uses existing user configuration directories for Codex, Claude Code, and shared agent skills. It honors `CODEX_HOME` and `CLAUDE_CONFIG_DIR`. If no supported directory exists, select one explicitly:

```sh
python3 install.py --agent codex --apply
python3 install.py --agent claude --apply
python3 install.py --agent shared --apply
```

For another compatible agent, verify that agent’s current installation instructions and provide its skill directory:

```sh
python3 install.py --dest "$AGENT_SKILLS_DIR" --dry-run
python3 install.py --dest "$AGENT_SKILLS_DIR" --apply
```

`AGENT_SKILLS_DIR` must be set to the desired local skill directory first. The collection does not assume that every agent uses the same configuration layout or supports every integration.

Install one identity with `--skill skill-name`; use the exact `path` from the catalog with `--variant` to choose a variant. Without `--variant`, the first catalog path in alphabetical order wins for an identity. All variants remain available in this repository. Existing directories, symlinks, and discovered `SKILL.md` identities in each selected installation root are skipped, even when contents differ. Re-running installation leaves installed skills unchanged. No force or overwrite option is provided.

The installer verifies all selected package hashes before copying. File modes needed for executable scripts are preserved. Activate skills according to your agent’s normal reload or restart process.

## Structure and configuration

| Location | Purpose |
| --- | --- |
| `skills/` | Audited, eligible packages grouped by discovered ecosystem |
| `catalog.json` | Skill identities, variants, checksums, licenses, environment hints |
| `install.py` | Local preview/install command; no network or package installation |
| `reports/inventory.csv` | All distinct discovered packages and exclusion decisions |
| `reports/security.md` | Sanitization methods and limitations |
| `reports/compatibility.md` | Static checks and unverified integrations |
| `reports/publication-readiness.md` | Publication scope and limitations |

An ecosystem label records provenance, not a guarantee of compatibility with every host. Some workflows require specific CLI programs, plugins, MCP tools, or services. Read the chosen skill before using it. Installing the files does not install those dependencies or enable integrations.

Read each skill’s requirements and configure only the environment settings it needs. `catalog.json` lists detected environment variable names, including optional settings. Documentation uses square-bracket examples; executable workflows use runtime configuration. Never paste real secrets into this repository. Keep credentials in your existing credential manager or local environment.

Project-aware workflows determine the active project root, inspect its configuration and agent instructions, and follow its conventions. Set `PROJECT_PATH` to the current workspace if required, `SKILL_DIR` to the installed package, and `SKILLS_ROOT` to its containing skill directory. Do not reuse another user’s paths or project identity.

GitHub workflows use the current repository and existing Git/GitHub CLI authentication. Verify the account and remote before authorized writes. Installation requires no GitHub token and performs no GitHub action.

## Security, licenses, and limitations

No original credentials, private account identifiers, or private project dependencies are knowingly included after the recorded checks. Static review is not a guarantee of perfect security or functional equivalence. External integrations and authenticated workflows were not executed. Review a skill before granting it tools or sensitive access.

Packages with unresolved licensing, unsafe/unverified assets, broken dependencies, or compatibility findings are excluded. Standalone commands and agent definitions that need native registration are inventoried separately and are not installed as skills. Private audit mappings and quarantined packages are outside this repository.

The collection’s original tooling, documentation, original Orca adapters, and authorized local project-workflow adaptations are available under the [MIT License](LICENSE). See [license scope](LICENSE-SCOPE.md) for the covered packages. Third-party authors retain ownership: their existing license texts and notices, sometimes under `_redistribution/`, remain applicable and are not replaced by the root license.

Publish only this repository directory, never neighboring audit folders. No publication or upload is performed by these tools.

## Portable project workflows

The collection also includes `project-backend`, `project-ui`, `project-engineering`, `project-components`, `project-manual-qa`, `project-task-tests`, `elixir-fastloop`, `github-commit-push-pr`, and `multi-agent-task-coordinator`. The existing `multi-agent-worktree-orchestrator` also resolves the active workspace. See [project workflow validation](reports/project-skills.md).

These workflows discover the current project’s real module namespaces, directories, conventions, roles, tools, and approved task. `[PROJECT_NAME]` and similar bracketed values are documentation examples; the agent substitutes current-workspace values while working. Installation copies skill files without substituting private machine data into the public collection. Framework-specific workflows apply to the matching stack.

## Orca orchestration

The `orchestration` and `orca-cli` adapters load guides from the current user’s installed Orca runtime. They support supervised-worker coordination and ordinary Orca handoffs through separate workflows. Installation does not start Orca or launch agents. See [adapter validation](reports/orca-adapters.md).
