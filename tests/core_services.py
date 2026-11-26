"""Exercise the Fuchsia Move Deleter and field EXP.ALL switch in game."""

import argparse
from pathlib import Path

from adventure_checkpoints import advance_text_until
from battle_stats_return import battle_ready
from cartridge_smoke import Game, seed_party
from exp_all import AwardCase, EXP_ALL, START_EXP, START_STAT_EXP, expected_shares, seed_award
from interrupted_save_smoke import booted_game
from pc_browsing import name_bytes


RIGHT, LEFT, UP, DOWN, A, B, START = 0, 1, 2, 3, 4, 5, 7
FUCHSIA, DELETER_HOUSE = 7, 0xF8
EXP_BAG = bytes((1, EXP_ALL, 1, 0xFF))
MOVES = bytes((0x0F, 0x21, 0x39, 0x62))  # Cut, Tackle, Surf, Quick Attack
PP = bytes((0xA1, 0x55, 0x8F, 0xC9))  # Include PP Up counts and partly used moves.


def press(game, button, frames=24):
    game.press(button)
    game.tick(frames)


def wait_text(game, *words):
    advance_text_until(game, lambda: all(word in game.visible_text() for word in words))
    game.tick(16)


def check_house(game, core):
    game.new_game()
    seed_party(game)
    game.put("wOptions", (0xC1,))
    game.put("wPartyMon1Nick", name_bytes("LEAFCUTTER"))
    game.put("wPartyMon1Moves", MOVES)
    game.put("wPartyMon1PP", PP)
    game.enter_map(FUCHSIA, 20, 15, 28)
    press(game, UP, 110)
    if not core:
        assert game.get("wCurMap") == FUCHSIA and game.get("wYCoord") == 28
        return
    assert (game.get("wCurMap"), game.get("wXCoord"), game.get("wYCoord")) == (DELETER_HOUSE, 2, 7)
    for key in (UP, RIGHT, RIGHT, RIGHT, UP):  # Walk to the NPC and face him.
        press(game, key, 35)

    def choose_mon(member=0):
        press(game, A)
        wait_text(game, "YES", "NO")
        press(game, A)
        wait_text(game, "160 160")
        game.tick(35)
        if game.get("wCurrentMenuItem") != member:
            press(game, DOWN if member else UP)
        press(game, A)

    def close_dialogue():
        for _ in range(5):
            press(game, B)

    def select_move(slot, move, *, member=0, nickname="LEAFCUTTER"):
        choose_mon(member)
        wait_text(game, "Forget which move", "START INFO", "B BACK")
        mon = f"wPartyMon{member + 1}"
        moves = game.get_bytes(mon + "Moves", 4)
        pp = game.get_bytes(mon + "PP", 4)
        count = len(moves.rstrip(b"\0"))
        assert game.core.GB_safe_read_memory(game.gb, 0xFF40) & 2 == 0
        assert game.visible_text().splitlines()[11].strip() == "Forget which move"
        # Inspect a neighbor, then return with the actual intended row selected.
        neighbor = (slot + 1) % count
        for _ in range(neighbor):
            press(game, DOWN)
        press(game, START)
        game.wait(lambda: game.get("wMoveInfoMove") == moves[neighbor] and "B BACK" in game.visible_text())
        press(game, 6)  # SELECT keeps the effect page open while browsing.
        for _ in range(abs(slot - neighbor)):
            press(game, DOWN if slot > neighbor else UP)
        assert game.visible_text().splitlines()[11].strip() == move
        assert "SEL STATS" in game.visible_text()
        press(game, A)
        assert "SEL STATS" in game.visible_text()
        press(game, B)
        assert game.get("wTileMap", (2 + slot * 2) * 20 + 1) == 0xED
        assert "Forget which move" in game.visible_text()
        assert game.get_bytes(mon + "Moves", 4) == moves
        assert game.get_bytes(mon + "PP", 4) == pp
        press(game, A)
        wait_text(game, "YES", "NO", nickname, move)
        assert game.get("wCurrentMenuItem") == 1  # NO is highlighted.

    # Decline an ordinary move, then delete the first slot (an HM).
    select_move(1, "TACKLE")
    press(game, A)
    close_dialogue()
    assert game.get_bytes("wPartyMon1Moves", 4) == MOVES
    assert game.get_bytes("wPartyMon1PP", 4) == PP
    select_move(0, "CUT")
    press(game, UP)
    press(game, A)
    wait_text(game, "forgot", "CUT")
    assert game.get_bytes("wPartyMon1Moves", 4) == MOVES[1:] + b"\0"
    assert game.get_bytes("wPartyMon1PP", 4) == PP[1:] + b"\0"
    close_dialogue()

    # On a second party member, erase a middle move and then the last slot.
    game.put("wPartyMon2Nick", name_bytes("TEAMMATE"))
    game.put("wPartyMon2Moves", MOVES)
    game.put("wPartyMon2PP", PP)
    for slot, move, remaining, remaining_pp in (
        (2, "SURF", MOVES[:2] + MOVES[3:] + b"\0", PP[:2] + PP[3:] + b"\0"),
        (2, "QUICK ATTACK", MOVES[:2] + bytes(2), PP[:2] + bytes(2)),
    ):
        select_move(slot, move, member=1, nickname="TEAMMATE")
        press(game, UP)
        press(game, A)
        wait_text(game, "forgot", move)
        assert game.get_bytes("wPartyMon2Moves", 4) == remaining
        assert game.get_bytes("wPartyMon2PP", 4) == remaining_pp
        assert game.get_bytes("wPartyMon1Moves", 4) == MOVES[1:] + b"\0"
        close_dialogue()

    # A two-move list still browses and cancels without exposing an empty slot.
    select_move(1, "TACKLE", member=1, nickname="TEAMMATE")
    press(game, A)  # NO
    close_dialogue()
    assert game.get_bytes("wPartyMon2Moves", 4) == MOVES[:2] + bytes(2)

    # Last-move refusal leaves its PP intact.
    game.put("wPartyMon1Moves", (0x21, 0, 0, 0))
    game.put("wPartyMon1PP", (0x55, 0, 0, 0))
    choose_mon()
    wait_text(game, "only knows one")
    close_dialogue()
    assert game.get_bytes("wPartyMon1Moves", 4) == b"\x21\0\0\0"
    assert game.get_bytes("wPartyMon1PP", 4) == b"\x55\0\0\0"

    press(game, START)
    game.wait(lambda: "OPTION" in game.visible_text())
    for _ in range(game.get("wMaxMenuItem") + 1):
        if game.get("wCurrentMenuItem") == game.get("wMaxMenuItem") - 3:
            break
        press(game, DOWN)
    press(game, A)
    wait_text(game, "SAVE", "YES")
    press(game, A)
    wait_text(game, "saved", "the game")
    return bytes(game.battery())


