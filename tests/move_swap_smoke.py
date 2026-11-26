"""Exercise FIGHT move reordering and its interaction with Counter in SameBoy."""

import argparse
from pathlib import Path

from cartridge_smoke import Game


TACKLE, EMBER, WATER_GUN, SCRATCH = 0x21, 0x34, 0x37, 0x0A
COUNTER, STRUGGLE = 0x44, 0xA5
MOVES = bytes((TACKLE, EMBER, WATER_GUN, SCRATCH))
PP = bytes((31, 21, 0x57, 0xDB))
UP, DOWN, A, B, SELECT, START = 2, 3, 4, 5, 6, 7
SOURCE_MARKER, CURSOR = 0xEC, 0xED


def battle_row(game, row):
    return game.get("wTileMap", (12 + row) * 20 + 5)


def wait_row(game, row):
    game.wait(lambda: game.get("wCurrentMenuItem") == row and battle_row(game, row) == CURSOR)
    game.tick(10)


def open_fight(game, row=1, count=4, *, disabled=0, transformed=False, link=False):
    game.put("wTileMap", bytes(360))
    game.put("wBattleMonMoves", MOVES[:count].ljust(4, b"\0"))
    game.put("wBattleMonPP", PP[:count].ljust(4, b"\0"))
    game.put("wPartyMon1Moves", MOVES)
    game.put("wPartyMon1PP", PP)
    game.put("wPlayerMonNumber", (0,))
    game.put("wPlayerMoveListIndex", (row - 1,))
    game.put("wPlayerDisabledMove", (disabled,))
    game.put("wPlayerBattleStatus3", (int(transformed) << 3,))
    game.put("wNumMovesMinusOne", (count - 1,))
    game.put("wMoveMenuType", (0,))
    game.put("wMenuItemToSwap", (0,))
    game.put("wMenuJoypadPollCount", (0,))
    game.put("wMenuWatchMovingOutOfBounds", (0,))
    game.put("wLinkState", (4 if link else 0,))
    game.put("wLinkBattleRandomNumberListIndex", (3,))
    game.invoke("MoveSelectionMenu")
    wait_row(game, row)


def hover(game):
    return (game.get("wPlayerSelectedMove"), game.get("wPlayerMovePower"),
            game.get("wPlayerMoveType"))


def close_with_b(game, remembered_row):
    game.press(B)
    game.return_to_stub()
    assert game.cpu.af & 0x80 == 0
    assert game.get("wPlayerMoveListIndex") == remembered_row - 1
    assert game.get("wMenuItemToSwap") == 0


def run_counter(game, expected_hit):
    game.put("hWhoseTurn", (1,))
    game.put("wEnemySelectedMove", (COUNTER,))
    game.put("wEnemyMoveEffect", (0,))
    game.put("wEnemyBattleStatus2", (1,))  # X Accuracy makes the hit deterministic.
    game.put("wPlayerBattleStatus1", (0,))
    game.put("wPlayerBattleStatus2", (0,))
    game.put("wDamage", (0, 19))
    game.invoke("HandleCounterMove")
    game.return_to_stub()
    assert game.get("wMoveMissed") == (0 if expected_hit else 1)
    assert game.get_bytes("wDamage", 2) == bytes((0, 38 if expected_hit else 19))


def check_counter(game, core):
    tackle = (TACKLE, 35, 0)
    ember = (EMBER, 40, 0x14)
    water_gun = (WATER_GUN, 40, 0x15)
    for anchor, mark, expected in ((1, False, water_gun), (1, True, tackle), (2, True, ember)):
        open_fight(game, anchor)
        for row in range(anchor + 1, 4):
            game.press(DOWN)
            wait_row(game, row)
        assert hover(game) == water_gun
        if mark:
            game.press(SELECT)
            game.wait(lambda: game.get("wMenuItemToSwap") == 3)
            wait_row(game, 3 if core else anchor)
            if core:
                assert "WATER" in game.visible_text()
                assert "23 30" in game.visible_text(), game.visible_text()
                game.press(START)
                game.wait(lambda: "SEL EFFECT" in game.visible_text())
                assert "WATER GUN" in game.visible_text()
                game.press(B)
                game.wait(lambda: "SEL EFFECT" not in game.visible_text())
                wait_row(game, 3)
        close_with_b(game, anchor if mark else 3)
        assert hover(game) == expected
        assert game.get_bytes("wBattleMonPP", 4) == PP
        run_counter(game, expected_hit=mark and anchor == 1)


