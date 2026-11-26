# PokéRGB Expansion

**Core and Minimal each build English Red, Blue and Green.** To see what changes in play, start with the [player guide](docs/16-game-changes.md). To make a hack, start with the [build instructions](../README.md#build) and [first three edits](../README.md#make-your-first-hack).

These documents track the game source. The [changelog](CHANGELOG.md) lists game releases separately from the earlier specification revisions, which ended at 0.1.48. The research files retain the measurements and alternatives behind each decision.

## Charter

Give hack authors a dependable Red/Blue engine for both small edits and new adventures. Preserve the original version differences and the single Special stat. Green uses Blue gameplay with its own title, palette and border. A developer should have reason to choose this foundation even when adopting it requires a rewrite. [Upstream source](https://github.com/pret/pokered/tree/ba9c0568f64ae602fadda577a08c66639f93082a) · [Build variants](docs/06-build-variants.md)

## Core, Minimal, and Extended

| Preset | Scope |
|---|---|
| **Minimal** | Preserves battle rules, team-building costs and progression choices. Includes accurate feedback, save safeguards and shortcuts to actions the player already qualifies for. |
| **Core** | Fixes documented bugs and adds selected conveniences. It fixes Focus Energy, keeps original critical-hit and trapping rules, and offers a Fuchsia Move Deleter, field EXP. ALL switch and optional Quick battle pace. |
| **Extended** | Planned developer features include larger rosters, additional types, and a Move Reminder in the party menu that remembers moves each Pokémon has learned. There is no Extended build target. |

Both released presets keep the twenty-slot Bag and manual box selection. An author can independently select the two [battle displays](research/battle-hud-displays.md). Automatic box overflow, direct box-to-box moves and wide species IDs remain future options. [Feature catalog](docs/14-features-and-extensions.md)

### Developer features

One source tree supports paired editions. The proposed Yellow Rogue example describes how a future author could share maps and quests across a classic and an expanded roster. [Paired-edition example](research/emerald-rogue-builds.md) · [Developer library](research/tutorial-library.md) · [Changes by size](research/refactor-scope.md)

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

From the repository root, run `python3 spec/tools/validate_spec.py` to check the documents and research records. The Git history tracks the specification. The project adds no blanket MIT license. [Provenance](docs/08-provenance.md)
