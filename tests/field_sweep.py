"""Exercise the cave options palette, Town Map pins and Cycling Road entry checks."""

import argparse
from pathlib import Path

from cartridge_smoke import Game
from field_shortcuts import open_party_move, setup_party
from route_cut_tree import walk_until


LEFT, UP, DOWN, A, B, START = 1, 2, 3, 4, 5, 7
BGP = 0xff47
ROUTE_1, ROUTE_10, ROCK_TUNNEL, POWER_PLANT = 0x0c, 0x15, 0x52, 0x53
ROCK_TUNNEL_B1F = 0xe8
BICYCLE, TOWN_MAP = 6, 5
FLASH, BOULDER_BADGE = 0x94, 1


def check_options(game, *, cave=False, basement=False, flash=False):
    game.new_game()
    game.enter_map(ROUTE_10, 10, 8, 18)
    if cave:
        walk_until(game, UP, lambda: game.get("wCurMap") == ROCK_TUNNEL and game.get("wCurMapWidth") == 20)
        game.tick(110)
    if basement:
        game.enter_map(ROCK_TUNNEL_B1F, 20, 33, 3, last_map=ROUTE_10)
    if flash:
        setup_party(game, FLASH, BOULDER_BADGE)
        open_party_move(game, "FLASH")
        game.wait(lambda: "lights the area" in game.visible_text(), accept=True)
        game.wait(lambda: "lights the area" not in game.visible_text(), accept=True)
        game.tick(100)
    dark = cave and not flash
    field_palette = 0xfe if dark else 0xe4
    palette = lambda: game.core.GB_safe_read_memory(game.gb, BGP)
    assert palette() == field_palette
    game.press(START)
    game.wait(lambda: "OPTION" in game.visible_text())
    for _ in range(4):
        game.press(DOWN)
        game.tick(12)
    assert palette() == field_palette
    game.press(A)
    game.wait(lambda: "TEXT SPEED" in game.visible_text() and palette() == 0xe4)
    game.tick(20)
    assert game.get("wMapPalOffset") == (6 if dark else 0)
    game.press(B)
    game.wait(lambda: "OPTION" in game.visible_text())
    assert palette() == field_palette
    game.press(B)
    game.tick(50)
    assert palette() == field_palette


def check_town_map(game, map_id, width, button, names):
    game.new_game()
    game.enter_map(map_id, width, 8, 8)
    game.put("wNumBagItems", (1, TOWN_MAP, 1, 0xff))
    game.press(START)
    game.wait(lambda: "OPTION" in game.visible_text())
    game.tick(30)
    game.press(DOWN)
    game.tick(24)
    game.press(A)
    game.wait(lambda: "TOWN MAP" in game.visible_text())
    game.tick(35)
    game.press(A)
    game.wait(lambda: "USE" in game.visible_text())
    game.tick(25)
    game.press(A)
    game.wait(lambda: game.get("hJoy7") and names[0] in game.visible_text())
    game.tick(65)
    for name in names[1:]:
        previous_pin = game.get_bytes("wShadowOAMBackupSprite04", 2)
        game.press(button)
        game.wait(lambda: game.visible_text().splitlines()[0].strip() == name)
        assert game.get_bytes("wShadowOAMBackupSprite04", 2) != previous_pin
        game.tick(25)
    game.press(B)
    game.wait(lambda: not game.get("hJoy7"))


def check_gate(game, gate, route, top_row, row, *, bike, held, core):
    game.new_game()
    game.put("wOptions", (1,))
    game.put("wNumBagItems", (1, BICYCLE, 1, 0xff) if bike else (0, 0xff))
    game.enter_map(gate, 4, 5, row, last_map=route)
    state = "wRoute16Gate1FCurScript" if route == 0x1b else "wRoute18Gate1FCurScript"
    game.core.GB_set_key_state(game.gb, LEFT, True)
    saw_guard = False
    passed = False
    try:
        for _ in range(160):
            game.tick(5)
            x = game.get("wXCoord")
            if x <= 2:
                passed = True
                break
            if saw_guard and x == 5 and game.get(state) == 0:
                break
            if "Excuse" in game.visible_text():
                saw_guard = True
                if not held:
                    game.core.GB_set_key_state(game.gb, LEFT, False)
            game.press(B)
        else:
            raise AssertionError((gate, row, "guard never finished"))
    finally:
        game.core.GB_set_key_state(game.gb, LEFT, False)
    assert saw_guard != bike
    assert passed == (bike or (not core and held and row == top_row)), (gate, row, bike, held, core)
    if passed:
        game.tick(45)
        if game.get("wYCoord") == top_row:
            walk_until(game, DOWN, lambda: game.get("wYCoord") == top_row + 1)
        walk_until(game, LEFT, lambda: game.get("wCurMap") == route)
        game.tick(120)
        assert game.get("wWalkBikeSurfState") == 1
    else:
        assert (game.get("wXCoord"), game.get("wYCoord")) == (5, top_row)
        assert game.get("wJoyIgnore") == 0


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
        locations = [{}, {"cave": True}]
        if color == "red":
            locations += [{"cave": True, "basement": True}, {"cave": True, "flash": True}]
        for location in locations:
            with Game(*fixture) as game:
                check_options(game, **location)
        for map_id, width, button, labels in (
            (ROUTE_1, 10, UP, ("ROUTE 1", "VIRIDIAN CITY", "ROUTE 2")),
            (POWER_PLANT, 20, DOWN, ("POWER PLANT", "INDIGO PLATEAU", "VICTORY ROAD")),
        ):
            with Game(*fixture) as game:
                check_town_map(game, map_id, width, button, labels)
        for gate, route, top in ((0xba, 0x1b, 7), (0xbe, 0x1d, 3)):
            cases = [(top, False, True), (top, True, True)]
            if color == "red":
                cases += [(top, False, False)] + [(y, False, True) for y in range(top + 1, top + 4)]
            for row, bike, held in cases:
                with Game(*fixture) as game:
                    check_gate(game, gate, route, top, row, bike=bike, held=held, core=core)
        print(f"{args.directory.name} {color}: field palette, map pins and Bicycle gates passed", flush=True)


if __name__ == "__main__":
    main()
