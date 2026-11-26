"""Check a full TM party preview, including its rendered return screen and held buttons."""

import argparse
from pathlib import Path
import struct
import zlib

from battle_stats_return import battle_ready, snapshot, start_battle
from cartridge_smoke import Game
from cgb_compatibility import display_pixels, start_menu_row
from move_info_authoring import shows
from pc_browsing import name_bytes
from shop_carry_count import bag
from title_smoke import SGB_HEIGHT, SGB_MODEL, SGB_WIDTH
from tm_party_info import A, B, DOWN, SELECT, START, open_counter, press

UP = 2
RAZOR_WIND = 0x0D
PARTY = (
    (0xB0, "CHARMANDER", "NOT ABLE"),
    (0x24, "PIDGEY", "ABLE"),
    (0x04, "CLEFAIRY", "NOT ABLE"),
    (0xA9, "GEODUDE", "NOT ABLE"),
    (0x66, "EEVEE", "NOT ABLE"),
    (0x96, "PIDGEOTTO", "KNOWS"),
)


def game_screen(pixels, sgb):
    if sgb:
        return tuple(pixels[(40 + y) * SGB_WIDTH + 48 + x] for y in range(144) for x in range(160))
    return tuple(pixels)


def region(screen, x, y, width, height):
    return tuple(pixel for row in range(y, y + height) for pixel in screen[row * 160 + x:row * 160 + x + width])


def write_gallery(path, screens, *, scale=2):
    # Arrange pairs of screens in reading order without blurring the pixels.
    assert screens and len(screens) % 2 == 0
    pairs, gap = len(screens) // 2, 4
    width = (320 + gap) * scale
    height = (144 * pairs + gap * (pairs - 1)) * scale
    rows = bytearray()
    for index in range(0, len(screens), 2):
        if index:
            rows.extend((b"\x00" + b"\xff" * (3 * width)) * (gap * scale))
        for y in range(144):
            row = (b"\xff" * (3 * gap * scale)).join(
                b"".join(rgb.to_bytes(3, "big") * scale for rgb in screen[y * 160:(y + 1) * 160])
                for screen in screens[index:index + 2]
            )
            rows.extend((b"\x00" + row) * scale)

    def chunk(name, data):
        return struct.pack(">I", len(data)) + name + data + struct.pack(">I", zlib.crc32(name + data))

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
                     + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b""))


def seed_six(game):
    game.new_game()
    game.put("wOptions", (0xC1,))
    game.put("wPlayerMoney", (1, 0, 0))
    game.put("wPartyCount", (6,))
    game.put("wPartySpecies", (*[species for species, _, _ in PARTY], 0xFF))
    for slot, (species, name, status) in enumerate(PARTY, 1):
        game.put(f"wPartyMon{slot}Species", (species,))
        game.put(f"wPartyMon{slot}Nick", name_bytes(name))
        game.put(f"wPartyMon{slot}Level", (23 + slot,))
        game.put(f"wPartyMon{slot}HP", (0, 35))
        game.put(f"wPartyMon{slot}MaxHP", (0, 50))
        game.put(f"wPartyMon{slot}Moves", (RAZOR_WIND if status == "KNOWS" else 0x21, 0, 0, 0))


def shop(game, *, sgb=False, gallery=None):
    pixels = display_pixels(game, SGB_WIDTH, SGB_HEIGHT) if sgb else display_pixels(game)
    seed_six(game)
    assert bool(game.get("wOnSGB")) == sgb
    open_counter(game, False, mart_row=2)
    shows(game, "RAZOR WIND", "START INFO")
    game.tick(30)
    initial = game_screen(pixels, sgb)
    expected_cursor = (game.get("wCurrentMenuItem"), game.get("wListScrollOffset"))
    bag_before = game.get_bytes("wNumBagItems", 42)
    party_before = game.get_bytes("wPartyMon1", 44 * 6)
    press(game, UP)
    shows(game, "REFLECT", "START INFO")
    press(game, START)
    shows(game, "REFLECT", "PSYCHIC", "EFFECT", "PARTY")
    game.tick(18)
    screens = [game_screen(pixels, sgb)]
    press(game, SELECT)
    shows(game, "REFLECT", "Doubles physical")
    game.tick(18)
    screens.append(game_screen(pixels, sgb))
    press(game, DOWN)
    shows(game, "RAZOR WIND", "Charges on turn 1")
    game.tick(18)
    screens.append(game_screen(pixels, sgb))
    # The highlighted machine and its two-thousand price are fresh behind INFO.
    assert region(screens[2], 40, 32, 120, 48) == region(initial, 40, 32, 120, 48)

    # Hold A beyond key repeat. Opening the preview must never start teaching or buying.
    game.core.GB_set_key_state(game.gb, A, True)
    game.tick(100)
    assert all(word in game.visible_text() for word in ("CHARMANDER", "PIDGEOTTO", "BACK"))
    game.core.GB_set_key_state(game.gb, A, False)
    game.tick(18)
    shows(game, "RAZOR WIND", "BACK", *[name for _, name, _ in PARTY])
    game.tick(25)
    screens.append(game_screen(pixels, sgb))
    labels = game.visible_text().splitlines()
    assert labels[13].split() == ["TM02", "RAZOR", "WIND"], labels
    assert labels[14].strip() == "2000", labels
    for row, (_, name, status) in enumerate(PARTY):
        assert len(set(region(screens[-1], 8, 16 * row, 16, 16))) >= 2, f"Missing icon for {name}"
        assert name in labels[2 * row], labels
        assert status == labels[2 * row + 1].strip(), labels
        assert len(set(region(screens[-1], 24, 16 * row, 8 * len(name), 8))) >= 2
        assert len(set(region(screens[-1], 96, 16 * row + 8, 8 * len(status), 8))) >= 2
    if gallery:
        write_gallery(gallery, screens)

    # Close with A and B together. Releasing B while A is held must not confirm a sale.
    for button in (A, B):
        game.core.GB_set_key_state(game.gb, button, True)
    game.tick(12)
    game.core.GB_set_key_state(game.gb, B, False)
    game.tick(50)
    game.core.GB_set_key_state(game.gb, A, False)
    game.tick(30)
    shows(game, "RAZOR WIND", "START INFO")
    assert (game.get("wCurrentMenuItem"), game.get("wListScrollOffset")) == expected_cursor
    assert game.get_bytes("wPlayerMoney", 3) == bytes((1, 0, 0))
    assert game.get_bytes("wNumBagItems", len(bag_before)) == bag_before
    assert game.get_bytes("wPartyMon1", len(party_before)) == party_before
    restored = game_screen(pixels, sgb)
    assert region(restored, 40, 32, 120, 48) == region(initial, 40, 32, 120, 48)
    assert region(restored, 8, 112, 144, 16) == region(initial, 8, 112, 144, 16)
    for _ in range(6):
        press(game, B)
        game.tick(45)
        if not game.get("wFontLoaded") & 1:
            break
    assert not game.get("wFontLoaded") & 1
    game.core.GB_set_key_state(game.gb, DOWN, True)
    game.wait(lambda: game.get("wYCoord") == 6)
    game.core.GB_set_key_state(game.gb, DOWN, False)
    game.tick(20)
    assert (game.get("wCurMap"), game.get("wXCoord")) == (0x7B, 6)


