#!/usr/bin/env python3
"""Compare selected gameplay tables in the English Red, Blue and Yellow retail builds."""

import argparse
import hashlib
import json
from pathlib import Path
import re

from check_foundation_tables import linked_offset, read_symbols


ROM_HASHES = {
    "pokered": "ea9bcae617fdf159b045185467ae58b2e4a48b9a",
    "pokeblue": "d7037c83e1ae5b39bde3c30787637ba1d4c48ce2",
    "pokeyellow": "cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1",
}


def level_records(rom, pointers, internal_index):
    pos = pointers + 2 * internal_index
    address = int.from_bytes(rom[pos:pos + 2], "little")
    pos = linked_offset((pointers // 0x4000, address))
    evos = []
    while rom[pos]:
        length = {1: 3, 2: 4, 3: 3}[rom[pos]]
        evos.append(tuple(rom[pos:pos + length]))
        pos += length
    pos += 1
    moves = []
    while rom[pos]:
        moves.append(tuple(rom[pos:pos + 2]))
        pos += 2
    return evos, moves


def decode(folder, name):
    rom = (folder / f"{name}.gbc").read_bytes()
    if hashlib.sha1(rom).hexdigest() != ROM_HASHES[name]:
        raise ValueError(f"Expected the English retail {name} build.")
    symbols = read_symbols(folder / f"{name}.sym")

    def offset(label):
        return linked_offset(symbols[label])

    names = re.findall(r"^\s*const DEX_(\w+)", (folder / "constants/pokedex_constants.asm").read_text(), re.M)
    move_names = re.findall(r"^\s*move (\w+),", (folder / "data/moves/moves.asm").read_text(), re.M)
    if len(names) != 151 or len(move_names) != 165:
        raise ValueError("Expected all 151 Pokédex entries and all 165 moves.")
    order = rom[offset("PokedexOrder"):offset("PokedexOrder") + 190]
    machine_moves = list(rom[offset("TechnicalMachines"):offset("TechnicalMachines") + 55])
    species = {}
    for dex, species_name in enumerate(names, start=1):
        pos = offset("BaseStats") + 28 * (dex - 1)
        if dex == 151 and name != "pokeyellow":
            pos = offset("MewBaseStats")
        if rom[pos] != dex or order.count(dex) != 1:
            raise ValueError(f"Species mapping mismatch for {species_name}.")
        evos, moves = level_records(rom, offset("EvosMovesPointerTable"), order.index(dex))
        species[species_name] = {
            "base_stats": list(rom[pos + 1:pos + 6]),
            "types": list(rom[pos + 6:pos + 8]),
            "catch_rate": rom[pos + 8],
            "base_exp": rom[pos + 9],
            "starting_moves": list(rom[pos + 15:pos + 19]),
            "growth_rate": rom[pos + 19],
            "machines": [move_names[m - 1] for bit, m in enumerate(machine_moves)
                         if rom[pos + 20 + bit // 8] & (1 << (bit % 8))],
            "evolutions": evos,
            "level_moves": moves,
        }
    pos = offset("TypeEffects")
    chart = []
    while rom[pos] != 255:
        chart.append(tuple(rom[pos:pos + 3]))
        pos += 3
    pos = offset("Moves")
    return {
        "species": species,
        "move_rows": {m: list(rom[pos + i * 6:pos + (i + 1) * 6]) for i, m in enumerate(move_names)},
        "machine_moves": machine_moves,
        "chart": chart,
    }


def compare(red_blue_dir, yellow_dir):
    red = decode(red_blue_dir, "pokered")
    blue = decode(red_blue_dir, "pokeblue")
    yellow = decode(yellow_dir, "pokeyellow")
    if red != blue:
        raise ValueError("Red and Blue differ within the selected tables.")
    species_changes = {}
    for field in next(iter(red["species"].values())):
        changed = [n for n, attrs in red["species"].items() if attrs[field] != yellow["species"][n][field]]
        species_changes[field] = changed
    machines = {}
    for name in species_changes["machines"]:
        old = set(red["species"][name]["machines"])
        new = set(yellow["species"][name]["machines"])
        machines[name] = {"added": sorted(new - old), "removed": sorted(old - new)}
    return {
        "rom_sha1": ROM_HASHES,
        "species_count": len(red["species"]),
        "machine_count": len(red["machine_moves"]),
        "move_count": len(red["move_rows"]),
        "non_neutral_chart_rows": len(red["chart"]),
        "red_blue_equal_in_scope": True,
        "yellow_machine_move_table_equal": red["machine_moves"] == yellow["machine_moves"],
        "yellow_type_table_equal_in_order": red["chart"] == yellow["chart"],
        "yellow_changed_move_rows": [m for m in red["move_rows"] if red["move_rows"][m] != yellow["move_rows"][m]],
        "yellow_species_changed_by_field": species_changes,
        "yellow_machine_changes": machines,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("red_blue_dir", type=Path, help="Built pret/pokered checkout")
    parser.add_argument("yellow_dir", type=Path, help="Built pret/pokeyellow checkout")
    args = parser.parse_args()
    print(json.dumps(compare(args.red_blue_dir, args.yellow_dir), indent=2))


if __name__ == "__main__":
    main()
