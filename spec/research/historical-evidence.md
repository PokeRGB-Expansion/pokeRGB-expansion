# Historical evidence and its limits

The [current rules review](core-rule-precedents.md) compares the badge, Ghost, Gust and Charizard cases, including the intermediate evidence in the [Yellow review](yellow-rules-review.md). Core now adopts the Ghost weakness and Flying Gust while Minimal preserves the English cartridge chart and move types.

Checked on 2026-10-12. The guidebook pages were inspected visually, with OCR used to locate them. [E53–E55](evidence.md#e53) record source URLs, scan fingerprints, page locations, and check dates. No guidebook files or pages are distributed in this specification package.

## Prima's guide

Elizabeth M. Hollinger's *Pokémon: Prima's Official Strategy Guide* has a Nintendo licensing seal and a 1998 copyright. Printed page 39 recommends Bug and Ghost Pokémon against Psychic Pokémon. These details were checked in the [archived scan](https://archive.org/details/PokemonOfficialPrimaStrategyGuide).

That advice does not specify a Ghost attack multiplier or prove an internal Game Freak decision. A Pokémon's type and its moves are different facts. A seal does not prove review of each statement.

## Nintendo Power's guide

Printed page 41 of the [Pokémon Red & Blue Player's Guide scan](https://archive.org/details/NintendoPower1998PokemonRedBlue) says Dream Eater puts its target to sleep and implies that training Haunter yields Gengar. The checked English game instead requires the target to be asleep for Dream Eater and lists Haunter's evolution as a trade. [E54](evidence.md#e54)

This is a concrete reason to test guidebook claims against the game. It does not make every statement in that guide false or settle the intended Ghost/Psychic relationship.

## Sabrina's gym dialogue

The pinned English Red/Blue gym text says Psychic Pokémon fear ghosts and bugs. The same game's table gives Ghost attacks zero effectiveness against Psychic; Lick has 20 power, while the fixed-damage path bypasses the ordinary chart. These are source facts. Dialogue about Pokémon matchups does not resolve internal intent or prove a particular attack multiplier was specified. [E62](evidence.md#e62)

The default chart is an explicit project choice. Keep the historical question separate from that requirement.

## Stadium interoperability

The [official Pokémon description](https://www.pokemon.com/uk/pokemon-video-games/pokemon-stadium/) confirms that the original N64 game imports RBY Pokémon through the Transfer Pak and can play the Game Boy games on a TV. [Nintendo's original-game description](https://www.nintendo.com/en-gb/Games/Nintendo-64/Pokemon-Stadium-269679.html) corroborates those functions.

Interoperability does not prove why the designers retained a type chart or that the N64 battle engine and Game Boy game must produce identical outcomes. PokéRGB's baseline is the pinned English Red/Blue code. Stadium support for a modified game remains unassessed, as listed in the compatibility plan.

## Questions not resolved by these sources

The pinned `pret/pokestadium` repository's `oldnotes/stadium1/text/` files contain matching ordered move names and descriptions. Night Shade's entry says its damage ignores the target's type. Karate Chop and Gust are described as Normal. These are checked text notes, not a build or a test of the Stadium battle engine. [E59](evidence.md#e59)

The full Stadium battle-engine table and Game Freak’s final internal design specification remain unverified. The [subsequent Yellow review](yellow-rules-review.md) compares the Japanese guide’s explicit Ghost weakness and Flying Gust, the US manual chart, both languages’ Gym hints and the Stadium 2 Academy’s explanation.

## Badge stat descriptions and reconstructed source

The original US manual assigns Speed to Thunder and Defense to Soul; the checked FireRed/LeafGreen calculation agrees. English Red/Blue implements the opposite mapping. See the [badge-intent review](badge-intent.md) for exact source/page locations, the likely-code-mix-up inference, interview-search limits, and the distinction between matching disassembly and original developer comments. [E75–E77](evidence.md#e75)

D25 accepts the RGB-010a code correction: Thunder→Speed and Soul→Defense, retaining original descriptions. This replaces the earlier text-only policy while preserving the separate stacking decision. Historical evidence supports the likely intended mapping; project adoption does not turn that inference into proof.
