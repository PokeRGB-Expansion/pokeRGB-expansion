# PokéRGB Expansion

Build English Gen 1 ROM hacks from a shared Red and Blue engine. Green plays like Blue and opens with Bulbasaur on its own English title screen.

Choose **Core** for bug fixes and conveniences such as the Fuchsia Move Deleter. Choose **Minimal** for the original battle and team-building rules with shared menu and safety improvements. Both keep the original Bag and box limits. [Player guide](spec/docs/16-game-changes.md) · [Project specification](spec/README.md)

## Play a release

1. Download the BPS patch for your preset and color. For example, Green uses `pokergb-green.bps` for Core or `pokergb-minimal-green.bps` for Minimal. [Release downloads](https://github.com/PokeRGB-Expansion/pokeRGB-expansion/releases/latest)
2. Open a BPS patcher. Select a clean English **Red** ROM for a Red patch, or a clean English **Blue** ROM for a Blue or Green patch. Select the downloaded patch and choose **Apply patch**. [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/)
3. Open the resulting game file in your Game Boy emulator. When upgrading, choose the same color and preset and keep a backup of your in-game save. [Tested saves and systems](spec/docs/07-testing-ci.md#link-and-save-testing)

## Compare moves in battle

In **FIGHT**, highlight a move and press **START**. **Up/Down** compares the active Pokémon’s moves on the current page. **SELECT** switches between stats and effect. **B** returns to FIGHT with the last move you inspected highlighted. Press **A** there to choose it. [In-game example](spec/docs/15-battle-information.md#compare-moves-in-fight)

## TM shopping

Highlight a TM at a Mart or the Game Corner prize counter and press **START**. Use **Up/Down** to compare offers in the counter’s order. The cursor and price follow you. **SELECT** switches between the move’s stats and its effect. Press **A** from either page to see all six party members and their compatibility. **B** returns to the last TM you inspected. Press A at the counter when you want to buy or redeem it.

In the Bag or item PC, use the same START, SELECT and A controls to inspect the highlighted machine. [Screens and controls](spec/docs/15-battle-information.md#before-buying-a-tm) · [Box previews and other game changes](spec/docs/16-game-changes.md) · [Custom trainer movesets](spec/research/tutorial-library.md#give-one-trainer-pokémon-a-custom-moveset)

## Build

Install GNU Make, a C compiler and RGBDS 1.0.4. Run these commands from the checkout. [Setup and download instructions](INSTALL.md)

```sh
make -j4
make -j4 PRESET=minimal
```

Each command builds all three colors. To build just one, pass `red`, `blue`, or `green` to Make. The game file (`.gbc`) and matching map and symbol files go under `build/core/` or `build/minimal/`. If RGBDS is outside your path, set `RGBDS` to its tool directory with a trailing slash.

Both presets show a Pokédex ball for a previously owned, identified wild species and a progress bar for the active Pokémon’s EXP. Authors can disable either display. For example, `make red BATTLE_CAUGHT_MARKER=0` keeps the EXP bar. Use `BATTLE_EXP_BAR=0` to hide the bar. Each switch accepts 0 or 1 and defaults to 1. Custom builds go in `build/hud-<marker>-<bar>/<preset>/`, so switching options keeps each configuration’s files separate. [Battle display rules](spec/research/battle-hud-displays.md)

The reference baseline is pret/pokered at `ba9c0568f64ae602fadda577a08c66639f93082a`. To check five existing upstream outputs against the original hashes, run `make compare BASELINE_DIR=/path/to/upstream/outputs`. [Upstream source](https://github.com/pret/pokered/tree/ba9c0568f64ae602fadda577a08c66639f93082a)

## Make your first hack

Try these three edits together in Red Core.

1. In the [Route 1 grass table](data/wild/maps/Route1.asm), change the first `db  3, PIDGEY` to `db  3, CATERPIE`. Each row gives the level and species. The first row accounts for 51 of 256 encounters. The [slot weights](data/wild/probabilities.asm) apply across routes.
2. In the [trainer parties](data/trainers/parties.asm), find `Rival1Data`. Replace its first row, `db 5, SQUIRTLE, 0`, with `db $FF, 3, METAPOD, 5, SQUIRTLE, 0`. The [Oak’s Lab script](scripts/OaksLab.asm) selects this team when **you choose Charmander**. The leading `$FF` gives each Pokémon its own level. The final zero ends the team.
3. In the [Route 1 clerk’s script](scripts/Route1.asm), change `lb bc, POTION, 1` to `lb bc, ANTIDOTE, 1`. Keep the event flag that tracks whether you took the sample. [GiveItem](home/give.asm) supplies the item name for the [receipt](text/Route1.asm), so the clerk’s message follows the edit.

Run `make -j4 red` and open `build/core/pokered.gbc` in an emulator. Start a new game, choose Charmander, and walk toward the lab exit to fight the new team. On Route 1, meet a level-3 Caterpie in the grass and accept the Antidote. Save and choose **Continue**. The clerk should give his follow-up dialogue and your Bag should still hold one Antidote.

## Tests

GitHub Actions builds each color and preset on Linux and macOS. Linux runs the emulator checks in eight parallel groups per preset. The local command runs all groups by default. To run the cartridge checks locally, build the game and provide the SameBoy 1.0.5 core library and its boot files.

```sh
python3 tests/run.py build/core --sameboy /path/to/library \
  --boot /path/to/dmg_boot.bin --sgb-boot /path/to/sgb_boot.bin
```

Use `build/minimal` for Minimal. Pass `--all-link-pairs` to test all Core color pairings in both cable roles. Pass `--rgbds /path/to/rgbds` when the tools are outside your path. Keep the SameBoy Color boot file, `cgb_boot.bin`, beside `dmg_boot.bin`, or pass `--cgb-boot` with its path.

Core's checks include a separate sample hack with a changed TM and move. The shop, item PC, Bag, prize counter, STATS, FIGHT, and level-up prompt all display the sample's move data. [Test plan](spec/docs/07-testing-ci.md)

## Credits

This unofficial project builds on [pret/pokered](https://github.com/pret/pokered). See its [tutorials](https://github.com/pret/pokered/wiki/Tutorials), [symbols](https://github.com/pret/pokered/tree/symbols), and [tools](https://github.com/pret/gb-asm-tools). Pokémon and the original games are the work of their respective creators and rights holders. [Research and source credits](spec/docs/08-provenance.md)
