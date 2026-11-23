#!/usr/bin/env python3
"""Check bag allocations at the specification's pinned pokered revision."""

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile


REVISION = 'af519899719f0754965776faac0e836a3b906e6d'


def run(command, cwd):
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True)


def symbols(path):
    result = {}
    for line in path.read_text().splitlines():
        parts = line.split()
        if len(parts) == 2 and ':' in parts[0]:
            result[parts[1]] = parts[0]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-checkout', type=Path, required=True)
    parser.add_argument('--rgbds-bin', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    checkout = args.source_checkout.resolve()
    tool_dir = args.rgbds_bin.resolve()
    revision = subprocess.check_output(
        ['git', '-C', str(checkout), 'rev-parse', 'HEAD'], text=True).strip()
    if revision != REVISION:
        parser.error('The source checkout must use revision ' + REVISION)
    versions = {}
    for name in ('rgbasm', 'rgblink'):
        versions[name] = subprocess.check_output(
            [str(tool_dir / name), '--version'], text=True).strip()

    with tempfile.TemporaryDirectory(prefix='pokergb-bag-audit-') as temp:
        work = Path(temp)
        archive = work / 'source.tar'
        subprocess.run([
            'git', '-C', str(checkout), 'archive', REVISION,
            'includes.asm', 'ram.asm', 'layout.link', 'constants', 'macros',
            'ram', '-o', str(archive)], check=True)
        with tarfile.open(archive) as bundle:
            for member in bundle.getmembers():
                path = Path(member.name)
                if path.is_absolute() or '..' in path.parts or member.issym() or member.islnk():
                    raise ValueError('Unexpected archive member: ' + member.name)
            bundle.extractall(work)
        layout = (work / 'layout.link').read_text()
        # OAM DMA is defined in a game-code object omitted from this RAM audit.
        layout = ('WRAM0\n' + layout.split('WRAM0\n', 1)[1]).replace(
            '\t"OAM DMA"\n', '')
        (work / 'ram-layout.link').write_text(layout)
        ram = work / 'ram/wram.asm'
        constants = work / 'constants/menu_constants.asm'
        original_ram = ram.read_text()
        original_constants = constants.read_text()
        fingerprints = {
            path: hashlib.sha256((work / path).read_bytes()).hexdigest()
            for path in ('ram/wram.asm', 'constants/menu_constants.asm', 'layout.link')
        }

        def build(name, capacity, ram_source):
            ram.write_text(ram_source)
            constants.write_text(original_constants.replace(
                'BAG_ITEM_CAPACITY EQU 20', f'BAG_ITEM_CAPACITY EQU {capacity}'))
            row = {'capacity': capacity}
            commands = [
                [str(tool_dir / 'rgbasm'), '-Q8', '-P', 'includes.asm', '-D',
                 '_RED', '-o', name + '.o', 'ram.asm'],
                [str(tool_dir / 'rgblink'), '-d', '-l', 'ram-layout.link', '-n',
                 name + '.sym', '-o', name + '.bin', name + '.o'],
            ]
            for command in commands:
                result = run(command, work)
                if result.returncode:
                    row.update(allocation_passed=False, error=result.stderr.strip())
                    return row, {}
            row['allocation_passed'] = True
            found = symbols(work / (name + '.sym'))
            for label in ('wNumBagItems', 'wBagItems', 'wPlayerMoney',
                          'wMainDataEnd', 'wBoxDataEnd'):
                row[label] = found[label]
            return row, found

        constant_rows = []
        baseline = None
        for capacity in (20, 21, 40, 60):
            row, found = build(f'constant-{capacity}', capacity, original_ram)
            assert row['allocation_passed'] == (capacity in (20, 21)), row
            constant_rows.append(row)
            if capacity == 20:
                baseline = found
                assert found['wBagItems'] == '00:d31e'
                assert found['wPlayerMoney'] == '00:d347'
            elif capacity == 21:
                assert found['wBagItems'] == baseline['wBagItems']
                assert found['wPlayerMoney'] == '00:d349'

        old = ('wNumBagItems:: db\n; item, quantity\n'
               'wBagItems:: ds BAG_ITEM_CAPACITY * 2 + 1')
        reserve = '\tds 78\nwGameProgressFlagsEnd::\n\n\tds 56'
        assert original_ram.count(old) == original_ram.count(reserve) == 1
        alternate = original_ram.replace(
            old, 'wLegacyNumBagItems:: db\nwLegacyBagItems:: ds 41')
        alternate = alternate.replace(reserve, 'UNION\n' + reserve + '''
NEXTU
wBagSaveVersion:: ds 4
wNumBagItems:: db
wBagItems:: ds BAG_ITEM_CAPACITY * 2 + 1
wExpandedBagEnd::
ASSERT wExpandedBagEnd - wBagSaveVersion <= 134
ENDU''')
        relocated_rows = []
        for capacity in (60, 64, 65):
            row, found = build(f'relocated-{capacity}', capacity, alternate)
            assert row['allocation_passed'] == (capacity <= 64), row
            if row['allocation_passed']:
                changes = {
                    name: [address, found.get(name)]
                    for name, address in baseline.items()
                    if name.startswith('w') and name not in ('wNumBagItems', 'wBagItems')
                    and found.get(name) != address
                }
                assert not changes, changes
                assert found['wBagItems'] == '00:d66f'
                row['other_wram_address_changes'] = changes
            else:
                assert 'Assertion failed' in row['error'], row
            relocated_rows.append(row)

    report = {
        'checked_date': date.today().isoformat(),
        'kind': 'RAM allocation/link audit; no gameplay or save-compatibility result',
        'pokered_commit': REVISION,
        'toolchain': versions,
        'source_sha256': fingerprints,
        'method': 'Link upstream RAM sections in upstream order with -d; omit the OAM DMA section from the RAM-only script. Compare WRAM labels only.',
        'constant_only_experiments': constant_rows,
        'separate_134_byte_reserve_with_4_byte_marker': relocated_rows,
    }
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print('Checked seven RAM allocations; all expected results match.')
    print('Other WRAM addresses stay fixed when the bag uses the separate reserve.')
    print('Game behavior, save conversion, and feature combinations were not tested.')


if __name__ == '__main__':
    main()
