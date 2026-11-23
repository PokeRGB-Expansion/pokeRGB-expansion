"""Check that VBlank does not copy unfinished battle slide steps."""

import argparse
import ctypes as C
from pathlib import Path

from cartridge_smoke import Game


DMG, SGB = 0x002, 0x004
SPACE = 0x7F
WIDTH, HEIGHT = 20, 18
BG_MAP = 0x1800  # Offset of tile map $9800 in VRAM.
PARTIAL_STEP_AT_LINE = {
    "faint": 142,
    "trainer": 140,
    "switch": 139,
}
PICTURE_CELLS = {
    "faint": (12, 0, 7, 7),
    "trainer": (12, 0, 7, 7),
    "switch": (0, 5, 8, 7),
}


def run_until(game, ready, *, limit=50000):
    for _ in range(limit):
        if ready():
            return
        game.core.GB_run(game.gb)
    raise AssertionError(f"No matching instruction at {game.cpu.pc:04x}.")


def picture(tilemap, kind):
    x, y, width, height = PICTURE_CELLS[kind]
    return b"".join(tilemap[(y + row) * WIDTH + x:(y + row) * WIDTH + x + width]
                    for row in range(height))


def first_complete_step(old, kind):
    if kind == "faint":
        return bytes((SPACE,)) * 7 + old[:-7]
    if kind == "trainer":
        return b"".join(bytes((SPACE,)) + old[start:start + 6] for start in range(0, len(old), 7))
    return bytes(tile + 7 if tile + 7 < 0x62 else SPACE for tile in old)


def seed_background(game):
    tiles = bytearray((SPACE,)) * (WIDTH * HEIGHT)
    for column in range(7):
        for row in range(7):
            tiles[row * WIDTH + 12 + column] = 7 * column + row
            tiles[(row + 5) * WIDTH + 1 + column] = 0x31 + 7 * column + row
    game.put("wTileMap", tiles)
    size = C.c_size_t()
    vram = game.core.GB_get_direct_access(game.gb, 3, C.byref(size), None)
    for row in range(HEIGHT):
        C.memmove(vram + BG_MAP + row * 32, bytes(tiles[row * WIDTH:(row + 1) * WIDTH]), WIDTH)
    return bytes(tiles), vram


def slide(game, kind):
    tilemap = game.addresses["wTileMap"][1]
    if kind == "faint":
        game.invoke("SlideDownFaintedMonPic")
        game.cpu.hl = tilemap + 5 * WIDTH + 12
        game.cpu.de = tilemap + 6 * WIDTH + 12
    elif kind == "trainer":
        game.invoke("SlideTrainerPicOffScreen")
        game.cpu.hl = tilemap + 18
        game.cpu.af = 8 << 8
    else:
        game.put("hWhoseTurn", (0,))
        game.invoke("AnimationSlideMonOff")


def check_step(game, kind, enabled):
    game.invoke("DelayFrame")
    game.return_to_stub()
    game.put("hAutoBGTransferDest", (0, 0x98))
    game.put("hAutoBGTransferEnabled", (enabled,))
    game.put("wStatusFlags5", (0x10,))
    game.put("wBattleResult", (1,))
    game.put("wIsInBattle", (2,))
    initial, vram = seed_background(game)

    # Force an interrupt during the first copy, instead of waiting for a lucky frame.
    line = PARTIAL_STEP_AT_LINE[kind]
    run_until(game, lambda: game.core.GB_safe_read_memory(game.gb, 0xFF44) == line)
    game.put("hAutoBGTransferPortion", (1 if kind == "switch" else 0,))
    game.write(0xFF0F, (0,))
    frame = game.get("wPlayTimeFrames")
    slide(game, kind)

    run_until(game, lambda: game.cpu.pc == game.addresses["AutoBgMapTransfer"][1])
    changed = picture(game.get_bytes("wTileMap", WIDTH * HEIGHT), kind)
    old = picture(initial, kind)
    assert changed not in (old, first_complete_step(old, kind)), kind
    assert game.get("hAutoBGTransferEnabled") == 0
    run_until(game, lambda: game.cpu.pc == game.addresses["VBlankCopyBgMap"][1])
    frame_bytes = b"".join(C.string_at(vram + BG_MAP + row * 32, WIDTH) for row in range(HEIGHT))
    assert picture(frame_bytes, kind) == old

    expected_frames = {"faint": 15, "trainer": 17, "switch": 25}[kind]
    game.tick(expected_frames - 1)
    run_until(game, lambda: game.cpu.pc == 0xC900)
    assert game.get("hAutoBGTransferEnabled") == enabled
    assert game.get("wStatusFlags5") == 0x10, (kind, enabled)
    assert game.get("wBattleResult") == 1
    assert game.get("wIsInBattle") == 2
    assert set(picture(game.get_bytes("wTileMap", WIDTH * HEIGHT), kind)) == {SPACE}
    # The first interrupt occurs early. The original waits account for the rest.
    elapsed = (game.get("wPlayTimeFrames") - frame) % 60
    assert elapsed == expected_frames, (kind, enabled, elapsed, expected_frames)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--sgb-boot", type=Path)
    args = parser.parse_args()
    models = [("DMG", DMG, args.boot)]
    if args.sgb_boot:
        models.append(("SGB", SGB, args.sgb_boot))
    for name, mode, boot in models:
        for color in ("red", "blue", "green"):
            with Game(args.sameboy, boot, args.directory / f"poke{color}.gbc", model=mode) as game:
                game.new_game()
                for kind in ("faint", "trainer", "switch"):
                    for enabled in (0, 1):
                        check_step(game, kind, enabled)
            print(f"{color.title()} {name}: battle slide timing passed", flush=True)


if __name__ == "__main__":
    main()
