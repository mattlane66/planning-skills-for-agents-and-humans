#!/usr/bin/env python3
"""Render an offline, inspectable HTML scorecard from one outcome report."""
from __future__ import annotations

import argparse
from html import escape
import json
from pathlib import Path


def show(value, *, percent=False):
    if value is None:
        return "Not measured"
    if percent:
        return f"{value * 100:.1f}%"
    return escape(str(value))


def generate(report: dict) -> str:
    if report.get("protocol") != "paired-hidden-artifact-v1":
        raise ValueError("unsupported outcome benchmark protocol")
    summary = report["summary"]
    baseline = summary["baseline"]
    skills = summary["skills"]
    rows = []
    for item in report["results"]:
        failed = [f"{check['path']}: {check['reason']}" for check in item["grade"]["checks"]
                  if not check["passed"]]
        label = "PASS" if item["grade"]["passed"] and not item.get("error") else "FAIL"
        rows.append(
            "<tr><td>" + escape(item["case_id"]) + "</td>"
            "<td>" + escape(str(item["trial"])) + "</td>"
            "<td>" + escape(item["arm"]) + "</td>"
            f"<td class='{label.lower()}'>{label}</td>"
            "<td>" + escape(str(item["grade"]["passed_checks"])) + "/"
            + escape(str(item["grade"]["total_checks"])) + "</td>"
            "<td>" + escape(str(item["wall_seconds"])) + "</td>"
            "<td>" + escape("; ".join(failed or ([item["error"]] if item.get("error") else []))) + "</td></tr>"
        )
    cards = []
    for title, metric, percent in [
        ("Safe task success", "safe_task_success_rate", True),
        ("Invariant preservation", "invariant_preservation_rate", True),
        ("Critical violations", "critical_violations", False),
        ("Mean wall time (seconds)", "mean_wall_seconds", False),
        ("Human minutes per success", "human_review_minutes_per_success", False),
    ]:
        cards.append(
            "<article><h2>" + escape(title) + "</h2><div class='compare'>"
            "<div><small>Baseline</small><strong>" + show(baseline[metric], percent=percent) + "</strong></div>"
            "<div><small>Planning Skills</small><strong>" + show(skills[metric], percent=percent) + "</strong></div>"
            "</div></article>"
        )
    caveats = "".join("<li>" + escape(str(entry)) + "</li>" for entry in report.get("caveats", []))
    info = (f"{report.get('runtime', 'unknown')} / {report.get('model', 'unknown')} · "
            f"{report.get('repeats', 'unknown')} trial(s) per task · "
            f"{report.get('generated_at', 'unknown')}")
    return """<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Planning Skills: outcome benchmark</title>
<style>
:root { font-family: system-ui,-apple-system,sans-serif; color-scheme:light dark; }
body { max-width:1100px; margin:0 auto; padding:32px 20px; line-height:1.55; }
small,.muted { opacity:.7 } .cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:14px; }
article { padding:16px; border:1px solid currentColor; border-radius:12px; }
article h2 { font-size:1rem; margin:0 0 12px; }
.compare { display:flex; gap:18px; justify-content:space-between; }
.compare div { display:grid; } strong { font-size:1.5rem; }
table { border-collapse:collapse; width:100%; font-size:.9rem; }
td,th { text-align:left; border-bottom:1px solid #8885; padding:8px 10px; vertical-align:top; }
.table-wrap { overflow-x:auto; } .pass { font-weight:700; } .fail { font-weight:700; text-decoration:underline; }
ul { padding-left:24px; } h1 { line-height:1.2; }
</style>
<main><h1>Planning Skills / outcome benchmark</h1>
<p class="muted">""" + escape(info) + """</p>
<section class="cards">""" + "".join(cards) + """</section>
<h2>Paired comparison</h2>
<p>Safe success-rate difference (skills minus baseline):
<strong>""" + show(summary.get("absolute_success_rate_difference"), percent=True) + """</strong>.
Mean elapsed-time difference: <strong>""" + show(summary.get("mean_wall_time_difference_seconds")) + """ seconds</strong>.
These are observations from this run, not causal proof or a universal model ranking.</p>
<h2>Auditable cases</h2><div class="table-wrap"><table>
<thead><tr><th>Case</th><th>Trial</th><th>Arm</th><th>Result</th><th>Checks</th><th>Seconds</th><th>Failures</th></tr></thead>
<tbody>""" + "".join(rows) + """</tbody></table></div>
<h2>Limits of this evidence</h2><ul>""" + caveats + """</ul></main></html>
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    output = generate(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    print(str(args.output))


if __name__ == "__main__":
    main()
