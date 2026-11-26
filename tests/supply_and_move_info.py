"""Inspect ordinary supplies and move traits through the original menus."""

import argparse
import ctypes as C
from pathlib import Path

from adventure_checkpoints import advance_text_until
from battle_stats_return import start_battle, battle_ready
from cgb_compatibility import start_menu_row
from cartridge_smoke import Game
from move_info_authoring import shows
from sprite_storage import direct_access
from tm_inspection_controls import PARTY, seed_six

A, B, SELECT, START, DOWN = 4, 5, 6, 7, 3
POTION, SUPER_REPEL, LIFT_KEY = 0x14, 0x38, 0x4A
QUICK_ATTACK, SLASH, POISON_STING = 0x62, 0xA3, 0x28


def press(game, button):
    game.tick(15)
    game.press(button)


def supplies(game, location):
    game.new_game()
    stock = bytes((3, POTION, SUPER_REPEL, LIFT_KEY, 0xff))
    bag = bytes((3, POTION, 7, SUPER_REPEL, 2, LIFT_KEY, 1, 0xff))
    game.put("wNumBagItems", bag)
    money = game.get_bytes("wPlayerMoney", 3)
    if location == "shop":
        game.put("wItemList", stock)
        game.invoke("DisplayPokemartDialogue_")
        shows(game, "BUY", "SELL")
        game.press(A)
        shows(game, "POTION", "START INFO", accept=True)
    elif location == "pc":
        game.put("wNumBoxItems", bag)
        game.invoke("PlayerPCWithdraw")
        shows(game, "POTION", "START INFO", accept=True)
    else:
        game.invoke("StartMenu_Item")
        shows(game, "POTION", "START INFO")
    for index, (name, text) in enumerate((("POTION", "20 HP"), ("SUPER REPEL", "200 steps"))):
        if index:
            press(game, DOWN)
        game.wait(lambda: game.get("wCurrentMenuItem") == index)
        offset = game.get("wListScrollOffset")
        press(game, START)
        shows(game, name, text, "B BACK")
        press(game, B)
        shows(game, "START INFO")
        assert game.get("wCurrentMenuItem") == index and game.get("wListScrollOffset") == offset
    press(game, DOWN)
    game.wait(lambda: game.get("wCurrentMenuItem") == 2)
    assert "START INFO" not in game.visible_text()
    press(game, START)
    game.tick(20)
    assert "B BACK" not in game.visible_text()
    assert game.get_bytes("wNumBagItems", len(bag)) == bag
    assert game.get_bytes("wPlayerMoney", 3) == money
    if location == "pc":
        assert game.get_bytes("wNumBoxItems", len(bag)) == bag


