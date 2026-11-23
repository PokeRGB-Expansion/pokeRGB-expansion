# Small repairs and usability improvements

The [player-experience sweep](player-experience-sweep.md) and [cross-system review](final-scope-audit.md) give current placements, including shared information displays. The [Game Corner route test](game-corner-redemption.md) gives the original clerk rule retained in both presets. Earlier recommendation labels below document the initial analysis.

The [later review](foundation-audit.md#gift-map-and-engine-decisions) checks the full transaction order at all 47 direct gift calls. The [usability inventory](usability-coverage.csv) now gives current preset placements beside the earlier findings.

Reviewed **2026-10-15**. This review covers rewards, purchases, item effects, Pokémon handling, field actions, progression, saves, text, sound, and graphics, as well as menus. The English Red/Blue reference is `pret/pokered` at `af519899719f0754965776faac0e836a3b906e6d`; its remote master head matched that pin during this review.

## Findings and recommendation

The strongest additions are small failures of an existing action or of its feedback: a wrong coin award, a wrong affordability check, a lost gift, and incorrect text or sound. These fit the existing [bug policy](../docs/03-bug-fix-policy.md) without adding a new game rule. Vending affordability, trade follow-up, Flute feedback, elevator floor handling, and quantity shortcuts are now accepted Core requirements. The subsequently reported rooftop exchange loss is a Core defect repair. Other recommendations retain their stated review status; no game patch is implemented.

A useful default improvement removes an unnecessary input step or makes existing state clear while retaining its costs and limits. Manual Flute use at Snorlax remains in Core because a prompt may disclose a puzzle solution; that contextual shortcut is deferred. A larger bag, free healing, a move relearner, or an escape from every battle has different effects and needs its own developer feature design.

“Small” describes the proposed scope, not a measured implementation estimate. The findings below are checked against source, not reproduced in a running game. A changed branch still needs the listed game checks. The code does not supply the original team's internal design reasons.

## Narrow corrections to prioritize

| ID | Source finding | Recommendation | Existing record |
|---|---|---|---|
| [UA-01](#ua-01) | A hidden Game Corner event encodes 40 coins but selects the 20-coin award path. | Award the encoded 40; retain the Coin Case and capacity rules. | CAT-057, now source-confirmed |
| [UA-02](#ua-02) | All three vending selections check for ¥200 before loading their actual price. | Check the selected drink's actual price before giving it. | New finding in this audit |
| [UA-03](#ua-03) | Oak sets his five-Poké-Ball gift flag before delivery and ignores delivery failure. | Leave the gift available after failure and use an accurate no-room response. | New finding; related to CAT-083's separate layout fault |
| [UA-04](#ua-04) | Two trade entries use a follow-up that says the Pokémon evolved; one is Raichu. | Correct the false statement without changing the trades or evolution rules. | CAT-084 / RGB-010b |
| [UA-05](#ua-05) | Oak's throwing instructions write two successive strings to the same bottom line. | Preserve the instructions and scroll/reflow them correctly. | CAT-083 |
| [UA-06](#ua-06) | Oak's introduction displays Nidorino but requests Nidorina's cry. | Match the cry to Nidorino. | CAT-082 / RGB-025 |
| [UA-07](#ua-07) | Poké Flute can wake the wild opponent without giving the wake-up confirmation. | Derive the response from the sleepers actually woken. Preserve its effect and turn cost. | New narrow feedback finding |

<a id="ua-01"></a>

### UA-01 — Hidden 40-coin award

**Verified:** the event at Game Corner coordinates X=11, Y=7 passes `COIN + 40`. The conversion branch for 40 jumps to `.bcd20`, leaving `.bcd40` unused. The message prints the converted amount, so the original also reports 20. This is not a case of showing 40 while crediting 20. [E88](evidence.md#e88)

**Scope:** use the existing 40 conversion. Preserve discovery, one-time flags, Coin Case ownership, and the 9,999-coin cap. Do not add Itemfinder hints or change other rewards as part of this correction.

**Required checks:** all four encoded amounts, first/repeated pickup, no Coin Case, and balances around the cap. Verify credited amount and displayed amount together. The cap's original overflow/discard behavior is a separate design choice.

<a id="ua-02"></a>

### UA-02 — Vending affordability

**Disposition:** accepted Core repair, PN-010 / RGB-031.

**Verified:** the menu loads ¥200 into the affordability check for every drink. Only after that check does it load Fresh Water ¥200, Soda Pop ¥300, or Lemonade ¥350. After delivery it subtracts the actual price. The shared subtraction clamps a negative result to zero. With room in the bag, ¥200–299 can therefore pass the Soda Pop check, and ¥200–349 can pass the Lemonade check. The code supports an underpayment, not a money-wrap windfall. [E89](evidence.md#e89)

**Scope:** load the chosen price before checking funds; give no drink and take no money on refusal. Preserve all three prices, item effects, delivery feedback, and bag rules. A repeated-purchase menu is a separate proposal.

**Required checks:** each drink at price minus one, exact price, and price plus one; ¥0/199/200/299/300/349/350; full bag versus space in an existing stack; cancellation; one correct deduction per successful delivery. Coordinate with inventory splitting rather than assuming its failure path is safe.

<a id="ua-03"></a>

### UA-03 — Gift delivery before completion flags

**Verified:** Oak's optional gift sets `EVENT_GOT_POKEBALLS_FROM_OAK` before `GiveItem`, ignores its success result (the assembly carry flag), and prints the success text. `GiveItem` reports failure if inventory insertion fails. In a full-bag/no-Poké-Ball fixture, the flag can be committed without receiving the five balls. [E90](evidence.md#e90)

The gift has other conditions: fewer than two owned species, no Poké Ball in the bag, and the first Route 22 rival victory. A normal progression fixture must retain those conditions, including keeping the starter unevolved if needed. A full bag injected into a fixture proves the local failure path; it is not by itself proof of a normal route to that state. The missing reward is five ordinary, buyable balls, not an irreplaceable key item or a demonstrated progression lock.

**Scope:** check delivery before committing the flag or saying the reward was received. Allow a later attempt while the existing eligibility conditions still hold. Preserve the amount and acquisition conditions.

A screen of all **47 direct `GiveItem`/`GivePokemon` calls under `scripts/`** found 45 with a nearby carry check and two without: Oak's gift and the Parcel delivery. The [call-site table](gift-call-sites.csv) records the screen. A nearby check is a lead, not proof of a whole script's safety.

The Parcel script also ignores delivery failure. A full starting bag is not established as reachable in the unmodified early game. Treat this as a foundation boundary to guard when downstream games change starting items, not as a proven vanilla softlock. Regular ground pickups, hidden items, Oak's aide rewards, and the selected Pokémon gifts already retain their object/reward after ordinary capacity refusal. Preserve those paths. [E100](evidence.md#e100)

**Required checks:** no room, room after a refusal, existing stack, ordinary success, repeated conversation, changed eligibility, and save/reload. No false success, duplication, or lost completion flag. For gifts of Pokémon, test full party and full current box separately.

<a id="ua-04"></a>

### UA-04 — False trade follow-up

**Disposition:** accepted Core text repair, PN-012.

**Verified:** the Poliwhirl→Jynx and Raichu→Electrode entries use the evolution dialogue set. Its post-trade text says the Pokémon given to the NPC “went and evolved.” This is false for the Raichu trade under the retained game data. The source comments also describe a localization history, but comments in this reconstruction are not original developer testimony. [E91](evidence.md#e91)

**Scope:** choose truthful follow-up wording that works for both users of that text. Keep the species requested and received, nicknames, trade effects, and evolution conditions. English Yellow's wording is a possible reference, not a reason to change these trades.

**Required checks:** both affected trades, other dialogue sets, name substitution, line layout, and follow-up visits. This is a text repair, not a Raichu evolution feature.

<a id="ua-05"></a>

### UA-05 — Oak's overwritten instructions

**Verified:** the Poké Ball explanation uses `line` twice in succession. That macro starts at the bottom line; `cont` scrolls to the next line. The second `line` overwrites the preceding bottom line. [E92](evidence.md#e92)

**Scope:** reflow the existing words with the appropriate scroll command. Review other catalog layout leads individually. For example, the archived Route 8 “chem” complaint is explicitly subjective; that abbreviation is not proved to be a typo.

**Required checks:** complete visible instructions at each text speed and ordinary input. Keep deliberate abbreviations, character voice, and pauses unless they cause a confirmed fault.

<a id="ua-06"></a>

### UA-06 — Introductory cry

**Verified:** the picture selection is Nidorino; the speech issues the Nidorina cry command, whose sound table maps to Nidorina. [E93](evidence.md#e93)

**Scope:** request the matching species cry. Audit users of the shared command before renaming or remapping it. Do not replace the soundtrack or redesign cries.

**Required checks:** intro picture and sound together, ordinary new-game/name flow, and other users of the same text-sound command. Source verification does not replace listening to the built game.

<a id="ua-07"></a>

### UA-07 — Poké Flute feedback

**Disposition:** accepted Core feedback repair, PN-011 / RGB-032.

**Verified:** the item clears sleep in the active wild opponent's status, but its response flag is set by party scans. In a wild battle with only that opponent asleep and other scanned slots awake, the effect can succeed while the flag remains zero. It selects the “catchy tune” response and omits the wake-up confirmation. The literal words “no effect” are not displayed. [E94](evidence.md#e94)

**Scope:** account for actual sleep before clearing it when choosing feedback. Preserve who wakes, item ownership, battle action costs, and other sleep behavior. This does not authorize modern sleep rules. Do not add a general refund for failed battle items.

**Required checks:** only the wild opponent asleep; only a player party member asleep; both; neither; trainer battles; and other status bits. Check message, sound, and resulting statuses. The helper scans six slots, so unused-slot state also needs a separate boundary fixture.

## Confirmed paths that need more display testing

| ID | Finding and scope | Why it is not yet a ready small patch |
|---|---|---|
| UA-08 | Trainer cure paths clear status but do not redraw the status area; the restoration path updates HP separately. Refresh visible state without changing AI choices, healing, or RNG. Existing RGB-024 / CAT-025. [E95](evidence.md#e95) | Capture exact stale frames after Full Heal/Full Restore, then verify ordinary healing and status drawing. |
| UA-09 | Escape/teleport spin paths enter a routine that reads a facing-list pointer while the pointer register HL still points to animation state. Restore the proper pointer. CAT-037. [E96](evidence.md#e96) | The pointer mismatch is source-confirmed. The reported original Game Boy/Super Game Boy appearance and a repair still need captures and hardware-mode checks. Keep warp and collision state unchanged. |

These fit the correctness category. Their visual checks matter even if a candidate edit is short.

## Small usability proposals worth choosing next

The table separates accepted scope, supported proposals, and deferred changes. None proves the original team's design reasons. Keep each independently scoped.

| ID | Proposal | Preserved choices and required review |
|---|---|---|
| UA-10 | **A at Snorlax → offer Poké Flute**, when it is in the bag. | Deferred outside the default. Preserve the manual puzzle interaction in Core. A later optional prompt would still need ownership, confirmation, the same event/battle, and existing loss/escape outcomes. The present interaction only gives sleeping-Pokémon text; manual Flute use already starts the event. Do not offer an unexplained solution before the Flute is owned. [E98](evidence.md#e98) |
| UA-11 | Identify machine moves. | Both presets include machine numbers, names and INFO in the bag, PC and offers. [Current scope](sweep-decisions.md) |
| UA-12 | Show occupied places. | Both presets show the bag, item PC, active Pokémon box and highlighted CHANGE BOX count. [Scope](sweep-decisions.md) |
| UA-13 | **Show the current elevator floor and prevent same-floor travel.** | Accepted PN-013. Current-floor input cannot cause travel animation/sound or warp-state changes. Prefer disabling/skipping that entry; keep other floors and exits. The checked menu lists destinations but provides no current-floor marker. Derive the label from the entered floor rather than stale menu selection. [E97](evidence.md#e97) |
| UA-14 | **Left/right quantity changes of ten.** | Accepted PN-014. Up/down already changes one and wraps to the maximum; retain both. Do not auto-buy the largest affordable amount or change caps. Specify endpoints and price recomputation. [E97](evidence.md#e97) |
| UA-15 | **Clear confirmation before overwriting a learned move.** | Safety candidate with a real tradeoff: one more step for every replacement. The current selection commits after choosing a non-HM move, though B can abandon learning. Show old/new move and Pokémon, with No/B returning to selection; retain single-use consumption only after success. The accepted release safeguard does not already approve this prompt. [E97](evidence.md#e97) |

A caught-status marker in battle is another reasonable information proposal. It shows a recorded fact rather than new species data. It still needs a UI design and Ghost/Transform/Dex-ownership checks. It is less urgent than incorrect feedback and is not included as an automatic Core requirement.

Static move details are included in both reference presets. Hidden DV/stat EXP displays, encounter guides and Itemfinder directions each have separate information rules.

## Safety work beyond menus

**Progression traps:** the existing queue already covers cut-tree traps, Oak-follow collision, disabled encounters, and bad new-game flags. Reproduce their exact states and repair the responsible event/collision path. Do not solve every report with a new free teleport, changed map, revised freeze rule, or a universal battle escape. Those can change the rules being preserved.

**Money gates:** Red/Blue's Safari entrance rejects less than ¥500. Saffron requires a carried drink, with vending purchases as the normal source. English Yellow has lower-cost Safari paths and eventually a one-ball route at zero money. These local checks and Yellow alternatives are verified; a claim of permanent Red/Blue deadlock also needs a state with no remaining recovery income/items/actions. [E99](evidence.md#e99)

A narrow recovery design deserves attention. It must define when help is available, what it costs, and how ordinary admission stays unchanged. Do not call permanent free Safari entry or removal of the drink gate a noncontroversial bug fix. This is important research, not a promised one-line correction.

**Data and saves:** inventory split bounds, incomplete save writes, Transform/PP metadata, and link state deserve high priority where reproduced. They are already recorded. Save recovery needs a real write/restore design and compatibility checks; adding a delay or a warning does not make writes safe. Severity and implementation effort are different.

**Accessibility and responsiveness:** reduced flashing and a bounded/reduced low-HP alarm are useful developer options to explore. Preserve the warning information. Text/animation speed, fewer pauses, and faster travel change pacing to different degrees. Keep them separate from wrong sounds, stale status, or a corrupt sprite. No medical safety claim or new player-settings layout is made by this audit.

## Existing behavior and settled choices to protect

- Accepted PN-001–PN-015 remain settled; they are not new proposals here. Medicine still returns to the bag. Repel renewal and MOVE POKÉMON remain optional. Under D55, automatic placement is also a separate developer option.
- TMs already reveal their move before teaching and display learnability in the party screen. An incompatible/already-known target does not consume a TM. A generic recommendation to add those protections would duplicate existing behavior. [E97](evidence.md#e97)
- The Pokédex already supports left/right page jumps. Item lists already support SELECT reordering. Quantity selection already wraps below one to the maximum. Preserve them. [E97](evidence.md#e97)
- The checked Name Rater can decline/cancel and retains its original-owner restriction. The Day Care already rejects a last party member and an HM user and checks return capacity/payment. These are existing safeguards; automatic move replacement and traded-name rules are separate design questions. [E100](evidence.md#e100)
- Adding bag slots, removing used quest items automatically, opening remote storage, relaxing field-move requirements, or removing Safari limits affects retained constraints. These remain developer-feature proposals, not incidental cleanup.
- Protected battle quirks stay protected. No general AI upgrade, rebalanced item effect, different type chart, or changed freeze/trapping rule follows from this review.

## Coverage and limits

The [coverage table](usability-coverage.csv) records 63 cases across the main routine systems. It distinguishes newly traced defects, accepted requirements, existing research, proposals, and retained behavior. The separate [gift-call screen](gift-call-sites.csv) lists every matching direct call under `scripts/`, including the exact nearby lines used for its mechanical screen. Both are snapshots of the stated pin.

The 94-entry archived bug intake remains intact. This pass promotes six catalog leads to source-confirmed status and adds several findings outside that catalog. Existing source-confirmed arithmetic records were checked for overlap, not reimplemented. PureRGB's feature list was used to find leads, not as proof that a feature belongs in Core or that its patch passes tests.

This is a broad source audit with explicit boundaries. It is not an exhaustive review of every map tile, all prose, every assembly path, or every possible legal playthrough. No ROM was built, no emulator/hardware regression was run, and no personal save was used. Link/save fault injection, screenshot/audio checks, and normal-play reproductions remain implementation work. The evidence index records exact paths, revisions, ranges, and file hashes for the new source claims.

<a id="ua-16"></a>

## UA-16 — Rooftop drink/TM loss

**Verified:** payment precedes TM delivery for all three drinks. The ordinary no-room branch does not restore it. A full bag with two drinks in the selected stack can lose one; the last drink can instead free a slot. Successful delivery sets the reward flag, while failure leaves it clear. The checked ordinary path does not demonstrate duplication. [E101](evidence.md#e101)

**Disposition:** Core defect repair [PN-015](../docs/13-playthrough-intake.md#pn-015), with all-or-nothing payment/reward checks. The earlier nearby-branch gift screen did not assess this ordering; its table now marks those calls. The [completed source-order review](gift-call-sites.csv) covers all 47 direct calls. The [remake comparison](remake-usability-comparison.md) records FireRed clues, static-information proposals, and the decision to defer contextual Flute use at Snorlax. Optional battle information is a separate accepted Extension direction.

## Item-list position follow-up

The item-PC return destination is already correct, but that does not establish row/scroll preservation. [E106](evidence.md#e106) confirms shared resets when a stack is deleted, plus separate row resets in shop loops. [PN-019](../docs/13-playthrough-intake.md#pn-019) accepts same-list position retention for item actions, with adjacent-entry selection after deletion and safe bounds. Preserve the existing medicine flow and successful Pokémon-transfer destinations. No game patch is implemented.

## Move reordering, stable box positions, and encounter boundaries

[The focused review](cursor-box-and-trainers.md) adds a source-confirmed move-cursor reset and box-order difference. PN-021 accepts cursor retention during SELECT; PN-022 selects append order for new boxed arrivals while preserving storage limits and full-record identity. D39/PN-023 restores sight for the three Burglars and keeps the three Scientists’ original behavior. The source verifies these states without proving the original design reasons. No game patch or runtime regression is included.
