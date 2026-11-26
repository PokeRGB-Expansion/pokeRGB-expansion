"""Check Core's optional battle pacing through OPTIONS and a live battle."""

import argparse
import ctypes as C
from pathlib import Path

from acid_armor import invoke_visual
from adventure_checkpoints import advance_text_until
from battle_stats_return import battle_ready, start_battle
from cartridge_smoke import Game, seed_party


RIGHT, UP, DOWN, A, B, START = 0, 2, 3, 4, 5, 7
QUICK = 1 << 4
LINK_BATTLE = 4
SEISMIC_TOSS, SPLASH = 0x45, 0x96


def select_start_item(game, index):
    game.press(START)
    game.wait(lambda: "OPTION" in game.visible_text())
    game.tick(20)
    for _ in range(7):
        if game.get("wCurrentMenuItem") == index:
            break
        game.press(DOWN)
        game.tick(12)
    assert game.get("wCurrentMenuItem") == index
    game.press(A)


def menu_and_save(game, core):
    game.new_game()
    seed_party(game)
    game.enter_map(12, 10, 5, 4)
    options = game.get("wOptions")
    assert not options & QUICK
    select_start_item(game, 4)  # OPTION without the Pokédex
    game.wait(lambda: "CANCEL" in game.visible_text())
    assert ("BATTLE PACE" in game.visible_text()) == core
    if core:
        game.wait(lambda: "QUICK" in game.visible_text())
        game.tick(20)
        for _ in range(3):
            game.press(DOWN)
            game.tick(12)
        game.press(RIGHT)
        game.wait(lambda: game.get("wOptions") == options | QUICK)
        # Keep the chosen pace when another option is edited.
        game.press(UP)
        game.tick(12)
        game.press(RIGHT)
        game.wait(lambda: game.get("wOptions") == (options ^ 0x40) | QUICK)
    game.press(B)
    game.wait(lambda: "OPTION" in game.visible_text())
    game.tick(12)
    game.press(B)
    game.tick(35)
    select_start_item(game, 3)  # SAVE
    game.wait(lambda: "YES" in game.visible_text(), accept=True)
    game.press(A)
    game.wait(lambda: "saved" in game.visible_text(), accept=True)
    game.tick(110)
    return bytes(game.battery()), game.get("wOptions")


def snapshot(game):
    ptr = C.c_void_p
    buf = C.POINTER(C.c_uint8)
    game.core.GB_get_save_state_size.argtypes = [ptr]
    game.core.GB_get_save_state_size.restype = C.c_size_t
    game.core.GB_save_state_to_buffer.argtypes = [ptr, buf]
    game.core.GB_save_state_to_buffer.restype = None
    game.core.GB_load_state_from_buffer.argtypes = [ptr, buf, C.c_size_t]
    game.core.GB_load_state_from_buffer.restype = C.c_int
    state = (C.c_uint8 * game.core.GB_get_save_state_size(game.gb))()
    game.core.GB_save_state_to_buffer(game.gb, state)
    return state


def restore(game, state):
    assert game.core.GB_load_state_from_buffer(game.gb, state, len(state)) == 0


def time_damage_pause(game, quick, *, link=0, battle_type=0):
    # Enter the real post-hit text routine with no critical hit or OHKO.
    game.put("wOptions", (0xc1 | (QUICK if quick else 0),))
    game.put("wLinkState", (link,))
    game.put("wBattleType", (battle_type,))
    game.put("wCriticalHitOrOHKO", (0,))
    stop = invoke_visual(game, "PrintCriticalOHKOText")
    returned = None
    music = []
    for frame in range(1, 65):
        game.tick()
        if returned is None and game.cpu.pc == stop:
            returned = frame
        music.append((
            game.get_bytes("wChannelCommandPointers", 8),  # four music tracks
            game.get_bytes("wChannelNoteDelayCounters", 4),
            game.get_bytes("wChannelFrequencyLowBytes", 4),
            game.get("wPlayTimeFrames"),
        ))
    assert returned is not None
    assert len({sample[0] for sample in music}) > 1
    return returned, music


def play_turn(game, quick):
    game.put("wOptions", (0xc1 | (QUICK if quick else 0),))
    game.put("wBattleMonMoves", (SEISMIC_TOSS, 0, 0, 0))
    game.put("wBattleMonPP", (20, 0, 0, 0))
    game.put("wBattleMonLevel", (5,))
    game.put("wPlayerBattleStatus2", (1,))  # X Accuracy removes the miss roll.
    game.put("wEnemyMonMoves", (SPLASH, 0, 0, 0))
    game.put("wEnemyMonPP", (40, 0, 0, 0))
    game.put("wEnemyMonHP", (0, 29))
    game.put("wEnemyMonMaxHP", (0, 29))
    game.tick(15)
    game.press(A)
    game.wait(lambda: "SEISMIC TOSS" in game.visible_text())
    game.tick(15)
    for _ in range(30):
        game.tick()
        assert "SEISMIC TOSS" in game.visible_text()
        assert game.get("wBattleMonPP") == 20
    game.press(A)
    # Only acknowledge existing battle text. Stop at the next command menu.
    for frames in range(1, 1500):
        if battle_ready(game):
            break
        game.core.GB_set_key_state(game.gb, A, frames % 8 < 2)
        game.tick()
    else:
        raise AssertionError(game.visible_text())
    game.core.GB_set_key_state(game.gb, A, False)
    assert game.get_bytes("wEnemyMonHP", 2) == bytes((0, 24))
    assert game.get("wBattleMonPP") == 19
    assert game.get("wBattleResult") == 0
    return frames


def check_battle(game, core):
    start_battle(game, tower=False, scoped=False)
    game.tick(30)
    state = snapshot(game)
    normal, music = time_damage_pause(game, False)
    restore(game, state)
    quick, fast_music = time_damage_pause(game, True)
    assert normal - quick == (15 if core else 0), (normal, quick)
    assert fast_music == music
    for link, special in ((LINK_BATTLE, 0), (0, 1), (0, 2)):
        restore(game, state)
        control, _ = time_damage_pause(game, True, link=link, battle_type=special)
        assert control == normal, (link, special, normal, control)
    restore(game, state)
    normal_turn = play_turn(game, False)
    restore(game, state)
    quick_turn = play_turn(game, True)
    if core:
        assert quick_turn < normal_turn
    else:
        assert quick_turn == normal_turn
    return normal_turn, quick_turn


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    core = args.directory.name == "core"
    for color in ("red", "blue", "green"):
        fixture = args.sameboy, args.boot, args.directory / f"poke{color}.gbc"
        with Game(*fixture) as game:
            battery, chosen = menu_and_save(game, core)
        with Game(*fixture) as game:
            game.battery()[:] = battery
            game.tick(440)
            game.press(START)
            advance_text_until(game, lambda: "CONTINUE" in game.visible_text())
            game.press(A)
            game.tick(85)
            game.press(A)
            game.tick(180)
            assert game.get("wCurMap") == 12 and game.get("wPartyCount") == 2
            assert game.get("wOptions") == chosen and bool(chosen & QUICK) == core
        with Game(*fixture) as game:
            normal, quick = check_battle(game, core)
        print(f"{args.directory.name} {color}: pace option and audio passed "
              f"({normal}/{quick} frames for the same turn)", flush=True)


if __name__ == "__main__":
    main()
