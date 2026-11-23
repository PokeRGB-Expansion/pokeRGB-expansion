"""Exercise Surf and Strength through map input and the ordinary party menus."""

import argparse
from pathlib import Path

from cartridge_smoke import Game, seed_party


RIGHT, LEFT, UP, DOWN, A, B, SELECT, START = range(8)
PALLET_TOWN, ROUTE_12, SEAFOAM_ISLANDS_1F, SEAFOAM_ISLANDS_B4F = 0x00, 0x17, 0xC0, 0xA2
SURF, STRENGTH, SPLASH = 0x39, 0x46, 0x96
SOUL_BADGE, RAINBOW_BADGE = 0x10, 0x08
WALKING, SURFING = 0, 2
STRENGTH_ACTIVE = 1


def position(game):
    return game.get("wXCoord"), game.get("wYCoord")


def shows(game, *words, accept=False):
    game.wait(lambda: all(word in game.visible_text() for word in words), accept=accept)
    game.tick(15)


def face(game, direction):
    game.put("wSpritePlayerStateData1FacingDirection", (direction,))
    game.put("wPlayerDirection", ((4, 8, 2, 1)[direction // 4],))


def setup_party(game, move, badge, *, second=False):
    seed_party(game)
    for number, name in ((1, "RIVER"), (2, "STAR")):
        game.put(f"wPartyMon{number}Nick",
                 bytes(ord(letter) - 65 + 0x80 for letter in name) + b"\x50")
    game.put(f"wPartyMon{2 if second else 1}Moves", (move, 0, 0, 0))
    game.put(f"wPartyMon{2 if second else 1}PP", (0, 0, 0, 0))
    game.put("wObtainedBadges", (badge,))
    game.put("wOptions", (1,))
    assert game.get("wNumBagItems") == 0


def shore(game):
    game.enter_map(PALLET_TOWN, 10, 5, 13)
    face(game, 0)  # South.


def open_party_move(game, move_name):
    game.press(START)
    shows(game, "SAVE")
    game.press(A)
    shows(game, "RIVER", "STAR")
    game.press(A)
    shows(game, move_name, "STATS")
    game.press(A)


def prompt(game, name):
    game.press(A)
    shows(game, f"Use {name}", "YES", "NO", accept=True)


def walk(game, key, arrived):
    game.core.GB_set_key_state(game.gb, key, True)
    try:
        game.wait(arrived)
    finally:
        game.core.GB_set_key_state(game.gb, key, False)
    game.tick(20)


def check_surf(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        setup_party(game, SURF, SOUL_BADGE, second=True)
        game.put("wPartyMon2HP", (0, 0))  # The manual action allows a fainted user.
        shore(game)
        # Holding the original A press cannot also accept the prompt.
        game.core.GB_set_key_state(game.gb, A, True)
        try:
            game.tick(100)
            assert "Use SURF" in game.visible_text()
            assert position(game) == (5, 13)
            assert game.get("wWalkBikeSurfState") == WALKING
        finally:
            game.core.GB_set_key_state(game.gb, A, False)
        shows(game, "Use SURF", "YES", "NO", accept=True)
        game.press(B)
        game.wait(lambda: "Use SURF" not in game.visible_text())
        game.tick(15)
        assert game.get("wWalkBikeSurfState") == WALKING

        prompt(game, "SURF")
        game.press(DOWN)
        game.wait(lambda: game.get("wLastMenuItem") == 1)
        game.press(A)
        game.wait(lambda: "Use SURF" not in game.visible_text())
        game.tick(15)
        assert position(game) == (5, 13)
        assert game.get("wWalkBikeSurfState") == WALKING

        prompt(game, "SURF")
        game.press(A)
        game.wait(lambda: position(game) == (5, 14)
                  and game.get("wWalkBikeSurfState") == SURFING, accept=True)
        game.tick(20)
        assert game.get("wWhichPokemon") == 1
        assert game.get("wPartyMon2PP") == 0
        assert game.get("wNumBagItems") == 0
        game.press(A)
        game.tick(36)
        assert position(game) == (5, 14)
        assert "Use SURF" not in game.visible_text()
        walk(game, UP, lambda: position(game) == (5, 13))
        assert game.get("wWalkBikeSurfState") == WALKING

    with Game(library, boot, rom) as game:
        game.new_game()
        for move, badge, destination in (
            (SPLASH, SOUL_BADGE, (5, 13)),
            (SURF, 0, (5, 13)),
            (SURF, SOUL_BADGE, (5, 12)),  # Ground facing the shore.
        ):
            setup_party(game, move, badge)
            game.enter_map(PALLET_TOWN, 10, *destination)
            face(game, 0)
            game.press(A)
            game.tick(55)
            assert "Use SURF" not in game.visible_text()
            assert position(game) == destination
            assert game.get("wWalkBikeSurfState") == WALKING
        shore(game)
        open_party_move(game, "SURF")
        game.wait(lambda: position(game) == (5, 14)
                  and game.get("wWalkBikeSurfState") == SURFING, accept=True)
        assert game.get("wPartyMon1PP") == 0


def check_surf_restrictions(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        setup_party(game, SURF, SOUL_BADGE)
        shore(game)
        # Apply the stock forced-cycling flag at an otherwise legal shore.
        flags = game.get("wStatusFlags6")
        game.put("wStatusFlags6", (flags | (1 << 5),))
        game.press(A)
        game.tick(55)
        assert "Use SURF" not in game.visible_text()
        assert position(game) == (5, 13)
        assert game.get("wWalkBikeSurfState") == WALKING
        game.put("wStatusFlags6", (flags,))

        # Face the water at the one Seafoam square with a current check.
        offset = 0x9D0 // 8  # Both fallen boulders share this event byte.
        address = game.addresses["wEventFlags"][1] + offset
        initial = game.get("wEventFlags", offset) & ~3
        for events in (0, 1, 3):
            game.write(address, (initial | events,))
            game.enter_map(SEAFOAM_ISLANDS_B4F, 15, 7, 11)
            face(game, 0)
            if events == 3:
                prompt(game, "SURF")
                game.press(B)
                game.wait(lambda: "Use SURF" not in game.visible_text())
            else:
                game.press(A)
                game.tick(55)
                assert "Use SURF" not in game.visible_text()
            assert game.get("wTileInFrontOfPlayer") == 0x14
            assert position(game) == (7, 11)
            assert game.get("wWalkBikeSurfState") == WALKING


def boulder(game):
    return game.get("wSprite01StateData2MapX"), game.get("wSprite01StateData2MapY")


def enter_boulder_room(game):
    game.enter_map(SEAFOAM_ISLANDS_1F, 15, 17, 10)
    game.put("wGrassRate", (0,))
    face(game, 12)  # East toward the boulder at (18, 10).


def strength_active(game):
    return bool(game.get("wStatusFlags1") & STRENGTH_ACTIVE)


def check_strength(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        for move, badge in ((SPLASH, RAINBOW_BADGE), (STRENGTH, 0)):
            setup_party(game, move, badge)
            enter_boulder_room(game)
            before = boulder(game)
            game.press(A)
            shows(game, "This requires", "STRENGTH to move")
            assert not strength_active(game) and boulder(game) == before
            game.press(B)
            game.tick(20)

        setup_party(game, STRENGTH, RAINBOW_BADGE, second=True)
        enter_boulder_room(game)
        before = boulder(game)
        prompt(game, "STRENGTH")
        game.press(B)
        game.wait(lambda: "Use STRENGTH" not in game.visible_text())
        game.tick(15)
        assert not strength_active(game) and boulder(game) == before
        assert position(game) == (17, 10)

        prompt(game, "STRENGTH")
        game.press(DOWN)
        game.wait(lambda: game.get("wLastMenuItem") == 1)
        game.press(A)
        game.wait(lambda: "Use STRENGTH" not in game.visible_text())
        game.tick(15)
        assert not strength_active(game) and boulder(game) == before

        prompt(game, "STRENGTH")
        game.press(A)
        shows(game, "STAR", "STRENGTH")
        assert strength_active(game) and boulder(game) == before
        assert game.get("wWhichPokemon") == 1
        shows(game, "move boulders", accept=True)
        game.press(A)
        game.tick(30)
        game.press(A)
        shows(game, "This requires", "STRENGTH to move")
        assert strength_active(game) and boulder(game) == before
        game.press(B)
        game.tick(20)
        walk(game, RIGHT, lambda: boulder(game) != before)
        assert boulder(game) == (before[0] + 1, before[1])
        assert game.get("wPartyMon2PP") == 0

        enter_boulder_room(game)
        assert not strength_active(game)
        setup_party(game, STRENGTH, RAINBOW_BADGE)
        game.enter_map(PALLET_TOWN, 10, 5, 12)
        open_party_move(game, "STRENGTH")
        game.wait(lambda: strength_active(game), accept=True)


def check_snorlax(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        setup_party(game, SURF, SOUL_BADGE)
        game.put("wNumBagItems", (1, 0x49, 1, 0xFF))  # Poké Flute.
        game.enter_map(ROUTE_12, 10, 10, 61)
        face(game, 0)
        game.press(A)
        shows(game, "sleeping", "blocks the way")
        assert position(game) == (10, 61)
        assert not game.get("wIsInBattle")
        assert game.get("wWalkBikeSurfState") == WALKING


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--color", choices=("red", "blue", "green"), nargs="+")
    args = parser.parse_args()
    for color in args.color or ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        check_surf(args.sameboy, args.boot, rom)
        check_surf_restrictions(args.sameboy, args.boot, rom)
        check_strength(args.sameboy, args.boot, rom)
        check_snorlax(args.sameboy, args.boot, rom)
        print(f"{args.directory.name} {color}: Surf, Strength, and Snorlax controls passed",
              flush=True)


if __name__ == "__main__":
    main()
