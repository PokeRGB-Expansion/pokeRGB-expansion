"""Check the compiled trainer teams and starter previews in a downstream game."""

import argparse
from pathlib import Path

from cartridge_smoke import Game
from pokedex_area import linked_offset, rom_offset
from trainer_movesets import load_team


def authored_moves(game, rom):
    if "TrainerMovesets" not in game.addresses:
        return {}
    pos = linked_offset(game, "TrainerMovesets")
    movesets = {}
    while address := int.from_bytes(rom[pos:pos + 2], "little"):
        slot = rom[pos + 2]
        movesets[address, slot] = rom[pos + 3:pos + 7]
        pos += 7
    return movesets


def check_trainers(game, rom):
    """Load each class/number and compare it with the team's own linked bytes."""
    bank, _ = game.addresses["TrainerDataPointers"]
    pointers = linked_offset(game, "TrainerDataPointers")
    pointer_end = linked_offset(game, "TrainerDataPointersEnd")
    starts = [int.from_bytes(rom[pos:pos + 2], "little") for pos in range(pointers, pointer_end, 2)]
    data_end = game.addresses["TrainerDataEnd"][1]
    overrides = authored_moves(game, rom)
    checked_overrides = set()
    move_table = linked_offset(game, "Moves")
    boundaries = sorted(set(starts) | {data_end})
    ends = dict(zip(boundaries, boundaries[1:]))
    team_count = 0
    game.put("wIsInBattle", (2,))
    for trainer, start in enumerate(starts, 1):
        # Empty classes in the reference games share the following class's label.
        if start == data_end or (trainer < len(starts) and start == starts[trainer]):
            continue
        end = ends[start]
        position = rom_offset(bank, start)
        limit = rom_offset(bank, end)
        number = 0
        while position < limit:
            address = 0x4000 + position % 0x4000
            level = rom[position]
            position += 1
            number += 1
            expected = []
            location = f"Trainer class {trainer}, team {number}"
            while position < limit and rom[position]:
                if level == 0xff:
                    member_level = rom[position]
                    position += 1
                else:
                    member_level = level
                assert position < limit and rom[position], f"{location}: missing species"
                expected.append((rom[position], member_level))
                position += 1
            assert position < limit and 1 <= len(expected) <= 6, f"{location}: invalid party or missing terminator"
            position += 1
            actual, _ = load_team(game, trainer, number)
            assert [mon[:2] for mon in actual] == expected, f"{location}: species or level differs from the team data"
            for slot, (_, _, moves, pp) in enumerate(actual):
                key = (address, slot)
                if key in overrides:
                    target = overrides[key]
                    # An unused move slot has zero PP. Each move record ends with its base PP.
                    expected_pp = bytes(rom[move_table + (move - 1) * 6 + 5] if move else 0 for move in target)
                    assert (moves, pp) == (target, expected_pp), f"{location}, slot {slot + 1}: custom moves or PP differ"
                    checked_overrides.add(key)
            team_count += 1
    assert checked_overrides == set(overrides), "A custom moveset does not point to a member of a trainer team"
    return team_count, len(checked_overrides)


def check_starter_previews(game, rom):
    balls = linked_offset(game, "OaksLabStarterBalls")
    order = linked_offset(game, "PokedexOrder")
    species = [rom[balls + slot * 4] for slot in range(3)]
    assert len(set(species)) == 3, "Choose three different lab starters"
    flag_bytes = game.addresses["wPokedexOwnedEnd"][1] - game.addresses["wPokedexOwned"][1]
    for chosen in species:
        assert chosen and rom[order + chosen - 1], f"Lab starter {chosen}: missing Pokédex entry"
        # Simulate a hack that already recorded some species before the lab.
        owned = bytearray([0x55] * flag_bytes)
        byte, bit = divmod(rom[order + chosen - 1] - 1, 8)
        owned[byte] &= ~(1 << bit)
        flags = {"wPokedexOwned": bytes(owned), "wPokedexSeen": bytes([0xff] * flag_bytes)}
        for field, expected in flags.items():
            game.put(field, expected)
        game.put("wPokedexNum", (chosen,))
        game.put("wNamedObjectIndex", (chosen,))
        game.invoke("StarterDex")
        # The first digit of weight can be blank. The tenths digit must be printed.
        game.wait(lambda: game.get("wTileMap", 8 * 20 + 16) >= 0xf6)
        game.wait(lambda: game.cpu.pc == 0xc900, accept=True)
        for field, expected in flags.items():
            assert game.get_bytes(field, flag_bytes) == expected, f"Starter {chosen}: preview changed {field}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build", type=Path, help="One game ROM or a build directory with poke*.gbc files.")
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    roms = sorted(args.build.glob("poke*.gbc")) if args.build.is_dir() else [args.build]
    if not roms or any(not rom.is_file() or not rom.with_suffix(".sym").is_file() for rom in roms):
        parser.error("Build the game first and keep its matching .sym file beside it.")
    for path in roms:
        data = path.read_bytes()
        with Game(args.sameboy, args.boot, path) as game:
            game.tick(240)  # Boot the hardware. Author checks do not start a Kanto adventure.
            teams, custom = check_trainers(game, data)
            check_starter_previews(game, data)
        print(f"{path.name}: checked {teams} trainer teams and three starter previews. Custom movesets checked: {custom}.", flush=True)


if __name__ == "__main__":
    main()
