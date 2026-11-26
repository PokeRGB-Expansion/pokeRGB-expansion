"""Preview box contents from a Pokémon Center without changing the active box or saving."""

import argparse
import ctypes as C
from contextlib import contextmanager
from pathlib import Path

from cartridge_smoke import Game, seed_party
from hp_and_level_one import create_mon
from pc_browsing import A, B, DOWN, UP, name_bytes, open_bill, rosters, shows


RIGHT, LEFT, START = 0, 1, 7
SPECIES = ((0x24, "PIDGEY"), (0x01, "RHYDON"), (0xB1, "SQUIRTLE"), (0xB0, "CHARMANDER"))


def select_box_menu(game):
    open_bill(game)
    for row in range(1, 4):
        game.press(DOWN)
        game.wait(lambda: game.get("wCurrentMenuItem") == row)
        game.tick(12)
    game.press(A)
    shows(game, "START  View box", "OCCUPIED")


def expect_picker(game, box):
    shows(game, "START  View box", "OCCUPIED")
    assert game.get("wCurrentMenuItem") == box - 1


def press_preview(game):
    game.press(START)
    shows(game, "B BACK")


def stored_name(box, slot):
    return "STORED" + chr(ord("A") + box - 1) + chr(ord("A") + slot)


def seed_saved_box(game, box, count):
    save = game.battery()
    base = game.box_position(box)
    nick_offset = game.addresses["wBoxMonNicks"][1] - game.addresses["wBoxCount"][1]
    save[base] = count
    for slot in range(count):
        save[base + 1 + slot] = SPECIES[slot % len(SPECIES)][0]
        start = base + nick_offset + slot * 11
        save[start:start + 11] = name_bytes(stored_name(box, slot))
    save[base + 1 + count] = 0xFF


@contextmanager
def detect_save_writes(game):
    """Catch even a write that stores the old value or is undone before B."""
    writes = []
    callback_type = C.CFUNCTYPE(C.c_bool, C.c_void_p, C.c_uint16, C.c_uint8)

    @callback_type
    def record(gb, address, value):
        if 0xA000 <= address < 0xC000:
            writes.append((address, value))
        return True

    callback = game.core.GB_set_write_memory_callback
    callback.argtypes = [C.c_void_p, callback_type]
    callback.restype = None
    callback(game.gb, record)
    try:
        yield
    finally:
        callback(game.gb, callback_type())
    assert not writes, writes[:4]


def check_boxes(game):
    game.new_game()
    seed_party(game)
    game.put("wOptions", (1,))
    # Box 1's live nickname differs from its stale SRAM copy.
    game.put("wCurrentBoxNum", (0x80,))
    game.put("wBoxCount", (1, 0x24, 0xFF))
    game.put("wBoxMon1Nick", name_bytes("ABCDEFGHIJ"))
    for box in range(1, 13):
        seed_saved_box(game, box, 20 if box == 12 else int(box != 6))
    select_box_menu(game)
    before = bytes(game.battery())
    team = rosters(game)
    for box in range(1, 13):
        if box > 1:
            game.press(DOWN)
            expect_picker(game, box)
        press_preview(game)
        if box == 6:
            shows(game, "This BOX is empty")
        elif box == 1:
            shows(game, "ABCDEFGHIJ", "PIDGEY")
            assert stored_name(box, 0) not in game.visible_text()
        else:
            shows(game, stored_name(box, 0), "PIDGEY")
        if box == 12:
            for page in range(5):
                for row, (_, species_name) in enumerate(SPECIES):
                    shows(game, stored_name(box, 4 * page + row), species_name)
                if page < 4:
                    game.press(RIGHT if page % 2 == 0 else DOWN)
            game.press(RIGHT)
            shows(game, stored_name(box, 19))
            for page in range(3, -1, -1):
                game.press(LEFT if page % 2 else UP)
                shows(game, stored_name(box, page * 4))
            game.press(UP)
            shows(game, stored_name(box, 0))
        game.press(B)
        expect_picker(game, box)
        assert game.get("wCurrentBoxNum") == 0x80
        assert rosters(game) == team and bytes(game.battery()) == before

    # Observe the RAM bus for the full preview and a declined save.
    with detect_save_writes(game):
        press_preview(game)
        game.press(B)
        expect_picker(game, 12)
        game.press(A)
        shows(game, "Save and change to", "BOX 12", "YES", "NO", accept=True)
        game.press(B)
        expect_picker(game, 12)
    assert bytes(game.battery()) == before and game.get("wCurrentBoxNum") == 0x80
    game.press(A)
    shows(game, "Save and change to", "YES", "NO", accept=True)
    game.press(A)
    shows(game, "WITHDRAW", "CHANGE BOX")
    assert game.get("wCurrentBoxNum") == 0x8B and game.get("wBoxCount") == 20
    assert game.get_bytes("wBoxMon20Nick", 11) == name_bytes(stored_name(12, 19))
    assert bytes(game.battery()) != before


def check_new_adventure(game):
    # Catch Pidgey through the battle Bag with a full party. The freshly boxed
    # Pokémon has not been saved or moved into an inactive box.
    create_mon(game, boxed=True, gift=False, level=5)
    assert not game.get("wCurrentBoxNum") & 0x80
    seed_saved_box(game, 2, 1)  # An inactive record from a different adventure.
    select_box_menu(game)
    before = bytes(game.battery())
    with detect_save_writes(game):
        press_preview(game)
        assert game.visible_text().count("PIDGEY") == 2  # nickname and species
        game.press(B)
        expect_picker(game, 1)
        game.press(DOWN)
        expect_picker(game, 2)
        press_preview(game)
        shows(game, "This BOX is empty")
        assert stored_name(2, 0) not in game.visible_text()
        game.press(B)
        expect_picker(game, 2)
        game.press(B)
        shows(game, "WITHDRAW", "CHANGE BOX")
    assert game.get("wCurrentBoxNum") == 0 and bytes(game.battery()) == before


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        for check in (check_boxes, check_new_adventure):
            with Game(args.sameboy, args.boot, args.directory / f"poke{color}.gbc") as game:
                check(game)
        print(f"{args.directory.name} {color}: read-only box browsing and confirmed box change passed",
              flush=True)


if __name__ == "__main__":
    main()
