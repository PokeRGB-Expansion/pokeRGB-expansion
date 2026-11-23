# Bug-fix policy

Use three distinct reasons for a change. **Likely original intent** can justify a narrow Core correction when contemporary instructions and independent clues converge. Conflicting evidence stays in the record. **Official revisions and usability improvements** can justify an explicit Core design choice even where the earlier behavior worked as written. **Author alternatives** cover credible choices that would substantially change a rule or workflow without enough reason for a shared default. Record the concrete player benefit, costs and limits retained, and what each preset does.

Minimal preserves battle results, practical team-building choices, and requirements such as a learned move, a badge or room in the selected box. Compare the original action with the shortcut from the same situation. If the player already qualifies and gets the same result at the same cost, faster controls can ship in Minimal. Accurate feedback and protection for a cancelled action also qualify. [Worked examples](../research/minimal-action-review.md)

## Acceptance rule

A core correction repairs an invalid state, data loss, failure of an existing function, wrong calculation within the current rules, or misleading output. It preserves unrelated behavior. A later generation changing a rule, a move feeling weak, or a type interaction seeming odd does not by itself prove a defect.

A verified bug can still be a protected part of the chosen Gen 1 contract. Hyper Beam's KO exception is preserved. Focus Energy's reversed effect is corrected. Classification alone does not decide the project policy.

The burden is on a proposed change to establish that it belongs in the default core. If its evidence, scope, or consequences remain uncertain, exclude the change and retain the current behavior. Research can continue without making its resolution a release gate. A later developer feature can offer a deliberate alternative with its own contract and tests.

Badge stacking is retained under this rule. A future optional correction must be disabled in the default build. This does not delay already accepted corrections such as Focus Energy or authorize an untested patch.

## Evidence and implementation are separate

Accepted safety and usability safeguards can prevent a valid original action without claiming that the original implementation was accidental. Minimal and Core protect the one-time EXP. ALL reward against tossing and selling. Record such changes in [playthrough findings](13-playthrough-intake.md), with their source evidence and implementation status. They do not authorize unrelated combat or resource changes.

Provide a developer option when it is straightforward to maintain. Keep the accepted safeguard enabled by default. Configuration is not a release gate for the safeguard and does not require a new player setting.

Track three independent fields:

| Field | Values |
|---|---|
| Evidence | Reported; source-confirmed; reproduced in an executable baseline; verified after correction |
| Disposition | Accepted in principle; proposed correction; investigate; preserve; extension only; outside core |
| Delivery | Not started; patch in review; merged; included in a named release |

Source-confirmed means the relevant code supports the stated behavior. It does not mean the bug was exercised in a ROM. Accepted in principle does not mean a candidate patch is safe or ready.

