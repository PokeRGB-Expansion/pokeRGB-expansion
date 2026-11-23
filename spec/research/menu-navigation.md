# Menu returns and STATS navigation

Initial audit checked **2026-10-14** against the pinned English Red/Blue reference, with party/shop paths rechecked on **2026-10-15**. The remote branch head matched the recorded commit at the initial check. Item-list cursor and mutation paths were checked separately on **2026-10-20** at the same retained pin. Battle move SELECT paths were checked on **2026-10-24** at the same pin. These are source findings and accepted requirements, not an implemented or played menu patch.

## Return-path inventory

| ID | Context | Original return path | Disposition |
|---|---|---|---|
| MN01 | Bill's PC WITHDRAW: view STATS, then leave | STATS returns to that Pokémon's action menu. B or CANCEL there returns to the PC main menu, bypassing the box list. | **Core change accepted:** leaving STATS or cancelling the selected-Pokémon action returns to the box list, with selection and scroll context retained. [E83](evidence.md#e83) |
| MN02 | Bill's PC DEPOSIT: view STATS, then leave | The same action-menu helper returns to the PC main menu on cancellation. | **Core change accepted:** return to the party list where deposit browsing is already available. Keep existing deposit eligibility and transfer rules. [E83](evidence.md#e83) |
| MN03 | Party STATS outside battle | Both pages run in sequence, then the caller returns to the party list. | **Core navigation accepted:** explicit page and Pokémon controls, with B returning to the list. Do not describe the existing return destination as a deeper-exit bug. [E84](evidence.md#e84) |
| MN04 | Party Pokémon action menu: CANCEL versus B | CANCEL leaves the party menu for the Start menu; B returns to the party list. | **Core change accepted, 2026-10-15:** make CANCEL match B, returning to the party list with the same Pokémon selected. [PN-009](../docs/13-playthrough-intake.md#pn-009) [E86](evidence.md#e86) |
| MN05 | Successful medicine use outside battle | The item caller returns to the bag after the party-target screen. | **Preserve:** do not keep the target selector open for repeated use. [E86](evidence.md#e86) |
| MN06 | Shop quantity cancellation or final price refusal | Returns to the corresponding item list, but the loop zeros the visible cursor row. | **Preserve the destination; restore position under PN-019.** Returning to the right list alone does not preserve selection. [E86](evidence.md#e86), [E106](evidence.md#e106) |
| MN07 | Shop refuses an unsellable item | Returns to BUY/SELL/QUIT. | **Core change accepted, 2026-10-15:** return to the SELL list with selection/scroll context. Keep item protection and the refusal message. [PN-008](../docs/13-playthrough-intake.md#pn-008) [E86](evidence.md#e86) |
| MN08 | Shop purchase fails for insufficient money or bag space | Returns to BUY/SELL/QUIT. | **Core change accepted, 2026-10-15:** return to the BUY list with selection/scroll context. Keep all price and capacity checks. [PN-008](../docs/13-playthrough-intake.md#pn-008) [E86](evidence.md#e86) |
| MN09 | Player PC item deposit/withdraw | Returns to the corresponding list. Removing a full stack zeros row and scroll through the shared helper. | **Core change accepted:** retain position under [PN-019](../docs/13-playthrough-intake.md#pn-019). The destination is already correct; the position reset needs repair. [E106](evidence.md#e106) |
| MN10 | Successful Pokémon deposit, withdrawal, or release | Returns to Bill's PC main menu. | **Preserve pending a separate decision:** approval of browsing returns does not authorize a repeat-transfer flow. [E83](evidence.md#e83), [E85](evidence.md#e85) |
| MN11 | Decline a Pokémon release | Returns to the release list. | **Preserve the return path; improve confirmation:** default to No and identify the Pokémon clearly. [E85](evidence.md#e85) |
| MN12 | Battle or trade STATS caller | Both status pages are called before the caller restores its battle or trade interface. | **Caller protection required:** use the new page controls without bypassing forced battle choices, changing trade state, or exposing another data context. [E84](evidence.md#e84) |
| MN13 | Bag/PC item toss | The toss helper uses shared removal, which clears current/saved position when an entry is deleted. | **Core position requirement PN-019:** select the adjacent entry safely; retain all protected-item and confirmation rules. [E106](evidence.md#e106) |
| MN14 | Shop sale completes | SELL loop zeros the visible row; removing the full stack also clears scroll state. | **Core position requirement PN-019:** keep the remaining entry or its neighbor and viewport. Preserve sale rules and money. [E106](evidence.md#e106) |
| MN15 | Shop purchase completes | BUY returns to its list but zeros the visible row. The chosen shop entry normally remains. | **Core position requirement PN-019:** keep the chosen shop entry and viewport; preserve stock/prices and explicit purchase confirmation. [E106](evidence.md#e106) |
| MN16 | Battle move SELECT: mark a source or complete a swap | Both redraws restore an older saved move index, often move one. | **Core position requirement PN-021:** retain the current row and source marker without changing swap data or battle input rules. [E110](evidence.md#e110) |

This is a first pass over these specific flows. It is not a full audit of every game menu. Source branches establish the destinations; cursor restoration, drawing, input timing, and integration still require game checks.

## Party action menu example

Open Start → POKéMON, then choose one Pokémon. The small action menu includes STATS, SWITCH, CANCEL, and any available field moves. In the original game:

- Pressing B returns to the party list.
- Selecting CANCEL returns to the Start menu, leaving the party list.

PN-009 corrects this MN04 difference in Core: CANCEL must match B and retain the selected Pokémon. B from the party list still returns to Start. The source does not establish the original design rationale for the different destinations. [E86](evidence.md#e86)

## Required STATS controls

The default retains its two existing pages and their information:

- **Up/down:** previous or next Pokémon in the available party or current-box list. Keep the selected page.
- **Left/right:** previous or next page for the same Pokémon.
- **B:** leave STATS from either page and restore its browsing context.

After moving between Pokémon, return to the Pokémon last viewed. If the Pokémon did not change, preserve its list position and scroll offset exactly. Otherwise, keep the old scroll position where possible while making the selected Pokémon visible. Navigation must not select WITHDRAW, DEPOSIT, RELEASE, or SWITCH as an action.

The caller supplies the data context, valid list bounds, selected Pokémon, and return destination. Battle and trade callers need explicit handling; do not assume every caller can browse a full box or freely cancel a required selection. Returning from STATS during a forced replacement must still require a legal replacement.

Keep page selection separate from the existing rendering code. Developers must be able to add a page without replacing the navigation controls. DV and stat EXP pages are future extension examples; the default adds neither. A small page table or equivalent is a sufficient implementation proposal. No general plug-in system is required. A can retain its old forward/finish behavior as an additional shortcut.

## Scoped changes and protection cases

PN-003 covers the PC return fix as well as browsing with a full party. PN-006 covers STATS navigation, PN-007 covers safer release confirmation, PN-008 covers the accepted shop returns, and PN-009 covers overworld party action-menu cancellation. [The intake](../docs/13-playthrough-intake.md) and [test plan](../docs/07-testing-ci.md#stats-and-menu-regression-coverage) record their acceptance cases.

Changing the shared Yes/No routine globally would exceed the release safeguard. Apply the No default to release confirmation, show the selected nickname and species, and preserve explicit release. No or B must leave data unchanged; Yes must release only that Pokémon once. Ordinary shop and healing prompts keep their own defaults.

Medicine's return-to-bag flow is explicitly retained. Repel renewal is a separate optional extension, disabled by default and a stretch goal. It keeps the original item cost, duration, and encounter rules. Its source baseline is [E87](evidence.md#e87).

For each additional return-path change, name the action, current destination, proposed destination, and affected cursor state. Review cancellation, inspection, failed actions, and completed actions separately. A global rule that every menu stays open would discard these distinctions.

## Item-list position and mutation

Returning to the correct list, retaining the selected entry, and retaining the visible scroll window are separate checks. E106 confirms the item-PC deletion reset and the shop loop's row reset. PN-019 applies the accepted position rule to same-list returns; it does not change which menus stay open.

After partial removal, retain the same stack. After deleting an entry, select its successor at the same logical index, or its predecessor if it was last. Retain the viewport where valid and adjust only enough for the shortened list and selected entry. Handle an empty list using its valid empty/cancel state. Duplicate item IDs do not identify a unique stack; track the entry within its actual list.

Keep the cursor context with the list owner across quantity prompts, confirmations, inspection, refusals, and mutations. Avoid an unconditional change to the shared removal helper without checking scripted and battle callers. Opening another list or leaving the menu can initialize its own context; persistent cursor state across separate PC visits is outside this requirement. [PN-019](../docs/13-playthrough-intake.md#pn-019) supplies the acceptance cases.

Position retention also applies when a list has no scrolling. [PN-021](../docs/13-playthrough-intake.md#pn-021) scopes this to battle move reordering: marking and completing SELECT must keep the current row, with the existing A/B and battle rules intact. A general ban on every menu reset is not implied.
