"""Power-cut checks on actual save routines using a disposable battery."""

import argparse
from pathlib import Path

from cartridge_smoke import Game, older_save


def battery_offset(game, label):
    bank, address = game.addresses[label]
    return bank * 8192 + address - 0xa000


def advance_to(game, label, predicate=lambda: True, steps=2_000_000):
    bank, address = game.addresses[label]
    for _ in range(steps):
        if game.cpu.pc == address and game.get("hLoadedROMBank") == bank and predicate():
            return
        game.core.GB_run(game.gb)
    raise AssertionError(f"Timed out before {label} at {game.cpu.pc:04x}.")


def booted_game(library, boot, rom, battery):
    game = Game(library, boot, rom)
    game.tick(240)
    # Leave the live title graphics scratch in bank 0 alone.
    hall = battery_offset(game, "sHallOfFame")
    game.battery()[hall:] = battery[hall:]
    return game


def assert_menu(library, boot, rom, battery, *, interrupted):
    with booted_game(library, boot, rom, battery) as game:
        game.invoke("MainMenu")
        if interrupted:
            game.wait(lambda: "Save interrupted" in game.visible_text())
            assert "CONTINUE" not in game.visible_text()
            game.press(4)
            game.wait(lambda: "NEW GAME" in game.visible_text() and game.get("wMaxMenuItem") == 1)
            assert game.get("wSaveFileStatus") == 1
            assert "CONTINUE" not in game.visible_text()
        else:
            game.wait(lambda: "CONTINUE" in game.visible_text() and game.get("wMaxMenuItem") == 2)
            assert game.get("wSaveFileStatus") == 2
        # Startup may use bank 0 video scratch. The save banks stay intact.
        assert bytes(game.battery()[8192:]) == battery[8192:]


def assert_main_checksum(game, battery):
    end = battery_offset(game, "sMainDataCheckSum")
    start = battery_offset(game, "sGameData")
    assert battery[end] == (255 - sum(battery[start:end])) & 255


def check_full_save(library, boot, rom, battery):
    with booted_game(library, boot, rom, battery) as game:
        game.invoke("TryLoadSaveFile")
        game.return_to_stub()
        assert game.get("wSaveFileStatus") == 2
        assert game.addresses["sGameData"] == (1, 0xa598)
        assert game.addresses["sMainDataCheckSum"] == (1, 0xb523)
        assert game.addresses["sSaveTransactionTag"] == (1, 0xb524)
        assert game.addresses["sSaveTransactionState"] == (1, 0xb52c)

        game.put("wPlayerMoney", (0, 0x12, 0x34))
        game.put("wPartyMon1HP", (0, 87))
        game.invoke("SaveGameData")
        advance_to(game, "BeginSaveTransaction")
        before_mark = bytes(game.battery())
        assert before_mark[8192:] == battery[8192:]

        advance_to(game, "WriteCurrentBoxData")
        partial = bytes(game.battery())
        assert_main_checksum(game, partial)
        # A fresh valid checksum covers the new world and the older party.
        party = battery_offset(game, "sPartyData")
        box = battery_offset(game, "sCurBoxData")
        assert partial[party:box] == battery[party:box]
        money = battery_offset(game, "sMainData") + (
            game.addresses["wPlayerMoney"][1] - game.addresses["wMainDataStart"][1]
        )
        assert partial[money:money + 3] == bytes((0, 0x12, 0x34))
        assert partial[money:money + 3] != battery[money:money + 3]

        advance_to(game, "CommitSaveTransaction")
        pending_commit = bytes(game.battery())
        assert_main_checksum(game, pending_commit)
        assert pending_commit[party:box] != battery[party:box]
        game.return_to_stub()
        completed = bytes(game.battery())
        marker = battery_offset(game, "sSaveTransactionState")
        assert bytes(game.battery())[marker] == 0
        assert pending_commit[:marker] == completed[:marker]
        assert pending_commit[marker + 1:] == completed[marker + 1:]
        assert_main_checksum(game, completed)

    for snapshot, interrupted in ((before_mark, False), (partial, True),
                                  (pending_commit, True), (completed, False)):
        assert_menu(library, boot, rom, snapshot, interrupted=interrupted)