def continue_inside_house(library, boot, rom, battery):
    with booted_game(library, boot, rom, battery) as game:
        press(game, START)
        advance_text_until(game, lambda: "CONTINUE" in game.visible_text())
        game.tick(30)
        press(game, A)
        game.wait(lambda: "BADGES" in game.visible_text())
        advance_text_until(game, lambda: "BADGES" not in game.visible_text())
        game.tick(150)
        assert game.get("wCurMap") == DELETER_HOUSE and game.get("wCurMapWidth") == 4
        assert game.get_bytes("wPartyMon2Moves", 4) == MOVES[:2] + bytes(2)
        assert game.get_bytes("wPartyMon2PP", 4) == PP[:2] + bytes(2)
        for key in (LEFT, LEFT, LEFT, DOWN):
            press(game, key, 35)
        press(game, DOWN, 100)
        assert (game.get("wCurMap"), game.get("wXCoord"), game.get("wYCoord")) == (FUCHSIA, 15, 28)


def use_from_bag(game, message, *, field_switch=False):
    press(game, START)
    game.wait(lambda: "OPTION" in game.visible_text())
    if game.get("wCurrentMenuItem") == 0:
        press(game, DOWN)
    press(game, A)
    game.wait(lambda: "CANCEL" in game.visible_text() and "EXP ALL" in game.visible_text())
    action = "USE"
    if field_switch:
        disabled = game.get("wExpAllDisabled")
        current = "OFF" if disabled else "ON"
        action = "TURN ON" if disabled else "TURN OFF"
        assert game.visible_text().splitlines()[5].strip() == current
    press(game, A)
    game.wait(lambda: action in game.visible_text() and "TOSS" in game.visible_text())
    if field_switch:
        press(game, B)
        game.wait(lambda: "TOSS" not in game.visible_text())
        assert game.get("wExpAllDisabled") == disabled
        press(game, A)
        game.wait(lambda: action in game.visible_text())
    press(game, A)
    wait_text(game, message)
    press(game, B)
    press(game, B)
    game.wait(lambda: "OPTION" in game.visible_text())
    press(game, B, 60)
    assert game.get_bytes("wNumBagItems", 4) == EXP_BAG


