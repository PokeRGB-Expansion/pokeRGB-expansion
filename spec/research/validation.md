# Specification validation

Specification 0.1.48 adopts [move INFO](../docs/15-battle-information.md). [Eight stock level-up fixtures](move-info-stock-checks.json) ran in SameBoy 1.0.5 on hash-matched English Red and Blue. In each color a level-31 Alakazam with four moves reached the replacement question with its moves and PP intact. With an empty slot it learned Recover with 20 PP. With Recover already known, or at level 32 without a new move, the routine returned without an offer. These are stock routine checks at the choice or write boundary. The new INFO control still needs tests in the game builds. The six prior stored-TM withdrawal cases and eight hidden-coin boundary checks also passed again.

Specification 0.1.47 records a [player-impact and decision audit](sweep-decisions.md). Six stock TM50 withdrawals in English Red and Blue tested when viewing the name of a stored machine would bypass a real bag-space requirement. Integrated UI behavior still needs tests for any display that is adopted.

Specification 0.1.46 compares paid Porygon redemption in stock Red and Blue with the withdrawn full-lot rule. It also checks insufficient funds, cancellation, full storage and a separate hidden pickup. The [test report](game-corner-redemption.md) distinguishes emulator runs from the balance model. The [Day Care comparison](day-care-history.md) identifies which games share the move rule and what their attendants actually say. Green’s Blue-equivalent results remain acceptance tests for the eventual integrated build.

