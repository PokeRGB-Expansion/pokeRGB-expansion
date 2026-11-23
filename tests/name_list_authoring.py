"""Check name lists that extend across the item IDs used for HMs."""

import argparse
from io import BytesIO
from pathlib import Path
import subprocess
import tarfile
from tempfile import TemporaryDirectory

from cartridge_smoke import Game

HM01 = 0xc4
TM01 = 0xc9
ITEM_NAME = 4
LISTS = (
    (1, "MonsterNames", "pokemon", "\tassert_table_length NUM_POKEMON_INDEXES", "dname",
     "NUM_POKEMON_INDEXES", "MON"),
    (2, "MoveNames", "moves", "\tassert_list_length NUM_ATTACKS", "li", "NUM_ATTACKS", "MOVE"),
    (7, "TrainerNames", "trainers", "\tassert_list_length NUM_TRAINERS", "li", "NUM_TRAINERS",
     "TRAINER"),
)


def extend_names(source):
    for _, _, folder, end_check, macro, count, name in LISTS:
        table = source / f"data/{folder}/names.asm"
        original = table.read_text()
        assert original.count(end_check) == 1
        rows = [
            end_check,
            f"REPT HM01 - 2 - {count}",
            f'\t{macro} "PADDING"',
            "ENDR",
            *(f'\t{macro} "{prefix} {name}"' for prefix in ("LOW", "MID", "TOP")),
        ]
        table.write_text(original.replace(end_check, "\n".join(rows)))


def read_name(game, list_id, bank, index):
    game.put("wNameListType", (list_id,))
    game.put("wNameListIndex", (index,))
    game.put("wPredefBank", (bank,))
    game.invoke("GetName")
    game.return_to_stub()
    codes = game.get_bytes("wNameBuffer", 13).split(b"\x50", 1)[0]
    return "".join(chr(value - 0x80 + ord("A")) if 0x80 <= value <= 0x99
                   else " " if value == 0x7f else chr(value - 0xf6 + ord("0"))
                   for value in codes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--rgbds", type=Path, help="Directory with the RGBDS 1.0.4 tools.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    archive = subprocess.check_output(["git", "archive", "HEAD"], cwd=root)
    with TemporaryDirectory(prefix="pokergb-name-lists-") as directory:
        source = Path(directory)
        with tarfile.open(fileobj=BytesIO(archive)) as files:
            files.extractall(source, filter="data")
        extend_names(source)
        command = ["make", "-j4", "red"]
        if args.rgbds:
            command.append(f"RGBDS={args.rgbds.resolve()}/")
        build = subprocess.run(command, cwd=source, capture_output=True, text=True)
        if build.returncode:
            raise SystemExit(build.stdout + build.stderr)

        with Game(args.sameboy.resolve(), args.boot.resolve(), source / "build/core/pokered.gbc") as game:
            game.new_game()
            for list_id, table, _, _, _, _, name in LISTS:
                bank = game.addresses[table][0]
                for index, prefix in zip(range(HM01 - 1, HM01 + 2), ("LOW", "MID", "TOP")):
                    assert read_name(game, list_id, bank, index) == f"{prefix} {name}"
            bank = game.addresses["ItemNames"][0]
            for offset in range(5):
                assert read_name(game, ITEM_NAME, bank, HM01 + offset) == f"HM{offset + 1:02d}"
            for offset in range(50):
                assert read_name(game, ITEM_NAME, bank, TM01 + offset) == f"TM{offset + 1:02d}"
            print("High Pokémon, move, and trainer name IDs and all 55 machine names passed.")


if __name__ == "__main__":
    main()