def check_bag_roster(game, context):
    # Fill only the unused part below SP. Its lowest untouched bytes measure
    # the margin inside the Game Boy's 256-byte stack on this path.
    low = game.addresses["wStack"][1] - 255
    pattern = bytes((29 + 43 * i) & 0xFF for i in range(game.cpu.sp - 2 - low))
    assert pattern
    game.write(low, pattern)
    press(game, START)
    shows(game, "RAZOR WIND", "PARTY")
    press(game, A)
    shows(game, "RAZOR WIND", "BACK")
    press(game, B)
    shows(game, "TM02", "START INFO")
    left = next((i for i, value in enumerate(pattern)
                 if game.core.GB_safe_read_memory(game.gb, low + i) != value), len(pattern))
    assert left > 0, f"{context} exhausted the reserved stack"
    print(f"{context}: {left} stack bytes untouched", flush=True)


def field_bag(game):
    seed_six(game)
    game.put("wNumBagItems", bag([(0xCA, 1)]))
    game.enter_map(12, 10, 5, 4)
    start_menu_row(game, 1)
    shows(game, "TM02", "START INFO")
    check_bag_roster(game, "Field Bag")
    press(game, B)
    shows(game, "ITEM", "OPTION")
    press(game, B)
    game.wait(lambda: not game.get("wFontLoaded") & 1)
    assert game.get_bytes("wNumBagItems", 4) == bag([(0xCA, 1)])


def battle_bag(game, *, sgb=False):
    pixels = display_pixels(game, SGB_WIDTH, SGB_HEIGHT) if sgb else display_pixels(game)
    start_battle(game, tower=False, scoped=False)
    game.tick(30)
    initial = game_screen(pixels, sgb)
    game.put("wNumBagItems", bag([(0xCA, 1)]))  # TM02, Razor Wind
    before = snapshot(game)
    stats = game.get_bytes("wBattleMonHP", 2)
    pp = game.get_bytes("wBattleMonPP", 4)
    press(game, DOWN)
    press(game, A)
    shows(game, "TM02", "START INFO")
    check_bag_roster(game, "Battle Bag")
    press(game, B)
    game.wait(lambda: battle_ready(game))
    game.tick(30)
    assert snapshot(game) == before
    assert region(game_screen(pixels, sgb), 0, 0, 160, 96) == region(initial, 0, 0, 160, 96)
    assert game.get_bytes("wBattleMonHP", 2) == stats
    assert game.get_bytes("wBattleMonPP", 4) == pp
    assert game.get_bytes("wNumBagItems", 4) == bag([(0xCA, 1)])
    press(game, UP)  # The command cursor returned to ITEM.
    press(game, A)
    shows(game, "SPLASH", "START INFO")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--sgb-boot", type=Path, required=True)
    parser.add_argument("--gallery", type=Path, help="Write the four DMG shop views as a PNG.")
    args = parser.parse_args()
    rom = args.directory / "pokegreen.gbc"
    with Game(args.sameboy, args.boot, rom) as game:
        shop(game, gallery=args.gallery)
    with Game(args.sameboy, args.sgb_boot, rom, model=SGB_MODEL) as game:
        shop(game, sgb=True)
    with Game(args.sameboy, args.boot, rom) as game:
        field_bag(game)
    with Game(args.sameboy, args.boot, rom) as game:
        battle_bag(game)
    with Game(args.sameboy, args.sgb_boot, rom, model=SGB_MODEL) as game:
        battle_bag(game, sgb=True)
    print(f"{args.directory.name} Green: DMG and SGB shop previews and battle Bag return passed.")


if __name__ == "__main__":
    main()
