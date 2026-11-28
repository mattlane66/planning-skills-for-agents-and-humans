"""Compare archived survey predictions on a fixed public respondent frame.

Run with the archived human and prediction CSV paths from the survey-simulations
ATP1 checkout. Only aggregate results leave this program.
"""

import argparse
import csv
import json
import math
import random
import statistics as st
from pathlib import Path

ATP1_CODING = {"A": 4, "B": 3, "C": 2, "D": 1, "E": 0}
REPEATS = 500
LABELED_BUDGET = 200
PILOT_BUDGET = 100
SEED = 2192


def read_answers(path: Path, response: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    with path.open(newline="", encoding="utf-8-sig") as source:
        for row in csv.DictReader(source):
            unit = row["id"]
            if not unit or unit in rows:
                raise ValueError("Expected exactly one row per respondent ID")
            rows[unit] = row[response].strip()
    return rows


def rectified(
    labeled: list[tuple[int, int]], unlabeled: list[tuple[int, int]], weight: float,
) -> float:
    return st.mean(y - weight * f for y, f in labeled) + weight * st.mean(
        f for _, f in unlabeled
    )


def replay(human_path: Path, prediction_path: Path) -> dict:
    human = read_answers(human_path, "correct_answer")
    prediction = read_answers(prediction_path, "answer")
    matched = sorted(human.keys() & prediction.keys())
    frame = [
        (ATP1_CODING[human[unit]], ATP1_CODING[prediction[unit]])
        for unit in matched
        if human[unit] in ATP1_CODING and prediction[unit] in ATP1_CODING
    ]
    if len(frame) < LABELED_BUDGET + 2:
        raise ValueError("Insufficient eligible respondents for declared disjoint groups")
    target = st.mean(y for y, _ in frame)
    rng = random.Random(SEED)
    errors: dict[str, list[float]] = {
        "human_only_200": [], "model_only": [], "full_correction_200": [],
        "pilot_100_correction_100": [],
    }
    weights: list[float] = []
    for _ in range(REPEATS):
        rng.shuffle(frame)
        pilot = frame[:PILOT_BUDGET]
        correction = frame[PILOT_BUDGET:LABELED_BUDGET]
        labeled = frame[:LABELED_BUDGET]
        unlabeled = frame[LABELED_BUDGET:]
        pilot_y, pilot_f = zip(*pilot, strict=True)
        denominator = (1 + len(correction) / len(unlabeled)) * st.variance(pilot_f)
        weight = min(1.0, max(0.0, st.covariance(pilot_y, pilot_f) / denominator)) if denominator else 0.0
        weights.append(weight)
        estimates = {
            "human_only_200": st.mean(y for y, _ in labeled),
            "model_only": st.mean(f for _, f in unlabeled),
            "full_correction_200": rectified(labeled, unlabeled, 1.0),
            "pilot_100_correction_100": rectified(correction, unlabeled, weight),
        }
        for method, estimate in estimates.items():
            errors[method].append(estimate - target)
    return {
        "frame": {
            "human_rows": len(human), "prediction_rows": len(prediction),
            "matched_ids": len(matched), "eligible_common_frame": len(frame),
            "human_mean": target,
        },
        "study_design": "ARCHIVED_FINITE_FRAME_DESCRIPTIVE",
        "repeats": REPEATS,
        "seed": SEED,
        "human_label_budget": LABELED_BUDGET,
        "pilot_budget": PILOT_BUDGET,
        "mean_pilot_weight": st.mean(weights),
        "methods": {
            name: {
                "signed_error": st.mean(values),
                "mean_absolute_error": st.mean(map(abs, values)),
                "rmse": math.sqrt(st.mean(value * value for value in values)),
            } for name, values in errors.items()
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("human", type=Path)
    parser.add_argument("predictions", type=Path)
    args = parser.parse_args()
    print(json.dumps(replay(args.human, args.predictions), indent=2))
