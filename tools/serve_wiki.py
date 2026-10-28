"""Read-only local Markdown wiki. Python 3.10+, no installed dependencies."""

import argparse
from functools import partial
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
import re
import sys
from urllib.error import URLError
from urllib.parse import parse_qs, unquote, urlsplit
from urllib.request import ProxyHandler, build_opener
import webbrowser


ROOT = Path(__file__).resolve().parents[1]
APP_ID = "math-playground-wiki-v1"
RAW_EXTENSIONS = {".md", ".py", ".json", ".txt", ".csv", ".png", ".jpg", ".jpeg", ".gif", ".webp"}
EXTRA_CONTENT = {"README.md", "AGENTS.md", "open_wiki.cmd", "viewer/THIRD_PARTY.md", "viewer/vendor/marked/LICENSE", "viewer/vendor/dompurify/LICENSE", "viewer/vendor/dompurify/LICENSE-MPL", "viewer/vendor/katex/LICENSE"}


def allowed_content(relative):
    return relative.as_posix() in EXTRA_CONTENT or (relative.parts[0] in {"wiki", "research", "templates"} and relative.suffix.lower() in RAW_EXTENSIONS)


def workspace_id(root):
    return hashlib.sha256(str(root.resolve()).casefold().encode()).hexdigest()[:20]


def resolve_content(root, value):
    """Allow only visible wiki/research/template content; never arbitrary root files."""
    relative = Path(value)
    if relative.is_absolute() or any(part in {"..", "."} or part.startswith(".") or ":" in part for part in relative.parts):
        raise ValueError("허용되지 않는 문서 경로입니다.")
    if not relative.parts:
        raise ValueError("문서 경로가 필요합니다.")
    if not allowed_content(relative):
        raise ValueError("위키 문서 폴더만 열 수 있습니다.")
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError("허용되지 않는 파일입니다.")
    resolved_parts = target.relative_to(root.resolve()).parts
    if any(part.startswith(".") for part in resolved_parts) or not allowed_content(target.relative_to(root.resolve())):
        raise ValueError("허용되지 않는 문서 대상입니다.")
    if not target.is_file():
        raise FileNotFoundError(value)
    return target


def text_label(value):
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    return value.replace("`", "").replace("**", "").strip()


def read_header(text):
    values = {}
    for line in text.splitlines():
        match = re.match(r"^- ([^:]+):\s*(.*)$", line)
        if match:
            values.setdefault(match.group(1), match.group(2))
        if line.startswith("## "):
            break
    return values


def read_evaluation(path):
    if not path.exists():
        return {}, None
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(data, dict):
            raise ValueError("메타데이터는 JSON 객체여야 합니다.")
        score = data.get("score")
        if score is not None and (type(score) is not int or not 0 <= score <= 100):
            raise ValueError("score는 0~100 정수 또는 null이어야 합니다.")
        for key in ("summary", "novelty", "evaluation_status", "assessed_at", "assessor", "scoring_version", "reassessment"):
            if key in data and not isinstance(data[key], str):
                raise ValueError(f"{key}는 문자열이어야 합니다.")
        if "rationale" in data and (not isinstance(data["rationale"], list) or not all(isinstance(item, str) for item in data["rationale"])):
            raise ValueError("rationale은 문자열 목록이어야 합니다.")
        return data, None
    except (OSError, ValueError) as error:
        return {}, str(error)


def catalog(root):
    notes, pages, warnings = [], [], []
    fingerprint = hashlib.sha256()
    paths = [root / "README.md", root / "AGENTS.md", root / "viewer/THIRD_PARTY.md"]
    for folder in ("wiki", "research", "templates"):
        paths.extend(sorted((root / folder).rglob("*.md")))
    for path in paths:
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        try:
            resolve_content(root, relative)
            text = path.read_text(encoding="utf-8-sig")
            fingerprint.update(relative.encode())
            fingerprint.update(text.encode())
            title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
            title = text_label(title_match.group(1)) if title_match else path.stem
            page = {"path": relative, "title": title, "section": path.relative_to(root).parts[0] if "/" in relative else "안내"}
            pages.append(page)
            if path.name != "note.md" or not relative.startswith("research/"):
                continue
            header = read_header(text)
            meta_path = path.with_name("meta.json")
            if meta_path.exists():
                resolve_content(root, meta_path.relative_to(root).as_posix())
                fingerprint.update(meta_path.read_bytes())
            meta, error = read_evaluation(meta_path)
            if error:
                warnings.append(f"{meta_path.relative_to(root).as_posix()}: {error}")
            review = text_label(header.get("독립 검토", "대기"))
            review_status = "미실시" if review.startswith("미실시") else "수정 필요" if "수정 필요" in review else "통과" if "통과" in review else "대기"
            notes.append({
                "id": path.parent.name, "path": relative, "title": title,
                "fields": [part.strip() for part in re.split(r"[,·]", text_label(header.get("분야", "미분류"))) if part.strip()],
                "created": header.get("작성일", ""), "updated": header.get("수정일", ""),
                "review_status": review_status, "review_label": review,
                "novelty": meta.get("novelty", text_label(header.get("문헌 관계", "미확인"))),
                "score": meta.get("score"), "summary": meta.get("summary", ""),
                "evaluation": meta, "metadata_error": error,
            })
        except (OSError, ValueError) as error:
            warnings.append(f"{relative}: {error}")
    # File order is immaterial. Sorting is a viewer responsibility.
    return {"notes": notes, "pages": pages, "warnings": warnings, "revision": fingerprint.hexdigest()}


class WikiServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = False


class Handler(BaseHTTPRequestHandler):
    server_version = "MathWiki/1"

    def __init__(self, *args, root=ROOT, **kwargs):
        self.root = Path(root).resolve()
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        if len(args) > 1 and str(args[1]).startswith(("4", "5")):
            super().log_message(format, *args)

    def send_data(self, data, content_type, status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)

    def send_json(self, data, status=200):
        self.send_data(json.dumps(data, ensure_ascii=False).encode(), "application/json; charset=utf-8", status)

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        port = self.server.server_port
        if self.headers.get("Host", "") not in {f"127.0.0.1:{port}", f"localhost:{port}"}:
            self.send_json({"error": "로컬 호스트 주소로 접속하세요."}, 403)
            return
        request = urlsplit(self.path)
        query = parse_qs(request.query)
        try:
            if request.path == "/api/health":
                self.send_json({"app": APP_ID, "workspace": workspace_id(self.root)})
            elif request.path == "/api/catalog":
                self.send_json(catalog(self.root))
            elif request.path in {"/api/document", "/api/file"}:
                path = resolve_content(self.root, query.get("path", [""])[0])
                if request.path == "/api/document":
                    if path.suffix.lower() != ".md":
                        raise ValueError("Markdown 문서만 열 수 있습니다.")
                    self.send_json({"path": path.relative_to(self.root).as_posix(), "content": path.read_text(encoding="utf-8-sig")})
                else:
                    suffix = path.suffix.lower()
                    kind = mimetypes.guess_type(str(path))[0] if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp"} else "text/plain; charset=utf-8"
                    self.send_data(path.read_bytes(), kind or "application/octet-stream")
            elif request.path == "/" or request.path == "/index.html":
                self.send_data((self.root / "viewer/index.html").read_bytes(), "text/html; charset=utf-8")
            elif request.path.startswith("/assets/"):
                value = unquote(request.path[len("/assets/"):])
                relative = Path(value)
                base = (self.root / "viewer").resolve()
                target = (base / relative).resolve()
                if relative.is_absolute() or any(p.startswith(".") or ":" in p for p in relative.parts) or not target.is_relative_to(base):
                    raise ValueError("허용되지 않는 에셋 경로입니다.")
                if not target.is_file() or target.suffix.lower() not in {".js", ".mjs", ".css", ".woff", ".woff2", ".ttf", ".svg", ".ico"}:
                    raise FileNotFoundError(value)
                kind = "text/javascript" if target.suffix in {".js", ".mjs"} else mimetypes.guess_type(str(target))[0] or "application/octet-stream"
                self.send_data(target.read_bytes(), kind)
            else:
                self.send_json({"error": "페이지를 찾을 수 없습니다."}, 404)
        except FileNotFoundError:
            self.send_json({"error": "파일을 찾을 수 없습니다."}, 404)
        except (ValueError, UnicodeError) as error:
            self.send_json({"error": str(error)}, 400)
        except OSError:
            self.send_json({"error": "파일을 읽지 못했습니다. 저장 상태를 확인하세요."}, 500)


def existing_server(root, port):
    opener = build_opener(ProxyHandler({}))
    try:
        with opener.open(f"http://127.0.0.1:{port}/api/health", timeout=0.4) as response:
            health = json.loads(response.read(4096))
        return isinstance(health, dict) and health.get("app") == APP_ID and health.get("workspace") == workspace_id(root)
    except (OSError, URLError, ValueError):
        return False


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--open", action="store_true", help="Open the default browser after binding.")
    args = parser.parse_args(argv)
    if not 0 <= args.port <= 65535:
        parser.error("port must be between 0 and 65535")
    candidates = [0] if args.port == 0 else range(args.port, min(args.port + 10, 65536))
    server = None
    # Reuse a server on any fallback port before considering a newly free port.
    for port in candidates:
        if port and existing_server(ROOT, port):
            url = f"http://127.0.0.1:{port}/"
            print(f"Already running: {url}", flush=True)
            if args.open:
                webbrowser.open(url)
            return 0
    for port in candidates:
        try:
            server = WikiServer(("127.0.0.1", port), partial(Handler, root=ROOT))
            break
        except OSError:
            continue
    if server is None:
        print("Could not bind a local port. Try --port 0.", file=sys.stderr)
        return 1
    missing = [name for name in ("marked/marked.umd.js", "dompurify/purify.min.js", "katex/katex.min.js", "katex/katex.min.css") if not (ROOT / "viewer/vendor" / name).is_file()]
    if missing:
        server.server_close()
        print("Missing viewer assets. Run: python tools/vendor_viewer_assets.py", file=sys.stderr)
        return 1
    url = f"http://127.0.0.1:{server.server_port}/"
    print(f"Math Playground Wiki: {url}", flush=True)
    print("Keep this window open. Press Ctrl+C to stop. Files refresh automatically.", flush=True)
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nWiki stopped.", flush=True)
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
