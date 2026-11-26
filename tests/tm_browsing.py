"""Compare machines without leaving INFO, then buy the offer on screen."""
import argparse
from pathlib import Path

from cartridge_smoke import Game
from move_info_authoring import shows
from shop_carry_count import bag
from tm_party_info import A, B, COIN_CASE, DOWN, SELECT, START, open_counter, press, setup


UP = 2
TM01 = 0xc9


def position(game):
    return game.get("wCurrentMenuItem"), game.get("wListScrollOffset")


def offer(game, name, number, price, *, prize=False):
    shows(game, name)
    screen = game.visible_text().splitlines()
    row = 4 + 2 * game.get("wCurrentMenuItem")
    assert f"TM{number:02}" in screen[row], screen
    assert str(price) in screen[row + 1], screen
    arrow = 1 if prize else 5
    assert game.get("wTileMap", 20 * row + arrow) == 0xED, screen  # ▶


def party_offer(game, name, number, price, *, prize=False):
    shows(game, name, "CABBAGE")
    lines = game.visible_text().splitlines()
    assert lines[13].strip() == f"TM{number:02} {name}", lines
    assert lines[14].strip() == (f"{price} COINS" if prize else str(price)), lines
    prefix = game.get("wTileMap", 20 * 14 + 1)
    assert (prefix == 0xF0) == (not prize), lines  # ¥ at a Mart


def hold(game, key, frames):
    game.core.GB_set_key_state(game.gb, key, True)
    game.tick(frames)
    game.core.GB_set_key_state(game.gb, key, False)
    game.tick(12)


def check_mart(game):
    setup(game)
    contents = bag([(COIN_CASE, 1)])
    game.put("wNumBagItems", contents)
    open_counter(game, False, mart_row=0)
    press(game, START)
    offer(game, "DOUBLE TEAM", 32, 1000)
    press(game, UP)
    assert position(game) == (0, 0)
    hold(game, DOWN, 18)  # before the ordinary half-second repeat delay
    offer(game, "REFLECT", 33, 1000)
    assert position(game) == (1, 0)
    press(game, UP)
    offer(game, "DOUBLE TEAM", 32, 1000)
    # A tap advances one machine. Stay on the effect page across a scroll.
    press(game, SELECT)
    shows(game, "Raises Evasion")
    for number, name, price, detail in (
        (33, "REFLECT", 1000, "Doubles physical"),
        (2, "RAZOR WIND", 2000, "Charges on turn 1"),
        (7, "HORN DRILL", 2000, "Knocks out the foe"),
    ):
        press(game, DOWN)
        offer(game, name, number, price)
        shows(game, detail)
    assert position(game) == (2, 1)
    press(game, A)
    party_offer(game, "HORN DRILL", 7, 2000)
    press(game, DOWN)
    party_offer(game, "EGG BOMB", 37, 2000)
    press(game, DOWN)
    party_offer(game, "MEGA PUNCH", 1, 3000)
    press(game, B)
    shows(game, "MEGA PUNCH", "START INFO")
    press(game, START)
    shows(game, "NORMAL", "POW", "PP")
    hold(game, DOWN, 125)
    offer(game, "SUBMISSION", 17, 3000)
    assert position(game) == (2, 6)
    press(game, DOWN)
    assert position(game) == (2, 6)
    assert game.get_bytes("wNumBagItems", len(contents)) == contents
    assert game.get_bytes("wPlayerMoney", 3) == bytes((1, 0, 0))
    # B with a direction held must not move the ordinary shop cursor.
    game.core.GB_set_key_state(game.gb, B, True)
    game.core.GB_set_key_state(game.gb, UP, True)
    game.tick(16)
    game.core.GB_set_key_state(game.gb, B, False)
    game.tick(36)
    game.core.GB_set_key_state(game.gb, UP, False)
    shows(game, "SUBMISSION", "START INFO", "CANCEL")
    assert position(game) == (2, 6)
    press(game, A)
    shows(game, "In bag", accept=True)
    press(game, A)
    shows(game, "YES", "NO", accept=True)
    press(game, A)
    game.wait(lambda: game.get_bytes("wPlayerMoney", 3) == bytes((0, 0x70, 0)), accept=True)
    assert game.get_bytes("wNumBagItems", 6) == bag([(COIN_CASE, 1), (TM01 + 16, 1)])


