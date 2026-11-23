"""Check a cut tree across the Route 14 and Route 15 connection."""

import argparse
from pathlib import Path

from cartridge_smoke import Game, seed_party


RIGHT, LEFT, A = 0, 1, 4
ROUTE_14, ROUTE_15 = 0x19, 0x1A
TREE, CUT_TREE = 0x35, 0x4C
TREE_TILE, PATH_TILE = 0x3D, 0x2C


def walk_until(game, direction, destination):
    game.core.GB_set_key_state(game.gb, direction, True)
    game.wait(destination)
    game.core.GB_set_key_state(game.gb, direction, False)
    game.tick(15)


def tree_block(game, width, block_x, block_y):
    offset = (width + 6) * (block_y + 3) + block_x + 3
    return game.get("wOverworldMap", offset)


def visible_tile(game, x, y):
    column = (game.get("hSCX") // 8 + x) % 32
    row = (game.get("hSCY") // 8 + y) % 32
    return game.core.GB_safe_read_memory(game.gb, 0x9800 + row * 32 + column)


def check_connection(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        game.put("wOptions", (1,))
        game.put("wStatusFlags4", (game.get("wStatusFlags4") | 0x10,))
        game.put("wPartyMon1Moves", (15, 0, 0, 0))  # Cut
        game.put("wObtainedBadges", (2,))  # Cascade Badge
        game.enter_map(ROUTE_14, 10, 2, 42)
        assert tree_block(game, 10, 1, 21) == TREE
        assert visible_tile(game, 10, 9) == TREE_TILE

        game.put("wSpritePlayerStateData1FacingDirection", (12,))  # East
        game.press(A)
        game.wait(
            lambda: all(word in game.visible_text() for word in ("Use CUT", "YES", "NO")),
            accept=True,
        )
        game.press(A)
        game.wait(
            lambda: tree_block(game, 10, 1, 21) == CUT_TREE
            and game.get("wUpdateSpritesEnabled") == 1,
            accept=True,
        )

        walk_until(game, LEFT, lambda: game.get("wCurMap") == ROUTE_15)
        assert tree_block(game, 30, 31, 3) == CUT_TREE
        assert visible_tile(game, 16, 9) == PATH_TILE
        walk_until(game, RIGHT, lambda: game.get("wCurMap") == ROUTE_14)
        assert tree_block(game, 10, 1, 21) == CUT_TREE
        walk_until(game, RIGHT, lambda: game.get("wXCoord") == 2 and not game.get("wWalkCounter"))
        assert game.get("wTileMap", 9 * 20 + 10) == PATH_TILE
        assert visible_tile(game, 10, 9) == PATH_TILE
        walk_until(game, RIGHT, lambda: game.get("wXCoord") == 3 and not game.get("wWalkCounter"))

        game.enter_map(ROUTE_14, 10, 2, 42)
        assert tree_block(game, 10, 1, 21) == TREE
        assert visible_tile(game, 10, 9) == TREE_TILE
        game.core.GB_set_key_state(game.gb, RIGHT, True)
        game.tick(35)
        game.core.GB_set_key_state(game.gb, RIGHT, False)
        assert game.get("wXCoord") == 2
        assert game.get("wTileInFrontOfPlayer") == TREE_TILE


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        check_connection(args.sameboy, args.boot, rom)
        print(f"Route 14 cut-tree test passed on {color.title()}.")


if __name__ == "__main__":
    main()
