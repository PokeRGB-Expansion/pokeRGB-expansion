"""Verify near-full HP displays and each preset's level-one creation rules."""

import argparse
from pathlib import Path

from adventure_checkpoints import advance_text_until
from battle_stats_return import battle_ready, start_battle
from cartridge_smoke import Game, seed_party
from exp_all import AwardCase, seed_award
from status_medicine import put_number


RIGHT, DOWN, A, B = 0, 3, 4, 5
PIDGEY, MASTER_BALL, SEISMIC_TOSS, SPLASH = 0x24, 1, 0x45, 0x96
ROUTE_1 = 0x0c
NEAR_FULL = bytes((0x6b,)) * 5 + bytes((0x6a,))
WRAPPED_LEVEL_ONE = 0xffffca


def check_hp(game):
    start_battle(game, tower=False, scoped=False)
    # Seismic Toss at level 1 removes exactly one HP. Put a 259-HP
    # opponent in this encounter and give it only Splash.
    game.put("wBattleMonLevel", (1,))
    game.put("wBattleMonMoves", (SEISMIC_TOSS, 0, 0, 0))
    game.put("wBattleMonPP", (20, 0, 0, 0))
    game.put("wEnemyMonMoves", (SPLASH, 0, 0, 0))
    game.put("wEnemyMonPP", (40, 0, 0, 0))
    put_number(game, "wEnemyMonHP", 259)
    put_number(game, "wEnemyMonMaxHP", 259)
    for mon in ("wBattleMon", "wPartyMon1"):
        put_number(game, mon + "HP", 258)
        put_number(game, mon + "MaxHP", 259)
    # The missed-hit roll remains legal. Repeat the turn if it occurs.
    for _ in range(4):
        game.tick(15)
        game.press(A)
        game.wait(lambda: "SEISMIC TOSS" in game.visible_text())
        game.tick(12)
        game.press(A)
        advance_text_until(game, lambda: battle_ready(game))
        if game.get_bytes("wEnemyMonHP", 2) == (258).to_bytes(2, "big"):
            break
    assert game.get_bytes("wEnemyMonHP", 2) == (258).to_bytes(2, "big")
    tiles = game.get_bytes("wTileMap", 360)
    assert tiles[44:50] == NEAR_FULL, tiles[44:50]
    assert tiles[192:198] == NEAR_FULL, tiles[192:198]

    game.tick(15)
    game.press(RIGHT)
    game.wait(lambda: game.get("wTopMenuItemX") == 15)
    game.tick(12)
    game.press(A)
    game.wait(lambda: "258 259" in game.visible_text() and "160 160" in game.visible_text()
              and game.get("wMaxMenuItem") == 1)
    assert NEAR_FULL in game.get_bytes("wTileMap", 360)
    game.tick(14)
    game.press(A)
    game.wait(lambda: "SWITCH" in game.visible_text())
    game.tick(12)
    game.press(DOWN)
    game.press(A)
    game.wait(lambda: "ATTACK" in game.visible_text())
    assert NEAR_FULL in game.get_bytes("wTileMap", 360)
    for hp, maximum, expected in ((1, 259, 1), (144, 257, 27), (256, 259, 47), (259, 259, 48)):
        game.invoke("GetHPBarLength")
        game.cpu.bc = hp
        game.cpu.de = maximum
        game.return_to_stub()
        assert game.cpu.de & 0xff == expected


def create_mon(game, *, boxed, gift, level):
    game.new_game()
    seed_party(game)
    game.put("wOptions", (0xc1,))
    if boxed:
        game.put("wPartyCount", (6,))
        game.put("wPartySpecies", (0x69, 0x1b, 0x69, 0x69, 0x69, 0x69, 0xff))
    if gift:
        game.invoke("GivePokemon")
        game.cpu.bc = PIDGEY * 256 + level
        done = lambda: game.cpu.pc == 0xc900
    else:
        game.put("wPokedexOwned", (0, 0x80))
        game.put("wNumBagItems", (1, MASTER_BALL, 1, 0xff))
        game.enter_map(ROUTE_1, 10, 5, 4)
        game.put("wCurOpponent", (PIDGEY,))
        game.put("wCurEnemyLevel", (level,))
        advance_text_until(game, lambda: battle_ready(game))
        game.press(DOWN)
        game.press(A)
        game.wait(lambda: "MASTER BALL" in game.visible_text())
        game.press(A)
        done = lambda: game.get("wIsInBattle") == 0
    for _ in range(300):
        if done():
            break
        text = game.visible_text()
        if "YES" in text and "NO" in text:
            game.press(DOWN)
        game.press(A)
        game.tick(5)
    assert done(), game.visible_text()
    mon = "wBoxMon1" if boxed else "wPartyMon3"
    assert game.get(mon + "Species") == PIDGEY
    assert game.get(mon + ("BoxLevel" if boxed else "Level")) == level, (mon, level)
    return int.from_bytes(game.get_bytes(mon + "Exp", 3), "big")


def check_first_award(game, initial, *, core):
    game.new_game()
    seed_award(game, AwardCase(1, False, party_count=1, fainted=None))
    game.put("wPartyMon1Exp", initial.to_bytes(3, "big"))
    game.put("wPartyMon1Level", (1,))
    game.put("wPartyMon1BoxLevel", (1,))
    game.put("wEnemyMonLevel", (1,))
    game.put("wEnemyMonBaseExp", (55,))
    game.invoke("FaintEnemyPokemon")
    advance_text_until(game, lambda: game.cpu.pc == 0xc900)
    assert game.get("wPartyMon1Level") == (1 if core else 100)
    xp = int.from_bytes(game.get_bytes("wPartyMon1Exp", 3), "big")
    assert xp == (7 if core else 1059860), xp


def check_growth_curves(game, core):
    # The two unused curves are available to authors as well.
    for curve, first, second in (
        (0, 1, 8), (1, -20, 16), (2, -50, 16),
        (3, -54, 9), (4, 0, 6), (5, 1, 10),
    ):
        for level, expected in ((1, first), (2, second)):
            game.put("wMonHGrowthRate", (curve,))
            game.invoke("CalcInitialExperience" if core else "CalcExperience")
            game.cpu.de = level << 8
            game.return_to_stub()
            stored = int.from_bytes(game.get_bytes("hExperience", 3), "big")
            assert stored == (max(0, expected) if core else expected % (1 << 24))
    # A valid high bit at an authored level above 100 remains intact.
    game.put("wMonHGrowthRate", (5,))
    game.invoke("CalcInitialExperience" if core else "CalcExperience")
    game.cpu.de = 200 << 8
    game.return_to_stub()
    assert int.from_bytes(game.get_bytes("hExperience", 3), "big") == 10_000_000


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    core = args.directory.name == "core"
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        fixture = args.sameboy, args.boot, rom
        with Game(*fixture) as game:
            check_hp(game)
        for boxed in (False, True):
            for gift in (False, True):
                with Game(*fixture) as game:
                    initial = create_mon(game, boxed=boxed, gift=gift, level=1)
                    assert initial == (0 if core else WRAPPED_LEVEL_ONE), (boxed, gift, initial)
        with Game(*fixture) as game:
            check_first_award(game, initial, core=core)
        with Game(*fixture) as game:
            assert create_mon(game, boxed=False, gift=True, level=2) == 9
            check_growth_curves(game, core)
        print(f"{args.directory.name} {color}: HP display, level-one captures, gifts and awards passed", flush=True)


if __name__ == "__main__":
    main()
