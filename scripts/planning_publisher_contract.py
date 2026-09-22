"""Canonical artifact parsing and publication-readiness validation."""

import re
from pathlib import Path


class ContractError(ValueError):
    pass


PLACEHOLDER_VALUES = {"", "...", "—", "-", "TBD", "TODO", "[...]"}


def frontmatter(text):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    meta = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta, text[end + 5 :]


def section(text, heading_pattern, level=2):
    marks = "#" * level
    match = re.search(
        rf"^{marks}\s+{heading_pattern}\s*$\n(.*?)(?=^{marks}\s+|\Z)",
        text,
        re.M | re.S | re.I,
    )
    return match.group(1).strip() if match else ""


def bullets(block):
    return [m.group(1).strip() for m in re.finditer(r"^\s*-\s+(.+)$", block, re.M)]


def key_values(block):
    result = {}
    for item in bullets(block):
        if ":" in item:
            key, value = item.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def table(block):
    lines = [line.strip() for line in block.splitlines() if line.strip().startswith("|")]
    if len(lines) < 3:
        return []
    rows = [[cell.strip().strip(chr(96)) for cell in line.strip("|").split("|")] for line in lines]
    if not all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in rows[1]):
        return []
    header = rows[0]
    return [dict(zip(header, row + [""] * max(0, len(header) - len(row)))) for row in rows[2:]]


def first_table(block):
    lines = block.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip().startswith("|")), None)
    if start is None:
        return []
    picked = []
    for line in lines[start:]:
        if not line.strip().startswith("|"):
            break
        picked.append(line)
    return table("\n".join(picked))


def title(text, suffix):
    match = re.search(r"^#\s+(.+)$", text, re.M)
    return (match.group(1).strip() if match else "Shaped Work").replace(suffix, "")


def clean_value(value):
    return str(value or "").strip().strip(chr(96)).strip()


def _artifact_type(path):
    meta, text = frontmatter(path.read_text(encoding="utf-8"))
    return clean_value(meta.get("artifact_type")).lower(), meta, text


def _breadboard_mode(meta, text):
    value = clean_value(meta.get("mode"))
    if value:
        return value
    values = key_values(section(text, r"Mode and authority"))
    return clean_value(values.get("Mode"))


def discover(directory, role):
    """Prefer frontmatter artifact_type/authority, then fall back to filenames."""
    directory = Path(directory)
    files = sorted(directory.glob("*.md"))
    typed = []
    fallback = []
    for path in files:
        artifact_type, meta, text = _artifact_type(path)
        stem = path.stem.lower()
        if artifact_type == role:
            score = 10
            if role == "breadboard":
                mode = _breadboard_mode(meta, text)
                if mode == "selected-design":
                    score += 6
                if clean_value(meta.get("source_of_truth")).lower() == "true":
                    score += 3
                if clean_value(meta.get("status")).lower() in {"accepted", "selected"}:
                    score += 1
            typed.append((score, path))
        if role == "frame" and "frame" in stem:
            fallback.append(path)
        elif role == "shaping" and "shaping" in stem:
            fallback.append(path)
        elif role == "breadboard" and "breadboard" in stem and "reflection" not in stem:
            fallback.append(path)
    if typed:
        return sorted(typed, key=lambda item: (-item[0], str(item[1])))[0][1]
    if role == "breadboard" and fallback:
        selected = []
        for path in fallback:
            _, meta, text = _artifact_type(path)
            if _breadboard_mode(meta, text) == "selected-design":
                selected.append(path)
        fallback = selected or [path for path in fallback if "candidate" not in path.stem.lower()] or fallback
    if fallback:
        return sorted(fallback)[0]
    raise ContractError(f"Could not discover {role} artifact in {directory}")


def shapes(text):
    block = section(text, r"Shapes")
    matches = list(re.finditer(r"^###\s+([A-Z][A-Z0-9_-]*):\s+(.+)$", block, re.M))
    output = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(block)
        output.append({
            "id": match.group(1),
            "name": match.group(2).strip(),
            "parts": first_table(block[match.end():end]),
        })
    return output


def _shape_choice(text, shape_ids):
    if not text:
        return ""
    exact = clean_value(text)
    if exact in shape_ids:
        return exact
    match = re.match(r"\*{0,2}([A-Z][A-Z0-9_-]*)\b", exact)
    return match.group(1) if match and match.group(1) in shape_ids else ""


def parse_frame(path):
    meta, text = frontmatter(Path(path).read_text(encoding="utf-8"))
    boundaries = section(text, r"Boundaries")
    less = section(text, r"Less about") or section(boundaries, r"Less about", level=3)
    more = section(text, r"More about") or section(boundaries, r"More about", level=3)
    return {
        "source": str(path),
        "title": title(text, " — Frame"),
        "problem": bullets(section(text, r"Problem")),
        "outcome": bullets(section(text, r"Outcome")),
        "transformation": key_values(section(text, r"Transformation frame[^\n]*")),
        "operating_model": key_values(section(text, r"Operating model[^\n]*")),
        "less_about": bullets(less),
        "more_about": bullets(more),
        "meta": meta,
    }, text


