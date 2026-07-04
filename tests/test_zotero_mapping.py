import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "paper-forge" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from lib.config import DEFAULT_CONFIG  # noqa: E402
from lib.obsidian import note_filename, source_note_content  # noqa: E402
from lib.text import safe_unicode_text  # noqa: E402
from lib.zotero import _resolve_attachment_path, metadata_from_item, pending_items  # noqa: E402
from lib.workspace import source_manifest_content  # noqa: E402


class ZoteroMappingTests(unittest.TestCase):
    def test_zotero_item_maps_to_paperforge_metadata(self):
        item = {
            "key": "ABCD1234",
            "data": {
                "key": "ABCD1234",
                "title": "Industrial Grasping Robustness",
                "creators": [{"firstName": "Ada", "lastName": "Lovelace"}],
                "date": "2026-07-04",
                "publicationTitle": "Robotics Letters",
                "DOI": "10.1000/robotics",
                "url": "https://example.test/paper",
                "dateAdded": "2026-07-04T00:00:00Z",
            },
        }

        metadata = metadata_from_item(item, DEFAULT_CONFIG)

        self.assertEqual(metadata["zotero_item_key"], "ABCD1234")
        self.assertEqual(metadata["authors"], ["Ada Lovelace"])
        self.assertEqual(metadata["year"], 2026)
        self.assertEqual(metadata["venue"], "Robotics Letters")
        self.assertEqual(metadata["doi"], "10.1000/robotics")

    def test_attachment_enclosure_file_url_resolves_to_pdf_path(self):
        attachment = {
            "links": {
                "enclosure": {
                    "href": "file:///D:/Research/ZoteroData/storage/PKG5Q2FS/RT-2%20Paper.pdf",
                    "type": "application/pdf",
                }
            },
            "data": {"key": "PKG5Q2FS", "contentType": "application/pdf"},
        }

        path = _resolve_attachment_path(attachment, DEFAULT_CONFIG)

        self.assertEqual(path.as_posix(), "D:/Research/ZoteroData/storage/PKG5Q2FS/RT-2 Paper.pdf")

    def test_pending_items_falls_back_to_collection_when_pending_tag_is_missing(self):
        config = dict(DEFAULT_CONFIG)
        calls = []

        def fake_get_json(_config, endpoint, params=None):
            calls.append((endpoint, params))
            if endpoint == "items":
                return []
            if endpoint == "collections":
                return [{"data": {"key": "COLL1234", "name": "PaperForge Inbox"}}]
            if endpoint == "collections/COLL1234/items":
                return [
                    {"data": {"key": "KEEP1234", "title": "New Paper", "tags": []}},
                    {"data": {"key": "SKIP1234", "title": "Old Paper", "tags": [{"tag": "paperforge:processed"}]}},
                ]
            raise AssertionError(endpoint)

        with patch("lib.zotero.zotero_get_json", side_effect=fake_get_json):
            items = pending_items(config)

        self.assertEqual([item["data"]["key"] for item in items], ["KEEP1234"])
        self.assertEqual(calls[0][0], "items")
        self.assertEqual(calls[1][0], "collections")

    def test_multilingual_author_names_survive_zotero_mapping_and_markdown_export(self):
        item = {
            "key": "UNICODE01",
            "data": {
                "key": "UNICODE01",
                "title": "Unicode Author Test",
                "creators": [
                    {"name": "王小明"},
                    {"firstName": "Jürgen", "lastName": "Müller"},
                    {"name": "山田太郎"},
                    {"name": "김민수"},
                    {"firstName": "Алексей", "lastName": "Иванов"},
                    {"name": "MIT Computer Science and Artificial Intelligence Laboratory"},
                ],
                "date": "2026-07-04",
            },
        }

        metadata = metadata_from_item(item, DEFAULT_CONFIG)
        manifest = source_manifest_content(metadata, None, None)
        source_note = source_note_content(metadata, "2026-07-04__Unicode_Author_Test__UNICODE01", None, DEFAULT_CONFIG, None)

        self.assertEqual(
            metadata["authors"],
            [
                "王小明",
                "Jürgen Müller",
                "山田太郎",
                "김민수",
                "Алексей Иванов",
                "MIT Computer Science and Artificial Intelligence Laboratory",
            ],
        )
        for author in metadata["authors"]:
            self.assertIn(author, manifest)
            self.assertIn(author, source_note)
        self.assertIn(note_filename("00").removesuffix(".md"), source_note)

    def test_safe_unicode_text_repairs_typical_mojibake_but_preserves_valid_unicode(self):
        self.assertEqual(safe_unicode_text("FranÃ§ois Dupont"), "François Dupont")
        self.assertEqual(safe_unicode_text("Ð\x90Ð»ÐµÐºÑ\x81ÐµÐ¹ Ð\x98Ð²Ð°Ð½Ð¾Ð²"), "Алексей Иванов")
        self.assertEqual(safe_unicode_text("ç\x8e\x8bå°\x8fæ\x98\x8e"), "王小明")
        self.assertEqual(safe_unicode_text("王小明"), "王小明")
        self.assertEqual(safe_unicode_text("Jürgen Müller"), "Jürgen Müller")
        self.assertEqual(safe_unicode_text("山田太郎"), "山田太郎")

    def test_unrecoverable_suspicious_author_name_is_preserved_with_warning(self):
        item = {
            "key": "WARN0001",
            "data": {
                "key": "WARN0001",
                "title": "Warning Test",
                "creators": [{"name": "Ã"}],
                "date": "2026-07-04",
            },
        }

        metadata = metadata_from_item(item, DEFAULT_CONFIG)

        self.assertEqual(metadata["authors"], ["Ã"])
        self.assertIn("paperforge_warnings", metadata)
        self.assertIn("Could not safely repair suspected mojibake", metadata["paperforge_warnings"][0])


if __name__ == "__main__":
    unittest.main()
