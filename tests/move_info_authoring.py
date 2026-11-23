"""Build a sample hack and check its custom move in the game menus."""

import argparse
from io import BytesIO
from pathlib import Path
import re
import subprocess
import tarfile
from tempfile import TemporaryDirectory

from cartridge_smoke import Game, seed_party

MACHINE_NUMBER = "TM23"
MACHINE_ID = 0xdf  # TM23
MOVE_ID = 0x81  # Swift
MOVE_NAME = "SWIFT TIDE"
WAIT_HINT = "SELECT EFFECT"
TEST_PARTY_MOVES = (0x21, 0x2d, 0x96, 0x0f)


def shows(game, *words, accept=False):
    game.wait(lambda: all(word in game.visible_text() for word in words), accept=accept)


def show_panel(game, expected_pp="PP 24"):
    shows(game, MOVE_NAME, "WATER", "POW  73", "ACC 91", expected_pp, WAIT_HINT)
    game.press(6)
    shows(game, "SELECT STATS", "May paralyze")
    game.press(5)
    game.wait(lambda: "SELECT STATS" not in game.visible_text())
    game.tick(15)


def bag(game):
    contents = bytes((1, MACHINE_ID, 1, 0xff))
    game.put("wNumBagItems", contents)
    game.invoke("StartMenu_Item")
    shows(game, MACHINE_NUMBER, MOVE_NAME, "START INFO")
    game.press(7)
    show_panel(game)
    shows(game, MACHINE_NUMBER, MOVE_NAME, "START INFO")
    assert game.get_bytes("wNumBagItems", len(contents)) == contents


def shop(game):
    game.put("wItemList", (1, MACHINE_ID, 0xff))
    game.invoke("DisplayPokemartDialogue_")
    shows(game, "BUY", "SELL")
    game.press(4)
    shows(game, MACHINE_NUMBER, MOVE_NAME, "START INFO", accept=True)
    money = game.get_bytes("wPlayerMoney", 3)
    bag = game.get_bytes("wNumBagItems", 6)
    game.press(7)
    show_panel(game)
    shows(game, MACHINE_NUMBER, MOVE_NAME, "START INFO")
    assert game.get_bytes("wPlayerMoney", 3) == money
    assert game.get_bytes("wNumBagItems", 6) == bag


def pc(game):
    game.put("wNumBoxItems", (1, MACHINE_ID, 1, 0xff))
    game.invoke("PlayerPCWithdraw")
    shows(game, MACHINE_NUMBER, MOVE_NAME, "START INFO", accept=True)
    stored = game.get_bytes("wNumBoxItems", 4)
    bag = game.get_bytes("wNumBagItems", 6)
    game.press(7)
    show_panel(game)
    shows(game, MACHINE_NUMBER, MOVE_NAME, "START INFO")
    assert game.get_bytes("wNumBoxItems", 4) == stored
    assert game.get_bytes("wNumBagItems", 6) == bag


def fight(game):
    game.put("wMoveMenuType", (0,))
    game.put("wBattleMonMoves", (MOVE_ID, 0x21, 0, 0))
    game.put("wBattleMonPP", (18, 35, 0, 0))
    game.invoke("MoveSelectionMenu")
    shows(game, MOVE_NAME, "START INFO")
    chosen = game.get("wPlayerSelectedMove")
    game.press(7)
    show_panel(game, "18 24")
    shows(game, MOVE_NAME, "START INFO")
    assert game.get_bytes("wBattleMonPP", 4) == bytes((18, 35, 0, 0))
    assert game.get("wPlayerMoveListIndex") == 0
    assert game.get("wPlayerSelectedMove") == chosen


def stats(game):
    seed_party(game)
    game.put("wPartyMon1Moves", (MOVE_ID, 0, 0, 0))
    game.put("wPartyMon1PP", (18, 0, 0, 0))
    game.put("wWhichPokemon", (0,))
    game.put("wMonDataLocation", (0,))
    game.invoke("StatusScreen")
    shows(game, "D PAD NAV", "ATTACK")
    game.tick(90)
    game.press(0)
    shows(game, MOVE_NAME, "START INFO")
    game.tick(90)
    game.press(7)
    show_panel(game, "18 24")
    shows(game, MOVE_NAME, "START INFO")
    assert game.get_bytes("wPartyMon1Moves", 4) == bytes((MOVE_ID, 0, 0, 0))
    assert game.get_bytes("wPartyMon1PP", 4) == bytes((18, 0, 0, 0))


def learn(game):
    seed_party(game)
    game.put("wPartyMon2Moves", TEST_PARTY_MOVES)
    game.put("wPartyMon2PP", (35, 40, 40, 30))
    game.put("wWhichPokemon", (1,))
    game.put("wPokedexNum", (0x1b,))  # Staryu learns Swift at level 32.
    game.put("wCurEnemyLevel", (32,))
    game.put("wMonDataLocation", (0,))
    game.invoke("LearnMoveFromLevelUp")
    shows(game, "YES", "NO", "START INFO", "TIDE", accept=True)
    game.press(7)
    show_panel(game)
    shows(game, "YES", "NO", "START INFO")
    game.press(4)
    shows(game, "TACKLE", "START INFO", accept=True)
    game.press(7)
    shows(game, "TACKLE", "KNOWN", WAIT_HINT)
    game.press(0)
    shows(game, MOVE_NAME, "NEW", "WATER", "POW  73", "ACC 91", "PP 24")
    game.press(1)
    shows(game, "TACKLE", "KNOWN", WAIT_HINT)
    game.press(5)
    shows(game, "TACKLE", "START INFO")
    assert game.get_bytes("wPartyMon2Moves", 4) == bytes(TEST_PARTY_MOVES)
    assert game.get_bytes("wPartyMon2PP", 4) == bytes((35, 40, 40, 30))


