"""Verify the Gen 1 critical-hit rules in each built cartridge."""

import argparse
from pathlib import Path

from cartridge_smoke import Game

FOCUS_ENERGY = 0x74
PUMPED = 1 << 2
LINK_BATTLE = 4
DIRE_HIT = 0x3a
JOLTEON = 0x68
TACKLE = 0x21
SLASH = 0xa3


def threshold(speed, move, pumped, core):
    ordinary = speed // 2
    base = min(255, ordinary * 8) if move == SLASH else ordinary
    if not pumped:
        return base
    if core:
        return min(255, base * 4)
    return (speed // 4) * 4 if move == SLASH else speed // 8


def set_attack(game, side, move, power, pumped):
    game.put("hWhoseTurn", (side == "Enemy",))
    game.put(f"w{side}MoveNum", (move, 0, power))
    game.put(f"w{side}BattleStatus2", (PUMPED if pumped else 0,))


def check_roll(game, expected, roll, *, speed=None, power=40):
    # BattleRandom rotates the byte left three times before comparing it.
    raw = ((roll >> 3) | (roll << 5)) & 0xff
    game.put("wLinkBattleRandomNumberList", (raw,))
    game.put("wLinkBattleRandomNumberListIndex", (0,))
    if speed is None:
        game.invoke("CriticalHitTest")
    else:
        game.put("wMonHBaseSpeed", (speed,))
        game.put("wCriticalHitOrOHKO", (0,))
        game.invoke("CriticalHitTest.readSpeed")
    # Keep a VBlank interrupt from entering between short routine calls.
    game.write(0xffff, (0,))
    for _ in range(1000):
        if game.cpu.pc == 0xc900:
            break
        game.core.GB_run(game.gb)
    else:
        raise AssertionError(f"Critical hit check did not return at {game.cpu.pc:04x}.")
    assert game.get("wLinkBattleRandomNumberListIndex") == int(power != 0)
    assert game.get("wCriticalHitOrOHKO") == int(roll < expected), (speed, roll, expected)


def check_thresholds(game, core):
    # The real link RNG reads a shared random byte each time, even on a miss.
    game.put("wLinkState", (LINK_BATTLE,))
    for side in ("Player", "Enemy"):
        species = "wBattleMonSpecies" if side == "Player" else "wEnemyMonSpecies"
        game.put(species, (JOLTEON,))
        for move in (TACKLE, SLASH):
            for pumped in (False, True):
                set_attack(game, side, move, 40, pumped)
                for speed in range(256):
                    expected = threshold(speed, move, pumped, core)
                    if expected:
                        check_roll(game, expected, expected - 1, speed=speed)
                    check_roll(game, expected, expected, speed=speed)

                # Also enter through the species lookup in the ordinary path.
                expected = threshold(130, move, pumped, core)
                check_roll(game, expected, expected - 1)
                check_roll(game, expected, expected)

        set_attack(game, side, FOCUS_ENERGY, 0, True)
        check_roll(game, 0, 0, power=0)


def check_pumped_effects(game):
    game.put("wIsInBattle", (1,))
    for side in ("Player", "Enemy"):
        set_attack(game, side, FOCUS_ENERGY, 0, False)
        other = "Player" if side == "Enemy" else "Enemy"
        game.put(f"w{other}BattleStatus2", (0,))
        game.invoke("FocusEnergyEffect_")
        game.wait(lambda: game.get(f"w{side}BattleStatus2") & PUMPED)
        assert game.get(f"w{other}BattleStatus2") == 0
        game.wait(lambda: game.cpu.pc == 0xc900, accept=True)

    game.put("wPlayerBattleStatus2", (0,))
    game.put("wNumBagItems", (1, DIRE_HIT, 1, 0xff))
    game.put("wCurItem", (DIRE_HIT,))
    game.put("wWhichPokemon", (0,))
    game.invoke("ItemUseDireHit")
    game.wait(lambda: game.cpu.pc == 0xc900, accept=True)
    assert game.get("wPlayerBattleStatus2") & PUMPED
    assert game.get_bytes("wNumBagItems", 2) == bytes((0, 0xff))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        with Game(args.sameboy, args.boot, rom) as game:
            game.new_game()
            check_thresholds(game, args.directory.name == "core")
        with Game(args.sameboy, args.boot, rom) as game:
            game.new_game()
            check_pumped_effects(game)
        print(f"{args.directory.name} {color}: critical hits, Focus Energy, and Dire Hit passed", flush=True)


if __name__ == "__main__":
    main()
