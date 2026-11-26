"""Check DMG compatibility mode using SameBoy’s CGB-E model."""

import argparse
import ctypes as C
from pathlib import Path

from cartridge_smoke import Game, seed_party
from title_smoke import RGBCallback, TITLES, encode_rgb


CGB_E = 0x205
UP, DOWN, A, B, START = 2, 3, 4, 5, 7
HOUSE = 0x26
THUNDERBOLT_TM = bytes((1, 0xE0, 1, 0xFF))


def shows(game, *words, accept=False):
    game.wait(lambda: all(word in game.visible_text() for word in words), accept=accept)
    game.tick(14)


def check_mode(game):
    for name in ("GB_is_cgb", "GB_is_cgb_in_cgb_mode"):
        function = getattr(game.core, name)
        function.argtypes = [C.c_void_p]
        function.restype = C.c_bool
    assert game.core.GB_is_cgb(game.gb)
    assert not game.core.GB_is_cgb_in_cgb_mode(game.gb)


def display_pixels(game, width=160, height=144):
    pixels = (C.c_uint32 * (width * height))()
    game.core.GB_set_pixels_output.argtypes = [C.c_void_p, C.POINTER(C.c_uint32)]
    game.core.GB_set_pixels_output.restype = None
    game.core.GB_set_pixels_output(game.gb, pixels)
    game.core.GB_set_rgb_encode_callback.argtypes = [C.c_void_p, RGBCallback]
    game.core.GB_set_rgb_encode_callback.restype = None
    game.core.GB_set_rgb_encode_callback(game.gb, encode_rgb)
    game.core.GB_set_rendering_disabled(game.gb, False)
    return pixels


def start_menu_row(game, index):
    game.press(START)
    shows(game, "ITEM", "SAVE", "OPTION")
    current = game.get("wCurrentMenuItem")
    for _ in range(abs(current - index)):
        game.press(DOWN if current < index else UP)
        game.tick(12)
    assert game.get("wCurrentMenuItem") == index
    game.press(A)


def bag_info(game, pixels):
    start_menu_row(game, 1)
    shows(game, "TM24", "START INFO")
    bag_picture = bytes(pixels)
    game.press(START)
    shows(game, "THUNDERBOLT", "ELECTRIC", "SELECT EFFECT")
    assert len(set(pixels)) > 1 and bytes(pixels) != bag_picture
    assert "95" in game.visible_text()
    game.press(B)
    shows(game, "TM24", "START INFO")
    assert game.get_bytes("wNumBagItems", 4) == THUNDERBOLT_TM
    game.press(B)
    shows(game, "ITEM", "SAVE", "OPTION")
    game.press(B)
    game.wait(lambda: not game.get("wFontLoaded") & 1)
    game.tick(12)


def check_compatibility(library, boot, rom, color):
    with Game(library, boot, rom, model=CGB_E) as game:
        pixels = display_pixels(game)
        game.new_game()
        check_mode(game)
        assert game.get("wCurMap") == HOUSE
        assert len(set(pixels)) > 1
        seed_party(game)
        game.put("wPlayerID", (0x12, 0x34))
        game.put("wNumBagItems", THUNDERBOLT_TM)
        game.put("wOptions", (1,))
        bag_info(game, pixels)

        start_menu_row(game, 3)
        shows(game, "YES", "NO", accept=True)
        game.press(A)
        shows(game, "saved", "the game", accept=True)
        game.wait(lambda: not game.get("wFontLoaded") & 1, accept=True)
        save = bytes(game.battery())
        party_size = game.addresses["wPartyDataEnd"][1] - game.addresses["wPartyDataStart"][1]
        party = game.get_bytes("wPartyDataStart", party_size)
        position = game.get_bytes("wYCoord", 2)

    # A new emulator instance starts from only the existing cartridge save.
    with Game(library, boot, rom, model=CGB_E) as game:
        game.battery()[:] = save
        _, column, tile_hex, *_ = TITLES[color]
        version_tiles = bytes.fromhex(tile_hex)
        offset = 20 * 8 + column
        for _ in range(250):
            game.tick(8)
            if game.get_bytes("wTileMap", offset + len(version_tiles))[offset:] == version_tiles:
                break
        else:
            raise AssertionError("The cold boot did not draw the expected title.")
        game.tick(160)
        title_bank = game.addresses["DisplayTitleScreen"][0]
        address = game.addresses["CheckForUserInterruption"][1]
        for _ in range(50000):
            if game.cpu.pc == address and game.get("hLoadedROMBank") == title_bank:
                break
            game.core.GB_run(game.gb)
        else:
            raise AssertionError("The title screen did not begin polling input.")
        game.press(START)
        shows(game, "CONTINUE")
        assert game.get("wSaveFileStatus") == 2
        game.press(A)
        game.wait(lambda: game.get("wCurMap") == HOUSE and game.get("wCurMapWidth"), accept=True)
        game.tick(20)
        check_mode(game)
        assert game.get_bytes("wPlayerID", 2) == bytes((0x12, 0x34))
        assert game.get_bytes("wYCoord", 2) == position
        assert game.get_bytes("wNumBagItems", 4) == THUNDERBOLT_TM
        assert game.get_bytes("wPartyDataStart", len(party)) == party


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", required=True, type=Path)
    parser.add_argument("--boot", required=True, type=Path, help="SameBoy's CGB boot ROM.")
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        check_compatibility(args.sameboy, args.boot, args.directory / f"poke{color}.gbc", color)
        print(f"{color.title()} entered New Game, opened TM INFO, and continued its save in CGB compatibility mode.",
              flush=True)


if __name__ == "__main__":
    main()
