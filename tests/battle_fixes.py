"""Check Blaine's Super Potion and Substitute's HP boundary."""

import argparse
from pathlib import Path

from acid_armor import invoke_visual
from cartridge_smoke import Game
from protected_mechanics import ENEMY, PLAYER, SWIFT, put_stat, seed_actions, stat

SUBSTITUTE = 0xa4
HAS_SUBSTITUTE = 1 << 4
SUPER_POTION = 0x13


def check_blaine(game, core):
    for starting_hp, roll, uses_item in (
        (256, 0, not core),
        (255, 0, True),
        (151, 0, True),
        (151, 255, False),
    ):
        seed_actions(game, ENEMY, SWIFT)
        put_stat(game, ENEMY, "MaxHP", 256)
        put_stat(game, ENEMY, "HP", starting_hp)
        game.put("wTrainerName", (0x81, 0x8b, 0x80, 0x88, 0x8d, 0x84, 0x50))
        game.put("wAIItem", (0,))
        game.put("wAICount", (2,))
        game.put("hWhoseTurn", (1,))
        game.invoke("BlaineAI")
        game.cpu.af = roll << 8
        game.wait(lambda: game.cpu.pc == 0xc900, accept=True)
        assert game.get("wAICount") == 2 - uses_item, (starting_hp, roll)
        assert game.get("wAIItem") == (SUPER_POTION if uses_item else 0)
        expected_hp = min(256, starting_hp + 50) if uses_item else starting_hp
        assert stat(game, ENEMY, "HP") == expected_hp


def check_substitute(game, core):
    for actor in (PLAYER, ENEMY):
        for starting_hp, had_doll in ((39, False), (40, False), (41, False), (80, True)):
            seed_actions(game, actor, SUBSTITUTE)
            put_stat(game, actor, "HP", starting_hp)
            game.put("hWhoseTurn", (actor == ENEMY,))
            game.put(f"w{actor}BattleStatus2", (HAS_SUBSTITUTE if had_doll else 0,))
            stop = invoke_visual(game, "SubstituteEffect_")
            game.wait(lambda: game.cpu.pc == stop, accept=True)
            creates_doll = not had_doll and starting_hp >= 40 + core
            expected_hp = starting_hp - 40 if creates_doll else starting_hp
            assert stat(game, actor, "HP") == expected_hp, (actor, starting_hp)
            assert bool(game.get(f"w{actor}BattleStatus2") & HAS_SUBSTITUTE) == (
                had_doll or creates_doll
            )
            if creates_doll:
                assert game.get(f"w{actor}SubstituteHP") == 40


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    core = args.directory.name == "core"
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        for check in (check_blaine, check_substitute):
            with Game(args.sameboy, args.boot, rom) as game:
                game.new_game()
                check(game, core)
        print(f"{args.directory.name} {color}: Blaine and Substitute passed", flush=True)


if __name__ == "__main__":
    main()
