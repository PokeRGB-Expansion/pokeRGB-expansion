"""Check EXP. ALL shares after a knockout in the linked battle code."""

import argparse
from pathlib import Path

from cartridge_smoke import Game, seed_party
from pc_browsing import name_bytes


EXP_ALL = 0x4B
PIDGEY = 0x24
ENEMY_STATS = (121, 119, 101, 77, 55)
ENEMY_EXP = 141
ENEMY_LEVEL = 23
START_EXP = 117360  # Pidgey at level 50.
START_STAT_EXP = (64, 192, 255, 256, 350)
PARTY_COUNT = 4
FAINTED_MEMBER = 3


def seed_award(game, participants, carrying):
    seed_party(game)
    game.put("wPartyCount", (PARTY_COUNT,))
    game.put("wPartySpecies", (PIDGEY,) * PARTY_COUNT + (0xFF,))
    stat_exp = b"".join(value.to_bytes(2, "big") for value in START_STAT_EXP)
    for index in range(1, PARTY_COUNT + 1):
        mon = f"wPartyMon{index}"
        hp = 0 if index - 1 == FAINTED_MEMBER else 100
        game.put(mon + "Species", (PIDGEY,))
        game.put(mon + "Level", (50,))
        game.put(mon + "BoxLevel", (50,))
        game.put(mon + "HP", (0, hp))
        game.put(mon + "MaxHP", (0, 100))
        game.put(mon + "Nick", name_bytes("BIRD" + chr(64 + index)))
        game.put(mon + "OTID", game.get_bytes("wPlayerID", 2))
        game.put(mon + "Exp", START_EXP.to_bytes(3, "big"))
        game.put(mon + "HPExp", stat_exp)

    game.put("wEnemyMonBaseStats", (*ENEMY_STATS, 45, ENEMY_EXP))
    game.put("wEnemyMonLevel", (ENEMY_LEVEL,))
    game.put("wEnemyMonHP", (0, 0))
    game.put("wEnemyMonNick", name_bytes("FOE"))
    game.put("wBattleMonHP", (0, 100))
    game.put("wPlayerMonNumber", (0,))
    game.put("wIsInBattle", (1,))  # Wild battle.
    game.put("wPartyGainExpFlags", ((1 << participants) - 1,))
    game.put("wPartyFoughtCurrentEnemyFlags", ((1 << participants) - 1,))
    game.put("wOptions", (0xC1,))
    bag = (1, EXP_ALL, 1, 0xFF) if carrying else (0, 0xFF)
    game.put("wNumBagItems", bag)
    return bytes(bag)


def expected_shares(participants, carrying, minimal):
    amounts = (*ENEMY_STATS, ENEMY_EXP)
    if carrying:
        amounts = tuple(value // 2 for value in amounts)

    first = tuple(value // participants for value in amounts)
    if carrying:
        party_source = first if minimal else amounts
        second = tuple(value // PARTY_COUNT for value in party_source)
    else:
        second = (0,) * len(amounts)

    def experience(base):
        return base * ENEMY_LEVEL // 7

    for member in range(PARTY_COUNT):
        if member == FAINTED_MEMBER:
            yield 0, (0,) * len(ENEMY_STATS)
            continue
        active = first if member < participants else (0,) * len(amounts)
        yield (experience(active[-1]) + experience(second[-1]),
               tuple(a + b for a, b in zip(active[:-1], second[:-1])))


def check(library, boot, rom, *, participants, carrying, minimal):
    with Game(library, boot, rom) as game:
        game.new_game()
        bag = seed_award(game, participants, carrying)
        game.invoke("FaintEnemyPokemon")
        game.wait(lambda: game.cpu.pc == 0xC900, accept=True)
        assert game.get("wBattleResult") == 0
        assert game.get_bytes("wNumBagItems", len(bag)) == bag

        for index, (xp, stats) in enumerate(expected_shares(participants, carrying, minimal), 1):
            label = f"wPartyMon{index}"
            total = int.from_bytes(game.get_bytes(label + "Exp", 3), "big")
            assert total == START_EXP + xp, (rom, participants, carrying, index, total, xp)
            stat_values = game.get_bytes(label + "HPExp", 10)
            actual_stats = tuple(int.from_bytes(stat_values[start:start + 2], "big") - start_stat
                                 for start, start_stat in zip(range(0, 10, 2), START_STAT_EXP))
            assert actual_stats == stats, (rom, participants, carrying, index, actual_stats, stats)
            assert game.get(label + "Level") == 50


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--minimal", action="store_true")
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        for participants, carrying in ((1, False), (2, False), (1, True), (2, True)):
            check(args.sameboy, args.boot, rom, participants=participants, carrying=carrying,
                  minimal=args.minimal)
        print(f"{rom}: EXP. ALL XP and all five stat XP awards passed", flush=True)


if __name__ == "__main__":
    main()
