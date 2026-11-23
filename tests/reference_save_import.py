"""Import a save created by the pinned English Red or Blue cartridge."""

import argparse
import hashlib
from pathlib import Path

from cartridge_smoke import Game, seed_party

REFERENCE_SHA1 = {
    "red": "ea9bcae617fdf159b045185467ae58b2e4a48b9a",
    "blue": "d7037c83e1ae5b39bde3c30787637ba1d4c48ce2",
}
BAG = bytes((3, 0x14, 3, 0x45, 1, 0x4b, 1, 0xff))
BOX = bytes((1, 0x24, 0xff))
PLAYER_ID = bytes((0x21, 0x87))
MAIN_SAVE_OFFSET = 8192


def create_reference_save(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        game.put("wPlayerID", PLAYER_ID)
        game.put("wNumBagItems", BAG)
        game.put("wBoxCount", BOX)
        game.put("wBoxMon1Species", (0x24,))
        game.put("wBoxMon1BoxLevel", (7,))
        game.invoke("SaveGameData")
        game.return_to_stub()
        return bytes(game.battery()[MAIN_SAVE_OFFSET:])


def restore_save(game, data):
    game.new_game()
    game.battery()[MAIN_SAVE_OFFSET:] = data
    game.invoke("TryLoadSaveFile")
    game.return_to_stub()
    assert game.get("wSaveFileStatus") == 2


def check_records(game, bag):
    assert game.get_bytes("wPlayerID", 2) == PLAYER_ID
    assert game.get_bytes("wPartySpecies", 3) == bytes((0x69, 0x1b, 0xff))
    assert game.get_bytes("wPartyMon1HP", 2) == bytes((0, 160))
    assert game.get_bytes("wBoxCount", 3) == BOX
    assert game.get("wBoxMon1Species") == 0x24
    assert game.get("wBoxMon1BoxLevel") == 7
    assert game.get_bytes("wNumBagItems", len(bag)) == bag
    assert game.get("wRegisteredItemTag") == 0


def check_import(library, boot, rom, reference_save):
    with Game(library, boot, rom) as game:
        restore_save(game, reference_save)
        check_records(game, BAG)
        updated_bag = BAG[:2] + bytes((2,)) + BAG[3:]
        game.put("wNumBagItems", updated_bag)
        game.invoke("SaveGameData")
        game.return_to_stub()
        changed_save = bytes(game.battery()[MAIN_SAVE_OFFSET:])

    with Game(library, boot, rom) as game:
        restore_save(game, changed_save)
        check_records(game, updated_bag)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--baseline-dir", type=Path, required=True)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    saves = {}
    for color, expected_hash in REFERENCE_SHA1.items():
        rom = args.baseline_dir / f"poke{color}.gbc"
        assert hashlib.sha1(rom.read_bytes()).hexdigest() == expected_hash, rom
        saves[color] = create_reference_save(args.sameboy, args.boot, rom)

    for color in ("red", "blue", "green"):
        source = "blue" if color == "green" else color
        rom = args.directory / f"poke{color}.gbc"
        check_import(args.sameboy, args.boot, rom, saves[source])
        print(f"{args.directory.name} {color}: imported and re-saved an English {source} save",
              flush=True)


if __name__ == "__main__":
    main()
