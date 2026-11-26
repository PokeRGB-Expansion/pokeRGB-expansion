"""Play the outdoor party shortcut, item disposal, rod shortcut and Pokédex sort."""

import argparse
from pathlib import Path

from adventure_checkpoints import advance_text_until, set_event
from battle_stats_return import battle_ready, start_battle
from cartridge_smoke import Game, seed_party
from field_shortcuts import RIGHT, LEFT, UP, DOWN, A, B, SELECT, START, shore, shows
from pc_browsing import name_bytes, stock_pc
from sprite_storage import direct_access


def check_party(game):
    game.new_game()
    stock_pc(game)
    species = game.get_bytes("wPartySpecies", 7)
    game.press(START)
    shows(game, "ITEM", "OPTION")
    game.press(A)
    shows(game, "PARTYA", "SELECT to switch")
    game.press(DOWN)
    game.tick(12)
    game.press(SELECT)
    game.wait(lambda: game.get("wMenuItemToSwap") == 2)
    assert game.get_bytes("wPartySpecies", 7) == species
    game.tick(20)
    game.press(DOWN)
    game.tick(12)
    game.press(B)
    shows(game, "SELECT to switch")
    assert game.get("wMenuItemToSwap") == 0 and game.get_bytes("wPartySpecies", 7) == species
    game.press(SELECT)
    game.wait(lambda: game.get("wMenuItemToSwap") == 3)
    game.tick(34)
    game.press(UP)
    game.tick(16)
    game.press(SELECT)
    game.wait(lambda: game.get("wMenuItemToSwap") == 0)
    game.tick(80)
    assert game.get_bytes("wPartySpecies", 7) == species[:1] + species[2:3] + species[1:2] + species[3:]
    assert game.get_bytes("wPartyMon2Nick", 11) == name_bytes("PARTYC")
    assert game.get_bytes("wPartyMon3Nick", 11) == name_bytes("PARTYB")


def check_battle_party(game):
    start_battle(game, tower=False, scoped=False)
    species = game.get_bytes("wPartySpecies", 7)
    game.press(RIGHT)
    game.wait(lambda: game.get("wTopMenuItemX") == 15)
    game.tick(12)
    game.press(A)
    game.wait(lambda: game.visible_text().count("160 160") == 2)
    game.tick(20)
    game.press(SELECT)
    game.tick(32)
    assert "SELECT to switch" not in game.visible_text()
    assert game.get("wMenuItemToSwap") == 0
    assert game.get_bytes("wPartySpecies", 7) == species
    game.press(B)
    game.wait(lambda: battle_ready(game))


def check_toss(game, pc, boundaries=False):
    game.new_game()
    inventory = "wNumBoxItems" if pc else "wNumBagItems"
    item, name, total = (0x21, "THUNDERSTONE", 99) if boundaries else (0x14, "POTION", 24)
    game.put(inventory, (1, item, total, 0xff))
    game.invoke("PlayerPCToss" if pc else "StartMenu_Item")
    cases = ((None, 1, B), (DOWN, 99, A)) if boundaries else ((RIGHT, 11, B), (RIGHT, 11, A))
    for step, count, answer in cases:
        list_text = (name, "CANCEL", "to toss away") if pc else (name, "CANCEL")
        shows(game, *list_text, accept=True)
        game.press(A)
        if not pc:
            shows(game, "USE", "TOSS")
            game.press(DOWN)
            game.tick(12)
            game.press(A)
        def quantity_open():
            screen = game.visible_text()
            return game.get("wItemQuantity") == 1 and " 01" in screen and (not pc or "How many" in screen)

        game.wait(quantity_open, accept=pc)
        game.tick(12)
        if step is not None:
            game.press(step)
            game.wait(lambda: game.get("wItemQuantity") == count)
            game.tick(12)
        game.press(A)
        shows(game, "Throw away", "YES", "NO", accept=True)
        # Read the question itself. The original list also displays the stack size.
        assert any(name in row and str(count) in row for row in game.visible_text().splitlines()[-4:])
        assert game.get(inventory, 2) == total
        game.press(answer)
        game.tick(16)
    if count == total:
        game.wait(lambda: game.get(inventory) == 0, accept=True)
    else:
        game.wait(lambda: game.get(inventory, 2) == total - count, accept=True)


