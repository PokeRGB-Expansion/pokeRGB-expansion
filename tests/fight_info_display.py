"""Check the rendered FIGHT comparison and its return to a battle, including a Tower ghost."""

import argparse
from pathlib import Path

from adventure_checkpoints import advance_text_until
from battle_stats_return import GASTLY, PIDGEY, POKEMON_TOWER_3F, ROUTE_1, battle_ready, snapshot
from cartridge_smoke import Game, seed_party
from cgb_compatibility import display_pixels
from move_info_authoring import shows
from move_swap_smoke import CURSOR, battle_row
from pc_browsing import name_bytes
from title_smoke import SGB_HEIGHT, SGB_MODEL, SGB_WIDTH
from tm_inspection_controls import game_screen, region, write_gallery
from tm_party_info import A, B, DOWN, SELECT, START, press

VAPOREON_MOVES = (0x62, 0x97, 0x3A, 0x2C)  # Quick Attack, Acid Armor, Ice Beam, Bite


def check(game, *, sgb, ghost, gallery=None):
    pixels = display_pixels(game, SGB_WIDTH, SGB_HEIGHT) if sgb else display_pixels(game)
    game.new_game()
    seed_party(game)
    game.put("wOptions", (0xC1,))
    game.put("wPartyMon1Nick", name_bytes("VAPOREON"))
    game.put("wPartyMon1Moves", VAPOREON_MOVES)
    game.put("wPartyMon1PP", (24, 20, 7, 21))
    game.put("wPartyMon1Exp", (0x01, 0x74, 0xF3))
    game.enter_map(POKEMON_TOWER_3F if ghost else ROUTE_1, 10, 5, 4)
    game.put("wCurOpponent", (GASTLY if ghost else PIDGEY,))
    game.put("wCurEnemyLevel", (5,))
    advance_text_until(game, lambda: battle_ready(game))
    game.tick(30)
    battlefield = game_screen(pixels, sgb)
    sprites = snapshot(game)
    press(game, A)
    shows(game, "START INFO", "QUICK ATTACK")
    press(game, START)
    shows(game, "QUICK ATTACK", "PRIORITY")
    press(game, SELECT)
    screens = []
    for row, name, effect in ((1, "QUICK ATTACK", "Goes before"), (2, "ACID ARMOR", "Raises Defense")):
        if row == 2:
            press(game, DOWN)
        shows(game, name, effect, "UP DOWN MOVE", "SEL STATS", "B BACK")
        game.tick(24)
        screen = game_screen(pixels, sgb)
        # Restore the player's name and battlefield above INFO, including the HP bar.
        assert region(screen, 0, 0, 160, 80) == region(battlefield, 0, 0, 160, 80)
        assert "START INFO" not in game.visible_text()
        assert game.get_bytes("wTileMap", 320)[316:319] == bytes((0xF6 + row, 0xF3, 0xFA))
        if ghost:
            assert "GHOST" in game.visible_text() and "GASTLY" not in game.visible_text()
        screens.append(screen)
    assert region(screens[0], 8, 88, 144, 32) != region(screens[1], 8, 88, 144, 32)
    if gallery:
        write_gallery(gallery, screens, scale=3)

    # B restores the last inspected row on press. Held B must stop here.
    game.core.GB_set_key_state(game.gb, B, True)
    game.tick(45)
    shows(game, "START INFO", "POISON", "20 40")
    assert game.get("wCurrentMenuItem") == 2
    assert battle_row(game, 2) == CURSOR and battle_row(game, 1) != CURSOR
    returned = game_screen(pixels, sgb)
    game.tick(35)
    assert game_screen(pixels, sgb) == returned
    game.core.GB_set_key_state(game.gb, B, False)
    game.tick(24)
    press(game, B)
    game.wait(lambda: battle_ready(game))
    game.tick(30)
    # This includes the numeric HP and EXP meter normally behind the INFO card.
    assert region(game_screen(pixels, sgb), 0, 0, 160, 96) == region(battlefield, 0, 0, 160, 96)
    assert snapshot(game) == sprites


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--sgb-boot", type=Path, required=True)
    parser.add_argument("--gallery", type=Path, help="Save two DMG effect pages from the same battle.")
    args = parser.parse_args()
    rom = args.directory / "pokegreen.gbc"
    for sgb, boot in ((False, args.boot), (True, args.sgb_boot)):
        for ghost in (False, True):
            with Game(args.sameboy, boot, rom, **({"model": SGB_MODEL} if sgb else {})) as game:
                check(game, sgb=sgb, ghost=ghost, gallery=args.gallery if not sgb and not ghost else None)
    print(f"{args.directory.name} Green: DMG/SGB FIGHT display, held B, Tower ghost and HUD return passed.")


if __name__ == "__main__":
    main()
