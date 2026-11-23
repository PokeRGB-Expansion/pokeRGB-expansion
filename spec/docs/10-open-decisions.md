# Remaining engineering work

**The move and inventory screens have preset decisions.** D61/D62 put them in the complete public Core and identify what also ships in Minimal. The [decision audit](../research/sweep-decisions.md) records the player effects. Both screens are implemented in the buildable source.

The [compatibility checks](07-testing-ci.md#verified-reference-configurations) record the support tested for Core. The complete [release check](09-roadmap.md#public-release-checks) still applies.

D50 settles the new Core battle data. D54–D56 settle equivalent shortcuts, manual box selection and the use of shared code. Save recovery for automatic placement and a high-ID link exchange remain engineering gates for their respective options. [Minimal decisions](../research/minimal-action-review.md) · [Storage](../research/storage-policy-and-code.md) · [Large rosters](../research/species-id-architecture.md)

## Q01

**Closed.** In Core, calculate the ordinary or high-critical threshold exactly as Red/Blue does without Focus. If the user is pumped, multiply that threshold by four and cap it at 255. Use the original comparison with the rotated random byte. The multiplier is a project choice informed by the described benefit and the stock arithmetic. The [threshold audit](../research/critical-hit-analysis.md) distinguishes the controlled prototype and the remaining full-game tests.

## Q03

**Closed for the first Core release.** The tested profile covers same-release Core trades and battles. Save imports cover the pinned English Red and Blue bases, with Blue imports for Green. [Verified configurations](07-testing-ci.md#verified-reference-configurations)

## Q04

**Closed.** The cartridge tests use SameBoy 1.0.5. The release records separately identify Game Boy, Super Game Boy, and Game Boy Color compatibility-mode evidence. [Verified configurations](07-testing-ci.md#verified-reference-configurations)

## Q05

**Closed.** Green uses Bulbasaur on the English title, the Green cartridge name, and the original Green Super Game Boy border with a Green palette. The [presentation record](06-build-variants.md#green-presentation-scope) lists the sources and checks.

## Settled and deferred records

The following IDs remain for existing references. Neither is an unresolved choice about what the initial core should contain.

## Q02

**Closed: retain badge stacking in the default core.**

Ordinary badge bonuses and repeated boosts are retained. D25 corrects Thunder→Speed and Soul→Defense to match the original descriptions; it does not change this stacking decision. The source excludes badge boosts from link battles; the stacking behavior is a single-player path. A status-medicine repair must preserve the stacking baseline with the corrected mapping.

A later developer feature can offer a narrow stacking correction. It must be disabled by default and have its own stat, rounding, and interaction tests. It does not block a core release. Burn/paralysis recalculation remains a separate research record, RGB-027.

## Q06

**Deferred research: unsafe legacy states.**

Protect supported normal play and repair proven corruption through narrow, verified changes. Do not claim support for arbitrary glitch Pokémon, arbitrary code execution, or malformed saves. Track particular exploits and data boundaries in the catalog.

If a proposed change's evidence or place in the core is uncertain, leave the change out and retain the current behavior. Review can continue per defect without a global glitch-policy decision or a release requirement for an unaccepted feature. A later developer extension can offer a deliberate alternative.

## Later engineering selections

The patch format, repository ownership, release version scheme, configuration syntax, measured performance budgets, and long-term mapper/ID design can be selected when their implementation is needed. Deferred expansion design is not an unresolved requirement for Core.

## Bounded usability design and research

PN-010–PN-015 are accepted repairs/interfaces with implementation checks remaining. Their inclusion is not an open decision. Keep manual Flute use at Snorlax in Core; the contextual prompt is deferred because it may reveal the puzzle solution.

D61 and D62 settle machine names, move INFO, storage counts and the other reviewed usability changes for each preset. The game builds still need readable layouts and input tests. [Preset decisions](../research/sweep-decisions.md)

Static INFO is included in Minimal and Core. The live type overlay is a separate author feature. [Controls and visibility](15-battle-information.md)

The encoded 40-coin payout and safe gift ordering belong in Core. Oak’s text layout and the intro cry qualify for Minimal and Core. Extra move-replacement prompts and caught markers stay optional. Admission keeps its original requirements. The [case decisions](../research/catalog-decisions.md) specify the remaining display checks. The [remake comparison](../research/remake-usability-comparison.md) records checked clues and missing evidence. A later game's choice is neither a default-inclusion rule nor proof of the first team's intent.

## Item-capacity implementation

The separate-reserve design is accepted in D36. [PN-020](13-playthrough-intake.md#pn-020) places the live bag in the 134-byte block while keeping all other fields at their existing addresses. The selected preset is 64, which fills the allocation exactly; gameplay support still requires tests. Reserve ownership and overlap checks are requirements. Remaining work includes the exact format marker, capacity/layout identity, save import policy, caller tests, initialization after the game-progress clear, and supported feature combinations. Any advertised PC-capacity alternative needs its own allocation and tests.

## Reviewed move and box behavior

[PN-021](13-playthrough-intake.md#pn-021) accepts SELECT cursor retention, and [PN-022](13-playthrough-intake.md#pn-022) selects append order for new boxed arrivals. D39/[PN-023](13-playthrough-intake.md#pn-023) now selects a scoped Core correction for the three Mansion Burglars, superseding their earlier preservation disposition. Range one is the proposed implementation target. The source comparisons in E112–E114 do not establish original intent. Runtime engagement, wandering movement, route-safety, and save checks remain engineering work; other zero-range trainers stay unchanged.

## Star-grass repair scope

D40/[PN-024](13-playthrough-intake.md#pn-024) accepts a Core correction for the confirmed grass-recognition mismatch. Inclusion is settled; the exact code change and regression checks remain engineering work. Choose a narrow Forest repair or explicitly review the broader Yellow corner change, which also affects shores. The [source review](../research/forest-encounters.md) establishes the defect; implementation and neighboring-case checks remain open. This research does not delay other releases.
