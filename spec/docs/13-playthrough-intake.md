# Playthrough findings

Keep new reports and accepted requirements here. Source confirmation, default inclusion, and implementation are separate states. The [feature catalog](14-features-and-extensions.md#feature-catalog) distinguishes these default requirements from accepted optional extensions. A report does not claim a tested game patch. These records supplement the archived bug catalog without changing its entry count.

| Note | Date | Requirement | Default disposition | Delivery |
|---|---|---|---|---|
| [PN-001](#pn-001) / RGB-029 | 2026-10-14 | EXP. ALL cannot be tossed or sold | Accepted item-safety safeguard | Implemented |
| [PN-002](#pn-002) | 2026-10-14 | Register a key item to SELECT, including the Bicycle | Accepted usability feature | Implemented |
| [PN-003](#pn-003) | 2026-10-14 | Browse the current box with a full party | Accepted usability feature | Implemented |
| [PN-004](#pn-004) | 2026-10-14 | Contextual HM prompts from A at a suitable target | Accepted interface feature | Implemented |
| [PN-005](#pn-005) / RGB-010c | 2026-10-14 | Correct Oak's geting spelling error | Accepted Core text correction | Implemented |
| [PN-006](#pn-006) | 2026-10-14 | Directional STATS navigation and page support | Accepted Core interface feature | Implemented |
| [PN-007](#pn-007) | 2026-10-14 | Clear release identity and No default | Accepted Core safety feature | Implemented |
| [PN-008](#pn-008) | 2026-10-15 | Return shop refusals and failed purchases to the relevant item list | Accepted Core interface feature | Implemented |
| [PN-009](#pn-009) | 2026-10-15 | Make party action-menu CANCEL return to the Pokémon list | Accepted Core interface feature | Implemented |
| [PN-010](#pn-010) / RGB-031 | 2026-10-15 | Correct selected vending-price checks | Accepted Core defect repair | Implemented |
| [PN-011](#pn-011) / RGB-032 | 2026-10-15 | Make Flute feedback reflect actual wake-ups | Accepted Core feedback repair | Implemented |
| [PN-012](#pn-012) / RGB-010b | 2026-10-15 | Correct the Raichu trade evolution claim | Accepted Core text repair | Implemented |
| [PN-013](#pn-013) | 2026-10-15 | Mark the current floor and prevent same-floor travel | Accepted Core interface requirement | Implemented |
| [PN-014](#pn-014) | 2026-10-15 | Left/right quantity steps of ten | Accepted Core control shortcut | Implemented |
| [PN-015](#pn-015) / RGB-030 | 2026-10-15 | Preserve rooftop payment when TM delivery fails | Core defect repair under the existing bug policy | Implemented |
| [PN-016](#pn-016) | 2026-10-15 | TM/HM names and move INFO before and after ownership | Minimal and Core under D61 | Implemented |
| [PN-017](#pn-017) | 2026-10-15 | Bag, item-PC and Pokémon-box capacity counts | Minimal and Core under D53/D62 | Implemented |
| [PN-018](#pn-018) | 2026-10-15 | Known and offered move INFO, optional live types | INFO in Minimal and Core. Live types are optional. | Implemented |
| [PN-019](#pn-019) | 2026-10-20 | Preserve item-list selection and scroll after actions | Accepted Core interface requirement | Implemented |
| [PN-020](#pn-020) | 2026-10-20 | Optional item capacity with a 64-slot bag target | Accepted Extension and separate reserve; save/runtime design pending | Not implemented |
| [PN-021](#pn-021) | 2026-10-24 | Retain the battle move cursor through SELECT reordering | Accepted Core interface requirement | Implemented |
| [PN-022](#pn-022) | 2026-10-24 | Append new boxed Pokémon consistently with deposits | Accepted Core usability policy | Implemented |
| [PN-023](#pn-023) | 2026-10-24; revised 2026-10-25 | Restore normal Mansion Burglar sight engagement | Accepted scoped Core correction; original intent unproven | Implemented |
| [PN-024](#pn-024) | 2026-10-25 | Viridian Forest star grass produces no encounters | Source-confirmed; accepted scoped Core correction | Implemented |
| [PN-025](#pn-025) | 2026-11-22 | Acid Armor leaves the active picture invisible | Stock ROMs confirmed. Restore the same sprite at animation end in Core under D41. | Implemented |

<a id="pn-001"></a>

## PN-001 — Protect EXP. ALL from tossing and selling

**Requirement:** refuse tossing EXP. ALL from the bag and player PC and selling it in shops. Toss attempts use the existing important-item refusal. Selecting it for sale shows the existing “I can't put a price on that.” message, as for the Bicycle, without a quantity/price offer or transaction. Preserve the item and money. PC deposit and withdrawal remain available. Keep the acquisition requirement and existing experience behavior.

**Evidence:** reported during a Red playthrough; source-confirmed at the pinned English Red/Blue reference. `EXP_ALL` has a false key-item flag. The shared toss routine protects HMs and key items, so EXP. ALL passes those guards. Oak's aide sets a reward event after giving it; subsequent conversations do not offer another copy when that event is set. The PC toss menu uses the same protected routine. [E68](../research/evidence.md#e68)

The follow-up playthrough report identifies selling EXP. ALL for zero. Its listed price is zero and its key-item flag is false. The shop checks key-item and HM status before offering a sale; confirmed sales then add the proceeds and remove the item. The Bicycle is flagged as a key item and takes the existing refusal path. A zero price alone does not give EXP. ALL that protection. These paths and the refusal text are source-checked, not an executable reproduction. [E74](../research/evidence.md#e74)

**Classification:** accepted default loss-prevention safeguard. Losing it does not block main-game progression. This record does not claim that the original flag was accidental.

**Proposed implementation:** change EXP. ALL's existing key-item flag from false to true. This uses the existing key-item guard for the required shop refusal as well as toss protection, and skips quantity prompts in PC transfers. Do not substitute a price increase or a blanket ban on selling all zero-price items. Check those paths; storage must still work. No item ID, save layout, battle calculation, or replacement-reward change is needed for this proposal.

**Regression requirements:**

- Bag and PC toss attempts refuse the action and leave inventory contents unchanged.
- PC deposit, withdrawal, full-storage rejection, and save/reload retain the item correctly.
- The aide still gives one copy under the existing requirement, with the original full-bag retry behavior.
- Carrying the item applies the existing experience behavior; storing it removes that effect. Core also corrects RGB-017, the independently verified double division of the second award. [EXP. ALL results](../research/foundation-audit.md#exp-all-gives-too-little-to-a-party-with-multiple-participants)
- Selecting EXP. ALL for sale gives exactly the existing important-item refusal, without offering a zero-price sale. Bag entries, quantities, and money remain unchanged, including on repeated attempts and after save/reload.
- Ordinary sales still remove the chosen quantity and pay the expected amount. Ordinary discardable items still work. Existing key items and HMs remain protected.

**Configuration:** provide a developer option if straightforward. Protection is enabled in the default core and does not depend on adding a toggle.

**Status:** The Bag, item PC and shop use the key-item safeguards. [Cartridge checks](../../tests/item_safety.py)

<a id="pn-002"></a>

## PN-002 — Register an item to SELECT

**Requirement:** register one eligible field-usable key item, then press SELECT in the overworld to use it without navigating the bag. The Bicycle is a required use case. Allow changing or clearing the registered choice. Keep normal menu use available.

**Evidence:** the checked overworld input handler handles START and A before directional checks, with no registered-item action. SELECT already swaps entries in item lists. The Bicycle effect rejects use in battle, while surfing, or where riding is not allowed. The item menu separately prevents getting off the Bicycle when `BIT_ALWAYS_ON_BIKE` is set. A shortcut must retain that menu guard as well as the effect's checks. [E69](../research/evidence.md#e69)

**Classification:** accepted default usability feature. This does not change when the Bicycle is earned, movement speed, map permissions, or combat rules.

**Proposed implementation:** add a register/clear action for eligible items and a context-aware overworld input path. Store the item ID, not its bag index. Use an explicit eligibility list; being a key item does not make a passive quest item usable. Reuse item-use behavior with shared validity checks rather than copying a Bicycle-only toggle. The exact menu layout and supported item list are implementation details; every advertised eligible item needs its own use case.

**Regression requirements:**

- Register the Bicycle and use SELECT to mount and dismount where allowed. A held button does not repeatedly toggle it.
- Refuse riding in prohibited places, while surfing, or without the Bicycle in the bag. Keep Cycling Road's forced-riding restriction.
- Menus, dialogue, battles, scripted movement, and transitions do not trigger the overworld shortcut. Existing SELECT menu controls still work.
- Changing or clearing registration works. Reordering the bag keeps the same registered item. Depositing it prevents shortcut use while it is absent.
- Save/load retains a valid choice. New games and supported imports without registration start safely with no item registered. Invalid stored IDs cannot dispatch an arbitrary item effect.
- Other advertised eligible items use their normal checks and behavior. Passive key items cannot be registered as usable items.

**Configuration:** enabled in the default core. Provide developer configuration when straightforward. Registering an item is a player control, not a choice between competing battle rules.

**Status:** The Bicycle is eligible in both presets. The game saves its item ID and checks the Bag before use. [Cartridge checks](../../tests/bicycle_shortcut.py)

<a id="pn-003"></a>

## PN-003 — Browse the box with a full party

**Requirement:** choosing WITHDRAW at Bill's PC opens the current box list even when the party is full. Selecting a Pokémon still offers the existing WITHDRAW, STATS, and CANCEL actions. Only choosing WITHDRAW for that Pokémon triggers the existing full-party error. Browsing, viewing stats, and cancelling remain available. Leaving STATS or cancelling the selected-Pokémon action returns to the Pokémon list, retaining its selection and scroll context. Apply the same return behavior to the accessible DEPOSIT browsing flow without changing its eligibility or transfer rules.

**Evidence:** `BillsPCWithdraw` checks `wPartyCount` against `PARTY_LENGTH` before `DisplayMonListMenu`, blocking the list when the party has six members. The selected-Pokémon menu already supports STATS and returns carry only for the deposit/withdraw action. The withdrawal path then calls `MoveMon` and `RemovePokemon`. The existing capacity error asks the player to deposit Pokémon first. [E70](../research/evidence.md#e70)

**Classification:** Minimal and Core may browse before checking room in the party. Both keep manual box selection. A direct MOVE POKÉMON interface and automatic placement remain separately selectable. [Storage choices](14-features-and-extensions.md#storage-extensions)

**Proposed implementation:** move the full-party check after `DisplayDepositWithdrawMenu` returns an actual withdrawal choice, before the transfer or removal calls. Reuse `CantTakeMonText`. Cancellation and STATS must not reach this guard. Retain the existing empty-box response and ordinary successful-withdrawal path. Preserve list context separately from the selected-Pokémon action menu, which currently resets shared cursor/scroll state. Returning from STATS and action cancellation must reach the list rather than BillsPCMenu. [E83](../research/evidence.md#e83)

**Regression requirements:**

- With six party members and a nonempty box, WITHDRAW opens the list. STATS displays the selected boxed Pokémon and returns to the list at that Pokémon, retaining scroll position.
- Choosing the selected Pokémon's WITHDRAW action with a full party shows the existing error. Party and box counts and Pokémon records remain unchanged.
- Cancelling the list or selected-Pokémon menu causes no capacity error or data change. Repeated browsing and failed withdrawal remain usable.
- With fewer than six party members, withdrawal transfers exactly the selected Pokémon and removes exactly that box entry. Check first, middle, and last entries and retained Pokémon data.
- An empty box keeps its existing message. Deposit eligibility, successful transfer destinations, and change-box behavior remain unchanged; only the specified browsing returns change.
- Save/reload after browsing or a refused withdrawal retains the original party and box contents. No save-format change is required by this proposal.
- Check action-menu B and CANCEL, first/middle/last visible rows, and a scrolled full box. After navigation, returning to the list highlights the Pokémon last viewed; no transfer occurs. Repeat within the accessible DEPOSIT list.

**Configuration:** enabled in the default core. Provide developer configuration when straightforward; a toggle is not required to deliver the feature.

**Status:** The list opens with a full party. The capacity check runs when the player chooses a Pokémon to withdraw. [Cartridge checks](../../tests/pc_browsing.py)

<a id="pn-004"></a>

## PN-004 — Contextual HM use

D54 includes these shortcuts in Minimal and Core. The party-menu commands remain available. The [field-action contract](../research/field-shortcut-contract.md) covers object priority, valid targets and actor checks.

**Requirement:** press A while facing a suitable field-move target, then confirm whether to use the move. Choose a party Pokémon that knows the move without opening the Pokémon menu. Cuttable trees, Surf entry from a valid shore, and Strength activation at a boulder are required cases. Keep manual party-menu use available.

**Classification:** accepted Core interface improvement. Preserve the need to teach and carry the move, its use of a move slot, the required badge, valid targets, and existing map/progression restrictions. The shortcut does not grant an HM ability merely because the player owns the HM item or has once learned the move. Do not add an HM-item possession requirement where the existing move use does not have one.

**Evidence:** the party menu builds field-move options from the selected Pokémon's moves. It checks badges before Cut, Fly, Surf, Strength, and Flash. Surf also calls a map-permission routine before the Surfboard effect checks shore/water and tile-pair collisions. Cut checks the facing tile and tileset; Strength activates a state bit, with boulder movement handled separately. The A-button interaction path already handles hidden events, objects, and signs. These are separate checks and contexts; calling a low-level effect alone is insufficient. [E73](../research/evidence.md#e73)

**Proposed implementation:** add a context-aware interaction path and share field-move validation with the menu. Refresh the facing target, find an eligible party user, set the same selected-Pokémon state used by the menu, and show a Yes/No prompt. Revalidate before applying the effect. Preserve existing interaction priority and guard against scripted input. The routine split and exact text are engineering choices.

| HM | Scope of this requirement |
|---|---|
| Cut | A at a cuttable tree, including existing gym trees, asks to use Cut. Preserve existing manual Cut use on grass. Do not prompt at every grass tile. |
| Surf | A at a valid shore while facing water asks to begin Surf. Retain map, forced-riding, current, and collision restrictions and existing dismount behavior. |
| Strength | A at a boulder asks to activate Strength when needed. Keep existing pushing and puzzle rules; an A press does not itself move the boulder. |
| Fly / Flash | Keep existing menu use and restrictions. These actions do not have the same facing-object context in the checked implementation. Their existing menu paths remain available; this requirement specifies no new trigger for them. |

**Regression requirements:**

- For each required shortcut, an eligible party and badge give the prompt. Yes performs the same action as menu use; No/B and held A do not trigger or repeat it.
- Missing the move, missing the badge, an invalid target, or a prohibited context cannot perform the action. Keep the menu's existing eligibility rules, including its treatment of party status. Do not add a new PP charge or bypass a move-slot cost.
- Party search selects a correct user and name with one or several eligible Pokémon, after party reordering, and after the only eligible user leaves the party.
- Cut handles outdoor/gym trees without affecting decorative trees or existing grass-cutting behavior. Reloading the map retains the normal tree-reset rules.
- Surf observes shore/tile-pair checks, Cycling Road restrictions, Seafoam current conditions, and normal mount/dismount states. No shortcut can strand the player or surf through a blocked tile.
- Strength activation retains map/reset behavior, boulder collision, the existing pushing sequence, and puzzle events. Repeated interaction while active does not reset or move a boulder.
- NPCs, signs, hidden items, doors, dialogue, battles, transitions, and scripted movement keep their behavior. Test prompts beside overlapping interaction targets.
- Menu use still works. Check relevant progression gates, return visits, and save/reload; no acquisition, badge, party, or move data changes arise from merely opening or cancelling a prompt.

**Configuration:** enabled in Core. Provide a developer control when straightforward; it is not a player rule setting or a prerequisite to deliver the feature.

**Status:** The field offers Cut, Surf, and Strength through A at eligible targets. [Surf and Strength checks](../../tests/field_shortcuts.py) · [Route 14 Cut check](../../tests/route_cut_tree.py)

<a id="pn-005"></a>

## PN-005 — Correct Oak's Pokédex rating typo

**Requirement:** correct geting to getting in Oak's 60–69-owned-species rating. Unambiguous typos are Core corrections under D06 and the [text policy](03-bug-fix-policy.md#typo-corrections).

**Evidence:** the pinned English Red/Blue text contains the reported misspelling. The PC calls the shared rating routine, which counts owned species and selects this rating for 60–69. Oak's Lab and the Hall of Fame also call the routine. [E82](../research/evidence.md#e82)

**Scope and display check:** add the missing letter and reflow the text as needed, retaining the rest of the sentence. The original first line has 18 characters; adding the letter directly produces 19. Check text width, scrolling, and completion in all three display paths. Keep thresholds, neighboring ratings, counts, and other game behavior unchanged. This is a narrow text edit; no new game test harness is needed.

**Delivery:** accepted and source-confirmed; no game text patch or rendered/game display check has been completed in this specification repository. The cause of the original spelling is unknown.

<a id="pn-006"></a>

## PN-006 — Navigate STATS by Pokémon and page

**Requirement:** up/down selects the previous/next Pokémon in the available party or current-box list, retaining the selected page. Left/right selects pages for the same Pokémon. B leaves any STATS page for its browsing context. Restore the Pokémon last viewed and keep list scroll position where possible. The default keeps the two existing pages and their information.

**Developer support:** adding a page must reuse the navigation controls. DV and stat EXP pages are future extension examples, not default information or first-release content requirements. A small page table or equivalent is an implementation proposal; no general plug-in framework is required.

**Evidence:** the original pages wait for A/B, and party, PC, battle, and trade callers invoke both in sequence. The PC caller has the separate return-path issue covered by PN-003. [E83–E84](../research/evidence.md#e83)

**Acceptance:** test one-member and full parties; one-entry and full/scrolled boxes; first/last entries; both pages; B from each page; page retention when changing Pokémon; and returning to the correct highlighted entry. Test empty contexts without reading nonexistent entries. A temporary third page must use the same controls. Protect battle replacement rules and trade context. Browsing must not transfer, release, switch, or alter Pokémon data.

**Delivery:** accepted Core feature; no game controller, added page, or executable regression is implemented. See the [menu inventory](../research/menu-navigation.md) and [test plan](07-testing-ci.md#stats-and-menu-regression-coverage).

<a id="pn-007"></a>

## PN-007 — Safer Pokémon release confirmation

**Requirement:** clearly show the selected Pokémon's nickname and species before release, default confirmation to No, and remove it only after an explicit Yes. B or No leaves the Pokémon unchanged and returns to the release list. Preserve intentional release.

**Evidence:** the PC calls the standard Yes/No initializer, which selects the first option by default. The release branch removes a Pokémon only after checking the result; refusal already returns to the release list. Apply the new default to this caller, preserving other Yes/No prompts. [E85](../research/evidence.md#e85)

**Acceptance:** check nicknames that hide the species, duplicate nicknames, first/last entries, scrolled lists, repeated A input at prompt entry, B/No, and explicit Yes. Refusal changes no records or counts; confirmation releases exactly the identified Pokémon once. Check text width and ordinary shop/healing prompt defaults. A release must not use a stale index left by STATS navigation.

**Delivery:** accepted Core safety feature; no game patch or executable confirmation test is implemented.

<a id="pn-008"></a>

## PN-008 — Keep the item list after a shop refusal

**Requirement:** after refusing an unsellable item, return to the SELL list. After a purchase fails for insufficient money or bag space, return to the BUY list. Retain the selected item and scroll position. Keep the refusal message and require a new explicit choice before attempting any transaction.

**Evidence:** the checked original paths send these cases to BUY/SELL/QUIT. Quantity cancellation, final price refusal, and completed transactions already loop back to the respective item lists. Those existing loops are narrow implementation candidates; review their cursor state before reusing them. [E86](../research/evidence.md#e86)

**Scope:** preserve prices, quantity limits, bag capacity and stacking, key-item/HM protection, confirmation, and normal exit behavior. A refusal or failed purchase changes no money, inventory, or completed-transaction state. EXP. ALL sale protection continues to use its existing important-item message. Empty SELL lists keep their existing response and return to the main shop menu.

**Acceptance:** check key items, HMs, and protected EXP. ALL; insufficient money; full bag/new stack; quantity limits; and valid additions to an existing stack. Check selected first/middle/last items and scrolled lists. After refusal, selecting another item must work without an automatic retry. B from the item list still returns to BUY/SELL/QUIT. Preserve quantity cancellation, declining the price, ordinary successful buys/sales, and empty-bag handling.

**Delivery:** accepted Core interface feature. Source paths were rechecked on 2026-10-15. No game patch or executable shop regression is implemented.

<a id="pn-009"></a>

## PN-009 — Return party action-menu CANCEL to the Pokémon list

**Requirement:** in Start → POKéMON → choose a Pokémon, selecting CANCEL returns to the party list with the same Pokémon highlighted, matching B.

**Evidence:** the original overworld action menu sends B to the party-list loop and CANCEL to the exit path that restores Start. These explicit branches establish the mismatch, not the original team's reason for it. Reusing the B destination is a narrow implementation candidate; selection and screen restoration still need game checks. [E86](../research/evidence.md#e86)

**Scope:** include this interface repair in Core. Preserve B from the party list to Start, STATS, SWITCH, field moves, and other callers' cancellation rules. This is not a global rule to change every CANCEL destination.

**Acceptance:** check one, two, and six party members, first/middle/last selections, and action menus with and without field moves. Both cancellation methods must retain the selected Pokémon and leave party records unchanged. Check repeated cancellation, choosing a different Pokémon afterwards, normal actions, and the normal party-list exit. Preserve battle, forced-replacement, item-targeting, trade, and PC flows.

**Delivery:** accepted Core interface feature. No game patch or executable menu regression is implemented.

<a id="pn-010"></a>

## PN-010 — Vending affordability

**Requirement:** compare funds with the selected price: Fresh Water ¥200, Soda Pop ¥300, Lemonade ¥350. A successful delivery deducts that price once. Insufficient money or space gives no drink and takes no money. Keep the original effects, stack rules, and cancellation.

**Evidence/status:** source-confirmed wrong ¥200 guard; explicitly accepted Core repair. The original underpayment path clamps money to zero, rather than wrapping it. [E89](../research/evidence.md#e89) No game patch is implemented.

**Regression:** each price minus one, exact price, and price plus one; ¥0/199/200/299/300/349/350; full bag with and without room in an existing stack; cancel; repeated purchases; displayed balance and actual item/money changes. Protect inventory boundaries separately.

<a id="pn-011"></a>

## PN-011 — Truthful Flute feedback

**Requirement:** feedback must reflect actual sleep cleared, including when only the wild opponent is asleep. Keep the existing wake targets and turn cost. This does not approve a contextual Snorlax prompt or different sleep rules.

**Evidence/status:** the source clears the wild opponent's sleep after party scans but does not set the response flag from that change. It can omit wake-up confirmation and show the alternate catchy-tune response. It does not literally say “no effect.” [E94](../research/evidence.md#e94) Explicitly accepted Core feedback repair; not implemented.

**Regression:** opponent alone asleep, party alone asleep, both, neither, trainer battle, unused party slots, and other status bits. Compare statuses, text, sound, action cost, and RNG use.

<a id="pn-012"></a>

## PN-012 — Raichu trade follow-up

**Requirement:** the follow-up must not claim Raichu evolved. Preserve species, nicknames, rewards, and evolution rules. The shared dialogue must remain truthful for its other user, the Poliwhirl→Jynx trade.

**Evidence/status:** both trade entries use the evolution dialogue set. Its statement about the Pokémon given to the NPC conflicts with retained Raichu data. [E91](../research/evidence.md#e91) Explicitly accepted Core text repair; not implemented. A precise English edit can be selected during implementation.

**Regression:** both users, other dialogue sets, first and later visits, name substitution, and rendered line layout. No added Raichu evolution or changed trade species.

<a id="pn-013"></a>

## PN-013 — Current elevator floor

**Requirement:** indicate the actual current floor in the floor menu. Selecting it must not trigger travel animation, travel sound, or destination changes. Prefer an entry that cannot be selected or that navigation skips. Preserve all other floors and cancellation.

**Evidence/status:** Red/Blue's shared menu treats a noncancel destination as travel without a same-floor exclusion. FireRed displays the current floor and skips animation for a same-floor Department Store selection, while still allowing that entry to be chosen. [E103](../research/evidence.md#e103) Explicitly accepted Core interface requirement; not implemented.

**Design/checks:** derive the entered floor from the actual entrance/destination state, not the elevator map ID or a stale cursor. Check every floor in the Department Store, Silph Co., and Rocket Hideout; first entry, consecutive trips, cancellation, and save/reload. Same-floor input must leave warp state unchanged; a real trip must still arrive correctly with its normal presentation. Preserve valid list navigation when the current floor is first/last or off the initial visible page.

<a id="pn-014"></a>

## PN-014 — Quantity changes of ten

**Requirement:** left decreases ten and right increases ten in the shared quantity selector. Preserve up/down unit steps and their wrap behavior, A confirmation, B cancellation, item limits, affordability checks, and transaction validation.

**Proposed endpoints:** left clamps at one, right at the current maximum, as in the checked Gold/Silver and FireRed handlers. Recompute displayed totals after any change. An unchanged endpoint must not accidentally confirm the action. This is a control change, not automatic purchase of the maximum.

**Evidence/status:** Red/Blue handles unit steps but ignores left/right here. Both comparison games provide tens. This does not establish a universal rule across every later game. [E103](../research/evidence.md#e103) Explicitly accepted Core shortcut; not implemented.

**Regression:** maxima 1, 2, 9, 10, 11, and 99; quantities around 1/10/11 and the maximum; repeated/held input; up/down wrap after a tens change; price totals; cancellation; and one transaction per confirmation. Cover shop buy/sell, bag toss, and item-PC deposit/withdraw/toss callers. Keep key-item paths that skip quantity selection.

<a id="pn-015"></a>

## PN-015 — Rooftop drink/TM exchange

**Requirement:** a drink exchange either takes one drink and gives its one-time TM, or preserves the drink, TM inventory, and reward flag. Keep Fresh Water→TM13 Ice Beam, Soda Pop→TM48 Rock Slide, and Lemonade→TM49 Tri Attack. Permit a valid exchange where the final drink frees the needed slot.

**Evidence:** all three scripts remove payment before `GiveItem`. With twenty occupied slots, at least two drinks in the selected stack, and no target TM stack with space, delivery fails after payment. With a final drink in that stack, removal frees a slot. A spare slot is therefore not always necessary. The reward flag is set only after successful delivery. The checked ordinary path does not prove duplication; retrying an undelivered reward is not an extra TM. [E101](../research/evidence.md#e101)

**Classification/status:** source-confirmed exchange defect, included under D06/D30. The reported duplication remains unverified and requires its own sequence. No game fix is implemented. A nearby-guard screen does not establish payment order; [the comparison](../research/remake-usability-comparison.md#rooftop-transaction-boundary) records that correction.

**Proposed design:** check capacity for the final exchange state, then commit safely, or use a verified rollback. Do not reject all full bags before accounting for the drink slot. Review stack insertion/splitting separately; a helper's success/failure branch is not by itself proof of atomicity, meaning all changes succeed together or none take effect.

**Regression:** every drink; 19/20 occupied slots; drink stack 1/2; absent target TM, existing TM stack with room, and 98/99 boundary stacks; other duplicate stacks where supported; completed reward, cancel, retry, repeated talk, and save/reload. Check exact drink/TM quantities and event bits on success/refusal. No payment loss, accidental duplicate reward, or false success text. Use disposable fixtures and supported saves.

<a id="pn-016"></a>

## PN-016 — TM information

Minimal and Core show the machine number and move name, with START for full INFO, in the bag, item PC and any shop or prize list offering a machine. INFO also covers a Pokémon’s known moves and a pending move-learning decision. [D61 and controls](15-battle-information.md)

**Evidence:** move identity is already revealed before teaching and by some NPCs. The battle move menu already shows type and PP. The checked original interfaces lack a general power/accuracy/effect reference. FireRed supplies that information in its TM Case and shows TM move names in its shop; Gold/Silver also adds names/descriptions. These observations do not establish the original team's reason for omission. [E102](../research/evidence.md#e102)

**Contract and checks.** Use the enabled machine/move data; keep machine IDs, prices, quantities, original learnability, and single-use TMs. Cover the bag, item PC, relevant shops/prizes, long names, and developer-edited tables. Reference fields are name, type, base power, nominal accuracy, base PP, and an accurate Gen 1 effect description. Fixed/variable damage and status moves need meaningful labels. Browsing does not buy, teach, consume, or change data. See [the original and remake comparison](../research/remake-usability-comparison.md#static-information-proposals).

<a id="pn-017"></a>

## PN-017 — Capacity counts

Minimal and Core show occupied places and capacity in the bag, item PC and active Pokémon box. The box chooser also shows the highlighted box’s occupancy under D53.

For example, show BAG 18/20, ITEM PC 42/50 and BOX 7/20. Bag and item-PC counts measure stacks. Each occupied duplicate stack counts. These totals grant no storage. [Original limits](../research/evidence.md#e103)

**Checks:** empty, nearly full, full, final-unit removal, stack split/merge, transfers, capture into the active box, changing boxes, and save/reload. Counts must reflect the live records and the configured limit. Show occupancy in the existing twelve-box chooser under D53. D55 keeps the choice of capture destination independent of count display. Verify original-screen readability and unchanged save data/capacity behavior.

<a id="pn-018"></a>

## PN-018 — Move INFO and optional live types

Both presets include static INFO for a move currently offered, known or selected. Live types for the two active battlers remain an independent developer option. D61 supersedes the earlier extension-only placement for viewing one’s own move. [Input and release tests](15-battle-information.md) · [Emerald Expansion precedent](../research/evidence.md#e104)

<a id="pn-019"></a>

## PN-019 — Keep item-list position after actions

**Requirement:** preserve selection and scroll when returning to the same item list after item-PC deposit, withdrawal, or toss; bag item use or toss; and shop buy/sell actions. This includes temporary quantity/confirmation prompts, cancellation, refusal, and completed actions that already return to that list. Keep the previously accepted menu destinations, including medicine returning to the bag. This does not authorize keeping a target selector open or changing successful Pokémon-transfer destinations.

**Position after changes:** if the selected entry remains, keep that exact entry and viewport. If it is removed, select the entry that takes its place; if it was last, select the preceding item. Preserve the old viewport when that choice remains visible and valid; otherwise move it only enough to show the selected entry without invalid rows. An empty list must have a valid empty/cancel state and follow its caller's exit policy. Do not jump to the top merely because a count changed.

**Evidence:** the pinned Red/Blue item-PC loops already return to the correct lists. The shared inventory-removal routine resets both current and saved row/scroll values when the last unit of a stack is removed. It skips that reset when units remain. Withdrawals, sales, and tossing also use the routine. Shop buy/sell loops separately reset the visible cursor row, even when returning from quantity cancellation or a declined price. A destination-only review missed these separate state changes. [E106](../research/evidence.md#e106)

**Classification/status:** accepted Core usability requirement. This removes repeated navigation while retaining inventory management, quantities, prices, capacity, item consumption, and confirmations. Source-confirmed at the retained reference; no game patch or runtime check is implemented.

**Proposed design:** each list owner retains its own list identity, selected entry, visible row, and scroll offset across child menus and data changes. Restore a valid position after applying the known mutation. Two stacks of the same item are separate entries; an item ID alone is insufficient. Do not simply remove every reset from the shared inventory routine: scripted rewards, battles, and other callers may depend on its current behavior. Review those callers before changing the helper. Cursor state can remain temporary; no new saved field or cross-session position promise is required.

**Acceptance:**

- Deposit several items near the bottom of a full bag in sequence. Check partial stacks, complete stacks, key items, and duplicate stacks. The next item must be accessible without scrolling down again.
- Cover PC withdrawal/toss, bag use/toss, and shop buy/sell returns. Check both quantity cancellation and declined confirmations, protected-item refusals, insufficient funds/capacity, and successful actions. Existing PN-008 refusal destinations remain required.
- Check first/middle/last entries, every visible row, empty/one-entry lists, 20-slot bag and 50-slot item PC boundaries, and repeated deletion through the end. No off-list cursor, stale index, or automatic follow-up action is permitted.
- Verify each chosen item, exact quantity, inventory order, money, and refusal state. A held confirmation button must not act on the new adjacent item. Keep unrelated list contexts separate and recheck non-list callers of shared removal.
- Preserve medicine's return to the bag, ordinary B exits, successful Pokémon-transfer destinations, and existing save data. These are future game checks; specification validation does not establish them.

<a id="pn-020"></a>

## PN-020 — Optional item-capacity expansion

**Accepted direction:** offer larger item capacity as a developer Extension, disabled in Core. The selected preset is a 64-slot bag. Keep bag and item-PC capacity independent: enabling the bag preset must not silently enlarge the PC or add pockets, sorting, reusable items, or other storage features. Core retains 20 bag slots and 50 item-PC slots. A 60-slot PC is a separate possible configuration; its layout is not established by the bag tutorial.

**Scope:** count occupied item stacks, not individual units. Retain the per-stack quantity limit, item identity, key-item protection, prices, effects, and acquisition rules. This is a capacity choice, not part of the default scroll-position repair. Keep the accepted PN-019 navigation behavior at each supported capacity.

**Verified allocation:** the original bag has no adjacent spare space: money immediately follows its 42-byte allocation. A separate 134-byte reserve at `$D66A–$D6EF` can hold a four-byte format marker, count, 64 two-byte entries, and terminator. A RAM-only link check passes for 60 and 64 there, preserves every other existing WRAM label, and rejects 65 by an allocation assertion. The selected 64-slot preset uses all 134 bytes including the marker, leaving no spare bytes in this block. This is a different reserve from the earlier 128-byte tutorial example; it is not a gameplay or save-conversion result. [E108](../research/evidence.md#e108)

**Accepted allocation design:** move only the enabled live bag into the separate 134-byte reserve. Keep the original 42-byte footprint, all other field addresses, total block sizes, and the intervening `wGameProgressFlagsEnd` boundary fixed. Core keeps its original layout when disabled. Assign the entire reserve to this feature, declare its address range and build conditions, and reject overlapping enabled allocations. Select 64 slots and assert the full 134-byte bound. Any future format growth must fit a separately reviewed allocation; it must not extend into neighboring fields. Check every index, copy, initialization, terminator, bulk access to the former reserve, and list caller before advertising support. See the [allocation contract](../research/bag-memory.md).

**Initialization:** initialize the enabled bag and its format marker after the game-progress clear, which otherwise overwrites their initial values in this reserve. Keep the original progress boundary fixed. [E109](../research/evidence.md#e109)

**Saves:** relocation changes the bag's saved location even if other offsets stay fixed. Publish a capacity/layout identifier and the actual compatibility policy before release. Use an explicit tested conversion for supported imports, or clearly require a fresh save for the enabled layout. Never reinterpret an old or differently configured save silently. Do not use the tutorial's deposit-items workaround as a migration design. The disabled profile must keep its promised save behavior.

**Acceptance:** test Core and the bag-64/PC-50 profile; test other PC settings independently and in combinations only if advertised. Verify entries 20/21 and 63/64, refusal of entry 65 as a new stack, addition to an existing stack while full, stack splitting and duplicates, insertion/removal, toss/use, shops, ground/scripted rewards, rooftop exchanges, registration, and PN-019 list retention. A supported capacity counter must show the configured denominator. Check guards around allocations, unchanged other-field addresses, single reserve ownership, overlap rejection, neighboring saved fields, new-game initialization after the progress clear, save/reload, supported imports, disabled-state behavior, advertised feature combinations, and original Game Boy builds. No game implementation, configured build, runtime regression, or safe conversion is claimed yet.

<a id="pn-021"></a>

## PN-021 — Retain the battle move cursor during SELECT reordering

The original cursor also writes move history that enemy Counter reads. Keep the stock interaction in Minimal until equivalence is verified. Test this side effect before shipping the Core cursor change, including marking a move, cancelling and switching without completing the swap. [Measured turns](../research/minimal-action-review.md)

**Requirement:** retain the cursor row when SELECT marks a move and when a second SELECT completes the swap. Marking move three leaves the cursor on three. Moving to four and pressing SELECT swaps three/four and leaves the cursor on four. Keep the source marker visible and separate from the active cursor. A repeat SELECT on the source is a no-op swap with the existing completion behavior.

**Evidence:** both SELECT paths jump back to the menu initializer, which restores a previous `wPlayerMoveListIndex`. The result is often move one, but the source does not hard-code a first-row reset. [E110](../research/evidence.md#e110)

**Classification/status:** accepted Core interface requirement. This is the same position-retention principle as PN-019, applied to a list without scrolling. No game patch or runtime regression is included.

**Implementation boundary:** preserve the current cursor across the redraw without treating SELECT as an attack choice. Retain the existing battle/party move and complete PP-byte swaps, Disable slot/duration handling, and A/B behavior. Keep existing rules for Transform, Mimic, empty move slots, unavailable moves, and link battles. Cursor storage must not change battle-history semantics or another caller's menu state.

**Acceptance:** check first/middle/last rows, two through four moves, a one-move no-op, same-slot selection, repeated swaps, and cancellation. Test three↔four with an earlier remembered selection at both one and two. Verify battle and party move/PP arrays, PP Up bits, and disabled-slot duration/index. The operation must consume no turn or PP and add no random draw. Test transformed/copied moves and preserve link input restrictions. A and B must keep their existing actions; opening a genuinely new menu may still initialize its own context.

<a id="pn-022"></a>

## PN-022 — Use consistent append order for boxed arrivals

**Requirement:** append newly caught Pokémon sent to the current box after its existing members, matching party deposits. Apply the same insertion rule to gifts that already use the new-boxed-Pokémon routine. Keep all existing members in their current positions. Never reorder an existing saved box merely on load.

**Evidence:** `SendNewMonToBox` prepends captures and boxed gifts, shifting the species list, original-trainer names, nicknames, and records. It names slot one directly. `_MoveMon` appends party deposits. The ordering difference is source-confirmed; its original design reason is not established. [E111](../research/evidence.md#e111)

**Classification/status:** accepted Core usability policy. Consistent append behavior preserves existing positions and all storage limits. Record it as a project choice, without claiming proof of an original programming error. The game change and runtime tests remain unimplemented.

**Implementation boundary:** give every part of the new boxed Pokémon the same destination index, including the nickname prompt and full record. Preserve species, OT, ID, nickname, level, experience, DVs, stat experience, moves, PP, and status according to the existing acquisition rules. Use the selected preset’s destination check. Preserve gift eligibility and completion, the six-member party, twenty members per box, confirmed box-change saves, transfer rules, and removal compaction. This adds no automatic box switching, sort, or MOVE POKÉMON feature and requires no new saved field.

**Acceptance:** with distinct existing members A/B/C, capture D into a full-party box and require A/B/C/D; deposit E and require A/B/C/D/E. Cover empty/one/19-entry boxes, the 19→20 boundary, the active-box refusal in both reference presets and the all-boxes-full refusal with automatic placement enabled, repeated captures, boxed gifts, nickname Yes/No, duplicate species/nicknames, and exact OT/record identity. Check withdrawal/release, save/reload, and box changes without reordering old members. Party arrivals keep their existing behavior. Test automatic capture storage and MOVE POKÉMON only in supported combinations; their absence must not block this Core feature.

<a id="pn-023"></a>

## PN-023 — Correct Mansion Burglar sight engagement

**Requirement:** the three Mansion Burglars on 2F, 3F, and B1F initiate battle through the normal sight check when undefeated, visible, facing the player, aligned, and within range. Talking must still work. Preserve the Scientists' existing settings and every other zero-range trainer.

**Evidence:** the original three Burglar ranges are zero; the Scientists' ranges are three, two, and three. All four floors use the normal sight routine. [E112](../research/evidence.md#e112) Yellow retains the zero values, while FireRed/LeafGreen gives all three Burglars range one. [E113](../research/evidence.md#e113) The Route 21 Fishers face adjacent water, which limits that analogy. [E114](../research/evidence.md#e114)

**Classification/status:** accepted scoped Core correction under D39. Treat the passive behavior as a likely oversight for this project. The original developer intent and the reason for the remake change remain unproven. This supersedes the earlier preserve-in-Core disposition for these three Burglars; it does not change the general uncertain-change policy. No game implementation or runtime test is included.

**Proposed implementation:** set each of these three view ranges to one, following the remake's minimal positive range, and use the existing engagement path. Keep trainer classes, parties, levels, rewards, dialogue, movement patterns, map layout, switches, doors, and defeat flags unchanged. Do not enable sight battles for all zero-range trainers or replace the trainer engine.

**Acceptance:** exercise all three Burglars at the proposed range, including facing/alignment, hidden or off-screen states, talking, and post-defeat behavior. Check the two wandering Burglars while moving and at movement boundaries. Battle must start once, restore valid map state, and award the existing reward once. Confirm that engagement and post-battle position do not block an exit, corner the player, or bypass a gate. Test narrow paths and the 3F table area. Preserve ordinary Scientist sight, map progress, save/reload, and unrelated zero-range trainers such as the Route 6 pair and Route 21 Fishers. These are release requirements, not completed checks.

<a id="pn-024"></a>

## PN-024 — Recognize Viridian Forest star grass for encounters

**Report:** some grass squares in Viridian Forest never produce wild encounters. The supplied [GameFAQs report](https://gamefaqs.gamespot.com/gameboy/367023-pokemon-red-version/faqs/64175/viridian-forest-encounter-rate-glitch) describes the star pattern and says Yellow is unaffected. Its text was available through the search index; the direct page fetch failed. The conclusion below was checked independently against source.

**Evidence:** Red/Blue checks the lower-right graphic tile for grass encounters. The Forest's star-pattern squares have ordinary grass at lower-left and decorative `0x34` at lower-right. The sprite code treats them as grass; the encounter gate rejects them. Yellow reads lower-left, with identical Forest map and blockset bytes and the same grass ID. The decoded map has 114 affected squares. [E115](../research/evidence.md#e115)

**Disposition:** source-confirmed mismatch; accepted scoped Core correction under D40. Treat the encounter effect as a likely oversight. Original intent is strongly inferred from the internal mismatch and Yellow comparison, without an original developer statement. This review does not claim game implementation or runtime reproduction.

**Required behavior:** affected grass can produce encounters under the existing rate, tables, species, levels, slot weights, and Repel rules. Preserve graphics, map layout, and ordinary non-grass paths. Review a narrow Forest recognition change against the broader Yellow corner change before choosing code; do not silently combine the separate Cinnabar-shore case.

**Acceptance:** check all affected and ordinary grass squares, controlled encounter thresholds, slot selection, Repel, direction changes, warps, scripted movement, and post-battle return. Check water, shores, Safari Zone maps sharing the tileset, and all three project variants. Preserve unrelated random-number behavior and save format. See the [review](../research/forest-encounters.md).

<a id="pn-025"></a>

## PN-025 — Acid Armor picture visibility

Acid Armor can leave an active battler or its Substitute invisible across later turns. When battle animations run, its dedicated sinking animation clears the picture from video memory. The user still gets the normal Defense increase and can take damage. Checks in the English Red, Blue, and Yellow ROMs confirm the behavior. [E116](../research/evidence.md#e116)

The original Japanese releases have the same animation. Viewing STATS in the battle party menu reloads the enemy picture while its Defense boost stays active. Haze can remove the Defense boost while the picture stays blank. Gold and Silver and the remakes restore the picture at animation end. A missing restoration is the best fit for this evidence. The intended duration in Gen I remains unknown. [E117](../research/evidence.md#e117), [E119](../research/evidence.md#e119)

Accepted for Core under D41. Keep the original melt. At animation end, restore the sprite that was visible when the melt began. Preserve the move mechanics and battle animation setting. Implementation and regression tests are pending. [Test plan](07-testing-ci.md#acid-armor-picture-checks)
