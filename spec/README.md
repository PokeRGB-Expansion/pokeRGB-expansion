# PokéRGB Expansion

**A shared base for making Generation I Pokémon ROM hacks.** Specification **0.1.48**, revised November 23, 2026. This repository contains the design and its evidence. Game features described below are planned unless a record gives a released game version.

## Charter

Build on the English Red/Blue engine so authors can make a small original-style hack or a new adventure. One source tree produces Red, Blue and Green. Red and Blue keep their version differences. Green uses Blue’s gameplay with its own presentation. The project targets English releases. [Upstream source](https://github.com/pret/pokered/tree/ba9c0568f64ae602fadda577a08c66639f93082a) · [Build variants](docs/06-build-variants.md)

Keep shared fixes, tools and commonly requested features in one place. An author chooses the rules when building their game. Changing an encounter or adding graphics should be easy with the original roster, trainer AI and battle system. The base should be worth choosing even when moving an existing hack requires a rewrite.

## Core, Minimal, and Extended

| Preset | What players can expect |
|---|---|
| **Minimal** | Keep the strength of each Pokémon, opponents’ choices, and the costs and preparation behind a strategy. Shorten the controls for actions the player can already take. An eligible Pokémon can Cut a tree from the map with the same badge, move and result as using the party menu. |
| **Core** | Keep Gen 1’s character and add selected corrections and usability improvements. Ghost beats Psychic, Gust is Flying and Charizard can learn Fly. Hyper Beam’s KO exception, ordinary critical hits, trapping and the single Special stat remain part of the game. |
| **Extended** | Start from Core and select additional features. Later species, types, battle information and alternative trainer AI can be developed and enabled independently where their data permits. |

Both Minimal and Core keep the twenty-slot bag and manual box selection. If the party and selected box are full, the player needs to make room or change boxes at a PC. Automatic placement, direct MOVE POKÉMON and move relearning are separate author choices. The [guide to game changes](docs/16-game-changes.md) explains what players see. The [build settings](docs/14-features-and-extensions.md) give the boundaries for each choice.

**Core is ready for the public when every accepted Core change works in Red, Blue and Green.** Internal builds can cover one system at a time. All three colors ship with the same Core feature set. The [release gate](docs/09-roadmap.md#public-release-checks) spells out what must pass. The [preset review](research/sweep-decisions.md) records what each change does for a player and the scope chosen for each preset.

### Developer features

An author can publish two editions of the same hack from one revision. A hypothetical Yellow Rogue could share maps and quests across a classic roster and an expanded roster, with one Special stat in both. [Emerald Rogue comparison and downstream example](research/emerald-rogue-builds.md)

A developer can keep stock battle rules, choose a different box policy or use later Pokémon without enabling every modern mechanic. Share routines that need to agree across builds. Enable costly storage and roster formats only for builds that use them. [Developer library](research/tutorial-library.md) · [Code changes by size](research/refactor-scope.md)

## Read the specification

| Document | Purpose |
|---|---|
| [Guide to game changes](docs/16-game-changes.md) | Player-facing differences, examples and how to document a change |
| [Move INFO and battle information](docs/15-battle-information.md) | Machine and move details, learn/forget controls, visibility and tests |
| [Core and extensions](docs/14-features-and-extensions.md) | Feature layers, catalog, developer choices, and storage examples |
| [Decisions](docs/01-decisions.md) | Settled requirements and their scope |
| [Architecture](docs/02-architecture.md) | Current engine, proposed boundaries, capacity and save design |
| [Bug-fix policy](docs/03-bug-fix-policy.md) | Evidence and review needed for a correction |
| [Bug triage](docs/04-bug-triage.md) | Priorities, precise defects, and the complete catalog intake |
| [Mechanics contract](docs/05-mechanics-contract.md) | Behavior the default core must preserve or correct |
| [Build variants](docs/06-build-variants.md) | Shared engine and cosmetic Green implementation |
| [Testing and CI](docs/07-testing-ci.md) | Regression cases, build checks, link tests, and release evidence |
| [Provenance](docs/08-provenance.md) | Source history, credit, notices, and distribution considerations |
| [Roadmap](docs/09-roadmap.md) | Complete Core release scope and acceptance criteria |
| [Remaining engineering work](docs/10-open-decisions.md) | Implementation choices, support evidence, and deferred research |
| [Research and corrections](docs/11-research.md) | Verified claims, earlier errors, and verification limits |
| [Adoption, maintenance, and contribution](docs/12-maintenance.md) | Launch plan, developer use, review workflow, upstream updates, and releases |
| [Playthrough findings](docs/13-playthrough-intake.md) | New reports, accepted safeguards, source checks, and implementation status |

## Maintain this foundation

Document every change from stock in the same update that introduces it. Give the player-facing result first. Link the reason, affected presets and test once. Use the [individual decisions](research/catalog-decisions.md) to see why other reported changes stay out. [Contributor and release process](docs/12-maintenance.md) · [Sources](research/evidence.md) · [Changelog](CHANGELOG.md)

Run `python3 tools/validate_spec.py` to check the documents and research records. The Git history tracks the specification. The project adds no blanket MIT license. [Provenance](docs/08-provenance.md)