def check_interrupted_first_save(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        game.invoke("SaveGameData")
        advance_to(game, "WriteMainData")
        before_player_name = bytes(game.battery())
        name = battery_offset(game, "sPlayerName")
        assert 0x50 not in before_player_name[name:name + 11]
    assert_menu(library, boot, rom, before_player_name, interrupted=True)


def check_standalone_trade(library, boot, rom, battery):
    with booted_game(library, boot, rom, battery) as game:
        game.invoke("TryLoadSaveFile")
        game.return_to_stub()
        assert game.get("wSaveFileStatus") == 2
        money = game.get_bytes("wPlayerMoney", 3)
        game.put("wPlayerMoney", (9, 0, 0))
        game.put("wPartyMon1HP", (0, 53))
        game.put("wPokedexOwned", (0xa3,))
        game.invoke("SavePartyAndDexData")
        advance_to(game, "CommitSaveTransaction")
        pending = bytes(game.battery())
        assert_main_checksum(game, pending)
        game.return_to_stub()
        completed = bytes(game.battery())
        game.invoke("TryLoadSaveFile")
        game.return_to_stub()
        assert game.get("wSaveFileStatus") == 2
        assert game.get_bytes("wPartyMon1HP", 2) == bytes((0, 53))
        assert game.get("wPokedexOwned") == 0xa3
        assert game.get_bytes("wPlayerMoney", 3) == money
    assert_menu(library, boot, rom, pending, interrupted=True)
    assert_menu(library, boot, rom, completed, interrupted=False)


def check_confirmed_box(library, boot, rom, battery, *, initialized):
    with booted_game(library, boot, rom, battery) as game:
        game.invoke("TryLoadSaveFile")
        game.return_to_stub()
        assert game.get("wSaveFileStatus") == 2
        game.put("wCurrentBoxNum", (0x80 if initialized else 0,))
        game.put("wOptions", (1,))
        game.invoke("ChangeBox")
        game.wait(lambda: game.get("wMaxMenuItem") == 11 and "OCCUPIED" in game.visible_text())
        game.press(3)
        game.tick(12)
        game.press(4)
        game.wait(lambda: all(word in game.visible_text() for word in ("YES", "NO")), accept=True)
        game.tick(14)
        game.core.GB_set_key_state(game.gb, 4, True)
        if not initialized:
            advance_to(game, "EmptyAllSRAMBoxes")
            before_initializing = bytes(game.battery())
            marker = battery_offset(game, "sSaveTransactionState")
            assert before_initializing[marker] == 0x5a
        advance_to(game, "WriteGameSaveAndCommit")
        between_box_and_main = bytes(game.battery())
        assert between_box_and_main[2 * 8192:] != battery[2 * 8192:]
        assert_main_checksum(game, between_box_and_main)
        game.core.GB_set_key_state(game.gb, 4, False)
        game.return_to_stub()
        committed = bytes(game.battery())
        assert game.get("wCurrentBoxNum") == 0x81
    assert_menu(library, boot, rom, between_box_and_main, interrupted=True)
    assert_menu(library, boot, rom, committed, interrupted=False)


def check_hall_of_fame(library, boot, rom, battery):
    with booted_game(library, boot, rom, battery) as game:
        game.invoke("TryLoadSaveFile")
        game.return_to_stub()
        game.put("wNumHoFTeams", (1,))
        game.put("wHallOfFame", (0xe4,))
        game.invoke("SaveHallOfFameTeams")
        game.return_to_stub()
        pending = bytes(game.battery())
        assert pending[battery_offset(game, "sHallOfFame")] == 0xe4
        game.invoke("SaveGameData")
        game.return_to_stub()
        committed = bytes(game.battery())
        assert committed[battery_offset(game, "sHallOfFame")] == 0xe4
    assert_menu(library, boot, rom, pending, interrupted=True)
    assert_menu(library, boot, rom, committed, interrupted=False)


def check_confirmed_erase(library, boot, rom, battery):
    with booted_game(library, boot, rom, battery) as game:
        game.invoke("ClearAllSRAMBanks")
        advance_to(game, "ClearAllSRAMBanks.PadSRAM_FF", lambda: game.cpu.af >> 8 == 1)
        partial = bytes(game.battery())
        assert partial[2 * 8192:] == bytes((0xff,)) * (2 * 8192)
        assert_main_checksum(game, partial)
        game.return_to_stub()
        finished = bytes(game.battery())
        assert finished[8192:] == bytes((0xff,)) * (3 * 8192)
    assert_menu(library, boot, rom, partial, interrupted=True)
    with booted_game(library, boot, rom, finished) as game:
        game.invoke("MainMenu")
        game.wait(lambda: "NEW GAME" in game.visible_text()
                  and "CONTINUE" not in game.visible_text()
                  and game.get("wMaxMenuItem") == 1)
        assert "Save interrupted" not in game.visible_text()


def run(library, boot, rom):
    fixture_save = older_save(library, boot, rom)
    with Game(library, boot, rom) as game:
        tag = battery_offset(game, "sSaveTransactionTag")
        marker = battery_offset(game, "sSaveTransactionState")
    # Model padding from a stock save, even if its last byte happens to
    # match the pending state. The full signature is required.
    stock = bytearray(fixture_save)
    stock[tag:marker] = bytes((0xff,)) * 8
    stock[marker] = 0x5a
    assert_menu(library, boot, rom, bytes(stock), interrupted=False)
    check_full_save(library, boot, rom, bytes(stock))
    check_interrupted_first_save(library, boot, rom)
    check_standalone_trade(library, boot, rom, fixture_save)
    for initialized in (False, True):
        check_confirmed_box(library, boot, rom, fixture_save, initialized=initialized)
    check_hall_of_fame(library, boot, rom, fixture_save)
    check_confirmed_erase(library, boot, rom, fixture_save)
    print(f"{rom}: stock padding, interrupted full/partial saves, both box switch paths, Hall of Fame, erase")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("roms", type=Path, nargs="+")
    arguments = parser.parse_args()
    for cartridge in arguments.roms:
        run(arguments.library, arguments.boot, cartridge)
