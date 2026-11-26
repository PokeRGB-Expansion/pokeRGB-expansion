"""Build a sample trainer team and use its custom moves in a Route 3 battle."""

import argparse
from io import BytesIO
from pathlib import Path
import subprocess
import tarfile
from tempfile import TemporaryDirectory

from adventure_checkpoints import advance_text_until, seed_water_party
from battle_stats_return import battle_ready
from cartridge_smoke import Game
from move_info_authoring import shows


ROOT = Path(__file__).resolve().parents[1]
PARTIES = Path("data/trainers/parties.asm")
YOUNGSTER, BROCK, RIVAL3 = 1, 0x22, 0x2B
RATTATA_MOVES = bytes((0x96, 0, 0, 0))  # Splash
RATTATA_PP = bytes((40, 0, 0, 0))
EKANS_MOVES = bytes((0x62, 0x89, 0x23, 0x2C))  # Quick Attack, Glare, Wrap, Bite
EKANS_PP = bytes((30, 30, 20, 25))
SAMPLE = (
    "trainer_party 11, RATTATA, EKANS\n"
    "\ttrainer_moves 1, SPLASH\n"
    "\ttrainer_moves 2, QUICK_ATTACK, GLARE, WRAP, BITE"
)


def customize(source):
    path = source / PARTIES
    original = path.read_text()
    changes = (
        ("YoungsterData:\n; Route 3\n\tdb 11, RATTATA, EKANS, 0",
         "YoungsterData:\n; Route 3\n\t" + SAMPLE),
        ("BrockData:\n\tdb $FF, 12, GEODUDE, 14, ONIX, 0",
         "BrockData:\n\ttrainer_party $ff, 12, GEODUDE, 14, ONIX\n\ttrainer_moves 2, SURF"),
    )
    for before, after in changes:
        assert original.count(before) == 1
        original = original.replace(before, after)
    path.write_text(original)


def load_team(game, trainer, number=1, signature=0, starter=0):
    game.put("wCurOpponent", (200 + trainer,))
    game.put("wTrainerNo", (number,))
    game.put("wLoneAttackNo", (signature,))
    game.put("wRivalStarter", (starter,))
    game.invoke("ReadTrainer")
    game.return_to_stub()
    count = game.get("wEnemyPartyCount")
    assert 1 <= count <= 6
    team = []
    for slot in range(1, count + 1):
        record = f"wEnemyMon{slot}"
        team.append((game.get(record + "Species"), game.get(record + "Level"),
                     game.get_bytes(record + "Moves", 4), game.get_bytes(record + "PP", 4)))
    return team, game.get_bytes("wAmountMoneyWon", 3)


def check_teams(stock, edited):
    for game in (stock, edited):
        game.new_game()
        game.put("wIsInBattle", (2,))
        game.put("wTrainerBaseMoney", (0, 0x12, 0))
    # The Champion's three teams use different rival starter values.
    cases = [(YOUNGSTER, 1, 0, 0), (YOUNGSTER, 2, 0, 0), (BROCK, 1, 1, 0),
             (0x23, 1, 2, 0), (0x2C, 1, 0, 0), (0x21, 1, 0, 0),
             (0x2E, 1, 0, 0), (0x2F, 1, 0, 0),
             (RIVAL3, 1, 0, 0xB1), (RIVAL3, 2, 0, 0x99), (RIVAL3, 3, 0, 0xB0)]
    for case in cases:
        expected, money = load_team(stock, *case)
        actual, custom_money = load_team(edited, *case)
        if case[:2] == (YOUNGSTER, 1):
            expected[0] = (*expected[0][:2], RATTATA_MOVES, RATTATA_PP)
            expected[1] = (*expected[1][:2], EKANS_MOVES, EKANS_PP)
        elif case[0] == BROCK:
            assert expected[1][2][2] == 0x75  # Bide on the stock Onix
            expected[1] = (*expected[1][:2], bytes((0x39, 0, 0, 0)), bytes((15, 0, 0, 0)))
        assert (actual, custom_money) == (expected, money), (case, actual, expected)

    # Keep a peer's moves and PP, even when its party matches an authored team.
    edited.put("wLinkState", (4,))
    edited.put("wCurOpponent", (200 + YOUNGSTER,))
    edited.put("wTrainerNo", (1,))
    before = edited.get_bytes("wEnemyMons", 6 * 44)
    edited.invoke("ReadTrainer")
    edited.return_to_stub()
    assert edited.get_bytes("wEnemyMons", len(before)) == before


