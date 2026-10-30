# Installer validation

The installer was tested locally using isolated directories outside this collection. No installed agent configuration was modified.

Seven fixture checks passed: dry-run creates no files; installation preserves executable status; repeat installation preserves customizations; metadata identity detects renamed installations; dangling destination symlinks are skipped; collection/ancestor destination paths are rejected; tampered package content is rejected before writing.

Full catalog installation: **467 identities installed**, 54 alternate variants skipped. Immediate second installation: **0 installed, 467 existing identities skipped**, 54 alternate variants skipped. All 521 catalog packages passed checksum preflight. The installer does not execute skill instructions, install dependencies, authenticate, or use the network.

This verifies local installation behavior. Host-specific activation and external workflow functionality remain unverified.

## Current project-workflow revision

After adding the portable project workflows, a fresh isolated installation copied **476 identities** and skipped 56 alternate variants. A second run copied **0**, skipped all **476 existing identities**, and skipped the 56 alternate variants. Previewing against the earlier 467-skill installation correctly proposed only 9 new identities. All 532 catalog packages passed integrity preflight. Existing installed identities remain unchanged, including older customized versions; this installer does not force updates.

## Orca adapters and copyable setup prompt

The current catalog contains 534 package variants and 478 installable identities. A fresh isolated installation copied all 478 identities and skipped 56 alternate variants; the repeat check skips all 478 existing identities. A separate local Git fixture verified shallow temporary cloning, dry-run behavior, installed copies independent of the clone, cleanup of only the owned temporary folder, and a working installed helper after clone deletion. The fixture made no external network requests or changes to the user’s repository. Public GitHub download availability was not tested.
