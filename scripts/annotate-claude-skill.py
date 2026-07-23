#!/usr/bin/env python3
"""Add Claude Code-only operational metadata to a generated skill copy."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from frontmatter import parse_frontmatter

ALIASED = {
    "framing-doc",
    "shaping",
    "sketch-reconciliation",
    "breadboarding",
    "kickoff-doc",
    "feed-planning-context",
    "breadboard-reflection",
}
DIRECT = {
    "statechart": "[accepted breadboard, selected scope or slice, and optional target statechart file]",
    "interface-contracts": "[selected breadboard or slice, boundary, and optional target contract file]",
    "executable-breadboards": "[selected breadboard, slice, contracts, examples, and optional target file]",
    "dumplink": "[shaping doc, breadboard, selected slice, appetite, or notes]",
}
TOOLS = ["Read", "Write", "Edit", "Glob", "Grep"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("skill")
    args = parser.parse_args()
    data, lines, end = parse_frontmatter(args.path)
    if args.skill in ALIASED:
        data["user-invocable"] = False
    if args.skill in DIRECT:
        data["argument-hint"] = DIRECT[args.skill]
        data["allowed-tools"] = TOOLS
    body = "\n".join(lines[end + 1 :]).lstrip("\n")
    header = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000).rstrip()
    args.path.write_text(f"---\n{header}\n---\n\n{body.rstrip()}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
