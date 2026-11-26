# Remaining engineering work

Core and Minimal have working Red, Blue and Green builds. Use the [player guide](16-game-changes.md) for current behavior and the [release checks](09-roadmap.md#public-release-checks) for the evidence required to publish it.

D67 settles the [three v0.3.0 follow-up features](../research/v030-core-candidates.md) for Minimal and Core. The table below covers separate future work.

## Decisions for future features

| Feature | Agreed direction | Work before shipping it |
|---|---|---|
| Move Reminder | Extended can support relearning outside battle from the party menu. Track the history of the individual Pokémon. Core offers move deletion in Fuchsia. | Define which moves qualify, how to store the history, and what an older save or traded Pokémon contributes when its prior history is unknown. |
| Larger bag | D36 proposes a 64-slot bag in 134 bytes of original padding. Both reference presets keep 20 slots. | Account for the registered item, which now uses two of those bytes. Choose the format marker and save-import rules. Test initialization, every inventory caller, and combinations with other options. An expanded PC needs its own allocation and tests. [PN-020](13-playthrough-intake.md#pn-020) |
| Automatic box placement | Both reference presets require manual box selection. Automatic placement and direct MOVE POKéMON are separate author features. | Prove recovery across an interrupted box change, including the last unsaved arrival. [Storage requirements](../research/storage-policy-and-code.md) |
| More species | Design for a large roster when Extended needs it. | Select the ID and bank layout from measured requirements. Test high IDs through the game, save format and any advertised cable exchange. [Species design](../research/species-id-architecture.md) |
| Other developer options | Extra move-replacement prompts, a contextual Flute prompt at Snorlax and a live type overlay can be considered separately. Manual Flute use preserves the puzzle in both current presets. | Define the effect on player choices, a disabled control and a test through the actual game. [Battle information](15-battle-information.md) |

<a id="q01"></a>

## Q01 · Focus Energy

**Closed.** Core calculates the ordinary or high-critical threshold as Red/Blue does. Focus Energy multiplies that threshold by four, capped at 255. The game compares it with the original rotated random byte. The multiplier is the project's interpretation of the described benefit and the stock arithmetic. [Threshold audit](../research/critical-hit-analysis.md) · [Cartridge tests](../../tests/critical_hits.py)

<a id="q02"></a>

## Q02 · Badge boosts

**Closed.** Both presets retain repeated badge boosts. Core assigns Thunder to Speed and Soul to Defense to match the descriptions. Stacking applies in single-player battles. A future author option could change it after testing stat rounding and medicine interactions. RGB-027 covers burn and paralysis separately. [Mechanics contract](05-mechanics-contract.md)

<a id="q03"></a>

## Q03 · Save and link compatibility

**Closed for the reference games.** v0.3.0 tested all nine color pairings for trades and battles within each preset. Original save imports cover the pinned English Red and Blue cartridges, with Blue imports for Green. [Results and limits](07-testing-ci.md#verified-reference-configurations)

<a id="q04"></a>

## Q04 · Test hardware and emulator

**Closed.** The cartridge tests use SameBoy 1.0.5. The release records distinguish Game Boy, Super Game Boy and Game Boy Color compatibility mode. [Verified configurations](07-testing-ci.md#verified-reference-configurations)

<a id="q05"></a>

## Q05 · Green’s title screen

**Closed.** Green opens with Bulbasaur on the English title, the Green cartridge name, and the original Green Super Game Boy border. Its title lettering and colors have their own reference checks. [Green presentation](06-build-variants.md#green-presentation-scope)

<a id="q06"></a>

## Q06 · Unsupported glitch states

**Deferred research.** The reference games protect normal play. Review unsupported legacy states individually when a reproducible case identifies affected data. Arbitrary glitch Pokémon, code execution and malformed saves are outside the supported profile. [Case decisions](../research/catalog-decisions.md)

## Closed scope records

- D50 sets Core's battle data. D54–D56 settle equivalent shortcuts, manual box selection and shared code. [Minimal review](../research/minimal-action-review.md)
- D61/D62 settle machine names, static move INFO and capacity counts. PN-010–PN-015 cover rewards, feedback, the elevator and quantity controls. The encoded 40-coin pickup and safe gift ordering belong to Core. Oak's text and the intro cry are shared. The original requirements for admission remain. [Player-impact decisions](../research/sweep-decisions.md) · [Case inventory](../research/catalog-decisions.md) · [Remake evidence](../research/remake-usability-comparison.md)
- Both presets support independent build options for the caught marker and battle EXP bar. [HUD design](../research/battle-hud-displays.md)
- PN-021/022 govern move-swap cursor retention and box insertion order. D39/PN-023 gives the three Mansion Burglars a one-square challenge in Core. Other zero-range trainers keep their behavior. The evidence supports the change without proving original intent. [Playthrough intake](13-playthrough-intake.md#pn-021) · [Mansion tests](../../tests/mansion_sight.py)
- D40/PN-024 repairs the missed grass squares in Viridian Forest in Core. The source limits the exception to that map. [Encounter source](../../engine/battle/wild_encounters.asm) · [Game checks](../../tests/forest_encounters.py)
