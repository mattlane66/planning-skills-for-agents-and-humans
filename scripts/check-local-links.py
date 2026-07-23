from __future__ import annotations

import pathlib
import re
import sys
from urllib.parse import unquote


ROOT = pathlib.Path(__file__).resolve().parent.parent
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
INLINE_MARKDOWN = re.compile(r"`([^`\n]+\.md)`")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")
SKIP_PARTS = {"node_modules", "dist", ".git"}


def markdown_files() -> list[pathlib.Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts)
    )


failures: list[str] = []

for document in markdown_files():
    text = document.read_text(encoding="utf-8")
    for raw_target in LINK.findall(text):
        target = raw_target.strip().strip("<>")
        if not target or target.startswith(SKIP_PREFIXES):
            continue

        target = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not target:
            continue

        candidate = ROOT / target.lstrip("/") if target.startswith("/") else document.parent / target
        if not candidate.resolve().exists():
            relative_document = document.relative_to(ROOT)
            failures.append(f"{relative_document}: {raw_target}")

    if "examples" in document.relative_to(ROOT).parts:
        for match in INLINE_MARKDOWN.finditer(text):
            raw_target = match.group(1)
            if match.start() > 0 and text[match.start() - 1] == "[" and text[match.end() :].startswith("]("):
                continue
            if any(marker in raw_target for marker in ("*", "{", "}", "<", ">")):
                continue
            candidate = ROOT / raw_target if raw_target.startswith("examples/") else document.parent / raw_target
            if not candidate.resolve().exists():
                relative_document = document.relative_to(ROOT)
                failures.append(f"{relative_document}: `{raw_target}`")

if failures:
    print("Broken local Markdown links:", file=sys.stderr)
    for failure in failures:
        print(f"- {failure}", file=sys.stderr)
    raise SystemExit(1)

print(f"Local Markdown links passed across {len(markdown_files())} files.")
