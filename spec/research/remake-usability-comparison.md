# Usability evidence and remake comparisons

The [player-impact review](sweep-decisions.md) records current placements. Original and remake screens provide evidence about what each display reveals.

Checked **2026-10-15** against the pinned English Red/Blue and FireRed/LeafGreen sources. Gold/Silver supplies a separate comparison for TM information and quantity controls. The [source lock](source-lock.json) records each revision. These are source findings, not game executions or access to original development records.

## How to use a remake as evidence

A later release can show that a design was practical or that a later team chose it. It cannot prove why the first game omitted it. Different engines, maps, item pockets, battle rules, and audiences limit direct comparisons. Retain the existing default when a proposed change's fit remains uncertain. A remake feature alone does not make a Core requirement.

## Findings

| Case | Checked original behavior | Later comparison | PokéRGB disposition |
|---|---|---|---|
| Hidden coins | The invisible Game Corner floor event at X=11, Y=7 encodes 40, but the conversion prints and awards 20. It is one of twelve floor coin events, not a gift from a gambler. [E88](evidence.md#e88) | FireRed's changed map includes a 40-coin floor entry at X=17, Y=5. This is a map-data comparison; this review does not trace its crediting routine. [E105](evidence.md#e105) | UA-01 remains a correction recommendation under investigation. |
| Vending price | The original checks ¥200 for every drink before loading the selected price. [E89](evidence.md#e89) | FireRed checks ¥200/300/350 for Fresh Water/Soda Pop/Lemonade respectively. [E101](evidence.md#e101) also identifies the shared rooftop file; the price paths are recorded below. | Accepted Core correction, PN-010. Keep prices and effects. |
| Rooftop drink exchange | Removes the drink before trying to give the TM. A full bag can lose payment without a reward. [E101](evidence.md#e101) | FireRed still removes the drink before its TM-space check. Its separate TM pocket changes the failure conditions. The remake is not a safe transaction template. | Core defect repair under the existing policy, PN-015. |
| TM/HM information | Numbered item names; teaching reveals the move. Some NPCs also name gifted moves. Battle move selection already shows the selected move's type and PP. [E97](evidence.md#e97), [E102](evidence.md#e102) | Gold/Silver TM browsing shows names and descriptions. FireRed's TM Case shows name, description, type, power, accuracy, and PP; its TM shop shows move names before purchase. [E102](evidence.md#e102) | Both presets show the number, move name and INFO before learning or purchase under D61. |
| Capacity counts | The limits are bag 20 item slots, item PC 50 slots, party six Pokémon, and each Pokémon box 20 Pokémon. [E103](evidence.md#e103) | A full comparison of later bag and box counter layouts has not been completed. Later pocket and box capacities must not be copied incidentally. | Both presets show bag, item PC and Pokémon-box counts under D62. |
| Elevator | Any noncancel destination can select travel; the shared menu has no same-floor exclusion. [E97](evidence.md#e97), [E103](evidence.md#e103) | FireRed draws a current-floor window. Its Department Store script skips travel animation for a same-floor selection, though that entry remains selectable. [E103](evidence.md#e103) | Accepted current-floor display and no false travel, PN-013. Disabling or skipping the entry is the preferred interface design, not a claim about FireRed. |
| Quantity controls | Up/down changes one and wraps; left/right is ignored. [E97](evidence.md#e97) | Both Gold/Silver and FireRed have left/right minus/plus ten, clamped at one and the maximum. [E103](evidence.md#e103) | Accepted Core shortcut, PN-014. No claim that every later game or every quantity selector behaves identically. |
| Snorlax and Flute | Talking gives sleeping-Pokémon text; manually using the carried Flute invokes the event. [E98](evidence.md#e98) | FireRed offers a Flute prompt when its acquisition flag is set. [E105](evidence.md#e105) | Keep the original manual puzzle interaction in Core. A contextual prompt is deferred outside the default. |
| Oak's optional five balls | The original commits the gift flag before an unchecked delivery. Normal-play reachability of the no-room fixture still needs work. [E90](evidence.md#e90) | FireRed calls an add-item/message macro, then sets completion, without a caller failure branch. Its changed early bag states need their own reachability review. [E105](evidence.md#e105) | UA-03 remains a scoped recommendation, not a newly accepted requirement. Neither ordering alone proves a safe transaction. |
| Oak's overwritten instructions | Consecutive bottom-line commands overwrite a line. [E92](evidence.md#e92) | FireRed uses a rewritten, paged explanation; it does not preserve this assembly layout. [E105](evidence.md#e105) | UA-05 remains a narrow layout recommendation. Do not import rewritten prose merely because the remake uses it. |
| Introductory cry | Nidorino picture with Nidorina cry. [E93](evidence.md#e93) | FireRed uses Nidoran♀ for both picture and cry. [E105](evidence.md#e105) | UA-06 remains a matching-cry recommendation. The remake is not evidence that Red's picture should become Nidoran♀. |
| Raichu trade, Flute feedback | The false trade follow-up and missing wild-opponent wake confirmation are source-checked. [E91](evidence.md#e91), [E94](evidence.md#e94) | A complete equivalent remake dialogue/effect comparison is not claimed. FireRed has different species trades and battle rules. | Accepted narrow Core repairs, PN-011 and PN-012, independently of remake behavior. |
| Trainer HUD, escape-spin pointer, move-overwrite confirmation, caught marker, admission recovery | See the individual audit records and their limits. | No complete, equivalent FireRed comparison or original-development testimony established in this pass. | Continue investigation. Preserve the default until the particular change is accepted. |

The vending comparison uses FireRed's `CeladonCity_DepartmentStore_Roof_EventScript_BuyFreshWater`, `BuySodaPop`, and `BuyLemonade` paths. They perform the respective price checks before the common delivery path. See [the additional E101 source range](evidence.md#e101).

## Rooftop transaction boundary

All three exchanges share the fault: Fresh Water→TM13 Ice Beam, Soda Pop→TM48 Rock Slide, and Lemonade→TM49 Tri Attack. The script checks whether that reward was already claimed, removes one drink, calls `GiveItem`, and sets completion only after success. Its no-room branch does not restore payment. [E101](evidence.md#e101)

A concrete failing fixture has twenty occupied bag slots, two units of the chosen drink, and no target TM stack with space. Removing one drink leaves its slot occupied, so the new TM cannot fit. With only one drink in that stack, removal frees a slot and the exchange can succeed. A target TM stack with room can also allow success without another slot.

The checked ordinary path does not demonstrate duplication. Failure leaves the reward flag clear because no TM was delivered. A later successful attempt can still claim that reward. Success then sets the one-time flag. Keep broader stack/split defects and any reported duplication sequence separate until reproduced.

The repair must commit both sides exactly once or leave both inventories and the reward flag unchanged. A blanket “require a free slot before talking” check is wrong: it rejects valid exchanges where handing over the final drink frees the needed slot. Account for existing stacks, stack limits, and the separate inventory-splitting defect before choosing a preflight or rollback design. See [PN-015](../docs/13-playthrough-intake.md#pn-015).

<a id="static-information-proposals"></a>

## Static information decisions

Keep the machine number and add its move name in the bag, item PC, shops and prize lists. Preserve quantities and prices. Use the current build’s machine-to-move table.

INFO gives full static details on owned and offered moves in both presets. It can inform a purchase or one-use teaching decision. [Reader design](../docs/15-battle-information.md)

Descriptions must match Gen 1 behavior and the enabled developer profile. Do not import modern descriptions that promise Rock Slide flinching, later Tri Attack status effects, a physical/special split, or later trapping rules. Fixed/variable damage and status moves need truthful labels rather than misleading raw data bytes. Accuracy is a nominal move value, not a promise of the exact final hit chance under Gen 1's calculation. [MC13/MC16](../docs/05-mechanics-contract.md)

**Capacity counts:** use labels such as `BAG 18/20` and `BOX 7/20`. Bag and item-PC counts measure occupied entries, not item units or distinct item IDs. If two stacks of the same item occupy two entries, they count twice. PN-017 covers the active box. D53 adds the highlighted box’s count in CHANGE BOX. D55 keeps manual placement in the default games and offers automatic placement as an option. Recompute after changes, including a final unit removing a stack, and preserve the twenty-slot bag and twenty-Pokémon box limits.

These displays explain choices in the existing game. The checked sources do not establish why the developers omitted them. Live battle type indicators remain independently selectable. [Controls](../docs/15-battle-information.md)

## Audit correction and remaining evidence

The 47-call screen identifies nearby delivery checks. It does not establish every payment/reward ordering. The rooftop calls have such checks and still lose payment. The [call-site table](gift-call-sites.csv) now marks that verified fault explicitly and leaves other complete transactions unreviewed unless separately traced. Do not describe 45 nearby checks as 45 safe gifts.

Remaining research concerns specific proposal effects, legal-state reproductions, and incomplete comparisons. It does not reopen accepted requirements. No built ROM, executable regression, save mutation, or original-development interview was produced by this review.
