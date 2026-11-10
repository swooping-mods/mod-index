# Existing Mod Index repository publication

Date: 2026-11-10. The user identified `https://github.com/swooping-mods/mod-index` as the existing index repository and authorized changing the local folder/remote and pushing it.

GitHub CLI metadata confirms the destination exists and is public. Git reference inspection and the GitHub branches API both showed no remote branches before publication. The existing visibility is preserved, and no new repository is created.

The local checkout was renamed from `moon-sweepers-mod-index` to `mod-index` with its Git history and ignored artifacts intact. `origin` points at `https://github.com/swooping-mods/mod-index.git`. The README, specs routing title and release-candidate artifact use the new name. The catalog schemas, 52 development entries and published-only output are unchanged.

Verification: `python3 tools/check.py` and `python3 tools/catalog.py --build`; source/secret-marker review, workflow syntax/full action pins, specs links, staged whitespace and tracked-output exclusions. Five focused tests pass and the generated index has zero published entries. Final local/remote `main` SHAs, public visibility, tracking and hosted CI status are recorded in ignored `artifacts/organization-push.json`.

Limits: offline catalog checks do not prove Nexus URL availability, download integrity or loader integration. No Nexus release, gameplay replay, PR, license, force push or dependency installation is included.
