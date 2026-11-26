# Testing and continuous integration

The [test runner](../../tests/run.py) lists the checks that run on the current source. The [build instructions](../../README.md#tests) show how to run them. The rest of this document describes the cases to check when changing a feature or making a release.

## Field, menu and battle checks added after v0.2.0

| Area | What the game checks |
|---|---|
| Field and map | Open OPTION in dark Rock Tunnel, after Flash and outdoors. Trace Town Map pins from Route 1 and the Power Plant. At both Cycling Road gates, try held and released direction input with and without a Bicycle. [Field tests](../../tests/field_sweep.py) |
| Party, items and Pokédex | Use SELECT in the party, confirm the item and amount in a TOSS prompt, register and use fishing rods, and browse the Pokédex by name. [Field menu tests](../../tests/field_menu_features.py) |
| Supply and move INFO | Open supply details in the Bag, item PC and at a Mart. Read a move’s priority or high-critical property through FIGHT. Check the menu cursor, inventory and PP on return. [INFO tests](../../tests/supply_and_move_info.py) |
| HP and level-one EXP | Compare full and damaged HP meters at high maximum HP. Catch and receive a level-one Pokémon into the party and an active box. Award its first seven EXP and check the resulting level. Check all six growth curves at levels one and two. [HP and EXP tests](../../tests/hp_and_level_one.py) |
| Core services | Enter the Fuchsia Move Deleter’s house, cancel and confirm deletions, and check moves and PP. Switch EXP. ALL in the Bag and test its supported and refused uses. Compare Minimal’s paths. [Service tests](../../tests/core_services.py) |
| Battle pace | Choose Quick through OPTION, save and Continue. Compare the same attack in Normal and Quick. Check damage, PP, input, music state and play-clock ticks. A link battle, tutorial or Safari battle keeps its ordinary pauses. [Pace tests](../../tests/battle_pace.py) |

## Baselines and test oracles

An oracle is the independent expected result for a test. Use the pinned vanilla source/ROM for preserved behavior and the approved contract for corrected behavior. A donor hack is a candidate implementation, not the expected result by default.

Keep two independent builds: pristine upstream and the modified foundation. First establish upstream byte identity using its published hashes. After fixes, stop expecting the modified builds to match vanilla hashes. Instead compare protected behavior and list the intended changes.

The upstream comparison covers five outputs: Red, Blue, Blue debug and two Virtual Console patches. Use `make compare BASELINE_DIR=/path/to/upstream/outputs` to verify a pristine build against those hashes. The modified games have their own release hashes. [E01–E03](../research/evidence.md#e01)

## Cartridge tests

The tests use SameBoy 1.0.5 to run the built game. They use its symbol files to set up cases and the Game Boy buttons to drive menus. Critical-hit checks supply controlled rolls through the link battle random number list. They exercise the shared random byte reader in one game instance. The two-endpoint tests below cover separate link requirements.

A small test-only assembly entry point may initialize a routine fixture and write result bytes to a mailbox in RAM. The runner can stop at a symbol or completion byte. It must execute the compiled routine, preserve registers/banks needed by production, and fail on timeout. A Python reimplementation alone cannot prove the game's implementation correct.

For integration, boot the normal game or a test-only battle initializer and observe actual turns, damage, status, PP, prompts and storage. Keep test hooks out of release builds and verify release behavior through some end-to-end cases too.

A fixture records test ID, RGB/MC requirement, game and tool revisions, variant, battle mode, initial state, input sequence, RNG bytes, expected outputs, time limit, and supporting evidence. Attach failure traces rather than only a screenshot or “passed.”

## Required regression groups

| Group | Required checks | Passing evidence |
|---|---|---|
| Build baseline | Pinned RGBDS 1.0.4; pristine Red/Blue and appropriate reference debug/patch hashes | Complete build log and hash manifest |
| Critical-hit threshold | Both actors, all 256 Speed values, ordinary and high-critical moves, with and without Focus Energy | At each threshold, check the critical flag and random-byte count against the expected result for the preset. |
| Critical-hit damage | Physical/special, stat boosts/drops, badge effects, burn/paralysis, screens, level and byte boundaries | Original preserved results; approved invalid-state corrections listed |
| Hyper Beam | KO, survives, miss, Substitute survives/breaks; both actors; next turn | Recharge/action trace |
| Fixed damage | Night Shade→Normal, Seismic Toss→Ghost, Dragon Rage/SonicBoom/Psywave/Super Fang; target checks | HP difference, hit/miss, no type multiplier, same RNG use where preserved |
| Types and display | All attacking/defending pairs, both type orders, monotypes, immunity and cancellation | With the same chart, the feedback fix preserves damage. Compare Minimal to stock and Core to D50. |
| Trapping/status | Duration choices, faster/slower actor, wake turn, freeze cures, confusion/paralysis interruption, copied moves | Complete turn-state/PP trace; no stuck flags |
| Badge stat mapping | All 256 badge masks; stat values 1–999; Thunder/Speed and Soul/Defense; both award orders; rounding, cap, stacking, and link exclusion | Only approved mapped-stat differences; original descriptions; preserved Attack/Special and RNG use |
| Stat recalculation | RGB-027 retained penalties, RGB-013 medicine rebuilding, and preserved badge stacking in separate fixtures | Both actors, stages, repeated/unrelated stat changes, link state, and explicit preserved/corrected expectations |
| OHKO and X Accuracy | Current Speed below/equal/above target, accuracy/evasion, X Accuracy on/off, original target checks | Speed eligibility and accuracy result tested separately; slower actor still fails with X Accuracy |
| Items and learning | PP Up bits, medicine stat rebuild, healing boundaries, multi-level prompts | Full affected data and item consumption; neighboring vanilla cases |
| Bounds/storage | Bag/PC capacity, duplicate stacks, party/boxes, sprite buffers, save/load and fault cases as supported | Memory guards and checksum/state records |
| Variants | Red/Blue original differences; Green/Blue equivalence; stale-object build checks | Decoded table comparison and shared fixtures |
| Presentation | Title, dialogue, HUD, palettes, audio and transition fixes | Captures in the relevant hardware mode; timing checks when needed |
| Adventure | Start, starters, gym/progression gates, Tower/Silph, Safari, League, postgame, normal save/load | Saved route/checkpoint evidence and smoke-test record |
| Link | Both host roles; all supported variant pairs; RNG rejection loops, status, switching, fainting, copied moves, trade | Endpoint states agree at defined turn boundaries |

CI tests the roll at each threshold and the one just below it when the threshold is positive. It does this for both actors at every Speed, including byte values outside the original species data. The earlier research checked the calculation and the final comparison separately in temporary builds. All 8,192 observed thresholds matched the expected values. The comparison then passed all 262,144 cases across the tested builds, covering every threshold and every random byte. [Current cartridge tests](../../tests/critical_hits.py) · [Compiled research results](../research/critical-hit-analysis.md#compiled-threshold-check)

Important critical-hit examples include Speed 55 and saturation boundaries. Test the actual high-critical move IDs and zero-power/set-damage paths as well as a generic high-critical flag. Dire Hit and Focus Energy must reach the same state behavior. The unpumped matrix must be bit-for-bit equivalent even after the corrected path is added.

Display tests must distinguish type neutrality from low final damage. Applying integer damage factors sequentially can retain original rounding. Correct the reported relationship without silently changing that arithmetic.

For a catalog report about expanded or malformed data, record whether its trigger exists in the vanilla reference. RGB-028 uses synthetic zero-coordinate items because the pinned coordinate table contains none. A synthetic fixture can prove an interface limit without proving that normal vanilla play reaches it.

## Preset checks

For a downstream pair, build both from the same source revision. Apply each patch to its declared base and verify the hash. Run one shared map, script, trainer and reward in both. Assert a deliberately different roster or rule and the shared single Special stat. Cross-check that switching editions cannot reuse stale objects or silently reinterpret a save. [Paired edition acceptance](../research/emerald-rogue-builds.md)

For a Minimal shortcut, compare two routes to the same action using the same party, badges, resource counts and gameplay rolls. Record state at the next meaningful choice, including turn cost, overworld position, event flags and the opponent’s next legal action. Include a refusal and cancellation. A different input sequence can be correct. A different Counter hit or newly catchable Pokémon needs its own gameplay decision. [Measured Counter example](../research/minimal-action-review.md)

Add stock and one-change fixtures for Charizard learning Fly, the Ghost/Psychic matchup and the Gen 2 move retypings. Include a 151-species build with one optional matchup and a wide-roster build with classic types, trainer AI and one Special stat. Stock comparison of 151 machine sets and move/evolution records can be repeated with [the Yellow data checker](../tools/compare_yellow_data.py).

Use the [new stock baselines](../research/foundation-checks.json) with their [fixture definitions](../research/foundation-audit.md) when building the corresponding fixes. For Minimal compare stock outcomes. For Core assert the selected correction plus each listed unaffected control. Seed the same game rolls, record both link peers where applicable, and check that each Green result agrees with Blue.

For Minimal, compare equivalent player actions and their gameplay results against the matching stock color, supplying the same random values at the gameplay rolls. Check the generator and roll sites separately. Different message lengths can shift timer samples in real play. Include a neutral dual-type hit, an unscoped Tower ghost after STATS, Focus Energy, and Blaine at full HP. Compare HP, move and item use, actions available, and encounter state. Record the expected picture, sound, or text separately.

For Core Blaine tests, force a successful item roll at full HP. Stock spends an item use and a turn. Core should preserve the item count and proceed with the trainer's normal action. Also test a failed roll, exhausted uses, one HP missing, and enough missing HP for the full heal. Verify the original roll still occurs where eligible and that neighboring trainers follow their original paths. For Extended AI, exercise its intended move and item choices in real turns and test the Core behavior when that feature is disabled.

## Differential tests

Feed equivalent fixtures to vanilla and PokéRGB. Compare damage, HP/status, stat modifiers, PP, turn choices, RNG calls, and state flags. Whitelist a deviation by stable RGB ID and exact observable; do not bless an entire routine or battle as “expected different.”

Once a corrected result changes state, later whole-battle trajectories may diverge legitimately. Reset at a well-defined fixture boundary or compare the shared subroutine contract. Arbitrary full-memory diffs also include scratch bytes and layout differences; define meaningful observations instead.

## Adventure checkpoints

Start with a small set of reproducible checkpoints and input scripts. Record how to recreate each checkpoint from its source revision. Use them to check:

- New game, starter choice, rival battle, capture, move learning, and evolution.
- Pokémon Centers, battle/field items, PC deposits/withdrawals, and box changes.
- Gym gates, S.S. Anne/Cut, Pokémon Tower/Silph Scope, and Silph Co.
- Safari Zone, fossil restoration, Cinnabar, and Victory Road.
- League, credits, postgame, and saving/reopening at several stages.

For an event-state repair, test the exact failing sequence and a normal route through the same event. A checkpoint suite is useful before a fully automated playthrough exists. Run the full adventure smoke suite on the release candidate. Record which paths were automated and which were played manually.

## Link and save testing

Link tests require two simulated or real endpoints. A single client reporting the right damage does not prove synchronization. Compare shared logical state after each turn and test both host roles. Initially test matching PokéRGB rules releases; test vanilla interoperability separately before claiming it. Corrected Focus Energy makes generic vanilla battle compatibility unsafe.

Save tests verify data after reopening the game, changing boxes and transferring Pokémon. Run fault injection before calling a save scheme power-loss safe. A check in a save routine is not proof that partially written data can be recovered.

**v0.2.0 to v0.3.0.** For each color and preset, a save made in the public v0.2.0 build loaded in the matching v0.3.0 build. The player ID, party, Bag and stored Pokémon survived a Bag edit, save and reload. Imported Core saves started with EXP. ALL on and battle pace Normal. The new Fuchsia interior exists only in v0.3.0 Core. Continue a save made inside that house in a Core build that includes it. These checks cover upgrades within the same color and preset. [Save import checks](../../tests/reference_save_import.py) · [Fuchsia visit](../../tests/core_services.py)

Use these criteria for each compatibility claim. The next table records the configurations covered by the reference tests.

| Interaction | Scope | Evidence needed |
|---|---|---|
| Single-player and save/load within one release | Required for the advertised paths in the public Core release | Adventure checkpoints and reopened save data |
| Trade between matching PokéRGB builds | Stable-core target | Both host roles, supported variant pairs, party/box data, cancellation and recovery |
| Battle between matching PokéRGB rules releases | Stable-core target | Two-endpoint turn/state/RNG agreement across the supported variant pairs |
| Import of a vanilla save | Evaluate separately | Exact supported base/version, layout checks, and round trips; document unsupported cases |
| Saves across PokéRGB releases | State a policy per release | A tested conversion, verified unchanged format, or a clear fresh-start requirement |
| Trade with original cartridges | Research target | Specific game/revision pairs and resulting Pokémon/storage data |
| Battle with vanilla games or mismatched feature profiles | No general guarantee | Separate full synchronization evidence; matching packet layouts are insufficient |
| Gen 2 Time Capsule and Stadium Transfer Pak | Unassessed interoperability | A dedicated design and tests before any support claim; no early-release gate |

Publish the tested subset, exact rules/save versions, and known incompatibilities. Being in this matrix is not a commitment to support every historical device or game.

### Verified reference configurations

These checks use SameBoy 1.0.5. The v0.3.0 release checks covered Red, Blue and Green in both Core and Minimal. Each test identifies the cartridge mode and operation it covers.

| Configuration | Checks |
| --- | --- |
| Game Boy mode | Adventure checkpoints, Move INFO, box operations, legacy save imports and re-saves. [Adventure checks](../../tests/adventure_checkpoints.py) · [Reference imports](../../tests/reference_save_import.py) |
| Super Game Boy mode | The first title Pokémon, English title tiles, the Green border and battle slide timing on all three colors. [Title checks](../../tests/title_smoke.py) · [Slide checks](../../tests/battle_slide_timing.py) |
| Game Boy Color compatibility mode | New Game, Bag TM INFO, and a save followed by CONTINUE on a fresh CGB-E instance. [Color compatibility checks](../../tests/cgb_compatibility.py) |
| Cable trade and battle | All nine ordered color pairings within each preset completed a Trade Center session and a Colosseum battle, for 36 sessions. Both endpoints were checked for the expected party record, battle state or save. The sessions start from seeded parties. [Cable checks](../../tests/link_cable_smoke.py) |
| Interrupted save | Detection before CONTINUE after incomplete main, box, link or Hall of Fame writes. Valid older records still load. Restore a backup when the game reports an interruption. [Save checks](../../tests/interrupted_save_smoke.py) |

The release records state which of these checks apply to the released source and package hashes. Use the matrix above to decide when another game version, emulator or physical device needs its own check.

## CI and release jobs

GitHub Actions builds both presets and all three colors on Linux and macOS. Linux runs the game tests in eight groups per preset. macOS checks color data and the spec. A normal CI run checks one ordered Core cable pairing. Use `--all-link-pairs` in release testing for all nine. Run pristine-ROM and cross-version save tests with the matching reference inputs. The table also lists checks to add when optional systems become available. [Workflow](../../.github/workflows/main.yml)

| Job | Frequency | Purpose |
|---|---|---|
| Documentation/data validation | Every change | Links, record IDs, invalid species/move/type references, table terminators and build selections |
| Linux clean builds | Every code change | Red/Blue/Green, isolated objects, warnings, link maps and reproducibility |
| Default core and customization example | Optional-system changes and release | Build without optional gameplay systems; check the protected contract and a documented small data edit |
| Focused regressions plus protected mechanics | Every relevant code change | Defect-specific cases and shared behavior guards |
| macOS build | Release and build/tooling changes; every change if affordable | Detect supported-platform drift |
| Two-endpoint link suite | Battle/link changes and release | Detect shared-state and RNG mismatch |
| Extended adventure/hardware-mode suite | Release; scheduled only once an implementation schedule is chosen | Broader integration and presentation coverage |

Pin tool/emulator versions and CI actions by revision. Preserve test binaries privately or as permitted by the release policy, symbols, map summaries, inputs and failure traces. Do not upload consumer ROMs as routine build artifacts without an explicit distribution decision.

Adding an optional system must keep the default builds working. Test its disabled state against the accepted core behavior. Test each advertised enabled configuration separately, with its declared dependencies. Developer tools and presentation features must not need expanded species or modern battle rules unless a specific feature depends on them.

Test the stock active-box gate in Minimal and Core. Test automatic placement separately with direct MOVE POKÉMON both on and off. Include eligible catches and gifts, the first box switch, the last unsaved arrival, interrupted saves, and link trades. [Storage cases](../research/box-overflow-contract.md) · [Distinct save paths](../research/storage-policy-and-code.md)

For an alternative trainer AI or random-number generator, test the original path and the alternative separately. Compare trainer decisions and generator state/output under controlled initial state and inputs. Exercise the actual routines: supplied random bytes test battle calculations, but do not prove that the generator itself is unchanged. When an unrelated feature is advertised as independent, include a build using that feature with the baseline AI and generator.

Use warnings and assertions meaningfully. Do not remove a truncation warning to hide an 8-bit overflow. Add a capacity report and fail when a required section overflows; establish acceptable headroom from actual use.

Run the [test command](../../README.md#tests) on a built preset to use the same checks as GitHub Actions. The individual scripts are also callable for specific tests. The full color matrix and physical hardware are separate release checks.

## Reproducibility and release claims

Build the same release twice from clean inputs and compare its own hashes. Record source, data/assets, tools, target configuration and test-suite revisions. For patch releases, apply each patch to the exact documented input ROM hash and verify the result hash.

A release report separates assembled, unit-tested, integration-tested, emulator-tested and hardware-tested results. Hardware tests should cover boot, battle, audio, save/reload and link where claimed. An accurate emulator plus a second independent implementation is useful interim evidence, but does not equal testing on every device.

Prioritize original Game Boy-compatible behavior, then verify the advertised CGB/SGB modes. Game Boy Pocket, GBA in GB mode, popular handheld emulators, and Analogue Pocket are additional compatibility checks when available. Record the actual model, emulator version, cartridge/mapper, and tested operations. Access to every device is not needed for a developer preview.

No tests should be added merely to mirror implementation or inflate counts. Boundary cases, independent expected results, and failures observable by developers or players are the reasons for a test.

## Contextual HM regression coverage

PN-004's shortcuts need executable comparisons with menu use. Cover Cut trees, Surf entry, and Strength activation with and without the required move and badge. Check cancellation, correct party-user selection, invalid targets, repeated input, and competing NPC/sign/hidden-event interactions. Exercise the real map and collision guards, including Cycling Road, Seafoam currents, gym trees, and boulder puzzles. Verify manual field use and normal reset/save behavior. The game tests cover [route trees](../../tests/route_cut_tree.py) and [Surf and Strength](../../tests/field_shortcuts.py). See [PN-004](13-playthrough-intake.md#pn-004) for the full contract.

Keep inventory-management coverage separate: the default bag still has 20 slots. Check a full bag receiving a new item, an addition to an existing quantity, bag/PC transfers, and save/reload. Accepted item safeguards must work within that limit rather than silently adding slots or a key-item pocket.

## Badge mapping regression coverage

RGB-010a changes the calculation to match the original descriptions. For an eligible single-player stat `s`, one bonus remains `min(999, s + floor(s / 8))`. Apply it to Speed for Thunder and Defense for Soul. Keep Boulder→Attack and Volcano→Special.

Execute the compiled routine over all 256 obtained-badge masks and supported stat values 1–999. Include distinct values in each stat so an incorrect field cannot pass by coincidence. Check the 7/8/9 rounding boundary and the 887/888/889 cap boundary. No-badge and unrelated-badge fixtures must preserve Speed/Defense.

Integration cases must award Thunder and Soul separately, in both orders, and together. Check the resulting turn order and physical damage. Original critical-hit threshold rules remain unchanged. Confirm all gym and badge-house descriptions agree with the corrected mapping.

Keep stacking tests separate from the mapping correction. Repeated boosts and unrelated stat changes must retain the original stacking behavior with the corrected assignment. Test burn/paralysis and the separately scoped status-medicine path. Link-battle fixtures must receive no badge bonus for any mask. Verify the mapping repair does not consume random bytes or change other badge, field-move, or obedience checks.

PureRGB's mapping is useful donor evidence, but its helper also changes stacking. Do not import that complete stat system as this repair. Use the [battle tests](../../tests/battle_fixes.py) and [status-medicine tests](../../tests/status_medicine.py) to check the implemented paths.

## STATS and menu regression coverage

PN-003 and PN-006 must exercise the real party and PC entry paths. Cover one/full party, one/full box, first/middle/last and scrolled entries, and unavailable/empty contexts. Up/down changes only the viewed Pokémon and retains page; left/right changes only page. B from either page restores the list, highlighting the last Pokémon viewed. If the Pokémon did not change, retain the exact original row and scroll offset. Selected-Pokémon action B/CANCEL also returns to the PC list. Confirm that none of these paths triggers withdrawal, deposit, release, or a battle switch.

Use a temporary third page to verify that the same navigation works without adding DV or stat EXP information to Core. Exercise battle and trade callers separately. A forced replacement must remain mandatory; viewing STATS must neither consume a battle turn nor cross to an unintended data context. Verify name, owner, moves/PP, HP/status, party/box counts, and save data remain intact after browsing.

PN-007 must show the selected nickname/species and default to No. B/No must leave records and counts intact. Explicit Yes removes that Pokémon exactly once. Check duplicate nicknames, scrolled lists, a recently viewed different Pokémon, held/repeated input at prompt entry, and text layout. Other Yes/No prompt defaults stay unchanged.

Keep medicine returning to the bag after each outside-battle use, with one item consumed per successful use and original battle action costs. The overworld party-CANCEL case in the [audit](../research/menu-navigation.md) is accepted under PN-009 and has focused requirements below. Shop refusal/failure returns are now accepted under PN-008 and have separate regression requirements below. Existing quantity-cancel and PC item-transfer return paths remain protection cases.

When the Repel extension is implemented, test disabled Core behavior, same-kind ownership/consumption, cancellation, all three durations, expiry timing, leading-Pokémon level checks, map changes, and save/reload. It is not a Core release gate. Track these cases with the optional feature.

## Shop return regression coverage

PN-008 must restore SELL after a protected-item refusal and BUY after insufficient money or inventory capacity. Check selection and scroll position before and after each message. Cover key items, HMs, protected EXP. ALL, insufficient money, full-bag new stacks, quantity limits, and additions to existing stacks under the original rules. Refused transactions must leave inventory, money, and completed-transaction state unchanged.

Repeated failures must not trigger an automatic retry or stale transaction. A subsequent valid transaction must use the newly selected item and quantity exactly once. Preserve B from the item list, quantity cancellation, final confirmation refusal, successful buy/sell loops, and empty SELL-list handling. The game tests cover [refused sales](../../tests/item_safety.py) and [purchases](../../tests/shop_carry_count.py).

## Party action-menu cancellation coverage

PN-009 must return both B and selecting CANCEL to the overworld party list, with the same Pokémon highlighted. Check parties of one, two, and six Pokémon; first, middle, and last selections; and action menus with and without learned field moves. Repeat cancellation and then open another Pokémon's action menu. Cancellation must not switch Pokémon, use a field move, or change party records.

B from the party list must still return to Start. Check STATS, SWITCH, and available field moves after cancellation. Preserve battle selection, forced replacement, item targeting, trade, and PC return rules. The [menu return tests](../../tests/menu_returns.py) exercise B and CANCEL.

## Feedback and reward checks

The [small-fix audit](../research/usability-audit.md) records specific required checks for each new recommendation. In particular, pair visible reward/feedback checks with data checks: encoded coins versus credited coins, selected vending price versus money deducted, gift receipt versus its completion flag, and Flute wake-up feedback versus actual status. Rendered text, cry playback, and original Game Boy/Super Game Boy spin checks require a built game. The source review does not satisfy those release checks.

## Accepted reward, feedback, elevator, and quantity repairs

Run the focused cases in [PN-010–PN-015](13-playthrough-intake.md#pn-010). Verify selected vending price against delivery and deduction; all rooftop drink/TM exchanges against payment, capacity, and completion flags; Flute feedback against actual wake-ups; and shared trade text against both users. A full-bag rooftop fixture needs drink counts one and two: the first can free a slot, while the second exposes the loss. Check existing target stacks and inventory split boundaries separately.

For elevators, exercise every supported entrance/destination and ensure current-floor input produces no travel presentation or warp-state change. For quantity controls, verify clamped tens, preserved unit wrapping, live prices, cancellation, and each shared caller. Source review does not replace those game tests.

Exercise move INFO on Minimal and Core through the actual machine, STATS, FIGHT and learn/forget screens. Check cancellation, unchanged state, matched-roll turns and two-peer link input. Test the optional live type overlay separately. [Acceptance cases](15-battle-information.md#acceptance-criteria)

## Game Corner and Day Care preservation

- Start with a Coin Case and zero coins. Buy all the coins for Porygon at the clerk, then claim it through the prize menu. Red needs 200 purchases for 9,999 coins. Blue and cosmetic Green need 130 for 6,500. Also redeem TM50 Substitute for 7,700 coins in Blue and Green. It is their most expensive prize. Check the money, final coin balance, species or item, level where applicable, and destination. Try again one coin short, cancel at the quoted price, and attempt delivery with both the party and selected box full. The observed Red and Blue results give the expected values for each case. [Prize routes](../research/game-corner-redemption.md)
- At the Route 5 Day Care, compare the ordinary deposit and pickup dialogue with the original. Test a Pokémon that gains a move while all four slots are occupied, and again with an empty slot. Check the original fee, surviving moves and their PP. Also exercise the existing last-member and HM refusals. At the PC and Day Care, a two-member party with a fainted reserve keeps its original deposit choice. [Day Care evidence](../research/day-care-history.md)

## Item-list position regression coverage

Use [PN-019](13-playthrough-intake.md#pn-019) to verify selected entry, visible row, and viewport separately from the return destination. Exercise item-PC deposit/withdraw/toss, bag use/toss, and shop buy/sell after partial/full-stack changes, cancellation, refusal, and success. Test consecutive operations near the bottom, duplicate stacks, first/last/empty lists, and shrinking the visible range. No stale index or held button may trigger an unintended action. Verify exact inventory/money changes alongside position. Protect shared removal callers, medicine's return-to-bag flow, and successful Pokémon-transfer destinations. No cursor persistence across separate sessions or new saved field is required.

## Optional item capacity regression coverage

Before advertising the 64-slot bag profile, run [PN-020](13-playthrough-intake.md#pn-020) at the 20/21 and 63/64/65 entry boundaries. Test stack space separately from free entries, all insertion/removal callers, the rooftop exchange, PN-019 selection retention, memory guards, and neighboring saved fields. Build Core with its unchanged layout and the bag-64/PC-50 profile; test PC alternatives and combined profiles only when advertised. Save/load and supported import/conversion need explicit evidence. These are future game checks, not results of the source/allocation calculation.

The proposed 64-slot bag needs all 134 bytes of the original reserve. The current games already use two of those bytes for the registered SELECT item and its tag. If the bag takes that range, give the registration its own storage and carry it over when importing a save. Test imports with the Bicycle registered, a rod registered and no registration. Save, reload and use SELECT to verify each result. [Current memory layout](../../ram/wram.asm) · [Allocation study](../research/bag-memory.md)

Preserve the original 42-byte bag footprint and `wGameProgressFlagsEnd`. Compare other field addresses and save offsets with the reference layout. Check that each byte has one owner in every supported feature combination. Audit reads, clears and copies of the old reserve, plus initialization and saving. [Repeatable allocation check](../research/bag-memory.md#repeat-the-allocation-check)

For the enabled bag, start a new game and verify the empty count, end marker, and format marker after the game-progress clear. Fill all 64 entries, save, reload, and verify the final entry and terminator without changing neighboring flags. The 65th new stack must be refused. Check the same initialization and save paths with each advertised feature combination. [E109](../research/evidence.md#e109) identifies the initialization order to repair; these game checks remain pending.

## Move-swap cursor and box insertion coverage

For [PN-021](13-playthrough-intake.md#pn-021), test marking and completing a three/four swap with the remembered move index at one and two. Check same-slot and repeated swaps, missing slots, A/B exits, battle and party move/PP bytes, PP Up bits, Disable index/duration, transformed/copied moves, and link restrictions. Cursor retention must add no turn, PP cost, random draw, or unintended battle-history update.

For [PN-022](13-playthrough-intake.md#pn-022), verify stable existing box positions after captures, gifts, and deposits. Use distinct complete records, duplicate names/species, nickname Yes/No, and empty/one/19/20-entry states. Check save/reload, box changes, removal compaction, full-box refusal, and supported storage-feature combinations. A correct species list alone does not establish aligned nicknames, OTs, or records.

For [PN-023](13-playthrough-intake.md#pn-023), test sight-triggered battles for all three Mansion Burglars, at the implemented range of one square. Cover facing/alignment, visibility, wandering movement boundaries, ordinary talk, defeated state, save/reload, and unchanged parties/rewards. Check narrow paths, doors, and the 3F table area so engagement and post-battle position cannot trap the player. Preserve the Scientists and unrelated zero-range trainers. [Mansion tests](../../tests/mansion_sight.py)

## Star-grass encounter regression

For [PN-024](13-playthrough-intake.md#pn-024), verify all 114 missed squares under controlled random inputs, ordinary grass and safe paths, unchanged encounter data, slot selection, and Repel. Cover direction changes, warps, scripts, and post-battle return. Check water, shores, and other Forest maps including the Safari Zone; any wider Yellow-style change needs its own scope. Run for Red, Blue, and cosmetic Green. Core’s [Forest checks](../../tests/forest_encounters.py) exercise the repaired encounter rule and nearby controls. Minimal keeps the original rule.

## Acid Armor picture checks

Use the [stock Acid Armor checks](../research/acid-armor.md#stock-rom-checks) to reproduce the bug. With animations on, a successful use can hide the ordinary picture, a Minimize image, or a Substitute across turns. It can stay blank through a hit or a Haze that removes the Defense boost. View STATS from the battle party menu to exercise the enemy picture reload. Test both battle sides.

For the D41 correction, check the original melt and sound. Verify that the sprite visible when the melt began is back by animation end on each supported build. Check the normal and transformed Pokémon, Minimize sprite, and Substitute doll. Verify repeated use, use at +6 Defense, animations off, later damage, switching, fainting, and both link roles. Keep ordinary move state, Defense, PP, and RNG calls identical with controlled inputs. Check Fly and Dig as controls. [Core scope](../research/acid-armor.md#core-correction) · [Stock results](../research/acid-armor-baseline.json)
