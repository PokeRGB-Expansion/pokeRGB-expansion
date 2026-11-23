"""Check key adventure gates with controller input from seeded map checkpoints."""

import argparse
from pathlib import Path

from cartridge_smoke import Game, seed_party


RIGHT, LEFT, UP, DOWN, A = range(5)
PALLET_TOWN = 0x00
PEWTER_CITY = 0x02
CERULEAN_CITY = 0x03
LAVENDER_TOWN = 0x04
FUCHSIA_CITY = 0x07
SAFFRON_CITY = 0x0A
ROUTE_22 = 0x21
ROUTE_23 = 0x22
OAKS_LAB = 0x28
PEWTER_GYM = 0x36
HALL_OF_FAME = 0x76
CHAMPIONS_ROOM = 0x78
POKEMON_TOWER_6F = 0x93
POKEMON_TOWER_7F = 0x94
SAFARI_ZONE_GATE = 0x9C
ROUTE_22_GATE = 0xC1
SAFARI_ZONE_CENTER = 0xDC
CERULEAN_CAVE_1F = 0xE4
SILPH_CO_11F = 0xEB
LORELEIS_ROOM = 0xF5
BRUNOS_ROOM = 0xF6

BROCK_DEFEATED_EVENT = 0x77
GHOST_DEFEATED_EVENT = 0x10F
IN_SAFARI_ZONE_EVENT = 0x24F
ROUTE_23_BADGE_EVENT = 0x530
SILPH_11_DOOR_OPEN_EVENT = 0x788
LORELEI_DEFEATED_EVENT = 0x8E1


def position(game):
    return game.get("wXCoord"), game.get("wYCoord")


