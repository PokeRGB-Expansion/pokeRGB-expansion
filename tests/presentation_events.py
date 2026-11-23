"""Check the Pewter guide, hidden-item sound, and Route 15 binoculars."""

import argparse
from pathlib import Path

from cartridge_smoke import Game

ARTICUNO = 0x4a
ARTICUNO_CRY = (0x80, 0x40)
AUDIO_VOLUME = 0xff24
POTION = 0x14
PICKUP_JINGLE = 0x89


def check_guide(game):
    # Start after the guide has brought the player to the Gym.
    game.enter_map(0x02, 20, 11, 18)
    game.put("wNPCMovementScriptPointerTableNum", (0,))
    game.invoke("PewterCityYoungsterShowsPlayerGymScript")
    game.wait(lambda: game.cpu.pc == 0xc900, accept=True)
    assert game.get("wSprite05StateData1XPixels") == 0x50
    assert game.get("wSprite05StateData1YPixels") == 0x3c
    assert game.get("wSprite05StateData2MapX") == 16
    assert game.get("wSprite05StateData2MapY") == 22


def read_hidden_potion(game):
    game.put("wHiddenEventX", (1,))
    game.put("wHiddenEventY", (18,))
    game.put("wHiddenEventFunctionArgument", (POTION,))
    game.invoke("HiddenItems")


def check_hidden_item(game, fading):
    game.enter_map(0x33, 17, 1, 19)
    game.put("wNumBagItems", (0, 0xff))
    if fading:
        game.put("wAudioFadeOutControl", (0x21,))
        game.put("wAudioFadeOutCounter", (250,))
        game.put("wAudioFadeOutCounterReloadValue", (250,))
        game.write(AUDIO_VOLUME, (0x44,))
    read_hidden_potion(game)
    game.wait(lambda: game.get("wChannelSoundIDs", 4) == PICKUP_JINGLE)
    assert game.get("wAudioFadeOutControl") == 0
    game.return_to_stub()
    assert game.get("wChannelSoundIDs", 4) == 0
    assert game.get("wAudioFadeOutControl") == (0x21 if fading else 0)
    if fading:
        assert 0 < game.get("wAudioFadeOutCounter") < 250
        assert game.core.GB_safe_read_memory(game.gb, AUDIO_VOLUME) == 0x44

    read_hidden_potion(game)
    game.return_to_stub()
    assert game.get_bytes("wNumBagItems", 4) == bytes((1, POTION, 1, 0xff))


def play_cry(game, species):
    game.invoke("PlayCry")
    game.cpu.af = species << 8
    game.return_to_stub()


def cry_parameters(game):
    return game.get("wFrequencyModifier"), game.get("wTempoModifier")


def check_binoculars(game):
    game.enter_map(0xb9, 4, 1, 3)
    for previous in (0x07, 0x1b):
        play_cry(game, previous)
        assert cry_parameters(game) != ARTICUNO_CRY
        game.put("wSpritePlayerStateData1FacingDirection", (4,))
        game.invoke("Route15GateLeftBinoculars")
        game.wait(lambda: game.get("wCurSpecies") == ARTICUNO
                  and cry_parameters(game) == ARTICUNO_CRY, accept=True)
        game.wait(lambda: game.cpu.pc == 0xc900, accept=True)


def check_fossils(game):
    game.enter_map(0x34, 10, 1, 2)
    for event in ("AerodactylFossil", "KabutopsFossil"):
        play_cry(game, 0x07)
        previous = cry_parameters(game)
        game.invoke(event)
        game.wait(lambda: game.cpu.pc == 0xc900, accept=True)
        assert cry_parameters(game) == previous


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        for check in (check_guide, check_binoculars, check_fossils):
            with Game(args.sameboy, args.boot, rom) as game:
                game.new_game()
                check(game)
        for fading in (False, True):
            with Game(args.sameboy, args.boot, rom) as game:
                game.new_game()
                check_hidden_item(game, fading)
        print(f"{args.directory.name} {color}: guide, item sound, and binoculars passed", flush=True)


if __name__ == "__main__":
    main()
