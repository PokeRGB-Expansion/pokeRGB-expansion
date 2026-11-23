"""Read the Bag, item PC, and active box counts on the linked cartridge."""

import argparse
from pathlib import Path

from adventure_checkpoints import A, advance_text_until, shows
from cartridge_smoke import Game, seed_party


B, START = 5, 7
BAG_CAPACITY = 20
ITEM_PC_CAPACITY = 50
BOX_CAPACITY = 20
TM24 = 0xE0
POTION = 0x14


def tile_bytes(label):
    tiles = {" ": 0x7F, "/": 0xF3}
    tiles.update({chr(65 + index): 0x80 + index for index in range(26)})
    tiles.update({str(index): 0xF6 + index for index in range(10)})
    return bytes(tiles[character] for character in label)


def count_visible(game, x, y, label, occupied, limit):
    expected = tile_bytes(f"{label} {occupied:2}/{limit:2}")
    offset = y * 20 + x
    return bytes(game.get("wTileMap", offset + index) for index in range(len(expected))) == expected


def expect_count(game, x, y, label, occupied, limit, *, accept=False):
    game.wait(lambda: count_visible(game, x, y, label, occupied, limit), accept=accept)


def put_item_list(game, label, count, first=TM24):
    items = (first, 1) + (POTION, 1) * max(count - 1, 0) if count else ()
    data = bytes((count, *items, 0xFF))
    game.put(label, data)
    return data


def check_bag(game, count):
    bag = put_item_list(game, "wNumBagItems", count)
    game.invoke("StartMenu_Item")
    expect_count(game, 5, 3, "BAG", count, BAG_CAPACITY)
    if count:
        shows(game, "TM24", "THUNDERBOLT", "START INFO")
        game.tick(12)
        game.press(START)
        shows(game, "ELECTRIC", "SELECT EFFECT")
        game.press(B)
        expect_count(game, 5, 3, "BAG", count, BAG_CAPACITY)
        shows(game, "THUNDERBOLT", "START INFO")
    else:
        shows(game, "CANCEL")
    assert game.get_bytes("wNumBagItems", len(bag)) == bag


def check_item_pc(game, count):
    bag = put_item_list(game, "wNumBagItems", BAG_CAPACITY - 1)
    pc = put_item_list(game, "wNumBoxItems", count)
    game.invoke("PlayerPC")
    advance_text_until(game, lambda: count_visible(game, 2, 1, "ITEM PC", count, ITEM_PC_CAPACITY))
    shows(game, "WITHDRAW ITEM", "DEPOSIT ITEM", "TOSS ITEM", accept=True)
    game.tick(20)
    if count:
        game.press(A)
        expect_count(game, 5, 3, "ITEM PC", count, ITEM_PC_CAPACITY, accept=True)
        shows(game, "THUNDERBOLT", "START INFO")
        game.tick(20)
        game.press(B)
        expect_count(game, 2, 1, "ITEM PC", count, ITEM_PC_CAPACITY)
        shows(game, "WITHDRAW ITEM", "DEPOSIT ITEM")
    else:
        game.press(A)
        advance_text_until(game, lambda: "stored" in game.visible_text())
        expect_count(game, 2, 1, "ITEM PC", 0, ITEM_PC_CAPACITY, accept=True)
    assert game.get_bytes("wNumBoxItems", len(pc)) == pc
    assert game.get_bytes("wNumBagItems", len(bag)) == bag
    if count == ITEM_PC_CAPACITY - 1:
        game.invoke("PlayerPCDeposit")
        expect_count(game, 5, 3, "BAG", BAG_CAPACITY - 1, BAG_CAPACITY, accept=True)
        shows(game, "THUNDERBOLT", "START INFO")
        game.tick(20)
        game.press(B)
        shows(game, "DEPOSIT ITEM", "TOSS ITEM")
        game.invoke("PlayerPCToss")
        expect_count(game, 5, 3, "ITEM PC", count, ITEM_PC_CAPACITY, accept=True)
        shows(game, "THUNDERBOLT", "START INFO")
        game.tick(20)
        game.press(B)
        shows(game, "DEPOSIT ITEM", "TOSS ITEM")
        assert game.get_bytes("wNumBoxItems", len(pc)) == pc
        assert game.get_bytes("wNumBagItems", len(bag)) == bag
    if count == ITEM_PC_CAPACITY:
        game.tick(20)
        game.press(A)
        expect_count(game, 5, 3, "ITEM PC", count, ITEM_PC_CAPACITY, accept=True)
        game.tick(20)
        game.press(A)
        shows(game, "How many", accept=True)
        game.tick(30)
        game.press(A)
        advance_text_until(game, lambda: "Withdrew" in game.visible_text())
        expect_count(game, 5, 3, "ITEM PC", count - 1, ITEM_PC_CAPACITY, accept=True)
        assert game.get_bytes("wNumBagItems", len(bag)) == bag[:2] + b"\x02" + bag[3:]
        assert game.get_bytes("wNumBoxItems", len(pc) - 2) == bytes((count - 1,)) + pc[3:]