def parse_shaping(path):
    meta, text = frontmatter(Path(path).read_text(encoding="utf-8"))
    requirement_block = section(text, r"Accepted Requirements") or section(text, r"Requirements")
    appetite_block = section(text, r"Accepted Appetite") or section(text, r"Appetite")
    decision_block = section(text, r"Human Decision") or section(text, r"Decision")
    decision_values = key_values(decision_block)
    shape_list = shapes(text)
    shape_ids = {item["id"] for item in shape_list}

    legacy_choice = re.search(r"Recorded human choice:\s*\*\*([^*]+)\*\*", decision_block, re.I)
    status = clean_value(decision_values.get("Status")).lower()
    if legacy_choice:
        picked = _shape_choice(legacy_choice.group(1), shape_ids)
        status = status or "selected"
    elif status == "selected":
        picked = _shape_choice(decision_values.get("Chosen direction"), shape_ids)
    else:
        picked = ""

    for shape in shape_list:
        shape["selected"] = shape["id"] == picked

    appetite = key_values(appetite_block)
    operating_model = key_values(section(text, r"Operating model[^\n]*"))
    requirements = first_table(requirement_block)
    req_auth = {clean_value(row.get("Authority")) for row in requirements if clean_value(row.get("Authority"))}
    appetite_authority = clean_value(appetite.get("Authority"))
    if not appetite_authority and section(text, r"Accepted Appetite"):
        appetite_authority = "Accepted"

    rationale = []
    reason = re.search(r"Reason:\s*(.*)", decision_block, re.S | re.I)
    if reason:
        rationale = bullets(reason.group(1))
    elif clean_value(decision_values.get("Why")):
        rationale = [clean_value(decision_values.get("Why"))]

    return {
        "source": str(path),
        "title": title(text, " — Shaping"),
        "appetite": appetite,
        "appetite_authority": appetite_authority or "Unknown",
        "operating_model": operating_model,
        "requirements": requirements,
        "requirements_authority": "Accepted" if req_auth == {"Accepted"} else ("Mixed" if req_auth else "Unknown"),
        "shapes": shape_list,
        "fit": first_table(section(text, r"Fit check")),
        "appetite_fit": first_table(section(text, r"Appetite fit")),
        "reverse_fit": first_table(section(text, r"Reverse fit check")),
        "selected_shape": picked,
        "decision_status": status or "unknown",
        "decision_rationale": rationale,
        "meta": meta,
    }, text


def _normalize_slice_row(row):
    raw = clean_value(row.get("Slice") or row.get("ID"))
    match = re.match(r"(V[\w.-]+)(?:\s*[—-]\s*(.+))?$", raw)
    if not match:
        return None
    slice_id = match.group(1)
    name = clean_value(row.get("Name")) or clean_value(match.group(2)) or clean_value(row.get("Demo")) or slice_id
    demo = clean_value(row.get("Demo"))
    refs = re.findall(r"\b(?:P|U|N|S)\d+(?:\.\d+)?\b", clean_value(
        row.get("Affordances / stores included") or row.get("Included affordances / stores")
    ))
    return {
        "id": slice_id,
        "name": name,
        "demo": [demo] if demo else [],
        "produces": clean_value(row.get("Produces")),
        "scope_refs": refs,
        "unknowns": clean_value(row.get("Unknowns")),
        "dependencies": clean_value(row.get("Dependencies")),
    }


def parse_slices_from_breadboard(text):
    current = first_table(section(text, r"Slice candidates.*"))
    if current:
        return [item for row in current if (item := _normalize_slice_row(row))]
    block = section(text, r"Candidate vertical slices")
    matches = list(re.finditer(r"^###\s+(V[\w.-]+)\s+[—-]\s+(.+)$", block, re.M))
    output = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(block)
        body = block[match.end():end]
        demo = re.search(r"Demo:\s*(.*?)(?=\nProduces:|\Z)", body, re.S | re.I)
        produced = re.search(r"Produces:\s*(.*?)(?=\n[A-Z][A-Za-z ]+:|\Z)", body, re.S | re.I)
        output.append({
            "id": match.group(1),
            "name": match.group(2).strip(),
            "demo": bullets(demo.group(1) if demo else ""),
            "produces": " ".join(
                line.strip("- ").strip()
                for line in (produced.group(1) if produced else "").splitlines()
                if line.strip()
            ),
            "scope_refs": [],
            "unknowns": "",
            "dependencies": "",
        })
    return output


