"""Build the opposite Move Deleter setting and reject invalid author data."""

import argparse
from io import BytesIO
from pathlib import Path
import subprocess
import tarfile
from tempfile import TemporaryDirectory

from adventure_checkpoints import advance_text_until, set_event
from cartridge_smoke import Game, seed_party
from core_services import A, check_house
from field_shortcuts import face

ROOT = Path(__file__).resolve().parents[1]


def route_14_advice(game, enabled):
    game.new_game()
    seed_party(game)
    game.put("wOptions", (0xc1,))
    set_event(game, 0x4a1)  # First Bird Keeper on Route 14, after his battle.
    game.enter_map(0x19, 10, 4, 5)
    face(game, 4)  # Look north at the trainer.
    game.press(A)
    expected = "moves easily" if enabled else "those moves"
    advance_text_until(game, lambda: expected in game.visible_text())


def expect_build_error(source, command, filename, old, new, expected, rom):
    path = source / filename
    original = path.read_text()
    assert old in original, filename
    try:
        path.write_text(original.replace(old, new, 1))
        result = subprocess.run(command, cwd=source, capture_output=True, text=True)
        assert result.returncode and expected in result.stderr, result.stderr
        assert not rom.exists(), "An invalid game was left in the output directory"
    finally:
        path.write_text(original)


def check(source, args):
    enabled = args.preset == "minimal"
    command = ["make", "-j4", "red", f"PRESET={args.preset}", f"MOVE_DELETER={int(enabled)}"]
    if args.rgbds:
        command.append(f"RGBDS={args.rgbds.resolve()}/")
    rom = source / f"build/deleter-{int(enabled)}" / args.preset / "pokered.gbc"
    subprocess.run(command, cwd=source, check=True, stdout=subprocess.DEVNULL)
    with Game(args.sameboy.resolve(), args.boot.resolve(), rom) as game:
        check_house(game, enabled)
    with Game(args.sameboy.resolve(), args.boot.resolve(), rom) as game:
        route_14_advice(game, enabled)
    if args.preset == "core":
        # Both errors would produce a working-looking ROM without build-time checks.
        before = rom.read_bytes()
        # Some versions of Make compare timestamps to the nearest second.
        command += ["-W", "data/wild/maps/Route1.asm", "-W", "data/moves/info_effects.asm"]
        expect_build_error(source, command, "data/wild/maps/Route1.asm", "3, PIDGEY", "3, NO_MON",
                           "Route1WildMons grass, slot 1: species $00", rom)
        expect_build_error(source, command, "data/moves/info_effects.asm", "Deals damage.@",
                           "Deals damage three times.@", "row 1: INFO has 25 tiles", rom)
        subprocess.run(command, cwd=source, check=True, stdout=subprocess.DEVNULL)
        assert rom.read_bytes() == before


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("preset", choices=("core", "minimal"))
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--rgbds", type=Path)
    args = parser.parse_args()
    archive = subprocess.check_output(["git", "archive", "HEAD"], cwd=ROOT)
    with TemporaryDirectory(prefix="pokergb-author-build-") as directory:
        source = Path(directory)
        with tarfile.open(fileobj=BytesIO(archive)) as files:
            files.extractall(source, filter="data")
        check(source, args)
    print(f"{args.preset}: Move Deleter build option and author data checks passed")


if __name__ == "__main__":
    main()
