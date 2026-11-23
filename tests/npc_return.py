"""Check the scope of the NPC wandering repair in linked cartridges."""

import argparse
from pathlib import Path

from cartridge_smoke import Game


CELADON_CITY = 0x06
WALK = 0xFE
STAY = 0xFF
GROUND = 0x5B
WATER = 0x14
NORTH, SOUTH, EAST = (8, -1, 0), (4, 1, 0), (1, 0, 1)


def check_walking_rule(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        game.put("wSpriteStateData1", bytes(256))
        game.put("wSpriteStateData2", bytes(256))
        game.put("wSprite03StateData1PictureID", (1,))
        game.put("wSprite03StateData2MovementByte1", (WALK,))
        collision_list = game.addresses["Overworld_Coll"][1]
        game.put("wTilesetCollisionPtr", collision_list.to_bytes(2, "little"))

        def step(direction, y, tile=GROUND):
            mask, dy, dx = direction
            game.put("hCurrentSpriteOffset", (0x30,))
            game.put("wSprite03StateData1YStepVector", (dy & 0xFF, y, dx, 64))
            game.invoke("CanWalkOntoTile")
            game.cpu.bc = (mask << 8) | tile
            game.cpu.de = (dy & 0xFF) << 8 | dx
            game.return_to_stub()
            return not bool(game.cpu.af & 0x10)

        for north_steps in (4, 5):
            game.put("wSprite03StateData2YDisplacement", (8, 8))
            for i in range(north_steps):
                assert step(NORTH, (5 - i) * 16 + 12)
                assert game.get("wSprite03StateData2YDisplacement") == 7 - i
            assert step(SOUTH, (5 - north_steps) * 16 + 12)
            assert game.get("wSprite03StateData2YDisplacement") == 9 - north_steps

        for vertical in (3, 4):
            game.put("wSprite03StateData2YDisplacement", (vertical, 8))
            assert not step(EAST, 28)
            assert game.get_bytes("wSprite03StateData2YDisplacement", 2) == bytes((vertical, 8))
        game.put("wSprite03StateData2YDisplacement", (5, 8))
        assert step(EAST, 28)
        assert game.get_bytes("wSprite03StateData2YDisplacement", 2) == bytes((5, 9))
        game.put("wSprite03StateData2YDisplacement", (3, 8))
        assert not step(SOUTH, 28, WATER)
        assert not step(SOUTH, 124)  # Bottom screen edge.
        assert not step(NORTH, 252)  # Top screen edge.

        for sprite in ("wSpritePlayerStateData1", "wSprite02StateData1"):
            game.put(sprite + "PictureID", (1,))
            game.put(sprite + "YPixels", (44,))
            game.put(sprite + "XPixels", (64,))
            assert not step(SOUTH, 28)
            game.put(sprite + "PictureID", (0,))

        game.put("wSprite03StateData2MovementByte1", (STAY,))
        assert not step(SOUTH, 28)
        game.put("wSprite03StateData2MovementByte1", (0,))  # Scripted path.
        assert step(SOUTH, 28, WATER)


def check_celadon_walker(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        game.enter_map(CELADON_CITY, 25, 17, 17)

        # Watch the actual north/south walker from the side of her path.
        previous_y = None
        for _ in range(10000):
            y = game.get("wSprite03StateData2MapY") - 4
            if previous_y == 14 and y == 15:
                assert game.get("wSprite03StateData2YDisplacement") == 4
                return
            previous_y = y
            game.tick(4)
        raise AssertionError("Celadon's walker did not return south from (14, 14).")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        check_walking_rule(args.sameboy, args.boot, rom)
        check_celadon_walker(args.sameboy, args.boot, rom)
        print(f"NPC return tests passed on {color.title()}.")


if __name__ == "__main__":
    main()
