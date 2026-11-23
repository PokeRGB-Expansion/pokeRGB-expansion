# Emerald Expansion configuration reference

Checked on 2026-10-12 against `rh-hideout/pokeemerald-expansion` master at `8fb02c6f2b81271e795d3f6aca61733fec739016` and the original `pret/pokeemerald` reference at `731ad5bfd6e6f265508d0efcca0ba42f9dcf5881`. This is a source and configuration review. No Emerald ROM was built, played, or compared with vanilla.

## What the source establishes

| Area | Checked stock default | Developer control |
|---|---|---|
| Species generations | All nine generation groups are enabled | Enable or disable generation groups and individual families |
| Later forms and evolutions | Mega, regional forms, and cross-generation evolution groups are enabled | Separate group controls; excluding later generation families alone is not a complete original-roster policy |
| Shared rule/data generation | `GEN_LATEST` is `GEN_9` | Change that value or override individual rule/data settings |
| Battle rules | Critical chances/damage and physical/special categories use the shared generation default | Select earlier rules independently where the engine provides that setting |
| Species data | Updated types, stats, and learnsets use the shared generation default | Select older data without selecting a species roster |
| Graphics and other Boolean features | Several defaults differ from original Emerald | Review their separate switches; the shared generation value does not control every feature |

The generation/family controls guard species data. For example, `P_FAMILY_TURTWIG` depends on `P_GEN_4_POKEMON`, and that family guard surrounds Turtwig's species record. [E63](evidence.md#e63)

Compiling species support and placing species in an adventure are separate tasks. The checked Route 101 encounter record lists Wurmple, Poochyena, and Zigzagoon even though all nine generation groups are enabled. A developer can choose the species in encounters and other content. This does not establish that every map or trainer is unchanged from original Emerald. [E63](evidence.md#e63)

The source warns that changing the highest enabled generation can change the save layout and require a fresh save. Generation controls follow the first introduced family member. Later evolutions and regional forms therefore need their own review when restricting a roster. [E63](evidence.md#e63)

## Default policy and an Emerald-like game

The project's configuration policy favors enabling developer improvements and modern Pokémon behavior. It treats save-changing additions separately and requires configuration for them. Its broad stock defaults are deliberate; it does not force downstream developers to keep those choices. [E64](evidence.md#e64)

An Emerald-like project can restrict its roster, use Gen 3 rule/data selections, and choose original-style assets and other features. That is supported configuration design. A single generation setting is not a verified “vanilla plus bug fixes” preset: species controls, forms, graphics, and independent features still need review. No whole-game equivalence or working combination is certified by this source-only check. [E63](evidence.md#e63), [E64](evidence.md#e64)

## Can a developer make a mostly vanilla hack?

Yes. The available controls and editable game data support a project with Emerald's adventure, an original-style roster, and a few small content changes. Later species do not have to be used. This conclusion follows from the checked configuration and data boundaries; it is not a claim that a complete vanilla preset was built and tested. [E63–E64](evidence.md#e63)

“Mostly vanilla” and “every original behavior except my chosen edits” are different targets. Two checked differences show why generation controls alone do not establish the latter:

- **Random-number generation:** original Emerald multiplies and adds fixed numbers to one 32-bit state value. Expansion uses SFC32, a different generator with four 32-bit state values and different seed/update functions. Its checked `Random` and `SeedRng` paths do not select the original algorithm through `GEN_LATEST`. Choosing Gen 3 rules therefore does not restore the original random sequence. [E65](evidence.md#e65)
- **Trainer decisions:** Expansion's documentation describes its basic trainer settings as making better move choices than vanilla. The three flags in that group are confirmed in the constants. This is a documented behavior claim with a checked flag definition, not a complete executable AI comparison. Older rule selections must not be treated as proof that the original trainer logic is restored. [E66](evidence.md#e66)

The trainer AI does have developer controls. The checked guide shows selecting flags in trainer records. It would be too broad to say that developers have no choice over AI behavior; a complete profile restoring the original implementation was not verified. The stated configuration policy favors modern behavior by default. The maintainers' specific reasoning about full original-game support was not established here. [E64](evidence.md#e64), [E66](evidence.md#e66)

Expansion also documents multiplayer support between Expansion games and excludes official-game compatibility. Its README recommends the original decompilation when that compatibility matters. This is its stated support boundary, not a test performed here. [E66](evidence.md#e66)

For an exact original-behavior starting point, `pret/pokeemerald` is the direct reference. Its README identifies the original ROM it reconstructs and its expected hash. A developer can make small edits there. This review did not execute that build. Restoring original behavior inside Expansion is source work and verification; the evidence above does not establish that it is impossible. [E67](evidence.md#e67)

## Application to PokéRGB Expansion

Use the separation of capabilities and developer choices as inspiration. Keep PokéRGB's own default: original Gen 1 behavior plus its accepted, verified corrections. Small, original-style hacks are a primary use case. Adding engine support for a later generation or alternative mechanic does not enable it in the reference game.

If a proposed change's evidence or place in the core is uncertain, exclude the change and keep the original behavior. Badge stacking is retained. A later developer feature may offer a correction with an explicit disabled default and interaction tests.

Test the default contract after adding any optional system. Publish the supported configurations and actual evidence.

## Reproduce the source check

The `expansion-config` and `emerald-vanilla` entries in [source-lock.json](source-lock.json) record these references separately. Earlier Emerald Expansion references stay at their original pin. [E63–E67](evidence.md#e63) record the exact files, line ranges, and fingerprints.
