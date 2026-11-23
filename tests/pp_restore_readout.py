"""Check the PP readout on the move an item will affect."""

import argparse
import re
from pathlib import Path

from adventure_checkpoints import advance_text_until
from cartridge_smoke import Game, seed_party


DOWN, UP, A, B = 3, 2, 4, 5
ETHER, MAX_ETHER, PP_UP = 0x50, 0x51, 0x4F
BASE_MOVES = bytes((0x21, 0x39, 0x2D, 0x81))  # Tackle, Surf, Growl, Swift
BASE_PP = bytes((0, 64 + 7, 128 + 54, 192 + 19))
ROWS = ((0, 35), (7, 18), (54, 54), (19, 32))


def text_on_screen(game, *words):
    return all(word in game.visible_text() for word in words)


def readout(game):
    row = game.visible_text().splitlines()[15]
    match = re.search(r"PP\s*(\d+)\s+(\d+)", row)
    return tuple(int(value) for value in match.groups()) if match else None


def seed_items(game, item):
    game.put("wNumBagItems", (1, item, 1, 0xFF))
    game.put("wOptions", (0xC1,))
    for slot in (1, 2):
        game.put(f"wPartyMon{slot}Moves", BASE_MOVES)
        game.put(f"wPartyMon{slot}PP", BASE_PP)


def open_party_items(game, target):
    game.wait(lambda: text_on_screen(game, "160 160") and game.get("wMaxMenuItem") == 1)
    game.tick(12)
    if game.get("wCurrentMenuItem") != target:
        game.press(DOWN if target else UP)
    assert game.get("wCurrentMenuItem") == target
    game.press(A)
    game.wait(lambda: readout(game) == ROWS[0], accept=True)
    assert game.get("wWhichPokemon") == target
    game.tick(12)


def open_field_item(game, name, target):
    game.invoke("StartMenu_Item")
    game.wait(lambda: name in game.visible_text())
    game.tick(12)
    game.press(A)
    game.wait(lambda: text_on_screen(game, "USE", "TOSS"))
    game.tick(12)
    game.press(A)
    open_party_items(game, target)


def check_field_ether(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        seed_items(game, ETHER)
        open_field_item(game, "ETHER", 1)
        for row in ROWS[1:]:
            game.press(DOWN)
            game.wait(lambda: readout(game) == row)
            game.tick(12)
            assert game.get_bytes("wPartyMon2PP", 4) == BASE_PP

        game.press(B)
        game.wait(lambda: text_on_screen(game, "160 160") and readout(game) is None)
        game.tick(12)
        game.press(B)
        game.wait(lambda: "ETHER" in game.visible_text(), accept=True)
        assert game.get_bytes("wPartyMon1PP", 4) == BASE_PP
        assert game.get_bytes("wPartyMon2PP", 4) == BASE_PP
        assert game.get_bytes("wNumBagItems", 4) == bytes((1, ETHER, 1, 0xFF))


def check_pp_up(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        seed_items(game, PP_UP)
        open_field_item(game, "PP UP", 1)
        game.press(A)
        game.wait(lambda: game.get("wNumBagItems") == 0, accept=True)
        assert game.get_bytes("wPartyMon2PP", 4) == bytes((64 + 7, *BASE_PP[1:]))
        assert game.get_bytes("wPartyMon1PP", 4) == BASE_PP


def check_transformed_target(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        seed_items(game, MAX_ETHER)
        game.enter_map(0x0C, 10, 5, 4)
        game.put("wCurOpponent", (0x24,))  # Pidgey
        game.put("wCurEnemyLevel", (5,))
        advance_text_until(game, lambda: game.get("wIsInBattle") == 1 and "FIGHT" in game.visible_text())

        game.put("wPlayerBattleStatus3", (1 << 3,))  # Transform
        game.put("wBattleMonMoves", (0x96, 0, 0, 0))  # Splash, a copied move.
        game.put("wBattleMonPP", (5, 0, 0, 0))
        game.put("wPlayerSelectedMove", (0x21,))  # Remembered Tackle.
        game.put("wPlayerMovePower", (35, 0))  # Power and Normal type.
        game.put("wDamage", (0, 23))
        history = game.get("wPlayerSelectedMove"), game.get_bytes("wPlayerMovePower", 2), game.get_bytes("wDamage", 2)
        hp = game.get_bytes("wBattleMonHP", 2), game.get_bytes("wEnemyMonHP", 2)

        game.press(DOWN)
        game.press(A)
        game.wait(lambda: "MAX ETHER" in game.visible_text())
        game.tick(18)
        game.press(A)
        open_party_items(game, 0)
        assert "TACKLE" in game.visible_text()
        assert "SPLASH" not in game.visible_text()
        game.press(DOWN)
        game.wait(lambda: readout(game) == ROWS[1])
        game.tick(12)
        game.press(B)
        game.wait(lambda: text_on_screen(game, "160 160") and readout(game) is None)
        game.tick(12)
        game.press(B)
        game.wait(lambda: "MAX ETHER" in game.visible_text())
        game.tick(18)
        game.press(B)
        game.wait(lambda: text_on_screen(game, "FIGHT", "RUN"))

        assert game.get_bytes("wBattleMonPP", 4) == bytes((5, 0, 0, 0)), (
            game.get_bytes("wBattleMonPP", 4), game.get_bytes("wPartyMon1PP", 4),
            game.get_bytes("wNumBagItems", 4),
        )
        assert game.get_bytes("wPartyMon1PP", 4) == BASE_PP
        assert game.get_bytes("wNumBagItems", 4) == bytes((1, MAX_ETHER, 1, 0xFF))
        assert history == (
            game.get("wPlayerSelectedMove"), game.get_bytes("wPlayerMovePower", 2),
            game.get_bytes("wDamage", 2),
        )
        assert hp == (game.get_bytes("wBattleMonHP", 2), game.get_bytes("wEnemyMonHP", 2))

        # Counter reads the remembered move and doubles the previous damage.
        game.put("hWhoseTurn", (1,))
        game.put("wEnemySelectedMove", (0x44,))  # Counter
        game.put("wEnemyBattleStatus2", (1,))  # X Accuracy removes the accuracy roll.
        game.invoke("HandleCounterMove")
        game.return_to_stub()
        assert game.get_bytes("wDamage", 2) == bytes((0, 46))
        assert game.get("wMoveMissed") == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        for check in (check_field_ether, check_pp_up, check_transformed_target):
            check(args.sameboy, args.boot, rom)
        print(f"{color.title()}: party PP readouts passed", flush=True)


if __name__ == "__main__":
    main()
