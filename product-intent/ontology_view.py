#!/usr/bin/env python3
"""Render a read-only ontology view of a canonical PlanningPackage.

No decisions are made or persisted here. No check result is inferred from a plan.
"""
import argparse
import json
from pathlib import Path

TEMPLATE = Path(__file__).with_name('ontology_view_template.html')


def _value(data, *fields):
    for name in fields:
        value = data.get(name)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ''


def _normalize_record(row):
    data = row.get('data', {}) if isinstance(row.get('data'), dict) else row
    kind = row.get('kind', 'requirement')
    ident = row.get('uid') or (kind + ':' + row.get('id', ''))
    title = _value(row, 'title') or _value(data, 'Requirement', 'Name', 'Title', 'Behavior', 'Decision', 'Summary') or row.get('id', ident)
    statement = _value(row, 'statement') or _value(data, 'Requirement', 'Statement', 'Description', 'Need', 'Meaning', 'Behavior', 'Why') or title
    status = row.get('status', 'working')
    return {
        'uid': ident, 'id': row.get('id', ident), 'kind': kind, 'title': str(title),
        'statement': str(statement), 'status': status, 'source': row.get('source', ''),
        'refs': row.get('resolved_refs') or row.get('refs') or [],
        'evidence': row.get('evidence') or [], 'verification': row.get('verification') or [],
        'approved_by': row.get('approved_by') or '',
        'alternatives': row.get('alternatives') or [],
        'reopen_when': row.get('reopen_when') or '',
    }


def project_package(package):
    if package.get('kind') != 'PlanningPackage':
        raise ValueError('Expected a compiled PlanningPackage, not a standalone intent guess')
    model = package.get('product_intent')
    if model is not None and (not isinstance(model, dict) or model.get('kind') != 'ProductIntentModel'):
        raise ValueError('Malformed product_intent; refusing to infer authority')
    shaping = package.get('shaping') or {}
    if model:
        records = [_normalize_record(x) for x in model.get('planning_records', []) + model.get('extension_records', [])]
        bindings = model.get('bindings', [])
    else:
        records = [_normalize_record({
            'kind': 'requirement', 'id': r.get('ID') or r.get('id') or '?',
            'status': 'accepted' if str((package.get('authority') or {}).get('requirements', '')).lower() == 'accepted' else 'working',
            'source': (package.get('sources') or {}).get('shaping', ''), 'data': r,
        }) for r in shaping.get('requirements', [])]
        bindings = []
    if len({r['uid'] for r in records}) != len(records):
        raise ValueError('Duplicate ontology identifiers')
    return {
        'schema_version': 1,
        'title': str(package.get('title') or (model or {}).get('product') or 'Product'),
        'authority': package.get('authority') or {},
        'has_intent_model': bool(model),
        'selected_shape': shaping.get('selected_shape') or '',
        'selected_slice': (package.get('breadboard') or {}).get('active_slice') or '',
        'records': records,
        'bindings': bindings,
        'sources': package.get('sources') or {},
        'unlinked_accepted_requirements': (model or {}).get('unlinked_accepted_requirements') or [],
    }


def render_html(package):
    data = project_package(package)
    # Escape script-breaking and HTML-significant characters in untrusted artifact text.
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    payload = payload.replace('&', r'\u0026').replace('<', r'\u003c').replace('>', r'\u003e').replace('\u2028', r'\u2028').replace('\u2029', r'\u2029')
    template = TEMPLATE.read_text(encoding='utf-8')
    token = '__ONTOLOGY_JSON_PAYLOAD__'
    if template.count(token) != 1:
        raise ValueError('Ontology viewer template payload placeholder missing/duplicated')
    return template.replace(token, payload)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Render product intent without inventing implementation status')
    parser.add_argument('--package', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    result = render_html(json.loads(args.package.read_text(encoding='utf-8')))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result, encoding='utf-8')
    print(args.output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
