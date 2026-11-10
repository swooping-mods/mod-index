#!/usr/bin/env python3
"""Validate local catalog metadata and emit a published-only index, without network access."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
VERSION = re.compile(r"\d+\.\d+\.\d+(?:-[a-z0-9.]+)?")


def text(value, field):
    if not isinstance(value, str) or not value.strip() or len(value) > 8000:
        raise ValueError("Invalid " + field)


def version(value):
    return isinstance(value, str) and bool(VERSION.fullmatch(value))


def url(value, host):
    if not isinstance(value, str):
        raise ValueError("Missing " + host + " URL")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or parsed.netloc != host or parsed.query or parsed.fragment:
        raise ValueError("Expected a canonical HTTPS " + host + " URL")
    return parsed.path


def validate(entries):
    by_id = {}
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("schema") != "moon-mod-index-entry/v1":
            raise ValueError("Invalid catalog entry schema")
        name = entry.get("id")
        if not isinstance(name, str) or len(name) > 64 or not ID.fullmatch(name) or name in by_id:
            raise ValueError("Invalid or duplicate catalog ID")
        by_id[name] = entry
        for field in ("name", "summary"):
            text(entry.get(field), field)
        if entry.get("kind") not in ("native", "companion"):
            raise ValueError("Invalid mod kind")
        if entry.get("status") not in ("development", "published"):
            raise ValueError("Invalid publication status")
        if entry.get("version") is not None and not version(entry["version"]):
            raise ValueError("Invalid version")
        for field in ("requires", "conflicts"):
            values = entry.get(field)
            if not isinstance(values, list) or any(not isinstance(v, str) or not ID.fullmatch(v) or v == name for v in values) or len(values) != len(set(values)):
                raise ValueError("Invalid " + field)
        builds = entry.get("supported_builds")
        if not isinstance(builds, list) or any(not isinstance(b, str) or not b for b in builds):
            raise ValueError("Invalid supported builds")
        if entry["status"] == "development":
            if any(entry.get(field) is not None for field in ("source", "nexus", "release")):
                raise ValueError("Development entries cannot claim published endpoints")
            continue
        if not version(entry.get("version")) or not builds:
            raise ValueError("Published entry needs a version and supported build")
        source = url(entry.get("source"), "github.com")
        if not re.fullmatch(r"/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", source):
            raise ValueError("Source URL must identify one repository")
        nexus = url(entry.get("nexus"), "www.nexusmods.com")
        if not re.fullmatch(r"/[a-z0-9]+/mods/[1-9][0-9]*", nexus):
            raise ValueError("Nexus URL must identify one mod page")
        release = entry.get("release")
        if not isinstance(release, dict) or not isinstance(release.get("sha256"), str) or not re.fullmatch("[a-f0-9]{64}", release["sha256"]):
            raise ValueError("Published release needs its archive SHA-256")
        if type(release.get("nexus_file_id")) is not int or release["nexus_file_id"] < 1:
            raise ValueError("Published release needs a Nexus file ID")
        filename = release.get("filename")
        if not isinstance(filename, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*\.msmod", filename):
            raise ValueError("Published release needs a portable .msmod filename")
    visiting, done = set(), set()

    def visit(name):
        if name in visiting:
            raise ValueError("Circular dependency: " + name)
        if name in done:
            return
        visiting.add(name)
        for dependency in by_id[name]["requires"]:
            if dependency not in by_id:
                raise ValueError("Missing dependency: " + dependency)
            if by_id[name]["status"] == "published" and by_id[dependency]["status"] != "published":
                raise ValueError("Published mod requires an unpublished dependency")
            visit(dependency)
        for conflict in by_id[name]["conflicts"]:
            if conflict not in by_id:
                raise ValueError("Unknown conflicting mod: " + conflict)
        visiting.remove(name)
        done.add(name)

    for name in sorted(by_id):
        visit(name)
    return by_id


def read(root=ROOT):
    entries = []
    for path in sorted((root / "catalog").glob("*.json")):
        entry = json.loads(path.read_text("utf-8"))
        if not isinstance(entry, dict) or path.stem != entry.get("id"):
            raise ValueError("Catalog filename must match its ID")
        entries.append(entry)
    return validate(entries)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    entries = read()
    published = [entries[name] for name in sorted(entries) if entries[name]["status"] == "published"]
    if args.build:
        out = ROOT / "artifacts"
        out.mkdir(exist_ok=True)
        path = out / "index.json"
        path.write_text(json.dumps({"schema": "moon-mod-index/v1", "mods": published}, indent=2, ensure_ascii=False) + "\n")
        (out / "SHA256SUMS").write_text(hashlib.sha256(path.read_bytes()).hexdigest() + "  index.json\n")
    print(json.dumps({"entries": len(entries), "published": len(published), "development": len(entries) - len(published)}))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        raise SystemExit(str(error))
