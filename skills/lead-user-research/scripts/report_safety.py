#!/usr/bin/env python3
"""Shared safety helpers for validating and rendering outward research reports."""

from __future__ import annotations

import re
from urllib.parse import urlsplit


_MARKDOWN_SPECIAL = re.compile(r"([\\`*_{}\[\]()<>#!|~])")


def markdown_escape(value: object) -> str:
    """Render an untrusted scalar as inert, single-line Markdown text."""
    text = " ".join(str(value).splitlines())
    return _MARKDOWN_SPECIAL.sub(r"\\\1", text)


def identity_pattern(identity: str) -> re.Pattern[str]:
    """Match an identity as a token or phrase, not inside an unrelated word."""
    normalized = identity.strip()
    left = r"(?<!\w)" if normalized and (normalized[0].isalnum() or normalized[0] == "_") else ""
    right = r"(?!\w)" if normalized and (normalized[-1].isalnum() or normalized[-1] == "_") else ""
    return re.compile(left + re.escape(normalized) + right, flags=re.IGNORECASE)


def contains_private_identity(text: str, identity: str) -> bool:
    if not identity.strip():
        return False
    return identity_pattern(identity).search(text) is not None


def safe_outward_url(value: object) -> str | None:
    """Return a Markdown-safe public HTTP(S) URL, or None when unsafe."""
    if not isinstance(value, str):
        return None
    url = value.strip()
    if not url or any(char.isspace() or ord(char) < 0x20 for char in url):
        return None
    if any(char in url for char in '<>"'):
        return None
    parsed = urlsplit(url)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        return None
    return (
        url.replace("\\", "%5C")
        .replace("(", "%28")
        .replace(")", "%29")
    )
