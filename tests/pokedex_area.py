"""Check Core's Pokédex AREA menu and encounter map storage."""

import argparse
from collections import Counter
from pathlib import Path

from adventure_checkpoints import A, DOWN, shows
from cartridge_smoke import Game
from sprite_storage import direct_access


BANK_SIZE = 0x4000
SLOT_COUNT = 10
MARKER_SLOTS = 36
NEST_TILE = 4
BACKGROUND_NEST_TILE = 0x70
EXCLUDED_CAVE_COORDS = 0x19


def rom_offset(bank, address):
    return bank * BANK_SIZE + address - 0x4000


def linked_offset(game, name):
    return rom_offset(*game.addresses[name])


def map_pointers(game, rom):
    start = linked_offset(game, "WildDataPointers")
    pointers = []
    for entry in range(start, len(rom) - 1, 2):
        address = int.from_bytes(rom[entry:entry + 2], "little")
        if address >> 8 == 0xFF:
            return pointers
        pointers.append(address)
    raise AssertionError("WildDataPointers has no terminator.")


def dex_species(game, rom):
    start = linked_offset(game, "PokedexOrder")
    table = rom[start:start + 190]
    return {dex: species for species, dex in enumerate(table, 1) if 1 <= dex <= 151}


def habitat_maps(game, rom):
    bank, _ = game.addresses["WildDataPointers"]
    found = {}
    for map_id, address in enumerate(map_pointers(game, rom)):
        cursor = rom_offset(bank, address)
        for _ in range(2):
            rate = rom[cursor]
            cursor += 1
            if rate:
                end = cursor + SLOT_COUNT * 2
                for species in rom[cursor + 1:end:2]:
                    found.setdefault(species, set()).add(map_id)
                cursor = end
    return found


def marker_coordinates(game, rom, maps):
    external = linked_offset(game, "ExternalMapEntries")
    internal = linked_offset(game, "InternalMapEntries")
    external_count = (internal - external) // 3
    coordinates = []
    for map_id in sorted(maps):
        if map_id == 0:
            continue
        if map_id < external_count:
            packed = rom[external + map_id * 3]
        else:
            for offset in range(internal, len(rom), 4):
                if map_id < rom[offset]:
                    packed = rom[offset + 1]
                    break
        if packed != EXCLUDED_CAVE_COORDS and packed not in coordinates:
            coordinates.append(packed)
    return coordinates


def marker_sprites(coordinates):
    return b"".join(bytes(((tile >> 4) * 8 + 24, (tile & 15) * 8 + 24, NEST_TILE, 0))
                    for tile in coordinates)


def check_collector(game, rom):
    expected = habitat_maps(game, rom)
    dex_entries = dex_species(game, rom)
    assert len(dex_entries) == 151
    start = game.addresses["wPokedexAreaMaps"][1]
    flags_length = game.addresses["wPokedexAreaMarkers"][1] - start
    scratch_end = game.addresses["wPokedexAreaWorkEnd"][1]
    backup_end = game.addresses["wShadowOAMBackupEnd"][1]
    guard = bytes((0xA5,)) * (backup_end - scratch_end)
    game.write(scratch_end, guard)
    for dex, species in sorted(dex_entries.items()):
        game.put("wBuffer", (0x5A,) * 30)
        game.put("wPokedexNum", (species,))
        game.invoke("FindWildLocationsOfMon")
        game.return_to_stub()
        flags = int.from_bytes(game.get_bytes("wPokedexAreaMaps", flags_length), "little")
        maps = {index for index in range(flags_length * 8) if flags & (1 << index)}
        assert maps == expected.get(species, set()), (dex, maps, expected.get(species))
        assert game.get_bytes("wBuffer", 30) == bytes((0x5A,)) * 30
        assert game.get_bytes("wPokedexAreaWorkEnd", len(guard)) == guard
        coordinates = marker_coordinates(game, rom, maps)
        expected_sprites = marker_sprites(coordinates)
        game.put("wShadowOAM", bytes((MARKER_SLOTS + 4) * 4))
        game.invoke("DrawPokedexAreaMarkers")
        game.return_to_stub()
        assert game.get_bytes("wShadowOAM", len(expected_sprites)) == expected_sprites, dex
        assert not game.get("wPokedexAreaBackgroundUsed"), dex
        assert game.get_bytes("wBuffer", 30)[1:] == bytes((0x5A,)) * 29
        assert game.get_bytes("wPokedexAreaWorkEnd", len(guard)) == guard


