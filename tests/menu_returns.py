"""Check cancellation and list positions through the party and PC menus."""

import argparse
from pathlib import Path

from cartridge_smoke import Game
from pc_browsing import (
    A, B, DOWN, UP, box_name, list_view, name_bytes, open_bill, rosters, scroll_list,
    shows, stock_pc, wait_list,
)


START = 7
ITEM_ENTRIES = [(item, 2 if item == 0x12 else 1) for item in range(0x0B, 0x14)]
HYPER_POTION = 0x12
SUPER_POTION = 0x13


def move_down(game, row):
    game.press(DOWN)
    game.wait(lambda: game.get("wLastMenuItem") == row)
    game.tick(14)


def release_prompt(game, nickname):
    game.tick(35)
    game.press(A)
    shows(game, f"Release {nickname}", "Species STARYU", "YES", "NO")
    assert game.get("wCurrentMenuItem") == 1


def check_release(game):
    stock_pc(game)
    before = rosters(game)
    game.invoke("SaveGameData")
    game.return_to_stub()
    saved = bytes(game.battery()[8192:])

    open_bill(game)
    move_down(game, 1)
    move_down(game, 2)
    game.press(A)
    wait_list(game, (0, 0), box_name(0))
    nickname = box_name(7)
    view = scroll_list(game, 7, nickname)
    assert view == (5, 2)

    # Pressing A without moving the cursor confirms No.
    release_prompt(game, nickname)
    game.press(A)
    wait_list(game, view, nickname)
    assert rosters(game) == before
    assert bytes(game.battery()[8192:]) == saved

    # Even with Yes highlighted, B cancels.
    release_prompt(game, nickname)
    game.press(UP)
    game.wait(lambda: game.get("wCurrentMenuItem") == 0)
    game.press(B)
    wait_list(game, view, nickname)
    assert rosters(game) == before
    assert bytes(game.battery()[8192:]) == saved

    # Explicitly selecting Yes removes exactly this record from the live box.
    release_prompt(game, nickname)
    game.press(UP)
    game.wait(lambda: game.get("wCurrentMenuItem") == 0)
    game.press(A)
    shows(game, "released")
    assert game.get("wBoxCount") == 19
    assert rosters(game)[0] == before[0]
    assert bytes(game.battery()[8192:]) == saved
    remaining_names = [box_name(index) for index in range(20) if index != 7]
    for index, name in enumerate(remaining_names, 1):
        assert game.get_bytes(f"wBoxMon{index}Nick", 11) == name_bytes(name)

    game.invoke("TryLoadSaveFile")
    game.return_to_stub()
    assert game.get("wSaveFileStatus") == 2
    assert rosters(game) == before


def check_party_cancel(game):
    stock_pc(game)
    before = rosters(game)
    game.press(START)
    shows(game, "ITEM", "OPTION")
    game.press(A)
    shows(game, "PARTYA", "PARTYF")
    for row in range(1, 4):
        move_down(game, row)

    for button in (A, B):
        game.press(A)
        shows(game, "STATS", "SWITCH", "CANCEL")
        assert game.get("wWhichPokemon") == 3
        if button == A:
            move_down(game, 1)
            move_down(game, 2)
        game.press(button)
        shows(game, "PARTYF")
        game.wait(lambda: game.get("wTopMenuItemY") == 1)
        assert game.get("wCurrentMenuItem") == 3
        assert "STATS" not in game.visible_text()

    game.press(B)
    shows(game, "ITEM", "OPTION")
    assert rosters(game) == before


def inventory_bytes(entries):
    return bytes((len(entries), *(value for slot in entries for value in slot), 0xFF))


def assert_inventory(game, label, entries):
    expected = inventory_bytes(entries)
    assert game.get_bytes(label, len(expected)) == expected


def open_item_pc(game, *, deposit):
    game.enter_map(0x29, 7, 13, 4)
    game.put("wSpritePlayerStateData1FacingDirection", (4,))
    game.press(A)
    shows(game, "SOMEONE", "LOG OFF", accept=True)
    move_down(game, 1)
    game.press(A)
    shows(game, "WITHDRAW ITEM", "DEPOSIT ITEM", "to do", accept=True)
    if deposit:
        move_down(game, 1)
    game.press(A)
    shows(game, "ANTIDOTE", "BURN HEAL", accept=True)
    wait_list(game, (0, 0), "ANTIDOTE")


def choose_quantity(game):
    game.tick(35)
    game.press(A)
    shows(game, "How many")
    game.wait(lambda: game.get("wItemQuantity") == 1)
    game.tick(18)


def check_item_cursor(game, *, deposit):
    stock_pc(game)
    source = "wNumBagItems" if deposit else "wNumBoxItems"
    destination = "wNumBoxItems" if deposit else "wNumBagItems"
    receipt = "stored via PC" if deposit else "Withdrew"
    game.put(source, inventory_bytes(ITEM_ENTRIES))
    game.put(destination, inventory_bytes([]))

    open_item_pc(game, deposit=deposit)
    view = scroll_list(game, 7, "HYPER POTION")
    assert view == (5, 2)

    choose_quantity(game)
    game.press(B)
    wait_list(game, view, "HYPER POTION")
    assert_inventory(game, source, ITEM_ENTRIES)
    assert_inventory(game, destination, [])

    choose_quantity(game)
    game.press(A)
    shows(game, receipt)
    game.press(A)
    wait_list(game, view, "HYPER POTION")
    assert_inventory(game, source, ITEM_ENTRIES[:7] + [(HYPER_POTION, 1)] + ITEM_ENTRIES[8:])
    assert_inventory(game, destination, [(HYPER_POTION, 1)])

    # Remove the last visible row. Its successor is selected in the same view.
    choose_quantity(game)
    game.press(A)
    shows(game, receipt)
    game.press(A)
    wait_list(game, view, "SUPER POTION")
    assert_inventory(game, source, ITEM_ENTRIES[:7] + ITEM_ENTRIES[8:])
    assert_inventory(game, destination, [(HYPER_POTION, 2)])

    # That successor is now the final entry. Removing it selects its predecessor.
    choose_quantity(game)
    game.press(A)
    shows(game, receipt)
    game.press(A)
    wait_list(game, (5, 1), "MAX POTION")
    assert list_view(game) == (5, 1)
    assert_inventory(game, source, ITEM_ENTRIES[:7])
    assert_inventory(game, destination, [(HYPER_POTION, 2), (SUPER_POTION, 1)])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        for check in (check_release, check_party_cancel):
            with Game(args.sameboy, args.boot, rom) as game:
                game.new_game()
                check(game)
        for deposit in (True, False):
            with Game(args.sameboy, args.boot, rom) as game:
                game.new_game()
                check_item_cursor(game, deposit=deposit)
        print(f"{rom}: named Release, party CANCEL, and item PC cursor returns passed", flush=True)


if __name__ == "__main__":
    main()
