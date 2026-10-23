#!/usr/bin/env python3
"""Refresh the offline Shaping Board's embedded compiler from its canonical source."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
source = (ROOT / "site/shaping-board/breadboard-core.cjs").read_text(encoding="utf-8").strip()
path = ROOT / "site/shaping-board/index.html"
html = path.read_text(encoding="utf-8")
start = "/* BEGIN INLINED BREADBOARD CORE — generated from breadboard-core.cjs */"
end = "/* END INLINED BREADBOARD CORE */"
if html.count(start) != 1 or html.count(end) != 1:
    raise SystemExit("Missing or duplicate inline compiler markers")
head, remainder = html.split(start, 1)
_, tail = remainder.split(end, 1)
updated = head + start + "\n" + source + "\n" + end + tail
if html != updated:
    path.write_text(updated, encoding="utf-8")
    print("Updated offline Shaping Board compiler")
else:
    print("Compiler already in sync")
