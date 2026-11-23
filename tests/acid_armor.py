"""Check the Acid Armor melt and the return of each active battle picture."""

import argparse
from pathlib import Path

from cartridge_smoke import Game
from protected_mechanics import ENEMY, PLAYER, seed_actions

ACID_ARMOR = 0x97
BATTLE_PICTURE_TILES = 49


def invoke_visual(game, label):
    # Several animation buffers use the usual test address. Put the return
    # loop in the unused space at the end of the battle data instead.
    stop = game.addresses["wMiscBattleDataEnd"][1] - 2
    game.invoke(label)
    game.write(stop, (0x18, 0xfe))
    game.write(0xdffd, stop.to_bytes(2, "little"))
    return stop


def prepare_picture(game, actor, picture):
    if picture == "substitute":
        game.put(f"w{actor}BattleStatus2", (1 << 4,))
        animation = "AnimationSubstitute"
    elif picture == "minimized":
        game.put(f"w{actor}MonMinimized", (1,))
        animation = "AnimationMinimizeMon"
    else:
        species = 0x1b if actor == ENEMY else 0x69
        if picture == "transformed":
            species = 0x69 if actor == ENEMY else 0x1b
            game.put(f"w{actor}BattleStatus3", (1 << 3,))
        game.put(f"wChangeMonPic{actor}TurnSpecies", (species,))
        animation = "ChangeMonPic"
    stop = invoke_visual(game, animation)
    game.wait(lambda: game.cpu.pc == stop, accept=True)


def actor_tiles(game, actor):
    tilemap = game.get_bytes("wTileMap", 360)
    top, left = (5, 1) if actor == PLAYER else (0, 12)
    return b"".join(
        tilemap[row * 20 + left:row * 20 + left + 7] for row in range(top, top + 7)
    )


def check_acid_armor(game, actor, picture):
    seed_actions(game, actor, ACID_ARMOR)
    game.put("hWhoseTurn", (actor == ENEMY,))
    game.put("wOptions", (1,))
    game.put("wTileMap", (0x7f,) * 360)
    prepare_picture(game, actor, picture)
    picture_label = "vBackPic" if actor == PLAYER else "vFrontPic"
    before = actor_tiles(game, actor)
    pixels = game.get_bytes(picture_label, BATTLE_PICTURE_TILES * 16)
    assert len(set(before)) > 1 and len(set(pixels)) > 1, (actor, picture)

    stop = invoke_visual(game, f"Execute{actor}Move")
    game.wait(lambda: actor_tiles(game, actor) == b"\x7f" * BATTLE_PICTURE_TILES, accept=True)
    game.wait(lambda: game.cpu.pc == stop, accept=True)
    assert actor_tiles(game, actor) == before, (actor, picture)
    assert game.get_bytes(picture_label, BATTLE_PICTURE_TILES * 16) == pixels, (actor, picture)
    assert game.get(f"w{actor}MonDefenseMod") == 9


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        for actor in (PLAYER, ENEMY):
            for picture in ("normal", "substitute", "minimized", "transformed"):
                with Game(args.sameboy, args.boot, rom) as game:
                    game.new_game()
                    check_acid_armor(game, actor, picture)
        print(f"{args.directory.name} {color}: Acid Armor pictures and Defense passed", flush=True)


if __name__ == "__main__":
    main()