def put_box(game, count):
    game.put("wBoxCount", (count, *(0x69,) * count, 0xFF))
    for position in range(1, count + 1):
        game.put(f"wBoxMon{position}Nick", (0x93, 0x84, 0x92, 0x93, 0x50))
        game.put(f"wBoxMon{position}BoxLevel", (10,))


def check_mon_box(game, count):
    seed_party(game)
    put_box(game, count)
    size = game.addresses["wBoxDataEnd"][1] - game.addresses["wBoxDataStart"][1]
    box = game.get_bytes("wBoxCount", size)
    game.invoke("BillsPC_")
    advance_text_until(game, lambda: count_visible(game, 2, 1, "BOX", count, BOX_CAPACITY))
    shows(game, "WITHDRAW", "DEPOSIT")
    game.tick(20)
    if count:
        game.press(A)
        expect_count(game, 5, 3, "BOX", count, BOX_CAPACITY)
        shows(game, "TEST")
        game.tick(20)
        game.press(B)
        expect_count(game, 2, 1, "BOX", count, BOX_CAPACITY)
        shows(game, "DEPOSIT", "RELEASE")
    else:
        game.press(A)
        advance_text_until(game, lambda: "here" in game.visible_text())
        expect_count(game, 2, 1, "BOX", 0, BOX_CAPACITY, accept=True)
    assert game.get_bytes("wBoxCount", size) == box
    assert game.get("wPartyCount") == 2
    if count == BOX_CAPACITY:
        game.invoke("BillsPCDeposit")
        advance_text_until(game, lambda: "This Box is" in game.visible_text()
                           and "full of" in game.visible_text())
        expect_count(game, 2, 1, "BOX", count, BOX_CAPACITY, accept=True)
        assert game.get_bytes("wBoxCount", size) == box
        assert game.get("wPartyCount") == 2


def check_shop(game):
    bag = put_item_list(game, "wNumBagItems", BAG_CAPACITY)
    game.put("wItemList", (1, TM24, 0xFF))
    game.invoke("DisplayPokemartDialogue_")
    shows(game, "BUY", "SELL")
    game.press(A)
    shows(game, "TM24", "THUNDERBOLT", "START INFO", "2000", accept=True)
    assert game.visible_text().splitlines()[3][5:19] == " " * 14
    assert game.get_bytes("wNumBagItems", len(bag)) == bag


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        cartridge = args.directory / f"poke{color}.gbc"
        for check, limit in ((check_bag, BAG_CAPACITY), (check_item_pc, ITEM_PC_CAPACITY),
                             (check_mon_box, BOX_CAPACITY)):
            for count in (0, limit - 1, limit):
                with Game(args.sameboy, args.boot, cartridge) as game:
                    game.new_game()
                    check(game, count)
        with Game(args.sameboy, args.boot, cartridge) as game:
            game.new_game()
            check_shop(game)
        print(f"{cartridge}: Bag, item PC, and active box capacity menus passed", flush=True)


if __name__ == "__main__":
    main()
