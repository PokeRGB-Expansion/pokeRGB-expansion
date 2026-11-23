"""Check that battle PARTY to STATS preserves both active pictures."""

import argparse
from pathlib import Path

from acid_armor import BATTLE_PICTURE_TILES, actor_tiles, invoke_visual, prepare_picture
from adventure_checkpoints import advance_text_until
from cartridge_smoke import Game, seed_party
from protected_mechanics import ENEMY, PLAYER


RIGHT, DOWN, A, B = 0, 3, 4, 5
GASTLY, PIDGEY, SILPH_SCOPE = 0x19, 0x24, 0x48
ROUTE_1, POKEMON_TOWER_3F = 0x0C, 0x90


def shows(game, *words):
    return all(word in game.visible_text() for word in words)


def battle_ready(game):
    return shows(game, "FIGHT", "RUN") and game.get("wTopMenuItemY") == 14


def start_battle(game, *, tower, scoped):
    game.new_game()
    seed_party(game)
    game.put("wOptions", (0xC1,))
    if scoped:
        game.put("wNumBagItems", (1, SILPH_SCOPE, 1, 0xFF))
    if tower:
        game.enter_map(POKEMON_TOWER_3F, 10, 5, 4)
    else:
        game.enter_map(ROUTE_1, 10, 5, 4)
    game.put("wCurOpponent", (GASTLY if tower else PIDGEY,))
    game.put("wCurEnemyLevel", (5,))
    advance_text_until(game, lambda: battle_ready(game))
    if tower:
        assert ("GASTLY" if scoped else "GHOST") in game.visible_text()


def snapshot(game):
    return tuple(
        (actor_tiles(game, actor), game.get_bytes(label, BATTLE_PICTURE_TILES * 16))
        for actor, label in ((PLAYER, "vBackPic"), (ENEMY, "vFrontPic"))
    )


def open_stats_and_return(game):
    game.press(RIGHT)
    game.wait(lambda: game.get("wTopMenuItemX") == 15)
    game.tick(12)
    game.press(A)
    game.wait(lambda: game.visible_text().count("160 160") == 2
              and game.get("wMaxMenuItem") == 1)
    game.tick(16)
    if game.get("wCurrentMenuItem") != 1:
        game.press(DOWN)
    assert game.get("wCurrentMenuItem") == 1, game.visible_text()
    game.press(A)
    game.wait(lambda: shows(game, "SWITCH", "STATS"))
    game.tick(12)
    game.press(DOWN)
    game.press(A)
    game.wait(lambda: "ATTACK" in game.visible_text())
    assert game.get("wWhichPokemon") == 1
    # The first page plays the selected Pokémon's cry before taking input.
    game.tick(110)
    game.press(B)
    game.wait(lambda: game.visible_text().count("160 160") == 2)
    game.tick(12)
    assert game.get("wCurrentMenuItem") == 1
    game.press(B)
    game.wait(lambda: battle_ready(game))


def check_pictures(library, boot, rom, player, enemy, *, tower=False, scoped=False, last_actor=PLAYER):
    with Game(library, boot, rom) as game:
        start_battle(game, tower=tower, scoped=scoped)
        for actor, form in ((PLAYER, player), (ENEMY, enemy)):
            if not form:
                continue
            game.put("hWhoseTurn", (actor == ENEMY,))
            prepare_picture(game, actor, form)
        if player or enemy:
            stop = invoke_visual(game, "SaveScreenTilesToBuffer1")
            game.wait(lambda: game.cpu.pc == stop)
            game.put("wBattleAndStartSavedMenuItem", (0,))
            invoke_visual(game, "MainInBattleLoop")
            game.wait(lambda: battle_ready(game))

        game.tick(30)
        game.press(A)
        game.wait(lambda: "SPLASH" in game.visible_text())
        game.tick(15)
        game.press(B)
        game.wait(lambda: battle_ready(game))
        assert game.get("hWhoseTurn") == 0
        game.put("hWhoseTurn", (last_actor == ENEMY,))
        before = snapshot(game)
        assert all(len(set(graphics)) > 1 for _, graphics in before)
        identity = game.get_bytes("wEnemyMonNick", 11)
        health = game.get_bytes("wBattleMonHP", 2), game.get_bytes("wEnemyMonHP", 2)
        form_fields = (
            "wPlayerBattleStatus2", "wEnemyBattleStatus2",
            "wPlayerMonMinimized", "wEnemyMonMinimized",
            "wPlayerBattleStatus3", "wEnemyBattleStatus3",
        )
        forms = tuple(game.get(field) for field in form_fields)

        open_stats_and_return(game)
        assert snapshot(game) == before, (player, enemy, tower, scoped, last_actor)
        assert game.get("hWhoseTurn") == int(last_actor == ENEMY)
        assert game.get_bytes("wEnemyMonNick", 11) == identity
        assert health == (game.get_bytes("wBattleMonHP", 2), game.get_bytes("wEnemyMonHP", 2))
        assert forms == tuple(game.get(field) for field in form_fields)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        fixture = args.sameboy, args.boot, rom
        check_pictures(*fixture, "substitute", "substitute")
        check_pictures(*fixture, "substitute", "minimized", last_actor=ENEMY)
        check_pictures(*fixture, "transformed", "minimized")
        check_pictures(*fixture, "minimized", None, tower=True)
        check_pictures(*fixture, None, None, tower=True, scoped=True)
        print(f"{color.title()}: battle STATS pictures passed", flush=True)


if __name__ == "__main__":
    main()
