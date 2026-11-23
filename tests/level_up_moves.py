"""Check move learning after one battle XP award gains several levels."""

import argparse
from pathlib import Path

from cartridge_smoke import Game, seed_party
from pc_browsing import A, B, DOWN, name_bytes, shows


PIDGEY = 0x24
GUST, TOXIC, DOUBLE_TEAM, SWIFT = 0x10, 0x5C, 0x68, 0x81
SAND_ATTACK, QUICK_ATTACK = 0x1C, 0x62
FIRST_LEVEL, FINAL_LEVEL, ENEMY_LEVEL = 4, 12, 25
FIRST_EXP, FINAL_EXP = 96, 1006
START_PP = (35, 10, 15, 20)


def award_experience(game, *, full):
    seed_party(game)
    game.put("wPartyCount", (1,))
    game.put("wPartySpecies", (PIDGEY, 0xFF))
    game.put("wPartyMon1Species", (PIDGEY,))
    game.put("wPartyMon1Nick", name_bytes("BIRD"))
    game.put("wPartyMon1OTID", game.get_bytes("wPlayerID", 2))
    game.put("wPartyMon1Level", (FIRST_LEVEL,))
    game.put("wPartyMon1BoxLevel", (FIRST_LEVEL,))
    game.put("wPartyMon1Exp", FIRST_EXP.to_bytes(3, "big"))
    game.put("wPartyMon1HP", (0, 18))
    game.put("wPartyMon1MaxHP", (0, 18))
    game.put("wBattleMonHP", (0, 18))
    game.put("wBattleMonLevel", (FIRST_LEVEL,))
    game.put("wPartyMon1Type", (0, 2))
    moves = (GUST, TOXIC, DOUBLE_TEAM, SWIFT) if full else (GUST, TOXIC, 0, 0)
    pp = START_PP if full else (*START_PP[:2], 0, 0)
    for label in ("wPartyMon1", "wBattleMon"):
        game.put(label + "Moves", moves)
        game.put(label + "PP", pp)

    # A level 25 wild Chansey awards floor(255 * 25 / 7) = 910 XP.
    game.put("wEnemyMonBaseStats", (250, 5, 5, 50, 105, 30, 255))
    game.put("wEnemyMonLevel", (ENEMY_LEVEL,))
    game.put("wCurEnemyLevel", (ENEMY_LEVEL,))
    game.put("wIsInBattle", (1,))
    game.put("wPlayerMonNumber", (0,))
    game.put("wPartyGainExpFlags", (1,))
    game.put("wOptions", (0xC1,))
    game.invoke("GainExperience")


def assert_award(game, moves, pp):
    assert game.get("wPartyMon1Level") == FINAL_LEVEL
    assert game.get("wBattleMonLevel") == FINAL_LEVEL
    assert game.get_bytes("wPartyMon1Exp", 3) == FINAL_EXP.to_bytes(3, "big")
    assert game.get("wCurEnemyLevel") == ENEMY_LEVEL
    assert game.get("wCanEvolveFlags") & 1
    assert game.get_bytes("wPartyMon1HP", 2) == game.get_bytes("wBattleMonHP", 2)
    assert game.get_bytes("wPartyMon1MaxHP", 2) == game.get_bytes("wBattleMonMaxHP", 2)
    for label in ("wPartyMon1", "wBattleMon"):
        assert game.get_bytes(label + "Moves", 4) == bytes(moves)
        assert game.get_bytes(label + "PP", 4) == bytes(pp)


def expect_offer(game, name):
    game.wait(lambda: all(word in game.visible_text() for word in ("YES", "NO", "START INFO")),
              accept=True)
    assert name in game.visible_text(), game.visible_text()
    game.tick(16)


def check_replacement(game, *, minimal):
    award_experience(game, full=True)
    if not minimal:
        expect_offer(game, "SAND ATTACK")
        game.press(B)
        shows(game, "Abandon learning", "YES", "NO", accept=True)
        game.press(A)
        shows(game, "did not learn", "SAND ATTACK", accept=True)
        assert game.get_bytes("wPartyMon1Moves", 4) == bytes((GUST, TOXIC, DOUBLE_TEAM, SWIFT))
    expect_offer(game, "QUICK ATTACK")
    game.press(A)
    shows(game, "GUST", "TOXIC", "DOUBLE TEAM", "SWIFT", accept=True)
    for row in (1, 2):
        game.press(DOWN)
        game.wait(lambda: game.get("wCurrentMenuItem") == row)
        game.tick(14)
    game.press(A)
    shows(game, "learned", "QUICK ATTACK", accept=True)
    game.wait(lambda: game.cpu.pc == 0xC900, accept=True)
    assert_award(game, (GUST, TOXIC, QUICK_ATTACK, SWIFT), (35, 10, 30, 20))


def check_empty_slots(game, *, minimal):
    award_experience(game, full=False)
    game.wait(lambda: "learned" in game.visible_text() and "ATTACK" in game.visible_text(),
              accept=True)
    assert ("QUICK ATTACK" if minimal else "SAND ATTACK") in game.visible_text()
    if not minimal:
        shows(game, "learned", "QUICK ATTACK", accept=True)
    game.wait(lambda: game.cpu.pc == 0xC900, accept=True)
    if minimal:
        assert_award(game, (GUST, TOXIC, QUICK_ATTACK, 0), (35, 10, 30, 0))
    else:
        assert_award(game, (GUST, TOXIC, SAND_ATTACK, QUICK_ATTACK), (35, 10, 15, 30))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--minimal", action="store_true")
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        for check in (check_replacement, check_empty_slots):
            with Game(args.sameboy, args.boot, rom) as game:
                game.new_game()
                check(game, minimal=args.minimal)
        print(f"{rom}: level gains and move learning passed", flush=True)


if __name__ == "__main__":
    main()
