"""Read every stock TM at the Celadon Mart and prize counter before paying."""

import argparse
from pathlib import Path

from cartridge_smoke import Game
from move_info_authoring import shows
from shop_carry_count import bag
from tm_party_info import B, COIN_CASE, DOWN, SELECT, START, open_counter, press, setup


# Machine, move, type, base power, listed accuracy, base PP and effect.
# These are the original shop and prize listings, in counter order.
MART = (
    (32, "DOUBLE TEAM", "NORMAL", "-", 100, 15, "Raises Evasion by 1 stage."),
    (33, "REFLECT", "PSYCHIC", "-", 100, 20, "Doubles physical Defense. Critical hits ignore it."),
    (2, "RAZOR WIND", "NORMAL", 80, 75, 10, "Charges on turn 1. Attacks on turn 2."),
    (7, "HORN DRILL", "NORMAL", "-", 30, 5, "Knocks out the foe on a hit. Fails if the foe is faster."),
    (37, "EGG BOMB", "NORMAL", 100, 75, 10, "Deals damage."),
    (1, "MEGA PUNCH", "NORMAL", 80, 85, 20, "Deals damage."),
    (5, "MEGA KICK", "NORMAL", 120, 75, 5, "Deals damage."),
    (9, "TAKE DOWN", "NORMAL", 90, 85, 20, "User loses 1/4 of the damage dealt, at least 1 HP."),
    (17, "SUBMISSION", "FIGHTING", 80, 80, 25, "User loses 1/4 of the damage dealt, at least 1 HP."),
)
PRIZES = (
    (23, "DRAGON RAGE", "DRAGON", "-", 100, 10, "Deals 40 damage when it hits."),
    (15, "HYPER BEAM", "NORMAL", 150, 90, 5, "Rest a turn after a hit. Skip on KO or a broken decoy."),
    (50, "SUBSTITUTE", "NORMAL", "-", 100, 10, "Uses 1/4 of max HP to make a decoy that takes hits."),
)


def panel_row(game, y):
    # Game.visible_text() hides punctuation, including the dash for base power.
    chars = game.visible_text().splitlines()[y][1:19]
    tiles = game.get_bytes("wTileMap", 20 * (y + 1))[-19:-1]
    punctuation = {0xE3: "-", 0xE8: ".", 0xF3: "/", 0xF4: ","}
    return "".join(punctuation.get(tile, char) for tile, char in zip(tiles, chars)).strip()


def check_counter(game, *, prize):
    setup(game)
    game.put("wNumBagItems", bag([(COIN_CASE, 1)]))
    game.put("wPlayerCoins", (0, 0))
    game.put("wPlayerMoney", (0, 0, 0))
    open_counter(game, prize, mart_row=0)
    contents = game.get_bytes("wNumBagItems", 42)
    for row, (number, name, element, power, accuracy, pp, effect) in enumerate(PRIZES if prize else MART):
        if row:
            press(game, DOWN)
        shows(game, f"TM{number:02}", name, "START INFO")
        selection = (game.get("wCurrentMenuItem"), game.get("wListScrollOffset"))
        press(game, START)
        shows(game, name, element, "SELECT EFFECT")
        assert panel_row(game, 12) == name
        assert panel_row(game, 13) == element
        shown_power, _, shown_accuracy = panel_row(game, 14).partition("ACC")
        assert shown_power.split() == ["POW", str(power)], (name, shown_power)
        assert shown_accuracy.strip() == f"{accuracy}/100", (name, shown_accuracy)
        assert panel_row(game, 15).split() == ["PP", str(pp)]
        press(game, SELECT)
        shows(game, "SELECT PARTY")
        displayed = " ".join(filter(None, (panel_row(game, y) for y in (13, 14, 15))))
        assert displayed == effect, (name, displayed)
        press(game, B)
        shows(game, f"TM{number:02}", name, "START INFO")
        assert (game.get("wCurrentMenuItem"), game.get("wListScrollOffset")) == selection
        assert game.get_bytes("wPlayerMoney", 3) == bytes(3)
        assert game.get_bytes("wPlayerCoins", 2) == bytes(2)
        assert game.get_bytes("wNumBagItems", 42) == contents


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        for prize in (False, True):
            with Game(args.sameboy, args.boot, args.directory / f"poke{color}.gbc") as game:
                check_counter(game, prize=prize)
        print(f"{args.directory.name} {color}: all 12 stock TMs show their move data before purchase", flush=True)


if __name__ == "__main__":
    main()
