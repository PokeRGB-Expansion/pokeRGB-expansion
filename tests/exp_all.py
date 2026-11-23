"""Check EXP. ALL shares after a knockout in the linked battle code."""

import argparse
from dataclasses import dataclass
from pathlib import Path

from adventure_checkpoints import advance_text_until
from cartridge_smoke import Game, seed_party
from pc_browsing import name_bytes


EXP_ALL = 0x4B
PIDGEY = 0x24
ENEMY_STATS = (121, 119, 101, 77, 55)
ENEMY_EXP = 141
ENEMY_LEVEL = 23
START_EXP = 117360  # Pidgey at level 50.
MAX_EXP = 1059860  # Pidgey at level 100.
START_STAT_EXP = (64, 192, 255, 256, 350)


@dataclass(frozen=True)
class AwardCase:
    participants: int
    carrying: bool
    party_count: int = 4
    fainted: int | None = 3
    trainer: bool = False
    traded: int | None = None
    capped: int | None = None


CASES = (
    *(AwardCase(participants, carrying) for participants in (1, 2) for carrying in (False, True)),
    *(AwardCase(count, True, party_count=count, fainted=None) for count in range(1, 7)),
    AwardCase(3, True, fainted=None, trainer=True, traded=0, capped=1),
)


def seed_award(game, case):
    seed_party(game)
    game.put("wPartyCount", (case.party_count,))
    game.put("wPartySpecies", (PIDGEY,) * case.party_count + (0xFF,))
    stat_exp = b"".join(value.to_bytes(2, "big") for value in START_STAT_EXP)
    for index in range(case.party_count):
        mon = f"wPartyMon{index + 1}"
        hp = 0 if index == case.fainted else 100
        level = 100 if index == case.capped else 50
        xp = MAX_EXP if index == case.capped else START_EXP
        owner = game.get_bytes("wPlayerID", 2)
        if index == case.traded:
            owner = bytes((owner[0], owner[1] ^ 1))
        game.put(mon + "Species", (PIDGEY,))
        game.put(mon + "Level", (level,))
        game.put(mon + "BoxLevel", (level,))
        game.put(mon + "HP", (0, hp))
        game.put(mon + "MaxHP", (0, 100))
        game.put(mon + "Nick", name_bytes("BIRD" + chr(65 + index)))
        game.put(mon + "OTID", owner)
        game.put(mon + "Exp", xp.to_bytes(3, "big"))
        game.put(mon + "HPExp", stat_exp)

    game.put("wEnemyMonBaseStats", (*ENEMY_STATS, 45, ENEMY_EXP))
    game.put("wEnemyMonLevel", (ENEMY_LEVEL,))
    game.put("wEnemyMonHP", (0, 0))
    game.put("wEnemyMonNick", name_bytes("FOE"))
    game.put("wBattleMonHP", (0, 100))
    game.put("wPlayerMonNumber", (0,))
    game.put("wIsInBattle", (2 if case.trainer else 1,))
    game.put("wPartyGainExpFlags", ((1 << case.participants) - 1,))
    game.put("wPartyFoughtCurrentEnemyFlags", ((1 << case.participants) - 1,))
    game.put("wOptions", (0xC1,))
    bag = (1, EXP_ALL, 1, 0xFF) if case.carrying else (0, 0xFF)
    game.put("wNumBagItems", bag)
    return bytes(bag)


def expected_shares(case, minimal):
    amounts = (*ENEMY_STATS, ENEMY_EXP)
    if case.carrying:
        amounts = tuple(value // 2 for value in amounts)

    first = tuple(value // case.participants for value in amounts)
    if case.carrying:
        party_source = first if minimal else amounts
        second = tuple(value // case.party_count for value in party_source)
    else:
        second = (0,) * len(amounts)

    def experience(base, member):
        xp = base * ENEMY_LEVEL // 7
        if member == case.traded:
            xp += xp // 2
        if case.trainer:
            xp += xp // 2
        return xp

    for member in range(case.party_count):
        if member == case.fainted:
            yield 0, (0,) * len(ENEMY_STATS)
            continue
        active = first if member < case.participants else (0,) * len(amounts)
        xp = experience(active[-1], member) + experience(second[-1], member)
        yield (xp,
               tuple(a + b for a, b in zip(active[:-1], second[:-1])))


def check(library, boot, rom, case, *, minimal):
    with Game(library, boot, rom) as game:
        game.new_game()
        bag = seed_award(game, case)
        game.invoke("FaintEnemyPokemon")
        advance_text_until(game, lambda: game.cpu.pc == 0xC900)
        assert game.get("wBattleResult") == 0
        assert game.get_bytes("wNumBagItems", len(bag)) == bag

        for index, (xp, stats) in enumerate(expected_shares(case, minimal)):
            label = f"wPartyMon{index + 1}"
            at_cap = index == case.capped
            expected_xp = MAX_EXP if at_cap else START_EXP + xp
            total = int.from_bytes(game.get_bytes(label + "Exp", 3), "big")
            assert total == expected_xp, (rom, case, index, total, expected_xp)
            stat_values = game.get_bytes(label + "HPExp", 10)
            actual_stats = tuple(int.from_bytes(stat_values[start:start + 2], "big") - start_stat
                                 for start, start_stat in zip(range(0, 10, 2), START_STAT_EXP))
            assert actual_stats == stats, (rom, case, index, actual_stats, stats)
            assert game.get(label + "Level") == (100 if at_cap else 50)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--minimal", action="store_true")
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        for case in CASES:
            check(args.sameboy, args.boot, rom, case, minimal=args.minimal)
        print(f"{rom}: EXP. ALL XP and all five stat XP awards passed", flush=True)


if __name__ == "__main__":
    main()