def check_aide(game, core):
    game.new_game()
    game.put("wOptions", (0xC1,))
    game.put("wPokedexOwned", bytes([0xFF] * 6 + [3]))  # 50 owned species
    game.put("wNumBagItems", (0, 0xFF))
    game.enter_map(0xB9, 4, 4, 3)  # Directly south of the Route 15 aide.
    press(game, UP)
    for _ in range(2):  # Receive the reward, then ask again.
        press(game, A)
        game.wait(lambda: game.get("wNumBagItems") == 1, accept=True)
        if core:
            game.wait(lambda: "with your party" in game.visible_text(), accept=True)
            game.wait(lambda: "fainted" in game.visible_text(), accept=True)
            game.wait(lambda: "turn it on or off" in game.visible_text(), accept=True)
        else:
            game.wait(lambda: "reduce the amount" in game.visible_text(), accept=True)
            game.wait(lambda: "store it via PC" in game.visible_text(), accept=True)
        assert game.get_bytes("wNumBagItems", len(EXP_BAG)) == EXP_BAG
        press(game, B, 50)


def check_switch(game, core):
    game.new_game()
    seed_party(game)
    game.put("wOptions", (0xC1,))
    game.put("wNumBagItems", EXP_BAG)
    if core:
        assert game.get("wExpAllDisabled") == 0
        use_from_bag(game, "is OFF", field_switch=True)
        assert game.get("wExpAllDisabled") == 1
        use_from_bag(game, "is ON", field_switch=True)
        assert game.get("wExpAllDisabled") == 0
        use_from_bag(game, "is OFF", field_switch=True)
        game.invoke("SaveGameData")
        game.return_to_stub()
        game.put("wExpAllDisabled", (0,))
        game.invoke("TryLoadSaveFile")
        game.return_to_stub()
        assert game.get("wSaveFileStatus") == 2 and game.get("wExpAllDisabled") == 1
    else:
        use_from_bag(game, "time to use that")

    # The carried item remains in the bag in both presets. Only Core has
    # switched it off, so it must pay exactly as though it were in storage.
    case = AwardCase(1, True, party_count=2, fainted=None)
    bag = seed_award(game, case)
    game.invoke("FaintEnemyPokemon")
    advance_text_until(game, lambda: game.cpu.pc == 0xC900)
    assert game.get_bytes("wNumBagItems", len(bag)) == bag
    expected = AwardCase(1, not core, party_count=2, fainted=None)
    for i, (xp, stats) in enumerate(expected_shares(expected, not core), start=1):
        assert int.from_bytes(game.get_bytes(f"wPartyMon{i}Exp", 3), "big") == START_EXP + xp
        values = game.get_bytes(f"wPartyMon{i}HPExp", 10)
        assert [int.from_bytes(values[j:j + 2], "big") for j in range(0, 10, 2)] == [
            baseline + gain for baseline, gain in zip(START_STAT_EXP, stats)
        ]


def check_battle_use(game, core):
    game.new_game()
    seed_party(game)
    game.put("wOptions", (0xC1,))
    game.put("wNumBagItems", EXP_BAG)
    game.enter_map(12, 10, 5, 4)
    game.put("wCurOpponent", (0x24,))
    game.put("wCurEnemyLevel", (5,))
    advance_text_until(game, lambda: battle_ready(game))
    hp = game.get_bytes("wBattleMonHP", 2)
    press(game, DOWN)
    press(game, A)
    wait_text(game, "EXP ALL", "CANCEL")
    press(game, A)
    wait_text(game, "time to use that")
    press(game, B)
    # The item list stays available after the refused use.
    press(game, B)
    game.wait(lambda: battle_ready(game))
    assert game.get_bytes("wNumBagItems", 4) == EXP_BAG
    assert game.get_bytes("wBattleMonHP", 2) == hp
    if core:
        assert game.get("wExpAllDisabled") == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        for test in (check_house, check_aide, check_switch, check_battle_use):
            with Game(args.sameboy, args.boot, rom) as game:
                saved = test(game, args.directory.name == "core")
            if test is check_house and saved is not None:
                continue_inside_house(args.sameboy, args.boot, rom, saved)
        print(f"{args.directory.name} {color}: Fuchsia house and EXP.ALL field use passed", flush=True)


if __name__ == "__main__":
    main()
