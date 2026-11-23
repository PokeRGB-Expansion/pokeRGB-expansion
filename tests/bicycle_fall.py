"""Check the music and arrival after falling into a Seafoam Islands hole."""

import argparse
from pathlib import Path

from cartridge_smoke import Game, seed_party


SEAFOAM_1F, SEAFOAM_B1F = 0xC0, 0x9F
ROUTE_20 = 0x1F
BICYCLE = 6
RIGHT, SELECT = 0, 6


def check_fall(library, boot, rom, *, riding):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        game.put("wOptions", (1,))
        game.put("wStatusFlags4", (game.get("wStatusFlags4") | 0x10,))
        game.enter_map(SEAFOAM_1F, 15, 16, 6, last_map=ROUTE_20)
        cave_music = game.get("wMapMusicSoundID")
        assert game.get("wLastMusicSoundID") == cave_music
        if riding:
            game.put("wNumBagItems", (1, BICYCLE, 1, 0xFF))
            game.put("wRegisteredItemTag", (0xD6, BICYCLE))
            game.press(SELECT)
            game.wait(lambda: game.get("wWalkBikeSurfState") == 1, accept=True)
            game.wait(lambda: "got on the" in game.visible_text(), accept=True)
            game.wait(lambda: "got on the" not in game.visible_text(), accept=True)
            assert game.get("wLastMusicSoundID") != cave_music

        game.core.GB_set_key_state(game.gb, RIGHT, True)
        game.wait(lambda: game.get("wXCoord") == 17 or game.get("wCurMap") == SEAFOAM_B1F)
        game.core.GB_set_key_state(game.gb, RIGHT, False)
        game.wait(lambda: game.get("wCurMap") == SEAFOAM_B1F)
        game.wait(lambda: game.get("wJoyIgnore") != 0)
        game.wait(lambda: game.get("wJoyIgnore") == 0)
        game.tick(12)
        assert game.get("wWalkBikeSurfState") == 0
        assert (game.get("wXCoord"), game.get("wYCoord")) == (18, 7)
        assert game.get("wLastMusicSoundID") == game.get("wMapMusicSoundID") == cave_music
        assert game.get("wChannelSoundIDs") == cave_music


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        for riding in (False, True):
            check_fall(args.sameboy, args.boot, rom, riding=riding)
        print(f"{color.title()}: Seafoam fall on foot and bicycle passed", flush=True)


if __name__ == "__main__":
    main()
