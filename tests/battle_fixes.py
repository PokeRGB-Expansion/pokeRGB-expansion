"""Check battle repair boundaries on the built cartridge."""

import argparse
from pathlib import Path

from acid_armor import invoke_visual
from cartridge_smoke import Game
from protected_mechanics import (
    ENEMY, PLAYER, SWIFT, mon_label, other, put_stat, random_bytes, seed_actions, stat,
)

SUBSTITUTE = 0xa4
HAS_SUBSTITUTE = 1 << 4
SUPER_POTION = 0x13
JUMP_KICK = 0x1a
JUMP_KICK_EFFECT = 0x2d
EXPLODE_EFFECT = 0x07
NORMAL, GROUND, ROCK = 0, 4, 5
WATER, GRASS, ELECTRIC, DRAGON = 0x15, 0x16, 0x17, 0x1a


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



def check_feedback(game, _core):
    cases = (
        (ELECTRIC, WATER, GRASS, 120, 10),
        (ELECTRIC, GRASS, WATER, 120, 10),
        (ELECTRIC, NORMAL, NORMAL, 120, 10),
        (WATER, GROUND, ROCK, 480, 40),
        (ELECTRIC, GRASS, DRAGON, 30, 2),
        (ELECTRIC, WATER, GROUND, 0, 0),
    )
    for actor in (PLAYER, ENEMY):
        seed_actions(game, actor, SWIFT)
        for move_type, type1, type2, damage, feedback in cases:
            game.put("hWhoseTurn", (actor == ENEMY,))
            game.put(f"w{actor}MoveType", (move_type,))
            game.put(mon_label(other(actor)) + "Type", (type1, type2))
            game.put("wDamage", (0, 120))
            game.put("wDamageMultipliers", (10,))
            game.put("wMoveMissed", (0,))
            game.invoke("AdjustDamageForMoveType")
            game.return_to_stub()
            assert game.get("wDamageMultipliers") == feedback
            assert int.from_bytes(game.get_bytes("wDamage", 2), "big") == damage
            assert game.get("wMoveMissed") == int(damage == 0)

            game.put("wTileMap", (0x7f,) * 360)
            if feedback:
                game.invoke("DisplayEffectiveness")
                game.wait(lambda: game.cpu.pc == 0xc900, accept=True)
                text = game.visible_text()
                assert ("super" in text) == (feedback > 10)
                assert ("not very" in text) == (feedback < 10)
            game.put("wFrequencyModifier", (0x12,))
            game.put("wTempoModifier", (0x34,))
            game.invoke("PlayApplyingAttackSound")
            game.return_to_stub()
            sound = game.get("wFrequencyModifier"), game.get("wTempoModifier")
            expected_sound = {0: (0x12, 0x34), 2: (0x50, 1),
                              10: (0x20, 0x30), 40: (0xe0, 0xff)}
            assert sound == expected_sound[feedback]


def check_damage_division(game, core):
    cases = [(77, 0), (1, EXPLODE_EFFECT), (255, 0)]
    if core:
        cases += [(0, 0), (256, 0), (499, 0), (499, EXPLODE_EFFECT)]
    attack, power, level = 215, 80, 50
    for actor in (PLAYER, ENEMY):
        for defense, effect in cases:
            game.put("hWhoseTurn", (actor == ENEMY,))
            game.put(f"w{actor}MoveEffect", (effect,))
            game.put("wDamage", (0, 0))
            game.invoke("CalculateDamage")
            game.cpu.bc = (attack << 8) | (defense & 0xff)
            game.cpu.de = (power << 8) | level
            game.cpu.hl = defense & 0xff00
            game.return_to_stub()
            divisor = max(1, defense // 2 if effect == EXPLODE_EFFECT else defense)
            before_division = (2 * level // 5 + 2) * power * attack
            expected = min(999, before_division // divisor // 50 + 2)
            assert int.from_bytes(game.get_bytes("wDamage", 2), "big") == expected, (
                actor, defense, effect, expected
            )


def check_self_damage(game, core):
    for actor in (PLAYER, ENEMY):
        target = other(actor)
        for confusion in (False, True):
            for own_doll, other_doll in ((False, False), (False, True), (True, False), (True, True)):
                seed_actions(game, actor, JUMP_KICK)
                game.put("hWhoseTurn", (actor == ENEMY,))
                game.put("wDamageMultipliers", (10,))
                game.put(f"w{actor}BattleStatus2", (HAS_SUBSTITUTE if own_doll else 0,))
                game.put(f"w{target}BattleStatus2", (HAS_SUBSTITUTE if other_doll else 0,))
                game.put(f"w{actor}SubstituteHP", (40,))
                game.put(f"w{target}SubstituteHP", (40,))
                if confusion:
                    game.put(f"w{actor}BattleStatus1", (1 << 7,))
                    game.put(f"w{actor}ConfusedCounter", (3,))
                    random_bytes(game, 255)
                    routine = f"Execute{actor}Move"
                else:
                    game.put(f"w{actor}MoveEffect", (JUMP_KICK_EFFECT,))
                    routine = "PrintMoveFailureText"
                stop = invoke_visual(game, routine)
                game.wait(lambda: game.cpu.pc == stop, accept=True)
                damage = 19 if confusion else 1
                assert stat(game, actor, "HP") == (160 if own_doll else 160 - damage)
                assert stat(game, target, "HP") == 160
                assert game.get(f"w{actor}SubstituteHP") == 40 - damage * (own_doll and core)
                assert game.get(f"w{target}SubstituteHP") == 40 - damage * (own_doll and not core)


def check_interrupted_charge(game, core):
    charging, invulnerable = 1 << 4, 1 << 6
    for actor in (PLAYER, ENEMY):
        for move in (0x13, 0x5b):  # Fly and Dig
            seed_actions(game, actor, move)
            game.put("hWhoseTurn", (actor == ENEMY,))
            game.put(mon_label(actor) + "Status", (1 << 6,))  # Paralysis.
            game.put(f"w{actor}MoveEffect", (0x2b,))  # FLY_EFFECT.
            game.put(f"w{actor}BattleStatus1", (charging | invulnerable,))
            random_bytes(game, 0)
            stop = invoke_visual(game, f"Execute{actor}Move")
            game.wait(lambda: game.cpu.pc == stop, accept=True)
            assert game.get(f"w{actor}BattleStatus1") == (0 if core else invulnerable)
            assert game.get_bytes(mon_label(actor) + "PP", 4) == bytes((15, 0, 0, 0))
            assert stat(game, other(actor), "HP") == 160


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    core = args.directory.name == "core"
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        for check in (check_blaine, check_substitute, check_feedback, check_damage_division,
                      check_self_damage, check_interrupted_charge):
            with Game(args.sameboy, args.boot, rom) as game:
                game.new_game()
                check(game, core)
        print(f"{args.directory.name} {color}: battle boundary checks passed", flush=True)


if __name__ == "__main__":
    main()