def check_dex(game):
    game.new_game()
    set_event(game, 0x25)
    # Seen Pidgey (#016), Vulpix (#037), and Abra (#063). Only Pidgey is owned.
    seen = bytearray(19)
    for dex in (16, 37, 63):
        seen[(dex - 1) // 8] |= 1 << ((dex - 1) % 8)
    game.put("wPokedexSeen", seen)
    game.put("wPokedexOwned", bytes((0, 0x80)) + bytes(17))
    game.put("wPokedexSavedRow", (0,))
    game.put("wPokedexSavedScrollOffset", (15,))
    game.press(START)
    shows(game, "ITEM", "OPTION")
    game.press(A)
    shows(game, "CONTENTS", "PIDGEY")
    game.press(SELECT)
    shows(game, "VULPIX", "ABRA", "PIDGEY")
    screen = game.visible_text()
    assert screen.index("ABRA") < screen.index("PIDGEY") < screen.index("VULPIX")
    assert game.get("wCurrentMenuItem") == 1  # same species after changing order
    assert game.get("wTileMap", 20 * 5 + 3) == 0x72
    game.press(UP)
    game.tick(16)
    game.press(A)
    game.wait(lambda: game.get("wPokedexNum") == 0x94)  # Abra's internal ID
    game.tick(18)
    game.press(A)
    shows(game, "ABRA")
    assert game.get_bytes("wPokedexOwned", 19) == bytes((0, 0x80)) + bytes(17)
    game.press(B)
    shows(game, "VULPIX", "PIDGEY", "ABRA", accept=True)
    game.press(SELECT)
    shows(game, "CONTENTS", "ABRA")
    assert game.get("wListScrollOffset") + game.get("wCurrentMenuItem") == 62
    game.press(UP)  # numeric #062 is unseen
    game.tick(15)
    game.press(SELECT)
    shows(game, "VULPIX", "PIDGEY", "ABRA")
    game.press(DOWN)
    game.tick(15)
    game.press(SELECT)
    game.wait(lambda: game.get("wDexAlphaMode") == 0)
    assert game.get("wListScrollOffset") + game.get("wCurrentMenuItem") == 61
    game.tick(15)
    game.press(B)
    shows(game, "OPTION")
    game.put("wPokedexSeen", bytes(19))
    game.put("wPokedexOwned", bytes(19))
    game.press(A)
    shows(game, "CONTENTS")
    game.press(SELECT)
    shows(game, "NONE SEEN")
    game.press(A)
    game.tick(15)
    assert "NONE SEEN" in game.visible_text()
    game.press(B)
    shows(game, "OPTION")


def check_complete_index(game):
    # Exercise the full list and an author's renamed and duplicate species.
    rom = direct_access(game, 0)
    def offset(label):
        bank, address = game.addresses[label]
        return bank * 0x4000 + address % 0x4000

    names = offset("MonsterNames")
    dex_numbers = bytes(rom[offset("PokedexOrder"):offset("PokedexOrder") + 190])
    for dex, new_name in ((1, "ZZZ"), (2, "Aaa"), (4, "AAA")):
        start = names + dex_numbers.index(dex) * 10
        rom[start:start + 10] = name_bytes(new_name)[:10]
    def sort_key(dex):
        start = names + dex_numbers.index(dex) * 10
        return bytes(c - 32 if 0xa0 <= c <= 0xb9 else c for c in rom[start:start + 10])
    expected = sorted(range(1, 152), key=sort_key)
    game.new_game()
    set_event(game, 0x25)
    game.put("wPokedexSeen", bytes([255] * 18 + [127]))
    game.press(START)
    shows(game, "OPTION")
    game.press(A)
    shows(game, "CONTENTS")
    game.press(SELECT)
    game.wait(lambda: game.get("wDexAlphaMode") == 1)
    assert game.get_bytes("wDexAlphaOrder", 151) == bytes(expected)
    assert expected.index(2) < expected.index(4)


def check_rod(game, rod):
    game.new_game()
    seed_party(game)
    game.put("wNumBagItems", (2, rod, 1, 6, 1, 0xff))
    game.put("wRegisteredItemTag", (0xd6, 6))  # existing Bicycle registration
    shore(game)
    game.press(START)
    shows(game, "ITEM", "OPTION")
    game.press(DOWN)
    game.tick(12)
    game.press(A)
    shows(game, {0x4c: "OLD ROD", 0x4d: "GOOD ROD", 0x4e: "SUPER ROD"}[rod], "CANCEL")
    assert game.visible_text().splitlines()[7].strip() == "SELECT"  # Bicycle
    game.press(A)
    shows(game, "REGISTER")
    game.press(DOWN)
    game.tick(12)
    game.press(A)
    game.wait(lambda: game.get("wRegisteredItem") == rod)
    game.wait(lambda: game.visible_text().splitlines()[5].strip() == "SELECT")
    assert "SELECT" not in game.visible_text().splitlines()[7]
    game.tick(20)
    game.press(B)
    shows(game, "OPTION")
    game.press(B)
    game.tick(80)
    game.press(SELECT)
    # A Good Rod can fail to hook anything. The shortcut keeps the ordinary roll.
    advance_text_until(game, lambda: battle_ready(game) or "nibble" in game.visible_text())
    if "nibble" in game.visible_text():
        assert rod != 0x4c
        return
    if rod == 0x4c:
        assert game.get("wEnemyMonSpecies2") == 0x85 and game.get("wEnemyMonLevel") == 5
    elif rod == 0x4d:
        assert game.get("wEnemyMonSpecies2") in (0x47, 0x9d) and game.get("wEnemyMonLevel") == 10
    else:
        assert game.get("wEnemyMonSpecies2") in (0x18, 0x47) and game.get("wEnemyMonLevel") == 15


def check_rod_off_water(game):
    game.new_game()
    # A deposited or invalid item cannot be used remotely.
    game.put("wRegisteredItemTag", (0xd6, 0x4c))
    game.enter_map(0x0c, 10, 5, 4)
    game.press(SELECT)
    game.tick(70)
    assert not game.get("wIsInBattle") and "OAK" not in game.visible_text()
    game.put("wNumBagItems", (1, 0x4c, 1, 0xff))
    game.press(SELECT)
    shows(game, "OAK")
    assert not game.get("wIsInBattle")
    assert game.get_bytes("wNumBagItems", 4) == bytes((1, 0x4c, 1, 0xff))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        for check in (check_party, lambda game: check_toss(game, False),
                      lambda game: check_toss(game, True), check_dex, check_rod_off_water):
            with Game(args.sameboy, args.boot, rom) as game:
                check(game)
        for rod in (0x4c, 0x4d, 0x4e):
            with Game(args.sameboy, args.boot, rom) as game:
                check_rod(game, rod)
        if color == "red":
            for check in (check_complete_index, check_battle_party,
                          lambda game: check_toss(game, False, boundaries=True),
                          lambda game: check_toss(game, True, boundaries=True)):
                with Game(args.sameboy, args.boot, rom) as game:
                    check(game)
        print(f"{args.directory.name} {color}: party, TOSS, rods and Pokédex passed", flush=True)


if __name__ == "__main__":
    main()
