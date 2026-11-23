"""Check Safari session state through the gate and overworld in SameBoy."""

import argparse
from pathlib import Path

from cartridge_smoke import Game, seed_party


FUCHSIA = 0x07
GATE = 0x9C
CENTER = 0xDC
CENTER_REST_HOUSE = 0xDD
EVENT_BYTE = 0x49
ACTIVE = 0x80
GAME_OVER = 0x40
LEAVING_SAFARI = 5
SET_SCRIPT_AFTER_MOVE = 6
UP, DOWN, A = 2, 3, 4


def session(game):
    flags = game.get("wEventFlags", EVENT_BYTE) & (ACTIVE | GAME_OVER)
    balls = game.get("wNumSafariBalls")
    steps = int.from_bytes(game.get_bytes("wSafariSteps", 2), "big")
    return flags, balls, steps


def seed_session(game, *, balls=21, steps=350):
    address = game.addresses["wEventFlags"][1] + EVENT_BYTE
    game.write(address, (game.get("wEventFlags", EVENT_BYTE) | ACTIVE,))
    game.put("wNumSafariBalls", (balls,))
    game.put("wSafariSteps", steps.to_bytes(2, "big"))
    game.put("wSafariZoneGateCurScript", (LEAVING_SAFARI,))


def load_map(game, map_id, width, x, y):
    game.put("wCurMap", (map_id,))
    game.put("wYCoord", (y, x, y % 2, x % 2))
    map_start = game.addresses["wOverworldMap"][1]
    view_start = map_start + (width + 6) * (y // 2 + 1) + x // 2 + 1
    game.put("wCurrentTileBlockMapViewPointer", view_start.to_bytes(2, "little"))
    game.put("wLastMap", (FUCHSIA,))
    game.invoke("EnterMap")
    game.wait(lambda: game.get("wCurMap") == map_id and game.get("wCurMapWidth") == width)
    game.tick(45)


def walk(game, key):
    game.core.GB_set_key_state(game.gb, key, True)
    game.tick(35)
    game.core.GB_set_key_state(game.gb, key, False)
    game.tick(16)


def wait_choice(game, question):
    def choice_is_visible():
        text = game.visible_text()
        return question in text and "YES" in text and "NO" in text

    game.wait(choice_is_visible, accept=True)


def gate_lobby(game):
    game.wait(
        lambda: game.get("wCurMap") == GATE and game.get("wYCoord") == 3
        and not game.get("wSafariZoneGateCurScript") and not game.get("wWalkCounter"),
        accept=True,
    )


def continue_game(game, save):
    game.new_game()
    game.battery()[:] = save
    game.put("wNextSafariZoneGateScript", (0,))
    game.invoke("MainMenu")
    game.wait(lambda: game.get("wSaveFileStatus") == 2 and "CONTINUE" in game.visible_text())
    game.tick(40)
    game.press(A)
    game.wait(lambda: "CONTINUE" not in game.visible_text(), accept=True)
    game.tick(85)


def check_decline_reload_and_fee(library, boot, rom, x):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        game.put("wOptions", (1,))
        seed_session(game)
        load_map(game, CENTER, 15, x, 24)

        walk(game, DOWN)
        wait_choice(game, "Leaving early")
        game.press(DOWN)
        game.press(A)
        game.wait(lambda: game.get("wCurMap") == CENTER, accept=True)
        game.tick(75)
        assert session(game) == (ACTIVE, 21, 349)
        assert game.get("wSafariZoneGateCurScript") == SET_SCRIPT_AFTER_MOVE

        # Step off the return warp before saving.
        game.core.GB_set_key_state(game.gb, UP, True)
        game.wait(lambda: game.get("wYCoord") == 24 and not game.get("wWalkCounter"))
        game.core.GB_set_key_state(game.gb, UP, False)
        game.tick(6)
        game.invoke("SaveGameData")
        game.return_to_stub()

        save = bytes(game.battery())

    # Boot with only the battery-backed save and continue through the game menu.
    with Game(library, boot, rom) as game:
        continue_game(game, save)
        assert game.get("wCurMap") == CENTER
        assert session(game) == (ACTIVE, 21, 348)

        walk(game, DOWN)
        wait_choice(game, "Leaving early")
        assert session(game) == (ACTIVE, 21, 347)
        game.press(A)
        gate_lobby(game)
        assert session(game) == (0, 0, 0)

        game.put("wPlayerMoney", (0, 0x12, 0x50))
        walk(game, UP)
        wait_choice(game, "join the hunt")
        game.press(DOWN)
        game.press(A)
        gate_lobby(game)
        assert session(game) == (0, 0, 0)
        assert game.get_bytes("wPlayerMoney", 3) == bytes((0, 0x12, 0x50))

        walk(game, UP)
        wait_choice(game, "join the hunt")
        game.press(A)
        game.wait(
            lambda: game.get("wCurMap") == CENTER and game.get("wCurMapWidth") == 15,
            accept=True,
        )
        game.tick(85)
        assert session(game) == (ACTIVE, 30, 500)
        assert game.get_bytes("wPlayerMoney", 3) == bytes((0, 0x07, 0x50))


def check_timeout(library, boot, rom, *, balls, steps):
    with Game(library, boot, rom) as game:
        game.new_game()
        game.put("wOptions", (1,))
        seed_session(game, balls=balls, steps=steps)
        load_map(game, CENTER, 15, 14, 24)
        if balls:
            walk(game, UP)
        gate_lobby(game)
        assert session(game) == (0, 0, 0)


def check_poison_blackout(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        game.put("wPartyCount", (1,))
        game.put("wPartySpecies", (0x69, 0xFF))
        game.put("wPartyMon1Status", (8,))
        game.put("wPartyMon1HP", (0, 1))
        game.put("wOptions", (1,))
        game.put("wLastBlackoutMap", (FUCHSIA,))
        seed_session(game)
        load_map(game, CENTER, 15, 14, 24)

        game.put("wStepCounter", (1,))
        walk(game, UP)
        game.wait(lambda: game.get("wCurMap") == FUCHSIA, accept=True)
        game.tick(100)
        assert session(game) == (0, 0, 0)
        assert game.get("wSafariZoneGateCurScript") == 0
        assert game.get_bytes("wPartyMon1HP", 2) == bytes((0, 160))


def check_house_and_stale_state(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_session(game)
        load_map(game, CENTER_REST_HOUSE, 4, 2, 4)
        assert session(game) == (ACTIVE, 21, 350)
        assert game.get("wSafariZoneGateCurScript") == LEAVING_SAFARI

        # A save made outside the Safari Zone by an older build can have live counters.
        load_map(game, FUCHSIA, 20, 18, 4)
        seed_session(game, balls=0)
        game.invoke("SaveGameData")
        game.return_to_stub()
        save = bytes(game.battery())

    with Game(library, boot, rom) as game:
        continue_game(game, save)
        assert game.get("wCurMap") == FUCHSIA
        assert session(game) == (0, 0, 0)
        assert game.get("wSafariZoneGateCurScript") == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color, x in (("red", 14), ("blue", 15), ("green", 14)):
        rom = args.directory / f"poke{color}.gbc"
        fixture = (args.sameboy, args.boot, rom)
        check_decline_reload_and_fee(*fixture, x)
        check_timeout(*fixture, balls=0, steps=120)
        check_timeout(*fixture, balls=12, steps=0)
        check_poison_blackout(*fixture)
        check_house_and_stale_state(*fixture)
        print(f"Safari session tests passed on {color.title()}.")


if __name__ == "__main__":
    main()
