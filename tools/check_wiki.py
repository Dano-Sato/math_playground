"""Check local Markdown links outside templates, code spans and code fences."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+\"[^\"]*\")?\s*\)")


def prose_lines(text):
    fence_char = None
    fence_size = 0
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence_char is None:
                fence_char, fence_size = token[0], len(token)
            elif token[0] == fence_char and len(token) >= fence_size:
                fence_char = None
            continue
        if fence_char is None:
            yield number, line


def main():
    failures = []
    documents = 0
    links = 0
    for path in sorted(ROOT.rglob("*.md")):
        relative = path.relative_to(ROOT)
        if any(part.startswith(".") for part in relative.parts):
            continue
        # Templates intentionally contain placeholders, not working destinations.
        if relative.parts[0] == "templates":
            continue
        documents += 1
        for line_number, line in prose_lines(path.read_text(encoding="utf-8")):
            line = re.sub(r"(`+).*?\1", "", line)
            for match in LINK.finditer(line):
                raw = match.group(1) or match.group(2)
                parsed = urlsplit(raw)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                links += 1
                target = (path.parent / unquote(parsed.path)).resolve()
                if not target.exists():
                    failures.append(f"{relative}:{line_number}: missing {raw}")
    if failures:
        print("\n".join(failures))
        return 1
    print(f"PASS: {links} local links in {documents} Markdown files.")
    print("Templates and code skipped; headings and external URLs not checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