The archived pret catalog explicitly says it is unvetted. Its entries and suggested patches are leads. A donor README likewise describes a project's claims, not proof of the patch's behavior. [E24](../research/evidence.md#e24)

## Minimum bug record

Use a stable ID and include:

1. A precise trigger and observed result, including variant, battle mode, and source revision.
2. The intended result under this project's contract and the evidence for it.
3. The affected routines and a small explanation of the cause.
4. A proposed correction, its donor/source history if any, risk, affected behavior, and save/link compatibility effects.
5. A regression case that fails for the defect and passes after correction.
6. Neighboring cases that protect the original rule, including relevant RNG use, both battle sides, and link state.
7. Evidence status, disposition, priority, owner, and release status.

Record actual steps instead of broad labels such as “softlocks” or “Transform bugs.” Split independently reproducible failures into separate records. Record dependencies for repairs that cannot safely stand alone.

## Typo corrections

Unambiguous spelling and typing errors belong in Core. Correct the smallest amount of text needed. Preserve meaning, character voice, puns, deliberate informal speech, and game terms. Record each confirmed error and check its layout and shared uses. Reflow lines when a corrected word needs more space. A display check is sufficient for a spelling-only repair; a new game test harness is not required.

Minimal preserves the characters’ original writing. For an accepted typo or false statement, correct the affected words or use an existing line that fits. A prompt for a new control, such as pressing A to Cut, belongs to that action. A mechanic that works as designed needs no new lesson from an NPC. Document its rules in the guide when an explanation helps. [Day Care example](../research/day-care-history.md)

## Review depth

For text and simple visual corrections, source evidence plus a rendered/game check can suffice. For battle arithmetic, memory writes, saves, or link behavior, require executable regression evidence and review of boundary cases. Use a second technical reviewer when the implementation risk warrants it; a fixed count of reviewers is not a substitute for evidence.

Do not bulk-merge a donor's “bug fixes.” Shin Lite also changes the critical-hit damage formula, fixed-damage immunities, Hyper Beam, accuracy, AI, and other protected rules. Solus's current Focus Energy implementation changes ordinary critical-hit probability. [E22](../research/evidence.md#e22), [E23](../research/evidence.md#e23)

## Correctness without incidental rebalance

Core keeps original trainer behavior except for specifically accepted corrections. D44 accepts a full-HP guard for Blaine. Minimal preserves his original item decision and turn cost. Broader changes to trainer strategy belong in Extended. Apply the [preset criteria](14-features-and-extensions.md#product-presets) to each new repair.

Review other battle-engine fixes that can make fights harder case by case. Show which outcomes change and why the change is necessary to repair the defect. Earlier accepted corrections, such as Focus Energy and the Thunder/Soul badge mapping, can change battle outcomes and remain part of Core.

For presentation fixes, keep damage and RNG unchanged. Correct the effectiveness text and sound using the combined type relationship; do not rewrite the damage pipeline to make the display easier.

For an invalid-state fix, preserve valid-state behavior. For example, stopping Substitute at exactly zero remaining HP does not authorize a general Gen 2 Substitute rewrite. Clearing interrupted Fly/Dig invulnerability does not authorize changing trapping duration.

## Review convenience features

The default data contract and explicitly accepted features govern inclusion in the core. SELECT item registration is an accepted default usability feature, not a claim that the original control scheme is a bug. It keeps the Bicycle's acquisition, speed, and use restrictions. The checks below are a proposed review method for other features. They do not prescribe the rules of downstream games or narrow the expansion mission.

The [Core and Extensions guide](14-features-and-extensions.md) records defaults and supported choices. Both faithful presets keep manual box selection. Direct MOVE POKÉMON and automatic placement are independent build options.

Judge a change by its effect on the game's meaningful constraints and choices. Neither a small patch nor the labels “quality of life” and “basic usability” establish that it belongs in the default core. More options do not by themselves improve a game.

For a proposed interface, travel, or resource change, record:

- What the player can do before and after it, and when it becomes available.
- Which costs change: money, items, move slots, time, or a choice that cannot be undone.
- Whether it gives new information or changes the reward for preparation, exploration, or repeated team changes.
- Which existing limits and progression rewards it preserves, and which it deliberately replaces.

Keep the 20-slot bag and inventory management in the default game. Contextual HM use is accepted because it changes access to an earned action while retaining learned moves, move slots, badges, and use restrictions. Original designer intent and our preservation choice are separate claims; code showing a limit does not by itself establish its historical motive.

For example, free move relearning can change the cost of choosing four moves. Field moves without a move slot can change team-building costs. Early faster travel can change the value of earning the Bicycle. These are design questions to assess in a developer feature proposal; they are not claims that every player will react the same way.

Accurate effectiveness text repairs misleading output. Adding encounter knowledge or removing a resource limit has a different scope. Keep such changes separate from that repair and from the agreed default game data. Later developer capabilities remain available through the [architecture plan](02-architecture.md).

Kayin's [design essay](../research/evidence.md#e58) is a useful review prompt about player incentives. It is an opinion source, not evidence of a Gen 1 defect or the original designers' intent.

## Review menu returns individually

Record the current destination, proposed destination, and cursor/scroll state for each action. Inspection, cancellation, failed actions, and completed actions can need different behavior. PC browsing, overworld party action-menu cancellation, and the specified shop refusal/failure returns are accepted in the [menu inventory](../research/menu-navigation.md). Review further return-path changes individually. Preserve medicine's return to the bag after use. Do not apply a global keep-open or back-one-level rule.

## Compatibility and release notes

Every accepted fix lists its vanilla behavior, corrected behavior, and compatibility effect. Test links between supported builds. Do not retain a broken rule only in link battles as an unannounced workaround.

Public Core ships with every accepted Core change. Publish known issues and the limits of support. New regressions, data loss introduced by the release and failures of advertised features block release. Each archived report has its own decision in the [release scope](09-roadmap.md#what-counts-toward-core).

## When evidence is insufficient

Leave the behavior unchanged and write the next specific investigation step. Do not label it intentional merely because it is absent from documentation. Do not label it fixed merely because a TODO checkbox is checked. Do not claim original intent from a single guidebook or later sequel without weighing contradictory evidence.

## Paid rewards

For an exchange, inspect payment removal, capacity, reward delivery, completion flags, and feedback as one action. A nearby delivery-result check does not prove that a refusal preserves payment. The rooftop drink/TM defect in [PN-015](13-playthrough-intake.md#pn-015) requires both sides to succeed together or remain unchanged. Test capacity after the offered item leaves its slot as well as existing reward stacks.

When a change affects how players earn or spend a resource, follow it through to what they can buy. Start from an ordinary balance and redeem the most expensive reward in each color. Check whether the change forces a different activity, requires a one-time pickup, or prevents delivery. Red’s Porygon caught a regression that forty checks of individual coin sales missed. [Worked example](../research/game-corner-redemption.md)
