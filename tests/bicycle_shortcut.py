"""Check Bicycle registration, field use, and its saved choice."""

import argparse
from pathlib import Path

from cartridge_smoke import Game

A, B, SELECT, DOWN, START = 4, 5, 6, 3, 7
BICYCLE = 6
REGISTER_TAG = 0xd6
BIKE_BAG = bytes((1, BICYCLE, 1, 0xff))


def choose_registration(game, action):
    game.press(START)
    game.wait(lambda: "ITEM" in game.visible_text() and "OPTION" in game.visible_text())
    game.tick(12)
    if game.get("wCurrentMenuItem") == 0:
        game.press(DOWN)
    game.press(A)
    game.wait(lambda: "BICYCLE" in game.visible_text() and "CANCEL" in game.visible_text())
    game.tick(12)
    game.press(A)
    game.wait(lambda: action in game.visible_text())
    game.tick(12)
    game.press(DOWN)
    game.press(A)
    game.wait(lambda: action not in game.visible_text() and "BICYCLE" in game.visible_text())
    game.tick(12)
    assert (game.visible_text().splitlines()[5].strip() == "SELECT") == (action == "REGISTER")
    game.press(B)
    game.wait(lambda: "OPTION" in game.visible_text())
    game.tick(12)
    game.press(B)
    game.tick(80)


def finish_bicycle_text(game, message):
    game.wait(lambda: message in game.visible_text() and "BICYCLE" in game.visible_text())
    game.tick(20)
    game.press(A)
    game.wait(lambda: message not in game.visible_text())
    game.tick(45)


def check_shortcut(game):
    assert game.get("wRegisteredItemTag") == 0
    assert game.get("wRegisteredItem") == 0
    game.put("wStatusFlags4", (game.get("wStatusFlags4") | 0x10,))
    game.enter_map(0x0c, 10, 5, 4)  # A clear square on Route 1.
    game.put("wNumBagItems", BIKE_BAG)
    choose_registration(game, "REGISTER")
    assert game.get("wRegisteredItemTag") == REGISTER_TAG
    assert game.get("wRegisteredItem") == BICYCLE
    assert game.get_bytes("wNumBagItems", 4) == BIKE_BAG

    # A normal text action can leave a different name in this scratch buffer.
    game.put("wStringBuffer", (0x93, 0x80, 0x82, 0x8a, 0x8b, 0x84, 0x50))  # TACKLE
    game.core.GB_set_key_state(game.gb, SELECT, True)
    game.wait(lambda: "got on the" in game.visible_text() and "BICYCLE" in game.visible_text())
    game.tick(60)
    assert game.get("wWalkBikeSurfState") == 1
    game.press(A)
    game.tick(80)
    assert game.get("wWalkBikeSurfState") == 1
    game.core.GB_set_key_state(game.gb, SELECT, False)
    game.wait(lambda: "got on the" not in game.visible_text())
    game.tick(45)
    game.press(SELECT)
    finish_bicycle_text(game, "got off")
    assert game.get("wWalkBikeSurfState") == 0

    game.put("wNumBagItems", (0, 0xff))
    game.press(SELECT)
    game.tick(75)
    assert game.get("wWalkBikeSurfState") == 0
    assert game.get("wRegisteredItem") == BICYCLE

    game.put("wNumBagItems", BIKE_BAG)
    game.put("wRegisteredItem", (0xe0,))
    game.press(SELECT)
    game.tick(75)
    assert game.get("wWalkBikeSurfState") == 0
    assert game.get_bytes("wNumBagItems", 4) == BIKE_BAG

    game.put("wRegisteredItem", (BICYCLE,))
    choose_registration(game, "CLEAR")
    assert game.get("wRegisteredItemTag") == 0
    assert game.get("wRegisteredItem") == 0
    game.press(SELECT)
    game.tick(75)
    assert game.get("wWalkBikeSurfState") == 0

    choose_registration(game, "REGISTER")
    game.invoke("SaveGameData")
    game.return_to_stub()
    game.put("wRegisteredItemTag", (0, 0))
    game.invoke("TryLoadSaveFile")
    game.return_to_stub()
    assert game.get("wSaveFileStatus") == 2
    assert game.get("wRegisteredItemTag") == REGISTER_TAG
    assert game.get("wRegisteredItem") == BICYCLE


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        with Game(args.sameboy, args.boot, rom) as game:
            game.new_game()
            check_shortcut(game)
        print(f"{args.directory.name} {color}: Bicycle registration and SELECT passed", flush=True)


if __name__ == "__main__":
    main()
