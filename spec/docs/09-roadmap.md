# Roadmap and acceptance criteria

Core and Minimal each ship English Red, Blue and cosmetic Green. Core v0.1.0 established the playable foundation. Both presets included the caught marker and battle EXP bar by v0.2.0. New releases keep the behavior, tests, source, patches and developer guide together. [Release history](https://github.com/PokeRGB-Expansion/pokeRGB-expansion/releases)

## What counts toward Core

Use the current decisions for each feature. Test each shared fix in both presets. An optional feature, a downstream example for an unbuilt capability, or an unadopted research lead does not become a Core requirement merely by appearing in the specification.

| What to include | Where the full requirements and tests live |
|---|---|
| Battle rules, deliberate data revisions and protected cartridge behavior | [Mechanics contract](05-mechanics-contract.md), [rule precedents](../research/core-rule-precedents.md), [battle and progression repairs](../research/core-scope-review.md), and [additional stock findings](../research/foundation-audit.md) |
| Menus, travel, encounters, rewards, capture, storage and safety | [Playthrough register](13-playthrough-intake.md), [individual repair records](04-bug-triage.md), [player-experience sweep](../research/player-experience-sweep.md) and [cross-system findings](../research/final-scope-audit.md) |
| Every accepted catalog item, including less conspicuous sound, text, hardware and map fixes | [94 case decisions](../research/catalog-decisions.md). For a split entry, include the part assigned to Core or to both presets. Include shared engine and safety work, and the applicable link rule in mixed link entries. Keep preserved or held behavior covered by its stated controls. |
| Reference games and author-facing delivery | [Build variants](06-build-variants.md), [developer features](14-features-and-extensions.md), [change guide](16-game-changes.md) and [maintenance requirements](12-maintenance.md) |

The [player-impact review](../research/sweep-decisions.md) gives the final placements for D61/D62. Include the accepted screens in the integrated Core release and test their normal entry and exit paths.

For each accepted item, record its implementation revision, test result and any affected save, link or hardware behavior. Link overlapping IDs to one implementation. A Core safety boundary needs a test at its supported limit. A report can be closed as inapplicable to stock only with evidence and a clear account of the supported developer case. An unimplemented accepted feature, a failing acceptance test or an unresolved choice that prevents testing keeps Core in development. Change a requirement explicitly if new evidence warrants it.

## Implementation sequence

1. **Reproduce the reference.** Build the pinned upstream source with RGBDS 1.0.4, verify the cartridge hashes and keep pristine test inputs. Run tests on compiled code with controlled initial state and gameplay rolls. Produce separate build objects for each color and configuration. The pristine reference build has matched all five upstream hashes. The buildable fork and GitHub Actions use the same tool version.
2. **Work in independently testable groups.** Start with cases that lose saved data, block normal play or corrupt a party member. Group battle fixes by the state they share. Test map and menu changes through their real callers. Document evidence for likely-intent corrections and chosen conveniences separately. A completed group is ready to integrate. Use a small classic/alternate example when testing paired-edition support. Core’s reference game and its public release do not depend on building a separate adventure or a wide roster.
3. **Test the whole game.** Build all three colors from the integrated source. Exercise starter selection, Gyms, Tower, Silph, Safari, fossils, League, postgame and saving. Include full inventories and boxes, a different trainer’s existing save, legal trades, map connections and cancelled actions. Compare Red/Blue differences and prove Green matches Blue wherever gameplay is concerned. [Test plan](07-testing-ci.md)
4. **Run the release check.** Compare the release candidate against every accepted Core record above. Publish only after all pass, the advertised hardware and multiplayer support match actual results, and a second developer can reproduce the builds and customize an encounter or trainer from the instructions.

## Current release scope

The v0.3 changes cover field menus, item and move information, and the Core-only gameplay fixes and services described in the [player guide](16-game-changes.md). Core’s Move Deleter, EXP. ALL switch and battle pace option each have a Minimal preservation check. A party-menu Move Reminder and per-Pokémon move histories belong to Extended. Work on Extended follows the Core and Minimal releases.

## Public release checks

- Every accepted Core behavior has evidence from the integrated game. A passing stock demonstration or an isolated prototype remains supporting evidence.
- Validate the original-style rules that Core protects. Exercise changed rules against neighboring cases. For example, Focus Energy’s improvement preserves ordinary critical odds, and Flying Gust changes Counter eligibility while retaining the original effect against Fly and Dig.
- Verify save, reset and supported link behavior. Test two endpoints in both roles for advertised link battles or trades. Publish the exact compatibility matrix. Keep the last valid save safe through cancelled operations. [Save and link tests](07-testing-ci.md#link-and-save-testing)
- Build all reference artifacts from a clean checkout. Verify the resulting hashes and apply the distributable patches to the documented inputs. Supply the version, selected settings and matching tests with each artifact.
- Publish the player change guide, source credits, known inherited quirks and an example that makes a small edit on the default base. A developer should be able to understand the changed behavior without reading assembly. [Release records](12-maintenance.md#release-record)

## Minimal, Extended and downstream editions

Each Minimal release must pass the Minimal equivalence checks. It keeps stock battle rules and resource limits, including the active-box limit, and shares the approved safeguards such as EXP. ALL protection. A developer can enable the implemented HUD options independently on either base. Extended is planned work. It builds on Core’s design and keeps unified Special as its starting point. Whole-generation rosters, extra types or a move-based damage category can be selected independently when their supporting code exists.

Provide a path for a downstream project to publish two editions of the same adventure. Share maps and scripts, name the two configurations, validate their content and produce separate, unambiguous patches. The hypothetical Yellow Rogue example is a test of the foundation’s authoring model. [Emerald Rogue prior art and build example](../research/emerald-rogue-builds.md)

Before large rosters ship, prove high species IDs through encounters, battle, evolution, storage, saves and any advertised link format. Measure cartridge space and performance for actual content. Develop optional storage, battle information, encounter generation or modern mechanics with their own acceptance tests. Features such as doubles or triples remain feasibility work. [Species design](../research/species-id-architecture.md) · [Feature inventory](14-features-and-extensions.md)

### Extended authoring milestones

Use a small two-edition Kanto adventure to test the foundation as a hack author would. Start with maps, events, trainers, learnsets and encounters. Then test switching independent features, authoring forms and crossing the first species-ID limit. Keep the two editions buildable as the engine changes. Each milestone has a playable acceptance check and a source for the design choice. [Author tasks and acceptance checks](../research/hack-engine-precedents.md#what-to-prove-in-extended)
