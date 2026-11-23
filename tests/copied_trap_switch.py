"""Check PP and copied trapping moves when an opponent switches over a cable."""

import argparse
from pathlib import Path

from cartridge_smoke import Game
from link_cable_smoke import (
    A, COLOSSEUM, DOWN, RIGHT, Cable, choose_room, in_battle_commands, setup_player,
    use_table_game_boys,
)


WRAP, METRONOME, MIRROR_MOVE, SWIFT = 0x23, 0x76, 0x77, 0x81
TRAPPING = 1 << 5
HP, LAST_PP, EMPTY_PP = 160, 0xC1, 0xC0
MOVES = {"wrap": WRAP, "metronome": METRONOME, "mirror-move": MIRROR_MOVE}


def random_bytes(cable, *values):
    for game in cable.players:
        game.put("wLinkBattleRandomNumberList", bytes(values).ljust(9, b"\xff"))
        game.put("wLinkBattleRandomNumberListIndex", (0,))


def hp(game, mon):
    return int.from_bytes(game.get_bytes(mon + "HP", 2), "big")


def setup_rosters(left, right, attacker, defender, move):
    setup_player(left, "BLUE", 0x69, "RIVER", (0x12, 0x34), SWIFT, 20)
    setup_player(right, "GREEN", 0x1B, "STAR", (0x56, 0x78), SWIFT, 20)
    attacker.put("wPartyMon1Moves", (move, SWIFT, 0, 0))
    attacker.put("wPartyMon1PP", (LAST_PP, 20, 0, 0))
    attacker.put("wPartyMon1Speed", (0, 120))
    length = defender.addresses["wPartyMon2Species"][1] - defender.addresses["wPartyMon1Species"][1]
    defender.put("wPartyMon2Species", defender.get_bytes("wPartyMon1Species", length))
    old_species = defender.get("wPartyMon1Species")
    new_species = 0x69 if old_species == 0x1B else 0x1B
    defender.put("wPartySpecies", (old_species, new_species, 0xFF))
    defender.put("wPartyMon2Species", (new_species,))
    defender.put("wPartyMon2Nick", bytes((0x92, 0x8F, 0x80, 0x91, 0x84, 0x50)))
    defender.put("wPartyCount", (2,))


def check_first_attack(cable, attacker, defender, move):
    if move == MIRROR_MOVE:
        attacker.put("wEnemyUsedMove", (WRAP,))
        defender.put("wPlayerUsedMove", (WRAP,))
    pick = (WRAP,) if move == METRONOME else ()
    random_bytes(cable, *pick, 0, 255, 255, 0)
    cable.tick(24)
    cable.press(A, *cable.players)
    cable.wait(lambda: all(game.get("wTopMenuItemY") == 12 for game in cable.players),
               "both FIGHT menus")
    cable.tick(24)
    cable.press(A, *cable.players)
    cable.wait(lambda: all(in_battle_commands(game) for game in cable.players)
               and bool(attacker.get("wPlayerBattleStatus1") & TRAPPING),
               "the first hit and trapping state", frames=2400)
    assert defender.get("wEnemyBattleStatus1") & TRAPPING
    assert 0 < hp(attacker, "wEnemyMon") == hp(defender, "wBattleMon") < HP
    assert hp(attacker, "wBattleMon") == HP
    assert attacker.get("wBattleMonPP") == attacker.get("wPartyMon1PP") == EMPTY_PP
    assert attacker.get("wPlayerUsedMove") == defender.get("wEnemyUsedMove") == WRAP


def switch_while_trapped(cable, attacker, defender):
    cable.tick(24)
    # The trapper's FIGHT command goes straight to the pending link exchange.
    cable.press(A, attacker)
    cable.press(RIGHT, defender)
    cable.wait(lambda: defender.get("wTopMenuItemX") == 15, "the party command")
    cable.tick(12)
    cable.press(A, defender)
    cable.wait(lambda: "SPARE" in defender.visible_text(), "the reserve Pokémon")
    cable.tick(24)
    cable.press(DOWN, defender)
    cable.wait(lambda: defender.get("wLastMenuItem") == 1, "the reserve cursor")
    cable.press(A, defender)
    cable.wait(lambda: "SWITCH" in defender.visible_text(), "the Switch action")
    cable.tick(12)
    cable.press(A, defender)
    cable.wait(lambda: all(in_battle_commands(game) for game in cable.players)
               and defender.get("wPlayerMonNumber") == 1
               and attacker.get("wEnemyMonPartyPos") == 1,
               "the completed switch round", frames=2400)


