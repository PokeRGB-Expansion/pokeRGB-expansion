"""Check that medicine preserves battle stats through the Bag and party menus."""

import argparse
from pathlib import Path

from cartridge_smoke import Game, seed_party


BURN, PARALYSIS, POISON = 0x10, 0x40, 0x08
BURN_HEAL, PARLYZ_HEAL, FULL_RESTORE, FULL_HEAL = 0x0C, 0x0F, 0x10, 0x34
ALL_STAT_BADGES = 0x55
BADLY_POISONED = 1
STATS = ("MaxHP", "Attack", "Defense", "Speed", "Special")
BASE_STATS = (160, 139, 87, 113, 203)
DOWN, A = 3, 4


def get_number(game, label):
    return int.from_bytes(game.get_bytes(label, 2), "big")


def put_number(game, label, number):
    game.put(label, number.to_bytes(2, "big"))


def active_stats(game):
    return tuple(get_number(game, "wBattleMon" + stat) for stat in STATS)


def run(game, label):
    game.invoke(label)
    game.wait(lambda: game.cpu.pc == 0xc900, accept=True)


def setup_battle(game, condition, hp, *, bench=False, badges=ALL_STAT_BADGES):
    seed_party(game)
    for mon, name in (("wPartyMon1", bytes((0x80, 0x92, 0x87))),
                      ("wPartyMon2", bytes((0x8C, 0x88, 0x92, 0x93, 0x98)))):
        game.put(mon + "Nick", name.ljust(11, b"\x50"))
        for stat, value in zip(STATS, BASE_STATS):
            put_number(game, mon + stat, value)
        game.put(mon + "Status", (0,))
    target = "wPartyMon2" if bench else "wPartyMon1"
    game.put(target + "Status", (condition,))
    put_number(game, target + "HP", hp)
    active_status = PARALYSIS if bench else condition
    game.put("wPartyMon1Status", (active_status,))
    game.put("wPlayerBattleStatus1", (0,))
    game.put("wPlayerBattleStatus2", (0,))
    game.put("wPlayerBattleStatus3", (BADLY_POISONED if active_status == POISON else 0,))
    game.put("wEnemyBattleStatus1", (0,))
    game.put("wEnemyBattleStatus2", (0,))
    game.put("wEnemyBattleStatus3", (0,))
    game.put("wEnemyMonStatus", (0,))
    game.put("wEnemyMonSpecies", (0x1B,))
    game.put("wEnemyMonNick", bytes((0x91, 0x88, 0x95, 0x80, 0x8B, 0x50)))
    game.put("wEnemyMonLevel", (45,))
    put_number(game, "wEnemyMonHP", 160)
    put_number(game, "wEnemyMonMaxHP", 160)
    game.put("wIsInBattle", (1,))
    game.put("wLinkState", (0,))
    game.put("wOptions", (0x81,))  # Battle animations off and fast text.
    game.put("wBattleType", (0,))
    game.put("wObtainedBadges", (badges,))
    game.put("wWhichPokemon", (0,))
    game.put("wPlayerMonNumber", (0,))
    game.put("wMenuJoypadPollCount", (0,))
    game.put("wMenuWatchMovingOutOfBounds", (0,))
    game.put("wPartyAndBillsPCSavedMenuItem", (0,))
    game.put("wBagSavedMenuItem", (0,))
    game.put("wBattleAndStartSavedMenuItem", (0,))
    game.put("wActionResultOrTookBattleTurn", (0,))
    game.put("wBattleMonSpecies2", (game.get("wPartyMon1Species"),))
    run(game, "LoadBattleMonFromParty")
    return target


def raise_stat(game, move, effect):
    game.put("hWhoseTurn", (0,))
    game.put("wPlayerMoveNum", (move,))
    game.put("wPlayerMoveEffect", (effect,))
    run(game, "StatModifierUpEffect")


def lower_stat(game, move, effect):
    game.put("hWhoseTurn", (1,))
    game.put("wEnemyMoveNum", (move,))
    game.put("wEnemyMoveEffect", (effect,))
    # Start at the normal stat change after accuracy and Substitute checks.
    game.invoke("StatModifierDownEffect.decrementStatMod")
    game.cpu.hl = game.addresses["wPlayerMonStatMods"][1]
    game.cpu.de = game.addresses["wEnemyMoveEffect"][1]
    game.cpu.af = (effect - 0x12) << 8
    game.wait(lambda: game.cpu.pc == 0xc900, accept=True)


