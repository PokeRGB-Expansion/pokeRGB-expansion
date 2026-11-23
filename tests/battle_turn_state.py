"""Check retreat text, Haze recovery, and the opponent's HUD after trainer items."""

import argparse
from pathlib import Path

from cartridge_smoke import Game

FROZEN = 1 << 5
ASLEEP = 2
POISONED = 1 << 3
LOCKED_MOVE = 0x73
RECHARGE = 1 << 5
RAGE = 1 << 6
HAZE = 0x72
TACKLE = 0x21


def set_number(game, label, value):
    game.put(label, value.to_bytes(2, "big"))


def check_retreat(game):
    game.put("wBattleMonNick", (0x93, 0x84, 0x92, 0x93, 0x50))
    for battle, cases in (
        (1, ((256, 259, "enough"), (261, 261, "enough"), (256, 255, "Come back"))),
        (2, ((256, 154, "OK"), (305, 75, "good"))),
    ):
        game.put("wIsInBattle", (battle,))
        for previous, current, text in cases:
            set_number(game, "wEnemyMonMaxHP", 320)
            set_number(game, "wLastSwitchInEnemyMonHP", previous)
            set_number(game, "wEnemyMonHP", current)
            # A previous calculation can leave a nonzero high byte.
            game.put("hMultiplicand", (0x34,))
            game.invoke("RetreatMon")
            game.wait(lambda: game.cpu.pc == 0xc900, accept=True)
            assert text in game.visible_text(), (previous, current, game.visible_text())
            assert game.get_bytes("wEnemyMonHP", 2) == current.to_bytes(2, "big")


def check_haze(game, core):
    game.put("wOptions", (0x81,))  # Battle animations off, fast text.
    game.put("wIsInBattle", (2,))
    for actor, target, target_status, user_status in (
        ("Player", "Enemy", "wEnemyMonStatus", "wBattleMonStatus"),
        ("Enemy", "Player", "wBattleMonStatus", "wEnemyMonStatus"),
    ):
        for condition in (FROZEN, ASLEEP, 0):
            game.put("hWhoseTurn", (actor == "Enemy",))
            game.put(f"w{actor}MoveNum", (HAZE,))
            game.put(f"w{actor}BattleStatus1", (1 << 5,))
            game.put(f"w{actor}BattleStatus2", (1 << 4,))
            game.put(f"w{target}SelectedMove", (TACKLE,))
            game.put(f"w{target}BattleStatus1", (LOCKED_MOVE,))
            game.put(f"w{target}BattleStatus2", (RECHARGE | RAGE,))
            game.put(target_status, (condition,))
            game.put(user_status, (POISONED,))
            game.invoke("HazeEffect_")
            game.wait(lambda: game.cpu.pc == 0xc900, accept=True)
            assert game.get(target_status) == 0
            assert game.get(user_status) == POISONED
            assert game.get(f"w{actor}BattleStatus1") == 1 << 5
            assert game.get(f"w{actor}BattleStatus2") == 1 << 4
            assert game.get(f"w{target}SelectedMove") == (0xff if condition else TACKLE)
            locks_end = core and condition
            assert game.get(f"w{target}BattleStatus1") == (0 if locks_end else LOCKED_MOVE)
            assert game.get(f"w{target}BattleStatus2") == (0 if locks_end else RECHARGE | RAGE)


def check_hud(game):
    game.put("wEnemyMonNick", (0x93, 0x84, 0x92, 0x93, 0x50))
    game.put("wEnemyMonLevel", (5,))
    game.put("wEnemyMonPartyPos", (0,))
    game.put("wTrainerName", (0x93, 0x84, 0x92, 0x93, 0x50))
    for effect, starting_hp, ending_hp, color in (
        ("AIUseFullHeal", 75, 75, 0),
        ("AIUseFullRestore", 35, 100, 0),
        ("AIUsePotion", 38, 58, 0),
    ):
        game.put("wAICount", (2,))
        game.put("wEnemyMonStatus", (POISONED,))
        game.put("wEnemyMon1Status", (POISONED,))
        game.put("wEnemyBattleStatus3", (1,))
        set_number(game, "wEnemyMonHP", starting_hp)
        set_number(game, "wEnemyMonMaxHP", 100)
        game.invoke("DrawEnemyHUDAndHPBar")
        game.return_to_stub()
        assert "PSN" in game.visible_text()
        game.invoke(effect)
        game.wait(lambda: game.cpu.pc == 0xc900, accept=True)
        cure = effect != "AIUsePotion"
        assert game.get("wEnemyMonStatus") == (0 if cure else POISONED)
        assert game.get("wEnemyMon1Status") == (0 if cure else POISONED)
        assert ("PSN" in game.visible_text()) != cure
        assert game.get_bytes("wEnemyMonHP", 2) == ending_hp.to_bytes(2, "big")
        assert game.get("wEnemyHPBarColor") == color, (effect, ending_hp, color)
        assert game.get("wAICount") == 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    args = parser.parse_args()
    for color in ("red", "blue", "green"):
        rom = args.directory / f"poke{color}.gbc"
        with Game(args.sameboy, args.boot, rom) as game:
            game.new_game()
            check_retreat(game)
            check_haze(game, args.directory.name == "core")
            check_hud(game)
        print(f"{args.directory.name} {color}: retreat text, Haze, and trainer item HUD passed", flush=True)


if __name__ == "__main__":
    main()
