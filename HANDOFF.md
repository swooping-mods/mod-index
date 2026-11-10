# Current milestone: existing Mod Index repository

Objective: publish the prepared index to the user's existing `swooping-mods/mod-index` repository and rename the local checkout to `mod-index`.

Decisions: use `https://github.com/swooping-mods/mod-index.git` as `origin`, preserve the destination's public visibility, and publish `main` without replacing any remote history. The existing remote was verified empty before the initial push. Keep the current Moon Sweepers schemas, 52 development entries and published-only output unchanged. Rename the local directory, documentation and CI candidate artifact; do not create another repository or assign a project license.

State: the normal local checkout is now `~/workspace/mod-index`, with its Git history and ignored evidence preserved. Source checks and catalog generation cover all 52 entries. Five focused checks pass. The push targets the existing repository; final SHA, visibility and CI verification is recorded in `artifacts/organization-push.json`.

Next action: continue index changes in this checkout. Real Nexus release references and loader consumption of the hosted index remain separate work; the generated published index remains empty until actual releases are assigned.

Evidence: `verification/organization-push.md`; `artifacts/organization-push.json`; `artifacts/checks.json`; `artifacts/index.json`; `artifacts/SHA256SUMS`; `vendored/extraction.json`; `specs/_readme.md`.
