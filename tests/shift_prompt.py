"""Defeat a trainer's first Pokémon and check SHIFT's reserve question."""

import argparse
from pathlib import Path

from adventure_checkpoints import seed_water_party
from cartridge_smoke import Game


A, B = 4, 5
VIRIDIAN_FOREST = 0x33
VAPOREON = 0x69
WEEDLE, CATERPIE = 0x70, 0x7B
ACTIVE_HP = 160


def seed_reserves(game, health):
    seed_water_party(game)
    length = game.addresses["wPartyMon2"][1] - game.addresses["wPartyMon1"][1]
    template = game.get_bytes("wPartyMon1", length)
    game.put("wPartyCount", (len(health),))
    game.put("wPartySpecies", (*([VAPOREON] * len(health)), 0xFF))
    for slot, hp in enumerate(health, 1):
        mon = f"wPartyMon{slot}"
        game.put(mon, template)
        game.put(mon + "HP", hp.to_bytes(2, "big"))
        game.put(mon + "Exp", (45 ** 3).to_bytes(3, "big"))
        game.put(mon + "PP", (15, 0, 0, 0))
        game.put(mon + "Nick", (0x93, 0x84, 0x92, 0x93, 0x50))


def advance(game, reached):
    screens = []
    offered_switch = False
    for _ in range(350):
        screen = game.visible_text()
        screens.append(screen)
        if reached():
            return " ".join(" ".join(screens).split()), offered_switch
        if "YES" in screen and "NO" in screen:
            offered_switch = True
            game.press(B)
        else:
            game.press(A)
        game.tick(8)
    raise AssertionError(f"The battle stopped before FIGHT.\n{game.visible_text()}")


def fight_is_ready(game, enemy):
    return (
        game.get("wEnemyMonSpecies") == enemy
        and game.get("wTopMenuItemY") == 14
        and "FIGHT" in game.visible_text()
        and "RUN" in game.visible_text()
    )


def check_shift(library, boot, rom, health, *, set_style=False):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_reserves(game, health)
        game.put("wOptions", (0xC1 if set_style else 0x81,))
        game.enter_map(VIRIDIAN_FOREST, 17, 29, 33)

        intro, asked_first = advance(game, lambda: fight_is_ready(game, WEEDLE))
        assert "sent out WEEDLE" in intro
        assert not asked_first and "about to use" not in intro
        active = health.index(ACTIVE_HP)
        assert game.get("wPlayerMonNumber") == active

        game.tick(15)
        game.press(A)
        game.wait(lambda: "SURF" in game.visible_text())
        game.tick(15)
        game.press(A)
        text, asked_next = advance(game, lambda: fight_is_ready(game, CATERPIE))
        assert "Enemy WEEDLE fainted" in text
        assert "sent out CATERPIE" in text
        expected = not set_style and any(
            hp for position, hp in enumerate(health) if position != active
        )
        assert asked_next == expected, (health, set_style, text)
        assert ("about to use" in text) == expected
        assert game.get("wPlayerMonNumber") == active
        assert game.get("wEnemyMonPartyPos") == 1
        assert game.get_bytes("wBattleMonHP", 2) == ACTIVE_HP.to_bytes(2, "big"), (
            health, set_style, game.get_bytes("wBattleMonHP", 2), text,
        )
        assert game.get("wBattleMonPP") == 14
        assert game.get("wPartyFoughtCurrentEnemyFlags") == 1 << active


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        fixture = args.sameboy, args.boot, rom
        for health in (
            (160,),
            (160, 0),
            (160, 1),
            (0, 0, 160, 0, 0, 0),
            (0, 0, 160, 0, 0, 1),
        ):
            check_shift(*fixture, health)
        check_shift(*fixture, (160, 1), set_style=True)
        print(f"{args.directory.name} {color}: SHIFT prompt passed", flush=True)


if __name__ == "__main__":
    main()
