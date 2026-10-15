#!/usr/bin/env python3
"""Read-only, human-scannable proposed Markdown revision; never writes planning truth."""

from __future__ import annotations

import difflib
import hashlib
import html
import json
from pathlib import Path

KINDS = {"editorial", "substantive", "uncertain"}
DECISIONS = {"pending", "accepted", "rejected", "deferred"}


class ReviewError(ValueError):
    """Unsafe or invalid review input."""


def read_source(path: Path) -> tuple[str, str]:
    if not path.is_file():
        raise ReviewError(f"Review input not found: {path}")
    if path.stat().st_size > 2_000_000:
        raise ReviewError(f"Review input exceeds 2 MB: {path}")
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8"), hashlib.sha256(raw).hexdigest()
    except UnicodeDecodeError as exc:
        raise ReviewError(f"Review input is not UTF-8: {path}") from exc


def load_record(path: Path | None, base_hash: str, proposal_hash: str) -> list[dict]:
    if path is None:
        return []
    text, _ = read_source(path)
    try:
        record = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ReviewError(f"Invalid review record JSON: {exc.msg}") from exc
    if not isinstance(record, dict) or not isinstance(record.get("deltas"), list):
        raise ReviewError("Review record must contain a deltas array")
    for key, actual in (("base_sha256", base_hash), ("proposal_sha256", proposal_hash)):
        if key in record and record[key] != actual:
            raise ReviewError(f"Stale review: {key} does not match the supplied file")
    if len(record["deltas"]) > 500:
        raise ReviewError("Review record exceeds 500 deltas")
    seen: set[str] = set()
    for entry in record["deltas"]:
        if not isinstance(entry, dict):
            raise ReviewError("Each delta must be an object")
        for field in ("id", "summary"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                raise ReviewError(f"Each delta requires nonempty {field}")
        if entry["id"] in seen:
            raise ReviewError(f"Duplicate delta ID: {entry['id']}")
        seen.add(entry["id"])
        if entry.get("kind") not in KINDS or entry.get("decision") not in DECISIONS:
            raise ReviewError("Delta kind or decision is invalid")
        for field in ("source_refs", "targets"):
            if not isinstance(entry.get(field), list) or not all(
                isinstance(value, str) and value.strip() for value in entry[field]
            ):
                raise ReviewError(f"Each delta needs a {field} string array")
        if entry["kind"] == "substantive" and not entry["targets"]:
            raise ReviewError("Substantive deltas require affected stable IDs")
        if entry["kind"] == "substantive" and not entry["source_refs"]:
            raise ReviewError("Substantive deltas require evidence source references")
    return record["deltas"]


def escape_line(line: str) -> str:
    return html.escape(line, quote=True) or " "


def inline_change(before: str, after: str) -> tuple[str, str]:
    before_markup: list[str] = []
    after_markup: list[str] = []
    for kind, a, b, c, d in difflib.SequenceMatcher(
        None, before, after, autojunk=False
    ).get_opcodes():
        old, new = escape_line(before[a:b]), escape_line(after[c:d])
        if kind == "equal":
            before_markup.append(old)
            after_markup.append(new)
        else:
            if old.strip():
                before_markup.append("<del>" + old + "</del>")
            if new.strip():
                after_markup.append("<ins>" + new + "</ins>")
    return "".join(before_markup), "".join(after_markup)


def render_review(base: str, proposal: str, deltas: list[dict], base_label: str,
                  proposal_label: str) -> str:
    base_lines, proposal_lines = base.splitlines(), proposal.splitlines()
    lines: list[str] = []
    def add(kind: str, old_no: str, new_no: str, old: str, new: str) -> None:
        lines.append(
            '<tr class="' + kind + '"><td class="num">' + old_no
            + '</td><td class="code">' + old + '</td><td class="num">' + new_no
            + '</td><td class="code">' + new + '</td></tr>'
        )

    for op, a, b, c, d in difflib.SequenceMatcher(
        None, base_lines, proposal_lines, autojunk=False
    ).get_opcodes():
        if op == "equal":
            for offset in range(b - a):
                add("unchanged", str(a + offset + 1), str(c + offset + 1),
                    escape_line(base_lines[a + offset]),
                    escape_line(proposal_lines[c + offset]))
        elif op == "replace":
            for offset in range(max(b - a, d - c)):
                has_old, has_new = a + offset < b, c + offset < d
                old, new = (base_lines[a + offset] if has_old else "",
                            proposal_lines[c + offset] if has_new else "")
                marked_old, marked_new = inline_change(old, new)
                add("modified", str(a + offset + 1) if has_old else "",
                    str(c + offset + 1) if has_new else "", marked_old, marked_new)
        elif op == "delete":
            for i in range(a, b):
                add("removed", str(i + 1), "", "<del>" + escape_line(base_lines[i]) + "</del>", "")
        elif op == "insert":
            for j in range(c, d):
                add("added", "", str(j + 1), "", "<ins>" + escape_line(proposal_lines[j]) + "</ins>")

    def esc(value: str) -> str:
        return html.escape(value, quote=True)

    def join_refs(values: list[str]) -> str:
        return ", ".join(esc(value) for value in values) or "—"

    delta_rows = [
        "<tr><td>" + esc(item["id"]) + "</td><td>" + esc(item["kind"])
        + "</td><td>" + esc(item["decision"]) + "</td><td>" + esc(item["summary"])
        + "</td><td>" + join_refs(item["source_refs"]) + "</td><td>"
        + join_refs(item["targets"]) + "</td></tr>"
        for item in deltas
    ]
    if not delta_rows:
        delta_rows = ['<tr><td colspan="6">No classified deltas supplied. The text diff does not establish decisions or authority.</td></tr>']

    # All user-provided content passes through HTML escaping. No external assets or JS.
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Proposed planning changes — review only</title>
<style>
:root{color-scheme:light dark;font:15px/1.5 system-ui,sans-serif}
body{margin:0 auto;max-width:1500px;padding:24px;color:CanvasText;background:Canvas}
h1{margin-bottom:4px}h2{margin-top:32px}
.notice{border-left:4px solid #b0771e;padding:10px 14px;background:color-mix(in srgb,CanvasText 6%,Canvas)}
.table-wrap{overflow:auto;border:1px solid #8885;border-radius:8px}
table{border-collapse:collapse;width:100%}th,td{border-bottom:1px solid #8884;padding:5px 8px;text-align:left;vertical-align:top}
th{background:color-mix(in srgb,CanvasText 7%,Canvas);position:sticky;top:0}
.diff{table-layout:fixed}.diff th.code{width:calc(50% - 40px)}.diff .num{width:40px;text-align:right;user-select:none;color:GrayText}
.diff .code{font:12px/1.6 ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere}
.diff tr.modified{background:rgba(230,160,50,.08)}.diff tr.added{background:rgba(24,160,100,.08)}
.diff tr.removed{background:rgba(220,70,70,.08)}
ins{background:#b6f3cc;color:#123722;text-decoration:none}del{background:#ffd0c8;color:#61221c;text-decoration:line-through}
.meta td{overflow-wrap:anywhere}
small{color:GrayText}
</style></head><body>
<h1>Proposed planning changes</h1>
<p class="notice"><strong>Review only.</strong> This is a derived comparison, not an accepted plan or a merge.
Recorded decisions are supplied by the author and are not independently verified.
Do not publish a proposal as accepted truth without the applicable human gate and downstream reconciliation.</p>
<p><strong>Current:</strong> """ + esc(base_label) + """ &nbsp; <strong>Proposal:</strong> """ + esc(proposal_label) + """</p>
<h2>Decision and provenance inventory</h2>
<div class="table-wrap"><table class="meta"><thead><tr><th>Delta</th><th>Type</th><th>Recorded decision</th><th>Summary</th><th>Evidence</th><th>Affected IDs</th></tr></thead><tbody>""" + "\n".join(delta_rows) + """</tbody></table></div>
<h2>Text differences</h2>
<p><small>Green: added. Red: removed. Amber: revised. Formatting changes are shown as text; semantic classification comes only from the supplied review record.</small></p>
<div class="table-wrap"><table class="diff"><thead><tr><th>#</th><th class="code">Current</th><th>#</th><th class="code">Proposal</th></tr></thead><tbody>""" + "\n".join(lines) + """</tbody></table></div>
</body></html>
"""


def write_review(base_path: Path, proposal_path: Path, output_path: Path,
                 record_path: Path | None = None, check: bool = False) -> None:
    sources = [base_path.resolve(), proposal_path.resolve()]
    if record_path:
        sources.append(record_path.resolve())
    if output_path.resolve() in sources:
        raise ReviewError("Review output cannot overwrite an input or the review record")
    if sources[0] == sources[1]:
        raise ReviewError("Current and proposed files must be distinct")
    base, base_hash = read_source(base_path)
    proposal, proposal_hash = read_source(proposal_path)
    deltas = load_record(record_path, base_hash, proposal_hash)
    if check:
        return
    result = render_review(base, proposal, deltas, base_path.name, proposal_path.name)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result, encoding="utf-8")
