"""Check fainting cleanup over a cable and Struggle at the FIGHT menu."""

import argparse
import ctypes as C
from pathlib import Path

from cartridge_smoke import Game
from link_cable_smoke import Cable, COLOSSEUM, choose_room, in_battle_commands, setup_player
from link_cable_smoke import use_table_game_boys
from protected_mechanics import (
    ENEMY, HP, NIGHT_SHADE, PLAYER, SWIFT, act, call, choose_first_move, put_stat,
    random_bytes, seed_actions, stat,
)


A, B = 4, 5
STRUGGLE = 0xA5
LINK_STRUGGLE = 0x0E
MOVES = (0x21, 0x0A, 0x34, 0x37)  # Tackle, Scratch, Ember, Water Gun.
STORED_DAMAGE = bytes((1, 0x25))
EXECUTION_CALLBACK = C.CFUNCTYPE(None, C.c_void_p, C.c_uint16, C.c_uint8)


def setup_pp(game, disabled_slot, bonus, usable_slot=None):
    seed_actions(game, PLAYER, SWIFT)
    pp = [bonus] * len(MOVES)
    if disabled_slot is not None:
        pp[disabled_slot] |= 10
        game.put("wPlayerDisabledMove", ((disabled_slot + 1) << 4 | 3,))
        game.put("wPlayerDisabledMoveNumber", (MOVES[disabled_slot],))
    if usable_slot is not None:
        pp[usable_slot] |= 1
    pp = bytes(pp)
    game.put("wBattleMonMoves", MOVES)
    game.put("wPartyMon1Moves", MOVES)
    game.put("wBattleMonPP", pp)
    game.put("wPartyMon1PP", pp)
    game.put("wNumMovesMinusOne", (3,))
    game.put("wMoveMenuType", (0,))
    game.put("wMenuItemToSwap", (0,))
    game.put("wTileMap", b"\x7F" * 360)
    return pp


def wait_for_fight_menu(game):
    game.wait(lambda: game.get("wTopMenuItemY") == 12 and "TACKLE" in game.visible_text())
    game.tick(16)


def check_menu(game, core, disabled_slot, bonus, usable_slot=None):
    has_move = usable_slot is not None
    slot = usable_slot if has_move else next(number for number in range(len(MOVES))
                                             if number != disabled_slot)
    pp = setup_pp(game, disabled_slot, bonus, usable_slot)
    game.put("wPlayerMoveListIndex", (slot,))
    game.invoke("MoveSelectionMenu")
    metadata_bug = not core and bonus and disabled_slot is not None
    if not has_move and not metadata_bug:
        game.wait(lambda: "moves left" in game.visible_text())
        game.return_to_stub()
        assert game.cpu.af & 0x80
        assert game.get("wPlayerSelectedMove") == STRUGGLE
    else:
        wait_for_fight_menu(game)
        assert game.get("wCurrentMenuItem") == slot + 1
        if has_move:
            game.press(A)
            game.return_to_stub()
            assert game.cpu.af & 0x80
            assert game.get("wPlayerSelectedMove") == MOVES[slot]
        else:
            if disabled_slot == 0 and bonus == 0x40:
                game.press(A)
                game.wait(lambda: "No PP left" in game.visible_text())
                game.tick(24)
                game.press(A)
                wait_for_fight_menu(game)
            game.press(B)
            game.return_to_stub()
            assert not (game.cpu.af & 0x80)
    assert game.get_bytes("wBattleMonPP", 4) == pp
    assert game.get_bytes("wPartyMon1PP", 4) == pp


def check_struggle(game, core):
    for disabled in (None, 0, 1, 2, 3):
        for bonus in (0, 0x40, 0x80, 0xC0):
            check_menu(game, core, disabled, bonus)
            for slot in range(len(MOVES)):
                if slot != disabled:
                    check_menu(game, core, disabled, bonus, usable_slot=slot)

    # Complete a forced attack after the FIGHT menu has chosen Struggle.
    check_menu(game, core, 0, 0xC0 if core else 0)
    before = game.get_bytes("wBattleMonPP", 4)
    random_bytes(game, 255, 255, 0)
    act(game, PLAYER)
    assert game.get("wPlayerUsedMove") == STRUGGLE
    assert game.get_bytes("wBattleMonPP", 4) == before
    assert game.get_bytes("wPartyMon1PP", 4) == before
    assert 0 < stat(game, ENEMY, "HP") < HP and 0 < stat(game, PLAYER, "HP") < HP

    # A remote Struggle command attacks and recoils without spending enemy PP.
    seed_actions(game, ENEMY, STRUGGLE)
    game.put("wSerialExchangeNybbleReceiveData", (LINK_STRUGGLE,))
    game.put("wEnemyMonPP", (0x80, 0, 0, 0))
    random_bytes(game, 255, 255, 0)
    act(game, ENEMY)
    assert game.get("wEnemyUsedMove") == STRUGGLE
    assert game.get_bytes("wEnemyMonPP", 4) == bytes((0x80, 0, 0, 0))
    assert 0 < stat(game, ENEMY, "HP") < HP and 0 < stat(game, PLAYER, "HP") < HP

    seed_actions(game, ENEMY, SWIFT)
    game.put("wLinkState", (0,))
    game.put("wIsInBattle", (1,))
    game.put("wEnemyMonPP", (0, 0, 0, 0))
    call(game, "SelectEnemyMove")
    assert game.get("wEnemySelectedMove") == SWIFT


