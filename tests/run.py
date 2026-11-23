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
    args = parser.parse_args()

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
    preset_flag = () if core else ("--minimal",)

    for test in (
        "cartridge_smoke", "critical_hits", "battle_fixes", "battle_turn_state", "status_medicine",
        "acid_armor", "battle_stats_return", "pp_restore_readout", "pokedex_capture_return", "bicycle_shortcut", "bicycle_fall",
        "bike_shop_sign", "npc_entry_position", "item_safety", "storage_counts", "shop_carry_count",
        "sprite_storage", "map_signs", "presentation_events", "adventure_checkpoints",
        "field_shortcuts", "pc_browsing", "shift_prompt", "celadon_roof_transactions",
        "forest_encounters", "mansion_sight", "menu_returns",
    ):
        run_script(f"tests/{test}.py", directory, *emulator)

    run_script("tests/cgb_compatibility.py", directory, "--sameboy", sameboy, "--boot", cgb_boot)
    run_script("tests/level_up_moves.py", directory, *emulator, *preset_flag)
    run_script("tests/title_smoke.py", directory, "--sameboy", sameboy, "--boot", sgb_boot)
    run_script("tests/battle_slide_timing.py", directory, *emulator, "--sgb-boot", sgb_boot)
    run_script("tests/protected_mechanics.py", directory, *emulator, "--linked")
    run_script("tests/bide_struggle.py", directory, *emulator, "--linked")
    run_script("tests/copied_trap_switch.py", roms[0], *emulator)
    run_script("tests/move_swap_smoke.py", *roms, *emulator, *preset_flag)
    run_script("tests/adventure_event_states.py", directory, *emulator, *preset_flag)
    run_script("tests/interrupted_save_smoke.py", *roms, "--library", sameboy, "--boot", boot)

    if core:
        for test in ("safari_session", "route_cut_tree", "npc_return", "ledge_landing",
                     "pokedex_area", "vermilion_gym_switches"):
            run_script(f"tests/{test}.py", directory, *emulator)

        pairs = product(roms, repeat=2) if args.all_link_pairs else ((roms[0], roms[2]),)
        for left, right in pairs:
            for room in ("trade", "battle"):
                run_script("tests/link_cable_smoke.py", left, right, *emulator, "--room", room)

        rgbds = ("--rgbds", args.rgbds.resolve()) if args.rgbds else ()
        for test in ("move_info_authoring", "trainer_loss_authoring", "name_list_authoring"):
            run_script(f"tests/{test}.py", *emulator, *rgbds)

    run_script("tools/check_reference_colors.py", directory)
    run_script("spec/tools/validate_spec.py")


if __name__ == "__main__":
    main()
