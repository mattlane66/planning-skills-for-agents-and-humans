#!/usr/bin/env python3
"""Shared safety helpers for validating and rendering outward research reports."""

from __future__ import annotations

import re
from urllib.parse import unquote, urlsplit


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


def sensitive_text_variants(value: str) -> set[str]:
    """Return renderer-produced variants of sensitive source text."""
    raw = value.strip()
    if not raw:
        return set()
    variants = {raw, markdown_escape(raw)}
    safe_url = safe_outward_url(raw)
    if safe_url:
        variants.add(safe_url)
        variants.add(markdown_escape(safe_url))
    return {variant for variant in variants if variant}


def contains_sensitive_text(text: str, value: str) -> bool:
    """Detect raw, Markdown-escaped, or percent-encoded sensitive text."""
    if not value.strip():
        return False
    normalized_texts = {
        text,
        re.sub(r"\\([\\`*_{}\[\]()<>#!|~])", r"\1", text),
        unquote(text),
        unquote(re.sub(r"\\([\\`*_{}\[\]()<>#!|~])", r"\1", text)),
    }
    targets = sensitive_text_variants(value) | {value.strip(), unquote(value.strip())}
    return any(
        target.casefold() in candidate.casefold()
        for candidate in normalized_texts
        for target in targets
        if target
    )


def redact_sensitive_text(text: str, value: str, replacement: str) -> str:
    """Redact known renderer variants without exposing the original spelling."""
    for variant in sorted(sensitive_text_variants(value), key=len, reverse=True):
        text = re.sub(re.escape(variant), lambda _match: replacement, text, flags=re.IGNORECASE)
    return text


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
