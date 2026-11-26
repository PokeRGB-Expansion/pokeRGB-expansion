"""Check party and box move cards and the three wild-battle escape descriptions."""

import argparse
from pathlib import Path

from adventure_checkpoints import advance_text_until
from battle_pace import restore, snapshot
from battle_stats_return import battle_ready, start_battle
from cartridge_smoke import Game, seed_party
from cgb_compatibility import display_pixels, start_menu_row
from fight_info_browsing import open_fight
from move_info_authoring import shows
from move_swap_smoke import A, B, DOWN, UP, SELECT, START, CURSOR
from pc_browsing import box_name, open_action, open_bill, rosters, stock_pc, view_stats, wait_list
from shift_prompt import VIRIDIAN_FOREST
from title_smoke import SGB_HEIGHT, SGB_MODEL, SGB_WIDTH
from tm_inspection_controls import game_screen, write_gallery
from tm_party_info import press

RIGHT = 0
MOVES = (0x21, 0x27, 0x62, 0)  # Tackle, Tail Whip, Quick Attack
PP = (12, 0x41, 0x87, 0)
ESCAPES = (
    (0x2E, "ROAR", "Scares away a", "ran away scared", "is unaffected"),
    (0x12, "WHIRLWIND", "Blows away a wild", "was blown away", "is unaffected"),
    (0x64, "TELEPORT", "User flees from a", "ran from battle", "failed"),
)


def check_stats(game, *, boxed, sgb, gallery=None):
    pixels = display_pixels(game, SGB_WIDTH, SGB_HEIGHT) if sgb else display_pixels(game)
    game.new_game()
    stock_pc(game)
    game.put("wOptions", (0xC1,))
    mon = "wBoxMon2" if boxed else "wPartyMon2"
    game.put(mon + "Moves", MOVES)
    game.put(mon + "PP", PP)
    name = box_name(1) if boxed else "PARTYB"
    before = rosters(game)
    if boxed:
        open_bill(game)
        game.press(A)
        wait_list(game, (0, 0), box_name(0))
        press(game, DOWN)
        wait_list(game, (0, 1), name)
        open_action(game, "WITHDRAW")
        view_stats(game, name)
    else:
        start_menu_row(game, 0)
        shows(game, "PARTYA", name, "SELECT to switch")
        game.tick(45)
        press(game, DOWN)
        game.wait(lambda: game.get("wCurrentMenuItem") == 1)
        press(game, A)
        shows(game, "STATS", "SWITCH")
        game.tick(25)
        press(game, A)
        shows(game, "D PAD NAV", name, "ATTACK")
        game.tick(90)
    press(game, RIGHT)
    shows(game, "START INFO", "TACKLE", "12 35")
    game.tick(40)
    original = game_screen(pixels, sgb)
    tiles = game.get_bytes("wTileMap", 360)
    saved_data = bytes(game.battery()[360:])
    press(game, START)
    shows(game, name, "KNOWN MOVES", "UP DOWN MOVE", "1 3", "SEL EFFECT", "B BACK")
    assert "START INFO" not in game.visible_text()
    press(game, SELECT)
    press(game, DOWN)
    shows(game, "SEL STATS", "Defense 1 stage", "2 3")
    assert game.get("wTileMap", 4 * 20 + 1) == CURSOR
    assert "12 35" not in game.visible_text()
    game.tick(15)
    effect = game_screen(pixels, sgb)
    press(game, SELECT)
    shows(game, "PP  1 36", "BASE 30")
    press(game, DOWN)
    press(game, DOWN)
    shows(game, "QUICK ATTACK", "3 3", "PP  7 42")
    press(game, UP)
    shows(game, "PP  1 36", "2 3")
    press(game, B)
    shows(game, "START INFO", "TACKLE")
    game.tick(30)
    assert game.get_bytes("wTileMap", 360) == tiles
    assert game_screen(pixels, sgb) == original
    assert bytes(game.battery()[360:]) == saved_data
    assert game.get("wWhichPokemon") == 1
    assert rosters(game) == before
    if gallery:
        write_gallery(gallery, [original, effect], scale=3)
    press(game, B)
    if boxed:
        wait_list(game, (0, 1), name)
    else:
        shows(game, name, "PARTYA")


def check_escape(game, *, trainer):
    if trainer:
        game.new_game()
        seed_party(game)
        game.put("wOptions", (0xC1,))
        game.enter_map(VIRIDIAN_FOREST, 17, 29, 33)
        advance_text_until(game, lambda: battle_ready(game))
    else:
        start_battle(game, tower=False, scoped=False)
    open_fight(game, tuple(move[0] for move in ESCAPES) + (0,), (20, 20, 20, 0))
    game.put("wPlayerBattleStatus2", (game.get("wPlayerBattleStatus2") | 1,))  # X Accuracy
    saved = snapshot(game)
    for index, (_, name, description, wild_result, trainer_result) in enumerate(ESCAPES):
        restore(game, saved)
        for _ in range(index):
            press(game, DOWN)
        press(game, START)
        press(game, SELECT)
        shows(game, name, description)
        press(game, B)
        press(game, A)
        result = trainer_result if trainer else wild_result
        advance_text_until(game, lambda: result in game.visible_text())
        if trainer:
            advance_text_until(game, lambda: battle_ready(game))
        else:
            actor = "TEST" if name == "TELEPORT" else "Enemy PIDGEY"
            assert actor in game.visible_text(), game.visible_text()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", required=True, type=Path)
    parser.add_argument("--boot", required=True, type=Path)
    parser.add_argument("--sgb-boot", required=True, type=Path)
    parser.add_argument("--gallery", type=Path)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        sgb = color == "blue"
        model = {"model": SGB_MODEL} if sgb else {}
        boot = args.sgb_boot if sgb else args.boot
        for boxed in (False, True):
            with Game(args.sameboy, boot, rom, **model) as game:
                gallery = args.gallery if color == "green" and not boxed else None
                check_stats(game, boxed=boxed, sgb=sgb, gallery=gallery)
    for trainer in (False, True):
        with Game(args.sameboy, args.boot, rom) as game:
            check_escape(game, trainer=trainer)
    print(f"{args.directory.name}: party and box STATS, Roar, Whirlwind and Teleport passed.")


if __name__ == "__main__":
    main()
