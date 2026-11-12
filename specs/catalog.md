# Player-facing mod directory

The repository is `swooping-mods/mod-index`; the local checkout is named `mod-index`. README.md is a plain categorized list of mod links. Each bullet has the mod name linked to its author's public repository and a short description. There are no tables, author columns, navigation menus or introduction paragraphs.

README.md is the only listing source. Categories group mods by player use, with save/server tools identified separately. Contributors edit one bullet and submit a PR. The author's repository owns downloads, installation requirements, compatibility details and gameplay support. Listing a mod does not require a Nexus page, release checksum, package format, loader affiliation or membership in Swooping Mods.

Listings are limited to the maintainer's own mods and external mods explicitly approved by the maintainer with confirmed author permission. A publicly accessible repository is insufficient on its own. MarsSweepers is the current external listing; the maintainer confirmed permission from its author. Add maintainer-owned mods when public repository links are available. Private permission correspondence stays outside the public repository.

The maintainer-owned API and desktop loader are listed under Modding tools.
The 60 maintainer-owned repositories transferred from nexus-modding are listed
only after their public main commits were verified. Categories retain their
package classification, with save/server tools, developer tests and historical
experiments identified separately. The native Mars Planet experiment is separate
from the approved external MarsSweepers project. Repository listings do not imply
that a GitHub Release or Nexus page exists, or establish gameplay qualification.

Source repositories may advance beyond a retained tested package. Listing
review preserves that distinction and leaves exact game/profile requirements,
framework dependencies and deferred build/runtime/save/co-op gates with the
owning repository. A source sync or API/loader update does not establish a new
mod release or extend compatibility. Private Workshop candidates stay unlisted
until their actual public repositories and inclusion approval exist.

`CONTRIBUTING.md` and the issue/PR templates explain listing additions and corrections. The index contains no mod source, payloads, generated catalog, dependency graph or release pipeline. The former 52 development-only records had no public repository links; they are retained in Git history rather than presented as downloadable mods.

`python3 tools/check.py` checks that listings are categorized, include a mod name, repository URL and description, use HTTPS repository links without credentials or query strings, and do not duplicate URLs. It also checks local Markdown links. The single CI workflow runs that same standard-library script without installing dependencies. It does not download mods, probe remote URLs or publish artifacts.

Listing review must establish ownership or author permission, maintainer approval and public repository availability. The automated check validates structure and links; it cannot establish permission. Mod functionality and combined compatibility were not tested. Local handoff and verification receipts belong outside the repository, following AGENTS.md.
