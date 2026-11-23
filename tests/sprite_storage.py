"""Check picture decoding and storage bounds on the linked cartridges."""

import argparse
import ctypes
from pathlib import Path
import re

from adventure_checkpoints import battery_offset
from cartridge_smoke import Game


ROOT = Path(__file__).resolve().parents[1]
BANK_SIZE = 0x4000
PIC_CHUNK_BYTES = 7 * 7 * 8
PIC_TILE_BYTES = PIC_CHUNK_BYTES * 2


def direct_access(game, memory):
    size = ctypes.c_size_t()
    pointer = game.core.GB_get_direct_access(game.gb, memory, ctypes.byref(size), None)
    return (ctypes.c_ubyte * size.value).from_address(pointer)


def finish_decode(game, routine):
    for _ in range(450_000):
        if game.cpu.pc == 0xC900:
            return
        game.core.GB_run(game.gb)
    raise AssertionError(f"{routine} did not return. PC is {game.cpu.pc:04x}.")


def decode(game, bank, address, *, flipped=False):
    saved_bank = game.get("hLoadedROMBank")
    game.put("wSpriteFlipped", (int(flipped),))
    game.invoke("UncompressSpriteFromDE")
    game.cpu.af = bank << 8
    game.cpu.de = address
    finish_decode(game, "UncompressSpriteFromDE")
    assert game.get("hLoadedROMBank") == saved_bank
    start = battery_offset(game, "sSpriteBuffer1")
    return bytes(game.battery()[start:start + PIC_TILE_BYTES])


def center(game, dimensions):
    saved_bank = game.get("hLoadedROMBank")
    destination = game.addresses["vFrontPic"][1]
    game.invoke("LoadUncompressedSpriteData")
    # The caller supplies width in A's low nybble and height in C's high nybble.
    game.cpu.af = (dimensions & 15) << 8
    game.cpu.bc = dimensions & 0xF0
    game.cpu.de = destination
    finish_decode(game, "LoadUncompressedSpriteData")
    assert game.get("hLoadedROMBank") == saved_bank
    offset = destination - 0x8000
    return bytes(direct_access(game, 3)[offset:offset + PIC_TILE_BYTES])


def picture_labels():
    for folder in (ROOT / "gfx", ROOT / "data" / "pokemon"):
        for path in sorted(folder.rglob("*.asm")):
            yield from re.findall(r'(?m)^(\w+)::\s+INCBIN "[^"]+\.pic"', path.read_text())


def picture_offset(bank, address):
    return bank * BANK_SIZE + address - 0x4000


def stock_sprites(game, reference=None):
    rom = direct_access(game, 0)
    count = 0
    for label in picture_labels():
        if label not in game.addresses:
            continue  # Some source assets are conditional on the color.
        bank, address = game.addresses[label]
        dimensions = rom[picture_offset(bank, address)]
        assert 1 <= dimensions >> 4 <= 7 and 1 <= dimensions & 15 <= 7, label
        # Include a flipped picture to exercise the other unpack tables.
        flipped = label == "RhydonPicFront"
        chunks = decode(game, bank, address, flipped=flipped)
        assert any(chunks), label
        sprite = center(game, dimensions)
        assert any(sprite), label
        if reference is not None:
            source = reference.addresses[label]
            assert chunks == decode(reference, *source, flipped=flipped), label
            assert sprite == center(reference, dimensions), label
        count += 1
    assert count >= 300
    return count


def malformed_sprites(game):
    # Install small asset fixtures in this disposable emulator copy.
    assert "ValidateSpriteDimensions" in game.addresses
    rom = direct_access(game, 0)
    bank = len(rom) // BANK_SIZE - 1
    address = 0x7FF8
    start = picture_offset(bank, address)
    original = bytes(rom[start:start + 8])
    try:
        for header in (0x00, 0x10, 0x01, 0x88, 0x81, 0x18, 0xFF):
            rom[start] = header
            assert decode(game, bank, address) == bytes(PIC_TILE_BYTES)
            assert game.get_bytes("wSpriteInputPtr", 2) == (address + 1).to_bytes(2, "little")
        # A short stream ends at the ROM boundary before its second chunk.
        rom[start + 7] = 0x11
        assert decode(game, bank, 0x7FFF) == bytes(PIC_TILE_BYTES)
        assert game.get_bytes("wSpriteInputPtr", 2) == bytes((0, 0x80))
        assert decode(game, bank, 0x8000) == bytes(PIC_TILE_BYTES)
        # A zero run whose length code is missing its end bit.
        rom[start:start + 4] = bytes((0x11, 0x3F, 0xFF, 0xFF))
        assert decode(game, bank, address) == bytes(PIC_TILE_BYTES)
        assert game.get_bytes("wSpriteInputPtr", 2) == (address + 4).to_bytes(2, "little")
    finally:
        rom[start:start + 8] = original

    bank, address = game.addresses["RhydonPicFront"]
    for dimensions in (0x07, 0x70, 0x87, 0x78):
        assert any(decode(game, bank, address))
        assert center(game, dimensions) == bytes(PIC_TILE_BYTES)


def check(library, boot, cartridge, reference_path):
    with Game(library, boot, cartridge) as game:
        game.tick(240)
        scratch_end = battery_offset(game, "sSpriteBuffer2") + PIC_CHUNK_BYTES
        hall = battery_offset(game, "sHallOfFame")
        assert scratch_end < hall
        battery = game.battery()
        # Cover the gap, Hall of Fame, main save and both PC box banks.
        protected = bytes((offset % 251) for offset in range(scratch_end, len(battery)))
        battery[scratch_end:] = protected

        if reference_path is None:
            count = stock_sprites(game)
        else:
            with Game(library, boot, reference_path) as reference:
                reference.tick(240)
                count = stock_sprites(game, reference)
        assert bytes(battery[scratch_end:]) == protected
        malformed_sprites(game)
        assert bytes(battery[scratch_end:]) == protected
    print(f"{cartridge}: {count} original pictures and malformed asset cases passed", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--reference-dir", type=Path,
                        help="Compare picture bytes with matching pre-change builds.")
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        name = f"poke{color}.gbc"
        reference = args.reference_dir / name if args.reference_dir else None
        check(args.sameboy, args.boot, args.directory / name, reference)


if __name__ == "__main__":
    main()
