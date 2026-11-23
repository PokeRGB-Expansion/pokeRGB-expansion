"""Check that the first-catch Pokédex entry exits the battle after dismissal."""

import argparse
from pathlib import Path

from adventure_checkpoints import advance_text_until
from cartridge_smoke import Game, seed_party


CLEFAIRY = 4
MASTER_BALL = 1
HAS_SUBSTITUTE = 1 << 4
ROUTE_1 = 0x0C
A, B, DOWN = 4, 5, 3


def check_capture(library, boot, rom, form):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        game.put("wOptions", (0xC1,))
        game.put("wNumBagItems", (1, MASTER_BALL, 1, 0xFF))
        game.enter_map(ROUTE_1, 10, 5, 4)
        game.put("wCurOpponent", (CLEFAIRY,))
        game.put("wCurEnemyLevel", (5,))
        advance_text_until(game, lambda: game.get("wIsInBattle") == 1 and "FIGHT" in game.visible_text())

        substitute = HAS_SUBSTITUTE if form == "substitute" else 0
        game.put("wEnemyBattleStatus2", (substitute,))
        game.put("wPlayerBattleStatus2", (substitute,))
        game.put("wEnemyMonMinimized", (form == "minimize",))
        game.press(DOWN)  # ITEM
        game.press(A)
        game.wait(lambda: "MASTER BALL" in game.visible_text())
        game.press(A)
        advance_text_until(game, lambda: "035" in game.visible_text() and "CLEFAIRY" in game.visible_text())
        game.press(B)

        for _ in range(250):
            if game.get("wIsInBattle") == 0:
                break
            text = game.visible_text()
            assert "FIGHT" not in text or "RUN" not in text
            if "YES" in text and "NO" in text:
                game.press(DOWN)
            game.press(A)
            game.tick(5)
        assert game.get("wIsInBattle") == 0
        assert game.get("wCurMap") == ROUTE_1
        assert game.get("wPartyCount") == 3
        assert game.get_bytes("wPartySpecies", 4) == bytes((0x69, 0x1B, CLEFAIRY, 0xFF))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        for form in ("ordinary", "substitute", "minimize"):
            check_capture(args.sameboy, args.boot, rom, form)
        print(f"{color.title()}: Pokédex first-catch return passed", flush=True)


if __name__ == "__main__":
    main()
