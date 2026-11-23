"""Check EXP. ALL protection and the Red Game Corner cash route."""

import argparse
from pathlib import Path

from cartridge_smoke import Game, seed_party

A, B, DOWN = 4, 5, 3
EXP_ALL = 0x4b
COIN_CASE = 0x45
PORYGON = 0xaa
ONE_EXP_ALL = bytes((1, EXP_ALL, 1, 0xff))


def shows(game, *words, accept=False):
    game.wait(lambda: all(word in game.visible_text() for word in words), accept=accept)


def check_disposal(game, core, inventory, refusal):
    if core:
        shows(game, refusal)
        assert game.get_bytes(inventory, 4) == ONE_EXP_ALL
    else:
        game.wait(lambda: game.get(inventory) == 0, accept=True)


def check_bag_toss(game, core):
    game.put("wNumBagItems", ONE_EXP_ALL)
    game.invoke("StartMenu_Item")
    shows(game, "EXP", "ALL")
    game.tick(12)
    game.press(A)
    shows(game, "USE", "TOSS")
    game.tick(8)
    game.press(DOWN)
    game.press(A)
    check_disposal(game, core, "wNumBagItems", "tant to toss")


def check_pc_toss(game, core):
    game.put("wNumBoxItems", ONE_EXP_ALL)
    game.invoke("PlayerPCToss")
    shows(game, "EXP", "ALL", accept=True)
    game.tick(12)
    game.press(A)
    check_disposal(game, core, "wNumBoxItems", "tant to toss")


def check_pc_storage(game, _core):
    game.put("wNumBagItems", ONE_EXP_ALL)
    game.put("wNumBoxItems", (0, 0xff))
    game.invoke("PlayerPCDeposit")
    shows(game, "EXP", "ALL", accept=True)
    game.tick(12)
    game.press(A)
    game.wait(lambda: game.get_bytes("wNumBoxItems", 4) == ONE_EXP_ALL
              and game.get("wNumBagItems") == 0, accept=True)

    # Start the item PC's Withdraw action with the same stored item.
    game.tick(150)
    game.invoke("PlayerPCWithdraw")
    shows(game, "EXP", "ALL", accept=True)
    game.tick(12)
    game.press(A)
    game.wait(lambda: game.get_bytes("wNumBagItems", 4) == ONE_EXP_ALL
              and game.get("wNumBoxItems") == 0, accept=True)


def check_shop_sale(game, core):
    game.put("wNumBagItems", ONE_EXP_ALL)
    money = game.get_bytes("wPlayerMoney", 3)
    game.invoke("DisplayPokemartDialogue_")
    shows(game, "BUY", "SELL")
    game.tick(12)
    game.press(DOWN)
    game.press(A)
    shows(game, "EXP", "ALL", accept=True)
    game.tick(12)
    game.press(A)
    check_disposal(game, core, "wNumBagItems", "price on that")
    assert game.get_bytes("wPlayerMoney", 3) == money


def check_hidden_coins(game, core):
    game.enter_map(0x87, 10, 4, 4)
    game.put("wNumBagItems", (1, COIN_CASE, 1, 0xff))
    for x, y, amount, before, after, spill in (
        (0, 8, 10, (0x99, 0x89), (0x99, 0x99), False),
        (1, 16, 10, (0x99, 0x90), (0x99, 0x99), True),
        (11, 7, 40, (0, 0), (0, 0x40 if core else 0x20), False),
    ):
        game.put("wPlayerCoins", before)
        game.put("wHiddenEventX", (x,))
        game.put("wHiddenEventY", (y,))
        game.put("wHiddenEventFunctionArgument", (0x3b + amount,))
        game.invoke("HiddenCoins")
        saw_spill = False
        for frame in range(250):
            saw_spill |= "Dropped" in game.visible_text()
            if game.cpu.pc == 0xc900:
                break
            if frame % 8 == 7:
                game.press(A)
            else:
                game.tick(2)
        else:
            raise AssertionError(game.visible_text())
        assert game.get_bytes("wPlayerCoins", 2) == bytes(after), (amount, before)
        assert saw_spill == spill, (amount, before, game.visible_text())

        game.put("wHiddenEventX", (x,))
        game.put("wHiddenEventY", (y,))
        game.put("wHiddenEventFunctionArgument", (0x3b + amount,))
        game.invoke("HiddenCoins")
        game.return_to_stub()
        assert game.get_bytes("wPlayerCoins", 2) == bytes(after)


def check_red_game_corner(game, _core):
    seed_party(game)
    game.put("wNumBagItems", (1, COIN_CASE, 1, 0xff))
    # 9,950 is the result of 199 ordinary purchases of 50 coins.
    game.put("wPlayerCoins", (0x99, 0x50))
    game.put("wPlayerMoney", (0x00, 0x15, 0x00))
    game.enter_map(0x87, 10, 4, 4)
    game.put("hTextID", (2,))
    game.invoke("DisplayTextID")
    shows(game, "YES", "NO", accept=True)
    game.press(A)
    shows(game, "50 coins")
    game.wait(lambda: game.cpu.pc == 0xc900, accept=True)
    assert game.get_bytes("wPlayerCoins", 2) == bytes((0x99, 0x99))
    assert game.get_bytes("wPlayerMoney", 3) == bytes((0x00, 0x05, 0x00))

    game.enter_map(0x89, 5, 4, 3, last_map=0x87)
    game.put("hTextID", (4,))
    game.invoke("DisplayTextID")
    shows(game, "PORYGON", "9999", accept=True)
    game.tick(18)
    game.press(DOWN)
    game.press(DOWN)
    game.press(A)
    shows(game, "YES", "NO", accept=True)
    game.press(A)
    for frame in range(200):
        if game.cpu.pc == 0xc900:
            break
        if "nickname" in game.visible_text():
            game.press(B)
        elif frame % 4 == 3:
            game.press(A)
        else:
            game.tick(4)
    else:
        raise AssertionError(game.visible_text())

    assert game.get("wPartyCount") == 3
    assert game.get("wPartyMon3Species") == PORYGON
    assert game.get_bytes("wPlayerCoins", 2) == bytes((0, 0))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    core = args.directory.name == "core"
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        checks = [check_bag_toss, check_pc_toss, check_pc_storage, check_shop_sale]
        if color == "red":
            checks.append(check_red_game_corner)
        for check in checks:
            with Game(args.sameboy, args.boot, rom) as game:
                game.new_game()
                check(game, core)
            print(f"{args.directory.name} {color}: {check.__name__.removeprefix('check_')} passed",
                  flush=True)
        with Game(args.sameboy, args.boot, rom) as game:
            game.new_game()
            check_hidden_coins(game, core)
        print(f"{args.directory.name} {color}: hidden coin awards and messages passed", flush=True)


if __name__ == "__main__":
    main()