def stone_party(game, *, custom=False):
    seed_six(game)
    if custom:
        # A hack can give Eevee a level requirement. The shelf and the Bag
        # must both read the edited rule. The next stone is still usable.
        rom = direct_access(game, 0)
        bank, address = game.addresses["EeveeEvosMoves"]
        start = bank * 0x4000 + address % 0x4000
        assert bytes(rom[start + 1:start + 3]) == bytes((0x20, 1))
        rom[start + 2] = 29  # The party's Eevee is level 28.
    game.enter_map(0x7d, 10, 5, 5)  # Face the fourth-floor shopkeeper.
    game.put("wSpritePlayerStateData1FacingDirection", (0,))
    press(game, A)
    shows(game, "BUY", "SELL", accept=True)
    press(game, A)
    shows(game, "FIRE STONE", "THUNDERSTONE", accept=True)
    press(game, DOWN)
    shows(game, "START INFO", "FIRE STONE")
    before = {key: game.get_bytes(key, size) for key, size in (
        ("wPlayerMoney", 3), ("wNumBagItems", 42), ("wPartyMon1", 44 * 6),
        ("wPartySpecies", 7), ("wPartyMonNicks", 11 * 6),
    )}
    press(game, START)
    shows(game, "Evolves certain", "A PARTY", "B BACK")
    press(game, A)

    def check_party(name, eevee_can_evolve, *, shop=True):
        expected_words = (name, "2100", "B BACK") if shop else ("Use item",)
        shows(game, "EEVEE", "PIDGEOTTO", *expected_words)
        rows = game.visible_text().splitlines()
        for slot, (_, nickname, _) in enumerate(PARTY):
            assert nickname in rows[slot * 2], rows
            expected = "ABLE" if nickname == "EEVEE" and eevee_can_evolve else "NOT ABLE"
            assert rows[slot * 2 + 1].strip() == expected, rows

    check_party("FIRE STONE", not custom)
    press(game, 2)  # At the first stone, Up must leave the unrelated Doll alone.
    check_party("FIRE STONE", not custom)
    press(game, DOWN)
    check_party("THUNDERSTONE", True)
    press(game, DOWN)
    check_party("WATER STONE", True)
    press(game, DOWN)
    check_party("LEAF STONE", False)
    press(game, DOWN)
    check_party("LEAF STONE", False)
    press(game, A)  # PARTY is read-only. A cannot evolve or buy anything.
    check_party("LEAF STONE", False)
    press(game, B)
    shows(game, "LEAF STONE", "START INFO", "2100")
    assert game.get("wListScrollOffset") + game.get("wCurrentMenuItem") == 4
    press(game, START)
    press(game, 2)
    press(game, 2)
    press(game, 2)
    shows(game, "Evolves certain", "A PARTY")
    press(game, B)
    shows(game, "START INFO", "FIRE STONE")
    assert game.get("wListScrollOffset") + game.get("wCurrentMenuItem") == 1
    for key, value in before.items():
        assert game.get_bytes(key, len(value)) == value, key
    press(game, A)
    shows(game, "In bag", accept=True)
    press(game, A)
    shows(game, "YES", "NO", accept=True)
    press(game, A)
    game.wait(lambda: game.get_bytes("wPlayerMoney", 3) == bytes((0, 0x79, 0)), accept=True)
    assert game.get_bytes("wNumBagItems", 4) == bytes((1, 0x20, 1, 0xff))
    # Enter the Bag normally after leaving the shop. Only USE may select a target.
    for _ in range(50):
        if not game.get("wFontLoaded") & 1:
            break
        press(game, B)
    else:
        raise AssertionError("Could not leave the Mart after buying the stone.")
    start_menu_row(game, 1)
    shows(game, "FIRE STONE", "START INFO")
    press(game, A)
    shows(game, "USE")
    press(game, A)
    check_party("FIRE STONE", not custom, shop=False)
    for _ in range(4):
        press(game, DOWN)
    assert game.get("wCurrentMenuItem") == 4
    press(game, A)
    if custom:
        shows(game, "effect", accept=True)
        assert game.get("wPartyMon5Species") == 0x66  # Eevee is below the edited level requirement.
        assert game.get_bytes("wNumBagItems", 4) == bytes((1, 0x20, 1, 0xff))
    else:
        advance_text_until(game, lambda: game.get("wPartyMon5Species") == 0x67
                           and game.get("wNumBagItems") == 0)  # Flareon, one stone spent.


def moves(game, *, custom=False):
    if custom:
        # Model an author replacing Karate Chop with Poison Sting in the actual battle list.
        size = C.c_size_t()
        base = game.core.GB_get_direct_access(game.gb, 0, C.byref(size), None)
        bank, address = game.addresses["HighCriticalMoves"]
        entry = C.c_uint8.from_address(base + bank * 0x4000 + address % 0x4000)
        assert entry.value == 2
        entry.value = POISON_STING
    start_battle(game, tower=False, scoped=False)
    slots = (QUICK_ATTACK, SLASH, POISON_STING, 0)
    pp = bytes((20, 15, 10, 0))
    game.put("wBattleMonMoves", slots)
    game.put("wBattleMonPP", pp)
    press(game, A)
    cases = (("QUICK ATTACK", "PRIORITY", "Goes before"),
             ("SLASH", "HIGH CRIT", "critical hit"),
             ("POISON STING", "HIGH CRIT" if custom else "POISON", "May poison"))
    for index, (name, label, description) in enumerate(cases):
        if index:
            press(game, DOWN)
        shows(game, "START INFO")
        press(game, START)
        shows(game, name, label, "SEL EFFECT")
        if index == 2 and not custom:
            assert "HIGH CRIT" not in game.visible_text()
        press(game, SELECT)
        shows(game, description, "SEL STATS")
        press(game, B)
        shows(game, "START INFO")
    press(game, B)
    game.wait(lambda: battle_ready(game))
    assert game.get_bytes("wBattleMonPP", 4) == pp


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        for location in ("bag", "shop", "pc"):
            with Game(args.sameboy, args.boot, rom) as game:
                supplies(game, location)
        with Game(args.sameboy, args.boot, rom) as game:
            moves(game)
        with Game(args.sameboy, args.boot, rom) as game:
            stone_party(game, custom=color == "blue")
        if color == "red":
            with Game(args.sameboy, args.boot, rom) as game:
                moves(game, custom=True)
        print(f"{args.directory.name} {color}: supply and move-trait INFO passed", flush=True)


if __name__ == "__main__":
    main()
