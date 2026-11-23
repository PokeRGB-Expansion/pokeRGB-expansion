"""Run protected battle actions with controlled random bytes in built cartridges."""

import argparse
from pathlib import Path

from cartridge_smoke import Game, seed_party
from link_cable_smoke import (
    A, COLOSSEUM, DOWN, Cable, choose_room, in_battle_commands, setup_player, use_table_game_boys,
)


PLAYER, ENEMY = "Player", "Enemy"
NORMAL, FIGHTING, GHOST, PSYCHIC = 0x00, 0x01, 0x08, 0x18
HYPER_BEAM, SWIFT, SLEEP_POWDER = 0x3F, 0x81, 0x4F
WRAP, BIND, CLAMP, FIRE_SPIN, MIRROR_MOVE = 0x23, 0x14, 0x80, 0x53, 0x77
NIGHT_SHADE, SEISMIC_TOSS, SONICBOOM, LICK = 0x65, 0x45, 0x31, 0x7A
DRAGON_RAGE, SUPER_FANG, PSYWAVE = 0x52, 0xA2, 0x95
RECHARGE, TRAPPING, SUBSTITUTE, FROZEN = 1 << 5, 1 << 5, 1 << 4, 1 << 5
HP, PP = 160, 15


def mon_label(side):
    return "wBattleMon" if side == PLAYER else "wEnemyMon"


def other(side):
    return ENEMY if side == PLAYER else PLAYER


def stat(game, side, name):
    return int.from_bytes(game.get_bytes(mon_label(side) + name, 2), "big")


def put_stat(game, side, name, value):
    game.put(mon_label(side) + name, value.to_bytes(2, "big"))


def call(game, routine):
    game.invoke(routine)
    game.wait(lambda: game.cpu.pc == 0xC900, accept=True)


def draws(game):
    return game.get("wLinkBattleRandomNumberListIndex")


def random_bytes(game, *values):
    # The battle core consumes the normal link random list. Extra values let
    # accidental draws return so the test can report the count.
    game.put("wLinkBattleRandomNumberList", bytes(values).ljust(9, b"\xff"))
    game.put("wLinkBattleRandomNumberListIndex", (0,))


def seed_actions(game, actor, move, *, attacker_type=NORMAL, defender_type=NORMAL, target_hp=HP):
    seed_party(game)
    for side in (PLAYER, ENEMY):
        name = mon_label(side)
        attacking = side == actor
        species = 0x69 if side == PLAYER else 0x1B
        chosen = move if attacking else SWIFT
        kind = attacker_type if attacking else defender_type
        game.put(name + "Species", (species,))
        game.put(name + "Level", (50,))
        game.put(name + "Nick", (0x93, 0x84, 0x92, 0x93, 0x50))
        game.put(name + "Type", (kind, kind))
        game.put(name + "Moves", (chosen, 0, 0, 0))
        game.put(name + "PP", (PP, 0, 0, 0))
        game.put(name + "Status", (0,))
        put_stat(game, side, "HP", HP if attacking else target_hp)
        put_stat(game, side, "MaxHP", HP)
        for stat_name, value in (("Attack", 100), ("Defense", 100), ("Speed", 90), ("Special", 100)):
            put_stat(game, side, stat_name, value)
            game.put(f"w{side}MonUnmodified{stat_name}", value.to_bytes(2, "big"))
        game.put(f"w{side}MonStatMods", (7,) * 8)
        game.put(f"w{side}MoveListIndex", (0,))
        game.put(f"w{side}DisabledMove", (0,))
        game.put(f"w{side}SelectedMove", (chosen,))
        game.put(f"w{side}UsedMove", (0,))
        game.put(f"w{side}NumAttacksLeft", (0,))
        for offset in (1, 2, 3):
            game.put(f"w{side}BattleStatus{offset}", (0,))
    game.put("wDamage", (0, 0))
    game.put("wPartyMon1Moves", game.get_bytes("wBattleMonMoves", 4))
    game.put("wPartyMon1PP", (PP, 0, 0, 0))
    game.put("wPlayerMonNumber", (0,))
    game.put("wEnemyMonPartyPos", (0,))
    game.put("wIsInBattle", (2,))
    game.put("wLinkState", (4,))
    game.put("wSerialExchangeNybbleReceiveData", (0,))
    game.put("wActionResultOrTookBattleTurn", (0,))
    game.put("wBattleType", (0,))
    game.put("wOptions", (0x81,))


