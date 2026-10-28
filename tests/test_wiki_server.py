import http.client
from functools import partial
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from serve_wiki import Handler, WikiServer, catalog, existing_server, main, read_evaluation, resolve_content


class WikiServerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="math-wiki-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ("wiki", "research/sample", "viewer"):
            (self.root / folder).mkdir(parents=True)
        (self.root / "viewer/index.html").write_text("<!doctype html><title>Wiki</title>", encoding="utf-8")
        (self.root / "viewer/THIRD_PARTY.md").write_text("# 라이선스", encoding="utf-8")
        (self.root / "open_wiki.cmd").write_text("@echo off", encoding="utf-8")
        (self.root / "wiki/Home.md").write_text("# 홈\n\n수학 위키", encoding="utf-8")
        (self.root / "research/sample/note.md").write_text("# 테스트 연구\n\n- 분야: 조합론, 해석학\n- 독립 검토: [통과](review.md)\n\n## 질문\n내용", encoding="utf-8")
        (self.root / "research/sample/meta.json").write_text(json.dumps({"score": 5, "summary": "검증 사례"}), encoding="utf-8")

    def test_catalog_reads_note_and_per_note_score(self):
        result = catalog(self.root)
        note = result["notes"][0]
        self.assertEqual((note["score"], note["review_status"], note["fields"]), (5, "통과", ["조합론", "해석학"]))
        (self.root / "research/sample/meta.json").write_text('{"score": 17}', encoding="utf-8")
        updated = catalog(self.root)
        self.assertNotEqual(result["revision"], updated["revision"])
        self.assertEqual(updated["notes"][0]["score"], 17)
        (self.root / "research/new").mkdir()
        (self.root / "research/new/note.md").write_text("# 새 노트", encoding="utf-8")
        self.assertEqual(len(catalog(self.root)["notes"]), 2)

    def test_invalid_metadata_is_visible_as_warning_and_unscored(self):
        path = self.root / "research/sample/meta.json"
        for content in ('{"score": true}', '{"score": 101}', '{"score": "5"}', '{"rationale": "text"}', 'broken json'):
            with self.subTest(content=content):
                path.write_text(content, encoding="utf-8")
                result = catalog(self.root)
                self.assertIsNone(result["notes"][0]["score"])
                self.assertEqual(len(result["warnings"]), 1)

    def test_unreviewed_note_keeps_its_explicit_status(self):
        path = self.root / "research/sample/note.md"
        path.write_text("# 자체 점검 노트\n\n- 독립 검토: 미실시(작성 세션 자체 점검)\n\n## 결과\n자체 점검 통과", encoding="utf-8")
        note = catalog(self.root)["notes"][0]
        self.assertEqual(note["review_status"], "미실시")
        self.assertIn("자체 점검", note["review_label"])

    def test_absent_metadata_is_unscored_without_error(self):
        meta, error = read_evaluation(self.root / "research/missing/meta.json")
        self.assertEqual((meta, error), ({}, None))

    def test_other_json_service_is_not_mistaken_for_wiki(self):
        for payload in (b"[]", b"null", b"123", b'{"app":"another"}'):
            with self.subTest(payload=payload), patch("serve_wiki.build_opener") as opener:
                opener.return_value.open.return_value.__enter__.return_value.read.return_value = payload
                self.assertFalse(existing_server(self.root, 8765))

    def test_existing_fallback_is_reused_before_binding_default(self):
        with patch("serve_wiki.existing_server", side_effect=lambda root, port: port == 8766), patch("serve_wiki.WikiServer") as server:
            self.assertEqual(main(["--port", "8765"]), 0)
            server.assert_not_called()

    def test_path_boundaries(self):
        for value in ("../secret.md", "research/../wiki/Home.md", ".codex/private.json", "C:\\Windows\\private.md", "viewer/index.html", "research/sample/verify.exe"):
            with self.subTest(value=value), self.assertRaises((ValueError, FileNotFoundError)):
                resolve_content(self.root, value)
        self.assertEqual(resolve_content(self.root, "wiki/Home.md"), (self.root / "wiki/Home.md").resolve())
        self.assertTrue(resolve_content(self.root, "viewer/THIRD_PARTY.md").is_file())
        self.assertTrue(resolve_content(self.root, "open_wiki.cmd").is_file())

    def test_http_routes_and_host_boundary(self):
        server = WikiServer(("127.0.0.1", 0), partial(Handler, root=self.root))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=3)
        self.addCleanup(connection.close)
        for route, expected in (("/", 200), ("/api/catalog", 200), ("/api/document?path=wiki%2FHome.md", 200), ("/api/document?path=research%2Fsample%2Fmeta.json", 400), ("/api/file?path=research%2Fsample%2Fmeta.json", 200), ("/api/document?path=..%2Fsecret.md", 400), ("/assets/..%2Ftools%2Fserve_wiki.py", 400), ("/missing", 404)):
            with self.subTest(route=route):
                connection.request("GET", route)
                response = connection.getresponse()
                content = response.read()
                self.assertEqual(response.status, expected, content)
                self.assertIn("script-src 'self'", response.getheader("Content-Security-Policy"))
                self.assertEqual(response.getheader("X-Content-Type-Options"), "nosniff")
        connection.request("GET", "/api/catalog", headers={"Host": "other.example"})
        response = connection.getresponse()
        response.read()
        self.assertEqual(response.status, 403)


if __name__ == "__main__":
    unittest.main()
