"""Check Mansion trainer sight through the ordinary overworld and battle loop."""

import argparse
from pathlib import Path
from typing import NamedTuple

from adventure_checkpoints import event, hold_until, seed_water_party, set_event, walk_to
from cartridge_smoke import Game
from trainer_loss_authoring import advance_battle


RIGHT, LEFT, UP, DOWN, A, B = range(6)
FACE_LEFT, FACE_RIGHT = 8, 12
CINNABAR_ISLAND, ROUTE_21 = 0x08, 0x20
MANSION_1F, MANSION_2F, MANSION_3F, MANSION_B1F = 0xA5, 0xD6, 0xD7, 0xD8
BURGLAR, SCIENTIST = 0x0B, 0x1C
SEEN_BY_TRAINER = 1


class Trainer(NamedTuple):
    map: int
    player: tuple[int, int]
    sprite: tuple[int, int]
    facing: int
    defeat_event: int
    trainer_class: int
    party: int
    level: int
    species: tuple[int, ...]


BURGLARS = (
    Trainer(MANSION_2F, (4, 17), (3, 17), FACE_RIGHT, 0x801, BURGLAR, 7, 34, (0xB0, 0xB2)),
    Trainer(MANSION_3F, (4, 11), (5, 11), FACE_LEFT, 0x811, BURGLAR, 8, 38, (0x53,)),
    Trainer(MANSION_B1F, (17, 23), (16, 23), FACE_RIGHT, 0x821, BURGLAR, 9, 34, (0x21, 0xA3)),
)
SCIENTIST_1F = Trainer(
    MANSION_1F, (15, 17), (17, 17), FACE_LEFT, 0x289, SCIENTIST, 4, 29, (0x8D, 0x8F)
)


def turn_on_trainer(game, number):
    offset, bit = divmod(number, 8)
    address = game.addresses["wEventFlags"][1] + offset
    game.write(address, (game.get("wEventFlags", offset) & ~(1 << bit),))


def sprite_position(game):
    return (game.get("wSprite01StateData2MapX") - 4, game.get("wSprite01StateData2MapY") - 4)


def prepare_scene(game, trainer, *, player=None):
    game.new_game()
    seed_water_party(game)
    game.put("wPartyMon1Exp", (45 ** 3).to_bytes(3, "big"))
    if trainer.map == MANSION_3F:
        # Win on the first turn even when Ninetales chooses Quick Attack.
        game.put("wPartyMon1Moves", (0x62, 0, 0, 0))
        game.put("wPartyMon1PP", (30, 0, 0, 0))
        game.put("wPartyMon1Attack", (999).to_bytes(2, "big"))
    game.put("wPlayerMoney", (0, 0x10, 0))
    game.put("wOptions", (0xC1,))  # Set style, fast text, and no battle animations.
    # Let the map load without starting the fight during the fixture's setup.
    set_event(game, trainer.defeat_event)
    game.enter_map(trainer.map, 15, *(player or trainer.player), last_map=CINNABAR_ISLAND)


def show_facing(game, trainer, facing):
    # Use the trainer's authored position in a resting walking frame.
    x, y = trainer.sprite
    game.put("wSprite01StateData2MapX", (x + 4,))
    game.put("wSprite01StateData2MapY", (y + 4,))
    game.put("wSprite01StateData1XPixels", (0x40 + 16 * (x - game.get("wXCoord")),))
    game.put("wSprite01StateData1YPixels", (0x3C + 16 * (y - game.get("wYCoord")),))
    game.put("wSprite01StateData1MovementStatus", (2,))
    game.put("wSprite01StateData2MovementDelay", (255,))
    game.put("wSprite01StateData1FacingDirection", (facing,))


def wait_no_sight(game):
    game.tick(35)
    assert game.get("wIsInBattle") == 0
    assert not game.get("wMiscFlags") & SEEN_BY_TRAINER
    assert game.get("wCurMapScript") == 0


def wait_battle(game, trainer):
    advance_battle(game, lambda: game.get("wIsInBattle") == 2
                   and "FIGHT" in game.visible_text())
    assert game.get("wTrainerClass") == trainer.trainer_class
    assert game.get("wTrainerNo") == trainer.party
    assert game.get("wEnemyMonLevel") == trainer.level
    assert game.get("wEnemyPartyCount") == len(trainer.species)
    assert game.get_bytes("wEnemyPartySpecies", len(trainer.species) + 1) == (
        bytes(trainer.species) + b"\xFF"
    )