def act(game, side, move=None):
    if move is not None:
        game.put(f"w{side}SelectedMove", (move,))
    game.put("hWhoseTurn", (side == ENEMY,))
    call(game, f"Execute{side}Move")


def flag(game, side, status_byte, bit):
    return bool(game.get(f"w{side}BattleStatus{status_byte}") & bit)


def beam(game, actor):
    defender = other(actor)
    for scenario, start_hp, substitute, recharge in (
        ("survives", HP, 0, True),
        ("faints", 1, 0, False),
        ("misses", HP, 0, False),
        ("substitute survives", HP, 255, True),
        ("substitute breaks", HP, 1, False),
    ):
        seed_actions(game, actor, HYPER_BEAM, target_hp=start_hp)
        if substitute:
            game.put(f"w{defender}BattleStatus2", (SUBSTITUTE,))
            game.put(f"w{defender}SubstituteHP", (substitute,))
        random_bytes(game, 255, 255, 255 if scenario == "misses" else 0)
        act(game, actor)
        hp_after = stat(game, defender, "HP")
        assert draws(game) == 3, (actor, scenario, draws(game))
        assert flag(game, actor, 2, RECHARGE) == recharge, (actor, scenario)
        if substitute:
            assert hp_after == HP
            assert flag(game, defender, 2, SUBSTITUTE) == (substitute == 255)
        elif scenario == "survives":
            assert 0 < hp_after < start_hp
        elif scenario == "faints":
            assert hp_after == 0
        else:
            assert game.get("wMoveMissed") == 1 and hp_after == start_hp
        if actor == PLAYER:
            assert game.get("wBattleMonPP") == game.get("wPartyMon1PP") == PP - 1

        # Give the second action a living target after the faint or Substitute.
        put_stat(game, defender, "HP", HP)
        game.put(f"w{defender}BattleStatus2", (0,))
        random_bytes(game, 255, 255)
        act(game, actor, SWIFT)
        assert not flag(game, actor, 2, RECHARGE)
        assert (stat(game, defender, "HP") == HP) == recharge, (actor, scenario)
        assert draws(game) == (0 if recharge else 2), (actor, scenario, draws(game))
        if actor == PLAYER:
            assert game.get("wBattleMonPP") == PP - (1 if recharge else 2)


def fixed_damage(game, actor, core):
    defender = other(actor)
    for move, attack_type, target_type, hp, expected in (
        (NIGHT_SHADE, GHOST, NORMAL, HP, 50),
        (NIGHT_SHADE, GHOST, PSYCHIC, HP, 50),
        (SEISMIC_TOSS, FIGHTING, GHOST, HP, 50),
        (SONICBOOM, NORMAL, GHOST, HP, 20),
        (DRAGON_RAGE, NORMAL, NORMAL, HP, 40),
        (SUPER_FANG, NORMAL, GHOST, 159, 79),
        (SUPER_FANG, NORMAL, GHOST, 1, 1),
        (PSYWAVE, PSYCHIC, PSYCHIC, HP, 37),
    ):
        seed_actions(game, actor, move, attacker_type=attack_type,
                     defender_type=target_type, target_hp=hp)
        random_bytes(game, 0, 37)
        act(game, actor)
        assert hp - stat(game, defender, "HP") == expected, (actor, move, expected)
        assert game.get("wDamageMultipliers") == 10, (actor, move)
        assert game.get("wMoveMissed") == 0
        assert draws(game) == (2 if move == PSYWAVE else 1), (actor, move, draws(game))

    # The fixed-damage path still checks whether the move hits.
    seed_actions(game, actor, NIGHT_SHADE, defender_type=NORMAL)
    random_bytes(game, 255)
    act(game, actor)
    assert game.get("wMoveMissed") == 1
    assert stat(game, defender, "HP") == HP
    assert draws(game) == 1

    # Only Core uses the same positive Psywave rule for both battlers.
    seed_actions(game, actor, PSYWAVE, defender_type=PSYCHIC)
    random_bytes(game, 0, 0, 37)
    act(game, actor)
    positive = core or actor == PLAYER
    assert HP - stat(game, defender, "HP") == (37 if positive else 0)
    assert draws(game) == (3 if positive else 2)

    # Ordinary Ghost damage still uses the selected preset's Psychic entry.
    seed_actions(game, actor, LICK, attacker_type=GHOST, defender_type=PSYCHIC)
    random_bytes(game, 255, 255 if core else 0, 0, 255)
    act(game, actor)
    assert (stat(game, defender, "HP") < HP) == core
    assert game.get("wDamageMultipliers") & 0x7F == (20 if core else 0)


