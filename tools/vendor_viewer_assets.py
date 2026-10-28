"""Fetch the viewer's pinned browser assets from npm, checking SHA-512 first.

Run with Python 3 from any directory. No package manager or global installation
is used. Only explicitly selected regular files are copied from each archive.
"""

import base64
import hashlib
import io
from pathlib import Path
import tarfile
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "viewer" / "vendor"
PACKAGES = {
    "marked": {
        "version": "18.1.2",
        "integrity": "sha512-DfOnvLAQ6WYeWxWO1u4RyFOeqyHup6dks5PPqnoFiooU7ipRvidO/2j8plhAHIiZg574E9ZlzSjUiPMLAzFkgg==",
        "files": {"package/lib/marked.umd.js": "marked.umd.js", "package/LICENSE": "LICENSE"},
    },
    "dompurify": {
        "version": "3.4.17",
        "integrity": "sha512-B/pSlYVHQ58kqISD/yDjuJ1yfzI34m1gF4lAod2bwSRhiN4K5Cl3H8Af7hqB2PmTL911tdEudnnXn5FnhRoz0w==",
        "files": {
            "package/dist/purify.min.js": "purify.min.js",
            "package/LICENSE": "LICENSE",
            "package/LICENSE-MPL": "LICENSE-MPL",
        },
    },
    "katex": {
        "version": "0.19.1",
        "integrity": "sha512-jG8uKntjSEcm2EpQOh0XturpPuuC9r3Sq5HLHdsFdWZT27E672SF19QEi+of0/YeOy15lDgRhKvr5614uRrEfA==",
        "files": {
            "package/dist/katex.min.js": "katex.min.js",
            "package/dist/katex.min.css": "katex.min.css",
            "package/dist/contrib/auto-render.min.js": "auto-render.min.js",
            "package/LICENSE": "LICENSE",
        },
    },
}


def download(name, package):
    version = package["version"]
    url = f"https://registry.npmjs.org/{name}/-/{name}-{version}.tgz"
    request = Request(url, headers={"User-Agent": "math-playground-local-wiki-vendor/1"})
    with urlopen(request, timeout=30) as response:
        data = response.read()
    actual = "sha512-" + base64.b64encode(hashlib.sha512(data).digest()).decode("ascii")
    if actual != package["integrity"]:
        raise ValueError(f"Integrity mismatch for {name} {version}; no files copied.")
    return data


def selected_files(name, package, data):
    selected = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        names = archive.getnames()
        for source, output in package["files"].items():
            if source not in names:
                raise ValueError(f"Missing expected file {source}; archive members: {names}")
            member = archive.getmember(source)
            if not member.isfile():
                raise ValueError(f"Expected a regular file: {source}")
            with archive.extractfile(member) as stream:
                selected[output] = stream.read()
        if name == "katex":
            for member in archive.getmembers():
                if member.name.startswith("package/dist/fonts/") and member.isfile():
                    filename = member.name.removeprefix("package/dist/")
                    if ".." in Path(filename).parts:
                        raise ValueError(f"Unexpected font path: {filename}")
                    with archive.extractfile(member) as stream:
                        selected[filename] = stream.read()
    return selected


def main():
    # Validate all downloaded archives and file selections before writing assets.
    outputs = {name: selected_files(name, package, download(name, package)) for name, package in PACKAGES.items()}
    count = total = 0
    for name, files in outputs.items():
        for output, data in files.items():
            path = DESTINATION / name / output
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            count += 1
            total += len(data)
        print(f"VERIFIED: {name} {PACKAGES[name]['version']} (SHA-512), {len(files)} files.")
    print(f"WROTE: {count} offline assets, {total:,} bytes, under viewer/vendor/.")


if __name__ == "__main__":
    main()