def use_medicine(game, item, *, bench=False, succeeds=True):
    game.put("wNumBagItems", (1, item, 1, 0xFF))
    game.invoke("DisplayBattleMenu")
    game.wait(lambda: "FIGHT" in game.visible_text() and "ITEM" in game.visible_text())
    game.tick(16)
    game.press(DOWN)
    game.wait(lambda: game.get("wLastMenuItem") == 1)
    game.press(A)
    game.wait(lambda: "CANCEL" in game.visible_text())
    game.tick(16)
    game.press(A)
    game.wait(lambda: "MISTY" in game.visible_text() and "ASH" in game.visible_text())
    game.tick(24)
    if bench:
        game.press(DOWN)
        game.wait(lambda: game.get("wLastMenuItem") == 1)
    game.press(A)
    if not succeeds:
        game.wait(lambda: "have any" in game.visible_text() and "effect" in game.visible_text())
        assert game.get("wActionResultOrTookBattleTurn") == 0
        assert game.get_bytes("wNumBagItems", 4) == bytes((1, item, 1, 0xFF))
        return
    game.wait(lambda: game.cpu.pc == 0xc900, accept=True)
    assert game.get("wActionResultOrTookBattleTurn") == 1
    assert game.get_bytes("wNumBagItems", 2) == bytes((0, 0xFF))


