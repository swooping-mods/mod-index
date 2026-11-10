# Mod Index

Static catalog metadata for Moon Sweepers mods in the Swooping Mods organization. Repository: [swooping-mods/mod-index](https://github.com/swooping-mods/mod-index). The local checkout is named `mod-index`.

Nexus Mods is the intended main player portal. This repository owns mod identities, dependency links and published release references. It does not own mod source, mod build pipelines or downloadable payloads. Code and gameplay issues belong in the API, loader or individual mod repository; catalog corrections belong here.

`catalog/` contains metadata migrated from the current development catalog. Every migrated entry is explicitly marked `development`, with `source`, `nexus` and `release` set to null because public destinations have not been selected. Existing development version strings are retained only where supplied. This is an inventory, not a claim that these mods are published or generally compatible.

```sh
python3 tools/check.py
python3 tools/catalog.py --build
```

Use installed Python 3.11+; no dependency installation is required. Building validates all entries and emits `artifacts/index.json` plus SHA256SUMS. Only `published` entries enter the public index, so the initial output intentionally contains no downloadable mods.

A published entry needs its source repository, canonical Nexus mod page, actual Nexus file ID, package filename, version, archive SHA-256 and supported game-build label. Dependencies must exist, be cycle-free and be published before a dependent mod is included. Checks run offline and do not prove remote URL availability or package contents.

Make catalog changes through GitHub PRs after the matching Nexus upload succeeds. The loader currently imports local packages; consuming this hosted index remains a separate integration step. [specs/_readme.md](specs/_readme.md) defines the format; [HANDOFF.md](HANDOFF.md) records the local milestone. No project license is assigned.
