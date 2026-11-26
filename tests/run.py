"""Run the game checks for a built Core or Minimal preset."""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import product
from pathlib import Path
import subprocess
import sys
from threading import Lock
from time import monotonic

COLORS = ("red", "blue", "green")
ROOT = Path(__file__).resolve().parents[1]
OUTPUT_LOCK = Lock()
# Other authoring checks build in their own temporary directories.
SHARED_BUILD_CHECK = "tests/battle_hud_options.py"

# Relative costs from the v0.4.2 Linux run. A new check uses the default cost
# until its timing warrants a separate weight. Filtered suites count per color.
CHECK_WEIGHTS = {
    "copied_trap_switch": 9, "field_sweep": 7, "field_menu_features": 7,
    "adventure_event_states": 6, "storage_counts": 6, "battle_fixes": 6,
    "protected_mechanics": 5, "shift_prompt": 5, "hp_and_level_one": 5,
    "safari_session": 5, "adventure_checkpoints": 4, "pp_restore_readout": 4,
    "bide_struggle": 4, "forest_encounters": 4, "battle_stats_return": 4,
    "cartridge_smoke": 4, "exp_all": 4, "presentation_events": 4,
    "celadon_roof_transactions": 4, "core_services": 4, "field_shortcuts": 4,
}


def shard_checks(checks, index, count):
    if count == 1:
        return checks
    groups = [[] for _ in range(min(count, len(checks)))]
    if index > len(groups):
        return []
    loads = [0] * len(groups)
    # Place the longest checks first. Adding a small check cannot shift a
    # series of long tests onto a single runner.
    for check in sorted(checks, key=check_weight, reverse=True):
        group = min(range(len(groups)), key=loads.__getitem__)
        groups[group].append(check)
        loads[group] += check_weight(check)
    return groups[index - 1]


def check_weight(check):
    script, _ = check
    return CHECK_WEIGHTS.get(Path(script).stem, 2)


def run_script(script, *args, grouped=False):
    label = script
    for flag in ("--color", "--room"):
        if flag in args:
            label += f" {args[args.index(flag) + 1]}"
    with OUTPUT_LOCK:
        print(f"Running {label}", flush=True)
    start = monotonic()
    result = subprocess.run(
        [sys.executable, "-B", ROOT / script, *args], cwd=ROOT,
        stdout=subprocess.PIPE if grouped else None,
        stderr=subprocess.STDOUT if grouped else None,
    )
    seconds = monotonic() - start
    with OUTPUT_LOCK:
        if result.stdout:
            sys.stdout.buffer.write(result.stdout)
            sys.stdout.buffer.flush()
        status = "Passed" if result.returncode == 0 else "Failed"
        print(f"{status} {label} in {seconds:.1f}s", flush=True)
    result.check_returncode()


