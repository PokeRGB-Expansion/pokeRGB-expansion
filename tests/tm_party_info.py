"""Inspect TMs at both Celadon counters, then buy or decline through the game."""

import argparse
import ctypes as C
from pathlib import Path

from cartridge_smoke import Game
from move_info_authoring import shows
from pc_browsing import name_bytes
from shop_carry_count import bag

DOWN, A, B, SELECT, START = 3, 4, 5, 6, 7
TM01, TM02, TM23, HM02, COIN_CASE = 0xc9, 0xca, 0xdf, 0xc5, 0x45
MEGA_PUNCH, DRAGON_RAGE = 0x05, 0x52
CELADON_MART_2F, GAME_CORNER_PRIZE_ROOM = 0x7b, 0x89

# The two traded-in moves deliberately include an otherwise ineligible Pidgey.
MEMBERS = (
    (0xb1, "TURTLE", 0x21),
    (0x85, "GOLDFISH", 0x21),
    (0x24, "LONGWINGER", MEGA_PUNCH),
    (0x15, "MYSTERY", 0x21),
    (0x58, "SERPENT", DRAGON_RAGE),
    (0x99, "CABBAGE", 0x21),
)


def press(game, key):
    game.tick(18)
    game.press(key)


def setup(game):
    game.new_game()
    game.put("wOptions", (0xc1,))
    game.put("wPartyCount", (len(MEMBERS),))
    game.put("wPartySpecies", (*[entry[0] for entry in MEMBERS], 0xff))
    for slot, (species, nick, move) in enumerate(MEMBERS, 1):
        game.put(f"wPartyMon{slot}Species", (species,))
        game.put(f"wPartyMon{slot}Moves", (move, 0, 0, 0))
        game.put(f"wPartyMon{slot}PP", (12, 0, 0, 0))
        game.put(f"wPartyMon{slot}HP", (0, 30))
        game.put(f"wPartyMon{slot}MaxHP", (0, 30))
        game.put(f"wPartyMon{slot}Nick", name_bytes(nick))
    game.put("wPlayerMoney", (1, 0, 0))  # 10,000
    game.put("wPlayerCoins", (0x50, 0))  # 5,000


def open_counter(game, prize, *, mart_row=5):
    if prize:
        game.enter_map(GAME_CORNER_PRIZE_ROOM, 5, 6, 3)
    else:
        game.enter_map(CELADON_MART_2F, 10, 6, 5)
    game.put("wSpritePlayerStateData1FacingDirection", (4,))
    press(game, A)
    if prize:
        shows(game, "TM23", "DRAGON RAGE", "START INFO", accept=True)
    else:
        shows(game, "BUY", "SELL", accept=True)
        press(game, A)
        shows(game, "TM32", "DOUBLE TEAM", "START INFO", accept=True)
        for _ in range(mart_row):
            press(game, DOWN)


def inspect(game, prize, *, duplicate=False):
    snapshot = {name: game.get_bytes(name, n) for name, n in (
        ("wNumBagItems", 42), ("wPlayerCoins", 2), ("wPlayerMoney", 3),
        ("wPartyMon1", 44 * 6), ("wCurPartySpecies", 1), ("wMonHeader", 28),
        ("wCurrentMenuItem", 1), ("wListScrollOffset", 1),
    )}
    name, detail = ("DRAGON RAGE", "Deals 40 damage") if prize else ("MEGA PUNCH", "Deals damage")
    press(game, START)
    if prize:
        shows(game, name, "DRAGON", "POW", "ACC100", "PP 10", "SELECT EFFECT")
        assert game.get("wTileMap", 14 * 20 + 5) == 0xe3  # no standard base power
    else:
        shows(game, name, "NORMAL", "POW  80", "ACC 85", "PP 20", "SELECT EFFECT")
    press(game, SELECT)
    shows(game, detail, "SELECT PARTY")
    press(game, SELECT)
    rows = (("UNABLE", "UNABLE", "UNABLE", "ABLE", "KNOWS", "UNABLE") if prize
            else ("UNABLE" if duplicate else "ABLE", "UNABLE", "KNOWS", "ABLE", "UNABLE", "UNABLE"))
    for start in (0, 3):
        shows(game, "SELECT MORE" if start == 0 else "SELECT STATS")
        screen = game.visible_text().splitlines()
        for rank in range(3):
            row = rank + start
            assert screen[13 + rank].split() == [MEMBERS[row][1], rows[row]], game.visible_text()
        press(game, SELECT)
    shows(game, name, "SELECT EFFECT")
    press(game, B)
    shows(game, "START INFO", name)
    for label, old in snapshot.items():
        assert game.get_bytes(label, len(old)) == old, label


def check_mart(game):
    setup(game)
    items = bag([(COIN_CASE, 1)])
    game.put("wNumBagItems", items)
    open_counter(game, False)
    shows(game, "TM01", "MEGA PUNCH", "START INFO")
    inspect(game, False)
    press(game, A)
    shows(game, "In bag", accept=True)
    press(game, B)
    shows(game, "MEGA PUNCH", "START INFO", accept=True)
    assert game.get_bytes("wPlayerMoney", 3) == bytes((1, 0, 0))
    press(game, A)
    shows(game, "In bag", accept=True)
    press(game, A)
    shows(game, "YES", "NO", accept=True)
    press(game, A)
    game.wait(lambda: game.get_bytes("wPlayerMoney", 3) == bytes((0, 0x70, 0)), accept=True)
    assert game.get_bytes("wNumBagItems", 6) == bag([(COIN_CASE, 1), (TM01, 1)])


