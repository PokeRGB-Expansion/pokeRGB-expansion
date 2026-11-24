"""Build all four HUD configurations and play the same wild encounter in each."""

import argparse
from itertools import product
from pathlib import Path
import subprocess

from adventure_checkpoints import advance_text_until, set_event
from battle_stats_return import battle_ready
from cartridge_smoke import Game, seed_party
from pc_browsing import name_bytes


ROOT = Path(__file__).resolve().parents[1]
PIDGEY, MASTER_BALL = 0x24, 1
A, DOWN = 4, 3
MARK = 1 * 20 + 1
METER = 11 * 20 + 10


def play(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        game.put("wOptions", (0xc1,))
        game.put("wPlayerID", (0x12, 0x34))
        game.put("wNumBagItems", (1, MASTER_BALL, 1, 0xff))
        set_event(game, 0x25)  # EVENT_GOT_POKEDEX
        game.put("wPokedexOwned", (0, 0x80))  # #016 Pidgey
        game.put("wPokedexSeen", (0, 0x80))
        game.put("wPartyMon1Nick", name_bytes("VAPOREON"))
        exp = (45**3 + (46**3 - 45**3) * 3 // 8).to_bytes(3, "big")
        game.put("wPartyMon1Exp", exp)
        game.enter_map(12, 10, 5, 4)  # Route 1
        game.put("wCurOpponent", (PIDGEY,))
        game.put("wCurEnemyLevel", (5,))
        advance_text_until(game, lambda: battle_ready(game))
        tiles = game.get_bytes("wTileMap", 20 * 18)

        game.put("wEnemyMonDVs", (0x77, 0x88))
        game.press(DOWN)
        game.press(A)
        game.wait(lambda: "MASTER BALL" in game.visible_text())
        game.press(A)
        for _ in range(250):
            if game.get("wIsInBattle") == 0:
                break
            if "YES" in game.visible_text() and "NO" in game.visible_text():
                game.press(DOWN)
            game.press(A)
            game.tick(5)
        assert game.get("wIsInBattle") == 0
        assert game.get("wPartyCount") == 3 and game.get("wNumBagItems") == 0
        assert game.get("wPartyMon3Species") == PIDGEY and game.get("wPartyMon3Level") == 5
        assert game.get_bytes("wPartyMon1Exp", 3) == exp
        return tiles


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("preset", choices=("core", "minimal"))
    parser.add_argument("--rgbds", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    screens = {}
    for caught, exp in product((0, 1), repeat=2):
        command = ["make", "-j4", "red", f"PRESET={args.preset}",
                   f"BATTLE_CAUGHT_MARKER={caught}", f"BATTLE_EXP_BAR={exp}"]
        if args.rgbds:
            command.append(f"RGBDS={args.rgbds.resolve()}/")
        subprocess.run(command, cwd=ROOT, check=True)
        directory = ROOT / "build"
        if (caught, exp) != (1, 1):
            directory /= f"hud-{caught}-{exp}"
        screens[caught, exp] = play(args.sameboy, args.boot, directory / args.preset / "pokered.gbc")

    original = screens[0, 0]
    assert original[MARK] == 0x7f and original[METER:METER + 8] == bytes([0x76] * 8)
    assert screens[1, 0][MARK] != original[MARK]
    assert screens[0, 1][METER:METER + 8] != original[METER:METER + 8]
    for (caught, exp), screen in screens.items():
        expected = bytearray(original)
        if caught:
            expected[MARK] = screens[1, 0][MARK]
        if exp:
            expected[METER:METER + 8] = screens[0, 1][METER:METER + 8]
        assert screen == expected, (caught, exp)
    print(f"{args.preset}: all four HUD settings passed a wild encounter and capture.")


if __name__ == "__main__":
    main()