def prize(game):
    game.put("wNumBagItems", (1, 0x45, 1, 0xff))
    game.put("hTextID", (5,))  # The third prize vendor.
    game.invoke("CeladonPrizeMenu")
    shows(game, MACHINE_NUMBER, MOVE_NAME, "START INFO", accept=True)
    coins = game.get_bytes("wPlayerCoins", 2)
    bag = game.get_bytes("wNumBagItems", 6)
    game.press(7)
    show_panel(game)
    shows(game, MACHINE_NUMBER, MOVE_NAME, "START INFO")
    assert game.get_bytes("wPlayerCoins", 2) == coins
    assert game.get_bytes("wNumBagItems", 6) == bag


def customize_move(source):
    table = source / "data/moves/tmhm_moves.asm"
    original = table.read_text()
    machine_entry = "\tmove_id TM{02d:n}_MOVE"
    assert original.count(machine_entry) == 1
    table.write_text(original.replace(
        machine_entry,
        "IF n == 1\n\tmove_id POUND\n"
        "ELIF n == 2\n\tmove_id STRUGGLE\n"
        f"ELIF n == 23\n\tmove_id SWIFT\nELSE\n{machine_entry}\nENDC",
    ))

    # Build with the first and last move IDs in all three authoring sources.
    bulbasaur = source / "data/pokemon/base_stats/bulbasaur.asm"
    original = bulbasaur.read_text()
    bulbasaur.write_text(original.replace(
        "starting_moves TACKLE, GROWL, NO_MOVE, NO_MOVE",
        "starting_moves POUND, STRUGGLE, NO_MOVE, NO_MOVE", 1,
    ))
    learnsets = source / "data/pokemon/evos_moves.asm"
    original = learnsets.read_text()
    learnsets.write_text(original.replace(
        "learnset_move 30, STOMP\n\tlearnset_move 35, TAIL_WHIP",
        "learnset_move 30, POUND\n\tlearnset_move 35, STRUGGLE", 1,
    ))

    names = source / "data/moves/names.asm"
    original = names.read_text()
    assert original.count('"SWIFT"') == 1
    names.write_text(original.replace('"SWIFT"', f'"{MOVE_NAME}"'))

    moves = source / "data/moves/moves.asm"
    row = "\tmove SWIFT, PARALYZE_SIDE_EFFECT1, 73, WATER, 91, 24"
    modified, replacements = re.subn(r"^\tmove SWIFT,.*$", row, moves.read_text(), flags=re.M)
    assert replacements == 1
    moves.write_text(modified)


def check_invalid_move_ids(source, command):
    checks = (
        ("data/moves/tmhm_moves.asm", "move_id POUND", "move_id NO_MOVE"),
        ("data/pokemon/base_stats/bulbasaur.asm", "starting_moves POUND,",
         "starting_moves NUM_ATTACKS + 1,"),
        ("data/pokemon/evos_moves.asm", "learnset_move 30, POUND", "learnset_move 30, NO_MOVE"),
    )
    for filename, valid, invalid in checks:
        path = source / filename
        original = path.read_text()
        assert valid in original, filename
        try:
            path.write_text(original.replace(valid, invalid, 1))
            build = subprocess.run(command, cwd=source, capture_output=True, text=True)
            output = build.stdout + build.stderr
            if not build.returncode or "Invalid move ID" not in output or filename not in output:
                raise AssertionError(f"Expected a move ID error in {filename}.\n{output}")
        finally:
            path.write_text(original)
        print(f"{filename}: rejected an invalid move ID", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--rgbds", type=Path, help="Directory with the RGBDS 1.0.4 tools.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    archive = subprocess.check_output(["git", "archive", "HEAD"], cwd=root)
    with TemporaryDirectory(prefix="pokergb-move-info-") as directory:
        source = Path(directory)
        with tarfile.open(fileobj=BytesIO(archive)) as files:
            files.extractall(source, filter="data")
        customize_move(source)
        command = ["make", "-j4", "red"]
        if args.rgbds:
            command.append(f"RGBDS={args.rgbds.resolve()}/")
        build = subprocess.run(command, cwd=source, capture_output=True, text=True)
        if build.returncode:
            raise SystemExit(build.stdout + build.stderr)
        rom = source / "build/core/pokered.gbc"
        for check in (bag, shop, pc, fight, stats, learn, prize):
            with Game(args.sameboy.resolve(), args.boot.resolve(), rom) as game:
                game.new_game()
                check(game)
                print(f"{check.__name__}: custom Move INFO passed", flush=True)
        check_invalid_move_ids(source, command)


if __name__ == "__main__":
    main()