Specification 0.1.45 records [the final scope review](final-scope-audit.md), the [paired-edition comparison](emerald-rogue-builds.md) and [measured stock and prototype results](scope-sweep-checks.json). Public readiness depends on the [complete integrated Core](../docs/09-roadmap.md#public-release-checks).

Specification 0.1.44 adds the [Minimal action review](minimal-action-review.md), [storage policy and source study](storage-policy-and-code.md), [refactor inventory](refactor-scope.md) and [fixture results](minimal-and-storage-checks.json). Eighteen stock cases cover the cursor, Counter, received field moves and the two save operations. The experimental ROMs passed 336 read-only destination searches and 24 original address checks. No test caught a Pokémon into another box. The named game presets remain planned.

Specification 0.1.43 includes [the controlled outcomes](core-refinement-checks.json) for the data-rule, field, capture and box-picker reviews. This review recorded 141 stock fixtures and 98 experimental-build fixtures. The 239 checks consist of 136 calls to type adjustment, 48 battle turns, 8 field routes, 6 capture menus, 24 capture gates, 3 PC round trips, 12 box-picker save cases and 2 numeric-count readouts. The save-memory allocation study is separate from those executions. The temporary builds are research fixtures. [Battle runs](core-rule-precedents.md) · [Field routes](field-shortcut-contract.md) · [Storage gates](box-overflow-contract.md) · [Cancellation and counts](box-picker-safety.md)

Specification 0.1.42 adds the [Red/Blue/Yellow retail table check](yellow-data-diff.json), [independent move checks](yellow-behavior-checks.json), [Yellow turn and movement fixtures](yellow-rules-review.md), [Guard Spec. and AREA checks](developer-hack-comparison.md), and [compiled wide-ID layout checks](species-id-architecture.md). The tutorial inventory covers 108 linked subjects and all nine to-do lines at the pinned index revision. A separate disposable one-permission Red/Blue build exercised Charizard’s Fly option. Game implementation remains a separate milestone.


On 2026-11-22 the [pre-build investigation](foundation-audit.md) added 36 stock Red/Blue battle fixtures and linked-table checks. [Recorded observations](foundation-checks.json) distinguish these from tests of a patched game. The 94 case dispositions and 47 gift paths have a complete source review.

Specification **0.1.40** reviewed on **2026-11-22**. D44 and D45 record individual battle and preset decisions. D57 governs publication. The existing stock-ROM checks in E120–E122 provide the donor survey baseline. Core patch tests are pending.

Initial source research and arithmetic checks completed on **2026-10-11**. Further code and historical checks completed on **2026-10-12**, with EXP. ALL, SELECT-control, and storage source checks on **2026-10-14**. Document links, record structure, cited repository file hashes/ranges, and source revisions rechecked for specification **0.1.22**. Focused shop and party-menu source paths were rechecked on **2026-10-15**. Existing repository pins and the critical-hit model are unchanged. A new FireRed/LeafGreen reference supports the badge comparison. Additional pins cover Stadium text notes, Shin Master, selected English Yellow data, Emerald Expansion configuration, and the original Emerald reference.

## Completed

- Read selected files at the seventeen Git references in the source lock. Some references cover the same repository at separate branches or revisions.
- Checked all cited repository paths, line ranges, file SHA-256 values and repository revisions against the local source checkouts.
- Checked all local Markdown links and referenced anchors.
- Confirmed the intake has 94 distinct entries, matching the pinned archived-catalog heading count.
- Generated 1,024 critical-threshold rows and checked the rotated-byte comparison over each possible random byte.
- Derived that pinned Solus differs from vanilla in 508 of 512 unpumped Speed/move-class inputs; the proposed formula preserves all 512 in the arithmetic model.
- Checked the version-selection intake has 119 source sites. Each is still marked unreviewed for implementation purposes.
- Traced stat-penalty paths, Itemfinder's coordinate comparisons and table, the donor status-medicine path, and OHKO/X Accuracy boundaries. The evidence index contains 114 records after the Route 21 spatial-context review.
- Visually inspected the cited guidebook pages, recorded PDF fingerprints/page locations, and checked the official Stadium descriptions. Guide scans remain research inputs outside this package.
- Checked selected PureRGB species/move data, Ghost damage selection and trapping duration; recorded documentation limits on restoring original rules.
- Read the primary design essay and recorded it as opinion. Checked selected Stadium text notes without claiming an executable mechanics audit.
- Checked the Master/Lite Hyper Beam paths, Eevee/Jolteon move access and evolution data flow, and the Sabrina gym text against the retained chart.
- Read current Emerald Expansion generation/family controls, a guarded species record, separate encounter data, rule/data defaults, graphics switches, and configuration policy at the added expansion-config pin. No configured Emerald build or vanilla-equivalence test was run.
- Compared the original Emerald and Expansion random-number functions. Checked Expansion's basic trainer flag group and its documented AI and multiplayer boundaries. Recorded the original decompilation's published output hash without claiming a successful build.
- Extended the AI documentation citation to its per-trainer flag example. This confirms developer controls; it does not verify a complete original-AI profile or the maintainers' reason for that boundary.
- Checked EXP. ALL's key-item flag, shared bag/PC toss guards, one-time reward event, PC storage paths, key-item selling restriction, and battle presence check. Recorded the accepted safeguard separately from the unresolved allocation report. No game patch or executable inventory regression was performed.

- Checked the overworld and list SELECT paths, Bicycle use routine, separate forced-riding menu guard, and door-exit input mask. Recorded PN-002 as an accepted feature without claiming a working shortcut.

- Traced Bill’s PC capacity check, list display, selected-Pokémon STATS/withdrawal actions, transfer/removal calls, and existing error text. Recorded PN-003 without claiming a working PC-menu patch.

- Checked the ball-use guard for a full party and full current box, the demonstration bypass, and the existing failure message. The pinned remote ball-use file also matched the local Git object. Recorded E71 and the optional storage directions without claiming a storage implementation.

- Confirmed the bag's 20-slot constant, insertion guard, working-memory allocation, and save-copy boundary. The source does not establish the original designers' reason for choosing 20.
- Traced learned field moves, all five HM badge checks, Cut targets, Surf permissions/collisions, Strength activation/pushing/reset, and the A interaction path. Checked the pinned remote menu/constants files against local Git bytes. Recorded PN-004 without claiming a working contextual shortcut.

- Checked EXP. ALL's zero price and false key-item flag against the Bicycle's protected flag, plus shop refusal, sale/removal paths, and the exact refusal text. The pinned remote shop file matches local Git bytes. Expanded PN-001 explicitly to prohibit selling; no executable transaction test was run.

- Rechecked Red/Blue badge-bit assignments and battle-stat field order. Traced FireRed/LeafGreen badge award flags into Speed/Defense calculations and checked cited files against the pinned Git objects. Visually inspected the original US manual cover, copyright page, and printed page 27, plus Prima printed pages 26 and 47. Recorded the likely-intent inference and the limits of the interview search before the later D25 mapping decision.

- Rechecked the current Solus, Shin Lite, PureRGB, and Solid Red branch heads against their pins. Compared their badge routines and gym/badge-house text, including field layouts for the sequential routines. Recorded D25 as the accepted Core mapping correction with independent stacking protection. No donor or PokéRGB executable test was run.

- Confirmed the reported Oak spelling error, the 60–69 rating selection, and shared PC/Lab/Hall of Fame callers. Recorded PN-005/RGB-010c as a Core text correction, with layout checks still required. Clarified D25's intent rationale without claiming certainty or an implemented code patch.

- Traced PC STATS/action returns, original page input, all four STATS caller contexts, release default/removal order, and selected party/shop/player-PC/medicine return paths. Rechecked the upstream branch head against the pin. Recorded a bounded inventory, accepted navigation/release scope, preserved medicine flow, and optional Repel renewal. No game menu implementation or executable regression was performed.

- Rechecked the exact party action B/CANCEL branches and shop refusal/failure destinations against the pinned Git files on 2026-10-15. Promoted MN07/MN08 to the accepted PN-008 Core requirement with MN04 tracked separately. No game patch or executable transaction check was performed.

## Not completed or claimed

No ROM build, gameplay reproduction, game fix, executable game regression, CI implementation, hardware test, link test, save migration or public release was performed. Source-confirmed observations are not presented as those outcomes.

Mutable web references were checked where reported in the evidence index. The validation script does not establish continued external-link availability or the accuracy of every donor feature claim.

The validator checks repository source fingerprints when `--source-root` is supplied. It does not download or inspect the historical PDFs. Their recorded fingerprints identify the copies reviewed; later checks need to fetch and inspect those sources separately.

## Repeat the artifact checks

```sh
python3 tools/analyze_critical_hits.py
python3 tools/validate_spec.py
```

For cited-source verification, supply `--source-root` to the validator with checkouts in directories named by the keys in `source-lock.json`, at their recorded revisions. The validator checks file fingerprints and line ranges; a human still needs to assess whether the source supports a claim.

- Recorded D29/PN-009 as the accepted MN04 correction after clarification: CANCEL returns to the overworld party list, matching B. Source evidence is unchanged; no game patch or executable menu regression was performed.

- Completed a bounded broad source audit on 2026-10-15: 57 routine-system cases and 47 direct script gift calls. Added E88–E100 with exact file hashes and ranges, and promoted six archived leads to source-confirmed status. The reference and PureRGB remote heads matched their existing pins. Compared pinned English Yellow admission code without adding a release target. No game build, emulator/hardware regression, or save-file operation was performed.

Reviewed rooftop payment/reward ordering, precise drink-stack failure conditions, selected FireRed and Gold/Silver comparisons, and current Expansion battle-information controls on 2026-10-15. Added E101–E105, two separate pins, a 61-case coverage table, and an explicit transaction-order field in the 47-call gift screen. Earlier source revisions and the critical-hit model are retained. No game implementation, runtime regression, personal-save operation, or original-intent proof is claimed.

On 2026-10-20, read Increase-Bag-Space.md at the existing wiki pin and checked original capacity constants, count/slot/terminator allocations, the 128-byte reserve, and main-data save/load copies. Derived 122 bytes for 60 slots and a 63-slot arithmetic bound for that reserve. Source pins remain unchanged. No 60-slot build, executable test, complete PC-expansion design, or save conversion was performed.

On 2026-10-23, repeated seven RAM allocation checks with RGBDS 1.0.4 using the retained pokered revision. The original 20-slot allocation and a constant-only 21-slot variant link; the latter shifts money. Constant-only 40/60 variants fail at the fixed stack boundary. Separate-reserve 60/64 variants link with all other existing WRAM addresses unchanged; 65 fails the explicit allocation assertion. The [method and results](bag-memory.md) state the RAM-only scope. No full ROM, game regression, save migration, or feature-combination test was performed.

On 2026-10-23, selected the 64-slot preset within the accepted separate reserve. Reviewed the existing initializer and FillMemory for E109: new-game setup must initialize the enabled bag after the progress clear. The earlier 60/64/65 RAM audit remains allocation evidence. This specification update adds no playable feature, runtime repair, save conversion, or combination test.

On 2026-10-24, traced the SELECT mark/completion redraws, both box insertion routines and shared gift/naming paths, and all six Mansion trainer classes/ranges plus their sight and talk handlers. Added E110–E112, three playthrough records, three coverage cases, and MN16. Selected cursor retention and consistent append as Core usability changes while preserving passive Mansion Burglars. Source pins and original conversation bytes are unchanged. This is specification/source validation without a game implementation, runtime reproduction, or save-file operation.

On 2026-10-25, compared ordinary zero-range trainers and the Mansion Burglars at four existing reference revisions. Verified E113 file hashes/ranges and ordinary trainer identities, plus the Gold/Silver and FireRed/LeafGreen sight paths. The comparison records Yellow continuity and the remake's range-one change without treating either as proof of original intent. No game build, runtime comparison, save operation, source-pin change, or Core encounter change was performed.

On 2026-10-25, decoded Route 21's 450 map blocks through the overworld blockset and combined the result with all four Fisher positions and directions. Inspected source-rendered crops of both land patches. Every forward square includes water; Fisher2's includes a shore lip. E114 records the binary fingerprints and derived geometry. No in-game test or original-intent proof was performed.

On 2026-10-25, updated the selected behavior for PN-023/D39 and its acceptance cases. Retained the original zero-range source findings and qualified historical intent. This was a requirements update without a new source finding, game implementation, runtime test, save change, or personal-save operation.

On 2026-10-25, checked E115 at the retained Red/Blue and Yellow source revisions. Decoded every Viridian Forest map square; confirmed 251 ordinary and 114 lower-right-mismatch grass squares, matching map/blockset bytes across versions, and each cited source fingerprint/range. Inspected the two source grass graphic tiles. These are static source checks. No executable game, ROM, save, or personal playthrough was changed or tested.

On 2026-10-25, recorded D40/PN-024 as accepted Core scope and aligned the feature catalog, triage, roadmap, and release checks. This was a requirement update. It adds no source finding, game code, ROM build, runtime result, or personal-save operation.

On 2026-11-22, verified the new Acid Armor source fingerprints and ranges. Used RGBDS 1.0.4 for Red/Blue symbols and 1.0.3 for Yellow symbols. SameBoy 1.0.5 ran 48 move cases and 18 follow-up cases on the original ROMs using an in-memory party and controlled move slots. Red and Blue ran in Game Boy mode. Yellow ran the main matrix in Game Boy and Game Boy Color modes. The tests covered single-player wild battles. Other games and hacks were compared in source or from author notes. See [the results](acid-armor-baseline.json).

SameBoy ran 76 more cases across the four version and hardware combinations for E119. The harness used the regular battle menus and controlled moves. It measured the loaded graphics, screen picture, and battle state separately. The total is 142 single-player stock-ROM checks. The results support the accepted repair in PN-025. [Stock-ROM results](acid-armor-baseline.json)

On 2026-11-22 a fresh archive of pokered revision af519899719f0754965776faac0e836a3b906e6d built with RGBDS 1.0.4. Upstream `make compare` matched the Red, Blue, and Blue debug ROMs and both Virtual Console patch hashes in `roms.sha1`. The critical-hit calculator also reproduced the checked-in 1,024-row table byte for byte, including all 512 unpumped cases. Verification of the proposed formula in compiled Core code remains pending. See the [Core readiness review](../docs/09-roadmap.md#public-release-checks).

## November upstream update

On 2026-11-22, upstream master pointed to `ba9c0568f64ae602fadda577a08c66639f93082a`, nine commits after `af519899719f0754965776faac0e836a3b906e6d`. Both pins build with RGBDS 1.0.4. A fresh clone of the new revision passed all five upstream `make compare` checks for Red, Blue, debug Blue, and the two Virtual Console patches. The source files for the four audited fixes match the previous revision. The update changes no Core, Minimal, or Extended decision. [Commit comparison](https://github.com/pret/pokered/compare/af519899719f0754965776faac0e836a3b906e6d...ba9c0568f64ae602fadda577a08c66639f93082a)

The changes improve source names and comments, add a build-time assertion for Twineedle, and update host tools including the include scanner. Use the new joypad and serial timeout labels for new fixtures. The serial routine now documents an existing timer-register issue. The Hall of Fame work buffer now accounts for a possible terminator. Comparing Red and Blue symbol files separately found the same addresses for all 2,819 shared w/h/s-prefixed RAM symbols checked in each build. Use the earlier research pins to reproduce archived source ranges and digests. [Serial routine](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/home/serial.asm#L27-L42)

The [Core scope review](core-scope-review.md) records 58 stock Red/Blue battle cases and 7,680 modeled Gym switch inputs across the two builds. The evidence distinguishes those results from future patch regressions.
