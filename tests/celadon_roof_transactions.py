"""Exercise the Celadon roof vending machine and drink exchange through A/B controls."""

import argparse
from pathlib import Path

from adventure_checkpoints import event
from cartridge_smoke import Game
from shop_carry_count import bag


A, B, START, UP, DOWN = 4, 5, 7, 2, 3
ROOF, CELADON = 0x7E, 0x06
POTION = 0x14
DRINKS = (
    (0x3C, 200, "FRESH WATER", 0xD5, 0x18C),
    (0x3D, 300, "SODA POP", 0xF8, 0x18D),
    (0x3E, 350, "LEMONADE", 0xF9, 0x18E),
)


def money_bytes(value):
    return bytes.fromhex(f"{value:06d}")


def shows(game, *words, accept=False):
    game.wait(lambda: all(word in game.visible_text() for word in words), accept=accept)
    game.tick(14)


def select_row(game, row):
    for index in range(1, row + 1):
        game.press(DOWN)
        game.wait(lambda: game.get("wCurrentMenuItem") == index)
        game.tick(10)
    assert game.get("wCurrentMenuItem") == row
    game.press(A)


def finish(game, words):
    shows(game, *words, accept=True)
    game.wait(lambda: not game.get("wFontLoaded") & 1, accept=True)
    game.tick(12)


def enter_roof(game, x, y):
    game.new_game()
    game.put("wOptions", (1,))
    game.enter_map(ROOF, 10, x, y, last_map=CELADON)
    game.put("wSpritePlayerStateData1FacingDirection", (4,))


def setup_bag(game, stacks):
    game.put("wNumBagItems", bag(stacks))


def assert_bag(game, stacks):
    expected = bag(stacks)
    assert game.get_bytes("wNumBagItems", len(expected)) == expected


def vending_menu(game):
    game.press(A)
    shows(game, "FRESH WATER", "SODA POP", "LEMONADE", "CANCEL", accept=True)
    assert all(str(price) in game.visible_text() for _, price, *_ in DRINKS)
    assert game.get("wMaxMenuItem") == 3


def check_drink_info(game):
    setup_bag(game, [])
    game.put("wPlayerMoney", money_bytes(400))
    vending_menu(game)
    assert game.visible_text().splitlines()[16].strip() == "START INFO"
    game.press(START)
    for row, hp in enumerate((50, 60, 80)):
        if row:
            game.press(DOWN)
        _, price, name, *_ = DRINKS[row]
        shows(game, name, f"{hp} HP", "B BACK")
        lines = game.visible_text().splitlines()
        assert name in lines[12] and str(price) in lines[6 + 2 * row], lines
        assert game.get("wCurrentMenuItem") == row
    game.press(DOWN)  # CANCEL is outside the three-drink comparison.
    game.tick(18)
    game.press(A)
    shows(game, "LEMONADE", "80 HP")
    game.press(B)
    shows(game, "START INFO", "CANCEL")
    assert game.get("wCurrentMenuItem") == 2
    assert_bag(game, [])
    assert game.get_bytes("wPlayerMoney", 3) == money_bytes(400)
    game.press(DOWN)
    game.wait(lambda: game.get("wCurrentMenuItem") == 3)
    game.tick(24)
    assert "START INFO" not in game.visible_text()
    game.press(START)
    game.tick(30)
    assert "B BACK" not in game.visible_text()
    game.press(UP)
    shows(game, "START INFO")
    game.press(A)
    finish(game, ("popped out",))
    assert_bag(game, [(DRINKS[2][0], 1)])
    assert game.get_bytes("wPlayerMoney", 3) == money_bytes(50)


def check_vending(library, boot, rom, *, core):
    with Game(library, boot, rom) as game:
        enter_roof(game, 10, 2)
        check_drink_info(game)
        for row, (drink, price, _, _, _) in enumerate(DRINKS):
            for cash in (0, price - 1, price, price + 1):
                setup_bag(game, [])
                game.put("wPlayerMoney", money_bytes(cash))
                vending_menu(game)
                assert str(cash) in game.visible_text().splitlines()[1]
                select_row(game, row)
                required = price if core else 200
                if cash < required:
                    finish(game, ("not enough", "money"))
                    assert_bag(game, [])
                    assert game.get_bytes("wPlayerMoney", 3) == money_bytes(cash)
                else:
                    finish(game, ("popped out",))
                    assert_bag(game, [(drink, 1)])
                    assert game.get_bytes("wPlayerMoney", 3) == money_bytes(max(cash - price, 0))

        # A full bag can accept a drink only if a matching stack has room.
        for quantity in (None, 98, 99):
            existing = [(POTION, 1)] * (20 if quantity is None else 19)
            if quantity is not None:
                existing.append((DRINKS[0][0], quantity))
            setup_bag(game, existing)
            game.put("wPlayerMoney", money_bytes(400))
            vending_menu(game)
            select_row(game, 0)
            if quantity == 98:
                finish(game, ("popped out",))
                assert_bag(game, existing[:-1] + [(DRINKS[0][0], 99)])
                assert game.get_bytes("wPlayerMoney", 3) == money_bytes(200)
            else:
                finish(game, ("room for stuff",))
                assert_bag(game, existing)
                assert game.get_bytes("wPlayerMoney", 3) == money_bytes(400)

        vending_menu(game)
        game.press(B)
        finish(game, ("Not thirsty",))
        assert_bag(game, existing)
        assert game.get_bytes("wPlayerMoney", 3) == money_bytes(400)


