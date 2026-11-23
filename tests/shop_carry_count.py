"""Check the Mart's carried count and normal purchase controls."""

import argparse
import re
from pathlib import Path

from cartridge_smoke import Game


RIGHT, DOWN, A, B = 0, 3, 4, 5
POTION, POKE_BALL = 0x14, 4


def bag(stacks):
    return bytes((len(stacks), *(value for pair in stacks for value in pair), 0xFF))


def shows(game, *words, accept=False):
    game.wait(lambda: all(word in game.visible_text() for word in words), accept=accept)


def show_quantity(game, count):
    game.press(A)
    shows(game, "In bag", accept=True)
    game.wait(lambda: game.get("wItemQuantity") == 1)
    digits = re.search(r"In bag\s+(\d+)", game.visible_text())
    assert digits and int(digits[1]) == count, game.visible_text()
    assert game.get("wMaxItemQuantity") == 99
    assert game.get_bytes("hMoney", 3) == bytes((0, 0x03, 0))  # Potion costs 300.


def confirm(game):
    game.press(A)
    shows(game, "YES", "NO", accept=True)
    game.press(A)


def check_mart(game):
    game.new_game()
    game.put("wOptions", (1,))
    game.put("wItemList", (1, POTION, 0xFF))
    game.put("wNumBoxItems", bag([(POTION, 99)]))
    game.put("wPlayerMoney", (0, 0x50, 0))  # 5,000
    game.invoke("DisplayPokemartDialogue_")
    shows(game, "BUY", "SELL")
    game.press(A)
    shows(game, "POTION", "Take your time", accept=True)
    game.tick(15)

    for amounts in ((), (1,), (99,), (99, 1), (99, 3), (99,) * 20):
        expected = bag([(POTION, amount) for amount in amounts])
        game.put("wNumBagItems", expected)
        show_quantity(game, sum(amounts))
        game.press(B)
        game.wait(lambda: "In bag" not in game.visible_text())
        game.tick(15)
        assert game.get_bytes("wNumBagItems", len(expected)) == expected

    expected = bag([(POKE_BALL, 1)] * 20)
    game.put("wNumBagItems", expected)
    show_quantity(game, 0)
    confirm(game)
    shows(game, "any more items")
    assert game.get_bytes("wNumBagItems", len(expected)) == expected
    assert game.get_bytes("wPlayerMoney", 3) == bytes((0, 0x50, 0))
    shows(game, "POTION", "Take your time", accept=True)
    game.tick(15)

    expected = bag([(POTION, 99), (POTION, 3)])
    game.put("wNumBagItems", expected)
    show_quantity(game, 102)
    game.press(RIGHT)
    game.wait(lambda: game.get("wItemQuantity") == 11)
    assert game.get_bytes("hMoney", 3) == bytes((0, 0x33, 0))
    confirm(game)
    game.wait(lambda: game.get_bytes("wPlayerMoney", 3) == bytes((0, 0x17, 0)), accept=True)
    assert game.get_bytes("wNumBagItems", 6) == bag([(POTION, 99), (POTION, 14)])
    assert game.get_bytes("wNumBoxItems", 4) == bag([(POTION, 99)])
    shows(game, "POTION", "Take your time", accept=True)
    game.tick(15)

    show_quantity(game, 113)
    game.press(RIGHT)
    game.wait(lambda: game.get("wItemQuantity") == 11)
    confirm(game)
    shows(game, "enough money")
    assert game.get_bytes("wPlayerMoney", 3) == bytes((0, 0x17, 0))
    assert game.get_bytes("wNumBagItems", 6) == bag([(POTION, 99), (POTION, 14)])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        with Game(args.sameboy, args.boot, rom) as game:
            check_mart(game)
        print(f"{color.title()}: Mart carry count and purchases passed", flush=True)


if __name__ == "__main__":
    main()
