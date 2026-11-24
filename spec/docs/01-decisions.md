# Decisions and requirement scope

These are the settled product requirements. Historical claims are checked separately in [research](11-research.md). Engineering proposals are not silently promoted to requirements.

The consequence column explains how a requirement applies. Suggested names, tools, interfaces, and implementation order remain proposals. Specific baseline cases in the mechanics contract apply these requirements to the checked upstream behavior; they do not authorize a new gameplay rule.

## Settled decisions

| ID | Requirement | Consequence |
|---|---|---|
| D01 | Keep **PokéRGB Expansion** as the preferred working name. | The name communicates broad capability and ambition. Describe the configurable Gen 1 base clearly; a final naming decision remains open. |
| D02 | Base the game on `pret/pokered`. | Preserve a pristine upstream reference. Review individual fixes from other projects instead of importing a finished hack's ruleset. |
| D03 | Maintain one English Red/Blue engine. | Red/Blue behavior differences belong in explicit data or small version conditions. No separate battle-engine forks. |
| D04 | Green is a cosmetic Blue variant. | Green shares Blue’s gameplay and uses the v0.1.2 title layout in Minimal and Core. [Gameplay base](06-build-variants.md#build-identity) · [Title decision](06-build-variants.md#green-presentation-scope) |
| D05 | Keep defining Gen 1 behavior. | Protect Hyper Beam's KO exception, fixed-damage immunity bypass, the core critical-hit calculation, trapping, unified Special, sleep/freeze, and the original accuracy system. |
| D06 | Fix demonstrable defects. | Focus Energy/Dire Hit, misleading effectiveness output, factual text errors, and unambiguous spelling or typing errors qualify. Other candidates follow the same evidence policy. |
| D07 | Keep ordinary and high-critical-hit probabilities unchanged when Focus Energy is absent. | A patch that changes those rates is unsuitable even if its Focus Energy multiplier appears correct. |
| D08 | Keep the default game's original data and resource constraints. | Original types, type chart, move typings, species stats/learnsets, encounters, evolutions, trainers, maps, story, and items remain the baseline, subject to accepted repairs and documented safeguards. No arbitrary rebalance. |
| D09 | Use developer choices rather than a consumer-facing toggle maze. | Future optional systems are build features. Existing vanilla options can stay. No player switch between a corrected and broken Focus Energy. |
| D10 | Build a foundation attractive enough to justify adoption. | Existing hacks may need substantial rewrites. Do not keep harmful internal structures merely to promise painless migration. |
| D11 | Consolidate expansion support over time. | Later species, Dark/Steel, Fairy, later mechanics, and forms such as Mega Evolution are legitimate future work. They do not enter the default core automatically. |
| D12 | Develop in small, testable steps. | Use internal milestones to isolate failures and review changes. D57 sets the single public Core acceptance gate. |
| D13 | Require rigorous regression evidence for battle changes. | Source review alone does not establish that an implemented game works. |
| D14 | Add no project-wide MIT license. | Keep provenance and applicable notices. Do not describe the entire derived codebase as MIT-licensed. |
| D15 | Exclude uncertain changes from the default core. | Retain existing behavior when a proposed correction's evidence or fit is unclear. Defer the change; a later developer extension can offer an alternative without changing the baseline. |
| D16 | Serve small, original-style hacks and ambitious Gen 1 projects equally well. | Common improvements are reusable developer choices. Using the foundation or one optional system must not force later-generation species, types, or unrelated rules into a game. Real dependencies must be explicit. |
| D17 | Keep optional engine behavior separate from the default contract. | Improved trainer AI and a replacement random-number generator must be separate developer choices, disabled by default. Unrelated features must work with the default choices. Accepted defect repairs still follow the core policy. |
| D18 | Treat developer adoption and public visibility as core success goals. | Plan release communication, working examples, and an easy build/edit path alongside implementation. Track independent developers using and contributing to the base. |
| D19 | Protect the one-time EXP. ALL reward in Minimal and Core. | The Bag and item PC refuse to toss it. Shops use the existing important-item sale refusal. The item PC still allows deposit and withdrawal. RGB-017 defines each preset’s experience awards. An author option may be useful when it is straightforward to maintain. The shared safeguard ships by default. |
| D20 | Include SELECT item registration in the default core. | Register one eligible key item for direct overworld use. Bicycle use is required, with existing ownership and use restrictions. Preserve SELECT's menu functions. |
| D21 | Allow box browsing with a full party. | Bill's PC WITHDRAW opens the current box list and allows STATS. Check party capacity only when WITHDRAW is chosen for a selected Pokémon, before changing party or box data. Use the existing error text. Leaving STATS or cancelling a selected-Pokémon action restores the browsing list and its selection/scroll context in the existing WITHDRAW/DEPOSIT browsing flows. |
| D22 | Keep developer choices independent. | Automatic capture placement, direct MOVE POKÉMON and larger box capacity are separate choices. D55 sets their reference defaults. |
| D23 | Preserve meaningful Gen 1 constraints and choices when improving the interface. | Retain the 20-slot bag and inventory management in Core. Assess the effect on play rather than calling a change basic usability. Original designer intent must not be claimed without evidence; preserving a constraint is a project choice. |
| D24 | Include contextual HM use in Core. | Press A at a suitable target and confirm use, without navigating the party menu. Cut trees, Surf water, and Strength boulders are required cases. Keep the party's learned-move requirement, move-slot cost, badge requirements, and existing use restrictions. |
| D25 | Correct the Thunder/Soul badge stat mapping in Core. | Thunder boosts Speed; Soul boosts Defense, matching the original English descriptions and the best-supported intent inference. Preserve the bonus amount, rounding, cap, other badges, link exclusion, and badge stacking. |
| D26 | Include directional STATS navigation in Core. | Up/down changes the Pokémon within the available list; left/right changes page; B returns to the browsing context. Keep the existing default information. Support additional developer pages without replacing these controls. |
| D27 | Make Pokémon release confirmation safe by default. | Show the selected nickname and species, default to No, and require an explicit Yes before removal. B or No returns without changing data. Apply this to release rather than changing all Yes/No prompts. |
| D28 | Preserve shopping context after a refusal or failed purchase. | Unsellable items return to the SELL list; insufficient money or bag space returns to the BUY list. Keep selection and scroll context, refusal messages, prices, capacity rules, and transaction checks. |
| D29 | Make overworld Pokémon action-menu CANCEL match B. | Both return to the party list with the same Pokémon selected. Preserve B from the party list to Start, existing actions, and other menu callers. |
| D30 | Correct the accepted small transaction and feedback defects in Core. | Use the selected vending price; preserve a rooftop drink when its TM cannot be delivered; report Flute wake-ups accurately; remove the false Raichu evolution claim. Keep prices, effects, trades, and evolution rules. PN-010–PN-012 and PN-015 define the boundaries. |
| D31 | Show the current elevator floor and prevent false travel. | Indicate the entered floor; selecting it cannot play travel animation/sound or change destination state. Prefer disabling/skipping that entry; preserve other destinations and cancellation. PN-013. |
| D32 | Support left/right quantity changes of ten in Core. | Preserve up/down unit steps and wrapping, action confirmation, cancellation, limits, and transaction checks. Endpoint clamping is the proposed design. PN-014. |
| D33 | Offer live type indicators as an independent developer option. | D61 places the player’s static move reader in Minimal and Core. The separate live type overlay stays off in both. [Controls and visibility](15-battle-information.md) |
| D34 | Preserve position when returning to the same item list. | Keep selection and scroll after item-PC deposit/withdraw/toss, bag use/toss, and shop buy/sell returns, including cancellation and refusal. If a stack disappears, select its successor or the preceding item when it was last. Clamp only as needed; keep existing menu destinations, constraints, and transaction rules. PN-019. |
| D35 | Offer larger item capacity as a developer Extension. | Disabled in Core, which keeps bag 20 and item PC 50 slots. Use the 64-slot bag preset as the selected target, keep PC capacity separate, retain per-stack limits and item rules, and verify allocation, saves, and menus before advertising support. PN-020. |
| D36 | Store the optional larger bag in the separate unused 134-byte reserve. | Relocate only the live bag; retain its original 42-byte footprint and all other existing field addresses and block boundaries. Give the reserve one owner and check feature combinations for overlap. Select 64 slots: four format-marker bytes, count, entries, and terminator use all 134 bytes. Core limits remain unchanged. Save and runtime support still require tests. PN-020; E108. |
| D37 | Retain the battle move cursor through SELECT swaps. | Marking a move and completing a swap keep the current row. Preserve source markers, complete move/PP swaps, Disable tracking, battle history, and existing A/B/link rules. PN-021. |
| D38 | Append new boxed Pokémon consistently. | Captures and gifts sent to the current box append, matching deposits. Keep prior members in place and every record component aligned; preserve storage limits, acquisition checks, and saved-box layout. This is a usability policy with original intent unverified. PN-022. |
| D39 | Correct the Mansion Burglars' passive sight behavior in Core. | Treat their zero range as a likely oversight and enable normal sight-triggered battles for these three trainers. Range one is the proposed target, supported by the remake comparison. Preserve Scientist settings, other zero-range trainers, and the remaining trainer and map data. This scoped decision supersedes PN-023's earlier preservation choice; original intent remains unproven. |
| D40 | Correct star-grass encounter recognition in Core. | Make the affected Viridian Forest grass squares eligible under the existing encounter rule. Preserve rate data, species, levels, slot weights, Repel rules, graphics, map layout, and ordinary safe paths. Keep the separate shore case explicit. Original intent remains unproven; code choice and regression checks remain engineering work. PN-024; E115. |
| D41 | Restore the Acid Armor sprite at the end of the animation in Core. | Keep the original melt and sound. Restore the sprite that was on screen when the melt began, including a transformed Pokémon, Minimize sprite, or Substitute doll. Preserve the move's mechanics and the battle animation setting. [PN-025](13-playthrough-intake.md#pn-025) |
| D42 | Keep original trainer decisions and battle difficulty as the Core starting point. | D44 supersedes the earlier placement of Blaine's potion guard in an Extension. Other changes to trainer decisions still need individual review. |
| D43 | Include both battle STATS redraws, the move-replacement sound and the empty SHIFT prompt repair in Minimal and Core. | The next opposing species still appears before the next legal decision. Offer SHIFT normally if any living reserve can enter. [Stock and prototype turns](../research/player-experience-sweep.md) |
| D44 | Correct Focus Energy, Dire Hit and Blaine’s full-HP potion use in Core. | Preserve the critical-hit calculation outside the pumped effect and keep Blaine’s other item rules. These repairs have the same release status as the rest of the accepted Core. |
| D45 | Maintain Minimal, Core and Extended in one source tree. | Minimal keeps the original battle rules and resource limits, shares the safeguards approved for it, and can include equivalent action shortcuts under D54. Core adds the accepted rule corrections. Extended supports additional choices. |
| D46 | Fix Transform targeting in Core. Preserve Swift hitting during Fly and Dig. | Transform contains a failure test for the exact state but reads the wrong value on both sides. Swift has a separate early success path. Minimal keeps both cartridge behaviors. Extended inherits Core as its starting point. [Evidence and intent](../research/core-scope-review.md#transform-and-swift) |
| D47 | Use named build presets and developer overrides in one source tree. | Keep content edits, optional rules, data formats, colors and debug mode separate. Reference presets get reproducible builds and tests. [Developer library](../research/tutorial-library.md) |
| D48 | Keep data choices independently configurable. | D50 supersedes the former shared Minimal/Core defaults for Ghost versus Psychic, Gust and Charizard. The other Yellow machine changes and Fighting Karate Chop remain developer selections. |
| D49 | Design for a wider roster and keep the compact format in standard builds. | Introduce two-byte species IDs before importing whole generations. Test save and link formats and capacity independently. [Measured design](../research/species-id-architecture.md) |
| D50 | Put Ghost → Psychic at 2×, Flying Gust and Charizard’s HM02 eligibility in Core. | Minimal retains all three stock values. Karate Chop and Sand-Attack stay Normal in both. Extended inherits Core with independent author overrides. Change only the chart row, move type and HM permission. [Reasons and tests](../research/core-rule-precedents.md) |
| D51 | Define safe routing for an arrival that can use PC storage. | D55 supersedes the earlier Core default. With the option enabled, try the party, selected box, then each remaining box once, keeping the selected box and save point. [Feature contract](../research/box-overflow-contract.md) |
| D52 | Offer target-based HM prompts with the stock eligibility checks. | D54 enables these prompts in both Minimal and Core. Keep Fly and Flash in the menu. [Field contract](../research/field-shortcut-contract.md) |
| D53 | Preserve the last saved game when a box selection is cancelled. Show box occupancy without modifying saved data. | Apply both safeguards to Minimal and Core. The normal confirmed box change still saves. [Stock reproduction and controls](../research/box-picker-safety.md) |
| D54 | Minimal preserves team strength, opponents, preparation and meaningful choices. | Include equivalent controls such as A-button Cut, Surf and Strength. Keep the original move, costs, availability, progression and battle results. Ordinary differences in time spent in menus are acceptable. [Placement and tests](../research/minimal-action-review.md) |
| D55 | Keep manual box selection in both Minimal and Core. | Automatic placement is a supported feature direction, off by default and independently selectable on any compatible preset. A full-box message and the box chooser can help players without granting a catch. A relearner is also optional. [Evidence](../research/storage-policy-and-code.md) |
| D56 | Share the code that enforces the same rule. Isolate work needed only by an option. | Use one field-action path and reusable destination and record helpers as needed. Preserve the compact box/save format on the manual path. Document every upstream difference and its first game release. [Engineering scope](../research/refactor-scope.md) · [Change guide](16-game-changes.md) |
| D57 | Release the complete agreed Core to the public. | All accepted Core and shared fixes, developer documentation and reference colors pass the [release gate](09-roadmap.md#what-counts-toward-core). Independent internal tests and prototypes are steps toward that release. |
| D58 | Support downstream paired editions from one source revision. | Treat edition, color and engine preset as separate choices. Test shared content and edition differences. Keep unified Special as the starting point in both classic and expanded Gen 1 games. [Worked example](../research/emerald-rogue-builds.md) |
| D59 | Apply Minimal’s equivalence rule to information, menus and shared repairs. | D61 includes static facts about the move being considered, even if stock requires a guide or a purchase to identify it. Preserve prices, move choices and battle outcomes. Treat concealed battle state and proactive reminders separately. |
| D60 | Preserve the original Day Care and Game Corner clerk in Minimal and Core. | Keep the Day Care’s move order, fee, and deposit and pickup dialogue. Keep the clerk’s price, cap, acceptance rule and speech. A player starting with zero coins can buy every coin needed for Red’s Porygon. [Day Care comparison](../research/day-care-history.md) · [Prize checks](../research/game-corner-redemption.md) |
| D61 | Include move INFO before acquisition, learning, replacement and use. | Minimal and Core show machine numbers and names and share one read-only move reference in the bag, PC, shops, prize lists, STATS, FIGHT and learning prompts. Extended inherits it. [Move INFO](15-battle-information.md) |
| D62 | Adopt the reviewed usability placements. | Both presets show storage counts, carried quantity at a Mart and PP in the item target list, remember the session’s Pokédex row and correct false coin-spill feedback. Only Core gives the proactive selected-box-full notice. [Placement and player effects](../research/sweep-decisions.md) |
| D63 | Show owned status and active EXP progress during battle in Minimal and Core. | Each display is a separate author choice. Preserve concealed encounters, the original reward and the existing turn and message flow. [Rules and tests](../research/battle-hud-displays.md) |

Both presets retain Bug↔Poison at 2×, Fire’s lack of Ice resistance, Toxic/Leech Seed, and the ordinary 1/256 accuracy failure. The [mechanics contract](05-mechanics-contract.md) specifies the scoped differences.

The [pre-build review](../research/foundation-audit.md) applies these decisions to individual reports. Each [catalog entry](../research/catalog-decisions.md) identifies its preset and required tests.

## Decisions with a narrower scope

**Focus Energy uses the rule selected in Q01.** Multiply the stock move threshold by four after the ordinary or high-critical calculation and cap it at 255. Minimal retains the cartridge bug. [Model and prototype](../research/critical-hit-analysis.md)

**Badge bonuses and badge stacking stay in the default core.** A stacking correction can be a later developer option. It is not an unresolved core choice or a release gate. D25 changes only the Thunder/Soul mapping to match the original descriptions. Preserve stacking with the corrected badge-to-stat assignment.

**Preserve a mechanic without claiming perfect vanilla compatibility.** Accepted fixes change some battle outcomes. The reference game is neither a byte-identical preservation build nor a promise of exact competitive RBY compatibility.

**Later generations describe capability, not an immediate roster commitment.** No fixed promise to ship every species from a numbered generation, including an unreleased or incompletely defined generation, is made here.

## Outside the default core

Do not add solo access to all 151 species, new trade-evolution rules, reusable TMs, extra field-move slots, running shoes, faster battles, difficulty modes, new Pokémon typings, revised trainers, or new story content as incidental bug fixes. Some may later become developer systems. A finished remaster built on this foundation can choose them deliberately.

The named exceptions are recorded in D50. Other chart rows, move typings and machine permissions retain the original values unless a developer selects an alternative.

## Decision changes

Record the old requirement, new requirement, reason, compatibility effect, and affected tests. A maintainer can decide routine implementation details within these requirements. Record a new feature idea as a proposal until the project adopts it. A test that demonstrates a behavior establishes what the game does. It does not by itself establish that players benefit from changing it.

### Badge mapping correction — 2026-10-14

- Previous requirement: retain Thunder→Defense and Soul→Speed, and change their descriptions.
- Current requirement: Thunder→Speed and Soul→Defense. Keep the original English gym and badge-house descriptions.
- Reason: the original dialogue, original US manual, and later FireRed/LeafGreen calculation all point to the descriptions as the intended mapping. This supports correcting the code. Original intent cannot be established with certainty from the available evidence. Other hacks use different approaches. See the [evidence review](../research/badge-intent.md).
- Compatibility effect: ordinary single-player Speed/Defense bonuses change. Turn order and damage can therefore change. The original bonus amount, rounding, cap, other badges, link exclusion, and repeated-boost behavior remain protected.
- Required tests: isolated and combined badge bits, either acquisition order, rounding/cap boundaries, repeated boosts and stat changes, original text, unchanged Attack/Special bonuses, and no badge boosts in link battles.

### Scoped menu behavior — 2026-10-14

D21 now includes returning from PC STATS and selected-Pokémon cancellation to the browsing list. D26 and D27 accept STATS navigation and safer release confirmation. Preserve medicine's existing return-to-bag behavior; repeated targeting is not a Core requirement. Repel renewal is an optional developer extension and stretch goal, disabled by default. Additional menu-return changes require separate review of the exact action and destination. See the [inventory](../research/menu-navigation.md).

### Shop return behavior — 2026-10-15

D28 accepts the previously reviewed shop cases as Core behavior. This changes the destination after a refusal or failed purchase, retaining the item list and its selection/scroll context. Empty SELL lists still use their existing response and return to the main shop menu. Party action-menu cancellation is covered separately by D29. See [PN-008](13-playthrough-intake.md#pn-008) and the [menu inventory](../research/menu-navigation.md).

### Party action cancellation — 2026-10-15

D29 accepts returning from CANCEL to the party list in the overworld Pokémon action menu. Match B and retain the selected Pokémon. This is a scoped interface repair; the original source confirms the different destinations but does not establish their design rationale. See [PN-009](13-playthrough-intake.md#pn-009).
