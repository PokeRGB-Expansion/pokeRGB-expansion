"""Play the Kanto starter choices and the optional Route 3 trainer tutorial."""

import argparse
from pathlib import Path

from adventure_checkpoints import advance_text_until, seed_water_party, set_event, walk_to, A, DOWN, LEFT, UP, OAKS_LAB
from battle_stats_return import battle_ready
from cartridge_smoke import Game
from pokedex_area import linked_offset


def check_lab(library, boot, rom, *, custom_second=False):
    image = rom.read_bytes()
    for slot in range(3):
        with Game(library, boot, rom) as game:
            ball = linked_offset(game, "OaksLabStarterBalls") + 4 * slot
            chosen, _, rival, _ = image[ball:ball + 4]
            name_at = linked_offset(game, "MonsterNames") + 10 * (chosen - 1)
            name = image[name_at:name_at + 10].split(b"\x50")[0]
            game.new_game()
            game.put("wOptions", (0xc1,))
            set_event(game, 0x20)  # Followed Oak into the lab.
            set_event(game, 0x21)  # Oak has asked the player to choose.
            game.put("wOaksLabCurScript", (6,))
            x = 6 + slot
            game.enter_map(OAKS_LAB, 5, x, 4)
            game.press(UP)
            game.tick(16)
            game.press(A)
            game.wait(lambda: name in game.get_bytes("wTileMap", 360) and game.get("wTileMap", 8 * 20 + 16) >= 0xf6)
            game.tick(30)
            assert any(game.get_bytes("wTileMap", 360)[11 * 20 + col] != 0x7f for col in range(1, 19)), "Missing Pokédex description"
            advance_text_until(game, lambda: "YES" in game.visible_text() and "NO" in game.visible_text())
            assert name in game.get_bytes("wTileMap", 360)[13 * 20:], "Oak's offer names the wrong starter"
            if custom_second and slot == 1:
                assert "partner" in game.visible_text(), "The custom offer did not appear"
            elif chosen in (0xb0, 0xb1, 0x99):
                adjective = {0xb0: "fire", 0xb1: "water", 0x99: "plant"}[chosen]
                assert adjective in game.visible_text(), "Oak's original offer changed"
            game.press(A)
            advance_text_until(game, lambda: "YES" in game.visible_text() and "nickname" in game.visible_text())
            game.press(DOWN)
            game.tick(12)
            game.press(A)
            advance_text_until(game, lambda: game.get("wOaksLabCurScript") == 10)
            assert game.get_bytes("wPartySpecies", 2) == bytes((chosen, 0xff))
            assert game.get("wPlayerStarter") == chosen and game.get("wRivalStarter") == rival
            game.tick(16)
            walk_to(game, DOWN, x, 5)
            walk_to(game, LEFT, 5, 5)
            walk_to(game, DOWN, 5, 6)
            advance_text_until(game, lambda: battle_ready(game))
            team = game.get_bytes("wEnemyPartySpecies", game.get("wEnemyPartyCount"))
            assert rival in team and game.get("wEnemyMonSpecies") == team[0], "The rival did not bring his starter to the battle"
        print(f"{rom.name}, ball {slot + 1}: full preview, offer, gift and rival battle passed", flush=True)


def check_route3_example(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_water_party(game)
        game.put("wOptions", (0xc1,))
        game.enter_map(0x0e, 35, 14, 5)  # Step into the Youngster's sight line.
        advance_text_until(game, lambda: battle_ready(game))
        assert game.get("wTrainerClass") == 1 and game.get("wTrainerNo") == 1
        assert (game.get("wEnemyMonSpecies"), game.get("wEnemyMonLevel")) == (0xa5, 11)
        assert game.get_bytes("wEnemyMonMoves", 4) == bytes((0x62, 0x27, 0, 0)), "Expected the tutorial Rattata's Quick Attack and Tail Whip"
        assert game.get_bytes("wEnemyMonPP", 4) == bytes((30, 30, 0, 0))
        print(f"{rom.name}: the Route 3 Youngster's Rattata entered battle with Quick Attack and Tail Whip at 30 PP each", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--route3-example", action="store_true", help="Also play the published Route 3 Youngster example.")
    args = parser.parse_args()
    check_lab(args.sameboy, args.boot, args.rom)
    if args.route3_example:
        check_route3_example(args.sameboy, args.boot, args.rom)
