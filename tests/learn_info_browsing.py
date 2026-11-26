"""Compare four known moves with an incoming move, then decline or replace one."""

import argparse
from pathlib import Path

from adventure_checkpoints import advance_text_until
from battle_exp_meter import threshold
from battle_pace import restore, select_start_item, snapshot
from battle_stats_return import battle_ready
from cartridge_smoke import Game, seed_party
from move_info_authoring import shows
from pc_browsing import name_bytes
from move_swap_smoke import A, B, DOWN, SELECT, START, UP
from tm_party_info import press

RIGHT, LEFT = 0, 1
PIDGEY, SQUIRTLE = 0x24, 0xB1
SWIFT, TOXIC, DOUBLE_TEAM, GUST, QUICK_ATTACK = 0x81, 0x5C, 0x68, 0x10, 0x62
TACKLE, TAIL_WHIP, WATER_GUN, SURF, MEGA_PUNCH = 0x21, 0x27, 0x37, 0x39, 0x05
TM01 = 0xC9


def moves_and_pp(game, mon):
    return game.get_bytes(mon + "Moves", 4), game.get_bytes(mon + "PP", 4)


def pending(game):
    advance_text_until(game, lambda: all(t in game.visible_text() for t in ("YES", "NO", "START INFO")))
    game.tick(16)


def info(game, name, role, description):
    # All five move names are visible. Verify which one the card describes.
    def matches():
        lines = game.visible_text().splitlines()
        return lines[11].split() == [role, *name.split()] and any(description in line for line in lines[12:17])

    game.wait(matches)


def at_forget_slot(game, slot):
    shows(game, "START INFO")
    game.wait(lambda: game.get("wCurrentMenuItem") == slot
              and game.get("wTileMap", (8 + slot) * 20 + 5) == 0xED)  # filled arrow


def close_while_holding(game, other):
    for key in (B, other):
        game.core.GB_set_key_state(game.gb, key, True)
    game.tick(12)
    game.core.GB_set_key_state(game.gb, B, False)
    game.tick(25)
    game.core.GB_set_key_state(game.gb, other, False)
    game.tick(18)


def check_level_up(game):
    # Win one ordinary Route 1 encounter one EXP short of Pidgey's level-12 move.
    game.put("wPartySpecies", (PIDGEY, 0x1B, 0xFF))
    game.put("wPartyMon1Species", (PIDGEY,))
    game.put("wPartyMon1Nick", name_bytes("BIRDA"))
    game.put("wPartyMon1OTID", game.get_bytes("wPlayerID", 2))
    game.put("wPartyMon1Level", (11,))
    game.put("wPartyMon1BoxLevel", (11,))
    game.put("wPartyMon1Exp", (threshold(3, 12) - 1).to_bytes(3, "big"))
    for stat in ("Attack", "Speed"):
        game.put("wPartyMon1" + stat, (0, 45))
    moves = bytes((SWIFT, TOXIC, DOUBLE_TEAM, GUST))
    game.put("wPartyMon1Moves", moves)
    game.put("wPartyMon1PP", (1, 0x4A, 0x89, 0xC7))
    game.enter_map(0x0C, 10, 5, 4)
    game.put("wCurOpponent", (PIDGEY,))
    game.put("wCurEnemyLevel", (2,))
    advance_text_until(game, lambda: battle_ready(game))
    press(game, A)
    shows(game, "SWIFT", "START INFO")
    press(game, A)
    pending(game)
    assert game.get("wPartyMon1Level") == 12 and game.get("wMoveNum") == QUICK_ATTACK
    pp = bytes((0, 0x4A, 0x89, 0xC7))  # Swift was spent on the knockout.
    party = moves_and_pp(game, "wPartyMon1")
    battler = moves_and_pp(game, "wBattleMon")
    assert party == battler == (moves, pp)
    unanswered = snapshot(game)

    # Open from NO; looking through every slot must leave that exact answer highlighted.
    press(game, DOWN)
    assert game.get("wCurrentMenuItem") == 1
    press(game, START)
    info(game, "QUICK ATTACK", "NEW", "PP 30")
    press(game, SELECT)
    info(game, "QUICK ATTACK", "NEW", "Goes before")
    for name, effect in (("SWIFT", "hit check"), ("TOXIC", "gets worse"),
                         ("DOUBLE TEAM", "Raises Evasion"), ("GUST", "Deals damage")):
        press(game, DOWN)
        info(game, name, "OLD", effect)
    press(game, DOWN)
    info(game, "GUST", "OLD", "Deals damage")
    press(game, RIGHT)
    info(game, "QUICK ATTACK", "NEW", "Goes before")
    press(game, A)  # Never answers the underlying question.
    press(game, UP)  # Revisiting a known move from NEW keeps the paired slot.
    info(game, "GUST", "OLD", "Deals damage")
    press(game, LEFT)
    info(game, "QUICK ATTACK", "NEW", "Goes before")
    press(game, RIGHT)
    info(game, "GUST", "OLD", "Deals damage")
    press(game, SELECT)
    info(game, "GUST", "OLD", "7 56")
    close_while_holding(game, UP)
    shows(game, "YES", "NO", "START INFO")
    assert game.get("wCurrentMenuItem") == 1
    assert moves_and_pp(game, "wPartyMon1") == party and moves_and_pp(game, "wBattleMon") == battler
    press(game, A)  # NO at the original question, then YES to stop learning.
    shows(game, "Abandon learning", "YES", "NO", accept=True)
    press(game, A)
    shows(game, "did not learn", "QUICK ATTACK", accept=True)
    assert moves_and_pp(game, "wPartyMon1") == party and moves_and_pp(game, "wBattleMon") == battler

    restore(game, unanswered)
    press(game, A)
    shows(game, "SWIFT", "GUST", "START INFO", accept=True)
    press(game, START)
    info(game, "SWIFT", "OLD", "0 20")
    press(game, UP)
    info(game, "SWIFT", "OLD", "0 20")
    press(game, DOWN)
    info(game, "TOXIC", "OLD", "10 12")
    press(game, DOWN)
    info(game, "DOUBLE TEAM", "OLD", "9 21")
    press(game, RIGHT)
    info(game, "QUICK ATTACK", "NEW", "PP 30")
    close_while_holding(game, A)  # Leave NEW without confirming the old move.
    shows(game, "SWIFT", "GUST", "START INFO")
    at_forget_slot(game, 2)
    assert moves_and_pp(game, "wPartyMon1") == party and moves_and_pp(game, "wBattleMon") == battler
    press(game, A)
    shows(game, "learned", "QUICK ATTACK", accept=True)
    expected = (bytes((SWIFT, TOXIC, QUICK_ATTACK, GUST)), bytes((0, 0x4A, 30, 0xC7)))
    assert moves_and_pp(game, "wPartyMon1") == moves_and_pp(game, "wBattleMon") == expected


