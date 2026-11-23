"""Check the Forest's grass, encounter rate, and a real step into star grass."""

import argparse
import ctypes as C
import json
from pathlib import Path

from cartridge_smoke import Game, seed_party
from trainer_loss_authoring import advance_battle


FOREST, SAFARI_CENTER = 0x33, 0xDC
GRASS, STAR, WATER = 0x20, 0x34, 0x14
WIDTH, HEIGHT = 17, 24
RIGHT, LEFT, UP, DOWN, A = range(5)
SOURCE = Path(__file__).resolve().parents[1]
SLOT_ENDS = (50, 101, 140, 165, 190, 215, 228, 241, 252, 255)


def call_without_interrupts(game, routine):
    bank, entry = game.addresses[routine]
    # Keep the return stub out of the loaded block map and visible tiles.
    stop = game.addresses["wStringBuffer"][1]
    game.write(stop, (0x18, 0xFE))
    game.write(0xDFFD, stop.to_bytes(2, "little"))
    game.write(0xFFFF, (0,))
    if bank:
        game.write(0x2000, (bank,))
        game.put("hLoadedROMBank", (bank,))
    game.cpu.sp = 0xDFFD
    game.cpu.pc = entry
    for _ in range(15000):
        if game.cpu.pc == stop:
            return bool(game.cpu.af & 0x80)
        game.core.GB_run(game.gb)
    raise AssertionError(f"{routine} did not return at {game.cpu.pc:04x}.")


