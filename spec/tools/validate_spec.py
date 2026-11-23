#!/usr/bin/env python3
"""Check specification links, research records, and optional source checkouts."""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit


def anchors(text):
    values = set(re.findall(r'<a\s+id="([^"]+)"', text))
    for line in text.splitlines():
        if re.match(r'^#{1,6} ', line):
            title = re.sub(r'^#{1,6} ', '', line).strip().lower()
            title = re.sub(r'[^\w\- ]', '', title)
            values.add(title.replace(' ', '-'))
    return values


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path,
                        help='Optional directory containing checkout folders named by source-lock keys.')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    errors = []
    links = 0
    for file in root.rglob('*.md'):
        text = file.read_text(encoding='utf-8')
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            parsed = urlsplit(target)
            if parsed.scheme:
                continue
            path = (file.parent / unquote(parsed.path)).resolve() if parsed.path else file
            links += 1
            if not path.is_file():
                errors.append(f'{file.relative_to(root)}: missing target {target}')
            elif parsed.fragment and path.suffix == '.md':
                if unquote(parsed.fragment) not in anchors(path.read_text(encoding='utf-8')):
                    errors.append(f'{file.relative_to(root)}: missing anchor {target}')
    lock = json.loads((root / 'research/source-lock.json').read_text())
    pins = {entry['key']: entry for entry in lock['repositories']}
    evidence = json.loads((root / 'research/evidence-index.json').read_text())['evidence']
    ids = [entry['id'] for entry in evidence]
    if len(ids) != len(set(ids)):
        errors.append('Duplicate evidence IDs.')
    for entry in evidence:
        for source in entry['sources']:
            if 'path' not in source:
                continue
            key = source['repository_key']
            if source['commit'] != pins[key]['commit']:
                errors.append(f"{entry['id']}: source pin mismatch")
            if source['start_line'] < 1 or source['end_line'] < source['start_line']:
                errors.append(f"{entry['id']}: invalid line range")
            if args.source_root:
                checkout = args.source_root / key
                path = checkout / source['path']
                if not path.is_file():
                    errors.append(f"{entry['id']}: missing checked source {path}")
                    continue
                data = path.read_bytes()
                if hashlib.sha256(data).hexdigest() != source['file_sha256']:
                    errors.append(f"{entry['id']}: changed source file {path}")
                if source['end_line'] > len(data.decode('utf-8').splitlines()):
                    errors.append(f"{entry['id']}: source range exceeds file")
    if args.source_root:
        for key, pin in pins.items():
            revision = subprocess.check_output(
                ['git', '-C', str(args.source_root / key), 'rev-parse', 'HEAD'], text=True).strip()
            if revision != pin['commit']:
                errors.append(f'{key}: checkout revision differs from source lock')
    for name, expected, field in [('bug-catalog.csv', 94, 'catalog_id')]:
        with (root / 'research' / name).open(newline='', encoding='utf-8') as stream:
            rows = list(csv.DictReader(stream))
        if len(rows) != expected or len({r[field] for r in rows}) != expected:
            errors.append(f'{name}: expected {expected} distinct catalog records')
        review = (root / 'research/catalog-decisions.md').read_text()
        for record in rows:
            anchor = record['catalog_id'].lower()
            if record.get('decision_record') != f'catalog-decisions.md#{anchor}':
                errors.append(f'{anchor}: missing decision reference')
            matching = [line for line in review.splitlines() if f'id="{anchor}"' in line]
            if len(matching) != 1 or f' | {record["disposition"]} | ' not in matching[0]:
                errors.append(f'{anchor}: missing or inconsistent preset decision')

    with (root / 'research/usability-coverage.csv').open(newline='', encoding='utf-8') as stream:
        usability = list(csv.DictReader(stream))
    for number, case in enumerate(usability, start=1):
        case_id = f'UC-{number:02}'
        if case['case_id'] != case_id:
            errors.append(f'{case_id}: missing, duplicate or unordered usability case')
        for field in ('disposition', 'preset_review', 'remaining_check'):
            if not case[field].strip():
                errors.append(f'{case_id}: missing {field}')

    with (root / 'research/critical-hit-thresholds.csv').open(newline='', encoding='utf-8') as stream:
        rows = list(csv.DictReader(stream))
    keys = {(r['base_speed'], r['high_critical'], r['pumped']) for r in rows}
    if len(rows) != 1024 or len(keys) != 1024:
        errors.append('Critical threshold data must contain 1,024 distinct input combinations.')
    for error in errors:
        print(error)
    if errors:
        raise SystemExit(1)
    print(f'Checked {links} local links and {len(evidence)} evidence records.')
    print(f'Catalog: 94 records. Usability: {len(usability)} records. Critical thresholds: 1,024 distinct inputs.')
    if args.source_root:
        print('All cited source file hashes, line ranges and repository revisions match.')
    print('External web availability and compiled game behavior are not tested by this check.')


if __name__ == '__main__':
    main()
