# Bug triage and repair inventory

The inventory links to source, reports, and stock-ROM checks where available. Each record gives the scope of its evidence and the status of the proposed game change.

**P0** means a reproducible crash, corrupted state, or progression failure on a supported path. **P1** means a wrong calculation or failed existing function. **P2** means misleading output or a visual/audio fault. Severity does not determine inclusion: a protected mechanic remains protected.

## Battle calculation and trainer repairs

| ID | Exact issue and cause | Evidence / disposition | Required regression |
|---|---|---|---|
| RGB-001 | Focus Energy reduces the threshold; Dire Hit sets the same state bit. | Accepted with the Q01 capped multiplier. See the compiled threshold results in the [sweep](../research/final-scope-audit.md). [E04](../research/evidence.md#e04) | All base-Speed bytes, both move classes, every random byte; both actors; Dire Hit parity; unaffected rates identical. |
| RGB-009 | Damage applies both relevant type factors, but the text/sound state retains one matching factor. | Source-confirmed; presentation correction accepted. [E14](../research/evidence.md#e14) | Grass into Water/Poison and Fighting into Normal/Flying report neutral; ¼×, ½×, 2×, 4×, immunity; damage and RNG unchanged. |
| RGB-010a | Surge and Koga text describes the opposite stats from the implemented Thunder/Soul bonuses; the badge house repeats it. | Source-confirmed mismatch; code correction accepted: Thunder→Speed, Soul→Defense. Original intent is inferred, not proven; see the [badge review](../research/badge-intent.md). [E12](../research/evidence.md#e12), [E42](../research/evidence.md#e42) | Thunder alone boosts Speed; Soul alone boosts Defense; both and either acquisition order work. Preserve original text, bonus amount/rounding/cap, Attack/Special, link exclusion, and stacking; see [regressions](07-testing-ci.md#badge-mapping-regression-coverage). |
| CAT-018 | Blaine can use a Super Potion at full HP. | Reproduced in stock Red and Blue. Accepted in Core under D44. [E121](../research/evidence.md#e121) | Exercise the normal trainer turn with the chance roll on both sides of the cutoff, full HP, 1 HP missing, and zero item uses. Check HP, remaining uses, and the next action. |

These records are examples from the complete Core inventory. The [roadmap](09-roadmap.md#what-counts-toward-core) defines the public release gate.

## Accepted spelling correction

| ID | Exact issue | Evidence / disposition | Required display check |
|---|---|---|---|
| RGB-010c | Oak's 60–69-owned-species Pokédex rating misspells getting as geting. | P2; source-confirmed; spelling correction accepted for Core. [E82](../research/evidence.md#e82), [PN-005](13-playthrough-intake.md#pn-005) | Correct the word and reflow as needed. Check the PC, Oak's Lab, and Hall of Fame display paths; preserve rating thresholds, other text, and game behavior. |

## Accepted item-safety safeguard

| ID | Requirement | Evidence / delivery | Required regression |
|---|---|---|---|
| RGB-029 | Prevent tossing EXP. ALL from the bag or player PC and selling it in shops; reuse the important-item refusal messages. Retain storage, acquisition, and experience behavior. | Source-confirmed loss path; default safeguard accepted; not implemented. [E68](../research/evidence.md#e68), [PN-001](13-playthrough-intake.md#pn-001) | Bag/PC toss refusal and shop sale refusal, item and money unchanged on refusal, PC deposit/withdraw and save round trip, ordinary item sales/discard still work, existing key-item behavior retained. |

This is a loss-prevention safeguard, not a progression softlock or the separate experience-allocation report RGB-017. Include the inventory and sale checks in Core acceptance.

## Source-confirmed repair candidates

The [Core scope review](../research/core-scope-review.md#core-battle-and-progression-repairs) identifies the accepted Core repairs in this inventory, including RGB-002 through RGB-006, RGB-011/012, and RGB-014. Other candidates retain their individual review status. Every implementation needs a failing stock case and a passing patched case.

| ID | Problem and narrow proposed repair | Priority | Evidence | Boundary cases and protected behavior |
|---|---|---|---|---|
| RGB-002 | A battle assigns the final gained level and checks that level's learnset once. Check each gained level for moves. | P1 | [E26](../research/evidence.md#e26) | Gain 0/1/many levels; several move prompts; duplicates; declined moves; four slots; evolution ordering; Rare Candy and daycare separately. |
| RGB-003 | Healing ignores the result of the high-byte HP comparison. Compare the complete HP values. | P1 | [E15](../research/evidence.md#e15) | Missing HP 254/255/256 and 510/511/512; full HP; small HP; Rest with existing statuses; player/enemy. |
| RGB-004 | Max Ether/Max Elixir compare PP with embedded PP Up bits. Mask current PP when testing for no effect. | P1 | [E25](../research/evidence.md#e25) | PP Ups 0–3; full/partial/zero PP; empty move slots; item consumption; metadata retained; ordinary Ether/Elixir. |
| RGB-005 | Substitute checks subtraction carry, allowing exactly zero remaining HP. Reject zero as well as underflow. | P0/P1 | [E16](../research/evidence.md#e16) | HP below/equal/above floor(max HP/4); max HP rounding; already active; both actors; retain existing cost and substitute behavior. |
| RGB-006 | Fly/Dig interruption can clear charging without clearing invulnerability. Clear the coupled state on those interruption paths. | P1 | [E07](../research/evidence.md#e07) | Full paralysis, confusion self-hit, normal completion, switching, fainting; both actors; accuracy and trapping unchanged. |
| RGB-011 | On enemy faint, Bide clears only the player's high damage byte; the opposite endpoint clears both. Clear both bytes consistently. | P0 | [E27](../research/evidence.md#e27) | Nonzero low byte; both faint directions and hosts; same builds over link; no unrelated Counter rewrite. |
| RGB-012 | Psywave's attacker loop rejects zero; the target loop accepts it. Use one specified range and matching RNG consumption. | P0 | [E28](../research/evidence.md#e28) | Both endpoints/hosts; level 1 and legal high levels; zero rerolls; fixed-damage immunity bypass retained; range choice recorded. |
| RGB-013 | A status medicine copies unmodified party stats into battle stats without reapplying the stage calculation. Repair the stat rebuild. | P1 | [E29](../research/evidence.md#e29) | Burn/paralysis, stage −6…+6, no status, Full Heal/Full Restore, badge interactions. Do not decide badge stacking through this repair. |
| RGB-014 | Capture logic assumes a transformed wild Pokémon is Ditto. Retain the original captured species. | P1 | [E47](../research/evidence.md#e47) | Actual Ditto, another species using Transform, Metronome path, repeated transformations, boxed capture. |
| RGB-015 | `GetName` selects machine names by numeric ID without first checking which name list is requested. Restrict that dispatch. | P1; expansion prerequisite | [E31](../research/evidence.md#e31) | High IDs from each name list; repeated TM/HM menu use; fix the dependent menu state too. [E48](../research/evidence.md#e48) |
| RGB-026 | Retain the stock AI neutral value. The no-match producer and sole scoring caller both use hexadecimal 10. | Preserve | [E126](../research/evidence.md#e126) | A producer-only edit would classify neutral moves as resisted. Verify both ends before changing any AI scoring scale. |
| RGB-027 | A stat-up path rebuilds the user's chosen stat without its burn/paralysis penalty, then reapplies penalties to the opposite actor. Stat-down paths can also reapply a penalty to an already penalized stat. | P1; deferred research, correction excluded from the current core | [E50](../research/evidence.md#e50) | Both actors and link roles; burn/paralysis; Attack/Speed and unrelated stat changes; stages −6…+6; repeated changes; rounding/minimum stats; critical damage; badges tested separately. |
| RGB-028 | Shared Itemfinder boundary repair for valid zero coordinates in author data. The stock 54 placements give identical results. | Shared engine | [E51](../research/evidence.md#e51) | Compare both axes, edges, radius limits and collection state. [CAT-038](../research/catalog-decisions.md#cat-038) |

Psywave's recommended range is 1 through `floor(3 × level / 2) − 1` for legal levels where that range exists. This follows the original attacker path. Core assigns exactly 1 damage at level 1 to avoid an empty-range loop. That safeguard belongs in the repair record, not an undocumented formula change. Glitch-level behavior is a separate input-bounds policy.

RGB-027 is separate from status-medicine rebuilding (RGB-013) and the settled badge-stacking baseline. The penalty paths are not excluded from link battles by the badge routine's guard. Source confirms the calculation paths; the default core retains them while the proposed repair's fit remains unclear. A later narrow repair or developer extension needs its own evidence and tests. Do not import an entire replacement stat system or delay the initial release for this record.

For RGB-028, all 54 entries in the pinned hidden-item coordinate table have positive X and Y values. The zero-coordinate defect is confirmed conditionally from source; an ordinary vanilla-play failure was not established. Keep it visible as a data-expansion boundary. Do not label the archived report a reproduced vanilla failure or a verified donor patch.

## Accepted battle display correction

| ID | Defect and accepted Core correction | Evidence | Required regression |
|---|---|---|---|
| [PN-025](13-playthrough-intake.md#pn-025) | P2. Acid Armor leaves the active picture erased across turns. Keep the sink and redraw the same picture at the end. | Reproduced in stock English ROMs. A graphics reload can restore the picture without affecting the Defense boost. Exact historical intent remains uncertain. [E116](../research/evidence.md#e116), [E119](../research/evidence.md#e119) | Check both sides, all current picture forms, animations off, use at +6, and the unchanged move effect. [Test plan](07-testing-ci.md#acid-armor-picture-checks) |

### Additional verified cases

The [scope review](../research/core-scope-review.md) specifies D46 (Transform), CAT-020 (ghost Pokédex entry), CAT-029 (second Gym lock), and the reproduced Struggle case RGB-018. These belong in Core.

## Core targets and conditional cases

| ID | Report / current disposition | Next concrete step |
|---|---|---|
| RGB-007 | Item-stack splitting can walk past the inventory terminator. The source path and catalog patch are identified; memory writes were not traced here. P0 safety boundary for both presets. [E30](../research/evidence.md#e30) | Bag and PC fixtures with stack 99, room/no room, repeated stacks, and memory guards; prove the out-of-bounds write before accepting a patch. |
| RGB-008a | Oak-follow movement can leave the player in a wall. Catalog report. | Reproduce the exact map position and input sequence; prove the script/collision fault. |
| RGB-008b | Core. The Mt. Moon fossil area can set a shared no-battles flag before leaving the floor. | Compare a direct exit with walking out of the marked area and protect other suppression owners. |
| RGB-008c | Both presets clear inherited Cycling Road restrictions on New Game. | Check starting controls and older-save integrity. [CAT-061](../research/catalog-decisions.md#cat-061) |
| RGB-008d | Core. Keep actual cut-tree collision and its visible state in agreement at the map connection. | Record the Route 14 connection and distinguish legitimate regrowth after a reload. |
| RGB-016 | Core. A cured target must regain a legal turn after an interrupted action. | Test Haze after freeze during recharge or a multi-turn move. Preserve the ordinary wake turn and target-only major status cure. |
| RGB-017 | Core. EXP. ALL reuses the first division for the second award. Stock under-awards both XP and stat experience. [Measured awards](../research/foundation-audit.md#exp-all-gives-too-little-to-a-party-with-multiple-participants) | Calculate each share independently. Cover rounding, 1–6 recipients, fainting, trade and trainer bonuses. |
| RGB-018 | Planned Core repair. Disable skips its own slot but counts PP Up bits as available PP in another empty slot, preventing forced Struggle. Reproduced in Red and Blue. [E124](../research/evidence.md#e124) | Test with and without Disable, all slots, all PP Up counts, zero PP and one usable PP. Keep the existing enemy PP rules. |
| RGB-019 | Core. Prevent last-PP wrap on forced reuse. Require matching peers after a copied trapping move and switch. | Compare both seats, consumed PP, turn choice and next random draw. Keep original trapping and switching. |
| RGB-020 | Core. Prevent a zero defensive divisor and a wrapped effective defense under Reflect or Light Screen. | Test both arithmetic boundaries independently. [Bounds and tests](../research/foundation-audit.md#damage-multi-turn-moves-and-link-play-beyond-the-catalog) |
| RGB-021 | Core. Charge the selected doll on the correct side for self-confusion and Jump Kick crash. | Use both actors with neither, either or both dolls active. Preserve ordinary recoil. |
| RGB-022 | Shared save safety. Bound writes on supported inputs. Preserve the documented limits for invalid species. | Protect Hall of Fame and box data. See [CAT-048](../research/catalog-decisions.md#cat-048). |
| RGB-023 | Shared save safety in both presets. Detect an incomplete save or recover a coherent one. | Test interruptions, backups, old imports and party/box consistency. [CAT-093](../research/catalog-decisions.md#cat-093) |
| RGB-024 | Minimal and Core presentation. Redraw affected trainer HP/status displays after the item resolves. | Capture the stale state, DMG and SGB colors, and the unchanged turn result. |
| RGB-025 | Rendering/audio problems include sprite tearing, lost tiles, incorrect cries and channel-state errors. Catalog reports. | Split by routine and hardware mode; reproduce and compare captures with measured timing. |
| RGB-010b | Other factually wrong dialogue or descriptions. Review queue. | Verify against the retained mechanics; edit each string under its own record and check layout. |

`RGB-008` and `RGB-010` were umbrella labels in the draft plan. Use the suffixed records for individual defects. RGB-010c records the accepted Oak spelling correction separately from the RGB-010b factual-text review queue. They are not promises that every event or every line of text has already been audited.

## Protected or excluded changes

| Topic | Disposition | Reason / required guard |
|---|---|---|
| 1/256 accuracy failure and 255/256 critical ceiling | Preserve | Explicit baseline. Test endpoint random byte and bypass moves separately. |
| Hyper Beam KO/recharge behavior | Preserve | Defining combat rule; no donor recharge patch. |
| Fixed-damage type-immunity bypass | Preserve | Source-confirmed original rule; no modern immunity import. |
| Original ordinary/high-critical calculation and damage treatment | Preserve | A Focus Energy correction cannot silently replace either. |
| Toxic plus Leech Seed interaction | Preserve | Explicit contract; do not include Shin's separation. |
| Badge stacking | Preserve in the default core | Settled baseline; an optional developer correction may come later. Ordinary badge bonuses remain protected. |
| Burn/paralysis stat recalculation | Deferred; retain current behavior | RGB-027's uncertain repair stays out of the current core. Future work needs its own evidence and fixtures; the medicine repair does not resolve it. |
| General Counter redesign | Investigate; no default overhaul | Fix a proven link/state defect independently of cartridge Counter quirks. |
| Substitute breaking cancels some move effects | Investigate; retain baseline initially | Changing it can affect Hyper Beam, recoil, and Explosion; it is not the zero-HP Substitute repair. |
| AI upgrades, unlimited-to-finite enemy PP, different Rage duration | Outside Core | Broad combat design changes need a separate proposal. |
| Ghost versus Psychic, move types, machine permission | D50 Core exceptions | Change one matchup, Gust’s type and Charizard’s HM02 permission. Other retypings and the rest of Yellow’s machine edits remain independent choices. |
| Emulator-only visual failures | Investigate emulator first | Hardware timing can be correct while an emulator is wrong. |

## Complete catalog intake

[bug-catalog.csv](../research/bug-catalog.csv) contains **all 94 topic entries** from the pinned archived pret catalog, with independent short labels, source locations, evidence status, initial disposition, priority, and links to curated records where available. This is complete coverage of that catalog snapshot, not a claim to know every Gen 1 bug.

Every archived topic now has a [decision, reason and test](../research/catalog-decisions.md). The evidence status in the CSV refers to the strength of the observed defect. A repair can have a clear place in the product before a stock symptom or its implementation has passed a release test. Cases beyond the archived list appear in the [pre-build investigation](../research/foundation-audit.md).

## Further source-reviewed candidates

The [final sweep](../research/final-scope-audit.md) updates shared-engine, menu, information and save-safety placements. For hidden coins, both builds report a dropped coin only after a real loss. Core’s separate 40-coin reward repair still applies.

D53 addresses a reproduced save-data loss during an abandoned first box change. Both presets should defer persistent writes until confirmation. The refused Surf dismount should return to the party list in Minimal and Core, subject to the unchanged-state tests. [Box picker](../research/box-picker-safety.md) · [Field move cases](../research/field-shortcut-contract.md)

Core should repair CAT-039’s blocked southward return and the Pokédex AREA list that records the same map repeatedly past its declared size. Minimal and Core should correct the Guard Spec. tip and the Safari East Area 1 sign. Review the Saffron Ghost hint against the active chart and localize the actual rules. Each scope has separate tests, and none expands the first-release list. [Yellow corrections](../research/yellow-rules-review.md) · [Hack comparison and AREA evidence](../research/developer-hack-comparison.md)

The [small-fix audit](../research/usability-audit.md) supplies precise scope and required checks for the following findings. The disposition column distinguishes accepted Core repairs from recommendations. None is implemented in this specification.

| Audit ID | Finding | Evidence | Disposition |
|---|---|---|---|
| UA-01 / CAT-057 | The encoded hidden 40-coin reward takes the 20-coin branch. | [E88](../research/evidence.md#e88) | Plan the narrow amount correction for Core. |
| UA-02 | Vending affordability is checked against ¥200 for every drink. | [E89](../research/evidence.md#e89) | Accepted PN-010 / RGB-031: check the selected price; preserve prices and capacity. |
| UA-03 | Oak commits his five-ball gift before delivery and ignores failure. | [E90](../research/evidence.md#e90) | Core requires successful delivery before the gift is marked received. Distinguish normal reachability from an injected full bag. |
| UA-04 / CAT-084 / RGB-010b | Trade follow-up says Raichu evolved. | [E91](../research/evidence.md#e91) | Accepted PN-012: truthful text, preserving trade and evolution data. |
| UA-05 / CAT-083 | Oak's throwing instructions overwrite a line. | [E92](../research/evidence.md#e92) | Recommend line-command repair; verify the displayed paragraph. |
| UA-06 / CAT-082 / RGB-025 | Introductory Nidorino uses Nidorina's cry. | [E93](../research/evidence.md#e93) | Recommend matching cry; check shared command users and listen to the build. |
| UA-07 | Flute can wake a wild opponent without its wake-up confirmation. | [E94](../research/evidence.md#e94) | Accepted PN-011 / RGB-032: accurate feedback; preserve effect and battle cost. |
| UA-08 / CAT-025 / RGB-024 | Trainer cure paths lack a status-area redraw. | [E95](../research/evidence.md#e95) | Source-supported; capture exact stale display and verify the correction. |
| UA-09 / CAT-037 | Escape/teleport spin reads from the wrong pointer. | [E96](../research/evidence.md#e96) | Source-confirmed pointer mismatch; original Game Boy/Super Game Boy display checks remain. |
| UA-16 / RGB-030 | Rooftop girl removes a drink before a failed TM delivery. | [E101](../research/evidence.md#e101) | Core defect repair PN-015; preserve payment on refusal and one-time reward semantics. |

UA-13/UA-14 are accepted interface changes under PN-013/PN-014. UA-10 is deferred outside the default; UA-11/UA-12 are shared display requirements under PN-016/017; the extra UA-15 move-forgetting prompt stays optional. Money-gate recovery and interrupted-save safety require further design and evidence. The release gate uses the accepted disposition of each case.

## Star-grass encounter recognition

CAT-028/[PN-024](13-playthrough-intake.md#pn-024) is source-confirmed. [E115](../research/evidence.md#e115) demonstrates a mismatch between the encounter corner and grass rendering, with Yellow recognizing the unchanged map correctly. D40 accepts the scoped Core repair in the [review](../research/forest-encounters.md). Delivery is not started; the exact change needs Forest, Safari Zone, shore, RNG, and Repel checks. Keep the separate CAT-027 shore case explicit.

## Donor survey dispositions

D43 accepts the four Core repairs below. The [Gen 1 bug-fix survey](../research/donor-bugfix-survey.md) gives donor comparisons, stock-ROM results, and patch acceptance checks. Public release gates follow the [roadmap](09-roadmap.md).

| Candidate | Accepted Core repair | Evidence |
|---|---|---|
| CAT-071 / P2 | Redraw enemy Substitute and Minimize on the enemy side when returning from battle STATS. | Stock Red and Blue reproduce the fault. Official Yellow corrects it. [E120](../research/evidence.md#e120) |
| CAT-021 / P2 | Keep an unidentified Pokémon Tower ghost's disguise when returning from STATS. | Reproduced in Red, Blue, and Yellow. [E120](../research/evidence.md#e120) |
| CAT-022 / P2 | Play the intended sound when replacing a move and resume the active music. | Source confirms the audio bank mismatch and Yellow's repair. Listen to the patch in battle and outside battle. [E122](../research/evidence.md#e122) |
| Empty SHIFT prompt / P2 | Ask to switch before the next opposing Pokémon only when a living reserve can enter. Keep SET and forced replacements unchanged. | Reproduced in stock Red and Blue. Also tested a living reserve at 1 HP. [E121](../research/evidence.md#e121) |

**CAT-018 ships in Core under D44.** The [battle records](#battle-calculation-and-trainer-repairs) give the repair and tests. Minimal retains the original trainer choice.