def play_route3(game):
    game.new_game()
    seed_water_party(game)
    game.put("wPartyMon1Moves", (0x27, 0, 0, 0))  # Tail Whip leaves the Rattata standing.
    game.put("wOptions", (0xC1,))
    game.enter_map(0x0E, 35, 14, 5)  # One square south of the first Route 3 Youngster.
    advance_text_until(game, lambda: battle_ready(game))
    assert game.get("wTrainerNo") == 1 and game.get("wTrainerClass") == YOUNGSTER
    assert game.get_bytes("wEnemyMonMoves", 4) == RATTATA_MOVES
    assert game.get_bytes("wEnemyMonPP", 4) == RATTATA_PP
    game.tick(20)
    game.press(4)
    shows(game, "TAIL WHIP")
    game.tick(20)
    game.press(4)
    shows(game, "Enemy RATTATA", "used SPLASH", accept=True)


def reject_invalid(source, command):
    path = source / PARTIES
    valid = path.read_text()
    row = "trainer_moves 1, SPLASH"
    team = "trainer_party 11, RATTATA, EKANS"
    for before, after, diagnostic in (
        (row, "trainer_moves 3, SPLASH", "no such party slot"),
        (row, "trainer_moves 1, NUM_ATTACKS + 1", "Invalid move ID"),
        (row, "trainer_moves 1, NO_MOVE", "Invalid move ID"),
        (row, "trainer_moves 1, SPLASH\n\ttrainer_moves 1, SURF", "already has a moveset"),
        (row, "trainer_moves 1, SURF, BITE, GLARE, WRAP, SPLASH", "one to four moves"),
        (row, "db 11, RATTATA, 0\n\ttrainer_moves 1, SPLASH", "immediately after its team"),
        (team, "trainer_party 11, NUM_POKEMON_INDEXES + 1", "Invalid trainer species"),
        (team, "trainer_party 0, RATTATA", "Trainer levels"),
        (team, "trainer_party $ff, 0, RATTATA", "Trainer levels"),
        (team, "trainer_party $ff, 11, RATTATA, 14", "one level per Pokemon"),
    ):
        path.write_text(valid.replace(before, after, 1))
        result = subprocess.run([*command, "red"], cwd=source, capture_output=True, text=True)
        assert result.returncode and diagnostic in result.stderr, (after, result.stderr)
    path.write_text(valid)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Reference build directory for one preset.")
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--rgbds", type=Path)
    args = parser.parse_args()
    preset = args.directory.name
    assert preset in ("core", "minimal")
    archive = subprocess.check_output(["git", "archive", "HEAD"], cwd=ROOT)
    with TemporaryDirectory(prefix="pokergb-trainer-moves-") as folder:
        source = Path(folder)
        with tarfile.open(fileobj=BytesIO(archive)) as files:
            files.extractall(source, filter="data")
        customize(source)
        command = ["make", "-j4", f"PRESET={preset}"]
        if args.rgbds:
            command.append(f"RGBDS={args.rgbds.resolve()}/")
        build = subprocess.run(command, cwd=source, capture_output=True, text=True)
        if build.returncode:
            raise SystemExit(build.stdout + build.stderr)
        for color in ("red", "blue", "green"):
            rom = f"poke{color}.gbc"
            params = (args.sameboy.resolve(), args.boot.resolve())
            sample = source / "build" / preset / rom
            with Game(*params, args.directory / rom) as stock, Game(*params, sample) as edited:
                check_teams(stock, edited)
            with Game(*params, sample) as edited:
                play_route3(edited)
            print(f"{preset} {color}: trainer teams, moves, PP and actual battle passed", flush=True)
        if preset == "core":
            reject_invalid(source, command)


if __name__ == "__main__":
    main()
