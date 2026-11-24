"""Check the Pokédex owned marker in battle and after returning from menus."""

import argparse
import ctypes as C
from pathlib import Path

from acid_armor import invoke_visual
from adventure_checkpoints import advance_text_until, set_event
from battle_stats_return import battle_ready, open_stats_and_return, shows
from cartridge_smoke import Game, seed_party
from level_up_moves import check_replacement
from title_smoke import RGBCallback, SGB_HEIGHT, SGB_MODEL, SGB_WIDTH, encode_rgb

DEX_EVENT = 0x25
PIDGEY, DITTO, MAROWAK = 0x24, 0x4C, 0x91
DEX_PIDGEY, DEX_DITTO, DEX_MAROWAK = 16, 132, 105
ROUTE_1, TOWER_6F = 0x0C, 0x93
SCOPE = 0x48
TILE, BLANK = 0xCB, 0x7F
A, B, START = 4, 5, 7


def mark_owned(game, dex_number, owned=True):
    byte, bit = divmod(dex_number - 1, 8)
    address = game.addresses["wPokedexOwned"][1] + byte
    value = game.get("wPokedexOwned", byte)
    game.write(address, (value | 1 << bit if owned else value & ~(1 << bit),))


def marker_tile(game):
    return game.get("wTileMap", 20 + 1)


def marker_graphics(game):
    size = C.c_size_t()
    vram = game.core.GB_get_direct_access(game.gb, 3, C.byref(size), None)
    return C.string_at(vram + 0x800 + (TILE - 0x80) * 16, 16)


def expected_graphics(game, rom, disabled):
    label = "FontGraphics" if disabled else "PokeballTileGraphics"
    bank, address = game.addresses[label]
    start = bank * 0x4000 + address % 0x4000
    data = rom.read_bytes()
    if disabled:
        # Authors can keep another character in the slot. The font loader
        # expands each 1bpp row into the two identical Game Boy bitplanes.
        start += (TILE - 0x80) * 8
        return bytes(value for row in data[start:start + 8] for value in (row, row))
    return data[start:start + 16]


def start_wild(game, *, safari=False):
    game.new_game()
    seed_party(game)
    set_event(game, DEX_EVENT)
    mark_owned(game, DEX_PIDGEY)
    game.put("wOptions", (0xC1,))
    game.enter_map(ROUTE_1, 10, 5, 4)
    if safari:
        game.put("wBattleType", (2,))
        game.put("wNumSafariBalls", (30,))
    game.put("wCurOpponent", (PIDGEY,))
    game.put("wCurEnemyLevel", (5,))
    if safari:
        advance_text_until(game, lambda: shows(game, "BAIT", "ROCK", "RUN"))
    else:
        advance_text_until(game, lambda: battle_ready(game))
    game.tick(24)


def check_battle(library, boot, rom, *, disabled, minimal):
    with Game(library, boot, rom) as game:
        assert ("DrawBattleCaughtMarker" not in game.addresses) == disabled
        start_wild(game)
        expected = BLANK if disabled else TILE
        graphics = expected_graphics(game, rom, disabled)
        assert marker_tile(game) == expected
        assert marker_graphics(game) == graphics

        game.press(A)
        game.wait(lambda: shows(game, "SPLASH"))
        game.tick(12)
        game.press(START)
        game.wait(lambda: shows(game, "SELECT EFFECT"))
        game.press(B)
        game.wait(lambda: shows(game, "SPLASH") and not shows(game, "SELECT EFFECT"))
        game.tick(12)
        game.press(B)
        game.wait(lambda: battle_ready(game))
        assert marker_tile(game) == expected and marker_graphics(game) == graphics

        open_stats_and_return(game)
        assert marker_tile(game) == expected and marker_graphics(game) == graphics

        def redraw(visible):
            owned = game.get_bytes("wPokedexOwned", 19)
            seen = game.get_bytes("wPokedexSeen", 19)
            # Leave a stale marker to confirm each negative case clears it.
            game.write(game.addresses["wTileMap"][1] + 21, (TILE,))
            stop = invoke_visual(game, "DrawEnemyHUDAndHPBar")
            game.wait(lambda: game.cpu.pc == stop)
            assert marker_tile(game) == (TILE if visible and not disabled else BLANK)
            assert game.get_bytes("wPokedexOwned", 19) == owned
            assert game.get_bytes("wPokedexSeen", 19) == seen

        # Seen alone is insufficient. Ownership survives releasing the last copy.
        mark_owned(game, DEX_PIDGEY, False)
        assert game.get("wPokedexSeen", 1) & 0x80
        redraw(False)
        mark_owned(game, DEX_PIDGEY)
        game.put("wPartyCount", (6,))
        game.put("wBoxCount", (20,))  # A full box does not clear a collection record.
        redraw(True)

        flag_byte, flag_bit = divmod(DEX_EVENT, 8)
        address = game.addresses["wEventFlags"][1] + flag_byte
        game.write(address, (game.get("wEventFlags", flag_byte) & ~(1 << flag_bit),))
        redraw(False)
        set_event(game, DEX_EVENT)
        for field, value in (("wIsInBattle", 2), ("wBattleType", 1), ("wLinkState", 4)):
            previous = game.get(field)
            game.put(field, (value,))
            redraw(False)
            game.put(field, (previous,))

        # A wild Ditto has copied owned Pidgey. Its own record decides the result.
        game.put("wEnemyMonSpecies2", (DITTO,))
        game.put("wEnemyBattleStatus3", (1 << 3,))
        redraw(False)
        mark_owned(game, DEX_DITTO)
        mark_owned(game, DEX_PIDGEY, False)
        redraw(True)

        # Scope alone must never add a marker to the scripted Marowak.
        game.put("wCurMap", (TOWER_6F,))
        redraw(False)
        game.put("wNumBagItems", (1, SCOPE, 1, 0xFF))
        redraw(True)
        game.put("wEnemyMonSpecies2", (MAROWAK,))
        game.put("wCurOpponent", (MAROWAK,))
        mark_owned(game, DEX_MAROWAK)
        redraw(False)
        game.put("wCurOpponent", (0,))  # Ordinary wild Marowak.
        game.put("wCurMap", (ROUTE_1,))
        redraw(True)
        for species in (0, 0x1F, 0xFF):  # No species, MissingNo., invalid index.
            game.put("wEnemyMonSpecies2", (species,))
            redraw(False)

        # A level-up offer can take the player to the move-replacement list.
        game.put("wEnemyMonSpecies2", (PIDGEY,))
        mark_owned(game, DEX_PIDGEY)
        if rom.stem == "pokered":
            check_replacement(game, minimal=minimal)
            redraw(True)
            assert marker_graphics(game) == graphics


