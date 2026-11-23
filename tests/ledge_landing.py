"""Check ledge jumps through a real route and the NPC movement routine."""

import argparse
from pathlib import Path

from cartridge_smoke import Game


ROUTE_1 = 0x0C
LEFT, DOWN = 1, 3
LEDGE_OR_FISHING = 0x40
SCRIPTED_MOVEMENT = 0x80
STAY, WALK = 0xFF, 0xFE
JUMP_X, JUMP_Y = 5, 4


def enter_route(game):
    game.new_game()
    game.put("wStatusFlags4", (game.get("wStatusFlags4") | 0x10,))
    game.enter_map(ROUTE_1, 10, JUMP_X, JUMP_Y)


def place_route_npc(game, x, y):
    game.put("wSprite01StateData2MapY", (y + 4, x + 4))
    screen_y = 60 + 16 * (y - JUMP_Y)
    screen_x = 64 + 16 * (x - JUMP_X)
    game.put("wSprite01StateData1YPixels", (screen_y, 0, screen_x))
    game.put("wSprite01StateData2MovementByte1", (STAY,))
    game.put("wSprite01StateData2MovementDelay", (255,))
    game.put("wSprite01StateData1MovementStatus", (2, 0, 0))
    game.tick(6)


def set_key(game, key, held):
    game.core.GB_set_key_state(game.gb, key, held)


def in_jump(game):
    return bool(game.get("wMovementFlags") & LEDGE_OR_FISHING)


def start_jump(game):
    set_key(game, DOWN, True)
    game.wait(lambda: in_jump(game))
    set_key(game, DOWN, False)


def check_jump_landing(library, boot, rom):
    with Game(library, boot, rom) as game:
        enter_route(game)
        place_route_npc(game, JUMP_X, JUMP_Y + 2)
        set_key(game, DOWN, True)
        game.tick(64)
        set_key(game, DOWN, False)
        assert game.get("wYCoord") == JUMP_Y
        assert not in_jump(game)
        assert game.get("wJoyIgnore") == 0

        place_route_npc(game, JUMP_X + 1, JUMP_Y + 2)
        start_jump(game)
        game.wait(lambda: not in_jump(game) and not game.get("wWalkCounter"))
        assert game.get("wYCoord") == JUMP_Y + 2
        assert game.get("wJoyIgnore") == 0
        set_key(game, LEFT, True)
        game.wait(lambda: game.get("wXCoord") == JUMP_X - 1 and not game.get("wWalkCounter"))
        set_key(game, LEFT, False)


def check_incoming_npc(library, boot, rom):
    with Game(library, boot, rom) as game:
        enter_route(game)
        place_route_npc(game, JUMP_X + 1, JUMP_Y + 2)
        # TryWalking sets the next map coordinate before the sprite reaches it.
        game.put("wSprite01StateData2MapX", (JUMP_X + 4,))
        game.put("wSprite01StateData2WalkAnimationCounter", (13,))
        game.put("wSprite01StateData1MovementStatus", (3,))
        game.put("wSprite01StateData1XStepVector", (255,))
        game.put("wSpritePlayerStateData1FacingDirection", (0,))
        game.put("hJoyHeld", (0x80,))  # Down
        game.invoke("HandleLedges")
        game.return_to_stub()
        assert not in_jump(game)
        assert game.get("wJoyIgnore") == 0


def check_landing_reserved(library, boot, rom):
    with Game(library, boot, rom) as game:
        enter_route(game)
        place_route_npc(game, JUMP_X + 1, JUMP_Y + 2)
        start_jump(game)
        assert game.get("wLedgeLandingY") == JUMP_Y + 2 + 4
        assert game.get("wLedgeLandingX") == JUMP_X + 4

        def npc_tries_left():
            game.put("hCurrentSpriteOffset", (0x10,))
            game.put("wSprite01StateData2MovementByte1", (WALK,))
            game.put("wSprite01StateData1XStepVector", (255,))
            game.invoke("CanWalkOntoTile")
            game.cpu.bc = 0x022C  # Left, into a passable path tile.
            game.cpu.de = 0x00FF
            game.return_to_stub()
            return not bool(game.cpu.af & 0x10)

        assert not npc_tries_left()
        game.put("wMovementFlags", (game.get("wMovementFlags") & ~LEDGE_OR_FISHING,))
        game.put("wStatusFlags5", (game.get("wStatusFlags5") & ~SCRIPTED_MOVEMENT,))
        assert npc_tries_left()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        fixture = (args.sameboy, args.boot, rom)
        check_jump_landing(*fixture)
        check_incoming_npc(*fixture)
        check_landing_reserved(*fixture)
        print(f"Ledge landing tests passed on {color.title()}.")


if __name__ == "__main__":
    main()
