"""Build an edited map and check trainer win and loss speech in real battles."""

import argparse
from io import BytesIO
from pathlib import Path
import subprocess
import tarfile
from tempfile import TemporaryDirectory

from adventure_checkpoints import BROCK_DEFEATED_EVENT, PEWTER_CITY, PEWTER_GYM, check_gym, event, seed_water_party
from cartridge_smoke import Game


VIRIDIAN_CITY = 0x01
VIRIDIAN_FOREST = 0x33
CUSTOM_WIN = "CUSTOM WIN"
CUSTOM_LOSS = "CUSTOM LOSS"
DEFAULT_WIN = "DEFAULT WIN"
BLACKOUT = "blacked out"


def customize_trainers(source):
    script = source / "scripts/ViridianForest.asm"
    original = script.read_text()
    loss = "FixtureTrainerLossText"
    row = next(
        line for line in original.splitlines()
        if line.startswith("\ttrainer EVENT_BEAT_VIRIDIAN_FOREST_TRAINER_0,")
    )
    original = original.replace(row, f"{row}, {loss}", 1)
    for name, message in (
        ("ViridianForestYoungster2EndBattleText", CUSTOM_WIN),
        ("ViridianForestYoungster3EndBattleText", DEFAULT_WIN),
    ):
        old = f"{name}:\n\ttext_far _{name}\n\ttext_end"
        new = f'{name}:\n\ttext_start\n\tline "{message}"\n\tprompt'
        assert old in original
        original = original.replace(old, new, 1)
    script.write_text(original + f'\n{loss}:\n\ttext_start\n\tline "{CUSTOM_LOSS}"\n\tprompt\n')


def advance_battle(game, done):
    screens = []
    for _ in range(400):
        screens.append(game.visible_text())
        if done():
            return " ".join(" ".join(screens).split())
        game.press(4)
        game.tick(10)
    raise AssertionError(f"Battle did not reach the expected end.\n{game.visible_text()}")


def prepare_battle(game, victory, blackout_map):
    game.new_game()
    seed_water_party(game)
    game.put("wPartyCount", (1,))
    game.put("wPartySpecies", (0x69, 0xFF))
    game.put("wOptions", (0xC1,))
    game.put("wPlayerMoney", (0, 0x10, 0))
    game.put("wLastBlackoutMap", (blackout_map,))
    if not victory:
        game.put("wPartyMon1Moves", (0x96, 0, 0, 0))  # Splash
        game.put("wPartyMon1HP", (0, 1))
        game.put("wPartyMon1Speed", (0, 1))


def check_battle(library, boot, rom, *, custom, victory):
    with Game(library, boot, rom) as game:
        prepare_battle(game, victory, VIRIDIAN_CITY)
        trainer_y = 33 if custom else 19
        trainer_event = 0x562 if custom else 0x563

        # Enter each trainer's line of sight through the normal map loop.
        game.enter_map(VIRIDIAN_FOREST, 17, 29, trainer_y)
        advance_battle(game, lambda: game.get("wIsInBattle") == 2 and "FIGHT" in game.visible_text())
        assert bool(game.get("wEndBattleLoseTextPointer") & 0x80) == custom

        if victory:
            text = advance_battle(
                game,
                lambda: game.get("wIsInBattle") == 0
                and event(game, trainer_event)
                and game.get("wViridianForestCurScript") == 0,
            )
            assert (CUSTOM_WIN if custom else DEFAULT_WIN) in text
            assert CUSTOM_LOSS not in text and BLACKOUT not in text
            assert game.get_bytes("wPlayerMoney", 3) > bytes((0, 0x10, 0))
            assert game.get("wCurMap") == VIRIDIAN_FOREST
        else:
            text = advance_battle(
                game,
                lambda: game.get("wCurMap") == VIRIDIAN_CITY and game.get("wIsInBattle") == 0,
            )
            assert (CUSTOM_LOSS in text) == custom
            assert BLACKOUT in text and CUSTOM_WIN not in text and DEFAULT_WIN not in text
            if custom:
                assert text.index(CUSTOM_LOSS) < text.index(BLACKOUT)
            assert not event(game, trainer_event)
            assert game.get_bytes("wPlayerMoney", 3) == bytes((0, 0x05, 0))
            assert game.get_bytes("wPartyMon1HP", 2) == bytes((0, 160))
        print(f"{'six' if custom else 'five'} arguments, {'win' if victory else 'loss'} passed", flush=True)


def check_manually_assigned_speech(library, boot, rom):
    check_gym(library, boot, rom)
    with Game(library, boot, rom) as game:
        prepare_battle(game, False, PEWTER_CITY)
        game.enter_map(PEWTER_GYM, 5, 4, 2, last_map=PEWTER_CITY)
        game.press(2)  # Face Brock.
        game.press(4)
        advance_battle(game, lambda: game.get("wIsInBattle") == 2 and "FIGHT" in game.visible_text())
        assert not game.get("wEndBattleLoseTextPointer") & 0x80
        text = advance_battle(
            game,
            lambda: game.get("wCurMap") == PEWTER_CITY and game.get("wIsInBattle") == 0,
        )
        assert BLACKOUT in text and "BOULDERBADGE" not in text
        assert not event(game, BROCK_DEFEATED_EVENT)
        assert game.get("wObtainedBadges") == 0
        assert game.get_bytes("wPlayerMoney", 3) == bytes((0, 0x05, 0))
    print("Manually assigned speech on Brock's win and loss passed", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--rgbds", type=Path, help="Directory with the RGBDS 1.0.4 tools.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    archive = subprocess.check_output(["git", "archive", "HEAD"], cwd=root)
    with TemporaryDirectory(prefix="pokergb-trainer-loss-") as directory:
        source = Path(directory)
        with tarfile.open(fileobj=BytesIO(archive)) as files:
            files.extractall(source, filter="data")
        customize_trainers(source)
        command = ["make", "-j4", "red"]
        if args.rgbds:
            command.append(f"RGBDS={args.rgbds.resolve()}/")
        build = subprocess.run(command, cwd=source, capture_output=True, text=True)
        if build.returncode:
            raise SystemExit(build.stdout + build.stderr)
        rom = source / "build/core/pokered.gbc"
        fixture = (args.sameboy.resolve(), args.boot.resolve(), rom)
        for custom in (False, True):
            for victory in (False, True):
                check_battle(*fixture, custom=custom, victory=victory)
        check_manually_assigned_speech(*fixture)


if __name__ == "__main__":
    main()
