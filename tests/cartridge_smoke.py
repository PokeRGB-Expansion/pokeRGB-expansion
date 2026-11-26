"""Run integrated cartridge smoke tests with the SameBoy core library."""

import argparse
import ctypes as C
from pathlib import Path


class Registers(C.Structure):
    _fields_ = [(name, C.c_uint16) for name in ("af", "bc", "de", "hl", "sp", "pc")]


class Game:
    def __init__(self, library, boot, rom, *, model=0x002):
        self.core = C.CDLL(str(library))
        ptr, byte, word = C.c_void_p, C.c_uint8, C.c_uint16
        signatures = {
            "alloc": (ptr, []),
            "init": (ptr, [ptr, word]),
            "dealloc": (None, [ptr]),
            "load_rom": (C.c_int, [ptr, C.c_char_p]),
            "load_boot_rom": (C.c_int, [ptr, C.c_char_p]),
            "set_rendering_disabled": (None, [ptr, C.c_bool]),
            "set_turbo_mode": (None, [ptr, C.c_bool, C.c_bool]),
            "run_frame": (C.c_ulonglong, [ptr]),
            "run": (C.c_uint, [ptr]),
            "safe_read_memory": (byte, [ptr, word]),
            "write_memory": (None, [ptr, word, byte]),
            "set_key_state": (None, [ptr, C.c_int, C.c_bool]),
            "get_registers": (C.POINTER(Registers), [ptr]),
            "get_direct_access": (ptr, [ptr, C.c_int, C.POINTER(C.c_size_t), C.POINTER(word)]),
        }
        for name, (result, args) in signatures.items():
            function = getattr(self.core, "GB_" + name)
            function.restype = result
            function.argtypes = args
        self.gb = self.core.GB_init(self.core.GB_alloc(), model)
        assert self.core.GB_load_rom(self.gb, bytes(rom)) == 0
        assert self.core.GB_load_boot_rom(self.gb, bytes(boot)) == 0
        self.core.GB_set_rendering_disabled(self.gb, True)
        self.core.GB_set_turbo_mode(self.gb, True, True)
        self.cpu = self.core.GB_get_registers(self.gb).contents
        self.addresses = {}
        for line in rom.with_suffix(".sym").read_text().splitlines():
            parts = line.split()
            if len(parts) == 2 and ":" in parts[0] and not line.startswith(";"):
                self.addresses[parts[1]] = tuple(int(value, 16) for value in parts[0].split(":"))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.core.GB_dealloc(self.gb)

    def tick(self, frames=1):
        for _ in range(frames):
            self.core.GB_run_frame(self.gb)

    def press(self, key):
        self.core.GB_set_key_state(self.gb, key, True)
        self.tick(3)
        self.core.GB_set_key_state(self.gb, key, False)
        self.tick(3)

    def get(self, label, offset=0):
        return self.core.GB_safe_read_memory(self.gb, self.addresses[label][1] + offset)

    def get_bytes(self, label, length):
        return bytes(self.get(label, offset) for offset in range(length))

    def write(self, address, data):
        for offset, value in enumerate(data):
            self.core.GB_write_memory(self.gb, address + offset, value)

    def put(self, label, data):
        self.write(self.addresses[label][1], data)

    def visible_text(self):
        def letter(tile):
            if 0x80 <= tile < 0x9a:
                return chr(tile - 0x80 + 65)
            if 0xa0 <= tile < 0xba:
                return chr(tile - 0xa0 + 97)
            if 0xf6 <= tile <= 0xff:
                return chr(tile - 0xf6 + 48)
            return " "

        tiles = self.get_bytes("wTileMap", 360)
        return "\n".join(
            "".join(letter(x) for x in tiles[row:row + 20])
            for row in range(0, 360, 20)
        )

    def wait(self, condition, *, accept=False):
        for attempt in range(250):
            if condition():
                return
            if accept and attempt % 8 == 7:
                self.press(4)
            else:
                self.tick(2)
        raise AssertionError(f"Timed out at {self.cpu.pc:04x}.\n{self.visible_text()}")

    def enter_map(self, map_id, width, x, y, *, last_map=None):
        """Place the player at a map position and run the normal map loader."""
        self.put("wCurMap", (map_id,))
        self.put("wYCoord", (y, x, y % 2, x % 2))
        map_start = self.addresses["wOverworldMap"][1]
        # Match the offset that event_displacement writes for map warps.
        view_start = map_start + (width + 6) * (y // 2 + 1) + x // 2 + 1
        self.put("wCurrentTileBlockMapViewPointer", view_start.to_bytes(2, "little"))
        if last_map is not None:
            self.put("wLastMap", (last_map,))
        self.invoke("EnterMap")
        self.wait(lambda: self.get("wCurMap") == map_id and self.get("wCurMapWidth") == width)
        self.tick(45)

    def enter_new_game(self, continue_present=False):
        if continue_present:
            self.press(3)
        self.press(4)
        if continue_present:
            self.tick(70)
        for _ in range(250):
            self.tick(12)
            if self.get("wCurMap") == 0x26 and self.get("wCurMapWidth"):
                self.tick(80)
                return
            if "NEW NAME" in self.visible_text():
                self.press(3)
            self.press(4)
        raise AssertionError("New Game did not reach the starting house.")

    def new_game(self):
        self.tick(240)
        self.press(7)
        self.tick(100)
        self.enter_new_game()

    def invoke(self, label):
        bank, address = self.addresses[label]
        if bank:
            self.write(0x2000, (bank,))
            self.put("hLoadedROMBank", (bank,))
        self.write(0xc900, (0x18, 0xfe))
        self.write(0xc940, (0xfb, 0xc3, address & 255, address >> 8))
        self.write(0xdffd, (0, 0xc9))
        self.write(0xffff, (1,))
        self.cpu.sp = 0xdffd
        self.cpu.pc = 0xc940

    def return_to_stub(self):
        self.wait(lambda: self.cpu.pc == 0xc900)

    def battery(self):
        size = C.c_size_t()
        pointer = self.core.GB_get_direct_access(self.gb, 2, C.byref(size), None)
        assert size.value == 32768
        return (C.c_ubyte * size.value).from_address(pointer)

    def box_position(self, index):
        bank, address = self.addresses[f"sBox{index}"]
        return bank * 8192 + address - 0xa000


def seed_party(game):
    game.put("wPartyCount", (2,))
    game.put("wPartySpecies", (0x69, 0x1b, 0xff))
    for slot, species in ((1, 0x69), (2, 0x1b)):
        mon = f"wPartyMon{slot}"
        game.put(mon + "Species", (species,))
        game.put(mon + "BoxLevel", (45,))
        game.put(mon + "Level", (45,))
        game.put(mon + "HP", (0, 160))
        game.put(mon + "MaxHP", (0, 160))
        game.put(mon + "Moves", (0x96, 0, 0, 0))
        game.put(mon + "PP", (40, 0, 0, 0))
        game.put(mon + "Nick", (0x93, 0x84, 0x92, 0x93, 0x50))


def older_save(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        game.put("wCurrentBoxNum", (0x80,))
        game.put("wPlayerID", (0x12, 0x34))
        game.put("wBoxCount", (0, 255))
        game.invoke("SaveGameData")
        game.return_to_stub()
        battery = game.battery()
        box_width = game.addresses["wBoxDataEnd"][1] - game.addresses["wBoxDataStart"][1]
        for index in range(1, 13):
            offset = game.box_position(index)
            battery[offset:offset + box_width] = bytes(box_width)
            battery[offset] = int(index in (2, 8))
            battery[offset + 1] = 0x1b if index in (2, 8) else 0xff
            battery[offset + 2] = 0xff
        for bank in (2, 3):
            start = bank * 8192
            end = start + 6 * box_width
            battery[end] = 255 - (sum(battery[start:end]) & 255)
            for index in range(6):
                lo = start + index * box_width
                battery[end + 1 + index] = 255 - (sum(battery[lo:lo + box_width]) & 255)
        return bytes(battery)


def check_box_changes(library, boot, rom):
    save = older_save(library, boot, rom)
    for confirm in (False, True):
        with Game(library, boot, rom) as game:
            game.new_game()
            game.battery()[:] = save
            game.invoke("MainMenu")
            game.wait(lambda: game.get("wSaveFileStatus") == 2 and game.get("wMaxMenuItem") == 2
                      and "CONTINUE" in game.visible_text())
            game.tick(15)
            game.enter_new_game(continue_present=True)
            assert not game.get("wCurrentBoxNum") & 0x80
            # Bank zero holds temporary sprite data. The player save is in banks 1–3.
            assert bytes(game.battery()[8192:]) == save[8192:]
            seed_party(game)
            game.put("wPlayerID", (0x56, 0x78))
            game.put("wOptions", (1,))
            game.invoke("ChangeBox")
            game.wait(lambda: game.get("wMaxMenuItem") == 11 and "BOX" in game.visible_text())
            assert game.get_bytes("wBoxMonCounts", 12) == bytes(12)
            game.wait(lambda: "OCCUPIED" in game.visible_text() and "0 20" in game.visible_text())
            if confirm:
                game.press(3)
                game.tick(12)
                game.press(4)
                game.wait(lambda: all(word in game.visible_text() for word in ("YES", "NO")), accept=True)
                game.tick(14)
                game.press(4)
                game.tick(170)
                assert game.get("wCurrentBoxNum") == 0x81
                assert bytes(game.battery()[8192:]) != save[8192:]
            else:
                game.press(5)
                game.return_to_stub()
                assert bytes(game.battery()[8192:]) == save[8192:]
            game.invoke("TryLoadSaveFile")
            game.return_to_stub()
            assert game.get("wSaveFileStatus") == 2
            assert game.get_bytes("wPlayerID", 2) == bytes((0x56, 0x78) if confirm else (0x12, 0x34))
            assert game.get("wPartyCount") == 2
            game.invoke("GetMonCountsForAllBoxes")
            game.return_to_stub()
            saved_counts = bytes(12) if confirm else bytes(int(n in (2, 8)) for n in range(1, 13))
            assert game.get_bytes("wBoxMonCounts", 12) == saved_counts


def check_machine_info(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        game.put("wNumBagItems", (1, 0xe0, 1, 0xff))
        game.invoke("StartMenu_Item")
        game.wait(lambda: "TM24" in game.visible_text() and "START INFO" in game.visible_text())
        rows = game.get_bytes("wTileMap", 360)
        game.press(7)
        game.wait(lambda: "THUNDERBOLT" in game.visible_text() and "SELECT EFFECT" in game.visible_text())
        assert "ELECTRIC" in game.visible_text()
        assert "95" in game.visible_text()
        assert game.get_bytes("wNumBagItems", 4) == bytes((1, 0xe0, 1, 0xff))
        game.press(5)
        game.wait(lambda: "SELECT EFFECT" not in game.visible_text() and "TM24" in game.visible_text())
        assert game.get("wCurrentMenuItem") == 0
        assert game.get_bytes("wNumBagItems", 4) == bytes((1, 0xe0, 1, 0xff))
        assert rows[:220] == game.get_bytes("wTileMap", 220)


def check_stats_info(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        game.put("wWhichPokemon", (0,))
        game.put("wMonDataLocation", (0,))
        game.invoke("StatusScreen")
        game.wait(lambda: "D PAD NAV" in game.visible_text() and "ATTACK" in game.visible_text())
        game.tick(90)
        assert game.get("wLoadedMonSpecies") == 0x69
        game.press(0)
        game.wait(lambda: "START INFO" in game.visible_text() and "SPLASH" in game.visible_text())
        game.tick(20)
        game.press(3)
        game.wait(lambda: game.get("wLoadedMonSpecies") == 0x1b and "SPLASH" in game.visible_text())
        game.tick(90)
        game.press(7)
        game.wait(lambda: "SELECT EFFECT" in game.visible_text())
        game.press(5)
        game.wait(lambda: "SELECT EFFECT" not in game.visible_text())
        game.tick(15)
        game.press(5)
        game.return_to_stub()
        assert game.get("wWhichPokemon") == 1
        assert game.get_bytes("wPartyMon2Moves", 4) == bytes((0x96, 0, 0, 0))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True, help="SameBoy DMG boot file.")
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        path = args.directory / f"poke{color}.gbc"
        check_box_changes(args.sameboy, args.boot, path)
        check_machine_info(args.sameboy, args.boot, path)
        check_stats_info(args.sameboy, args.boot, path)
        print(f"{args.directory.name} {color}: box saves, Bag Move INFO, and STATS controls passed", flush=True)


if __name__ == "__main__":
    main()
