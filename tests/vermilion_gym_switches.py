"""Check every possible adjacent switch draw and the gym's A-button flow."""

import argparse
from collections import Counter
from pathlib import Path

from adventure_checkpoints import event, set_event
from cartridge_smoke import Game
from celadon_roof_transactions import finish


GYM, VERMILION = 0x5C, 0x05
SECOND_LOCK, FIRST_LOCK = 0x160, 0x161
FIRST_TRAINER, LAST_TRAINER = 0x162, 0x164
A = 4


def clear_locks(game):
    offset = SECOND_LOCK // 8
    address = game.addresses["wEventFlags"][1] + offset
    game.write(address, (game.get("wEventFlags", offset) & ~3,))


def neighbors(can):
    x, y = divmod(can, 3)
    return {
        3 * other_x + other_y
        for other_x, other_y in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
        if 0 <= other_x < 5 and 0 <= other_y < 3
    }


def draw_second_switch(game, first, draw):
    clear_locks(game)
    game.put("wFirstLockTrashCanIndex", (first,))
    game.put("wHiddenEventFunctionArgument", (first,))
    game.invoke("GymTrashScript")
    game.write(0xFFFF, (0,))  # Keep VBlank's unrelated random draws out of this check.
    random = game.addresses["Random"][1]
    done = game.addresses["GymTrashScript.done"][1]
    calls = 0
    for _ in range(500):
        if game.cpu.pc == done:
            assert event(game, FIRST_LOCK) and not event(game, SECOND_LOCK)
            return game.get("wSecondLockTrashCanIndex"), calls
        if game.cpu.pc == random:
            # Return a controlled byte from the real call site. A retry gets zero.
            stack = game.cpu.sp
            low = game.core.GB_safe_read_memory(game.gb, stack)
            high = game.core.GB_safe_read_memory(game.gb, stack + 1)
            game.cpu.pc = low | high << 8
            game.cpu.sp += 2
            game.cpu.af = (draw if calls == 0 else 0) << 8
            calls += 1
        game.core.GB_run(game.gb)
    raise AssertionError(f"The switch draw did not finish for can {first}, byte {draw:02x}.")


def check_every_draw(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        for first in range(0, 15, 2):  # Stock's first-lock sampler chooses even indices.
            allowed = neighbors(first)
            seen = Counter()
            for draw in range(256):
                second, calls = draw_second_switch(game, first, draw)
                seen[second] += 1
                assert calls == (2 if draw == 255 and len(allowed) == 3 else 1)
            assert set(seen) == allowed, (first, seen, allowed)
            assert max(seen.values()) - min(seen.values()) <= 1


def aim_at_can(game, can):
    column, row = divmod(can, 3)
    game.enter_map(GYM, 5, 2 + 2 * column, 7 + 2 * row, last_map=VERMILION)
    game.put("wSpritePlayerStateData1FacingDirection", (8,))  # Left.


def door_block(game):
    return game.get("wOverworldMap", 5 * 11 + 5)


def check_door(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        game.put("wOptions", (1,))
        for trainer in range(FIRST_TRAINER, LAST_TRAINER + 1):
            set_event(game, trainer)

        # Check the first can, then deliberately check it again for the second lock.
        aim_at_can(game, 4)
        game.put("wFirstLockTrashCanIndex", (4,))
        game.press(A)
        finish(game, ("1st electric", "lock opened"))
        assert event(game, FIRST_LOCK) and not event(game, SECOND_LOCK)
        assert game.get("wSecondLockTrashCanIndex") in neighbors(4)
        game.press(A)
        finish(game, ("locks were reset",))
        assert not event(game, FIRST_LOCK) and not event(game, SECOND_LOCK)
        assert door_block(game) == 0x24
        assert game.get("wFirstLockTrashCanIndex") in range(0, 15, 2)

        game.put("wFirstLockTrashCanIndex", (4,))
        game.press(A)
        finish(game, ("1st electric", "lock opened"))
        second = game.get("wSecondLockTrashCanIndex")
        assert second in neighbors(4)
        aim_at_can(game, second)
        game.press(A)
        finish(game, ("motorized door", "opened"))
        game.wait(lambda: door_block(game) == 5)
        assert event(game, FIRST_LOCK) and event(game, SECOND_LOCK)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        fixture = args.sameboy, args.boot, args.directory / f"poke{color}.gbc"
        check_every_draw(*fixture)
        check_door(*fixture)
        print(f"{color.title()}: adjacent gym switches and door progression passed", flush=True)


if __name__ == "__main__":
    main()
