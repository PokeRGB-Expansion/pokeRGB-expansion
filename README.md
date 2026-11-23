# PokéRGB Expansion

PokéRGB Expansion is a developer foundation for English Generation I Pokémon ROM hacks. It builds Red, Blue, and a cosmetic Green from one source tree. Green uses Blue's gameplay with a Bulbasaur title and its own Super Game Boy colors.

Core is the default preset. Minimal keeps the original battle rules and inventory limits while sharing selected interface and safety fixes. [Downloads](https://github.com/PokeRGB-Expansion/pokeRGB-expansion/releases) · [Project specification](spec/README.md) · [Core release checks](spec/docs/09-roadmap.md)

## Build

Install GNU Make, a C compiler, libpng, and RGBDS 1.0.4. [Platform instructions](INSTALL.md)

```sh
make -j4
make -j4 PRESET=minimal
```

Each command builds all three colors. To build just one, pass `red`, `blue`, or `green` to Make. The cartridge and matching map and symbol files go under `build/core/` or `build/minimal/`. If RGBDS is outside your path, set `RGBDS` to its tool directory with a trailing slash.

The reference baseline is pret/pokered at `ba9c0568f64ae602fadda577a08c66639f93082a`. To check five existing upstream outputs against the original hashes, run `make compare BASELINE_DIR=/path/to/upstream/outputs`. [Upstream source](https://github.com/pret/pokered/tree/ba9c0568f64ae602fadda577a08c66639f93082a)

## Make your first edit

In [Route 1's encounter table](data/wild/maps/Route1.asm), change the first `db  3, PIDGEY` to `db  3, CATERPIE`. Build Red Core with `make -j4 red`, open `build/core/pokered.gbc` in your emulator, and walk through the grass on Route 1. Caterpie now appears at level 3 in one of the original encounter slots.

## Tests

GitHub Actions builds each color and preset on Linux and macOS. To run the cartridge checks locally, build the game and provide the SameBoy 1.0.5 core library and its boot files.

```sh
python3 tests/run.py build/core --sameboy /path/to/library \
  --boot /path/to/dmg_boot.bin --sgb-boot /path/to/sgb_boot.bin
```

Use `build/minimal` for Minimal. Pass `--all-link-pairs` to test all Core color pairings in both cable roles. Pass `--rgbds /path/to/rgbds` when the tools are outside your path.

Core's checks include a separate sample hack with a changed TM and move. The shop, item PC, Bag, prize counter, STATS, FIGHT, and level-up prompt all display the sample's move data. [Test plan](spec/docs/07-testing-ci.md)

## Credits

This unofficial project builds on [pret/pokered](https://github.com/pret/pokered). See its [tutorials](https://github.com/pret/pokered/wiki/Tutorials), [symbols](https://github.com/pret/pokered/tree/symbols), and [tools](https://github.com/pret/gb-asm-tools). Pokémon and the original games are the work of their respective creators and rights holders. [Research and source credits](spec/docs/08-provenance.md)
