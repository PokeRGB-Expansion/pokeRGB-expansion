# Default mechanics compatibility contract

This contract defines the reference builds. It preserves meaningful Gen 1 rules and allows a reviewed set of corrections. It does not promise byte identity or complete agreement with competitive simulators.

## Required baseline

| ID | System | Required behavior | Main evidence / test |
|---|---|---|---|
| MC01 | Types and effectiveness | Original 15 usable types. Minimal uses Ghost → Psychic 0×. Core uses 2×. All other chart entries match the stock reference, including Ghost → Normal 0× and Bug↔Poison 2×. | Compare every pair against the stock chart plus the one approved override. [D50](01-decisions.md) |
| MC02 | Stats | HP, Attack, Defense, Speed, unified Special; original stat experience and DVs. | [E17](../research/evidence.md#e17); data and stat fixtures |
| MC03 | Attack category | Original type-based physical/special division. | Damage-routine reference comparison |
| MC04 | Ordinary critical hits | Base-Speed formula and byte comparison retained exactly when unpumped. | [E04](../research/evidence.md#e04); exhaustive threshold test |
| MC05 | High-critical moves | Existing move list and threshold retained exactly when unpumped, including odd-Speed rounding. | [E04](../research/evidence.md#e04); all list members, ordinary controls |
| MC06 | Critical damage | Original calculation and handling of modified/unmodified stats; no Stadium or Shin damage formula. | [E44](../research/evidence.md#e44); levels, boosts, penalties, screens |
| MC07 | Focus Energy / Dire Hit | Correct the reversed effect under one documented algorithm; the same pumped state has the same effect for either actor. | RGB-001; exact method Q01 |
| MC08 | Hyper Beam | No recharge after KO; preserve original miss and Substitute-related behavior unless a separately approved defect changes a boundary. | [E08](../research/evidence.md#e08); KO, survival, miss, Substitute |
| MC09 | Fixed/set damage | Preserve original type-immunity bypass for the set-damage path. Night Shade can damage Normal; Seismic Toss can damage Ghost. No STAB or type multiplier added. | [E07](../research/evidence.md#e07); exact HP loss and immune types |
| MC10 | Partial trapping | Original Wrap/Bind/Clamp/Fire Spin turn lock and duration distribution; do not import later chip-damage rules. | [E09](../research/evidence.md#e09); speeds, switch, repeated turns |
| MC11 | Sleep | Original generated duration counter, including loss of the wake-up move turn. Rest's own behavior is tested separately. | [E10](../research/evidence.md#e10); counter/turn traces |
| MC12 | Freeze | Original absence of a spontaneous thaw roll and original thaw/cure paths. | [E10](../research/evidence.md#e10); turn and cure traces |
| MC13 | Accuracy | Original calculation and random-byte comparison; retain 1/256 failure at a threshold of 255. Swift/X Accuracy bypass paths stay distinct. | [E11](../research/evidence.md#e11) |
| MC14 | Toxic / Leech Seed | Original shared escalating-damage interaction; no automatic donor separation. | [E45](../research/evidence.md#e45) |
| MC15 | Badges | Thunder boosts Speed; Soul boosts Defense. Keep original descriptions and the bonus amount, rounding, cap, and other badge assignments. No badge bonus in link battles. Preserve original stacking with the corrected mapping. | [E12–E13](../research/evidence.md#e12), [D25](01-decisions.md), [regressions](07-testing-ci.md#badge-mapping-regression-coverage) |
| MC16 | Moves and roster | Core uses Flying Gust and gives Charizard HM02 Fly. Minimal retains Normal Gust and stock eligibility. Both retain Normal Karate Chop and Sand-Attack, original high-critical flags, base power, accuracy and PP. | [Stock comparison](../research/yellow-data-diff.json) · [Core rule tests](../research/core-rule-precedents.md) |
| MC17 | Substitute | Original valid-state behavior; Core refuses activation when paying the original cost would leave zero HP. Do not wholesale replace status or move-effect interactions. | RGB-005, RGB-021 |
| MC18 | Progression and economy | Original capture/experience formulas, evolution methods, item availability/use limits, maps, encounters and trainers except approved repairs and recorded safeguards. | Data comparison and adventure tests |
| MC19 | AI | Core skips Blaine's Super Potion at full HP after the original chance roll. Keep his existing behavior below full HP and the original trainer choices elsewhere unless separately approved. Minimal preserves the original full-HP turn. | [E121](../research/evidence.md#e121). Compare action, potion count, HP, and random calls. |
| MC20 | Information | Text, sound and animation describe the retained rules accurately. A display correction does not change damage. | RGB-009/010 and UI capture |
| MC21 | Secondary effects and repeated hits | Preserve original same-type secondary-effect restrictions, multi-hit calculation reuse and valid move-effect timing, except separately approved defects. Body Slam's Normal-type paralysis restriction is included. | [E49](../research/evidence.md#e49); complete turn fixtures |
| MC22 | OHKO moves and X Accuracy | Preserve the current battle-Speed eligibility check separately from accuracy. A slower user fails; equal or greater Speed passes that gate. X Accuracy bypasses the ordinary accuracy roll, not the Speed gate or every earlier target check. | [E56](../research/evidence.md#e56); both actors, slower/equal/faster, X Accuracy on/off and baseline target checks |
| MC23 | Random-number generation | Retain the original generator in the default core. A replacement is a separate developer option. An accepted repair that changes when random values are consumed must record and test that effect. | Real generator fixtures with controlled initial state and hardware inputs; call/state comparison |
| MC24 | EXP. ALL protection | Minimal and Core refuse to toss EXP. ALL from the Bag or item PC and to sell it in shops. Use the existing important-item refusal messages. Keep acquisition and PC storage. For XP and stat experience, Core applies RGB-017 and Minimal keeps the original awards. | RGB-029; [PN-001](13-playthrough-intake.md#pn-001); inventory and menu regression |
| MC25 | Registered item | Allow one eligible key item to be used with SELECT in the overworld, including the Bicycle. Keep possession/use checks and existing SELECT menu functions. | [PN-002](13-playthrough-intake.md#pn-002); input, Bicycle restrictions, and save/load cases |
| MC26 | Box browsing | A full party does not block the current box list or STATS in Bill's PC WITHDRAW flow. An attempted withdrawal still obeys the party limit and uses the existing error. Leaving STATS or cancelling a selected-Pokémon action restores the accessible browsing list and its selection/scroll context. | [PN-003](13-playthrough-intake.md#pn-003); browsing, capacity, and unchanged data cases |
| MC27 | Inventory management | Keep the 20-slot bag and its existing capacity rules; no incidental larger bag or separate key-item pocket. | [E72](../research/evidence.md#e72); full-bag acquisition, storage, and save cases |
| MC28 | Contextual HM use | A at a suitable target offers confirmation for an eligible party Pokémon's field move. Cut trees, Surf water, and Strength boulders retain learned moves, move slots, badges, and use restrictions. | [PN-004](13-playthrough-intake.md#pn-004), [E73](../research/evidence.md#e73); target, eligibility, cancellation, and progression tests |
| MC29 | STATS navigation | Up/down changes Pokémon; left/right changes page; B returns to the caller's browsing context. Default information stays unchanged. Additional developer pages use the same controls. | [PN-006](13-playthrough-intake.md#pn-006), [menu inventory](../research/menu-navigation.md) |
| MC30 | Release confirmation | Identify the selected nickname and species. Default to No. Only explicit Yes removes that Pokémon once; B/No leaves data unchanged. | [PN-007](13-playthrough-intake.md#pn-007), [E85](../research/evidence.md#e85) |
| MC31 | Medicine menu flow | Outside battle, preserve the return to the bag after use. Do not retain the target selector for repeated uses. Battle item costs and action rules stay unchanged. | [E86](../research/evidence.md#e86); menu regression |
| MC32 | Shop return context | Refused sales restore the SELL list; failed purchases for money or bag space restore the BUY list. Keep selection/scroll and all messages, prices, capacity, and transaction rules. | [PN-008](13-playthrough-intake.md#pn-008), [E86](../research/evidence.md#e86) |
| MC33 | Party action-menu cancellation | Outside battle, CANCEL and B both restore the party list with the same Pokémon selected. B from the party list still returns to Start. Preserve other actions and caller rules. | [PN-009](13-playthrough-intake.md#pn-009), [E86](../research/evidence.md#e86) |
| MC34 | Vending affordability | Check the actual chosen price before delivery; refusals take no money and give no drink. Keep the original prices and item effects. | [PN-010](13-playthrough-intake.md#pn-010), [E89](../research/evidence.md#e89) |
| MC35 | Flute feedback | Report actual sleepers woken, including a wild opponent. Keep effect targets, turn cost, ownership, and sleep rules. | [PN-011](13-playthrough-intake.md#pn-011), [E94](../research/evidence.md#e94) |
| MC36 | Trade follow-up | Remove the false evolved-Raichu statement. Keep requested/received species, trade data, and evolution rules. | [PN-012](13-playthrough-intake.md#pn-012), [E91](../research/evidence.md#e91) |
| MC37 | Elevators | Show the actual current floor. Selecting it causes no travel animation, travel sound, or destination change. | [PN-013](13-playthrough-intake.md#pn-013), [E103](../research/evidence.md#e103) |
| MC38 | Quantity controls | Left/right changes ten. Up/down unit changes and wrap remain. Keep bounds, live price display, confirmation, and cancellation. | [PN-014](13-playthrough-intake.md#pn-014), [E103](../research/evidence.md#e103) |
| MC39 | Rooftop exchange | Take exactly one chosen drink and give its one-time TM together; on refusal, preserve payment, reward, and completion flag. Allow a final drink to free a slot. | [PN-015](13-playthrough-intake.md#pn-015), [E101](../research/evidence.md#e101) |
| MC40 | Item-list position | Retain the same entry and viewport when returning to the same list; after deletion choose the successor, otherwise the preceding item. Keep bounds valid and preserve existing caller destinations and transaction rules. | [PN-019](13-playthrough-intake.md#pn-019), [E106](../research/evidence.md#e106) |

“Original” in this table means the pinned English Red/Blue source, not Japanese versions, Stadium, Yellow-only differences, or a simulator's interpretation. Add executable baseline fixtures where a rule spans several routines.

Burn/paralysis stat recalculation remains unchanged; RGB-027's proposed correction is deferred outside the current core. The original critical-damage formula and badge stacking are protected throughout. A narrow status-medicine repair must preserve them.

### Transform and Swift

Under D46, Core checks the target’s Fly/Dig invulnerability before Transform copies any state. Swift keeps its cartridge targeting and normal type immunities. Test each move on both sides against airborne, underground and grounded targets. For failed Transform, also check species, moves, PP, stats, and the transformed flag against the ordinary failure path. [Decision rationale](../research/core-scope-review.md#transform-and-swift)

## Exact critical-hit baseline

For nonzero-power moves entering `CriticalHitTest`, let `S` be the species' base Speed and `H = floor(S / 2)`. With Focus Energy absent:

```text
ordinary threshold = H
high-critical threshold = min(8 × H, 255)
critical hit when rotate_left_8(random_byte, 3) < threshold
```

The probability is `threshold / 256` when input random bytes are uniform. This is a conditional calculation for this test, not an assertion that every in-game random stream is independent and uniform.

The common shorthand `S / 512` omits integer rounding. The high-critical shortcut `min(4 × S, 255)` is wrong at some odd Speeds. For `S = 55`, the original high-critical threshold is 216, not 220. Neither rounding nor the `255/256` ceiling can be changed incidentally. [E04](../research/evidence.md#e04)

With the original broken Focus Energy active, the ordinary threshold is `floor(S / 8)`, and the high-critical threshold is `min(4 × floor(floor(S / 2) / 2), 255)`. Preserve those values only as regression inputs demonstrating the old defect.

## Core battle repairs

Minimal and Core use the selected box for a PC-eligible arrival. An author can enable [automatic placement](../research/box-overflow-contract.md). Both presets protect an older save on cancellation. [Box picker checks](../research/box-picker-safety.md)

With D50, Lick follows the chosen Ghost multiplier, Night Shade retains level-based damage and Confuse Ray uses its status checks. Gust remains physical under either Gen 1 type. Counter eligibility follows its actual type. Use the original bugs-and-ghosts hint with Core and Yellow’s bugs hint with Minimal. Developer overrides must keep the advice truthful. Test HM02 teaching separately from Fly as a battle or field move. [Evidence and prototype results](../research/core-rule-precedents.md)

The [Core battle rules](../research/foundation-audit.md#five-stock-battle-findings) cover EXP. ALL, drain effects, Rest, transformed move swaps and the trainer alternative-slot check. The [damage and link rules](../research/foundation-audit.md#damage-multi-turn-moves-and-link-play-beyond-the-catalog) specify arithmetic boundaries, doll ownership and Psywave endpoints. Minimal preserves the stock gameplay result for these cases.

## Focus Energy correction

**Accepted:** make Focus Energy and Dire Hit increase critical-hit likelihood while leaving all unpumped rates unchanged. Keep the original core critical-hit system and its 255/256 ceiling. Both set the same pumped-state bit. [E43](../research/evidence.md#e43)

**Core rule (Q01).** Calculate the unchanged ordinary/high-critical threshold first, then apply a saturating multiplier of four when pumped:

```text
base = H                         # ordinary move
base = min(8 × H, 255)            # high-critical move
corrected threshold = min(4 × base, 255) if pumped else base
```

At base Speed 130, an ordinary move uses threshold 65 before Focus and 255 after it. The stock pumped threshold is 16. The [critical-hit audit](../research/critical-hit-analysis.md) gives the exact rounding, bounds and scope of the prototype.

The precise multiplier order, rounding and interaction with high-critical moves must be approved before implementation. Once chosen, the algorithm belongs in the fix record and must be tested over every byte input.

**Implementation trap:** swapping a branch or moving a shift can lower ordinary rates or cap before the final division. The checked Solus patch gives Speed 130 an ordinary unpumped threshold of 16 and pumped threshold of 65. It is not the proposed unchanged-normal-rate correction. Some wiki alternatives also alter high-critical odd-Speed rounding or reach a 127 threshold after an early cap. [E22](../research/evidence.md#e22), [critical-hit analysis](../research/critical-hit-analysis.md)

Guard the original move eligibility, high-critical list, random call count and three-bit rotation. Tests must distinguish the threshold from the final damage calculation. A stronger corrected Focus Energy can change strategy; that consequence is documented rather than hidden behind a balance patch.

## Hyper Beam, fixed damage, and trapping boundaries

Test Hyper Beam against an opponent that survives, faints, has a Substitute that survives or breaks, and an attack that misses. Test both battle sides and the next actual turn. A fix that merely keeps the recharge flag set after a KO violates MC08.

Set-damage moves bypass the normal calculation and type-adjustment path. They still follow their original hit/target checks. Do not interpret “bypasses immunity” as “cannot miss” or “ignores every target state.” Test Night Shade, Seismic Toss, SonicBoom, Dragon Rage, Super Fang and Psywave by their own effects. Counter is a separate routine. A Psywave desynchronization correction does not authorize modern immunities. [E07](../research/evidence.md#e07)

Trapping tests must observe the target's actions, repeated damage, PP, release turn, misses, switches, and copied moves. A narrow state/PP fix must preserve the successful trapping rule. Test Ghost targets separately: a zero-damage Normal trapping attack can still have turn-control effects under the original code; do not infer those effects from the type chart alone.

## Correction register and comparisons

The implemented project's compatibility report must enumerate every intentional deviation by RGB ID. Compare all other protected results with an executable vanilla baseline. Keep presentation, gameplay calculations, RNG calls, serialization, and saved data as separate observables.

Fixes may change a match result without introducing arbitrary balance. Do not advertise exact competitive compatibility or vanilla link compatibility when such changes exist. A later rules feature gets its own contract and supported-build tests; it does not rewrite this baseline silently.

## Information boundaries

The D43 repairs keep the correct enemy picture after battle STATS and play the intended move-replacement sound. In SHIFT, offer the between-opponent switch only when a reserve can enter. Keep SET, forced replacements, and the rules for a valid switch. See the [accepted repair scopes](04-bug-triage.md#donor-survey-dispositions).

Core retains manual Flute use at Snorlax. Both presets include static INFO on selected moves, even before a purchase or a learning decision. Hidden opponent information and live type indicators stay outside that reader. [Full contract](15-battle-information.md)
