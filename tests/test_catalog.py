import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from catalog import read, validate


def entry(name="example"):
    return {"schema": "moon-mod-index-entry/v1", "id": name, "name": "Example", "summary": "Synthetic example",
            "kind": "native", "version": "1.0.0", "requires": [], "conflicts": [], "supported_builds": ["synthetic-build"],
            "status": "development", "source": None, "nexus": None, "release": None}


def published(name="example"):
    result = entry(name)
    result.update(status="published", source="https://github.com/example/example",
                  nexus="https://www.nexusmods.com/example/mods/1",
                  release={"filename": "example-1.0.0.msmod", "sha256": "a" * 64, "nexus_file_id": 1})
    return result


class CatalogChecks(unittest.TestCase):
    def test_migrated_metadata_is_explicitly_unpublished(self):
        entries = read()
        self.assertGreater(len(entries), 0)
        self.assertTrue(all(e["status"] == "development" for e in entries.values()))

    def test_published_entry_requires_real_release_identity(self):
        value = published()
        validate([value])
        for patch in ({"nexus": None}, {"source": "https://github.com/example/example?token=secret"},
                      {"release": None}, {"version": None}, {"supported_builds": []}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                validate([{**value, **patch}])

    def test_duplicate_missing_and_cyclic_dependencies(self):
        first, second = entry("first"), entry("second")
        with self.assertRaises(ValueError):
            validate([first, first])
        first["requires"] = ["second"]
        with self.assertRaises(ValueError):
            validate([first])
        second["requires"] = ["first"]
        with self.assertRaisesRegex(ValueError, "Circular"):
            validate([first, second])

    def test_published_mod_cannot_depend_on_unpublished_mod(self):
        first, second = published("first"), entry("second")
        first["requires"] = ["second"]
        with self.assertRaisesRegex(ValueError, "unpublished dependency"):
            validate([first, second])

    def test_unknown_conflict_and_false_release_identity(self):
        value = entry()
        value["conflicts"] = ["missing"]
        with self.assertRaises(ValueError):
            validate([value])
        value = published()
        for update in ({"filename": "../escape.msmod"}, {"sha256": "incorrect"}, {"nexus_file_id": True}):
            with self.subTest(update=update), self.assertRaises(ValueError):
                validate([{**value, "release": {**value["release"], **update}}])


if __name__ == "__main__":
    unittest.main()
