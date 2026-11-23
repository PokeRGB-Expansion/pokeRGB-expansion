# PokéRGB Expansion

PokéRGB Expansion is a developer foundation for English Generation I Pokémon ROM hacks. It builds Red, Blue, and a cosmetic Green from one source tree. Green uses Blue's gameplay with a Bulbasaur title and its own Super Game Boy colors.

Core is the default preset. Minimal keeps the original battle and resource rules while sharing selected interface and safety fixes. The complete public Core release is in development. [Project specification](spec/README.md) · [Core release checks](spec/docs/09-roadmap.md)

## Build

Install GNU Make, a C compiler, libpng, and RGBDS 1.0.4. [Platform instructions](INSTALL.md)

```sh
make -j4
make -j4 PRESET=minimal
```

Each command builds all three colors. To build just one, pass `red`, `blue`, or `green` to Make. The cartridge and matching map and symbol files go under `build/core/` or `build/minimal/`. If RGBDS is outside your path, set `RGBDS` to its tool directory with a trailing slash.

The reference baseline is pret/pokered at `ba9c0568f64ae602fadda577a08c66639f93082a`. To check five existing upstream outputs against the original hashes, run `make compare BASELINE_DIR=/path/to/upstream/outputs`. [Upstream source](https://github.com/pret/pokered/tree/ba9c0568f64ae602fadda577a08c66639f93082a)

## Tests

CI builds each preset and checks gameplay tables across reference colors. To run the linked-cartridge smoke tests locally, point this command at your SameBoy 1.0.5 core library and its DMG boot file.

```sh
python3 tests/cartridge_smoke.py build/core --sameboy /path/to/library --boot /path/to/dmg_boot.bin
```

The smoke tests reach New Game in each color, test confirmed and cancelled box changes against a disposable save, and exercise Bag Move INFO and STATS navigation.

## Credits

This unofficial project builds on [pret/pokered](https://github.com/pret/pokered). See its [tutorials](https://github.com/pret/pokered/wiki/Tutorials), [symbols](https://github.com/pret/pokered/tree/symbols), and [tools](https://github.com/pret/gb-asm-tools). Pokémon and the original games are the work of their respective creators and rights holders. [Research and source credits](spec/docs/08-provenance.md)