def load_view(game, width, x, y):
    base = game.addresses["wOverworldMap"][1]
    address = base + 7 + width + (width + 6) * (y // 2) + x // 2
    game.put("wCurrentTileBlockMapViewPointer", address.to_bytes(2, "little"))
    game.put("wYCoord", (y, x, y % 2, x % 2))
    call_without_interrupts(game, "LoadCurrentMapView")
    return tuple(game.get("wTileMap", 9 * 20 + col) for col in (8, 9))


def encounter(game, rate_roll, slot_roll=0):
    game.put("hRandomAdd", (rate_roll,))
    game.put("hRandomSub", (slot_roll,))
    result = call_without_interrupts(game, "TryDoWildEncounter")
    assert game.get("hRandomAdd") == rate_roll
    assert game.get("hRandomSub") == slot_roll
    return result


def map_grass():
    blocks = (SOURCE / "maps" / "ViridianForest.blk").read_bytes()
    tiles = (SOURCE / "gfx" / "blocksets" / "forest.bst").read_bytes()
    found = {}
    for y in range(HEIGHT * 2):
        for x in range(WIDTH * 2):
            block = blocks[(y // 2) * WIDTH + x // 2]
            cell = block * 16 + (y % 2) * 8 + (x % 2) * 2 + 4
            if tiles[cell] == GRASS:
                found[(x, y)] = tuple(tiles[cell:cell + 2])
    audit = json.loads((SOURCE / "spec" / "research" / "forest-encounter-audit.json").read_text())
    audited = {tuple(row["position"]) for row in audit["pokered"]["mismatches"]}
    assert len(audited) == 114
    assert {point for point, pair in found.items() if pair == (GRASS, STAR)} == audited
    assert sum(pair == (GRASS, GRASS) for pair in found.values()) == 251
    return found


def check_map(library, boot, rom, core, red):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        game.enter_map(FOREST, WIDTH, 6, 5)
        assert game.get("wGrassTile") == GRASS
        assert game.get("wGrassRate") == 8
        assert game.get("wWaterRate") == 0
        game.put("wNPCMovementScriptPointerTableNum", (0,))
        game.put("wMovementFlags", (0,))
        game.put("wRepelRemainingSteps", (0,))
        expected_first = (4, 0x70 if red else 0x7B)
        assert tuple(game.get_bytes("wGrassMons", 2)) == expected_first
        for (x, y), pair in map_grass().items():
            assert load_view(game, WIDTH, x, y) == pair, (x, y, pair)
            eligible = pair[1] == GRASS or core
            assert encounter(game, 7) == eligible, (x, y, pair, eligible)
            if eligible:
                assert (game.get("wCurEnemyLevel"), game.get("wEnemyMonSpecies2")) == expected_first
            assert not encounter(game, 8), (x, y, pair)

        for position in ((6, 5), (7, 5), (8, 5), (1, 0), (15, 47)):
            assert load_view(game, WIDTH, *position)[1] != GRASS
            assert not encounter(game, 0), position
        for location in ((6, 6), (7, 6)) if core else ((6, 6),):
            load_view(game, WIDTH, *location)
            data = game.get_bytes("wGrassMons", 20)
            for slot, high in enumerate(SLOT_ENDS):
                low = SLOT_ENDS[slot - 1] + 1 if slot else 0
                for value in (low, high):
                    assert encounter(game, 0, value)
                    assert (game.get("wCurEnemyLevel"), game.get("wEnemyMonSpecies2")) == (
                        data[2 * slot], data[2 * slot + 1]
                    )
            for party_level, allowed in ((5, False), (4, True), (3, True)):
                game.put("wPartyMon1Level", (party_level,))
                game.put("wRepelRemainingSteps", (2,))
                assert encounter(game, 0) == allowed
                assert game.get("wRepelRemainingSteps") == 1
            game.put("wRepelRemainingSteps", (0,))
            game.put("wNPCMovementScriptPointerTableNum", (1,))
            assert not encounter(game, 0)
            game.put("wNPCMovementScriptPointerTableNum", (0,))


def check_safari(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        game.enter_map(SAFARI_CENTER, 15, 5, 2)
        game.put("wNPCMovementScriptPointerTableNum", (0,))
        game.put("wMovementFlags", (0,))
        assert game.get("wGrassRate") == 30 and game.get("wWaterRate") == 0
        for position, pair, eligible in (
            ((5, 2), (GRASS, GRASS), True),
            ((5, 4), (GRASS, STAR), False),
            ((9, 8), (WATER, WATER), False),
        ):
            assert load_view(game, 15, *position) == pair
            assert encounter(game, 0) == eligible


def check_step(library, boot, rom, start, key, eligible):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        game.put("wPartyMon1Speed", (0, 180))
        game.put("wOptions", (0xC1,))
        game.enter_map(FOREST, WIDTH, *start)
        game.put("wNumberOfNoRandomBattleStepsLeft", (0,))
        target = (7, 6)
        bank, address = game.addresses["TryDoWildEncounter"]
        signature = C.CFUNCTYPE(None, C.c_void_p, C.c_uint16, C.c_uint8)
        set_callback = game.core.GB_set_execution_callback
        set_callback.argtypes = [C.c_void_p, signature]
        set_callback.restype = None
        attempted = []

        @signature
        def fix_roll(_, pc, opcode):
            if pc == address and game.get("hLoadedROMBank") == bank:
                if (game.get("wXCoord"), game.get("wYCoord")) == target:
                    attempted.append(target)
                    game.put("hRandomAdd", (0,))
                    game.put("hRandomSub", (0,))

        set_callback(game.gb, fix_roll)
        try:
            game.core.GB_set_key_state(game.gb, key, True)
            try:
                game.wait(lambda: (game.get("wXCoord"), game.get("wYCoord")) == target)
            finally:
                game.core.GB_set_key_state(game.gb, key, False)
            if eligible:
                advance_battle(game, lambda: game.get("wIsInBattle") == 1
                               and "FIGHT" in game.visible_text())
                assert game.get("wEnemyMonLevel") == 4
                if key == RIGHT:
                    game.tick(24)
                    game.press(RIGHT)
                    game.wait(lambda: game.get("wTopMenuItemX") == 15)
                    game.tick(12)
                    game.press(DOWN)
                    game.wait(lambda: game.get("wLastMenuItem") == 1)
                    game.press(A)
                    advance_battle(game, lambda: game.get("wIsInBattle") == 0
                                   and game.get("wCurMap") == FOREST)
                    assert (game.get("wXCoord"), game.get("wYCoord")) == target
            else:
                game.tick(110)
                assert game.get("wIsInBattle") == 0
            assert attempted == [target], attempted
        finally:
            set_callback(game.gb, signature())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--color", choices=("red", "blue", "green"), nargs="+")
    args = parser.parse_args()
    core = args.directory.name == "core"
    for color in args.color or ("red", "blue", "green"):
        fixture = (args.sameboy, args.boot, args.directory / f"poke{color}.gbc")
        check_map(*fixture, core, color == "red")
        check_safari(*fixture)
        for start, direction in (((6, 6), RIGHT), ((8, 6), LEFT), ((7, 5), DOWN), ((7, 7), UP)):
            check_step(*fixture, start, direction, core)
        print(f"{args.directory.name} {color}: Forest grass, nearby paths, and Safari controls passed",
              flush=True)


if __name__ == "__main__":
    main()
