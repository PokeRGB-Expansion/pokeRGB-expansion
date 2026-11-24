"""Build or verify the three BPS release patches against English Red and Blue."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory


FLIPS_VERSION = "Floating IPS v198"
# Keep the public Core file names used since v0.1.0.
PACKAGES = {
    "core": ("pokergb-", "patches.json"),
    "minimal": ("pokergb-minimal-", "patches-minimal.json"),
}
# English cartridge hashes from the pinned pret/pokered roms.sha1.
BASE_SHA1 = {
    "red": "ea9bcae617fdf159b045185467ae58b2e4a48b9a",
    "blue": "d7037c83e1ae5b39bde3c30787637ba1d4c48ce2",
}
TARGET_BASES = {"red": "red", "blue": "blue", "green": "blue"}


def run_flips(flips, *args):
    return subprocess.run([flips, *args], check=True, capture_output=True, text=True)


def check_flips(flips):
    version = run_flips(flips, "--version").stdout.strip()
    if version != FLIPS_VERSION:
        raise ValueError(f"Expected {FLIPS_VERSION}. Found {version or 'no version'}.")


def check_bases(bases):
    for color, path in bases.items():
        digest = hashlib.sha1(path.read_bytes()).hexdigest()
        if digest != BASE_SHA1[color]:
            raise ValueError(
                f"Use the exact original English {color.title()} cartridge.\n"
                f"Expected SHA-1 {BASE_SHA1[color]}. Found {digest} in {path}."
            )


def read_targets(build):
    targets = {}
    for color in TARGET_BASES:
        path = build / f"poke{color}.gbc"
        contents = path.read_bytes()
        title = f"POKEMON {color.upper()}".encode("ascii")
        if contents[0x134:0x144].rstrip(b"\0") != title:
            raise ValueError(f"{path} does not have the expected {color.title()} title.")
        targets[color] = (path, contents)
    return targets


def compare_patches(flips, bases, targets, folder, preset):
    prefix, _ = PACKAGES[preset]
    manifest = {"format": "BPS", "patcher": FLIPS_VERSION, "targets": []}
    with TemporaryDirectory(prefix="pokergb-verify-") as scratch:
        for color, base_color in TARGET_BASES.items():
            patch = folder / f"{prefix}{color}.bps"
            data = patch.read_bytes()
            if not data.startswith(b"BPS1"):
                raise ValueError(f"{patch} is not a BPS file.")
            rebuilt = Path(scratch) / f"poke{color}.gbc"
            run_flips(flips, "--apply", patch, bases[base_color], rebuilt)
            path, target = targets[color]
            if rebuilt.read_bytes() != target:
                raise ValueError(f"{patch} did not rebuild {path} byte for byte.")
            manifest["targets"].append({
                "target": path.name,
                "target_sha256": hashlib.sha256(target).hexdigest(),
                "patch": patch.name,
                "patch_sha256": hashlib.sha256(data).hexdigest(),
                "base": f"English {base_color.title()}",
                "base_sha1": BASE_SHA1[base_color],
            })
    return manifest


def create_patches(flips, bases, targets, output, preset):
    prefix, manifest_name = PACKAGES[preset]
    if output.exists() or output.is_symlink():
        raise ValueError(f"{output} already exists. Choose a new output directory.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".pokergb-patches-", dir=output.parent) as scratch:
        stage = Path(scratch) / "patches"
        stage.mkdir()
        for color, base_color in TARGET_BASES.items():
            patch = stage / f"{prefix}{color}.bps"
            run_flips(flips, "--create", "--bps-delta", bases[base_color], targets[color][0], patch)
        manifest = compare_patches(flips, bases, targets, stage, preset)
        contents = json.dumps(manifest, indent=2) + "\n"
        (stage / manifest_name).write_bytes(contents.encode("utf-8"))
        stage.rename(output)


def verify_patches(flips, bases, targets, output, preset):
    _, manifest_name = PACKAGES[preset]
    manifest = json.loads((output / manifest_name).read_text(encoding="utf-8"))
    if manifest != compare_patches(flips, bases, targets, output, preset):
        raise ValueError(f"{output / manifest_name} does not match the verified patch and build hashes.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("create", "verify"))
    parser.add_argument("--base-red", type=Path, required=True)
    parser.add_argument("--base-blue", type=Path, required=True)
    parser.add_argument("--build-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--preset", choices=PACKAGES, help="Preset to package. Inferred from the build directory when named core or minimal.")
    parser.add_argument("--flips", default="flips", help="Path to Floating IPS v198.")
    args = parser.parse_args()
    preset = args.preset or (args.build_dir.name if args.build_dir.name in PACKAGES else "core")
    if args.build_dir.name in PACKAGES and preset != args.build_dir.name:
        parser.error("The preset must match the build directory.")
    bases = {"red": args.base_red, "blue": args.base_blue}
    try:
        check_bases(bases)
        targets = read_targets(args.build_dir)
        check_flips(args.flips)
        if args.action == "create":
            create_patches(args.flips, bases, targets, args.output, preset)
        else:
            verify_patches(args.flips, bases, targets, args.output, preset)
    except subprocess.CalledProcessError as error:
        details = error.stderr.strip() or error.stdout.strip()
        parser.exit(1, f"Floating IPS failed. {details}\n")
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")

    print(f"Verified Red from Red, Blue from Blue, and Green from Blue in {args.output}.")


if __name__ == "__main__":
    main()
