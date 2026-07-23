#!/usr/bin/env python3
"""Validate portable Agent Skills and Claude-specific command frontmatter."""

from __future__ import annotations

import argparse
from pathlib import Path

from frontmatter import normalize_tools, parse_frontmatter

SKILL_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
CLAUDE_KEYS = {
    "name",
    "description",
    "when_to_use",
    "argument-hint",
    "arguments",
    "disable-model-invocation",
    "user-invocable",
    "allowed-tools",
    "model",
    "effort",
    "context",
    "agent",
    "hooks",
    "paths",
    "shell",
}
KNOWN_TOOLS = {"Read", "Write", "Edit", "Glob", "Grep", "Bash", "Skill"}
MANUAL_COMMANDS = {
    "frame",
    "shape",
    "criteria",
    "appetite",
    "sketch-shapes",
    "fit-check",
    "select-shape",
    "reconcile-sketch",
    "breadboard",
    "statechart",
    "dumplink",
    "kickoff",
    "feed-context",
    "reflect-breadboard",
}


def validate_skill(path: Path) -> None:
    data, lines, _ = parse_frontmatter(path)
    unexpected = sorted(set(data) - SKILL_KEYS)
    if unexpected:
        raise ValueError(f"unexpected portable skill keys in {path}: {', '.join(unexpected)}")
    for required in ("name", "description"):
        if not isinstance(data.get(required), str) or not data[required].strip():
            raise ValueError(f"missing required skill field {required!r}: {path}")
    if path.parent.name != data["name"]:
        raise ValueError(f"skill name must match directory for {path}")
    if len(data["description"]) > 1024:
        raise ValueError(f"skill description exceeds 1024 characters: {path}")
    if data.get("license") != "MIT":
        raise ValueError(f"skill must declare license: MIT: {path}")
    if len(lines) > 500:
        raise ValueError(f"SKILL.md must stay at or below 500 lines; split references: {path} ({len(lines)} lines)")
    if "allowed-tools" in data:
        normalize_tools(data["allowed-tools"])


def validate_command(path: Path) -> None:
    data, _, _ = parse_frontmatter(path)
    unexpected = sorted(set(data) - CLAUDE_KEYS)
    if unexpected:
        raise ValueError(f"unexpected Claude command keys in {path}: {', '.join(unexpected)}")
    if not isinstance(data.get("description"), str) or not data["description"].strip():
        raise ValueError(f"missing command description: {path}")
    tools = normalize_tools(data.get("allowed-tools"))
    unknown = sorted(tool for tool in tools if tool.split("(", 1)[0] not in KNOWN_TOOLS)
    if unknown:
        raise ValueError(f"unknown Claude tools in {path}: {', '.join(unknown)}")
    if path.stem in MANUAL_COMMANDS and data.get("disable-model-invocation") is not True:
        raise ValueError(f"human gate command must be manual-only: {path}")
    if path.stem == "check-drift" and data.get("disable-model-invocation") is True:
        raise ValueError(f"check-drift should remain model-invocable: {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=("skill", "command"), required=True)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    if args.kind == "skill":
        validate_skill(args.path)
    else:
        validate_command(args.path)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
