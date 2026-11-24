"""Check the English reference title screens in Super Game Boy mode."""

import argparse
import ctypes as C
from pathlib import Path

from cartridge_smoke import Game

SGB_MODEL = 0x004
SGB_WIDTH = 256
SGB_HEIGHT = 224
RGBCallback = C.CFUNCTYPE(C.c_uint32, C.c_void_p, C.c_uint8, C.c_uint8, C.c_uint8)

# First title Pokémon, version text column and tiles, and rendered title colors.
TITLES = {
    "red": (0xb0, 7, "60 61 7f 65 66 67 68 69", 0xad0021, 0xf7b58c),
    "blue": (0xb1, 7, "61 62 63 64 65 66 67 68", 0x739cef, 0xf7b58c),
    "green": (0x99, 6, "60 61 62 63 64 65 66 67 68", 0x42a552, 0x4aa55a),
}


@RGBCallback
def encode_rgb(_, red, green, blue):
    return red << 16 | green << 8 | blue


def pixels_in(pixels, left, top, width, height):
    return {
        pixels[y * SGB_WIDTH + x]
        for y in range(top, top + height)
        for x in range(left, left + width)
    }


def check_title(game, color):
    species, column, tile_hex, version_color, species_color = TITLES[color]
    pixels = (C.c_uint32 * (SGB_WIDTH * SGB_HEIGHT))()
    game.core.GB_set_color_correction_mode.argtypes = [C.c_void_p, C.c_int]
    game.core.GB_set_color_correction_mode.restype = None
    game.core.GB_set_color_correction_mode(game.gb, 0)
    game.core.GB_set_rgb_encode_callback.argtypes = [C.c_void_p, RGBCallback]
    game.core.GB_set_rgb_encode_callback.restype = None
    game.core.GB_set_rgb_encode_callback(game.gb, encode_rgb)
    game.core.GB_set_pixels_output.argtypes = [C.c_void_p, C.POINTER(C.c_uint32)]
    game.core.GB_set_pixels_output.restype = None
    game.core.GB_set_pixels_output(game.gb, pixels)
    game.core.GB_set_rendering_disabled(game.gb, False)

    # Allow the Super Game Boy boot sequence and the game's intro to finish.
    for _ in range(2500):
        game.tick()
        if game.get("wTitleMonSpecies") == species:
            break
    else:
        raise AssertionError(f"{color}: title did not reach the first Pokémon.")
    game.tick(200)
    assert game.get("wOnSGB") == 1
    assert game.get("wTitleMonSpecies") == species
    version_tiles = bytes.fromhex(tile_hex)
    offset = 20 * 8 + column
    assert game.get_bytes("wTileMap", offset + len(version_tiles))[offset:] == version_tiles

    # The game screen starts at (48, 40) inside the Super Game Boy border.
    assert version_color in pixels_in(pixels, 48, 104, 160, 16)
    assert species_color in pixels_in(pixels, 48, 120, 160, 64)
    if color == "green":
        assert species_color in pixels_in(pixels, 48, 120, 80, 56)
        # The trainer and copyright keep the original portrait palette.
        for region in ((128, 120, 80, 56), (48, 176, 160, 8)):
            colors = pixels_in(pixels, *region)
            assert 0xf7b58c in colors and species_color not in colors
        # The word Green uses five pixel rows, like the original Blue lettering.
        green_word = [
            ".####....................",
            "##....####..###..###.###.",
            "##.##.##...##.#.##.#.##.#",
            "##..#.##...###..###..##.#",
            ".####.##....###..###.##.#",
        ]
        for y, row in enumerate(green_word, 107):
            actual = "".join("#" if pixels[y * SGB_WIDTH + x] == version_color else "."
                             for x in range(100, 100 + len(row)))
            assert actual == row, (actual, row)
        # The GREEN label is in a different tilemap than the Blue label.
        assert pixels_in(pixels, 100, 24, 55, 9) == {0x296b42, 0x94d67b}

    # Blue and Green share the exact Version artwork and vertical alignment.
    if color in ("blue", "green"):
        left = 48 + column * 8 + (24 if color == "blue" else 34)
        return tuple(pixels[y * SGB_WIDTH + x] == version_color
                     for y in range(104, 112) for x in range(left, left + 36))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True, help="SameBoy Super Game Boy boot file.")
    args = parser.parse_args()
    versions = {}
    for color in TITLES:
        rom = args.directory / f"poke{color}.gbc"
        with Game(args.sameboy, args.boot, rom, model=SGB_MODEL) as game:
            versions[color] = check_title(game, color)
        print(f"{args.directory.name} {color}: Super Game Boy title passed", flush=True)

    assert versions["green"] == versions["blue"]


if __name__ == "__main__":
    main()
