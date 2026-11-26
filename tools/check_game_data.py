"""Check encounter species and rendered INFO text in a newly built game."""

import argparse
from pathlib import Path

from check_reference_colors import Cartridge


def read_pointer(rom, pos):
    # These tables use 16-bit pointers in their own ROM bank.
    address = int.from_bytes(rom.data[pos:pos + 2], "little")
    if not 0x4000 <= address < 0x8000:
        raise ValueError(f"Invalid banked pointer ${address:04x} at ROM offset ${pos:x}.")
    return (pos // 0x4000) * 0x4000 + address - 0x4000


def check_species(dex, species, location):
    if not 1 <= species <= len(dex) or not dex[species - 1]:
        raise ValueError(f"{location}: species ${species:02x} has no Pokédex entry. "
                         "Use a species with an entry in data/pokemon/dex_order.asm.")


def check_encounters(rom, labels, dex):
    slots = len(rom.between("WildMonEncounterSlotChances", "WildMonEncounterSlotChances.end")) // 2

    def check_group(pos, count, group):
        for slot in range(count):
            species = rom.data[pos + 2 * slot + 1]
            check_species(dex, species, f"{group}, slot {slot + 1}")
        return pos + 2 * count

    pos = rom.offset("WildDataPointers")
    checked = set()
    while rom.data[pos:pos + 2] != b"\xff\xff":
        start = read_pointer(rom, pos)
        pos += 2
        if start in checked:
            continue
        checked.add(start)
        group = labels.get(start, f"wild table at ${start:x}")
        entry = start
        for habitat in ("grass", "water"):
            rate = rom.data[entry]
            entry += 1
            if rate:
                entry = check_group(entry, slots, f"{group} {habitat}")

    pos = rom.offset("SuperRodData")
    checked.clear()
    while rom.data[pos] != 0xff:
        start = read_pointer(rom, pos + 1)
        pos += 3
        if start not in checked:
            checked.add(start)
            check_group(start + 1, rom.data[start], labels.get(start, f"fishing table at ${start:x}"))


def check_descriptions(rom, labels):
    descriptions = {rom.offset(name) for name in ("MoveInfoHighCritical", "MoveInfoPriority", "MoveInfoBothTraits")}
    for pos in range(rom.offset("MoveInfoDescriptions"), rom.offset("MoveInfoDescriptions.end"), 2):
        descriptions.add(read_pointer(rom, pos))
    for table, end, width in (("MoveInfoSpecificDescriptions", 0, 4), ("SupplyInfoEntries", 0xff, 3)):
        pos = rom.offset(table)
        while rom.data[pos] != end:
            descriptions.add(read_pointer(rom, pos + width - 2))
            pos += width

    for start in sorted(descriptions):
        name = labels.get(start, f"INFO at ${start:x}")
        end = rom.data.find(b"\x00", start, (start // 0x4000 + 1) * 0x4000)
        if end == -1:
            raise ValueError(f"{name}: end the INFO description with a zero byte.")
        # @ ends a row. Each encoded glyph takes one tile, including contractions.
        lines = rom.data[start:end].removesuffix(b"\x50").split(b"\x50")
        if len(lines) > 3:
            raise ValueError(f"{name}: INFO has {len(lines)} rows. Use at most 3.")
        for row, line in enumerate(lines, 1):
            if len(line) > 18:
                raise ValueError(f"{name}, row {row}: INFO has {len(line)} tiles. Use at most 18 per row.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("game", type=Path)
    args = parser.parse_args()
    rom = Cartridge(args.game)
    labels = {rom.offset(name): name for name, (_, address) in rom.symbols.items()
              if address < 0x8000 and "._" not in name and not name.endswith(".end")}
    try:
        dex = rom.between("PokedexOrder", "PokedexOrder.end")
        for slot, species in enumerate(rom.table("OaksLabStarterBalls", 12)[::4], 1):
            check_species(dex, species, f"Lab starter {slot}")
        check_encounters(rom, labels, dex)
        check_descriptions(rom, labels)
    except ValueError as error:
        parser.exit(1, f"{args.game}: {error}\n")


if __name__ == "__main__":
    main()
