# Architecture

## Verified starting point

The implementation base is `pret/pokered` at [ba9c0568](https://github.com/pret/pokered/tree/ba9c0568f64ae602fadda577a08c66639f93082a). It reconstructs English Red/Blue with RGBDS 1.0.4. The source lock records this revision under `implementation_base`. Historical research citations identify the exact sources originally checked. [Upstream review](../research/validation.md#november-upstream-update)

The engine is RGBDS assembly, not an Emerald-style C decompilation. Keep that toolchain for the first implementation. Modern C configuration snippets from the discussion were illustrations, not an implementation choice.

Current responsibilities already have useful locations:

| Area | Upstream locations | Initial approach |
|---|---|---|
| Battle flow and calculations | `engine/battle/core.asm`, `effects.asm`, `move_effects/` | Small fixes and well-defined routine inputs/outputs |
| Rules and game data | `constants/`, `data/moves/`, `data/types/`, `data/pokemon/`, `data/wild/` | Keep existing formats initially; add validators where needed |
| World and events | `maps/`, `scripts/`, `engine/overworld/`, `engine/events/` | Target specific invalid states; preserve progression |
| Graphics and sound | `gfx/`, `data/sgb/`, `audio/`, movie/animation routines | Share assets, with explicit visual overrides |
| Memory and storage | `ram/`, `macros/ram.asm`, `layout.link`, save routines | Audit bounds and preserve the initial layout where possible |
| Builds and tooling | `Makefile`, `.rgbds-version`, `tools/`, `.github/` | Pin tools, add Green, and add a real test runner |

These are code ownership boundaries, not a requirement to reorganize the whole tree before shipping.

## Proposed initial structure

Fork the pinned upstream tree with its history. Keep changes grouped by purpose: one defect or tightly coupled repair per change. Keep the pristine reference available as a recorded commit and independently built test input. Store fixtures, expected results, and bug records beside the game tests.

Start with the named build settings and the routines that need them. Extract a routine when a concrete fix, test, or second caller makes its contract useful. Document registers read/written, flags, bank requirements, memory used, and side effects. That gives developers dependable entry points without prematurely designing an abstract engine.

For a routine called across ROM banks, document its bank and use the established switching interface. A bank is a portion of cartridge memory selected into the CPU's address space. The current helpers save and restore a one-byte bank number; larger capacity can require changing more than the cartridge header. [E18](../research/evidence.md#e18)

## Memory and capacity

The baseline targets original Game Boy behavior. The proposed Core hardware targets are DMG, CGB in compatible mode, and SGB presentation where upstream supports it. The exact tested hardware list is a release claim that must be earned, not inferred from an emulator launch.

The original Game Boy has 8 KiB each of work RAM and video RAM. The cartridge is accessed through 16 KiB ROM windows. MBC5 can address 8 MiB of ROM and, without rumble-specific restrictions, up to 128 KiB of cartridge RAM. Those capacities do not increase CPU speed or internal RAM. The pinned build currently specifies MBC3 with RAM and battery, not MBC5. [E02](../research/evidence.md#e02), [E19–E21](../research/evidence.md#e19)

Keep MBC3 initially unless an implemented feature needs a change. Do not reserve a large modern battle-state structure merely because later systems may need it. Track used and free bytes per ROM/RAM section from linker maps. Record frame/cycle cost for routines that affect animation, audio, or input. Set limits from measured headroom; do not invent fixed performance budgets in advance.

MBC5 expansion needs a separate design for the ninth ROM-bank bit, nested calls, interrupt handlers, graphics/audio reads, SRAM selection, save writes, and test cartridges. A header change alone cannot complete it.

## Species and move identifiers

Plan the shared data definitions and the places that read or write species IDs now. Keep the initial Core and Minimal builds compact. Introduce the two-byte representation before shipping large rosters, independently of battle rules and enabled content. The [architecture review](../research/species-id-architecture.md) identifies the exact stock structures, measured changes in a built prototype and the required save and link tests.

Party, box, and battle structures currently store species in one byte. Move slots also use one byte per move. A byte has 256 possible values, with sentinels and historical internal indexes consuming some of them. It is not a clean promise of 255 usable species. Pokédex numbering and internal species IDs are different concepts. [E17](../research/evidence.md#e17)

Use compact identifiers in the reference Core. Avoid adding new interfaces that unnecessarily promise an 8-bit species limit. A future wider-ID migration must cover:

- Party, boxes, encounters, trainer teams, battle state, names, graphics and cries.
- Learnsets, evolutions, move effects, type lookups, species-to-Pokédex mappings and seen/caught flags.
- Save checksums, box transfer, link serialization, debugging tools, and data generators.
- Empty/end markers, arithmetic, table indexing, and banked reads.

Test values at every representation boundary, including IDs above 255. Supporting a larger ID is only useful if storage, UI, battles, saves, and data validation all work with it.

## Data, rules, and future systems

Keep these choices conceptually independent:

| Choice | Must not silently require |
|---|---|
| A small encounter, trainer, or map edit | Expanded species support or changed battle rules |
| A presentation or developer-tool feature | Later Pokémon, types, or unrelated gameplay systems |
| A graphics, interface, or editing feature | Improved trainer AI or a replacement random-number generator |
| A MOVE POKÉMON storage interface | Automatic capture overflow into another box or increased capacity |
| Automatic capture storage in another available box | A MOVE POKÉMON interface, expanded capacity, or later-generation battle rules |
| Larger species roster | New critical-hit rules or a new type chart |
| Dark/Steel | Fairy, abilities, or a move-based physical/special split |
| Fairy | Mega Evolution or every modern combat system |
| Move-based physical/special split | Replacing all species stats and learnsets |
| Forms and transformations | A complete contemporary battle ruleset |

Independence means avoiding unnecessary coupling. Real dependencies still need explicit checks. A Mega Evolution design may require form data, temporary battle state, an activation mechanism, and possibly held items. Do not promise that every combination of features is supported.

The default build remains the original Gen 1 contract plus accepted corrections and interface improvements as the library grows. It is a maintained, tested starting point for small hacks. Later species, types, mechanics, and optional corrections do not become enabled merely because the engine supports them. Badge-stacking correction is a possible later developer feature; the default retains stacking.

Preserve the original trainer-decision rules and random-number algorithm in the default core, except for individually accepted defect repairs. If an alternative AI or generator is introduced, keep the baseline implementation available and test it through the real engine. An option labeled original is insufficient if it still calls changed decision or generator routines. Do not make a developer restore those routines by hand to use an unrelated feature.

Pokéemerald Expansion demonstrates separate controls for species families, forms, and rule generations. Its current stock defaults enable all nine generations and many modern rules. Use its configuration model as a reference while keeping this project's agreed conservative defaults. See [the checked comparison](../research/expansion-configuration.md). [E63–E64](../research/evidence.md#e63)

Use the [Core and Extensions guide](14-features-and-extensions.md) as the entry point for feature scope and defaults. Keep one shared source tree, a central developer configuration, and documentation for each extension. These are build choices; they do not require separate downloads or a runtime plug-in system.

When at least two real configurations exist, choose a small build manifest or assembly configuration format and validate it before assembly. Reject incompatible selections with a useful error. Compile unused systems out. Publish a short list of supported configurations and test that list. Do not create an exponential matrix of untested switches.

The first customization example must use the default core with only a small data or content edit. Later capability examples should include original rules with an expanded roster, a Dark/Steel configuration without Fairy, and a separate Fairy-enabled configuration. Their exact release order depends on measured costs.

## Save and link boundaries

A refactor can have shared source and two build behaviors. Make common box addressing and full-record handling available to callers that use them. Manual builds need only the live party and selected box. Enable remote search, pending arrivals and recovery only in an automatic-placement build. Preserve the original post-trade partial save. [Measured storage scope](../research/storage-policy-and-code.md) · [Other engine changes](../research/refactor-scope.md)

The [optional overflow contract](../research/box-overflow-contract.md) includes a measured storage allocation for the compact roster, a candidate design for unsaved arrivals and separate recovery tests. The [first-use box repair](../research/box-picker-safety.md) prevents a cancelled selection from changing an older save. Both affect which persistent writes are safe.

Initial proposal: preserve the vanilla serialized layout where practical, with a tested import path rather than a blanket promise that every save works. Separate game data in saves from temporary battle state. A changed species representation or storage system needs an explicit save-format version and a tested conversion or a clearly documented fresh-start requirement.

Do not silently interpret a mismatched save. Keep a backup during conversion. Test box changes, full storage, checksums, and interrupted writes; delaying a save write is not proof of safe recovery from power loss. [E32](../research/evidence.md#e32)

Keep mechanics compatibility separate from link packet compatibility. Two games can serialize the same bytes and calculate different battle results. Focus Energy alone makes a guarantee of vanilla link-battle compatibility unsafe. The proposed support boundary is matching PokéRGB mechanics releases; trade interoperability remains a separate test question. See [open decisions](10-open-decisions.md#q03).

## Developer experience

A downstream edition is a choice of content and rules independent of game color. Provide one documented command or build matrix for multiple named editions from one revision, with separate intermediate files, patch names, save identifiers and expected tests. [Emerald Rogue precedent and Yellow Rogue example](../research/emerald-rogue-builds.md)

The early developer guide must let a new contributor build, choose a variant, edit an encounter or learnset, run a focused regression, and find the reason for every deviation from upstream. Provide one documented command for the routine build-and-test workflow, plus a way to run a single regression. The exact command interface is an implementation choice.

Select color, product preset, and release/debug mode independently. Core is the initial default. Keep gameplay repairs small enough that Minimal can select the original rule from the same tree. Add a build switch when the second supported behavior needs it. Validate each supported selection before assembly. A debug build should expose enough battle state to reproduce a bug while keeping debug controls out of release builds. Recheck important scenarios in the normal release build; debug hooks can change timing or memory use.

Add diagnostics in small steps:

| Diagnostic | Useful result |
|---|---|
| ROM/RAM capacity | Used/free bytes per section and bank; fail on overflow and report measured headroom |
| Data references | Identify the file and record containing an invalid species, move, type, map, or event reference |
| Learnsets and evolutions | Check required fields, bounds, end markers, and references; preserve deliberate downstream choices |
| Encounters and trainers | Check record lengths, valid IDs, legal encoded values, and table structure |
| Scripts and events | Catch undefined labels/events and invalid arguments before playing the affected path |
| Debug sessions | Preserve symbols, maps, source/tool revisions, initial state, inputs, and supplied RNG for a repeatable failure |

Begin with checks over existing assembly data and clearer macros. Introduce a generated data format only when a real editing or capacity need justifies the conversion.

Large changes can break downstream source integration. Publish migration notes for deliberate interface changes. This is useful maintenance, not a promise to avoid rewrites.

## Trainer win and loss speech

A map trainer can take a sixth argument for a line shown when the player loses.

```asm
trainer EVENT_BEAT_ROUTE_3_TRAINER_0, 2, ChallengeText, PlayerWonText, AfterBattleText, PlayerLostText

PlayerLostText:
	text_start
	line "Try again later."
	prompt
```

The fourth argument is the trainer's speech when the player wins. The fifth is for talking to the trainer again after winning. Give the sixth argument a text script in the trainer's map bank. Use a local `text_far` wrapper if the dialogue itself lives in another bank. The game adds the trainer's name, so the example starts the speech on the next line. The loss speech plays before the usual blackout message and leaves the penalty and return point in place. Existing five-argument declarations keep their usual speech and blackout behavior. [Cartridge check](../../tests/trainer_loss_authoring.py)

## Later presentation and solo-play features

SELECT item registration is an accepted default feature, separate from the later capabilities below. Store an item ID rather than a bag position, validate possession and eligibility at use, and share the existing item's use restrictions. Bicycle checks span two paths: the forced-riding guard is in the menu, while other use checks are in the effect routine. A shortcut must retain both. Persist the registered choice through save/load, with no registration as the safe value for new games or imported saves lacking that field. The exact storage location and import handling require implementation review. See [PN-002](13-playthrough-intake.md#pn-002).

Contextual HM use is also an accepted default feature. Detect an eligible target on a fresh A press, identify a party Pokémon that knows the move, and ask for confirmation. Cut trees, Surf water, and Strength boulders are the required target cases. Share the existing move eligibility, badge and use checks before dispatching the effect. Those checks currently span the party menu and effect routines; calling an effect alone can bypass a badge or map guard. Preserve NPCs, signs, hidden events, and scripted input. See [PN-004](13-playthrough-intake.md#pn-004).

Keep the bag's 20-slot limit. An optional capacity change must account for working-memory allocation and serialized save data, rather than only editing the capacity constant. This engineering boundary does not establish the original designers' motive for the limit. [E72](../research/evidence.md#e72)

Optional developer capabilities can include separate field-move support that removes the learned-move or move-slot requirement, trade-evolution alternatives, a way to configure solo species availability, improved asset tools, and color features. They need their own data, rules, and tests. They are not default bug fixes or first-release requirements. Choose the next capability from an actual developer use case.

Presentation acceleration is a separate long-term proposal. A downstream game could shorten movement, text, battle animations, and transitions while keeping music and sound playback at normal timing. It must preserve battle calculations, event order, turn rules, and save behavior.

Fewer delays can change when inputs and random values are read. Test outcomes under controlled RNG, record any changed RNG call order, and check timing-sensitive events and two-endpoint link behavior. Measure audio and frame behavior on the supported hardware. Do not promise that an emulator fast-forward setting achieves these goals.

Keep this capability disabled in the default core. Use a small, tested build profile rather than many player settings. Any CGB-only implementation must declare that hardware requirement in a separate supported build; the baseline remains compatible with the original Game Boy.

## STATS view and return context

D26 requires one navigation contract across the existing STATS pages. Keep the selected Pokémon and selected page separate. A caller provides its data context, valid list, selection, scroll position, and return destination. A small page table is a proposal that lets a developer add a page without replacing the controls. The default retains the existing two pages; DV/stat EXP views remain extension examples.

The source has party, PC, battle, and trade callers. Preserve each caller's allowed data and action state. A common controller must not turn browsing into a transfer, release, battle switch, or trade choice. PC action menus currently overwrite shared list cursor state, so preserve browsing context before entering them. Protect the original medicine flow while changing shared menu helpers. See the [source audit](../research/menu-navigation.md) and [regressions](07-testing-ci.md#stats-and-menu-regression-coverage).

## Move INFO and optional battle information

Use one read-only move lookup for machines, known moves and learning offers. Pass the move ID and, for a known move, the correct party, box or battle slot. Display the active preset’s data and effect descriptions. The live type overlay is an independent author feature. [Controls and acceptance cases](15-battle-information.md)

## Optional item capacity

The accepted [item-capacity design](../research/bag-memory.md) puts the enabled bag in the separate 134-byte reserve at `$D66A–$D6EF`. Retain the original 42-byte bag footprint and all other existing field addresses, including the intervening `wGameProgressFlagsEnd` boundary. The selected 64-slot preset uses all 134 bytes: four format-marker bytes, a count, 128 entry bytes, and a terminator. Core keeps its original layout when disabled. Assign the entire reserve to the bag feature and reject overlapping enabled allocations. Verify the declared layouts for supported combinations, plus shared inventory and save routines. The RAM-only audit proves allocation fit and unchanged other WRAM addresses; it does not prove game or save compatibility. [E108](../research/evidence.md#e108)

The enabled bag and its format marker must be initialized after the existing game-progress clear. That clear includes the first 78 bytes of this reserve; initializing the bag earlier would lose its count and end marker. Preserve the original progress boundary and disabled behavior. [E109](../research/evidence.md#e109)

## Move-menu and box state

The current move-menu cursor and the move marked for swapping are separate states. A SELECT redraw must restore the cursor without committing an attack or changing remembered battle-history state. Keep the battle/party move and PP swap paths intact. [PN-021](13-playthrough-intake.md#pn-021)

Box insertions must use one destination index for the species list, full record, OT, and nickname. Append new captures and boxed gifts as deposits already do; update the existing nickname destination too. Preserve the packed array layout, count, terminator, and old saved-box order. This is independent of the later storage Extensions. [PN-022](13-playthrough-intake.md#pn-022)
