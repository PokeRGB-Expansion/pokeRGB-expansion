"""Read corrected signs and type advice on the linked cartridge."""

import argparse
from pathlib import Path

from adventure_checkpoints import (
    A, LEFT, UP, advance_text_until, checkpoint, hold_until, position, set_event, shows,
)
from cartridge_smoke import Game, seed_party
from safari_session import seed_session


CELADON_CITY = 0x06
FUCHSIA_CITY = 0x07
SAFFRON_CITY = 0x0A
SAFFRON_GYM = 0xB2
SAFARI_EAST = 0xD9
SAFARI_NORTH = 0xDA
SAFARI_CENTER = 0xDC
DEFEATED_SAFFRON_TRAINER = 0x363
GHOST_TYPE = 0x08
PSYCHIC_TYPE = 0x18


def check_celadon(game):
    checkpoint(game, CELADON_CITY, 25, 39, 22, last_map=CELADON_CITY)
    game.press(UP)
    assert position(game) == (39, 22)
    game.press(A)
    advance_text_until(game, lambda: "GUARD SPEC" in game.visible_text())
    advance_text_until(game, lambda: "GROWL" in game.visible_text()
                       and "lowering stats" in game.visible_text())
    advance_text_until(game, lambda: "DEPT" in game.visible_text()
                       and "STORE" in game.visible_text())


def safari_steps(game):
    return int.from_bytes(game.get_bytes("wSafariSteps", 2), "big")


def check_safari(game):
    seed_party(game)
    seed_session(game)
    checkpoint(game, SAFARI_EAST, 15, 5, 24, last_map=FUCHSIA_CITY)
    steps = safari_steps(game)
    game.press(UP)
    assert position(game) == (5, 24)
    game.press(A)
    shows(game, "AREA 1", "NORTH", "AREA 2")
    assert safari_steps(game) == steps
    advance_text_until(game, lambda: "NORTH" not in game.visible_text())

    checkpoint(game, SAFARI_NORTH, 20, 13, 32, last_map=FUCHSIA_CITY)
    game.press(UP)
    game.press(A)
    shows(game, "AREA 2")
    advance_text_until(game, lambda: "AREA 2" not in game.visible_text())

    for row, destination in ((4, SAFARI_NORTH), (22, SAFARI_CENTER)):
        checkpoint(game, SAFARI_EAST, 15, 1, row, last_map=FUCHSIA_CITY)
        steps = safari_steps(game)
        hold_until(game, LEFT, lambda: game.get("wCurMap") == destination)
        assert safari_steps(game) == steps - 1


def check_saffron(game, cartridge):
    # Look up the exact pairing from the linked chart used in battle.
    bank, address = game.addresses["TypeEffects"]
    chart = cartridge.read_bytes()
    start = bank * 0x4000 + (address & 0x3FFF)
    end = chart.index(0xFF, start)
    ghost_effect = next(factor for attack, target, factor in
                        zip(chart[start:end:3], chart[start + 1:end:3], chart[start + 2:end:3])
                        if (attack, target) == (GHOST_TYPE, PSYCHIC_TYPE))

    set_event(game, DEFEATED_SAFFRON_TRAINER)
    checkpoint(game, SAFFRON_GYM, 10, 17, 2, last_map=SAFFRON_CITY)
    game.press(UP)
    assert position(game) == (17, 2)
    game.press(A)
    if ghost_effect > 10:
        shows(game, "fear only ghosts")
        advance_text_until(game, lambda: "and bugs" in game.visible_text())
    else:
        shows(game, "fear only bugs")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        cartridge = args.directory / f"poke{color}.gbc"
        for check in (check_celadon, check_safari):
            with Game(args.sameboy, args.boot, cartridge) as game:
                game.new_game()
                check(game)
        with Game(args.sameboy, args.boot, cartridge) as game:
            game.new_game()
            check_saffron(game, cartridge)
        print(f"{cartridge}: Guard Spec., Safari signs and routes, and Saffron advice passed",
              flush=True)


if __name__ == "__main__":
    main()
