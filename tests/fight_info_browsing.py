"""Compare live battle moves in INFO, then cancel, reorder or choose one."""

import argparse
from pathlib import Path

from adventure_checkpoints import advance_text_until, shows
from battle_pace import restore, snapshot
from battle_stats_return import battle_ready, start_battle
from cartridge_smoke import Game
from move_swap_smoke import (
    A, B, UP, DOWN, SELECT, START, CURSOR, SOURCE_MARKER, battle_row, hover, run_counter, wait_row,
)
from supply_and_move_info import press


TACKLE, TAIL_WHIP, DRAGON_RAGE, SPLASH, TRANSFORM = 0x21, 0x27, 0x52, 0x96, 0x90
MOVES = bytes((TACKLE, TAIL_WHIP, DRAGON_RAGE, SPLASH))
PP = bytes((35, 0x40, 0x82, 0xC7))  # zero, one, two and three PP Ups


def open_fight(game, moves=MOVES, pp=PP):
    # Use the player's own Pokémon so disobedience cannot replace a chosen move.
    game.put("wPartyMon1OTID", game.get_bytes("wPlayerID", 2))
    for mon in ("wPartyMon1", "wBattleMon"):
        game.put(mon + "Moves", moves)
        game.put(mon + "PP", pp)
    game.put("wEnemyMonMoves", (SPLASH, 0, 0, 0))
    game.put("wEnemyMonPP", (40, 0, 0, 0))
    press(game, A)
    wait_row(game, 1)


def stats(game, name, remaining, maximum, base):
    shows(game, name, "POW", "BASE")
    rows = [line.split() for line in game.visible_text().splitlines()]
    assert ["PP", str(remaining), str(maximum), "BASE", str(base)] in rows, rows


def battle_state(game):
    # Gen 1 Counter can read the selected move, its power/type, and wDamage.
    fields = (("wDamage", 2), ("wBattleMonMoves", 4), ("wBattleMonPP", 4),
              ("wPartyMon1Moves", 4), ("wPartyMon1PP", 4),
              ("wBattleMonHP", 2), ("wEnemyMonHP", 2), ("wEnemyMonPP", 4),
              ("wPlayerDisabledMove", 1), ("wMenuItemToSwap", 1),
              ("wPlayerMoveNum", 6), ("wPlayerUsedMove", 1), ("wEnemyUsedMove", 1))
    return hover(game), tuple(game.get_bytes(field, size) for field, size in fields)


def check_compare_and_choose(game):
    open_fight(game)
    before = battle_state(game)
    press(game, START)
    stats(game, "TACKLE", 35, 35, 35)
    press(game, UP)
    press(game, A)
    stats(game, "TACKLE", 35, 35, 35)
    press(game, SELECT)
    shows(game, "Deals damage")
    press(game, DOWN)
    shows(game, "TAIL WHIP", "Defense 1 stage")
    press(game, SELECT)
    stats(game, "TAIL WHIP", 0, 36, 30)
    press(game, B)
    wait_row(game, 2)
    assert battle_state(game) == before

    # A fresh A on the read-only zero-PP slot still triggers the stock refusal.
    press(game, A)
    shows(game, "No PP left")
    advance_text_until(game, lambda: "TAIL WHIP" in game.visible_text() and battle_row(game, 2) == CURSOR)
    wait_row(game, 2)
    assert game.get_bytes("wBattleMonPP", 4) == PP

    press(game, START)
    press(game, DOWN)
    stats(game, "DRAGON RAGE", 2, 14, 10)
    press(game, SELECT)
    shows(game, "Deals 40 damage")
    press(game, DOWN)
    shows(game, "SPLASH", "Has no effect")
    press(game, DOWN)
    shows(game, "SPLASH", "Has no effect")
    press(game, UP)
    shows(game, "DRAGON RAGE", "Deals 40 damage")
    press(game, DOWN)
    press(game, SELECT)
    stats(game, "SPLASH", 7, 61, 40)
    press(game, B)
    wait_row(game, 4)
    assert "7 61" in game.visible_text()
    assert game.get_bytes("wBattleMonPP", 4) == PP

    press(game, A)
    used = PP[:3] + bytes((0xC6,))
    advance_text_until(game, lambda: game.get_bytes("wBattleMonPP", 4) == used and battle_ready(game))
    assert game.get("wPlayerSelectedMove") == game.get("wPlayerUsedMove") == SPLASH
    assert game.get_bytes("wPartyMon1PP", 4) == used


