"""Check Bike Shop exit paths and the sign between Routes 16 and 17."""

import argparse
from pathlib import Path

from cartridge_smoke import Game

A, B, DOWN = 4, 5, 3
BIKE_VOUCHER = 0x2d
BICYCLE = 0x06
NO_TEXT_DELAY = 1 << 6


def check_bike_shop(game, choice, speed):
    game.put("wOptions", (speed,))
    game.put("wStatusFlags5", (game.get("wStatusFlags5") & ~NO_TEXT_DELAY,))
    if choice == "voucher":
        game.put("wNumBagItems", (1, BIKE_VOUCHER, 1, 0xff))
    money = game.get_bytes("wPlayerMoney", 3)
    game.put("hTextID", (1,))
    game.invoke("DisplayTextID")
    if choice != "voucher":
        game.wait(lambda: "CANCEL" in game.visible_text() and "want it" in game.visible_text(),
                  accept=True)
        game.tick(30)
        if choice == "B":
            game.press(B)
        else:
            if choice == "cancel":
                game.press(DOWN)
            game.press(A)
    game.wait(lambda: game.cpu.pc == 0xc900, accept=True)
    assert game.get("wStatusFlags5") & NO_TEXT_DELAY == 0, (choice, speed)
    assert game.get("wOptions") == speed
    assert game.get_bytes("wPlayerMoney", 3) == money
    if choice == "voucher":
        assert game.get_bytes("wNumBagItems", 4) == bytes((1, BICYCLE, 1, 0xff))


def check_route_sign(game):
    for map_id, width, x, y, direction in (
        (0x1b, 20, 5, 16, 0),
        (0x1b, 20, 4, 17, 0x0c),
        (0x1b, 20, 6, 17, 0x08),
        (0x1c, 10, 5, 0, 0x04),
    ):
        game.enter_map(map_id, width, x, y)
        # The downhill script can move the rider while the map loads.
        game.put("wYCoord", (y, x, y % 2, x % 2))
        game.put("wSpritePlayerStateData1FacingDirection", (direction,))
        game.invoke("IsSpriteOrSignInFrontOfPlayer")
        game.return_to_stub()
        assert game.get("hTextID"), (map_id, x, y, direction)

        game.invoke("DisplayTextID")
        game.wait(lambda: "FUCHSIA CITY" in game.visible_text(), accept=True)
        game.wait(lambda: game.cpu.pc == 0xc900, accept=True)

    game.put("wSpritePlayerStateData1FacingDirection", (0,))
    game.invoke("IsSpriteOrSignInFrontOfPlayer")
    game.return_to_stub()
    assert game.get("hTextID") == 0


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
            game.enter_map(0x42, 4, 4, 4, last_map=3)
            for speed in (1, 3, 5):
                for choice in ("B", "cancel", "refuse"):
                    check_bike_shop(game, choice, speed)
            check_bike_shop(game, "voucher", 3)
            check_route_sign(game)
        print(f"{args.directory.name} {color}: Bike Shop and Route 16 sign passed", flush=True)


if __name__ == "__main__":
    main()