def trapping(game, actor):
    defender = other(actor)
    for move, duration, duration_bytes, immune, copied in (
        (WRAP, 2, (0,), False, False),
        (BIND, 3, (1,), False, False),
        (CLAMP, 4, (2, 2), False, False),
        (FIRE_SPIN, 5, (3, 3), False, False),
        (WRAP, 2, (0,), True, False),
        (WRAP, 2, (0,), False, True),
    ):
        seed_actions(game, actor, MIRROR_MOVE if copied else move,
                     defender_type=GHOST if immune else NORMAL)
        if copied:
            game.put(f"w{defender}UsedMove", (move,))
        random_bytes(game, *duration_bytes, 255, *((0,) if immune else (255, 0)))
        act(game, actor)
        damage = HP - stat(game, defender, "HP")
        assert (damage == 0) == immune, (actor, move, damage)
        assert flag(game, actor, 1, TRAPPING), (actor, move, immune)
        assert game.get(f"w{actor}NumAttacksLeft") == duration - 1
        if actor == PLAYER:
            assert game.get("wBattleMonPP") == game.get("wPartyMon1PP") == PP - 1
        for turn in range(duration):
            if turn:
                random_bytes(game, 255)
                act(game, actor)
                assert draws(game) == 0, (actor, move, turn, draws(game))
                assert stat(game, defender, "HP") == HP - damage * (turn + 1)
            random_bytes(game, 255, 255)
            act(game, defender)
            assert stat(game, actor, "HP") == HP, (actor, move, turn)
            assert draws(game) == 0
            if actor == ENEMY:
                assert game.get("wBattleMonPP") == PP
            call(game, "CheckNumAttacksLeft")
            assert flag(game, actor, 1, TRAPPING) == (turn + 1 < duration)
        if actor == PLAYER:
            assert game.get("wBattleMonPP") == game.get("wPartyMon1PP") == PP - 1
        act(game, defender)
        assert stat(game, actor, "HP") < HP

    seed_actions(game, actor, WRAP)
    random_bytes(game, 0, 255, 255, 255)
    act(game, actor)
    assert game.get("wMoveMissed") == 1
    assert not flag(game, actor, 1, TRAPPING)
    assert stat(game, defender, "HP") == HP


def trap_durations(game, actor):
    seed_actions(game, actor, WRAP)
    counts = [0] * 4
    for first in range(4):
        for second in range(4):
            game.put(f"w{actor}BattleStatus1", (0,))
            game.put("hWhoseTurn", (actor == ENEMY,))
            random_bytes(game, first, second)
            call(game, "TrappingEffect")
            counts[game.get(f"w{actor}NumAttacksLeft") - 1] += 1
            assert draws(game) == (1 if first < 2 else 2)
    assert counts == [6, 6, 2, 2]


def sleep(game, actor):
    defender = other(actor)
    seed_actions(game, actor, SLEEP_POWDER)
    random_bytes(game, 0, 0, 2)
    act(game, actor)
    assert game.get(mon_label(defender) + "Status") == 2
    assert draws(game) == 3
    for counter in (1, 0):
        random_bytes(game, 255, 255)
        act(game, defender)
        assert game.get(mon_label(defender) + "Status") == counter
        assert game.get(f"w{defender}UsedMove") == 0
        assert stat(game, actor, "HP") == HP
        assert draws(game) == 0
        if defender == PLAYER:
            assert game.get("wBattleMonPP") == PP
    act(game, defender)
    assert stat(game, actor, "HP") < HP

    seed_actions(game, actor, SWIFT)
    game.put(mon_label(actor) + "Status", (FROZEN,))
    random_bytes(game, 255, 255)
    act(game, actor)
    assert game.get(mon_label(actor) + "Status") == FROZEN
    assert stat(game, defender, "HP") == HP
    assert draws(game) == 0


