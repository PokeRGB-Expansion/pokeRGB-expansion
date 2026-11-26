# Change the starters and test your trainers

Both Core and Minimal use the same starter and trainer data. This example gives the player a choice of Pikachu, Squirtle or Bulbasaur. It also gives the first Route 3 Youngster’s Rattata Quick Attack and Tail Whip.

## Change Oak’s three starters

In [the species constants](../../constants/pokemon_constants.asm), change `DEF STARTER1 EQU CHARMANDER` to `DEF STARTER1 EQU PIKACHU`. The three entries run from left to right across Oak’s table. Use three different species with Pokédex entries.

Each ball now shows the chosen species’ full Pokédex entry. Oak names that Pokémon when he offers it. Accept the first ball to receive Pikachu and face Squirtle. Accept the third to receive Bulbasaur and face Pikachu. A preview leaves the player’s own Pokédex records intact.

The stock trio keeps Oak’s original fire, water and plant descriptions. Other species get an offer using their name. For custom dialogue, replace the corresponding `starter_offer STARTER1`, `STARTER2` or `STARTER3` invocation in [Oak’s text](../../text/OaksLab.asm) with a text block ending in `done`. Use `text_ram wNameBuffer` to insert the selected Pokémon’s name.

The rival’s [three lab teams](../../data/trainers/parties.asm) start with `STARTER2`, `STARTER3` and `STARTER1`, respectively. The rival always takes the next ball, going back to the first after the third. Later rival teams have explicit species and levels. Edit those rosters if you want the rival to keep, evolve or replace the custom starter later in the story. Check the [Champion’s signature moves](../../engine/battle/read_trainer_party.asm), too. A `trainer_moves` entry for that member overrides its signature moves.

## Give a trainer one custom moveset

Follow the [Route 3 Youngster example](tutorial-library.md#give-one-trainer-pokémon-a-custom-moveset). Rattata gets two moves. Ekans keeps the moves it would ordinarily know. The other Youngsters keep their own teams.

## Check your edited game

Build the color and preset you want to test. Keep the `.sym` symbol file next to its ROM. With [SameBoy’s test library and boot file](../docs/07-testing-ci.md), run:

```sh
python3 tests/author_checks.py build/core/pokered.gbc \
  --sameboy /path/to/library --boot /path/to/dmg_boot.bin
```

You can also pass a build directory to check the games in it. The command loads your compiled trainer teams in the emulator and checks their species and levels against your trainer data. For explicit `trainer_moves` entries it also checks the actual moves and starting PP. It opens each of your three starter previews and checks that it shows the Pokémon’s weight and preserves the seen and owned records. It does not need the original Kanto dialogue, movesets, map layout or a playthrough. It expects PokéRGB’s trainer table format and starter preview routine. If your project replaces either system, adapt those checks to its design.

For the tutorial above, also play the original Kanto map events in the emulator:

```sh
python3 tests/author_walkthrough.py build/core/pokered.gbc --route3-example \
  --sameboy /path/to/library --boot /path/to/dmg_boot.bin
```

This starts separate games in Oak’s Lab, selects each starter with the controls, checks the offer and gift, and walks to the rival battle. The Route 3 check enters the Youngster’s sight line and reads Rattata’s two moves and their PP after it enters battle. Omit `--route3-example` to check just the lab. These checks depend on the original lab layout, starter events and first rival encounter. The Route 3 check also expects the Youngster at his original position with the tutorial moveset.

PokéRGB’s [full reference checks](../../tests/run.py) cover its own complete Kanto adventure. Content-specific expectations there can change when you build a different adventure.