def badge_boost(value):
    return min(999, value + value // 8)


def check_cure(game, core, condition, item, hp, *, bench=False):
    target = setup_battle(game, condition, hp, bench=bench)
    result_hp = 160 if item == FULL_RESTORE else hp
    expected_attack = expected_speed = None
    if condition == BURN and not bench:
        raise_stat(game, 0x0E, 0x32)  # Swords Dance.
        lower_stat(game, 0x2D, 0x12)  # Growl reduces Attack to stage +1.
        attack = badge_boost(BASE_STATS[1] * 15 // 10)
        assert get_number(game, "wBattleMonAttack") == attack // 2
        lower_stat(game, 0x27, 0x13)  # Tail Whip reapplies the burn penalty and badges.
        assert get_number(game, "wBattleMonAttack") == badge_boost(attack // 2) // 2
        raise_stat(game, 0x6A, 0x0B)  # Harden reapplies the badges again.
        expected_attack = badge_boost(badge_boost(attack))
        assert expected_attack == 295
    elif condition == PARALYSIS and not bench:
        raise_stat(game, 0x61, 0x34)  # Agility.
        lower_stat(game, 0x51, 0x14)  # String Shot reduces Speed to stage +1.
        speed = badge_boost(BASE_STATS[3] * 15 // 10)
        assert get_number(game, "wBattleMonSpeed") == speed // 4
        lower_stat(game, 0x27, 0x13)
        assert get_number(game, "wBattleMonSpeed") == badge_boost(speed // 4) // 4
        expected_speed = badge_boost(speed)
        assert expected_speed == 213
    else:
        lower_stat(game, 0x2D, 0x12)
        raise_stat(game, 0x6A, 0x0B)
    before = active_stats(game)
    modifiers = game.get_bytes("wPlayerMonStatMods", 8)
    battle_condition = game.get("wBattleMonStatus")
    use_medicine(game, item, bench=bench)
    assert game.get_bytes("wPlayerMonStatMods", 8) == modifiers
    assert game.get(target + "Status") == 0
    assert get_number(game, target + "HP") == result_hp
    if bench:
        assert game.get("wBattleMonStatus") == battle_condition
        assert active_stats(game) == before
        assert get_number(game, "wBattleMonHP") == 160
        return
    assert game.get("wBattleMonStatus") == 0
    assert get_number(game, "wBattleMonHP") == result_hp
    toxic_left = not core and condition == POISON and item == FULL_RESTORE and hp < 160
    assert bool(game.get("wPlayerBattleStatus3") & BADLY_POISONED) == toxic_left
    expected = list(before)
    if expected_attack is not None:
        expected[1] = expected_attack
    if expected_speed is not None:
        expected[3] = expected_speed
    if not core:
        expected = before if item == FULL_RESTORE and hp < 160 else BASE_STATS
    assert active_stats(game) == tuple(expected), (active_stats(game), expected)


def check_minimum_stage(game, core):
    setup_battle(game, BURN, 160, badges=0)
    game.put("wPlayerMonAttackMod", (2,))  # The next drop reaches stage -6.
    lower_stat(game, 0x2D, 0x12)
    assert get_number(game, "wBattleMonAttack") == (139 // 4) // 2
    use_medicine(game, BURN_HEAL)
    assert game.get("wPlayerMonAttackMod") == 1
    assert get_number(game, "wBattleMonAttack") == (139 // 4 if core else 139)


def check_maximum_stage(game, core):
    setup_battle(game, PARALYSIS, 160, badges=0)
    game.put("wPlayerMonSpeedMod", (11,))  # The next boost reaches stage +6.
    raise_stat(game, 0x61, 0x34)
    lower_stat(game, 0x27, 0x13)
    assert get_number(game, "wBattleMonSpeed") == 113
    use_medicine(game, PARLYZ_HEAL)
    assert game.get("wPlayerMonSpeedMod") == 13
    assert get_number(game, "wBattleMonSpeed") == (113 * 4 if core else 113)


def check_stat_rebuild(game, core):
    setup_battle(game, BURN, 160)
    lower_stat(game, 0x2D, 0x12)
    put_number(game, "wPlayerMonUnmodifiedAttack", 177)
    game.put("wCalculateWhoseStats", (0,))
    # The level-up path rebuilds the staged stats, then applies penalties and badges.
    run(game, "CalculateModifiedStats")
    run(game, "ApplyBurnAndParalysisPenaltiesToPlayer")
    run(game, "ApplyBadgeStatBoosts")
    reduced = 177 * 66 // 100
    assert get_number(game, "wBattleMonAttack") == badge_boost(reduced // 2)
    use_medicine(game, BURN_HEAL)
    assert get_number(game, "wBattleMonAttack") == (badge_boost(reduced) if core else 139)


def check_haze(game):
    setup_battle(game, BURN, 160)
    lower_stat(game, 0x2D, 0x12)
    assert active_stats(game) != BASE_STATS
    game.put("hWhoseTurn", (0,))
    game.put("wPlayerMoveNum", (0x72,))  # Haze.
    run(game, "HazeEffect_")
    assert game.get("wBattleMonStatus") == BURN
    assert active_stats(game) == BASE_STATS
    use_medicine(game, BURN_HEAL)
    assert active_stats(game) == BASE_STATS


def check_transform(game, core):
    setup_battle(game, BURN, 160)
    lower_stat(game, 0x2D, 0x12)
    copied_stats = (160, 187, 128, 121, 155)
    for stat, value in zip(STATS, copied_stats):
        put_number(game, "wEnemyMon" + stat, value)
    game.put("wEnemyMonSpecies2", (0x1B,))
    game.put("wEnemyMonStatMods", bytes((7,)) * 8)
    game.put("wEnemyMonMoves", (0x96, 0, 0, 0))
    game.put("hWhoseTurn", (0,))
    game.put("wPlayerMoveNum", (0x90,))  # Transform.
    run(game, "TransformEffect_")
    assert game.get("wPlayerBattleStatus3") & (1 << 3)
    assert game.get("wBattleMonStatus") == BURN
    assert active_stats(game) == copied_stats
    use_medicine(game, BURN_HEAL)
    assert active_stats(game) == (copied_stats if core else BASE_STATS)
    assert game.get("wPlayerBattleStatus3") & (1 << 3)


def check_no_effect(game):
    for condition, item in ((PARALYSIS, BURN_HEAL), (0, FULL_RESTORE)):
        setup_battle(game, condition, 160)
        lower_stat(game, 0x27, 0x13)
        before = active_stats(game)
        use_medicine(game, item, succeeds=False)
        assert active_stats(game) == before
        assert game.get("wBattleMonStatus") == condition
        assert game.get("wPartyMon1Status") == condition
        assert get_number(game, "wBattleMonHP") == 160


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--color", choices=("red", "blue", "green"), nargs="+")
    args = parser.parse_args()
    core = args.directory.name == "core"
    for color in args.color or ("red", "blue", "green"):
        with Game(args.sameboy, args.boot, args.directory / f"poke{color}.gbc") as game:
            game.new_game()
            for condition, item, hp in (
                (BURN, BURN_HEAL, 160),
                (PARALYSIS, PARLYZ_HEAL, 160),
                (BURN, FULL_RESTORE, 160),
                (PARALYSIS, FULL_RESTORE, 60),
                (POISON, FULL_HEAL, 75),
                (POISON, FULL_RESTORE, 75),
                (0, FULL_RESTORE, 60),
            ):
                check_cure(game, core, condition, item, hp)
            check_cure(game, core, BURN, BURN_HEAL, 160, bench=True)
            check_cure(game, core, BURN, FULL_RESTORE, 60, bench=True)
            check_minimum_stage(game, core)
            check_maximum_stage(game, core)
            check_stat_rebuild(game, core)
            check_haze(game)
            check_transform(game, core)
            check_no_effect(game)
        print(f"{args.directory.name} {color}: Bag medicine stats and HP passed", flush=True)


if __name__ == "__main__":
    main()
