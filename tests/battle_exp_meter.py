"""Check the battle EXP meter against party records and the original HUD."""

import argparse
import ctypes as C
from pathlib import Path

from adventure_checkpoints import advance_text_until
from battle_stats_return import A, DOWN, RIGHT, PIDGEY, ROUTE_1, battle_ready, open_stats_and_return
from cartridge_smoke import Game, seed_party
from exp_all import AwardCase, START_EXP, expected_shares, seed_award
from pc_browsing import name_bytes

LABEL = bytes((0xC0, 0xC1))
EMPTY_TRACK = 0xC2
WIDTH = 48
STOCK_BORDER = bytes((0x76,)) * 8
GROWTH = ((1, 1, 0, 0, 0), (3, 4, 10, 0, 30), (3, 4, 20, 0, 70),
          (6, 5, -15, 100, 140), (4, 5, 0, 0, 0), (5, 4, 0, 0, 0))


def threshold(curve, level):
    a, b, c, d, e = GROWTH[curve]
    return max(0, a * level**3 // b + c * level**2 + d * level - e)


def filled(curve, level, xp):
    if level == 100:
        return 0
    lower, upper = threshold(curve, level), threshold(curve, level + 1)
    return max(0, min(WIDTH, (xp - lower) * WIDTH // (upper - lower)))


def track(pixels):
    return LABEL + bytes(EMPTY_TRACK + max(0, min(8, pixels - 8 * slot)) for slot in range(6))


def rail(game, tilemap="wTileMap"):
    return game.get_bytes(tilemap, 11 * 20 + 18)[11 * 20 + 10:]


def check_math(game):
    scratch = bytes(range(0x50, 0x5a))
    for curve in range(len(GROWTH)):
        game.put("wMonHGrowthRate", (curve,))
        game.put("wPlayerMonNumber", (1,))
        for level in (1, 2, 45, 99, 100):
            low, high = threshold(curve, level), threshold(curve, level + 1)
            for xp in {max(0, low - 1), low, low + (high - low) * 3 // 8, high - 1, high, 0xffffff}:
                game.put("wPartyMon2Exp", xp.to_bytes(3, "big"))
                game.put("hDividend", scratch)
                game.invoke("CacheBattleExpPixels")
                game.cpu.de = level << 8
                game.return_to_stub()
                result = game.get("wBattleExpPixels")
                assert result == filled(curve, level, xp), (curve, level, xp, result)
                assert game.get_bytes("hDividend", len(scratch)) == scratch

    # A partial or unsupported species record must not index past GrowthRateTable.
    for invalid in (len(GROWTH), 26, 0xff):
        game.put("wMonHGrowthRate", (invalid,))
        game.put("wBattleExpPixels", (17,))
        game.invoke("CacheBattleExpPixels")
        game.cpu.de = 45 << 8
        game.return_to_stub()
        assert game.get("wBattleExpPixels") == 0


def check_authored_curve(game):
    # Edit the test emulator's copy of the first growth record to 10 * level³.
    # Its last ten levels cross both signed 24-bit EXP and 16-bit level widths.
    size = C.c_size_t()
    rom = game.core.GB_get_direct_access(game.gb, 0, C.byref(size), None)
    bank, address = game.addresses["GrowthRateTable"]
    curve = rom + bank * 0x4000 + address % 0x4000
    assert C.c_ubyte.from_address(curve).value == 0x11
    C.c_ubyte.from_address(curve).value = 0xa1
    level = 95
    low, high = 10 * level**3, 10 * (level + 1)**3
    xp = low + (high - low) // 3
    game.put("wPartyMon2Exp", xp.to_bytes(3, "big"))
    game.put("wMonHGrowthRate", (0,))
    game.invoke("CacheBattleExpPixels")
    game.cpu.de = level << 8
    game.return_to_stub()
    assert game.get("wBattleExpPixels") == WIDTH * (xp - low) // (high - low)


def check_wild_battle(game, enabled):
    game.new_game()
    seed_party(game)
    # Vaporeon (medium fast) and Squirtle (medium slow) share the same level,
    # but sit at different points between thresholds.
    game.put("wPartySpecies", (0x69, 0xb1, 0xff))
    game.put("wPartyMon1Nick", name_bytes("VAPOREON"))
    game.put("wPartyMon2Nick", name_bytes("SQUIRTLE"))
    game.put("wPartyMon2Species", (0xb1,))
    # Give each level-45 Pokémon its ordinary battle stats at zero DVs
    # and stat experience. An enemy attack after SWITCH uses these fields.
    for slot, stats in ((1, (63, 59, 63, 104)), (2, (48, 63, 43, 50))):
        for field, value in zip(("Attack", "Defense", "Speed", "Special"), stats):
            game.put(f"wPartyMon{slot}{field}", value.to_bytes(2, "big"))
    for slot, curve, percent in ((1, 0, 25), (2, 3, 75)):
        low, high = threshold(curve, 45), threshold(curve, 46)
        xp = low + (high - low) * percent // 100
        game.put(f"wPartyMon{slot}Exp", xp.to_bytes(3, "big"))
    game.put("wOptions", (0xc1,))
    game.enter_map(ROUTE_1, 10, 5, 4)
    game.put("wCurOpponent", (PIDGEY,))
    game.put("wCurEnemyLevel", (5,))
    advance_text_until(game, lambda: battle_ready(game))

    def check_slot(slot, curve):
        xp = int.from_bytes(game.get_bytes(f"wPartyMon{slot}Exp", 3), "big")
        expected = track(filled(curve, 45, xp)) if enabled else STOCK_BORDER
        assert rail(game) == expected, (slot, rail(game), expected)

    check_slot(1, 0)
    # Go through real STATS and return to the battle menu.
    open_stats_and_return(game)
    check_slot(1, 0)

    game.tick(16)
    game.press(RIGHT)
    game.wait(lambda: game.get("wTopMenuItemX") == 15)
    game.tick(12)
    game.press(A)
    game.wait(lambda: game.visible_text().count("160 160") == 2)
    game.tick(20)
    if game.get("wCurrentMenuItem") == 0:
        game.press(DOWN)
    game.wait(lambda: game.get("wCurrentMenuItem") == 1)
    game.tick(14)
    game.press(A)
    game.wait(lambda: "SWITCH" in game.visible_text())
    game.tick(14)
    game.press(A)
    advance_text_until(game, lambda: game.get("wPlayerMonNumber") == 1 and battle_ready(game))
    check_slot(2, 3)

    if enabled:
        # A copied monster's species must never change the awarded party member's curve.
        game.put("wBattleMonSpecies", (0x69,))
        game.put("wPlayerBattleStatus3", (1 << 3,))
        game.invoke("DrawPlayerHUDAndHPBar")
        game.return_to_stub()
        check_slot(2, 3)


def check_award(game, minimal, enabled):
    game.new_game()
    case = AwardCase(2, True, trainer=True, traded=0)
    seed_award(game, case)
    game.put("wBattleMonNick", name_bytes("BIRDA"))
    game.put("wBattleMonLevel", (50,))
    game.put("wBattleMonMaxHP", (0, 100))
    game.put("wMonHGrowthRate", (3,))  # Pidgey
    game.invoke("DrawPlayerHUDAndHPBar")
    game.return_to_stub()
    game.invoke("FaintEnemyPokemon")
    advance_text_until(game, lambda: game.cpu.pc == 0xc900)
    award, _ = next(expected_shares(case, minimal))
    total = START_EXP + award
    assert int.from_bytes(game.get_bytes("wPartyMon1Exp", 3), "big") == total
    expected = track(filled(3, 50, total)) if enabled else STOCK_BORDER
    assert rail(game) == expected, (rail(game), expected)
    assert rail(game, "wTileMapBackup") == expected


def check_visible_award(game, start_exp, enabled):
    game.new_game()
    seed_party(game)
    game.put("wOptions", (0xc1,))
    game.put("wPartyMon1Nick", name_bytes("VAPOREON"))
    game.put("wPartyMon1OTID", game.get_bytes("wPlayerID", 2))
    game.put("wPartyMon1Exp", start_exp.to_bytes(3, "big"))
    for field in ("BoxLevel", "Level"):
        game.put("wPartyMon1" + field, (8,))
    for field in ("Attack", "Speed"):
        game.put("wPartyMon1" + field, (0, 150))
    game.put("wPartyMon1Moves", (129, 0, 0, 0))  # Swift guarantees the KO.
    game.put("wPartyMon1PP", (20, 0, 0, 0))
    game.enter_map(ROUTE_1, 10, 5, 4)
    game.put("wCurOpponent", (PIDGEY,))
    game.put("wCurEnemyLevel", (2,))
    advance_text_until(game, lambda: battle_ready(game))

    def check_panel(level, xp):
        expected = track(filled(0, level, xp)) if enabled else STOCK_BORDER
        assert game.get("wBattleMonLevel") == level and rail(game) == expected
        # The battle window uses the second BG tilemap. Verify actual VRAM
        # while the message is on screen, before the next button press.
        size = C.c_size_t()
        vram = game.core.GB_get_direct_access(game.gb, 3, C.byref(size), None)
        assert C.string_at(vram + 0x1c00 + 11 * 32 + 10, 8) == expected

    game.tick(24)
    check_panel(8, start_exp)
    game.press(A)
    game.wait(lambda: "SWIFT" in game.visible_text())
    game.tick(16)
    game.press(A)
    game.wait(lambda: "gained" in game.visible_text(), accept=True)
    game.tick(20)
    total = start_exp + 15
    assert int.from_bytes(game.get_bytes("wPartyMon1Exp", 3), "big") == total
    check_panel(8, total)
    if total >= threshold(0, 9):
        game.wait(lambda: "grew" in game.visible_text(), accept=True)
        game.tick(20)
        check_panel(9, total)


def check_exclusions(game):
    for battle_type, link_state in ((1, 0), (2, 0), (0, 4)):
        game.put("wBattleType", (battle_type,))
        game.put("wLinkState", (link_state,))
        game.invoke("DrawPlayerHUDAndHPBar")
        game.return_to_stub()
        assert rail(game) == STOCK_BORDER, (battle_type, link_state, rail(game))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--color", choices=("red", "blue", "green"))
    args = parser.parse_args()
    for color in (args.color,) if args.color else ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        with Game(args.sameboy, args.boot, rom) as game:
            enabled = "DrawBattleExpMeter" in game.addresses
            check_wild_battle(game, enabled)
            check_exclusions(game)
        with Game(args.sameboy, args.boot, rom) as game:
            check_award(game, args.directory.name == "minimal", enabled)
            if enabled:
                check_math(game)
                check_authored_curve(game)
        if color == "red":
            for xp in (600, 728):
                with Game(args.sameboy, args.boot, rom) as game:
                    check_visible_award(game, xp, enabled)
        print(f"{args.directory.name} {color}: battle EXP meter and award checks passed", flush=True)


if __name__ == "__main__":
    main()