def finish_mansion_3f(game, trainer):
    advance_battle(game, lambda: game.get("wIsInBattle") == 0
                   and event(game, trainer.defeat_event)
                   and game.get("wPokemonMansion3FCurScript") == 0)
    assert (game.get("wXCoord"), game.get("wYCoord")) == trainer.player
    assert game.get_bytes("wPlayerMoney", 3) == bytes((0, 0x44, 0x20))
    show_facing(game, trainer, trainer.facing)
    wait_no_sight(game)
    game.put("wSpritePlayerStateData1FacingDirection", (trainer.facing ^ 4,))
    game.press(A)
    game.wait(lambda: "my partner went" in game.visible_text())
    for _ in range(25):
        if not game.get("wFontLoaded") & 1:
            break
        game.press(B)
        game.tick(8)
    assert not game.get("wFontLoaded") & 1
    assert game.get_bytes("wPlayerMoney", 3) == bytes((0, 0x44, 0x20))
    # Leave the table area by the normal 3F staircase.
    game.put("wGrassRate", (0,))
    walk_to(game, UP, 4, 10)
    hold_until(game, RIGHT, lambda: game.get("wCurMap") == MANSION_2F)
    game.tick(70)
    game.invoke("SaveGameData")
    game.return_to_stub()
    turn_on_trainer(game, trainer.defeat_event)
    game.invoke("TryLoadSaveFile")
    game.return_to_stub()
    assert game.get("wSaveFileStatus") == 2 and event(game, trainer.defeat_event)


def burglar_case(library, boot, rom, trainer, *, core):
    with Game(library, boot, rom) as game:
        prepare_scene(game, trainer)
        assert game.get("wSprite01StateData1ImageIndex") != 0xFF
        show_facing(game, trainer, trainer.facing ^ 4)
        turn_on_trainer(game, trainer.defeat_event)
        wait_no_sight(game)
        show_facing(game, trainer, trainer.facing)
        if core:
            game.wait(lambda: bool(game.get("wMiscFlags") & SEEN_BY_TRAINER))
        else:
            wait_no_sight(game)
            game.put("wSpritePlayerStateData1FacingDirection", (trainer.facing ^ 4,))
            game.press(A)
        wait_battle(game, trainer)
        if trainer.map == MANSION_3F:
            finish_mansion_3f(game, trainer)


def check_geometry(library, boot, rom):
    trainer = BURGLARS[0]
    for position in ((1, 17), (2, 16)):
        with Game(library, boot, rom) as game:
            prepare_scene(game, trainer, player=position)
            show_facing(game, trainer, FACE_LEFT)
            game.tick(6)
            assert game.get("wSprite01StateData1ImageIndex") != 0xFF
            turn_on_trainer(game, trainer.defeat_event)
            wait_no_sight(game)
    with Game(library, boot, rom) as game:
        prepare_scene(game, trainer, player=(4, 10))
        assert game.get("wSprite01StateData1ImageIndex") == 0xFF
        turn_on_trainer(game, trainer.defeat_event)
        wait_no_sight(game)

    for trainer in BURGLARS[:2]:
        with Game(library, boot, rom) as game:
            prepare_scene(game, trainer)
            assert game.get("wSprite01StateData2MovementByte1") == 0xFE  # WALK.
            game.wait(lambda: sprite_position(game)[0] != trainer.sprite[0])
            assert sprite_position(game)[1] == trainer.sprite[1]
            wait_no_sight(game)


def check_talk(library, boot, rom):
    trainer = BURGLARS[0]
    with Game(library, boot, rom) as game:
        prepare_scene(game, trainer)
        show_facing(game, trainer, FACE_LEFT)
        turn_on_trainer(game, trainer.defeat_event)
        wait_no_sight(game)
        game.put("wSpritePlayerStateData1FacingDirection", (FACE_LEFT,))
        game.press(A)
        wait_battle(game, trainer)


def check_scientist(library, boot, rom):
    with Game(library, boot, rom) as game:
        prepare_scene(game, SCIENTIST_1F)
        show_facing(game, SCIENTIST_1F, FACE_LEFT)
        turn_on_trainer(game, SCIENTIST_1F.defeat_event)
        game.wait(lambda: bool(game.get("wMiscFlags") & SEEN_BY_TRAINER))
        wait_battle(game, SCIENTIST_1F)
        assert sprite_position(game) == (16, 17)


def check_fisher(library, boot, rom):
    with Game(library, boot, rom) as game:
        game.new_game()
        seed_water_party(game)
        game.put("wWalkBikeSurfState", (2,))
        game.enter_map(ROUTE_21, 10, 3, 24)
        assert sprite_position(game) == (4, 24)
        assert game.get("wSprite01StateData1FacingDirection") == FACE_LEFT
        wait_no_sight(game)


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
        for trainer in BURGLARS:
            burglar_case(*fixture, trainer, core=core)
        check_geometry(*fixture)
        check_talk(*fixture)
        check_scientist(*fixture)
        check_fisher(*fixture)
        print(f"{args.directory.name} {color}: Mansion Burglar sight and trainer controls passed",
              flush=True)


if __name__ == "__main__":
    main()
