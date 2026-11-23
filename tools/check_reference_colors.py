#!/usr/bin/env python3
"""Check selected gameplay tables and cartridge identities in the reference builds."""

import argparse
from pathlib import Path


class Cartridge:
    def __init__(self, path):
        self.data = path.read_bytes()
        self.symbols = {}
        for line in path.with_suffix(".sym").read_text().splitlines():
            if line and not line.startswith(";"):
                address, name = line.split()
                if ":" not in address:
                    continue
                bank, offset = (int(part, 16) for part in address.split(":"))
                self.symbols[name] = (bank, offset)
        assert len(self.data) % 0x4000 == 0, path
        assert (0xFF - sum(self.data[0x134:0x14D]) - 24) & 0xFF == self.data[0x14D], path

    def offset(self, symbol):
        bank, address = self.symbols[symbol]
        assert address < 0x8000, symbol
        return bank * 0x4000 + (address & 0x3FFF)

    def table(self, symbol, length):
        start = self.offset(symbol)
        result = self.data[start:start + length]
        assert len(result) == length, symbol
        return result

    def between(self, first, after):
        return self.table(first, self.offset(after) - self.offset(first))

    def until(self, symbol, terminator):
        start = self.offset(symbol)
        end = self.data.index(terminator, start)
        assert start // 0x4000 == end // 0x4000, symbol
        return self.data[start:end + 1]

    def title(self):
        return self.data[0x134:0x144].rstrip(b"\0").decode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Directory for one reference preset.")
    args = parser.parse_args()
    red, blue, green = (
        Cartridge(args.directory / f"poke{color}.gbc") for color in ("red", "blue", "green")
    )
    assert (red.title(), blue.title(), green.title()) == ("POKEMON RED", "POKEMON BLUE", "POKEMON GREEN")
    for label, length in (
        ("Moves", 165 * 6),
        ("TechnicalMachines", 55),
        ("PrizeMenuMon1Entries", 4),
        ("PrizeMenuMon1Cost", 7),
        ("PrizeMenuMon2Entries", 4),
        ("PrizeMenuMon2Cost", 7),
        ("PrizeMenuTMsEntries", 4),
        ("PrizeMenuTMsCost", 7),
        ("KeyItemFlags", 15),
    ):
        assert blue.table(label, length) == green.table(label, length), label
    for label in ("TypeEffects",):
        assert blue.until(label, b"\xff") == green.until(label, b"\xff"), label
    assert blue.between("BaseStats", "CryData") == green.between("BaseStats", "CryData"), "BaseStats"
    assert blue.between("TrainerDataPointers", "EvosMovesPointerTable") == green.between(
        "TrainerDataPointers", "EvosMovesPointerTable"
    ), "Trainer parties"
    assert red.table("PrizeMenuMon2Cost", 7) != blue.table("PrizeMenuMon2Cost", 7), "Version-specific prizes"
    print("Verified Red, Blue, and Green headers, version-specific prizes, and selected Blue/Green gameplay tables.")


if __name__ == "__main__":
    main()