def check_swap(game):
    for anchor, transformed in ((1, False), (2, True)):
        open_fight(game, anchor, disabled=0x34, transformed=transformed)
        for row in range(anchor + 1, 4):
            game.press(DOWN)
            wait_row(game, row)
        game.press(SELECT)
        game.wait(lambda: game.get("wMenuItemToSwap") == 3)
        wait_row(game, 3)
        assert "disabled" in game.visible_text()
        game.press(DOWN)
        wait_row(game, 4)
        assert battle_row(game, 3) == SOURCE_MARKER
        game.press(SELECT)
        game.wait(lambda: game.get("wMenuItemToSwap") == 0)
        wait_row(game, 4)
        swapped_moves = MOVES[:2] + MOVES[2:][::-1]
        swapped_pp = PP[:2] + PP[2:][::-1]
        assert game.get_bytes("wBattleMonMoves", 4) == swapped_moves
        assert game.get_bytes("wBattleMonPP", 4) == swapped_pp
        assert game.get_bytes("wPartyMon1Moves", 4) == (MOVES if transformed else swapped_moves)
        assert game.get_bytes("wPartyMon1PP", 4) == (PP if transformed else swapped_pp)
        assert game.get("wPlayerDisabledMove") == 0x44
        assert "disabled" in game.visible_text()
        assert game.get("wLinkBattleRandomNumberListIndex") == 3
        game.press(UP)
        wait_row(game, 3)
        game.press(A)
        game.return_to_stub()
        assert game.cpu.af & 0x80
        assert game.get("wPlayerMoveListIndex") == 2
        assert game.get("wPlayerSelectedMove") == SCRATCH
        assert game.get_bytes("wBattleMonPP", 4) == swapped_pp


def check_other_controls(game):
    for count in (1, 2, 3):
        open_fight(game, count, count)
        game.press(SELECT)
        game.wait(lambda: game.get("wMenuItemToSwap") == count)
        wait_row(game, count)
        game.press(SELECT)
        game.wait(lambda: game.get("wMenuItemToSwap") == 0)
        wait_row(game, count)
        close_with_b(game, count)
        assert game.get_bytes("wBattleMonMoves", 4) == MOVES[:count].ljust(4, b"\0")
        assert game.get_bytes("wBattleMonPP", 4) == PP[:count].ljust(4, b"\0")

    # A uses the visible row immediately after SELECT and clears its marker.
    open_fight(game)
    game.press(DOWN)
    wait_row(game, 2)
    game.press(SELECT)
    game.wait(lambda: game.get("wMenuItemToSwap") == 2)
    wait_row(game, 2)
    game.press(A)
    game.return_to_stub()
    assert game.cpu.af & 0x80
    assert game.get("wPlayerMoveListIndex") == 1
    assert hover(game) == (EMBER, 40, 0x14)
    assert game.get("wMenuItemToSwap") == 0

    # The remembered row reads the swapped record. A second swap can undo it.
    open_fight(game)
    for source, dest, direction, expected_moves, expected_hover in (
        (1, 2, DOWN, bytes((EMBER, TACKLE)) + MOVES[2:], (EMBER, 40, 0x14)),
        (2, 1, UP, MOVES, (TACKLE, 35, 0)),
    ):
        game.press(SELECT)
        game.wait(lambda: game.get("wMenuItemToSwap") == source)
        wait_row(game, source)
        game.press(direction)
        wait_row(game, dest)
        game.press(SELECT)
        game.wait(lambda: game.get("wMenuItemToSwap") == 0)
        wait_row(game, dest)
        assert game.get_bytes("wBattleMonMoves", 4) == expected_moves
        assert hover(game) == expected_hover
    close_with_b(game, 1)
    assert game.get_bytes("wBattleMonPP", 4) == PP

    # A disabled remembered row keeps the stock Struggle fallback on redraw.
    open_fight(game, disabled=0x14)
    game.press(DOWN)
    wait_row(game, 2)
    game.press(SELECT)
    game.wait(lambda: game.get("wMenuItemToSwap") == 2)
    wait_row(game, 2)
    close_with_b(game, 1)
    assert hover(game) == (STRUGGLE, 40, 0x14)

    open_fight(game, link=True)
    game.press(DOWN)
    wait_row(game, 2)
    game.press(SELECT)
    game.tick(10)
    assert game.get("wMenuItemToSwap") == 0
    wait_row(game, 2)
    close_with_b(game, 2)
    assert game.get_bytes("wBattleMonMoves", 4) == MOVES
    assert game.get_bytes("wBattleMonPP", 4) == PP
    assert game.get("wLinkBattleRandomNumberListIndex") == 3


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path, nargs="+")
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True, help="SameBoy DMG boot file.")
    parser.add_argument("--minimal", action="store_true", help="Check the stock cursor rules.")
    args = parser.parse_args()
    for rom in args.rom:
        with Game(args.sameboy, args.boot, rom) as game:
            game.new_game()
            check_counter(game, core=not args.minimal)
            if not args.minimal:
                check_swap(game)
                check_other_controls(game)
            print(f"{rom.parent.name} {rom.name}: move swap and Counter controls passed", flush=True)


if __name__ == "__main__":
    main()
