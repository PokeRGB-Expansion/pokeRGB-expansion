#!/usr/bin/env python3
"""Verify the pre-build audit's linked data with a built English pokered checkout."""

import argparse
import hashlib
import json
from pathlib import Path


def read_symbols(path):
    symbols = {}
    for line in path.read_text().splitlines():
        if line and not line.startswith(";"):
            address, name = line.split()
            if ":" not in address:
                continue
            bank, offset = address.split(":")
            symbols[name] = (int(bank, 16), int(offset, 16))
    return symbols


def linked_offset(symbol):
    bank, address = symbol
    return bank * 0x4000 + address % 0x4000


def verify_color(checkout, color, expected):
    stem = checkout / f"poke{color}"
    rom = stem.with_suffix(".gbc").read_bytes()
    symbols = read_symbols(stem.with_suffix(".sym"))
    if hashlib.sha1(rom).hexdigest() != expected["rom_sha1"]:
        raise ValueError(f"Expected the stock English {color} ROM.")

    pos = linked_offset(symbols["PokemonTower2FRivalEncounterEventCoords"])
    points = []
    while rom[pos] != 0xFF:
        points.append([rom[pos + 1], rom[pos]])
        pos += 2
    tower = expected["tower_2f"]
    assert len(points) == tower["pairs_before_terminator"]
    assert points[:2] == tower["expected_xy"]
    extra = [p for p in points[2:] if p[0] < 20 and p[1] < 18]
    assert extra == tower["extra_xy_within_20_by_18"]

    blocks = (checkout / "maps/PokemonTower2F.blk").read_bytes()
    tiles = (checkout / "gfx/blocksets/cemetery.bst").read_bytes()
    pos = linked_offset(symbols["Cemetery_Coll"])
    walkable = set(rom[pos:rom.index(0xFF, pos)])
    for entry in tower["terrain"]:
        x, y = entry["xy"]
        block = blocks[(y // 2) * 10 + x // 2]
        lower_left = tiles[block * 16 + (y % 2) * 8 + (x % 2) * 2 + 4]
        assert lower_left == entry["lower_left_tile"]
        assert (lower_left in walkable) == entry["walkable"]

    pos = linked_offset(symbols["BenchGuyTextPointers"])
    bench = expected["bench_text"]
    assert len(set(rom[pos:pos + bench["terminator_offset"]:3])) == bench["records"]
    assert rom[pos + bench["terminator_offset"]] == 0xFF

    _, start = symbols["wMapSpriteData"]
    movement = expected["sprite_movement"]
    assert int(movement["table_address"], 16) == start
    for slot in (14, 15):
        index = 2 * (slot - 1)
        wrapped = (start & 0xFF00) | ((start + index) & 0xFF)
        if slot == 14:
            assert start + index == wrapped == int(movement["slot_14_expected_and_read"], 16)
        else:
            assert start + index == int(movement["slot_15_expected"], 16)
            assert wrapped == int(movement["slot_15_read"], 16)

    invalid = [x for x in range(256) if (8 if x < 7 else x) >> 3 == 0]
    assert invalid == expected["slot_machine"]["random_byte_with_unmatchable_zero"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path, help="Built checkout with ROM and .sym files")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "research/foundation-checks.json").read_text())
    for color, expected in data["binary_and_source_models"].items():
        verify_color(args.checkout, color, expected)
    print("Verified both ROMs, Tower coordinates and terrain, bench records, movement addresses and slot-selector model.")


if __name__ == "__main__":
    main()
