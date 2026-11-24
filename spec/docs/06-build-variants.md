# Red, Blue, and Green build plan

## Build identity

Select game color separately from product preset and release/debug mode. Within each supported preset and feature configuration, Green uses Blue gameplay. Build only the combinations advertised for that release. Include color, preset, and selected features in the build record and keep their generated objects separate.

| Build | Gameplay data | Visual identity | Language |
|---|---|---|---|
| Red | Pinned English Red, plus the shared correction set | Red | English |
| Blue | Pinned English Blue, plus the shared correction set | Blue | English |
| Green | Exactly Blue's gameplay data and correction set | Green cosmetic overrides | English |

Red and Blue remain distinct games where upstream defines a gameplay difference. Green introduces no new encounters, trades, prize costs, learnsets, mechanics, or progression. There is no Japanese target and no requirement to reconstruct Japanese Green.

Solus and PureRGB have cosmetic RGB variants because they consolidate availability. That is a useful presentation model, not a reason to merge this foundation's Red/Blue distributions. [E33–E34](../research/evidence.md#e33)

## Build implementation

Keep one source tree and use per-target object outputs. Upstream already assembles `_red.o`, `_blue.o`, and `_blue_debug.o` separately and defines `_RED` or `_BLUE` for each target. [E02](../research/evidence.md#e02)

Green sets `_BLUE` for gameplay and `_GREEN_VISUALS` for presentation. The assembler checks that Green uses the Blue selection. Keep new Green cases in presentation code and data.

Do not define `_RED` and `_BLUE` together. Upstream sometimes uses separate `IF DEF(...)` blocks, so defining both can emit both variants. Invalid or contradictory target selections must fail before assembly.

The `red`, `blue`, and `green` targets write `pokered.gbc`, `pokeblue.gbc`, and `pokegreen.gbc` under the selected preset directory. The filename suffix is shared across Game Boy models.

Reuse the shared engine and shared graphics inputs, with variant-safe dependency tracking. A source or asset change must invalidate the correct objects for every target. Build in isolated per-target directories or fix shared generated-file races. Verify clean parallel builds, sequential Red→Green→Blue builds, and rebuilds after a variant-specific edit.

Keep Blue debug support available during development. A Green debug build is useful after its visual overrides exist, but it is not a fourth consumer release or separate engine.

## Gameplay differences to preserve

Audit every upstream `_RED`/`_BLUE` selection, including:

- Wild species and encounter slots/rates.
- Game Corner species, prices, prize levels, and related dialogue.
- Any version-dependent trades, scripts, names or information.
- Presentation branches in title/intro, credits, animations, SGB palettes/borders, and asset inclusion.

The source branch audit is [variant-sites.csv](../research/variant-sites.csv). Its classification is a routing hint, not a completed gameplay audit. A version-specific routine must not be treated as cosmetic merely because it is outside the encounter directory.

Preserve Red/Blue's actual data wherever it differs. Do not create differences where the source shares a table. The test should compare extracted compiled data with the relevant reference, rather than rely on a hand-written list of “version exclusives.”

## Green presentation scope

Green uses a `POKEMON GREEN` cartridge header and an English “Green Version” title. Bulbasaur appears first, using its English-game sprite. Red starts with Charmander, and Blue starts with Squirtle.

| Green change | Source |
|---|---|
| Cartridge name and checksum | Green target in [Makefile](../../Makefile) |
| Title text and Bulbasaur | [Title code](../../engine/movie/title.asm) and the [original lettering in English Red](../../gfx/title/red_version.png), using [Japanese Green’s tile order](https://github.com/Narishma-gb/pokegreen/blob/953f41b34108621b2bf13c3b1e53abfc9c3e5aec/engine/movie/title.asm#L347-L354) |
| Green subtitle, with Blue’s shared palette for the Pokémon, trainer, and copyright | [Palettes](../../data/sgb/sgb_palettes.asm) and [title palette command](../../data/sgb/sgb_packets.asm) |
| Super Game Boy border | [Border selection and colors](../../data/sgb/sgb_border.asm). The tiles and tilemap are the original Green border assets already tracked by pret/pokered. [Upstream import](https://github.com/pret/pokered/commit/2ebbb0d95eead4f40ec0bb7e9edd19526c2b2f3a) |

The [title test](../../tests/title_smoke.py) checks the first Pokémon, English title tiles, and rendered palette in Super Game Boy mode. Green keeps Blue's gameplay, including the names, encounters, and scripts used after the title. Compare Blue and Green at the first gameplay decision with controlled random inputs. Real-time timer samples can vary across title sequences.

## Equality checks

Green is not required to be byte-identical to Blue. Cosmetics, headers, checksums and code layout can differ. Its gameplay data and calculations must be equivalent.

For Blue/Green, compare decoded species/move/type data, encounters, trainer sets, trades, prices and scripts. Compare symbol-selected routines where feasible; use behavioral fixtures where layout changes make raw byte comparison unsuitable. Any remaining binary difference must map to an approved visual/header change or documented linker-layout effect.

Run the same protected-mechanics fixtures on Red, Blue, and Green with equal initial battle state and supplied RNG. Compare Green/Blue progression and a save/load trace. For Red/Blue, expected data differences must match the pinned upstream's version selections.

## Acceptance criteria

A downstream project may also publish different content editions. Its expanded edition can keep one Special stat while selecting different species or battle rules. Advertise the actual settings for each artifact. [Paired-edition example and tests](../research/emerald-rogue-builds.md)

Public Core includes Red, Blue and cosmetic Green. Apply these checks to all three integrated targets.

1. All three targets build from one clean checkout with the pinned toolchain.
2. Engine corrections and mechanics tests are shared and pass on every target.
3. Red/Blue data differences match the original reference unless an RGB fix explicitly changes one.
4. Green/Blue gameplay comparisons have no unexplained difference.
5. Green's title and relevant SGB presentation are checked visually; menus and battle screens remain readable in DMG-compatible output.
6. Per-variant builds cannot reuse stale objects from another target.
7. Release notes state that Green is the project's cosmetic Blue variant.
