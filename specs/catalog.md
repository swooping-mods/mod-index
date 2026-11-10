# Catalog format and published output

The owning repository is `swooping-mods/mod-index`, with the local checkout named `mod-index`. This rename does not change the Moon Sweepers catalog schemas or publication rules.

`catalog/<id>.json` uses `moon-mod-index-entry/v1`. The filename must match its lowercase hyphenated ID (at most 64 characters). Required metadata includes `name`, `summary`, `kind` (`native` or `companion`), `version` (nullable in development), `requires`, `conflicts`, `supported_builds`, `status`, `source`, `nexus` and `release`.

The initial 52 entries preserve project-owned names/summaries, kind, explicit development versions and dependency/conflict IDs from the development catalog. Native entries retain the development target `steam-windows-il2cpp-1.0.5`; this label is not fresh game qualification or a substitute for package executable hashes. Absent development versions stay null.

Development entries have `status: development` and no source/Nexus/release endpoints. They are excluded from the generated public index. A published entry requires an explicit semantic version, nonempty supported-build labels, canonical HTTPS GitHub source repository, canonical `www.nexusmods.com/<game>/mods/<id>` page, and `release` containing a portable `.msmod` `filename`, lowercase archive `sha256` and positive integer `nexus_file_id`.

Dependencies must exist and be acyclic. A published mod cannot depend on an unpublished mod. Conflict IDs must identify existing entries. These checks validate catalog structure; the package manifest and loader resolver remain authoritative for binary compatibility and hook arbitration.

`tools/catalog.py --build` validates all metadata, emits only published entries in ID order as `artifacts/index.json` (`moon-mod-index/v1`), and records SHA256SUMS. Output is deterministic and contains no timestamps or local paths. The initial published list is empty because no new public releases have been assigned. Build/check code uses only the Python standard library and no network.

Verification: `python3 tools/check.py` covers the migrated inventory, valid/missing release identity, duplicate IDs, missing/cyclic dependencies, publication dependency closure, unknown conflicts and invalid checksums/file IDs/filenames. CI checks source on PR/push and can retain a candidate manually. It does not publish or create catalog PRs. Remote URL availability, downloaded payload integrity and loader integration require future separate checks.