def check_cancel_counter(game):
    open_fight(game)
    before = battle_state(game)
    press(game, START)
    press(game, DOWN)
    press(game, DOWN)
    stats(game, "DRAGON RAGE", 2, 14, 10)
    press(game, B)
    wait_row(game, 3)
    assert game.visible_text().splitlines()[10][2:10].strip() == "DRAGON"
    assert battle_state(game) == before
    press(game, B)
    game.wait(lambda: battle_ready(game))
    assert battle_state(game) == before
    # Tackle is counterable. The Dragon-type move the player read about is not.
    run_counter(game, expected_hit=True)


def check_pending_swap(game):
    open_fight(game)
    press(game, SELECT)
    game.wait(lambda: game.get("wMenuItemToSwap") == 1)
    before = battle_state(game)
    press(game, START)
    press(game, DOWN)
    press(game, DOWN)
    stats(game, "DRAGON RAGE", 2, 14, 10)
    press(game, B)
    wait_row(game, 3)
    assert battle_row(game, 1) == SOURCE_MARKER
    assert game.visible_text().splitlines()[10][2:10].strip() == "DRAGON"
    assert battle_state(game) == before
    press(game, SELECT)
    game.wait(lambda: game.get("wMenuItemToSwap") == 0)
    for mon in ("wPartyMon1", "wBattleMon"):
        assert game.get_bytes(mon + "Moves", 4) == bytes((DRAGON_RAGE, TAIL_WHIP, TACKLE, SPLASH))
        assert game.get_bytes(mon + "PP", 4) == bytes((0x82, 0x40, 35, 0xC7))


def check_disabled(game):
    open_fight(game)
    game.put("wPlayerDisabledMove", (0x35,))  # Slot three is disabled for five turns.
    before = battle_state(game)
    press(game, START)
    press(game, DOWN)
    press(game, DOWN)
    stats(game, "DRAGON RAGE", 2, 14, 10)

    # B wins over Down. A still-held direction must not reach the FIGHT list.
    for key in (B, DOWN):
        game.core.GB_set_key_state(game.gb, key, True)
    game.tick(20)
    game.core.GB_set_key_state(game.gb, B, False)
    game.tick(40)
    game.core.GB_set_key_state(game.gb, DOWN, False)
    wait_row(game, 3)
    shows(game, "disabled")
    assert battle_state(game) == before
    press(game, A)
    shows(game, "The move is", "disabled")
    assert game.get_bytes("wBattleMonPP", 4) == PP


def check_single_move(game):
    open_fight(game, bytes((SPLASH, 0, 0, 0)), bytes((2, 0, 0, 0)))
    press(game, START)
    press(game, DOWN)
    press(game, UP)
    stats(game, "SPLASH", 2, 40, 40)
    assert "UP DOWN" not in game.visible_text()
    press(game, B)
    wait_row(game, 1)


def check_transform(game):
    original = bytes((TRANSFORM, TACKLE, 0, 0))
    open_fight(game, original, bytes((10, 35, 0, 0)))
    copied = bytes((SPLASH, TAIL_WHIP, 0, 0))
    game.put("wEnemyMonMoves", copied)
    game.put("wEnemyMonPP", (40, 30, 0, 0))
    press(game, A)
    advance_text_until(game, lambda: game.get_bytes("wBattleMonMoves", 4) == copied and battle_ready(game))
    assert game.get_bytes("wBattleMonPP", 4) == bytes((5, 5, 0, 0))
    press(game, A)
    wait_row(game, 1)
    before = battle_state(game)
    press(game, START)
    shows(game, "SPLASH", "PP", "BASE")
    press(game, SELECT)
    press(game, DOWN)
    shows(game, "TAIL WHIP", "Defense 1 stage")
    press(game, DOWN)  # Two empty slots follow; neither is a move.
    shows(game, "TAIL WHIP", "Defense 1 stage")
    press(game, SELECT)
    stats(game, "TAIL WHIP", 5, 30, 30)
    press(game, B)
    wait_row(game, 2)
    assert battle_state(game) == before
    press(game, B)
    game.wait(lambda: battle_ready(game))
    assert hover(game) == before[0]
    assert game.get_bytes("wPartyMon1Moves", 4) == original


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        with Game(args.sameboy, args.boot, args.directory / f"poke{color}.gbc") as game:
            start_battle(game, tower=False, scoped=False)
            entered = snapshot(game)
            for check in (check_compare_and_choose, check_cancel_counter, check_pending_swap,
                          check_disabled, check_single_move, check_transform):
                restore(game, entered)
                check(game)
        print(f"{args.directory.name} {color}: FIGHT move comparison, swap and Transform passed", flush=True)


if __name__ == "__main__":
    main()
