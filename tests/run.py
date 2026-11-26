"""Run the game checks for a built Core or Minimal preset."""

import argparse
from itertools import product
from pathlib import Path
import subprocess
import sys

COLORS = ("red", "blue", "green")
ROOT = Path(__file__).resolve().parents[1]


def run_script(script, *args):
    subprocess.run([sys.executable, "-B", ROOT / script, *args], cwd=ROOT, check=True)


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
    args = parser.parse_args()
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
    add_check("tests/battle_hud_options.py", directory.name, *emulator, *rgbds)
    for test in ("field_sweep", "hp_and_level_one", "core_services", "field_menu_features",
                 "supply_and_move_info", "battle_pace"):
        add_check(f"tests/{test}.py", directory, *emulator)

    for script, arguments in checks[index - 1::count]:
        print(f"Running {script}", flush=True)
        run_script(script, *arguments)


if __name__ == "__main__":
    main()
