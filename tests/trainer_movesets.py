"""Build a sample trainer team and use its custom moves in a Route 3 battle."""

import argparse
from pathlib import Path
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory

from adventure_checkpoints import advance_text_until, seed_water_party
from battle_stats_return import battle_ready
from cartridge_smoke import Game
from move_info_authoring import shows
from pokedex_area import linked_offset
from author_walkthrough import check_lab


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
    # Prepend our own teams. Authors can change the original members and their
    # moves, or use trainer_party, without breaking the regression fixture.
    fixtures = {
        "YoungsterData": SAMPLE,
        "BrockData": "trainer_party $ff, 12, GEODUDE, 14, ONIX\n\ttrainer_moves 2, SURF",
    }
    for label, team in fixtures.items():
        anchor = f"{label}:\n"
        assert original.count(anchor) == 1, f"Missing trainer class label {label}"
        original = original.replace(anchor, f"{anchor}\t{team}\n")
    path.write_text(original)

    path = source / "constants/pokemon_constants.asm"
    constants = path.read_text()
    for slot, species in enumerate(("PIKACHU", "EEVEE", "POLIWAG"), 1):
        constants, count = re.subn(rf"^DEF STARTER{slot} EQU .+$", f"DEF STARTER{slot} EQU {species}", constants, flags=re.M)
        assert count == 1, f"Missing STARTER{slot} definition"
    path.write_text(constants)
    path = source / "text/OaksLab.asm"
    text = path.read_text()
    anchor = "_OaksLabYouWantSquirtleText::\n"
    start = text.index(anchor) + len(anchor)
    end = text.index("\n_OaksLabYouWantBulbasaurText::", start)
    path.write_text(text[:start] + '\ttext "Your partner:"\n\tline "@"\n\ttext_ram wNameBuffer\n\ttext "?"\n\tdone\n' + text[end:])


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


def check_teams(stock, edited, base_rom, sample_rom):
    for game in (stock, edited):
        game.new_game()
        game.put("wIsInBattle", (2,))
        game.put("wTrainerBaseMoney", (0, 0x12, 0))
    # The Champion's three teams use different rival starter values.
    def starters(game, path):
        offset = linked_offset(game, "OaksLabStarterBalls")
        return path.read_bytes()[offset:offset + 12:4]

    base_starters = starters(stock, base_rom)
    new_starters = starters(edited, sample_rom)
    cases = [(YOUNGSTER, 1, 0, 0), (YOUNGSTER, 2, 0, 0), (BROCK, 1, 1, 0),
             (0x23, 1, 2, 0), (0x2C, 1, 0, 0), (0x21, 1, 0, 0),
             (0x2E, 1, 0, 0), (0x2F, 1, 0, 0),
             (RIVAL3, 1, 0, base_starters[1]), (RIVAL3, 2, 0, base_starters[2]), (RIVAL3, 3, 0, base_starters[0])]
    for trainer, number, signature, starter in cases:
        expected, money = load_team(stock, trainer, number, signature, starter)
        # The original Youngster and Brock teams follow our fixture team.
        shifted = number + (trainer in (YOUNGSTER, BROCK))
        # The Champion uses the rival's chosen starter to select a signature move.
        sample_starter = new_starters[base_starters.index(starter)] if trainer == RIVAL3 else starter
        actual = load_team(edited, trainer, shifted, signature, sample_starter)
        assert actual == (expected, money), (trainer, number, actual, expected)

    team, _ = load_team(edited, YOUNGSTER)
    assert team == [(0xA5, 11, RATTATA_MOVES, RATTATA_PP), (0x6C, 11, EKANS_MOVES, EKANS_PP)]
    team, _ = load_team(edited, BROCK, signature=1)
    assert team[1] == (0x22, 14, bytes((0x39, 0, 0, 0)), bytes((15, 0, 0, 0)))

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
    with TemporaryDirectory(prefix="pokergb-trainer-moves-") as folder:
        source = Path(folder)
        # Use the same files the author built, including edits since the last commit.
        files = subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT,
        ).decode().split("\0")
        for name in files:
            if name and (ROOT / name).is_file():
                target = source / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, target)
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
                check_teams(stock, edited, args.directory / rom, sample)
            with Game(*params, sample) as edited:
                play_route3(edited)
            print(f"{preset} {color}: trainer teams, moves, PP and actual battle passed", flush=True)
        check_lab(*params, args.directory / "pokered.gbc")
        check_lab(*params, source / "build" / preset / "pokered.gbc", custom_second=True)
        if preset == "core":
            reject_invalid(source, command)


if __name__ == "__main__":
    main()
