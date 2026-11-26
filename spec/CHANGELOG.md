# Specification changelog

## Game release 0.4.1

- Compare TMs at a Mart or the Game Corner with Up/Down. Keep the stats, effect or party view open while browsing. A opens one read-only screen for the whole party, with the move and its price. B returns to the last inspected offer. The move name and START hint now replace the previous prompt cleanly. [Controls](docs/15-battle-information.md#before-buying-a-tm)

## Game release 0.4.0

- Inspect a TM’s type, power, accuracy, PP, effect and its compatibility with each party member before buying it or spending Game Corner coins. Bill’s PC can preview the contents of a highlighted box before saving or changing boxes. [Player guide](docs/16-game-changes.md)
- Authors can give one trainer Pokémon its own moveset in either preset. [Trainer example](research/tutorial-library.md#give-one-trainer-pokémon-a-custom-moveset)
- Core’s Route 15 aide explains how sharing benefits conscious teammates that sat out. [EXP. ALL](research/exp-pacing-and-move-services.md#exp-all-in-the-bag)

## Documentation after v0.3.0

The [player guide](docs/16-game-changes.md) explains preset differences and the [README](../README.md#play-a-release) shows which patch to use. The [feature review](research/v030-core-candidates.md) records proposals for the next round.

## Game release 0.3.0 — 2026-11-26

- All six public patches reproduced the tested builds byte for byte. All 18 release checks passed. [Downloads and checksums](https://github.com/PokeRGB-Expansion/pokeRGB-expansion/releases/tag/v0.3.0) · [CI run](https://github.com/PokeRGB-Expansion/pokeRGB-expansion/actions/runs/45791157984)
- The [player guide](docs/16-game-changes.md) covers the shared field, menu and battle improvements and Core's EXP. ALL switch, Fuchsia Move Deleter and Quick battle pace.
- D65 and D66 settle the new preset choices and defer individual move history to Extended. Historical research records retain the alternatives and original reproduction steps.

## Earlier game releases

- v0.2.0 added the caught marker and battle EXP bar to both presets. [Display rules and tests](research/battle-hud-displays.md)
- Protect the one-time EXP. ALL reward from tossing and selling in Minimal and Core. Core calculates the two experience shares independently under RGB-017. Minimal keeps the original awards.

## 0.1.48 — 2026-11-23

- Adopt static move INFO in Minimal and Core for machines, known moves and new moves before replacement. Include pre-purchase inspection and keep live opponent types optional.
- Settle the other display placements, document exact hidden-coin outcomes, and verify when the stock level-up routine writes a move.

## 0.1.47 — 2026-11-23

- Trace the last preset review to the earlier decisions. Separate new interface suggestions from release requirements and document their effects on spending, preparation, move choices and navigation.
- Distinguish decisions needed to start Core from Green artwork and compatibility evidence needed before publication.

## 0.1.46 — 2026-11-23

- Keep the original Game Corner clerk in Minimal and Core. Verify that a player starting with zero coins can buy and redeem Porygon in Red and Blue. Green follows Blue.
- Keep the original Day Care dialogue and move order in both presets. Retain the original PC and Day Care deposit choices. Record how FireRed and other games handle the same case.

## 0.1.45 — 2026-11-23

- Set one public gate for the complete Core. Review all archived bug placements, playthrough decisions, usability cases and authoring topics under the Minimal rule.
- Add the downstream paired-edition design, settle the machine and capacity displays, and record new coin, Day Care, Pokédex and box feedback cases.
- Select the Focus Energy rounding and cap order, and add evidence from compiled threshold, shop, battle, map and presentation tests.

## 0.1.44 — 2026-11-23

- Include equivalent field and menu shortcuts in Minimal. Keep team strength, move access, resource limits and strategic preparation intact.
- Keep manual boxes in Minimal and Core. Document what can be shared across builds, what automatic placement must add, and what the prototype actually verified.
- Add a concise guide to game changes and regression cases for SELECT, Counter, received moves and two different save operations.

## 0.1.43 — 2026-11-22

- Apply the badge precedent to Ghost versus Psychic and Gust, adopt Yellow’s Charizard/Fly permission in Core, and keep Karate Chop Normal. Record stock and prototype battle outcomes.
- Define Core overflow placement and overworld HM shortcuts. Minimal keeps manual captures and field commands. Direct MOVE POKÉMON remains a developer option.
- Record a reproduced prior-save loss from cancelling the first box change, a tested correction, the box occupancy display requirement and the refused Surf dismount fix.

## 0.1.42 — 2026-11-22

- Compare the retail Red/Blue and Yellow tables, original manuals and cartridge behavior for disputed learnsets and type rules. Record optional data settings and three shared presets.
- Add focused field, text and Pokédex corrections from the Yellow and donor reviews. Map upstream tutorial subjects to author tools, defaults and options.
- Record measured party, box and link format costs for wide species IDs. Keep compact builds and define the gates for large rosters.

## 0.1.41 — 2026-11-22

- Give all 94 archived reports a preset decision, reason and test. Record the transaction order at 47 gift sites and the scope of 66 usability findings.
- Add 36 stock Red/Blue battle cases covering EXP. ALL, draining moves versus Substitute, Rest, Transform move swaps and Sabrina’s scoring. Add checks for damage arithmetic, map data and supported link rules.
- Record the accepted Core repairs, developer options and the specific evidence needed for deferred cases.

## 0.1.40 — 2026-11-22

- Record the Core scope review, including the accepted Transform target check and the reason Swift preserves its original targeting. Add Core repair scopes and correct the neutral-AI proposal.
- Add 58 stock-ROM battle cases, the Vermilion Gym switch-table analysis, and the distinction between a ghost picture repair and a Pokédex progress change.

## 0.1.39 — 2026-11-22

- Advance the implementation base to the November 14 pokered revision. Verify the four audited source paths, RAM symbol addresses, and all five upstream build hashes. Keep historical evidence tied to the revisions originally checked.

## 0.1.38 — 2026-11-22

- Include Focus Energy and Blaine’s healing correction in Core. Record the later Minimal preset and the Extended feature scope. Add per-preset review and test criteria.
- Verify the clean upstream build and record the remaining Core release checks.

## 0.1.37 — 2026-11-22

- Keep original trainer AI and battle difficulty as the default. Leave Blaine's full-HP potion use in Core and put the proposed guard in a developer-selected trainer AI extension. D42 keeps earlier scoped corrections in force.
- Accept four survey fixes in Core under D43. Correct both battle STATS redraws and the move-replacement sound. Skip the SHIFT prompt when no reserve can enter. Implementation and patch tests are pending.

## 0.1.36 — 2026-11-22

- Compare Gen 1 fixes across 18 projects. Record 35 stock-ROM checks and five Core recommendations for battle display, move replacement sound, the SHIFT prompt, and Blaine's potion use. These are candidates for review.

## 0.1.35 — 2026-11-22

- Accept D41/PN-025 in Core. Keep Acid Armor's original melt and restore the same sprite at animation end. Preserve the move's mechanics. Implementation and regression tests are pending.

## 0.1.34 — 2026-11-22

- Record when the Acid Armor picture returns in stock Red, Blue, and Yellow. STATS can reload the enemy picture while its Defense boost remains. Haze can remove the boost while the picture stays blank.
- Recommend a scoped Core display repair in PN-025. Keep the original melt and restore the same picture at animation end. Game code and patch tests are pending.

## 0.1.33 — 2026-11-22

- Record Acid Armor's disappearing picture and 66 stock-ROM checks in PN-025 and E116–E118.
- Retain the shipped animation in Core under D15. Record later official animations, donor alternatives, and a possible developer option.

## 0.1.32 — 2026-10-25

- Accept D40/PN-024: correct star-grass encounter recognition in Core while preserving the existing rate and encounter tables.
- Keep original intent unproven and the separate shore case explicit. Code choice and regression checks remain engineering work; no game implementation is included.

## 0.1.31 — 2026-10-25

- Confirm the star-grass encounter mismatch in CAT-028/PN-024, with E115 and a map audit. Recommend a scoped Core recognition repair.
- Check Yellow's corrected corner against identical Forest map and blockset data. Keep historical intent separate from source facts.
- Record repair boundaries and future regression cases; no game implementation or runtime test is included.

## 0.1.30 — 2026-10-25

- Accept D39: correct sight engagement for the three Mansion Burglars in Core, superseding PN-023's earlier preservation disposition.
- Propose range one, following the remake. Preserve Scientists and unrelated zero-range trainers; require sight, wandering movement, route-safety, and post-battle tests.
- Treat the behavior as a likely oversight while keeping original intent unproven. Existing source evidence is unchanged; no game patch or runtime check is included.

## 0.1.29 — 2026-10-25

- Add E114 and the Route 21 geometry record: all four Fishers stand at the water's edge and face adjacent water.
- Qualify the Fisher analogy. Their fishing context does not establish Mansion Burglar intent; keep that intent unresolved.
- Preserve PN-023 and all other Core/Extension decisions. No game code or encounter setting changes.

## 0.1.28 — 2026-10-25

- Add E113: ordinary zero-range trainers in Red/Blue and Gold/Silver, unchanged Mansion ranges in Yellow, and range-one Burglars in FireRed/LeafGreen.
- Distinguish likely encounter intent from proof. The source setting alone does not settle intent; the remake may reflect a correction or redesign.
- Keep PN-023 and all other Core/Extension decisions unchanged. No game change or runtime comparison is included.

## 0.1.27 — 2026-10-24

- Accept PN-021/D37: keep the battle move cursor on its current row when SELECT marks or swaps moves. Preserve move/PP/Disable data and battle input rules.
- Accept PN-022/D38: append new captures and boxed gifts, matching deposits and retaining existing box positions and storage limits. Treat this as a usability policy with original intent unverified.
- Record PN-023: preserve the Mansion's zero-range Burglars and positive-range Scientists. All four maps retain the normal trainer sight routine.
- Add E110–E112, a focused source review, three coverage cases, and MN16. No game patch or runtime regression is included.

## 0.1.26 — 2026-10-23

- Select 64 slots for the optional bag, using the full 134-byte reserve with its four-byte format marker. Keep the surrounding layout and Core limits fixed.
- Update acceptance cases to 63/64/65 entries and require exclusive reserve ownership across enabled features.
- Add E109: initialize the expanded bag after the existing game-progress clear. Allocation and source checks do not establish gameplay, save conversion, or feature-combination support.

## 0.1.25 — 2026-10-23

- Accept D36: put the optional larger bag in the separate 134-byte reserve while retaining its original footprint and all other field addresses. Keep the 60-slot working preset and unchanged Core limits.
- Require single reserve ownership, overlap rejection, and checks of supported feature combinations. Retain explicit save/import requirements.
- Add E108, a repeatable RAM-only allocation audit, and recorded 60/64/65 boundary results. Allocation evidence does not establish gameplay or save compatibility.

## 0.1.24 — 2026-10-20

- Record optional item-capacity expansion with a 60-slot bag target; keep PC capacity separate and Core at bag 20/PC 50.
- Add E107 for the upstream relocation tutorial, original allocation/save boundaries, and derived 122-byte fit. Distinguish the preset from a universal engine maximum.
- Specify disabled-layout preservation, reserve ownership, save compatibility, and capacity/caller tests. No game implementation or configured build is included.

## 0.1.23 — 2026-10-20

- Accept PN-019/D34/MC40: retain item-list position after actions and temporary prompts; choose the adjacent entry safely when a stack disappears.
- Confirm shared full-stack row/scroll resets and shop row resets in E106 at the retained Red/Blue pin. Distinguish correct return destinations from position preservation.
- Extend menu cases without changing medicine flow, successful Pokémon-transfer destinations, inventory constraints, or transaction rules. No game patch or runtime regression is included.

## 0.1.22 — 2026-10-15

- Record accepted vending, Flute-feedback, trade-text, elevator, and quantity requirements; add the rooftop drink/TM payment-loss repair.
- Trace exact rooftop failure conditions and distinguish lost payment from the unverified duplication claim. Extend the gift screen to expose payment-order review.
- Defer contextual Flute use at Snorlax outside Core. Record TM information and capacity counts as supported proposals with scope still to settle.
- Add source-backed remake comparisons and independent optional battle type/move-information contracts for original Game Boy controls.
- Add E101–E105 and separate current Expansion/Gold references, retaining existing pins. No game implementation or runtime tests are included.

## 0.1.21 — 2026-10-15

- Add a broad small-fix and usability audit with 57 coverage cases and all 47 direct script gift-call sites.
- Add E88–E100 for reward, purchase, delivery, text, sound, feedback, display, control, and progression findings; source-confirm six archived leads.
- Separate correction recommendations and usability proposals from accepted scope. Source revisions and settled mechanics are unchanged.
- Record exact limits: coin conversion also changes the reported amount, vending underflow clamps to zero, and Flute omits a wake-up message rather than literally reporting no effect.

## 0.1.20 — 2026-10-15

- Accept D29/PN-009: overworld Pokémon action-menu CANCEL returns to the party list, matching B and retaining the selected Pokémon.
- Record focused acceptance cases and protect the normal party-list exit, actions, and other callers.
- Close MN04's review state. The original reason for its different return paths remains unknown.

## 0.1.19 — 2026-10-15

- Accept PN-008 / D28: return unsellable items to SELL and money/space purchase failures to BUY, preserving selection, scroll, messages, and transaction rules.
- Add focused regression and release criteria for those shop returns.
- Explain the party action-menu CANCEL/B difference with a concrete path. Keep that separate case under review.

## 0.1.18 — 2026-10-14

- Accept Core STATS controls: up/down for Pokémon, left/right for pages, B to the browsing context; support later developer pages while retaining default information.
- Extend PN-003 to restore the PC list and selection/scroll context after STATS or selected-Pokémon cancellation. Record the precise original return path.
- Accept safer release confirmation with nickname/species and a No default. Preserve medicine's return-to-bag flow.
- Record Repel renewal as an optional extension and stretch goal. Audit selected menu returns individually; additional party/shop candidates remain unapproved.

## 0.1.17 — 2026-10-14

- State D25's reason explicitly: dialogue, the original US manual, and FireRed/LeafGreen point to the descriptions as intended, while certainty is unavailable from the checked evidence.
- Include unambiguous typos in Core. Record Oak's geting→getting correction as PN-005 / RGB-010c.
- Verify the rating text, owned-species selection, and shared display callers. Require a layout check; no game patch is implemented.

## 0.1.16 — 2026-10-14

- Accept the Core code correction Thunder→Speed and Soul→Defense, matching original descriptions. This replaces RGB-010a's text-only policy.
- Preserve badge amount, rounding, cap, other badges, link exclusion, and original stacking. Add focused regression and release criteria.
- Verify four hacks at their current pinned branch heads: PureRGB fixes code, Shin Lite fixes text, and Solus/Solid Red retain the mismatch. Do not infer a community majority or import unrelated donor changes.

## 0.1.15 — 2026-10-14

- Add the original US manual and Prima badge descriptions, plus a pinned FireRed/LeafGreen calculation comparison.
- Separate verified mappings from the likely original intent and explain what a matching reconstruction can establish.
- Clarify that RGB-010a preserves shipped mechanics by correcting text. Remove the unsupported word “intended” from MC15; no Core stat swap is approved.

## 0.1.14 — 2026-10-14

- Require EXP. ALL sale refusal explicitly alongside bag/PC toss protection in PN-001 and the default contract.
- Reuse the shop's existing important-item refusal message, with no transaction or item/money change.
- Verify the zero price, key-item flags, shop checks, removal path, and refusal text. Record focused sale regressions.

The existing key-item flag proposal covers both protections. No game patch or executable shop test is implemented.

## 0.1.13 — 2026-10-14

- Define Core inclusion by effects on meaningful constraints and choices, rather than the label basic usability or the size of a change.
- Retain the 20-slot bag and inventory management, with source evidence separate from unverified original-intent claims.
- Accept contextual HM prompts in Core, with Cut trees, Surf water, and Strength boulders as the required cases.
- Record shared move/badge/map checks and focused regression requirements in PN-004. Keep move-slot costs and manual field use.

No game shortcut or inventory change is implemented. MOVE POKÉMON and capture overflow remain independent optional extensions.

## 0.1.12 — 2026-10-14

- Define Core and Extensions as the two feature layers, with a central feature guide and catalog.
- Keep the three accepted basic safety/usability features in Core. Treat QoL as a description, not an inclusion rule.
- Accept MOVE POKÉMON and automatic capture storage in another available box as independent future Extensions, disabled by default.
- Record the original full-party/full-active-box ball-use restriction and proposed storage acceptance cases.

No game feature or build configuration is implemented. Optional storage work is not a gate for initial core releases.

## 0.1.11 — 2026-10-14

- Accept current-box browsing and STATS with a full party in Bill's PC WITHDRAW flow.
- Move the planned capacity check to the actual withdrawal action, before party/box changes, with the existing error text.
- Record the checked source flow and focused acceptance cases in PN-003 and E70.

No game patch is included. Party and box limits remain unchanged.

## 0.1.10 — 2026-10-14

- Accept SELECT key-item registration in the default core, with the Bicycle as a required use case.
- Verify the existing overworld/list controls and Bicycle checks, including the separate forced-riding menu guard.
- Record registration, possession, input-context, and save/load requirements in PN-002.

No game shortcut is implemented. Bicycle acquisition, speed, and use restrictions remain protected.

## 0.1.9 — 2026-10-14

- Start the playthrough findings register with PN-001 / RGB-029: EXP. ALL discard protection is accepted in the default core.
- Verify its key-item flag, shared bag/PC toss guards, one-time reward event, storage paths, and experience-presence check against the pinned source.
- Allow explicitly accepted safety and usability safeguards in the default contract. Provide developer configuration when straightforward; it is not required to ship a safeguard.

No game patch is included. EXP. ALL's experience calculation and the separate RGB-017 report are unchanged.

## 0.1.8 — 2026-10-12

- Require separate developer choices for improved trainer AI and a replacement random-number generator, with tested baseline behavior and independent unrelated features.
- Add explicit generator coverage to the mechanics contract and test plan.
- Keep PokéRGB Expansion as the preferred working name and describe the broad configurable base.
- Add adoption and public visibility goals, with a proposed release and outreach plan.
- Clarify that Emerald Expansion provides trainer AI controls; a complete original-AI restoration profile was not verified.

Accepted defect repairs remain part of the default core. No game implementation, public announcement, or new name is included.

## 0.1.7 — 2026-10-12

- Make small, original-style hacks a primary use case, alongside larger Gen 1 projects.
- Require a minimal customization example and protect the default build as optional systems grow.
- Keep PokéRGB Expansion as the working name; no new name is selected.
- Compare Emerald Expansion's random-number generator and documented trainer AI with the original Emerald reference. Separate a mostly vanilla game from exact original behavior.

The default mechanics contract is unchanged. No game implementation or Emerald build is included.

## 0.1.6 — 2026-10-12

- Make the conservative inclusion rule explicit: uncertain changes stay out of the default core.
- Close Q02 for the default core: retain badge stacking; a later developer option can offer a correction.
- Separate four remaining implementation items from deferred legacy-state research.
- Check current Emerald Expansion roster controls, modern defaults, and configuration policy against a separate pinned revision.

No game implementation is included. Existing core behavior is unchanged; its badge-stacking policy is now settled.

## 0.1.5 — 2026-10-12

- Clarify the boundary between settled requirements, their consequences, source findings, and engineering proposals.
- Mark the convenience-feature review method as proposed; downstream developers choose their own rules.

Settled requirements, default mechanics, and the six open decisions remain unchanged. Source pins and research results are unchanged. No game implementation is included.

## 0.1.4 — 2026-10-12

- Separate Shin Master's configurable Hyper Beam KO behavior from the checked Lite path; correct the location of conflicting documentation.
- Verify Yellow/Solus Eevee-to-Jolteon Focus Energy access without changing the default learnsets or the corrected Solus arithmetic finding.
- Trace Sabrina's gym advice to source while keeping original intent unresolved.
- Require a short release table explaining actual mechanics changes and their test records.

Settled mechanics and the six open decisions remain unchanged. No game implementation is included.

## 0.1.3 — 2026-10-12

- Add a concrete review rule for convenience features that affect choices, costs, information, and progression.
- Verify selected PureRGB redesign examples and document the limits of its restoration options.
- Trace the cited Stadium move wording to pinned text notes; leave its untested battle-engine claims explicit.
- Add the primary design essay as an opinion source, with its project application kept separate from historical evidence.

Settled mechanics and the six open decisions remain unchanged. No game implementation is included.

## 0.1.2 — 2026-10-12

- Add separate source-backed records for burn/paralysis stat recalculation and Itemfinder's zero-coordinate limit.
- Record that the pinned hidden-item table has no zero-coordinate entries; a conditional code defect is not proof of a failed ordinary play path.
- Make the original OHKO Speed gate and X Accuracy interaction explicit in the mechanics contract and test plan.
- Add a donor review that separates documentation claims, checked code, and untested integration.
- Verify the cited guidebook pages and narrow the historical inference about Ghost/Psychic intent.

Settled mechanics and the six open decisions remain unchanged. No game implementation is included.

## 0.1.1 — 2026-10-12

- Expand the developer workflow with build profiles, data checks, capacity reports, and reproducible debugging.
- Specify optional presentation acceleration with normal audio timing and explicit gameplay, RNG, and link checks.
- Add save/link support targets, checkpoint testing, and a proposed single command for routine checks.
- Add contribution guidance, deliberate upstream-update review, release records, and a focused risk register.
- Allow a useful Red/Blue correction release before Green's cosmetic build is ready.

Settled mechanics and the six open decisions are unchanged. No game implementation is included.

## 0.1.0 — 2026-10-11

- Establish the charter, settled decisions and default mechanics contract.
- Specify shared English RGB builds with Green inheriting Blue gameplay.
- Add architecture, bug-fix policy, triage, testing/CI, provenance and phased acceptance criteria.
- Record pinned research, the full archived-catalog intake and a critical-hit arithmetic audit.
- Correct unsupported donor-patch, build-tool, badge, licensing and historical claims.
- Record the remaining engineering decisions and verification limits.

No game implementation is included in this specification release.