def parse_breadboard(path):
    meta, text = frontmatter(Path(path).read_text(encoding="utf-8"))
    authority_values = key_values(section(text, r"Mode and authority"))
    mode = _breadboard_mode(meta, text)
    chosen = re.search(
        r"Recorded human choice:\s*\*\*([^*]+)\*\*",
        section(text, r"Human slice selection"),
        re.I,
    )
    chosen_text = chosen.group(1).strip() if chosen else ""
    slice_id = re.match(r"(V[\w.-]+)", chosen_text)
    return {
        "source": str(path),
        "title": title(text, " — Breadboard"),
        "mode": mode,
        "requirements_authority": clean_value(authority_values.get("Requirements authority")) or "Unknown",
        "appetite_authority": clean_value(authority_values.get("Appetite authority")) or "Unknown",
        "places": first_table(section(text, r"Places")),
        "ui": first_table(section(text, r"UI affordances")),
        "non_ui": first_table(section(text, r"Non-UI affordances")),
        "stores": first_table(section(text, r"Stores")),
        "behavior_traces": first_table(section(text, r"Behavior traces")),
        "reverse_trace": first_table(section(text, r"Reverse-trace audit")),
        "slices": parse_slices_from_breadboard(text),
        "active_slice": slice_id.group(1) if slice_id else "",
        "active_slice_text": chosen_text,
        "meta": meta,
    }, text


def discover_slices_artifact(directory):
    directory = Path(directory)
    typed = []
    fallback = []
    for path in sorted(directory.glob("*.md")):
        artifact_type, _, _ = _artifact_type(path)
        if artifact_type == "slices":
            typed.append(path)
        elif "slices" in path.stem.lower():
            fallback.append(path)
    return (typed or fallback or [None])[0]


def parse_slices_artifact(path):
    if not path:
        return None
    meta, text = frontmatter(Path(path).read_text(encoding="utf-8"))
    rows = first_table(section(text, r"Slice inventory"))
    slices = [item for row in rows if (item := _normalize_slice_row(row))]
    selected = key_values(section(text, r"Selected slice"))
    active_raw = clean_value(selected.get("Slice"))
    match = re.match(r"(V[\w.-]+)", active_raw)
    return {
        "source": str(path),
        "slices": slices,
        "active_slice": match.group(1) if match else "",
        "active_slice_text": active_raw,
        "meta": meta,
    }


def validate_package(package):
    errors = []
    shaping = package["shaping"]
    breadboard = package["breadboard"]

    if shaping.get("decision_status") == "selected" or shaping.get("selected_shape"):
        if not shaping["requirements"]:
            errors.append(f"{package['sources']['shaping']}: selected shaping has no parsed requirements")
        if shaping.get("requirements_authority") != "Accepted":
            errors.append(f"{package['sources']['shaping']}: selected shaping requirements must be Accepted")
        if shaping.get("appetite_authority") != "Accepted":
            errors.append(f"{package['sources']['shaping']}: selected shaping Appetite must be Accepted")
        if not shaping.get("selected_shape"):
            errors.append(f"{package['sources']['shaping']}: selected decision has no recognized chosen direction")
        elif shaping["selected_shape"] not in {item["id"] for item in shaping["shapes"]}:
            errors.append(f"{package['sources']['shaping']}: chosen direction is not a declared shape")

    if breadboard.get("mode") == "selected-design":
        current_contract = clean_value(breadboard["meta"].get("artifact_type")).lower() == "breadboard"
        if current_contract:
            if clean_value(breadboard["meta"].get("source_of_truth")).lower() != "true":
                errors.append(f"{package['sources']['breadboard']}: accepted selected-design breadboard must set source_of_truth: true")
            if breadboard.get("requirements_authority") != "Accepted":
                errors.append(f"{package['sources']['breadboard']}: selected-design Requirements authority must be Accepted")
            if breadboard.get("appetite_authority") != "Accepted":
                errors.append(f"{package['sources']['breadboard']}: selected-design Appetite authority must be Accepted")
        if not breadboard["places"]:
            errors.append(f"{package['sources']['breadboard']}: selected-design breadboard has no parsed places")
        if not breadboard["behavior_traces"]:
            errors.append(f"{package['sources']['breadboard']}: selected-design breadboard has no parsed behavior traces")

    known = set()
    for row in shaping["requirements"]:
        if row.get("ID"):
            known.add(row["ID"])
    for shape in shaping["shapes"]:
        known.add(shape["id"])
        known.update(row.get("Part", "") for row in shape["parts"] if row.get("Part"))
    for key in ("places", "ui", "non_ui", "stores"):
        known.update(row.get("ID", "") for row in breadboard[key] if row.get("ID"))
    known.update(item["id"] for item in breadboard["slices"])

    referenced = set()
    for key in ("ui", "non_ui"):
        for row in breadboard[key]:
            referenced.update(re.findall(r"\b(?:P|U|N|S)\d+(?:\.\d+)?\b", " ".join(str(v) for v in row.values())))
    for row in breadboard["behavior_traces"]:
        referenced.update(re.findall(r"\b(?:P|U|N|S)\d+(?:\.\d+)?\b", " ".join(str(v) for v in row.values())))
    missing = sorted(ref for ref in referenced if ref not in known)
    if missing:
        errors.append(f"{package['sources']['breadboard']}: references unknown breadboard IDs: {', '.join(missing)}")

    if errors:
        raise ContractError("Publication readiness failed:\n- " + "\n- ".join(errors))
    return package
