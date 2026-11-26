"""Inspect ordinary supplies and move traits through the original menus."""

import argparse
import ctypes as C
from pathlib import Path

from battle_stats_return import start_battle, battle_ready
from cartridge_smoke import Game
from move_info_authoring import shows

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
        shows(game, name, label, "SELECT EFFECT")
        if index == 2 and not custom:
            assert "HIGH CRIT" not in game.visible_text()
        press(game, SELECT)
        shows(game, description, "SELECT STATS")
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
        if color == "red":
            with Game(args.sameboy, args.boot, rom) as game:
                moves(game, custom=True)
        print(f"{args.directory.name} {color}: supply and move-trait INFO passed", flush=True)


if __name__ == "__main__":
    main()