def check_tm(game):
    # TM01 is used on the second party member so the lead cannot supply its moves or PP.
    game.put("wPartySpecies", (0x69, SQUIRTLE, 0xFF))
    game.put("wPartyMon2Species", (SQUIRTLE,))
    game.put("wPartyMon2Nick", name_bytes("SQUIRTLE"))
    game.put("wPartyMon2Moves", (TACKLE, TAIL_WHIP, WATER_GUN, SURF))
    game.put("wPartyMon2PP", (0x47, 0, 0x82, 0xC3))
    bag = bytes((1, TM01, 1, 0xFF))
    game.put("wNumBagItems", bag)
    game.enter_map(0x0C, 10, 5, 4)
    select_start_item(game, 1)
    shows(game, "TM01", "START INFO")
    press(game, A)
    shows(game, "USE", accept=True)
    press(game, A)
    pending(game)
    press(game, START)
    shows(game, "MEGA PUNCH", "POW", "PP 20")
    press(game, DOWN)
    shows(game, "MEGA PUNCH", "POW", "PP 20")
    assert "OLD" not in game.visible_text()  # No pupil has been selected yet.
    press(game, B)
    shows(game, "YES", "NO", "START INFO")
    press(game, A)
    shows(game, "Use TM on which", "SQUIRTLE", accept=True)
    press(game, DOWN)
    press(game, A)
    pending(game)
    assert game.get("wWhichPokemon") == 1
    lead = moves_and_pp(game, "wPartyMon1")
    pupil = moves_and_pp(game, "wPartyMon2")

    press(game, START)
    info(game, "MEGA PUNCH", "NEW", "PP 20")
    press(game, LEFT)
    info(game, "TACKLE", "OLD", "7 42")
    press(game, DOWN)
    info(game, "TAIL WHIP", "OLD", "0 30")
    press(game, B)
    shows(game, "YES", "NO", "START INFO")
    assert game.get("wCurrentMenuItem") == 0
    press(game, A)
    shows(game, "TACKLE", "SURF", "START INFO", accept=True)
    press(game, DOWN)
    press(game, START)
    info(game, "TAIL WHIP", "OLD", "0 30")
    press(game, DOWN)
    info(game, "WATER GUN", "OLD", "2 35")
    press(game, DOWN)
    info(game, "SURF", "OLD", "3 24")
    press(game, RIGHT)
    info(game, "MEGA PUNCH", "NEW", "PP 20")
    press(game, B)
    shows(game, "TACKLE", "SURF", "START INFO")
    at_forget_slot(game, 3)
    press(game, A)
    shows(game, "HM", "delete", accept=True)
    assert moves_and_pp(game, "wPartyMon2") == pupil and game.get_bytes("wNumBagItems", 4) == bag
    shows(game, "TACKLE", "SURF", "START INFO", accept=True)
    press(game, START)
    press(game, DOWN)
    press(game, DOWN)
    info(game, "WATER GUN", "OLD", "2 35")
    press(game, B)
    shows(game, "TACKLE", "SURF", "START INFO")
    at_forget_slot(game, 2)
    assert moves_and_pp(game, "wPartyMon2") == pupil
    assert game.get_bytes("wNumBagItems", 4) == bag
    press(game, A)
    game.wait(lambda: game.get("wNumBagItems") == 0, accept=True)
    assert moves_and_pp(game, "wPartyMon2") == (bytes((TACKLE, TAIL_WHIP, MEGA_PUNCH, SURF)),
                                               bytes((0x47, 0, 20, 0xC3)))
    assert moves_and_pp(game, "wPartyMon1") == lead


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        with Game(args.sameboy, args.boot, args.directory / f"poke{color}.gbc") as game:
            game.new_game()
            seed_party(game)
            game.put("wOptions", (0xC1,))
            start = snapshot(game)
            check_level_up(game)
            restore(game, start)
            check_tm(game)
        print(f"{args.directory.name} {color}: level-up and TM learning comparisons passed", flush=True)


if __name__ == "__main__":
    main()