def seed_link_rosters(left, right):
    setup_player(left, "BLUE", 0x69, "RIVER", (0x12, 0x34), SWIFT, 20)
    setup_player(right, "GREEN", 0x1B, "STAR", (0x56, 0x78), SWIFT, 20)
    left.put("wPartyMon1Moves", (HYPER_BEAM, SWIFT, 0, 0))
    left.put("wPartyMon1PP", (5, 20, 0, 0))
    left.put("wPartyMon1Speed", (0, 120))
    length = right.addresses["wPartyMon2Species"][1] - right.addresses["wPartyMon1Species"][1]
    right.put("wPartyMon2Species", right.get_bytes("wPartyMon1Species", length))
    right.put("wPartySpecies", (0x1B, 0x69, 0xFF))
    right.put("wPartyMon2Species", (0x69,))
    right.put("wPartyMon2Nick", bytes((0x92, 0x8F, 0x80, 0x91, 0x84, 0x50)))
    right.put("wPartyCount", (2,))


def choose_first_move(cable, *players):
    cable.tick(24)
    cable.press(A, *players)
    cable.wait(lambda: all(game.get("wTopMenuItemY") == 12 for game in players),
               "the selected player's FIGHT menu")
    cable.tick(24)
    cable.press(A, *players)


def link_beam(library, boot, rom):
    with Game(library, boot, rom) as left, Game(library, boot, rom) as right:
        seed_link_rosters(left, right)
        with Cable(left, right) as cable:
            choose_room(cable, COLOSSEUM)
            use_table_game_boys(cable)
            cable.wait(lambda: all(in_battle_commands(game) for game in cable.players),
                       "both battle command menus", frames=2400)
            for game in cable.players:
                random_bytes(game, 255, 255, 0, 255, 255)
            choose_first_move(cable, left, right)
            cable.wait(lambda: in_battle_commands(right) and flag(right, ENEMY, 2, RECHARGE),
                       "a surviving target and the attacker's recharge", frames=2400)
            remaining = stat(right, PLAYER, "HP")
            assert 0 < remaining == stat(left, ENEMY, "HP") < HP
            assert flag(left, PLAYER, 2, RECHARGE) and left.get("wBattleMonPP") == 4

            choose_first_move(cable, right)
            cable.wait(lambda: all(in_battle_commands(game) for game in cable.players)
                       and not flag(left, PLAYER, 2, RECHARGE), "both sides after the recharge",
                       frames=2400)
            assert left.get("wBattleMonPP") == 4
            assert stat(right, PLAYER, "HP") == remaining

            # Start the next round with a target at one HP on both copies of the battle.
            put_stat(left, ENEMY, "HP", 1)
            put_stat(right, PLAYER, "HP", 1)
            for game in cable.players:
                random_bytes(game, 255, 255, 0)
            choose_first_move(cable, left, right)
            cable.wait(lambda: "SPARE" in right.visible_text() and stat(right, PLAYER, "HP") == 0,
                       "the right player's replacement menu", advance=(right,))
            cable.tick(24)
            cable.press(DOWN, right)
            cable.wait(lambda: right.get("wLastMenuItem") == 1, "the replacement Pokémon")
            cable.press(A, right)
            cable.wait(lambda: all(in_battle_commands(game) for game in cable.players)
                       and right.get("wPlayerMonNumber") == 1, "the next round after the knockout")
            assert left.get("wBattleMonPP") == 3
            assert not flag(left, PLAYER, 2, RECHARGE)
            assert not flag(right, ENEMY, 2, RECHARGE)
            assert stat(left, ENEMY, "HP") == stat(right, PLAYER, "HP") == HP


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--color", choices=("red", "blue", "green"), nargs="+")
    parser.add_argument("--linked", action="store_true", help="Also run the live cable battle.")
    args = parser.parse_args()
    for color in args.color or ("red", "blue", "green"):
        with Game(args.sameboy, args.boot, args.directory / f"poke{color}.gbc") as game:
            game.new_game()
            for actor in (PLAYER, ENEMY):
                beam(game, actor)
                fixed_damage(game, actor, args.directory.name == "core")
                trapping(game, actor)
                trap_durations(game, actor)
                sleep(game, actor)
        print(f"{args.directory.name} {color}: recharge, fixed damage, trapping, and sleep passed",
              flush=True)
    if args.linked:
        color = (args.color or ("red",))[0]
        link_beam(args.sameboy, args.boot, args.directory / f"poke{color}.gbc")
        print(f"{args.directory.name} {color}: live cable Hyper Beam passed", flush=True)


if __name__ == "__main__":
    main()
