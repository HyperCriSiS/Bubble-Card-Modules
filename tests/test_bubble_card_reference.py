"""Offline tests for the Bubble Card reference synchronizer."""
import json
import tempfile
import unittest
from pathlib import Path
from scripts import sync_bubble_card_reference as sync


class SelectionTests(unittest.TestCase):
    def test_tracks_contracts(self):
        for path in (
            "src/modules/module-documentation.md",
            "src/components/sub-button/styles.css",
            "src/cards/sub-buttons/create.js",
            "src/tools/ha-conditions.js",
        ):
            self.assertTrue(sync.wanted(path), path)

    def test_excludes_bundles_and_tests(self):
        for path in (
            "dist/bubble-card.js",
            "src/modules/parser.test.js",
            "src/components/sub-button/changes.test.js",
            ".github/workflows/untrusted.yml",
            "src/tools/other.js",
        ):
            self.assertFalse(sync.wanted(path), path)

    def test_git_blob_sha(self):
        self.assertEqual(
            sync.blob_sha(b"hello\n"),
            "ce013625030ba8dba906f756967f9e9ca394464a",
        )


class SnapshotTests(unittest.TestCase):
    def test_delta_deterministic(self):
        old = {"tracked_files": [
            {"path": "a.js", "sha": "one"},
            {"path": "b.js", "sha": "two"},
        ]}
        new = {"tracked_files": [
            {"path": "a.js", "sha": "changed"},
            {"path": "c.js", "sha": "new"},
        ]}
        self.assertEqual(sync.change_list(old, new), [
            "modified a.js", "removed b.js", "added c.js",
        ])

    def test_verify_detects_tamper_and_unexpected_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "main/src/modules/parser.js"
            source.parent.mkdir(parents=True)
            contents = b"/* verified source */\n"
            source.write_bytes(contents)
            manifest = {
                "channel": "main",
                "tracked_files": [{
                    "path": "src/modules/parser.js",
                    "sha": sync.blob_sha(contents),
                    "bytes": len(contents),
                }],
            }
            (root / "main/manifest.json").write_text(json.dumps(manifest))
            sync.check_channel("main", root)
            source.write_bytes(b"tampered")
            with self.assertRaisesRegex(RuntimeError, "Hash mismatch"):
                sync.check_channel("main", root)
            source.write_bytes(contents)
            (root / "main/extra.txt").write_text("unexpected")
            with self.assertRaisesRegex(RuntimeError, "Unexpected snapshot"):
                sync.check_channel("main", root)

    def test_comparison_independent_of_order(self):
        files = [
            {"path": "src/modules/parser.js", "sha": "p"},
            {"path": "src/modules/editor.js", "sha": "e"},
        ]
        old = {"tracked_files": files}
        new = {"tracked_files": files[::-1]}
        self.assertEqual(sync.change_list(old, new), [])


if __name__ == "__main__":
    unittest.main()