def case(library, boot, rom, *, attacker_index, move):
    with Game(library, boot, rom) as left, Game(library, boot, rom) as right:
        pair = (left, right)
        attacker, defender = pair[attacker_index], pair[1 - attacker_index]
        setup_rosters(left, right, attacker, defender, move)
        with Cable(left, right) as cable:
            choose_room(cable, COLOSSEUM)
            use_table_game_boys(cable)
            cable.wait(lambda: all(in_battle_commands(game) for game in cable.players),
                       "both opening battle command menus", frames=2400)
            check_first_attack(cable, attacker, defender, move)
            if move == METRONOME:
                random_bytes(cable, SWIFT, 255, 255)
            else:
                random_bytes(cable, 1, 255, 255, 0)
            switch_while_trapped(cable, attacker, defender)
            assert hp(attacker, "wBattleMon") == HP
            return {
                "pp": (attacker.get("wBattleMonPP"), attacker.get("wPartyMon1PP")),
                "reserve_hp": (hp(attacker, "wEnemyMon"), hp(defender, "wBattleMon")),
                "last_move": (attacker.get("wPlayerUsedMove"), defender.get("wEnemyUsedMove")),
                "trapping": (bool(attacker.get("wPlayerBattleStatus1") & TRAPPING),
                             bool(defender.get("wEnemyBattleStatus1") & TRAPPING)),
                "draws": (attacker.get("wLinkBattleRandomNumberListIndex"),
                          defender.get("wLinkBattleRandomNumberListIndex")),
            }


def check_result(result, move, core):
    wanted_pp = EMPTY_PP if core else 0xBF
    assert result["pp"] == (wanted_pp, wanted_pp), result
    local_hp, remote_hp = result["reserve_hp"]
    if move == MIRROR_MOVE:
        if core:
            assert local_hp == remote_hp == HP, result
            assert result["last_move"] == (MIRROR_MOVE, MIRROR_MOVE), result
            assert result["trapping"] == (False, False), result
            assert result["draws"] == (0, 0), result
        else:
            assert 0 < local_hp < remote_hp == HP, result
            assert result["last_move"] == (WRAP, MIRROR_MOVE), result
            assert result["trapping"] == (True, False), result
            assert result["draws"] == (4, 0), result
    elif move == METRONOME:
        assert 0 < local_hp == remote_hp < HP, result
        assert result["last_move"] == (SWIFT, SWIFT), result
        assert result["trapping"] == (False, False), result
        assert result["draws"] == (3, 3), result
    else:
        assert 0 < local_hp == remote_hp < HP, result
        assert result["last_move"] == (WRAP, WRAP), result
        assert result["trapping"] == (True, True), result
        assert result["draws"] == (4, 4), result


def check_pp_bytes(library, boot, rom, core):
    with Game(library, boot, rom) as game:
        game.new_game()
        game.put("wPlayerSelectedMove", (WRAP,))
        game.put("wPlayerMonNumber", (0,))
        game.put("wPlayerMoveListIndex", (1,))
        for offset in (1, 2, 3):
            game.put(f"wPlayerBattleStatus{offset}", (0,))
        for starting, ending in (
            (1, 0), (0xC1, 0xC0), (0, 0 if core else 255), (0xC0, 0xC0 if core else 0xBF),
        ):
            game.put("wBattleMonPP", (9, starting, 8, 0))
            game.put("wPartyMon1PP", (9, starting, 8, 0))
            game.invoke("DecrementPP")
            game.cpu.de = game.addresses["wPlayerSelectedMove"][1]
            game.return_to_stub()
            wanted = bytes((9, ending, 8, 0))
            assert game.get_bytes("wBattleMonPP", 4) == wanted
            assert game.get_bytes("wPartyMon1PP", 4) == wanted


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--move", choices=MOVES, nargs="+")
    parser.add_argument("--seat", type=int, choices=(0, 1), nargs="+")
    args = parser.parse_args()
    core = args.rom.parent.name == "core"
    check_pp_bytes(args.sameboy, args.boot, args.rom, core)
    for seat in args.seat or (0, 1):
        for move in args.move or MOVES:
            result = case(args.sameboy, args.boot, args.rom, attacker_index=seat, move=MOVES[move])
            check_result(result, MOVES[move], core)
            print(f"{args.rom.parent.name} {move}, cable seat {seat}: {result}", flush=True)


if __name__ == "__main__":
    main()
