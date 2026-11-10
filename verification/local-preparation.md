# Local preparation verification

Date: 2026-11-10. Target: `swooping-mods/moon-sweepers-mod-index`. Source is a selected first-party extraction, with source byte identities under `vendored/extraction.json`.

Outcome: 5 focused tests pass, with no skipped or excluded tests in the final local run. All 52 development entries validate, including dependency/conflict references. Publication guards, release identity, duplicate/missing/cyclic dependencies and invalid file metadata are checked. The generated published-only index has zero entries, matching the absence of assigned public releases.

All Python files parse. Both workflow YAML files parse and reference full action commit pins with read-only repository permissions. This is local structural review, not an actual GitHub Actions run. Source hygiene review found no game/compiled/asset payloads, private absolute paths, personal remote references or common credential/private-key markers in the source tree. Generated outputs are ignored. Specs routing links resolve to existing files.

Evidence: `artifacts/checks.json`, `artifacts/index.json`, `artifacts/SHA256SUMS`. Generated evidence is retained locally under ignored `artifacts/`; it is not part of the new source repository's initial history.

Limits: no game, Wine, native Windows or co-op replay; no GitHub-hosted CI execution; no Nexus upload or URL liveness checks. The loader's current-game adapter and legacy ABI are preserved, not newly gameplay-qualified. No external dependencies were downloaded, organization repositories/remotes created, pushes performed or PRs opened.
