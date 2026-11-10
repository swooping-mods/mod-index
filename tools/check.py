#!/usr/bin/env python3
"""Check the README directory without dependencies or network access."""
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LISTING = re.compile(r"- \[([^\]]+)\]\(([^)]+)\) — (.+)")


def main():
    readme = (ROOT / "README.md").read_text("utf-8")
    category = None
    listings = {}
    categories = set()
    for line in readme.splitlines():
        if line.startswith("## "):
            category = line[3:].strip()
        if not line.startswith("- ["):
            continue
        row = LISTING.fullmatch(line)
        if not category or not row:
            raise ValueError("Listing needs a category, linked name and description: " + line)
        name, url, description = row.groups()
        if not all(value.strip() for value in (name, description)):
            raise ValueError("Incomplete listing: " + name)
        parsed = urlsplit(url)
        parts = [part for part in parsed.path.split("/") if part]
        if (parsed.scheme != "https" or not parsed.hostname or "." not in parsed.hostname
                or parsed.username or parsed.password or parsed.port or parsed.query or parsed.fragment
                or len(parts) < 2 or any(char.isspace() for char in url)):
            raise ValueError("Expected a public HTTPS repository URL: " + url)
        if parsed.hostname == "github.com" and len(parts) != 2:
            raise ValueError("Link to the repository root: " + url)
        key = url.rstrip("/").casefold()
        if key in listings:
            raise ValueError("Duplicate repository: " + url)
        listings[key] = name
        categories.add(category)
    if not listings:
        raise ValueError("The README has no mod listings")
    for document in (ROOT / "README.md", ROOT / "CONTRIBUTING.md", *sorted((ROOT / "specs").glob("*.md"))):
        for link in re.findall(r"\]\(([^)]+)\)", document.read_text("utf-8")):
            if not urlsplit(link).scheme and not link.startswith("#") and not (document.parent / link.split("#")[0]).is_file():
                raise ValueError("Missing local document: " + link)
    print(f"Index OK: {len(listings)} repository links in {len(categories)} categories; local links resolve.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        raise SystemExit(str(error))