def check_sgb(library, boot, rom, *, disabled):
    with Game(library, boot, rom, model=SGB_MODEL) as game:
        pixels = (C.c_uint32 * (SGB_WIDTH * SGB_HEIGHT))()
        game.core.GB_set_rgb_encode_callback.argtypes = [C.c_void_p, RGBCallback]
        game.core.GB_set_rgb_encode_callback(game.gb, encode_rgb)
        game.core.GB_set_pixels_output.argtypes = [C.c_void_p, C.POINTER(C.c_uint32)]
        game.core.GB_set_pixels_output(game.gb, pixels)
        game.core.GB_set_rendering_disabled(game.gb, False)
        start_wild(game)
        assert game.get("wOnSGB")
        graphics = expected_graphics(game, rom, disabled)
        if not disabled:
            graphics = bytes(plane for low, high in zip(graphics[::2], graphics[1::2])
                             for plane in (high, low & high))
        assert marker_graphics(game) == graphics
        max_hp = int.from_bytes(game.get_bytes("wEnemyMonMaxHP", 2), "big")
        first_picture = None
        for hp, color in ((max_hp, 0), (max_hp // 2, 1), (1, 2)):
            game.put("wEnemyMonHP", hp.to_bytes(2, "big"))
            stop = invoke_visual(game, "DrawEnemyHUDAndHPBar")
            game.wait(lambda: game.cpu.pc == stop)
            game.tick(25)
            assert game.get("wEnemyHPBarColor") == color
            assert marker_tile(game) == (BLANK if disabled else TILE)
            # The SGB frame places the GB screen at (48, 40).
            picture = tuple(pixels[y * SGB_WIDTH + x]
                            for y in range(48, 56) for x in range(56, 64))
            assert len(set(picture)) == (1 if disabled else 3)
            if first_picture is None:
                first_picture = picture
            assert picture == first_picture


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--sgb-boot", type=Path)
    expected = parser.add_mutually_exclusive_group()
    expected.add_argument("--disabled", action="store_true")
    expected.add_argument("--enabled", action="store_true")
    parser.add_argument("--color", choices=("red", "blue", "green"))
    args = parser.parse_args()
    for color in (args.color,) if args.color else ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        if args.enabled or args.disabled:
            disabled = args.disabled
        else:
            disabled = " DrawBattleCaughtMarker\n" not in rom.with_suffix(".sym").read_text()
        check_battle(args.sameboy, args.boot, rom, disabled=disabled,
                     minimal=args.directory.name == "minimal")
        with Game(args.sameboy, args.boot, rom) as game:
            start_wild(game, safari=True)
            assert marker_tile(game) == (BLANK if disabled else TILE)
        if args.sgb_boot:
            check_sgb(args.sameboy, args.sgb_boot, rom, disabled=disabled)
        print(f"{args.directory.name} {color}: caught marker visibility, graphics and redraws passed",
              flush=True)


if __name__ == "__main__":
    main()
