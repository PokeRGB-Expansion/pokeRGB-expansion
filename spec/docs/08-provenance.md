# Provenance and distribution

## Settled scope

No project-wide MIT license is added. Keep the notices attached to inherited and imported files.

Keep this process small and factual. Preserve source history, credit the work used, retain applicable file-level notices, and avoid claims of rights the project has not established. A disclaimer does not create rights or guarantee protection from a takedown.

GitHub's licensing documentation distinguishes a license grant from merely making source visible. The technical spec does not rely on a blanket claim that a missing license permits every reuse. [GitHub licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)

## What the checked repositories establish

The pinned `pret/pokered`, Solus, Shin Lite, PureRGB and Solid Red trees have no root project-wide `LICENSE`/`COPYING` file under those names. Pokéemerald Expansion also has no such root file, but contains licenses/notices for several tools. The absence of a root file is a limited repository observation, not a complete rights review. [E38](../research/evidence.md#e38)

Pokéemerald Expansion asks users to credit RHH and contributors. That is useful evidence for its attribution practice; it is not an MIT declaration for the whole project. [E35](../research/evidence.md#e35)

The repository retains upstream Git history. Keep research comparisons distinct from actual imports and distinguish inherited disassembly, imported contributor work, independently written fixes, tools, and assets.

## Record each imported change

For code or an asset used directly, record the source repository, commit, file/routine, author where known, existing notice, reason for use, and integration changes. Preserve the original commit attribution where appropriate. Link the related bug/test record.

For a newly written implementation informed by a report, credit the report and identify the implementation separately. Do not describe a close port as independent work merely because labels or register choices changed.

For graphics and audio, record the actual creator/source. Do not strip credits because an asset is easy to find online. If a Green asset is based on an original-game asset, describe that provenance accurately.

Use a simple `CREDITS.md` plus a structured import ledger when code imports begin. This spec's [source lock](../research/source-lock.json) is a research ledger; it is not an import or permission ledger.

## Release form

The release package uses BPS patches. Apply Red to the original English Red cartridge image. Apply Blue and Green to the original English Blue cartridge image. Core uses the original `pokergb-<color>.bps` names and `patches.json`. Minimal uses `pokergb-minimal-<color>.bps` and `patches-minimal.json`. Each manifest records the exact input SHA-1 and output SHA-256 for each color, plus each patch's SHA-256.

Build all three colors from the same checkout and preset before you package a release. Use the Floating IPS v198 command-line tool. If you build the tool from its tagged source, use `make TARGET=cli COMMIT_COUNT=198 CFLAGS=-O2`. [Floating IPS v198](https://github.com/Alcaro/Flips/tree/v198)

```sh
python3 tools/release_patches.py create \
  --base-red /path/to/original-red.gb \
  --base-blue /path/to/original-blue.gb \
  --build-dir build/core --output build/release-core \
  --flips /path/to/flips
```

The command creates an output directory with three patches and the manifest after it checks the original cartridge hashes and applies each patch to verify its result against the corresponding build. Run the command again with `verify` in place of `create` to check an existing package. To check reproducibility, build again from clean inputs, create a second package in a fresh directory, and compare the two packages.

The source tree also builds each color directly. See the [build instructions](../../README.md#build).

Public project text can identify the project as an unofficial fan effort and credit the original game rights holders and community sources. Do not claim Nintendo, Game Freak, Creatures, or The Pokémon Company approval. Do not invent special wording that supposedly prevents enforcement.

## Boundaries still requiring engineering evidence

Patch compatibility, save interoperability and link compatibility are technical test claims. They are not established by provenance or by keeping a familiar cartridge title. Resolve them in the implementation and publish only the tested support matrix.