def open_area(game, dex, name):
    seen = bytearray(19)
    byte, bit = divmod(dex - 1, 8)
    seen[byte] = 1 << bit
    game.put("wPokedexSeen", seen)
    game.put("wPokedexSavedScrollOffset", (max(dex - 7, 0),))
    game.put("wPokedexSavedRow", (min(dex - 1, 6),))
    game.invoke("ShowPokedexMenu")
    shows(game, name, "AREA", "DATA")
    game.tick(20)
    game.press(A)
    game.wait(lambda: game.get("wTopMenuItemX") == 15)
    game.tick(15)
    game.press(DOWN)
    game.press(DOWN)
    assert game.get("wCurrentMenuItem") == 2
    game.press(A)
    shows(game, name, "NEST")
    game.tick(20)


def check_visible_markers(game, coordinates):
    sprites = []
    background_coordinates = []
    rows = Counter()
    for coordinate in coordinates:
        row = coordinate >> 4
        if len(sprites) < MARKER_SLOTS and rows[row] < 8:
            sprites.append(coordinate)
            rows[row] += 1
        else:
            background_coordinates.append(coordinate)
    data = game.get_bytes("wShadowOAMBackup", (MARKER_SLOTS + 4) * 4)
    first_markers = data[:MARKER_SLOTS * 4]
    expected = marker_sprites(sprites)
    assert first_markers[:len(expected)] == expected
    assert NEST_TILE not in first_markers[len(expected) + 2::4]
    background = set()
    for tile in range(256):
        x = (tile & 15) + 2
        y = (tile >> 4) + 1
        if game.get("wTileMap", y * 20 + x) == BACKGROUND_NEST_TILE:
            background.add(tile)
    assert background == set(background_coordinates)
    if background:
        vram = direct_access(game, 3)
        lcd = game.core.GB_safe_read_memory(game.gb, 0xFF40)
        assert lcd & 0x20  # AREA draws through the Game Boy window.
        bg_map = 0x1C00 if lcd & 0x40 else 0x1800
        for tile in background:
            x = (tile & 15) + 2
            y = (tile >> 4) + 1
            assert vram[bg_map + y * 32 + x] == BACKGROUND_NEST_TILE
        icon = linked_offset(game, "MonNestIcon")
        source = direct_access(game, 0)[icon:icon + 8]
        assert bytes(vram[0x1700:0x1710]) == bytes(value for row in source for value in (row, row))
    if coordinates:
        # The player icon still uses the last four reserved slots.
        assert all(data[offset] == tile
                   for tile, offset in enumerate(range(MARKER_SLOTS * 4 + 2, len(data), 4)))
    else:
        shows(game, "AREA UNKNOWN")


def add_duplicate_map_sample(game, rom, species):
    maps = map_pointers(game, rom)
    bank, _ = game.addresses["WildDataPointers"]
    # Reuse one record with land and water data in the disposable emulator.
    address = next(address for address in maps
                   if rom[rom_offset(bank, address)]
                   and rom[rom_offset(bank, address) + 1 + SLOT_COUNT * 2])
    start = rom_offset(bank, address)
    # Both habitats repeat the same species in every slot.
    habitat = bytes((1,)) + bytes((5, species)) * SLOT_COUNT
    data = habitat + habitat
    rom[start:start + len(data)] = data
    pointers = linked_offset(game, "WildDataPointers")
    rom[pointers:pointers + 2 * len(maps)] = address.to_bytes(2, "little") * len(maps)


def check(library, boot, cartridge):
    with Game(library, boot, cartridge) as game:
        game.tick(240)
        check_collector(game, direct_access(game, 0))
    samples = ((16, "PIDGEY"), (92, "GASTLY"), (72, "TENTACOOL"), (129, "MAGIKARP"))
    for dex, name in samples:
        with Game(library, boot, cartridge) as game:
            game.new_game()
            rom = direct_access(game, 0)
            species = dex_species(game, rom)[dex]
            maps = habitat_maps(game, rom).get(species, set())
            coordinates = marker_coordinates(game, rom, maps)
            open_area(game, dex, name)
            check_visible_markers(game, coordinates)
            if name == "MAGIKARP":
                assert not maps  # Fishing catches still do not appear in AREA.
            game.press(5)
            shows(game, "DATA", "AREA")
    with Game(library, boot, cartridge) as game:
        game.new_game()
        rom = direct_access(game, 0)
        add_duplicate_map_sample(game, rom, dex_species(game, rom)[16])
        maps = habitat_maps(game, rom)[dex_species(game, rom)[16]]
        coordinates = marker_coordinates(game, rom, maps)
        assert len(coordinates) > MARKER_SLOTS
        open_area(game, 16, "PIDGEY")
        check_visible_markers(game, coordinates)
        game.press(5)
        shows(game, "DATA", "AREA", "PIDGEY")
    print(f"{cartridge}: 151 land/Surf searches, four AREA menu checks, and large map sample passed",
          flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        check(args.sameboy, args.boot, args.directory / f"poke{color}.gbc")


if __name__ == "__main__":
    main()
