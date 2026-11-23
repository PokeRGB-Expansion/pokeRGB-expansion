"""Check the first visible NPC position during map entry events and menus."""

import argparse
from pathlib import Path

from adventure_checkpoints import advance_text_until, position
from cartridge_smoke import Game, seed_party


VIRIDIAN_CITY, VIRIDIAN_POKECENTER = 0x01, 0x29
ROUTE_16, ROUTE_16_GATE = 0x1B, 0xBA
A, B = 4, 5


def initialize_nurse(game, x):
    game.new_game()
    seed_party(game)
    game.put("wOptions", (1,))
    game.enter_map(VIRIDIAN_POKECENTER, 7, x, 4, last_map=VIRIDIAN_CITY)

    # Recreate the six sprite bytes LoadMapHeader leaves before the first update.
    game.put("wSprite01StateData1MovementStatus", (0, 0xFF, 0, 0, 0, 0))
    game.invoke("UpdateSprites")
    game.return_to_stub()
    assert game.get("wSprite01StateData1MovementStatus") == 1
    assert game.get("wSprite01StateData1ImageIndex") == 0xFF
    assert game.get_bytes("wSprite01StateData2YDisplacement", 2) == bytes((8, 8))


def check_nurse_position(game, x):
    # The nurse stands at (3, 1). The camera centers the player at (64, 60).
    assert game.get("wSprite01StateData1XPixels") == 64 + (3 - x) * 16
    assert game.get("wSprite01StateData1YPixels") == 60 + (1 - 4) * 16


def check_first_start_menu(library, boot, rom):
    with Game(library, boot, rom) as game:
        initialize_nurse(game, 5)
        check_nurse_position(game, 5)
        # Open START before an ordinary movement update can place the nurse.
        game.put("hTextID", (0,))
        game.invoke("DisplayTextID")
        game.wait(lambda: "SAVE" in game.visible_text() and "OPTION" in game.visible_text())
        assert game.get("wSprite01StateData1ImageIndex") != 0xFF
        check_nurse_position(game, 5)
        game.press(B)
        game.wait(lambda: "OPTION" not in game.visible_text())
        assert position(game) == (5, 4)
        check_nurse_position(game, 5)


def check_hidden_interaction(library, boot, rom):
    with Game(library, boot, rom) as game:
        initialize_nurse(game, 1)
        game.put("wSpritePlayerStateData1FacingDirection", (8,))  # Face the hidden bench event.
        game.invoke("OverworldLoop")
        game.press(A)
        game.wait(lambda: "heal your tired" in game.visible_text(), accept=True)
        check_nurse_position(game, 1)
        assert position(game) == (1, 4)


def check_forced_movement(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        game.put("wOptions", (1,))
        game.enter_map(ROUTE_16_GATE, 4, 4, 9, last_map=ROUTE_16)
        game.wait(lambda: "Excuse me" in game.visible_text(), accept=True)
        advance_text_until(
            game,
            lambda: position(game) == (5, 7)
            and game.get("wRoute16Gate1FCurScript") == 0
            and game.get("wSimulatedJoypadStatesIndex") == 0,
        )
        assert game.get("wJoyIgnore") == 0
        assert game.get("wSprite01StateData1XPixels") == 48
        assert game.get("wSprite01StateData1YPixels") == 28


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        for check in (check_first_start_menu, check_hidden_interaction, check_forced_movement):
            check(args.sameboy, args.boot, rom)
        print(f"{color.title()}: initial NPC positions passed", flush=True)


if __name__ == "__main__":
    main()