def check_prize(game):
    setup(game)
    game.put("wPlayerCoins", (0x80, 0))
    contents = bag([(COIN_CASE, 1)])
    game.put("wNumBagItems", contents)
    open_counter(game, True)
    press(game, START)
    offer(game, "DRAGON RAGE", 23, 3300, prize=True)
    press(game, SELECT)
    shows(game, "Deals 40 damage")
    press(game, DOWN)
    offer(game, "HYPER BEAM", 15, 5500, prize=True)
    shows(game, "Rest a turn")
    press(game, DOWN)
    offer(game, "SUBSTITUTE", 50, 7700, prize=True)
    hold(game, DOWN, 50)
    offer(game, "SUBSTITUTE", 50, 7700, prize=True)
    press(game, UP)
    offer(game, "HYPER BEAM", 15, 5500, prize=True)
    press(game, A)
    party_offer(game, "HYPER BEAM", 15, 5500, prize=True)
    press(game, UP)
    party_offer(game, "DRAGON RAGE", 23, 3300, prize=True)
    shows(game, "SERPENT", "KNOWS")
    press(game, DOWN)
    party_offer(game, "HYPER BEAM", 15, 5500, prize=True)
    press(game, DOWN)
    party_offer(game, "SUBSTITUTE", 50, 7700, prize=True)
    press(game, A)
    shows(game, "SUBSTITUTE", "CABBAGE")  # party comparison is read-only
    press(game, B)
    shows(game, "SUBSTITUTE", "START INFO", "THANKS")
    assert game.get("wCurrentMenuItem") == 2
    assert game.get_bytes("wPlayerCoins", 2) == bytes((0x80, 0))
    assert game.get_bytes("wNumBagItems", len(contents)) == contents
    press(game, A)
    shows(game, "YES", "NO", accept=True)
    press(game, A)
    game.wait(lambda: game.get_bytes("wPlayerCoins", 2) == bytes((0x03, 0)), accept=True)
    assert game.get_bytes("wNumBagItems", 6) == bag([(COIN_CASE, 1), (TM01 + 49, 1)])


def check_mixed_shop(game):
    setup(game)
    game.put("wItemList", (5, TM01, 0x14, 0x38, 0x14, TM01 + 4, 0xff))
    game.invoke("DisplayPokemartDialogue_")
    shows(game, "BUY", "SELL")
    press(game, A)
    shows(game, "MEGA PUNCH", "START INFO", accept=True)
    press(game, START)
    press(game, DOWN)
    offer(game, "MEGA KICK", 5, 3000)
    assert position(game) == (2, 2)
    press(game, UP)
    offer(game, "MEGA PUNCH", 1, 3000)
    assert position(game) == (0, 0)
    press(game, B)
    shows(game, "MEGA PUNCH", "START INFO")


def check_only_machine(game):
    setup(game)
    game.put("wItemList", (3, 0x14, TM01, 0x38, 0xff))
    game.invoke("DisplayPokemartDialogue_")
    shows(game, "BUY", "SELL")
    press(game, A)
    shows(game, "POTION", "START INFO", accept=True)
    press(game, DOWN)
    shows(game, "MEGA PUNCH", "START INFO")
    press(game, START)
    for key in (UP, DOWN):
        press(game, key)
        offer(game, "MEGA PUNCH", 1, 3000)
        assert "UP DOWN" not in game.visible_text()
    game.core.GB_set_key_state(game.gb, A, True)
    shows(game, "MEGA PUNCH", "CABBAGE")  # open immediately, before A is released
    assert "UP DOWN" not in game.visible_text()
    game.core.GB_set_key_state(game.gb, A, False)
    press(game, B)
    shows(game, "MEGA PUNCH", "START INFO")
    assert position(game) == (1, 0)

    press(game, START)
    shows(game, "MEGA PUNCH", "POW")
    game.tick(15)
    for key in (A, B):
        game.core.GB_set_key_state(game.gb, key, True)
    game.tick(18)
    for key in (A, B):
        game.core.GB_set_key_state(game.gb, key, False)
    shows(game, "MEGA PUNCH", "START INFO")  # B wins without opening a transaction
    assert position(game) == (1, 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        for check in (check_mart, check_prize, check_mixed_shop, check_only_machine):
            with Game(args.sameboy, args.boot, args.directory / f"poke{color}.gbc") as game:
                check(game)
        print(f"{args.directory.name} {color}: TM browsing and purchases passed", flush=True)


if __name__ == "__main__":
    main()