def place_roof_girl(game):
    # Use the original object and script. Hold her at her initial map tile.
    game.put("wSprite02StateData2MapY", (9, 9))
    game.put("wSprite02StateData2MovementByte1", (0xFF,))
    game.put("wSprite02StateData2MovementDelay", (255,))
    game.put("wSprite02StateData1MovementStatus", (2, 0, 0, 44, 0, 64))
    game.tick(10)
    game.put("wSpritePlayerStateData1FacingDirection", (4,))


def offer_drink(game, name):
    game.press(A)
    shows(game, "YES", "NO", accept=True)
    game.press(A)
    shows(game, "Give her which", name)


def clear_rewards(game):
    byte, _ = divmod(DRINKS[0][4], 8)
    reward_bits = sum(1 << (spec[4] % 8) for spec in DRINKS)
    address = game.addresses["wEventFlags"][1] + byte
    game.write(address, (game.get("wEventFlags", byte) & ~reward_bits,))


def check_reward_repeat(game, original, name, reward_event):
    setup_bag(game, original)
    offer_drink(game, name)
    select_row(game, 0)
    finish(game, ("No thank you",))
    assert_bag(game, original)
    assert event(game, reward_event)


def check_exchange(library, boot, rom, *, core):
    with Game(library, boot, rom) as game:
        enter_roof(game, 5, 6)
        place_roof_girl(game)
        fillers = [(POTION, 1)] * 19
        for drink, _, name, tm, reward in DRINKS:
            clear_rewards(game)
            setup_bag(game, [(drink, 2)] + fillers)
            offer_drink(game, name)
            game.press(B)
            game.wait(lambda: not game.get("wFontLoaded") & 1)
            game.tick(12)
            assert_bag(game, [(drink, 2)] + fillers)
            assert not event(game, reward)

            offer_drink(game, name)
            select_row(game, 0)
            finish(game, ("space for this",))
            assert_bag(game, [(drink, 2 if core else 1)] + fillers)
            assert not event(game, reward)

            # Repeating a blocked trade preserves both drinks in Core.
            # The stock trade has one drink left, so the retry can succeed.
            offer_drink(game, name)
            select_row(game, 0)
            if core:
                finish(game, ("space for this",))
                assert_bag(game, [(drink, 2)] + fillers)
                assert not event(game, reward)
                setup_bag(game, [(drink, 2)] + fillers[:-1])
                offer_drink(game, name)
                select_row(game, 0)
                expected = [(drink, 1)] + fillers[:-1] + [(tm, 1)]
            else:
                expected = fillers + [(tm, 1)]
            finish(game, ("received",))
            assert_bag(game, expected)
            assert event(game, reward)
            check_reward_repeat(game, [(drink, 1), (tm, 1)], name, reward)

            # The last drink can free a slot in an otherwise full bag.
            clear_rewards(game)
            setup_bag(game, [(drink, 1)] + fillers)
            offer_drink(game, name)
            select_row(game, 0)
            finish(game, ("received",))
            assert_bag(game, fillers + [(tm, 1)])
            assert event(game, reward)

            # Existing TM stacks at 98 and 99 exercise the other capacity boundary.
            for quantity in (98, 99):
                clear_rewards(game)
                setup_bag(game, [(drink, 2), (tm, quantity)] + fillers[:-1])
                offer_drink(game, name)
                select_row(game, 0)
                finish(game, ("received",) if quantity == 98 else ("space for this",))
                assert_bag(game, [
                    (drink, 2 if core and quantity == 99 else 1), (tm, 99),
                ] + fillers[:-1])
                assert event(game, reward) == (quantity == 98)

        # All three drinks can be offered. Choosing Soda Pop changes only its trade.
        clear_rewards(game)
        setup_bag(game, [(spec[0], 2) for spec in DRINKS])
        offer_drink(game, "LEMONADE")
        select_row(game, 1)
        finish(game, ("received",))
        assert_bag(game, [(0x3C, 2), (0x3D, 1), (0x3E, 2), (0xF8, 1)])
        assert [event(game, spec[4]) for spec in DRINKS] == [False, True, False]

        game.invoke("SaveGameData")
        game.return_to_stub()
        clear_rewards(game)
        setup_bag(game, [])
        game.invoke("TryLoadSaveFile")
        game.return_to_stub()
        assert game.get("wSaveFileStatus") == 2
        assert event(game, DRINKS[1][4])
        saved_bag = [(0x3C, 2), (0x3D, 1), (0x3E, 2), (0xF8, 1)]
        assert_bag(game, saved_bag)
        game.enter_map(ROOF, 10, 5, 6, last_map=CELADON)
        place_roof_girl(game)
        offer_drink(game, "LEMONADE")
        select_row(game, 1)
        finish(game, ("No thank you",))
        assert_bag(game, saved_bag)
        assert event(game, DRINKS[1][4])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    core = args.directory.name == "core"
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        fixture = args.sameboy, args.boot, rom
        check_vending(*fixture, core=core)
        check_exchange(*fixture, core=core)
        print(f"{args.directory.name} {color}: Celadon roof transactions passed", flush=True)


if __name__ == "__main__":
    main()
