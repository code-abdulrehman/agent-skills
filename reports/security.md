# Security sanitization

Inspected 1955 distinct packages. Sanitized 2550 source-comparable files; 383 are included in this export. Counts include neutralizing potentially sensitive examples and do not establish that any live credential was found.

| Category | References |
| --- | ---: |
| contextual-credential-literal | 22 |
| document-author-metadata | 2 |
| documentation-network-portability-fix | 18 |
| dynamic-project-guidance | 61 |
| embedded-url-auth | 59 |
| environment-example-credential-value | 2 |
| github-runtime-identity-discovery | 1 |
| github-token | 2 |
| image-metadata-stripped | 121 |
| internal-domain | 40 |
| local-filesystem-path | 216 |
| personal-account | 4 |
| personal-email | 1 |
| personal-name | 1 |
| private-ip | 130 |
| project-specific-reference | 159 |
| relative-reference-portability-fix | 15091 |

All files were inspected as text, supported structured assets, or binary strings/metadata. Image OCR, archive inspection, contextual credential detection, base64 inspection, entropy triage, known-identity matching, and targeted token patterns complemented each other. Unsupported or unresolved assets and instruction risks were excluded. No third-party security scanner was available. No scan proves absence of every possible secret or malicious behavior.

The export contains no known original account identifiers or credentials after the final checks. Public upstream authors and attribution are intentionally preserved. Authentication and external integrations were not exercised.

Reference counts include example redactions and portability fixes, not confirmed leaked live secrets. `summary.json` separates sensitive-reference sanitization from all modifications. Relative-link repair counts may include repeated repair attempts during iterative validation.

Project workflow revision: 11 variants added and one existing package updated after reviewing 68 adapted files. See `project-skills.md` for the checks, runtime diagnostic changes, and explicit redistribution authorization. Baseline source-comparison counts above describe the initial collection pass.

Final export recheck after the project-workflow revision found no matches for the tested known-private-identity and credential patterns in publishable files, and verified all 532 package manifests. User-created root `.git` administration is local repository state and is excluded from exported-file scans; it was preserved. No source Git history was imported and no commit or push was performed.

Two original Orca adapters add six text/script files. Their wrapper never evaluates shell source, changes runtime state, or prints raw failed-command output. Vendor guides are read locally and not bundled in this export.

Current Orca-adapter revision: all 534 catalog packages passed integrity preflight, and the tested known-private-identifier and credential patterns returned no findings in the publishable files. The README’s copyable prompt requires an explicitly supplied repository URL and cleanup of only the newly created temporary clone.
