"""Check poison blackouts and Mt. Moon battle suppression on the cartridge."""

import argparse
from pathlib import Path

from adventure_checkpoints import (
    A, DOWN, LEFT, PEWTER_GYM, RIGHT, UP, advance_text_until, battery_offset,
    checkpoint, position, set_event, shows, walk_to,
)
from cartridge_smoke import Game, seed_party


START = 7
REDS_HOUSE_2F = 0x26
VIRIDIAN_CITY = 0x01
PEWTER_CITY = 0x02
MT_MOON_B2F = 0x3D
BEAT_MT_MOON_SUPER_NERD = 0x579
NO_BATTLES = 0x10
POISON = 0x08
BEFORE_BLACKOUT = bytes((0, 0x12, 0x35))
AFTER_BLACKOUT = bytes((0, 0x06, 0x17))


def poison_party(game, *, hp, survivor):
    seed_party(game)
    game.put("wPartyMon1HP", (0, hp))
    game.put("wPartyMon1Status", (POISON,))
    game.put("wPartyMon2HP", (0, 160 if survivor else 0))
    game.put("wPlayerMoney", BEFORE_BLACKOUT)
    game.put("wLastBlackoutMap", (VIRIDIAN_CITY,))


def load_save(game, saved):
    game.tick(240)
    start = battery_offset(game, "sHallOfFame")
    game.battery()[start:] = saved[start:]
    game.invoke("MainMenu")
    shows(game, "CONTINUE", "NEW GAME")
    game.tick(35)
    game.press(A)
    shows(game, "PLAYER", "BADGES")
    game.tick(45)
    game.press(A)


def check_blackout(game, *, location):
    advance_text_until(game, lambda: "blacked" in game.visible_text())
    assert (game.get("wCurMap"), position(game)) == location
    advance_text_until(game, lambda: game.get("wCurMap") == VIRIDIAN_CITY
                       and game.get("wJoyIgnore") == 0)
    game.tick(100)
    assert position(game) == (23, 26)
    assert game.get_bytes("wPlayerMoney", 3) == AFTER_BLACKOUT
    assert game.get_bytes("wPartyMon1HP", 2) == bytes((0, 160))
    assert game.get_bytes("wPartyMon2HP", 2) == bytes((0, 160))
    assert game.get("wPartyMon1Status") == 0


def saved_poison_party(library, boot, rom, *, survivor, hp=0, status=POISON):
    with Game(library, boot, rom) as game:
        game.new_game()
        poison_party(game, hp=hp, survivor=survivor)
        game.put("wPartyMon1Status", (status,))
        game.invoke("SaveGameData")
        game.return_to_stub()
        return bytes(game.battery())


def check_poison_reload(library, boot, rom, *, minimal):
    # Resume saves with an all-fainted party, with or without a poison status.
    for status in (POISON, 0):
        saved = saved_poison_party(library, boot, rom, survivor=False, status=status)
        with Game(library, boot, rom) as game:
            load_save(game, saved)
            if minimal:
                game.tick(90)
                assert position(game) == (3, 6)
                walk_to(game, RIGHT, 4, 6)
                assert game.get_bytes("wPlayerMoney", 3) == BEFORE_BLACKOUT
                assert game.get_bytes("wPartyMon1HP", 2) == bytes(2)
            else:
                check_blackout(game, location=(REDS_HOUSE_2F, (3, 6)))
                assert bytes(game.battery()[8192:]) == saved[8192:]

    saved = saved_poison_party(library, boot, rom, survivor=True, hp=1)
    with Game(library, boot, rom) as game:
        load_save(game, saved)
        game.tick(90)
        assert position(game) == (3, 6)
        for key, x in ((RIGHT, 4), (LEFT, 3), (RIGHT, 4)):
            walk_to(game, key, x, 6)
            assert game.get_bytes("wPartyMon1HP", 2) == bytes((0, 1))
        walk_to(game, LEFT, 3, 6)
        advance_text_until(game, lambda: "fainted" in game.visible_text())
        advance_text_until(game, lambda: "fainted" not in game.visible_text())
        assert game.get_bytes("wPartyMon1HP", 2) == bytes(2)
        assert game.get_bytes("wPartyMon2HP", 2) == bytes((0, 160))
        assert game.get_bytes("wPlayerMoney", 3) == BEFORE_BLACKOUT
        assert game.get("wCurMap") == REDS_HOUSE_2F

    with Game(library, boot, rom) as game:
        game.new_game()
        game.invoke("SaveGameData")
        game.return_to_stub()
        empty_party_save = bytes(game.battery())
        money = game.get_bytes("wPlayerMoney", 3)
    with Game(library, boot, rom) as game:
        load_save(game, empty_party_save)
        game.tick(90)
        walk_to(game, RIGHT, 4, 6)
        assert game.get("wPartyCount") == 0
        assert game.get("wCurMap") == REDS_HOUSE_2F
        assert game.get_bytes("wPlayerMoney", 3) == money