def record_faint(game, side, entry):
    field = f"w{side}BideAccumulatedDamage"
    target = game.addresses[entry]
    slide = game.addresses["SlideDownFaintedMonPic"]
    trace = []

    @EXECUTION_CALLBACK
    def sample(_, pc, _opcode):
        if pc in (target[1], slide[1]):
            address = game.get("hLoadedROMBank"), pc
            if address == target:
                trace.append(("before", game.get_bytes(field, 2)))
            elif address == slide and len(trace) == 1:
                trace.append(("after", game.get_bytes(field, 2)))

    setter = game.core.GB_set_execution_callback
    setter.argtypes = [C.c_void_p, EXECUTION_CALLBACK]
    setter.restype = None
    setter(game.gb, sample)
    return trace, sample


def check_bide_link(library, boot, rom, seat, core):
    with Game(library, boot, rom) as left, Game(library, boot, rom) as right:
        setup_player(left, "BLUE", 0x69, "RIVER", (0x12, 0x34), SWIFT, 20)
        setup_player(right, "GREEN", 0x1B, "STAR", (0x56, 0x78), SWIFT, 20)
        players = (left, right)
        winner, loser = players[seat], players[1 - seat]
        winner.put("wPartyMon1Moves", (NIGHT_SHADE, SWIFT, 0, 0))
        winner.put("wPartyMon1PP", (15, 20, 0, 0))
        winner.put("wPartyMon1Speed", (0, 120))
        with Cable(left, right) as cable:
            choose_room(cable, COLOSSEUM)
            use_table_game_boys(cable)
            cable.wait(lambda: all(in_battle_commands(game) for game in players),
                       "both battle menus", frames=2400)
            put_stat(winner, ENEMY, "HP", 1)
            put_stat(loser, PLAYER, "HP", 1)
            for game in players:
                random_bytes(game, 0)
            # The surviving battler has the same stored damage on both Game Boys.
            # Observe it when the faint routine starts and before the slide animation.
            winner.put("wPlayerBideAccumulatedDamage", STORED_DAMAGE)
            loser.put("wEnemyBideAccumulatedDamage", STORED_DAMAGE)
            # Keep both callback objects alive until the traces complete.
            winner_trace, winner_callback = record_faint(winner, PLAYER, "FaintEnemyPokemon")
            loser_trace, loser_callback = record_faint(loser, ENEMY, "RemoveFaintedPlayerMon")
            try:
                choose_first_move(cable, *players)
                cable.wait(lambda: len(winner_trace) >= 2 and len(loser_trace) >= 2,
                           "the faint animation on both Game Boys", frames=1500)
            finally:
                for game in players:
                    game.core.GB_set_execution_callback(game.gb, EXECUTION_CALLBACK())
            expected_player = bytes(2) if core else bytes((0, STORED_DAMAGE[1]))
            assert winner_trace == [("before", STORED_DAMAGE), ("after", expected_player)], (
                seat, winner_trace
            )
            assert loser_trace == [("before", STORED_DAMAGE), ("after", bytes(2))], (
                seat, loser_trace
            )
            cable.wait(lambda: all(game.get("wLinkState") == 1 and not game.get("wIsInBattle")
                                   for game in players), "both games to return to the Colosseum",
                       frames=1500)
            assert winner.get("wBattleResult") == 0 and loser.get("wBattleResult") == 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--color", choices=("red", "blue", "green"), nargs="+")
    parser.add_argument("--linked", action="store_true", help="Run Bide's live cable cases.")
    args = parser.parse_args()
    core = args.directory.name == "core"
    for color in args.color or ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        with Game(args.sameboy, args.boot, rom) as game:
            game.new_game()
            check_struggle(game, core)
        print(f"{args.directory.name} {color}: Struggle and PP controls passed", flush=True)
    if args.linked:
        color = (args.color or ("red",))[0]
        rom = args.directory / f"poke{color}.gbc"
        for seat in (0, 1):
            check_bide_link(args.sameboy, args.boot, rom, seat, core)
            print(f"{args.directory.name} {color}: Bide faint reset passed in cable seat {seat}",
                  flush=True)


if __name__ == "__main__":
    main()
