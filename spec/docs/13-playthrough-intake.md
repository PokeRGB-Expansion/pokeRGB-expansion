# Playthrough findings

Each entry records the original behavior, the preset decision and its checks. The [feature catalog](14-features-and-extensions.md#feature-catalog) includes later additions and planned extensions.

| Note | Date | Requirement | Default disposition | Delivery |
|---|---|---|---|---|
| [PN-001](#pn-001) / RGB-029 | 2026-10-14 | EXP. ALL cannot be tossed or sold | Minimal and Core | Implemented |
| [PN-002](#pn-002) | 2026-10-14 | Register the Bicycle or a fishing rod on SELECT | Minimal and Core | Implemented |
| [PN-003](#pn-003) | 2026-10-14 | Browse the current box with a full party | Minimal and Core | Implemented |
| [PN-004](#pn-004) | 2026-10-14 | Contextual HM prompts from A at a suitable target | Minimal and Core | Implemented |
| [PN-005](#pn-005) / RGB-010c | 2026-10-14 | Correct Oak's geting spelling error | Minimal and Core | Implemented |
| [PN-006](#pn-006) | 2026-10-14 | Directional STATS navigation and page support | Minimal and Core | Implemented |
| [PN-007](#pn-007) | 2026-10-14 | Clear release identity and No default | Minimal and Core | Implemented |
| [PN-008](#pn-008) | 2026-10-15 | Return shop refusals and failed purchases to the relevant item list | Minimal and Core | Implemented |
| [PN-009](#pn-009) | 2026-10-15 | Make party action-menu CANCEL return to the Pokémon list | Minimal and Core | Implemented |
| [PN-010](#pn-010) / RGB-031 | 2026-10-15 | Correct selected vending-price checks | Accepted Core defect repair | Implemented |
| [PN-011](#pn-011) / RGB-032 | 2026-10-15 | Make Flute feedback reflect actual wake-ups | Minimal and Core | Implemented |
| [PN-012](#pn-012) / RGB-010b | 2026-10-15 | Correct the Raichu trade evolution claim | Minimal and Core | Implemented |
| [PN-013](#pn-013) | 2026-10-15 | Mark the current floor and prevent same-floor travel | Minimal and Core | Implemented |
| [PN-014](#pn-014) | 2026-10-15 | Left/right quantity steps of ten | Minimal and Core | Implemented |
| [PN-015](#pn-015) / RGB-030 | 2026-10-15 | Preserve rooftop payment when TM delivery fails | Core defect repair under the existing bug policy | Implemented |
| [PN-016](#pn-016) | 2026-10-15 | TM/HM names and move INFO before and after ownership | Minimal and Core | Implemented |
| [PN-017](#pn-017) | 2026-10-15 | Bag, item-PC and Pokémon-box capacity counts | Minimal and Core | Implemented |
| [PN-018](#pn-018) | 2026-10-15 | Known and offered move INFO, optional live types | Minimal and Core | Move INFO implemented. Live types planned. |
| [PN-019](#pn-019) | 2026-10-20 | Preserve item-list selection and scroll after actions | Minimal and Core | Implemented |
| [PN-020](#pn-020) | 2026-10-20 | Optional item capacity with a 64-slot bag target | Accepted Extension and separate reserve; save/runtime design pending | Not implemented |
| [PN-021](#pn-021) | 2026-10-24 | Retain the battle move cursor through SELECT reordering | Accepted Core interface requirement | Implemented |
| [PN-022](#pn-022) | 2026-10-24 | Append new boxed Pokémon consistently with deposits | Accepted Core usability policy | Implemented |
| [PN-023](#pn-023) | 2026-10-24; revised 2026-10-25 | Restore normal Mansion Burglar sight engagement | Accepted scoped Core correction; original intent unproven | Implemented |
| [PN-024](#pn-024) | 2026-10-25 | Viridian Forest star grass produces no encounters | Source-confirmed; accepted scoped Core correction | Implemented |
| [PN-025](#pn-025) | 2026-11-22 | Acid Armor leaves the active picture invisible | Minimal and Core | Implemented |

<a id="pn-001"></a>

## PN-001 — Protect EXP. ALL from tossing and selling

Oak’s aide gives EXP. ALL once. In retail Red/Blue its key-item flag is clear, so the Bag and item PC allow TOSS. A shop can buy it for zero. The aide records the reward and cannot replace the item. [TOSS and reward](../research/evidence.md#e68) · [Shop sale](../research/evidence.md#e74)

Both presets mark EXP. ALL as a key item. Tossing it gives the normal important-item refusal. A shop says “I can't put a price on that.” The player can still deposit or withdraw it. Minimal shares experience whenever the player carries it. Core also requires the field switch to be on, its initial setting. RGB-017 defines how Core divides experience. [Experience awards](../research/foundation-audit.md#exp-all-gives-too-little-to-a-party-with-multiple-participants) · [Switch and award checks](../../tests/core_services.py)

Check the aide’s full-Bag retry and single reward, repeated refusals in the Bag, PC and Mart, and PC transfers across save/reload. Verify the item, money and quantities after each attempt. Ordinary sales and discards still work. [Item safety checks](../../tests/item_safety.py)

<a id="pn-002"></a>

## PN-002 — Register an item to SELECT

In both presets, choose REGISTER on the Bicycle, Old Rod, Good Rod or Super Rod in the Bag. Press SELECT in the field to use it. Registering a different item replaces the previous choice. CLEAR removes the shortcut. The save holds the item ID so reordering the Bag keeps the choice. The shortcut checks possession on each use. A deposited item is unavailable until withdrawn.

The Bicycle keeps the usual map, surfing and forced-riding checks. A rod uses its own fishing routine, including its shore, bite, species and level rules. Retail SELECT already reorders items in the Bag. The field shortcut only handles a fresh press when the player controls the character. A talk or scripted action keeps its usual input. [Original inputs](../research/evidence.md#e69) · [Field input](../../engine/overworld/registered_item.asm)

Check replacement, clearing, save/reload, invalid saved IDs and repeated or simultaneous button presses. Verify the Bicycle in and out of Cycling Road, all three rods at the shore and a refusal inland. Passive quest items have no registration action. [Bicycle checks](../../tests/bicycle_shortcut.py) · [Bag and fishing checks](../../tests/field_menu_features.py)

<a id="pn-003"></a>

## PN-003 — Browse the box with a full party

WITHDRAW opens the current box in both presets even with six party members. The original capacity check ran before the list opened. The game now checks after the player picks a Pokémon and chooses WITHDRAW. A full party gets the existing error and keeps every party and box record. Empty boxes retain their original message. [Original guard](../research/evidence.md#e70)

In both WITHDRAW and DEPOSIT, leaving STATS or cancelling a Pokémon’s action menu returns to the list. The last Pokémon viewed stays selected, with the same scroll position where possible. Confirmed transfers still follow the ordinary capacity rules. Direct MOVE and automatic storage are separate extension designs. [Menu evidence](../research/evidence.md#e83) · [Storage choices](14-features-and-extensions.md#storage-extensions)

Check full, nearly full and one-member parties, empty and full boxes, first/middle/last entries, repeated cancellation, scrolling, both exit buttons and save/reload. A successful withdrawal moves the selected record once. Browsing and a refused withdrawal move nothing. [Cartridge checks](../../tests/pc_browsing.py)

<a id="pn-004"></a>

## PN-004 — Contextual HM use

In both presets, press A at a valid target and confirm Cut, Surf or Strength. A party member must know the move and have its usual field permission. Owning the HM alone grants no shortcut. Manual use from the party menu still works. The field interaction checks the facing target, party, badge and map restrictions and gives existing NPCs, signs and events their normal priority. [Field-action contract](../research/field-shortcut-contract.md) · [Source evidence](../research/evidence.md#e73)

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

[Surf and Strength checks](../../tests/field_shortcuts.py) · [Route 14 Cut check](../../tests/route_cut_tree.py)

<a id="pn-005"></a>

## PN-005 — Correct Oak's Pokédex rating typo

**Requirement:** correct geting to getting in Oak's 60–69-owned-species rating. Both presets correct unambiguous typos under D06 and the [text policy](03-bug-fix-policy.md#typo-corrections).

**Evidence:** the pinned English Red/Blue text contains the reported misspelling. The PC calls the shared rating routine, which counts owned species and selects this rating for 60–69. Oak's Lab and the Hall of Fame also call the routine. [E82](../research/evidence.md#e82)

**Scope and display check:** add the missing letter and reflow the text as needed, retaining the rest of the sentence. The original first line has 18 characters; adding the letter directly produces 19. Check text width, scrolling, and completion in all three display paths. Keep thresholds, neighboring ratings, counts, and other game behavior unchanged. This is a narrow text edit; no new game test harness is needed.

**Delivery:** The game uses “getting” in Oak’s rating. The cause of the original spelling is unknown.

<a id="pn-006"></a>

## PN-006 — Navigate STATS by Pokémon and page

**Requirement:** up/down selects the previous/next Pokémon in the available party or current-box list, retaining the selected page. Left/right selects pages for the same Pokémon. B leaves any STATS page for its browsing context. Restore the Pokémon last viewed and keep list scroll position where possible. The default keeps the two existing pages and their information.

**Developer support:** adding a page must reuse the navigation controls. DV and stat EXP pages remain possible extensions.

**Evidence:** the original pages wait for A/B, and party, PC, battle, and trade callers invoke both in sequence. The PC caller has the separate return-path issue covered by PN-003. [E83–E84](../research/evidence.md#e83)

**Acceptance:** test one-member and full parties; one-entry and full/scrolled boxes; first/last entries; both pages; B from each page; page retention when changing Pokémon; and returning to the correct highlighted entry. Test empty contexts without reading nonexistent entries. A temporary third page must use the same controls. Protect battle replacement rules and trade context. Browsing must not transfer, release, switch, or alter Pokémon data.

**Delivery:** The directional controls work across the original STATS pages. [Cartridge checks](../../tests/cartridge_smoke.py) · [Menu inventory](../research/menu-navigation.md)

<a id="pn-007"></a>

## PN-007 — Safer Pokémon release confirmation

**Requirement:** clearly show the selected Pokémon's nickname and species before release, default confirmation to No, and remove it only after an explicit Yes. B or No leaves the Pokémon unchanged and returns to the release list. Preserve intentional release.

**Evidence:** the PC calls the standard Yes/No initializer, which selects the first option by default. The release branch removes a Pokémon only after checking the result; refusal already returns to the release list. Apply the new default to this caller, preserving other Yes/No prompts. [E85](../research/evidence.md#e85)

**Acceptance:** check nicknames that hide the species, duplicate nicknames, first/last entries, scrolled lists, repeated A input at prompt entry, B/No, and explicit Yes. Refusal changes no records or counts; confirmation releases exactly the identified Pokémon once. Check text width and ordinary shop/healing prompt defaults. A release must not use a stale index left by STATS navigation.

**Delivery:** The release prompt shows the Pokémon’s nickname and species and starts on No. [Cartridge checks](../../tests/menu_returns.py)

<a id="pn-008"></a>

## PN-008 — Keep the item list after a shop refusal

**Requirement:** after refusing an unsellable item, return to the SELL list. After a purchase fails for insufficient money or bag space, return to the BUY list. Retain the selected item and scroll position. Keep the refusal message and require a new explicit choice before attempting any transaction.

**Evidence:** the checked original paths send these cases to BUY/SELL/QUIT. Quantity cancellation, final price refusal, and completed transactions already loop back to the respective item lists. [E86](../research/evidence.md#e86)

**Scope:** preserve prices, quantity limits, bag capacity and stacking, key-item/HM protection, confirmation, and normal exit behavior. A refusal or failed purchase changes no money, inventory, or completed-transaction state. EXP. ALL sale protection continues to use its existing important-item message. Empty SELL lists keep their existing response and return to the main shop menu.

**Acceptance:** check key items, HMs, and protected EXP. ALL; insufficient money; full bag/new stack; quantity limits; and valid additions to an existing stack. Check selected first/middle/last items and scrolled lists. After refusal, selecting another item must work without an automatic retry. B from the item list still returns to BUY/SELL/QUIT. Preserve quantity cancellation, declining the price, ordinary successful buys/sales, and empty-bag handling.

**Delivery:** The shop returns to the relevant item list after a refusal or failed purchase. [Quantity-menu checks](../../tests/shop_carry_count.py)

<a id="pn-009"></a>

## PN-009 — Return party action-menu CANCEL to the Pokémon list

**Requirement:** in Start → POKéMON → choose a Pokémon, selecting CANCEL returns to the party list with the same Pokémon highlighted, matching B.

**Evidence:** the original overworld action menu sends B to the party-list loop and CANCEL to the exit path that restores Start. The source does not explain the difference. [E86](../research/evidence.md#e86)

**Scope:** both presets use the party-list return. Preserve B from the party list to Start, STATS, SWITCH, field moves, and other callers' cancellation rules. This is not a global rule to change every CANCEL destination.

**Acceptance:** check one, two, and six party members, first/middle/last selections, and action menus with and without field moves. Both cancellation methods must retain the selected Pokémon and leave party records unchanged. Check repeated cancellation, choosing a different Pokémon afterwards, normal actions, and the normal party-list exit. Preserve battle, forced-replacement, item-targeting, trade, and PC flows.

**Delivery:** CANCEL returns to the same row in the party list. [Cartridge checks](../../tests/menu_returns.py)

<a id="pn-010"></a>

## PN-010 — Vending affordability

**Requirement:** compare funds with the selected price: Fresh Water ¥200, Soda Pop ¥300, Lemonade ¥350. A successful delivery deducts that price once. Insufficient money or space gives no drink and takes no money. Keep the original effects, stack rules, and cancellation.

**Evidence/status:** source-confirmed wrong ¥200 guard; explicitly accepted Core repair. The original underpayment path clamps money to zero, rather than wrapping it. [E89](../research/evidence.md#e89) Core checks the selected drink price. [Cartridge checks](../../tests/celadon_roof_transactions.py)

**Regression:** each price minus one, exact price, and price plus one; ¥0/199/200/299/300/349/350; full bag with and without room in an existing stack; cancel; repeated purchases; displayed balance and actual item/money changes. Protect inventory boundaries separately.

<a id="pn-011"></a>

## PN-011 — Truthful Flute feedback

**Requirement:** feedback must reflect actual sleep cleared, including when only the wild opponent is asleep. Keep the existing wake targets and turn cost. This does not approve a contextual Snorlax prompt or different sleep rules.

**Evidence/status:** the source clears the wild opponent's sleep after party scans but does not set the response flag from that change. It can omit wake-up confirmation and show the alternate catchy-tune response. It does not literally say “no effect.” [E94](../research/evidence.md#e94) Both presets select the message from actual wake-ups.

**Regression:** opponent alone asleep, party alone asleep, both, neither, trainer battle, unused party slots, and other status bits. Compare statuses, text, sound, action cost, and RNG use.

<a id="pn-012"></a>

## PN-012 — Raichu trade follow-up

**Requirement:** the follow-up must not claim Raichu evolved. Preserve species, nicknames, rewards, and evolution rules. The shared dialogue must remain truthful for its other user, the Poliwhirl→Jynx trade.

**Evidence/status:** both trade entries use the evolution dialogue set. Its statement about the Pokémon given to the NPC conflicts with retained Raichu data. [E91](../research/evidence.md#e91) The game uses a follow-up line that fits Raichu’s evolution data.

**Regression:** both users, other dialogue sets, first and later visits, name substitution, and rendered line layout. No added Raichu evolution or changed trade species.

<a id="pn-013"></a>

## PN-013 — Current elevator floor

**Requirement:** indicate the actual current floor in the floor menu. Selecting it must not trigger travel animation, travel sound, or destination changes. Preserve all other floors and cancellation.

**Evidence/status:** Red/Blue's shared menu treats a noncancel destination as travel without a same-floor exclusion. FireRed displays the current floor and skips animation for a same-floor Department Store selection, while still allowing that entry to be chosen. [E103](../research/evidence.md#e103) The game marks the current floor and skips travel when selected.

**Design/checks:** derive the entered floor from the actual entrance/destination state, not the elevator map ID or a stale cursor. Check every floor in the Department Store, Silph Co., and Rocket Hideout; first entry, consecutive trips, cancellation, and save/reload. Same-floor input must leave warp state unchanged; a real trip must still arrive correctly with its normal presentation. Preserve valid list navigation when the current floor is first/last or off the initial visible page.

<a id="pn-014"></a>

## PN-014 — Quantity changes of ten

**Requirement:** left decreases ten and right increases ten in the shared quantity selector. Preserve up/down unit steps and their wrap behavior, A confirmation, B cancellation, item limits, affordability checks, and transaction validation.

**Bounds:** left clamps at one, right at the current maximum, as in the checked Gold/Silver and FireRed handlers. Recompute displayed totals after any change. An unchanged endpoint must not accidentally confirm the action. For a Bag or item-PC discard, the final TOSS question shows the item name and selected quantity. [TOSS checks](../../tests/field_menu_features.py)

**Evidence/status:** Red/Blue handles unit steps but ignores left/right here. Both comparison games provide tens. This does not establish a universal rule across every later game. [E103](../research/evidence.md#e103) The game accepts left and right for steps of ten.

**Regression:** maxima 1, 2, 9, 10, 11, and 99; quantities around 1/10/11 and the maximum; repeated/held input; up/down wrap after a tens change; price totals; cancellation; and one transaction per confirmation. Cover shop buy/sell, bag toss, and item-PC deposit/withdraw/toss callers. Keep key-item paths that skip quantity selection.

<a id="pn-015"></a>

## PN-015 — Rooftop drink/TM exchange

**Requirement:** a drink exchange either takes one drink and gives its one-time TM, or preserves the drink, TM inventory, and reward flag. Keep Fresh Water→TM13 Ice Beam, Soda Pop→TM48 Rock Slide, and Lemonade→TM49 Tri Attack. Permit a valid exchange where the final drink frees the needed slot.

**Evidence:** all three scripts remove payment before `GiveItem`. With twenty occupied slots, at least two drinks in the selected stack, and no target TM stack with space, delivery fails after payment. With a final drink in that stack, removal frees a slot. A spare slot is therefore not always necessary. The reward flag is set only after successful delivery. The checked ordinary path does not prove duplication; retrying an undelivered reward is not an extra TM. [E101](../research/evidence.md#e101)

**Classification/status:** source-confirmed exchange defect, included under D06/D30. The reported duplication remains unverified and requires its own sequence. Core checks the whole exchange before spending the drink. [Cartridge checks](../../tests/celadon_roof_transactions.py) A nearby-guard screen does not establish payment order; [the comparison](../research/remake-usability-comparison.md#rooftop-transaction-boundary) records that correction.

A last drink in the stack frees its slot for the TM. A full Bag can also accept the reward in an existing TM stack with room. Validate the final inventory, including the 99-unit stack limit.

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

Both presets include static INFO for a move currently offered, known or selected. Live types for the two active battlers remain a planned, independent extension. [Input and release tests](15-battle-information.md) · [Emerald Expansion precedent](../research/evidence.md#e104)

<a id="pn-019"></a>

## PN-019 — Keep item-list position after actions

**Requirement:** preserve selection and scroll when returning to the same item list after item-PC deposit, withdrawal, or toss; bag item use or toss; and shop buy/sell actions. This includes temporary quantity/confirmation prompts, cancellation, refusal, and completed actions that already return to that list. Keep the previously accepted menu destinations, including medicine returning to the bag. This does not authorize keeping a target selector open or changing successful Pokémon-transfer destinations.

**Position after changes:** if the selected entry remains, keep that exact entry and viewport. If it is removed, select the entry that takes its place; if it was last, select the preceding item. Preserve the old viewport when that choice remains visible and valid; otherwise move it only enough to show the selected entry without invalid rows. An empty list must have a valid empty/cancel state and follow its caller's exit policy. Do not jump to the top merely because a count changed.

**Evidence:** the pinned Red/Blue item-PC loops already return to the correct lists. The shared inventory-removal routine resets both current and saved row/scroll values when the last unit of a stack is removed. It skips that reset when units remain. Withdrawals, sales, and tossing also use the routine. Shop buy/sell loops separately reset the visible cursor row, even when returning from quantity cancellation or a declined price. [E106](../research/evidence.md#e106)

**Classification/status:** both presets keep the same list position. This removes repeated navigation while retaining inventory management, quantities, prices, capacity, item consumption, and confirmations. The Bag, shop, and item PC preserve the item position as the list changes. [Item PC checks](../../tests/menu_returns.py)

**Implementation boundary:** keep the selected row and scroll offset within the list that owns them. Two stacks of the same item are separate entries. After a removal, restore the nearest valid row. Scripted rewards, battles and other list owners keep their own state. Cursor memory here lasts for the current interaction.

**Acceptance:**

- Deposit several items near the bottom of a full bag in sequence. Check partial stacks, complete stacks, key items, and duplicate stacks. The next item must be accessible without scrolling down again.
- Cover PC withdrawal/toss, bag use/toss, and shop buy/sell returns. Check both quantity cancellation and declined confirmations, protected-item refusals, insufficient funds/capacity, and successful actions. Existing PN-008 refusal destinations remain required.
- Check first/middle/last entries, every visible row, empty/one-entry lists, 20-slot bag and 50-slot item PC boundaries, and repeated deletion through the end. No off-list cursor, stale index, or automatic follow-up action is permitted.
- Verify each chosen item, exact quantity, inventory order, money, and refusal state. A held confirmation button must not act on the new adjacent item. Keep unrelated list contexts separate and recheck non-list callers of shared removal.
- Preserve medicine's return to the bag, ordinary B exits, successful Pokémon-transfer destinations, and existing save data.

<a id="pn-020"></a>

## PN-020 — Optional item-capacity expansion

**Planned extension:** a 64-slot Bag. Core and Minimal currently have 20 Bag slots and 50 item-PC slots. The Bag extension must keep the item PC independent. A 60-slot PC, pockets, sorting and reusable items are separate choices. The Bag study did not establish a layout for a larger PC.

**Scope:** count occupied item stacks, not individual units. Retain the per-stack quantity limit, item identity, key-item protection, prices, effects, and acquisition rules. This is a capacity choice, not part of the default scroll-position repair. Keep the accepted PN-019 navigation behavior at each supported capacity.

**Upstream allocation check.** Money follows the original 42-byte Bag. On the pinned upstream source, a separate 134-byte block at `$D66A–$D6EF` fits four marker bytes, a count byte, 64 two-byte entries and a terminator. The RAM-only check linked 60 and 64 slots without moving existing labels. Its size check rejected 65. The earlier tutorial studied a different 128-byte block. [E108](../research/evidence.md#e108)

**Current constraint.** Both released presets use `$D6B8–$D6B9` inside that block for the SELECT registration tag and item ID. A future 64-slot build that uses all 134 bytes must relocate these fields and carry the choice over when importing a supported save. Keep the original 42-byte Bag footprint, other field addresses, block sizes and `wGameProgressFlagsEnd` fixed. Reject overlapping allocations. Check indexing, copying, terminators, bulk writes and list callers against the new layout before offering this option. [Current memory layout](../../ram/wram.asm) · [Allocation study](../research/bag-memory.md)

**Initialization:** initialize the enabled bag and its format marker after the game-progress clear, which otherwise overwrites their initial values in this reserve. Keep the original progress boundary fixed. [E109](../research/evidence.md#e109)

**Saves:** relocation changes the bag's saved location even if other offsets stay fixed. Publish a capacity/layout identifier and the actual compatibility policy before release. Use an explicit tested conversion for supported imports, or clearly require a fresh save for the enabled layout. Never reinterpret an old or differently configured save silently. Do not use the tutorial's deposit-items workaround as a migration design. The disabled profile must keep its promised save behavior.

**Acceptance:** test Core and the bag-64/PC-50 profile; test other PC settings independently and in combinations only if advertised. Verify entries 20/21 and 63/64, refusal of entry 65 as a new stack, addition to an existing stack while full, stack splitting and duplicates, insertion/removal, toss/use, shops, ground/scripted rewards, rooftop exchanges, registration, and PN-019 list retention. A supported capacity counter must show the configured denominator. Check guards around allocations, unchanged other-field addresses, single reserve ownership, overlap rejection, neighboring saved fields, new-game initialization after the progress clear, save/reload, supported imports, disabled-state behavior, advertised feature combinations, and original Game Boy builds. No game implementation, configured build, runtime regression, or safe conversion is claimed yet.

<a id="pn-021"></a>

## PN-021 — Retain the battle move cursor during SELECT reordering

The original cursor also writes move history that enemy Counter reads. Minimal keeps the stock interaction. Core keeps the visible cursor at the marked row while preserving the history Counter reads. Regression cases include marking a move, cancelling and switching before completing a swap. [Measured turns](../research/minimal-action-review.md)

**Requirement:** retain the cursor row when SELECT marks a move and when a second SELECT completes the swap. Marking move three leaves the cursor on three. Moving to four and pressing SELECT swaps three/four and leaves the cursor on four. Keep the source marker visible and separate from the active cursor. A repeat SELECT on the source is a no-op swap with the existing completion behavior.

**Evidence:** both SELECT paths jump back to the menu initializer, which restores a previous `wPlayerMoveListIndex`. The result is often move one, but the source does not hard-code a first-row reset. [E110](../research/evidence.md#e110)

**Classification/status:** accepted Core interface requirement. This is the same position-retention principle as PN-019, applied to a list without scrolling. [Cartridge checks](../../tests/move_swap_smoke.py)

**Implementation boundary:** preserve the current cursor across the redraw without treating SELECT as an attack choice. Retain the existing battle/party move and complete PP-byte swaps, Disable slot/duration handling, and A/B behavior. Keep existing rules for Transform, Mimic, empty move slots, unavailable moves, and link battles. Cursor storage must not change battle-history semantics or another caller's menu state.

**Acceptance:** check first/middle/last rows, two through four moves, a one-move no-op, same-slot selection, repeated swaps, and cancellation. Test three↔four with an earlier remembered selection at both one and two. Verify battle and party move/PP arrays, PP Up bits, and disabled-slot duration/index. The operation must consume no turn or PP and add no random draw. Test transformed/copied moves and preserve link input restrictions. A and B must keep their existing actions; opening a genuinely new menu may still initialize its own context.

<a id="pn-022"></a>

## PN-022 — Use consistent append order for boxed arrivals

**Requirement:** append newly caught Pokémon sent to the current box after its existing members, matching party deposits. Apply the same insertion rule to gifts that already use the new-boxed-Pokémon routine. Keep all existing members in their current positions. Never reorder an existing saved box merely on load.

**Evidence:** `SendNewMonToBox` prepends captures and boxed gifts, shifting the species list, original-trainer names, nicknames, and records. It names slot one directly. `_MoveMon` appends party deposits. The ordering difference is source-confirmed; its original design reason is not established. [E111](../research/evidence.md#e111)

**Classification/status:** accepted Core usability policy. Consistent append behavior preserves existing positions and all storage limits. Record it as a project choice, without claiming proof of an original programming error. Core appends new boxed arrivals.

**Implementation boundary:** give every part of the new boxed Pokémon the same destination index, including the nickname prompt and full record. Preserve species, OT, ID, nickname, level, experience, DVs, stat experience, moves, PP, and status according to the existing acquisition rules. Use the selected preset’s destination check. Preserve gift eligibility and completion, the six-member party, twenty members per box, confirmed box-change saves, transfer rules, and removal compaction. This adds no automatic box switching, sort, or MOVE POKÉMON feature and requires no new saved field.

**Acceptance:** with distinct existing members A/B/C, capture D into a full-party box and require A/B/C/D; deposit E and require A/B/C/D/E. Cover empty/one/19-entry boxes, the 19→20 boundary, the active-box refusal in both reference presets and the all-boxes-full refusal with automatic placement enabled, repeated captures, boxed gifts, nickname Yes/No, duplicate species/nicknames, and exact OT/record identity. Check withdrawal/release, save/reload, and box changes without reordering old members. Party arrivals keep their existing behavior. Test automatic capture storage and MOVE POKÉMON only in supported combinations; their absence must not block this Core feature.

<a id="pn-023"></a>

## PN-023 — Correct Mansion Burglar sight engagement

**Requirement:** the three Mansion Burglars on 2F, 3F, and B1F initiate battle through the normal sight check when undefeated, visible, facing the player, aligned, and within range. Talking must still work. Preserve the Scientists' existing settings and every other zero-range trainer.

**Evidence:** the original three Burglar ranges are zero; the Scientists' ranges are three, two, and three. All four floors use the normal sight routine. [E112](../research/evidence.md#e112) Yellow retains the zero values, while FireRed/LeafGreen gives all three Burglars range one. [E113](../research/evidence.md#e113) The Route 21 Fishers face adjacent water, which limits that analogy. [E114](../research/evidence.md#e114)

**Classification/status:** accepted scoped Core correction under D39. Treat the passive behavior as a likely oversight for this project. The original developer intent and the reason for the remake change remain unproven. This supersedes the earlier preserve-in-Core disposition for these three Burglars; it does not change the general uncertain-change policy. The Core map data sets the three sight ranges. [Cartridge checks](../../tests/mansion_sight.py)

**Implementation:** Core uses a one-square sight range for each Burglar, as in the remake. Keep trainer classes, parties, levels, rewards, dialogue, movement patterns, map layout, switches, doors, and defeat flags unchanged. Do not enable sight battles for all zero-range trainers or replace the trainer engine.

**Acceptance:** exercise all three Burglars one square away, including facing/alignment, hidden or off-screen states, talking, and post-defeat behavior. Check the two wandering Burglars while moving and at movement boundaries. Battle must start once, restore valid map state, and award the existing reward once. Confirm that engagement and post-battle position do not block an exit, corner the player, or bypass a gate. Test narrow paths and the 3F table area. Preserve ordinary Scientist sight, map progress, save/reload, and unrelated zero-range trainers such as the Route 6 pair and Route 21 Fishers.

<a id="pn-024"></a>

## PN-024 — Recognize Viridian Forest star grass for encounters

**Report:** some grass squares in Viridian Forest never produce wild encounters. The supplied [GameFAQs report](https://gamefaqs.gamespot.com/gameboy/367023-pokemon-red-version/faqs/64175/viridian-forest-encounter-rate-glitch) describes the star pattern and says Yellow is unaffected. The source comparison below checks that report.

**Evidence:** Red/Blue checks the lower-right graphic tile for grass encounters. The Forest's star-pattern squares have ordinary grass at lower-left and decorative `0x34` at lower-right. The sprite code treats them as grass; the encounter gate rejects them. Yellow reads lower-left, with identical Forest map and blockset bytes and the same grass ID. The decoded map has 114 affected squares. [E115](../research/evidence.md#e115)

**Disposition:** source-confirmed mismatch; accepted scoped Core correction under D40. Treat the encounter effect as a likely oversight. Original intent is strongly inferred from the internal mismatch and Yellow comparison, without an original developer statement. Core treats the star grass as an eligible encounter tile in the forest. [Cartridge checks](../../tests/forest_encounters.py)

**Required behavior:** affected grass can produce encounters under the existing rate, tables, species, levels, slot weights, and Repel rules. Preserve graphics, map layout, and ordinary non-grass paths. Core limits the rule to the affected Forest grass. Cinnabar shore has a separate decision.

**Acceptance:** check all affected and ordinary grass squares, controlled encounter thresholds, slot selection, Repel, direction changes, warps, scripted movement, and post-battle return. Check water, shores, Safari Zone maps sharing the tileset, and all three project variants. Preserve unrelated random-number behavior and save format. See the [review](../research/forest-encounters.md).

<a id="pn-025"></a>

## PN-025 — Acid Armor picture visibility

Acid Armor can leave an active battler or its Substitute invisible across later turns. When battle animations run, its dedicated sinking animation clears the picture from video memory. The user still gets the normal Defense increase and can take damage. Checks in the English Red, Blue, and Yellow ROMs confirm the behavior. [E116](../research/evidence.md#e116)

The original Japanese releases have the same animation. Viewing STATS in the battle party menu reloads the enemy picture while its Defense boost stays active. Haze can remove the Defense boost while the picture stays blank. Gold and Silver and the remakes restore the picture at animation end. A missing restoration is the best fit for this evidence. The intended duration in Gen I remains unknown. [E117](../research/evidence.md#e117), [E119](../research/evidence.md#e119)

In both presets, the original melt ends by restoring the sprite that was visible when it began. The move’s effect and animation setting still work as before. [Cartridge checks](../../tests/acid_armor.py) · [Acceptance criteria](07-testing-ci.md#acid-armor-picture-checks)