def check_prize(game, *, full):
    setup(game)
    items = bag([(COIN_CASE, 1), *([(item, 1) for item in range(1, 20)] if full else [])])
    game.put("wNumBagItems", items)
    open_counter(game, True)
    inspect(game, True)
    press(game, A)
    shows(game, "YES", "NO", accept=True)
    press(game, A)
    if full:
        shows(game, "enough room", accept=True)
        assert game.get_bytes("wPlayerCoins", 2) == bytes((0x50, 0))
        assert game.get_bytes("wNumBagItems", len(items)) == items
    else:
        game.wait(lambda: game.get_bytes("wPlayerCoins", 2) == bytes((0x17, 0)), accept=True)
        assert game.get_bytes("wNumBagItems", 6) == bag([(COIN_CASE, 1), (TM23, 1)])


def check_duplicate(game):
    # TM02 and TM01 now both teach Mega Punch. Squirtle can learn only TM01.
    setup(game)
    size = C.c_size_t()
    base = game.core.GB_get_direct_access(game.gb, 0, C.byref(size), None)
    bank, address = game.addresses["TechnicalMachines"]
    tm02_move = C.c_uint8.from_address(base + bank * 0x4000 + address % 0x4000 + 1)
    tm02_move.value = MEGA_PUNCH
    items = bag([(TM02, 1)])
    game.put("wNumBagItems", items)
    game.invoke("StartMenu_Item")
    shows(game, "TM02", "MEGA PUNCH", "START INFO")
    inspect(game, False, duplicate=True)
    press(game, A)
    shows(game, "USE", accept=True)
    press(game, A)
    shows(game, "YES", "NO", accept=True)
    press(game, A)
    shows(game, "Use TM on which", "NOT ABLE", "KNOWS", accept=True)
    press(game, A)
    shows(game, "compatible with", accept=True)
    assert game.get_bytes("wNumBagItems", len(items)) == items
    assert game.get_bytes("wPartyMon1Moves", 4) == bytes((0x21, 0, 0, 0))

    # Mew is eligible for the second machine. Teach and consume just this TM.
    shows(game, "Use TM on which", "NOT ABLE", "KNOWS", accept=True)
    for _ in range(3):
        press(game, DOWN)
    press(game, A)
    game.wait(lambda: game.get("wNumBagItems") == 0, accept=True)
    assert game.get_bytes("wPartyMon4Moves", 4) == bytes((0x21, MEGA_PUNCH, 0, 0))
    assert game.get_bytes("wPartyMon4PP", 4) == bytes((12, 20, 0, 0))


def check_stored_hm(game, *, core, empty):
    setup(game)
    game.put("wPartyCount", (0 if empty else 1,))
    game.put("wPartySpecies", (0xff,) if empty else (0xb4, 0xff))
    game.put("wPartyMon1Species", (0xb4,))  # Charizard
    game.put("wPartyMon1Nick", name_bytes("CHARIZARD"))
    game.put("wNumBoxItems", bag([(HM02, 1)]))
    game.invoke("PlayerPCWithdraw")
    shows(game, "HM02", "FLY", "START INFO", accept=True)
    press(game, START)
    shows(game, "FLY", "FLYING", "SELECT EFFECT")
    press(game, SELECT)
    shows(game, "SELECT PARTY")
    press(game, SELECT)
    shows(game, "SELECT STATS")
    if empty:
        assert "No party" in game.visible_text()
    else:
        assert game.visible_text().splitlines()[13].split() == [
            "CHARIZARD", "ABLE" if core else "UNABLE"
        ]
    press(game, B)
    shows(game, "HM02", "START INFO")
    assert game.get_bytes("wNumBoxItems", 4) == bag([(HM02, 1)])


def check_counter_power(game):
    game.new_game()
    game.put("wNumBoxItems", bag([(0xda, 1)]))  # TM18
    game.invoke("PlayerPCWithdraw")
    shows(game, "TM18", "COUNTER", "START INFO", accept=True)
    press(game, START)
    shows(game, "COUNTER", "FIGHTING", "POW", "SELECT EFFECT")
    assert game.get("wTileMap", 14 * 20 + 5) == 0xe3
    press(game, SELECT)
    shows(game, "Returns double", "SELECT PARTY")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        cases = [check_mart, lambda game: check_prize(game, full=False)]
        if color == "red":
            cases += [
                lambda game: check_prize(game, full=True), check_duplicate, check_counter_power,
                lambda game: check_stored_hm(game, core=args.directory.name == "core", empty=False),
                lambda game: check_stored_hm(game, core=args.directory.name == "core", empty=True),
            ]
        for test in cases:
            with Game(args.sameboy, args.boot, rom) as game:
                test(game)
        print(f"{args.directory.name} {color}: inspected TMs before paying at both counters", flush=True)


if __name__ == "__main__":
    main()