def run_checks(checks, jobs):
    if jobs == 1:
        for script, arguments in checks:
            run_script(script, *arguments)
        return

    # The HUD check may run Make on the default ROM as well as its variants.
    for script, arguments in checks:
        if script == SHARED_BUILD_CHECK:
            run_script(script, *arguments)

    with ThreadPoolExecutor(max_workers=jobs) as workers:
        futures = [workers.submit(run_script, script, *arguments, grouped=True)
                   for script, arguments in checks if script != SHARED_BUILD_CHECK]
        try:
            for future in as_completed(futures):
                future.result()
        finally:
            for future in futures:
                future.cancel()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Build output directory for one preset.")
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True, help="SameBoy DMG boot file.")
    parser.add_argument("--sgb-boot", type=Path, required=True, help="SameBoy Super Game Boy boot file.")
    parser.add_argument("--cgb-boot", type=Path, help="SameBoy Color boot file. Defaults to cgb_boot.bin beside the DMG file.")
    parser.add_argument("--rgbds", type=Path, help="Directory with the RGBDS 1.0.4 tools.")
    parser.add_argument("--all-link-pairs", action="store_true", help="Check all nine Core color pairs.")
    parser.add_argument("--shard", type=int, nargs=2, metavar=("INDEX", "COUNT"), default=(1, 1),
                        help="Run one of COUNT disjoint groups, numbered from 1.")
    parser.add_argument("--jobs", type=int, default=1, help="Number of independent test scripts to run at once.")
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be at least 1.")
    index, count = args.shard
    if not 1 <= index <= count:
        parser.error("--shard requires 1 <= INDEX <= COUNT.")

    directory = args.directory.resolve()
    if directory.name not in ("core", "minimal"):
        parser.error("Use the build directory for Core or Minimal.")
    core = directory.name == "core"
    roms = [directory / f"poke{color}.gbc" for color in COLORS]
    if missing := [rom for rom in roms if not rom.is_file()]:
        parser.error(f"Build {', '.join(rom.name for rom in missing)} first.")
    sameboy = args.sameboy.resolve()
    boot = args.boot.resolve()
    sgb_boot = args.sgb_boot.resolve()
    cgb_boot = args.cgb_boot.resolve() if args.cgb_boot else boot.with_name("cgb_boot.bin")
    emulator = ("--sameboy", sameboy, "--boot", boot)
    rgbds = ("--rgbds", args.rgbds.resolve()) if args.rgbds else ()
    preset_flag = () if core else ("--minimal",)

    checks = []

    def add_check(script, *arguments):
        checks.append((script, arguments))

    for test in (
        "cartridge_smoke", "critical_hits", "battle_fixes", "battle_turn_state", "status_medicine",
        "acid_armor", "battle_stats_return", "pp_restore_readout", "pokedex_capture_return", "bicycle_shortcut", "bicycle_fall",
        "bike_shop_sign", "npc_entry_position", "item_safety", "storage_counts", "shop_carry_count",
        "sprite_storage", "map_signs", "presentation_events", "adventure_checkpoints",
        "field_shortcuts", "pc_browsing", "shift_prompt", "celadon_roof_transactions",
        "forest_encounters", "mansion_sight", "menu_returns",
    ):
        # In parallel runs, schedule the slow color-independent cases separately.
        long_color_suite = test in ("adventure_checkpoints", "pp_restore_readout", "mansion_sight")
        if long_color_suite and (count > 1 or args.jobs > 1):
            for color in COLORS:
                add_check(f"tests/{test}.py", directory, *emulator, "--color", color)
        else:
            add_check(f"tests/{test}.py", directory, *emulator)

    add_check("tests/cgb_compatibility.py", directory, "--sameboy", sameboy, "--boot", cgb_boot)
    add_check("tests/level_up_moves.py", directory, *emulator, *preset_flag)
    add_check("tests/exp_all.py", directory, *emulator, *preset_flag)
    add_check("tests/title_smoke.py", directory, "--sameboy", sameboy, "--boot", sgb_boot)
    add_check("tests/battle_slide_timing.py", directory, *emulator, "--sgb-boot", sgb_boot)
    add_check("tests/protected_mechanics.py", directory, *emulator, "--linked")
    add_check("tests/bide_struggle.py", directory, *emulator, "--linked")
    add_check("tests/copied_trap_switch.py", roms[0], *emulator)
    add_check("tests/move_swap_smoke.py", *roms, *emulator, *preset_flag)
    add_check("tests/adventure_event_states.py", directory, *emulator, *preset_flag)
    add_check("tests/interrupted_save_smoke.py", *roms, "--library", sameboy, "--boot", boot)

    if core:
        for test in ("safari_session", "route_cut_tree", "npc_return", "ledge_landing",
                     "pokedex_area", "vermilion_gym_switches"):
            add_check(f"tests/{test}.py", directory, *emulator)

        pairs = product(roms, repeat=2) if args.all_link_pairs else ((roms[0], roms[2]),)
        for left, right in pairs:
            for room in ("trade", "battle"):
                add_check("tests/link_cable_smoke.py", left, right, *emulator, "--room", room)

        for test in ("move_info_authoring", "trainer_loss_authoring", "name_list_authoring"):
            add_check(f"tests/{test}.py", *emulator, *rgbds)

    add_check("tools/check_reference_colors.py", directory)
    add_check("spec/tools/validate_spec.py")
    add_check("tests/battle_caught_marker.py", directory, *emulator, "--sgb-boot", sgb_boot)
    add_check("tests/battle_exp_meter.py", directory, *emulator)
    add_check(SHARED_BUILD_CHECK, directory.name, *emulator, *rgbds)
    for test in ("field_sweep", "hp_and_level_one", "core_services", "field_menu_features",
                 "supply_and_move_info", "battle_pace", "tm_party_info", "purchasable_tms", "box_preview"):
        add_check(f"tests/{test}.py", directory, *emulator)

    add_check("tests/fight_info_browsing.py", directory, *emulator)
    add_check("tests/fight_info_display.py", directory, *emulator, "--sgb-boot", sgb_boot)
    add_check("tests/tm_browsing.py", directory, *emulator)
    add_check("tests/tm_inspection_controls.py", directory, *emulator, "--sgb-boot", sgb_boot)
    add_check("tests/trainer_movesets.py", directory, *emulator, *rgbds)

    add_check("tests/learn_info_browsing.py", directory, *emulator)
    run_checks(shard_checks(checks, index, count), args.jobs)


if __name__ == "__main__":
    main()