def checkpoint(game, map_id, width, x, y, *, last_map):
    # Match event_displacement in macros/coords.asm. The cartridge loads its
    # own map, collisions, objects and scripts from this starting position.
    view = game.addresses["wOverworldMap"][1] + 7 + width
    view += (width + 6) * (y // 2) + x // 2
    game.put("wCurMap", (map_id,))
    game.put("wCurrentTileBlockMapViewPointer", view.to_bytes(2, "little"))
    game.put("wYCoord", (y, x, y % 2, x % 2))
    game.put("wLastMap", (last_map,))
    game.put("wDestinationWarpID", (0xFF,))
    game.put("wMovementFlags", (0,))
    game.put("wCurMapTileset", (game.get("wCurMapTileset") & 0x7F,))
    game.invoke("EnterMap")
    game.tick(24)
    assert game.get("wCurMap") == map_id
    assert game.get("wCurMapWidth") == width


def event(game, number):
    byte, bit = divmod(number, 8)
    return bool(game.get("wEventFlags", byte) & (1 << bit))


def set_event(game, number):
    byte, bit = divmod(number, 8)
    address = game.addresses["wEventFlags"][1] + byte
    game.write(address, (game.get("wEventFlags", byte) | (1 << bit),))


def shows(game, *words, accept=False):
    game.wait(lambda: all(word in game.visible_text() for word in words), accept=accept)


def advance_text_until(game, condition, *, attempts=200):
    for _ in range(attempts):
        if condition():
            return
        game.press(A)
        game.tick(8)
    raise AssertionError(f"Text did not end at {position(game)}.\n{game.visible_text()}")


def hold_until(game, key, reached):
    game.core.GB_set_key_state(game.gb, key, True)
    try:
        game.wait(reached)
    except AssertionError as error:
        raise AssertionError(f"Could not walk from {position(game)}.") from error
    finally:
        game.core.GB_set_key_state(game.gb, key, False)


def walk_to(game, key, x, y):
    hold_until(game, key, lambda: position(game) == (x, y))
    game.wait(lambda: game.get("wWalkCounter") == 0)


def check_starter(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        assert game.get("wPartyCount") == 0
        checkpoint(game, PALLET_TOWN, 10, 10, 2, last_map=PALLET_TOWN)
        walk_to(game, UP, 10, 1)
        advance_text_until(game, lambda: game.get("wCurMap") == OAKS_LAB
                           and game.get("wOaksLabCurScript") == 6)
        assert position(game) == (5, 3)
        walk_to(game, DOWN, 5, 4)
        walk_to(game, RIGHT, 8, 4)
        # Face the Bulbasaur ball. Its occupied square prevents walking.
        game.press(UP)
        game.press(A)
        shows(game, "BULBASAUR", "YES", "NO", accept=True)
        game.press(A)
        advance_text_until(game, lambda: "YES" in game.visible_text()
                           and "nickname" in game.visible_text())
        game.press(DOWN)
        game.press(A)
        advance_text_until(game, lambda: game.get("wOaksLabCurScript") >= 10)
        assert game.get_bytes("wPartySpecies", 2) == bytes((0x99, 0xFF))
        assert game.get("wPartyCount") == 1
        assert game.get("wRivalStarter") == 0xB0  # Charmander.


def check_league_badges(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        checkpoint(game, ROUTE_22_GATE, 5, 4, 3, last_map=ROUTE_22)
        walk_to(game, UP, 4, 2)
        shows(game, "BOULDERBADGE", "yet", accept=True)
        game.wait(lambda: position(game) == (4, 3) and game.get("wRoute22GateCurScript") == 0,
                  accept=True)
        game.put("wObtainedBadges", (0x01,))
        walk_to(game, UP, 4, 2)
        shows(game, "Go right ahead", accept=True)
        advance_text_until(game, lambda: game.get("wRoute22GateCurScript") == 2
                           and "Go right ahead" not in game.visible_text())
        hold_until(game, UP, lambda: game.get("wCurMap") == ROUTE_23)
        game.tick(60)

        walk_to(game, UP, 7, 136)
        shows(game, "CASCADEBADGE", "yet", accept=True)
        game.wait(lambda: position(game) == (7, 137) and game.get("wRoute23CurScript") == 0,
                  accept=True)
        assert not event(game, ROUTE_23_BADGE_EVENT)
        game.put("wObtainedBadges", (0x03,))
        walk_to(game, UP, 7, 136)
        shows(game, "go right ahead", accept=True)
        game.wait(lambda: event(game, ROUTE_23_BADGE_EVENT), accept=True)
        advance_text_until(game, lambda: game.get("wRoute23CurScript") == 0)
        walk_to(game, UP, 7, 135)


def check_safari(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        game.put("wPlayerMoney", (0, 0x10, 0))
        checkpoint(game, SAFARI_ZONE_GATE, 4, 4, 3, last_map=FUCHSIA_CITY)
        walk_to(game, UP, 4, 2)
        shows(game, "YES", "NO", accept=True)
        game.press(DOWN)
        game.press(A)
        game.wait(lambda: position(game) == (4, 3) and game.get("wSafariZoneGateCurScript") == 0,
                  accept=True)
        assert game.get_bytes("wPlayerMoney", 3) == bytes((0, 0x10, 0))
        assert not event(game, IN_SAFARI_ZONE_EVENT)
        walk_to(game, UP, 4, 2)
        shows(game, "YES", "NO", accept=True)
        game.press(A)
        advance_text_until(game, lambda: game.get("wCurMap") == SAFARI_ZONE_CENTER)
        assert game.get_bytes("wPlayerMoney", 3) == bytes((0, 0x05, 0))
        assert game.get("wNumSafariBalls") == 30
        assert event(game, IN_SAFARI_ZONE_EVENT)
        steps = int.from_bytes(game.get_bytes("wSafariSteps", 2), "big")
        assert 498 <= steps <= 502


def seed_water_party(game):
    seed_party(game)
    game.put("wPartyMon1OTID", game.get_bytes("wPlayerID", 2))
    game.put("wPartyMon1Moves", (0x39, 0, 0, 0))  # Surf
    game.put("wPartyMon1Type", (0x15, 0x15))  # Water
    game.put("wPartyMon1Special", (0, 180))
    game.put("wPartyMon1Speed", (0, 180))


def check_gym(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_water_party(game)
        assert game.get("wObtainedBadges") == 0
        game.put("wOptions", (0xC1,))  # Set style, no animations, fast text.
        checkpoint(game, PEWTER_GYM, 5, 4, 2, last_map=PEWTER_CITY)
        game.press(UP)
        game.press(A)
        advance_text_until(game, lambda: "FIGHT" in game.visible_text()
                           and "GEODUDE" in game.visible_text())
        advance_text_until(game, lambda: game.get("wObtainedBadges") == 1
                           and game.get("wPewterGymCurScript") == 0, attempts=450)
        assert event(game, BROCK_DEFEATED_EVENT)
        assert game.get_bytes("wNumBagItems", 4) == bytes((1, 0xEA, 1, 0xFF))
        assert game.get("wCurMap") == PEWTER_GYM


def check_tower(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_water_party(game)
        # No random encounter tiles lie between this position and the stairs.
        checkpoint(game, POKEMON_TOWER_6F, 10, 11, 16, last_map=LAVENDER_TOWN)
        walk_to(game, LEFT, 10, 16)
        advance_text_until(game, lambda: all(word in game.visible_text()
                                             for word in ("GHOST", "FIGHT", "RUN")))
        game.press(RIGHT)
        game.press(DOWN)
        game.press(A)
        advance_text_until(game, lambda: game.get("wIsInBattle") == 0
                           and position(game) == (11, 16)
                           and game.get("wPokemonTower6FCurScript") == 0)
        assert not event(game, GHOST_DEFEATED_EVENT)

        game.put("wNumBagItems", (1, 0x48, 1, 0xFF))  # Silph Scope
        walk_to(game, LEFT, 10, 16)
        advance_text_until(game, lambda: "MAROWAK" in game.visible_text()
                           and "FIGHT" in game.visible_text())
        game.press(A)
        shows(game, "SURF")
        game.press(A)
        advance_text_until(game, lambda: game.get("wIsInBattle") == 0
                           and event(game, GHOST_DEFEATED_EVENT)
                           and game.get("wPokemonTower6FCurScript") == 0)
        hold_until(game, LEFT, lambda: game.get("wCurMap") == POKEMON_TOWER_7F)


def check_silph(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        checkpoint(game, SILPH_CO_11F, 9, 6, 14, last_map=SAFFRON_CITY)
        game.press(UP)
        assert position(game) == (6, 14)
        game.press(A)
        shows(game, "CARD KEY", "needs")
        assert not event(game, SILPH_11_DOOR_OPEN_EVENT)
        advance_text_until(game, lambda: "needs" not in game.visible_text())

        key = bytes((1, 0x30, 1, 0xFF))
        game.put("wNumBagItems", key)
        game.press(A)
        advance_text_until(game, lambda: "opened the door" in game.visible_text())
        advance_text_until(game, lambda: event(game, SILPH_11_DOOR_OPEN_EVENT))
        assert game.get_bytes("wNumBagItems", len(key)) == key

        # After leaving and returning, the door stays open.
        checkpoint(game, SILPH_CO_11F, 9, 6, 14, last_map=SAFFRON_CITY)
        walk_to(game, UP, 6, 13)


def check_league_room(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        checkpoint(game, LORELEIS_ROOM, 5, 4, 1, last_map=ROUTE_23)
        assert game.get("wElite4Flags") & 2
        game.core.GB_set_key_state(game.gb, UP, True)
        game.tick(50)
        game.core.GB_set_key_state(game.gb, UP, False)
        assert game.get("wCurMap") == LORELEIS_ROOM
        assert position(game) == (4, 1)
        set_event(game, LORELEI_DEFEATED_EVENT)
        checkpoint(game, LORELEIS_ROOM, 5, 4, 1, last_map=ROUTE_23)
        hold_until(game, UP, lambda: game.get("wCurMap") == BRUNOS_ROOM)


def battery_offset(game, label):
    bank, address = game.addresses[label]
    return bank * 8192 + address - 0xA000


def check_hall_of_fame(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        checkpoint(game, CERULEAN_CITY, 20, 4, 13, last_map=CERULEAN_CITY)
        game.press(UP)
        assert position(game) == (4, 13)
        game.press(A)
        shows(game, "CAVE", accept=True)

    with Game(library, boot, rom) as game:
        game.new_game()
        seed_party(game)
        # Start at the Champion's exit after the rival battle. The game
        # walks to Oak, records the party, plays the credits and saves.
        checkpoint(game, HALL_OF_FAME, 5, 4, 7, last_map=CHAMPIONS_ROOM)
        team = battery_offset(game, "sHallOfFame")
        checksum = battery_offset(game, "sMainDataCheckSum")
        main = battery_offset(game, "sGameData")
        battery = game.battery()
        advance_text_until(game, lambda: game.get("wSaveFileStatus") == 2
                           and battery[team] == 0x69 and battery[team + 16] == 0x1B
                           and battery[checksum] == (255 - sum(battery[main:checksum])) & 255,
                           attempts=1100)
        # Allow the full-save routines to finish when the primary checksum
        # first starts to match.
        game.tick(200)
        saved = bytes(battery[team:])

    with Game(library, boot, rom) as game:
        game.tick(240)
        game.battery()[team:] = saved
        game.invoke("TryLoadSaveFile")
        game.return_to_stub()
        assert game.get("wSaveFileStatus") == 2
        assert game.get("wNumHoFTeams") == 1
        assert game.get("wLastBlackoutMap") == PALLET_TOWN
        assert game.get_bytes("wPartySpecies", 3) == bytes((0x69, 0x1B, 0xFF))
        checkpoint(game, CERULEAN_CITY, 20, 4, 13, last_map=CERULEAN_CITY)
        hold_until(game, UP, lambda: game.get("wCurMap") == CERULEAN_CAVE_1F)



def check_evolution(library, boot, rom):
    pikachu, raichu = 0x54, 0x55
    pidgey, pidgeotto = 0x24, 0x96
    kadabra, alakazam = 0x26, 0x95
    thunder_stone = 0x21
    core = rom.parent.name == "core"
    cases = (
        (pikachu, 18, "level", pikachu if core else raichu),
        (pidgey, 18, "level", pidgeotto),
        (pikachu, 18, "item", raichu),
        (kadabra, 24, "trade", alakazam),
    )
    for species, level, trigger, expected in cases:
        with Game(library, boot, rom) as game:
            game.new_game()
            seed_party(game)
            game.put("wPartySpecies", (species, 0x1b, 0xff))
            game.put("wPartyMon1Species", (species,))
            game.put("wPartyMon1Level", (level,))
            game.put("wPartyMon1BoxLevel", (level,))
            game.put("wWhichPokemon", (0,))
            game.put("wCanEvolveFlags", (1,))
            game.put("wForceEvolution", (0,))
            # This shared slot can hold a species ID after an ordinary battle.
            game.put("wCurItem", (thunder_stone,))
            if trigger == "item":
                game.put("wNumBagItems", (1, thunder_stone, 1, 0xff))
                game.invoke("ItemUseEvoStone")
                shows(game, "TEST")
            elif trigger == "trade":
                game.put("wLinkState", (0x32,))
                game.invoke("TryEvolvingMon")
            else:
                game.invoke("EvolutionAfterBattle")
            advance_text_until(game, lambda: game.cpu.pc == 0xc900)
            assert game.get("wPartySpecies") == expected, (species, trigger)
            assert game.get("wPartyMon1Species") == expected
            if trigger == "item":
                assert game.get("wNumBagItems") == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        for check in (check_starter, check_gym, check_tower, check_silph, check_safari,
                      check_evolution, check_league_badges, check_league_room, check_hall_of_fame):
            check(args.sameboy, args.boot, rom)
            print(f"{args.directory.name} {color}: {check.__name__.removeprefix('check_')} passed",
                  flush=True)


if __name__ == "__main__":
    main()
