#!/usr/bin/env python3
"""Select a bounded inspection batch from already ranked discovery results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def inspection_batch(results: list[dict], budget: int, low_rank_count: int) -> list[dict]:
    """Reserve a low-rank check and return original source refs in inspection order."""
    if budget < 1 or low_rank_count < 0 or low_rank_count >= budget:
        raise ValueError("Reserve fewer low-ranked inspections than the positive batch size")
    originals: dict[str, str] = {}
    for result in results:
        ref = result.get("source_ref")
        original = result.get("original_ref") or ref
        if not isinstance(ref, str) or not isinstance(original, str) or not ref or not original:
            raise ValueError("Every ranked result needs a source_ref and optional original_ref")
        originals.setdefault(original, ref)
    ranked = list(originals)
    lower_ranked = ranked[max(len(ranked) // 2, 1):]
    sampled = lower_ranked[-low_rank_count:] if low_rank_count else []
    highest = [ref for ref in ranked if ref not in sampled][:budget - len(sampled)]
    return [
        {"original_ref": ref, "ranked_result_ref": originals[ref], "low_rank_sample": ref in sampled}
        for ref in highest + sampled
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ranked_results", type=Path, help="JSON list in rank order")
    parser.add_argument("--budget", type=int, required=True)
    parser.add_argument("--low-rank", type=int, default=1)
    args = parser.parse_args()
    try:
        results = json.loads(args.ranked_results.read_text(encoding="utf-8"))
        if not isinstance(results, list) or not all(isinstance(row, dict) for row in results):
            raise ValueError("Ranked results must be a JSON list of objects")
        batch = inspection_batch(results, args.budget, args.low_rank)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(batch, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
