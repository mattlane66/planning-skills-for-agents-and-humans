#!/usr/bin/env python3
"""Shared YAML-frontmatter utilities for repository validation and packaging."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], list[str], int]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"missing opening frontmatter marker: {path}")
    try:
        end = lines[1:].index("---") + 1
    except ValueError as exc:
        raise ValueError(f"missing closing frontmatter marker: {path}") from exc
    raw = "\n".join(lines[1:end])
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        raise ValueError(f"frontmatter must be a mapping: {path}")
    return data, lines, end


def normalize_tools(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        import re

        return [item for item in re.split(r"[\s,]+", value.strip()) if item]
    raise ValueError("allowed-tools must be a string or YAML list")