def check_ordinary_poison(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        poison_party(game, hp=1, survivor=False)
        for key, x in ((RIGHT, 4), (LEFT, 3), (RIGHT, 4)):
            walk_to(game, key, x, 6)
            assert game.get_bytes("wPartyMon1HP", 2) == bytes((0, 1))
        walk_to(game, LEFT, 3, 6)
        check_blackout(game, location=(REDS_HOUSE_2F, (3, 6)))


def battles_suppressed(game):
    return bool(game.get("wStatusFlags4") & NO_BATTLES)


def fossil_area(game):
    game.new_game()
    seed_party(game)
    set_event(game, BEAT_MT_MOON_SUPER_NERD)
    game.put("wNumBagItems", (1, 0x1D, 1, 0xFF))  # Escape Rope.
    game.put("wLastBlackoutMap", (PEWTER_CITY,))
    checkpoint(game, MT_MOON_B2F, 20, 14, 7, last_map=PEWTER_CITY)
    game.wait(lambda: battles_suppressed(game))


def check_fossil_escape(library, boot, rom, *, minimal):
    with Game(library, boot, rom) as game:
        fossil_area(game)
        game.press(START)
        shows(game, "ITEM", "OPTION")
        game.tick(20)
        game.press(DOWN)
        game.press(A)
        shows(game, "ESCAPE ROPE")
        game.tick(20)
        game.press(A)
        shows(game, "USE", "TOSS")
        game.tick(20)
        game.press(A)
        game.wait(lambda: game.get("wCurMap") == PEWTER_CITY and game.get("wJoyIgnore") == 0)
        game.tick(60)
        assert position(game) == (13, 26)
        assert game.get("wNumBagItems") == 0
        assert battles_suppressed(game) == minimal
        if not minimal:
            # The same session can now start a normal trainer battle.
            checkpoint(game, PEWTER_GYM, 5, 4, 2, last_map=PEWTER_CITY)
            game.press(UP)
            game.press(A)
            advance_text_until(game, lambda: game.get("wIsInBattle") == 2)

    with Game(library, boot, rom) as game:
        fossil_area(game)
        game.put("wPartyMon1Moves", (0x5B, 0, 0, 0))  # Dig.
        game.press(START)
        shows(game, "ITEM", "OPTION")
        game.tick(20)
        game.press(A)
        shows(game, "TEST", "160")
        game.tick(20)
        game.press(A)
        shows(game, "DIG", "STATS")
        game.tick(20)
        game.press(A)
        game.wait(lambda: game.get("wCurMap") == PEWTER_CITY and game.get("wJoyIgnore") == 0)
        game.tick(60)
        assert position(game) == (13, 26)
        assert game.get_bytes("wNumBagItems", 4) == bytes((1, 0x1D, 1, 0xFF))
        assert battles_suppressed(game) == minimal


def check_fossil_boundaries(library, boot, rom):
    with Game(library, boot, rom) as game:
        fossil_area(game)
        walk_to(game, RIGHT, 15, 7)
        game.wait(lambda: not battles_suppressed(game))

    with Game(library, boot, rom) as game:
        game.new_game()
        # Call the common special warp with a scripted suppression bit set
        # outside Mt. Moon. The Mt. Moon cleanup must leave this bit alone.
        game.put("wStatusFlags4", (game.get("wStatusFlags4") | NO_BATTLES,))
        game.put("wDestinationMap", (PEWTER_CITY,))
        game.put("wStatusFlags6", (game.get("wStatusFlags6") | 0x04,))
        game.invoke("PrepareForSpecialWarp")
        game.return_to_stub()
        assert battles_suppressed(game)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--minimal", action="store_true")
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        fixture = args.sameboy, args.boot, args.directory / f"poke{color}.gbc"
        check_poison_reload(*fixture, minimal=args.minimal)
        check_ordinary_poison(*fixture)
        check_fossil_escape(*fixture, minimal=args.minimal)
        check_fossil_boundaries(*fixture)
        print(f"{args.directory.name} {color}: poison reload, normal blackout, and Mt. Moon exits passed",
              flush=True)


if __name__ == "__main__":
    main()
