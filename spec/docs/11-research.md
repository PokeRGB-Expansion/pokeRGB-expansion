# Research findings and technical corrections

The [v0.2.0 feature sweep](../research/v020-feature-sweep.md) compares candidate changes with the released games and records their player effects, preset decisions and reproduction results. The [follow-up](../research/exp-pacing-and-move-services.md) covers level-one acquisition, EXP. ALL, music-preserving speed options and move services.

Two checks protect the original experience. Buying coins from zero must still pay for Red’s most expensive prize. The Route 5 attendant keeps his existing lines, and the Day Care keeps the move order also found in the Kanto remake. [Game Corner redemption](../research/game-corner-redemption.md) · [Day Care comparison](../research/day-care-history.md)

The [player-impact review](../research/sweep-decisions.md) gives current preset decisions. The [scope audit](../research/final-scope-audit.md) records the original comparisons. [Emerald Rogue](../research/emerald-rogue-builds.md) supplies a separate edition-publishing precedent.

[The current scope review](../research/minimal-action-review.md) compares field and menu shortcuts with rules that change team building. The [storage study](../research/storage-policy-and-code.md) and [refactor inventory](../research/refactor-scope.md) set the technical boundaries for the options.

The [badge precedent and data changes](../research/core-rule-precedents.md) specify current Core decisions. The [box](../research/box-overflow-contract.md), [save](../research/box-picker-safety.md) and [field](../research/field-shortcut-contract.md) reviews include new stock fixtures and distinguish inspected source from observed results.

The [pre-build investigation](../research/foundation-audit.md), [archived case decisions](../research/catalog-decisions.md) and [stock observations](../research/foundation-checks.json) give the current inventory and evidence limits.

Repository pins established on **2026-10-11**, **2026-10-12**, and **2026-10-14**. Git repositories were read at the exact revisions in [source-lock.json](../research/source-lock.json). [evidence.md](../research/evidence.md) provides source locations and the scope of each finding. Mutable web pages carry a check date rather than an invented commit pin.

## Evidence levels

**Source-verified:** a checked routine, data table or repository file supports the finding. **Derived:** arithmetic or an inference follows from that source and is labeled. **Reported:** documentation or an announcement makes the claim; implementation may need more proof. **Proposed:** a project engineering choice. **Unresolved:** the required evidence or decision is incomplete.

Source review establishes the code path. The [Gen 1 bug-fix survey](../research/donor-bugfix-survey.md) adds 35 stock-ROM cases for two battle STATS display problems, Blaine's potion use, and the SHIFT prompt. The scope of each test is recorded with its result. The survey also compares 18 projects and records the current preset decisions. Patched builds and real hardware checks remain pending.

## Material corrections

| Claim requiring correction | Verified finding / project consequence |
|---|---|
| A Solus-style Focus Energy fix can be copied while retaining normal Gen 1 critical rates. | The pinned Solus routine lowers ordinary unpumped rates as well. For Speed 130, its ordinary threshold is 16 without Focus and 65 with it; vanilla is 65 without Focus. Do not port that routine unchanged. [E04](../research/evidence.md#e04), [E22](../research/evidence.md#e22) |
| Jolteon-like Speed 130 in Solus gets a vanilla ordinary rate and almost-certain Focus critical hits. | The proposed correction can produce 65/256 and 255/256, but the checked Solus source produces 16/256 and 65/256. Yellow and Solus do support obtaining Focus Energy through Eevee at level 36 before evolution; Red/Blue's own Eevee learnset does not. Move access and arithmetic are separate findings. [E61](../research/evidence.md#e61) |
| Replacing the Focus branch or using a wiki patch necessarily preserves the whole critical system. | Shift order, odd-Speed rounding and early saturation matter. Some alternatives change high-critical thresholds; an early 255 cap followed by division gives 127. Use exhaustive tests. [critical-hit analysis](../research/critical-hit-analysis.md) |
| The ordinary formula is exactly Speed/512 and a high-critical threshold is always four times Speed. | Those are useful approximations, not exact integer rules. The checked unpumped thresholds are floor(Speed/2) and min(8 × floor(Speed/2), 255). [E04](../research/evidence.md#e04) |
| A fixed-damage immunity change is an unobjectionable defect repair. | English Red/Blue deliberately routes set-damage effects around ordinary type adjustment in its code. Night Shade and Seismic Toss bypass immunities. Whether that was the original designers' intent is a historical question; the project's preservation decision is settled. [E07](../research/evidence.md#e07) |
| Shin Lite is a ready-made mechanically faithful bug-fix base. | Its documented changes include forced Hyper Beam recharge on KO, modern fixed-damage immunities, removed 1/256 misses and changed critical damage. “Lite” does not establish compatibility with this contract. [E23](../research/evidence.md#e23) |
| Every Shin build unavoidably requires Hyper Beam recharge on KO; its game text reverses its source behavior. | The pinned Master branch can skip recharge through a clause, and its NPC text agrees with its handler. A README history line conflicts. The checked Lite path sets recharge without that guard. Keep branch-specific claims separate. [E60](../research/evidence.md#e60) |
| Badge stacking should also occur in ordinary link battles because stat recalculation exists there. | The badge-boost routine exits for link battle state. Recalculation faults can still affect other state, but badge boosts are a separate single-player path. [E12–E13](../research/evidence.md#e12) |
| Badge stacking, status medicine, and burn/paralysis recalculation are one repair. | They have different triggers. Stat moves can reapply or erase penalties through the checked paths even though badges are excluded from link battles. Track RGB-027 separately from RGB-013 and Q02. [E50](../research/evidence.md#e50) |
| An Itemfinder report necessarily proves a broken ordinary vanilla-play path. | The routine excludes items at coordinate zero, but the pinned 54-entry coordinate table contains none. It is a confirmed conditional data boundary, with vanilla reachability unproven. [E51](../research/evidence.md#e51) |
| Fixing badge text means swapping the boosted stats. | English Red/Blue implements Thunder→Defense and Soul→Speed, while several strings say the reverse. The original US manual and FRLG calculations support Thunder→Speed and Soul→Defense as likely intended. D25 now accepts that code correction in Core, retaining original descriptions and stacking. This is an explicit behavior change; it is not proof of internal design intent. [Badge review](../research/badge-intent.md), [E75–E77](../research/evidence.md#e75). [E42](../research/evidence.md#e42) |
| A latest pret-based fork automatically performs vanilla hash checks in CI. | Pinned upstream runs `compare` conditionally for owner `pret`; forks run a build branch. Add a pristine-reference check deliberately. The pinned RGBDS version is 1.0.4, not the earlier 1.0.3 claim. [E03](../research/evidence.md#e03) |
| Single-byte species fields provide a ready 255-species expansion limit. | There are 256 encodings, but sentinels, internal indexes, tables and other formats constrain usable IDs. Widening storage, Dex mappings, saves and links is an engine migration, not a larger table alone. [E17](../research/evidence.md#e17) |
| Increasing cartridge ROM alone makes modern mechanics inexpensive. | Internal RAM and processing limits remain. Current code uses MBC3 and one-byte bank tracking; MBC5's capacity needs compatible bank-switching changes. [E18–E21](../research/evidence.md#e18) |
| Every RGB release is effectively the same game or a reconstruction of Japanese Blue/Green. | The verified English upstream has Red/Blue data selections. Solus/Pure consolidate gameplay differences for their own releases. Our Green is a chosen cosmetic Blue variant, not a historical reconstruction. [E02](../research/evidence.md#e02), [E33–E34](../research/evidence.md#e33) |
| October 15, 1996 is only an announcement date, so calling it Japanese Blue's release date is wrong. | The official Pokémon page lists October 15, 1996 as the release date. Its 30th anniversary falls on October 15, 2026. A more specific first-delivery timeline was not established here. [E40](../research/evidence.md#e40) |
| Emerald Expansion ignores all licensing notices or is project-wide MIT. | The checked tree has no root project-wide license file under the usual names, but does retain tool-level notices and attribution guidance. Neither observation grants rights to the entire derived game. [E38](../research/evidence.md#e38) |
| A save-write delay provides full power-loss protection. | The catalog suggests moving a write after a wait, but this is not proof of transactional recovery. A claimed safe-save design needs write-phase fault injection and a recovery rule. [E32](../research/evidence.md#e32) |
| Existing hacks must migrate without rewriting to make this foundation worthwhile. | That is not a requirement. Heart & Soul's developer repository confirms the Expansion foundation and pre-2.0 save incompatibility. Radical Red's announcement describes an Expansion remake and incompatible saves, rather than a finished migration. [E39](../research/evidence.md#e39), [E41](../research/evidence.md#e41) |

## Findings that should not become stronger claims

The [historical evidence review](../research/historical-evidence.md) verifies the cited Prima passage and its cover/publication details from the scan. The Sabrina advice recommends Bug and Ghost Pokémon; it is not an explicit specification of a Ghost attack multiplier. The checked gym dialogue gives similar advice while the stock chart records immunity. The early Japanese guide goes further and explicitly shows a Ghost attack advantage in its matchup table. Core follows that evidence under D50. Nintendo Power's cited page also contains demonstrably inaccurate move/evolution advice. These sources do not establish Game Freak's internal design or approval process. Original intent is not needed to preserve the agreed default chart. [E53–E54](../research/evidence.md#e53), [E62](../research/evidence.md#e62)

Official Stadium descriptions confirm importing RBY Pokémon and playing the Game Boy games on a TV. That establishes interoperability, not the reason a particular type relationship was retained or a requirement for identical battle rules. [E55](../research/evidence.md#e55)

The pinned `pret/pokestadium` text notes contain Night Shade's immunity-independent wording and describe Karate Chop and Gust as Normal. Text notes are narrower evidence than executable battle code. The complete Stadium comparison of type-chart entries, Focus Energy, Hyper Beam, and effectiveness messages was not verified against that engine here. The [Yellow comparison](../research/yellow-rules-review.md) now distinguishes the Japanese and English Gym hints. See the [historical review](../research/historical-evidence.md). [E59](../research/evidence.md#e59)

The broad Japanese Blue→international code lineage is common historical reporting. This task did not establish a complete source-to-source lineage comparison. It is not an implementation premise: `pret/pokered` directly provides the English versions needed. The original Japanese Red/Green predate Japanese Blue, so “every version is based on Blue” is too broad in any case.

Solus/PureRGB documentation verifies their stated variant/design choices. It does not establish every current bug's implementation or every player's behavior. TODOs and missing feature-list entries cannot prove deliberate preservation. The Focus Energy finding is based on its actual pinned routine. Selected PureRGB move data, species types, Ghost damage selection, and trapping duration were also checked in source. The [donor review](../research/donor-review.md) separates checked code from documentation claims; it is not a complete runtime audit or a ranking by fix count. [E57](../research/evidence.md#e57)

Solid Red's README supports its narrow bug-fix mission. This review does not claim that its wiki is a complete implementation inventory or that no other usable foundation exists. Claims that the work will be easy, almost complete, or universally liked are not established technical facts.

Pokéemerald Expansion's feature/configuration files and tests support using it as a developer-experience reference. Its GBA C implementations are not drop-in Game Boy assembly, and the presence of a test file does not prove every listed modern feature combination works. [E35–E37](../research/evidence.md#e35)

## Expansion configuration reference

The current Emerald Expansion source enables all nine species generations by default and sets `GEN_LATEST` to `GEN_9`. Developers can disable generations or families, control later forms/evolutions, and select older rule/data settings. Encounter tables are separate from species support. Its configuration policy favors modern gameplay defaults; that is not this project's chosen baseline. See [the source-backed comparison](../research/expansion-configuration.md). [E63–E64](../research/evidence.md#e63)

A mostly vanilla Emerald hack is a supported design direction, with later species excluded or unused. Exact original behavior requires more than generation settings: the checked Expansion random-number generator differs from the original one, and its basic trainer AI is documented as making better move choices than vanilla. These findings do not imply that restoring behavior in editable source is impossible. [E65–E66](../research/evidence.md#e65)

Trainer AI flags are developer choices. A claim that Expansion provides no AI controls would be incorrect. The narrower limitation is that this review did not verify a complete original-AI profile. Its configuration policy favors modern defaults; the maintainers' specific reasoning about full original-game support was not established here. [E64](../research/evidence.md#e64), [E66](../research/evidence.md#e66)

The original `pret/pokeemerald` identifies a reconstruction of the original ROM. It is the direct reference for an original-behavior starting point; that build was not executed here. PokéRGB's baseline is its own Gen 1 contract plus accepted corrections, with small hacks supported as directly as projects using optional systems. [E67](../research/evidence.md#e67)

## Design reference

Kayin's [Quality of Life](https://kayin.moe/quality-of-life), published January 18, 2025, argues that convenience changes can alter player incentives and rewards. The [convenience review](03-bug-fix-policy.md#review-convenience-features) applies that question to proposed developer features. Its Pokémon examples are design considerations, not measured player outcomes or evidence of original intent. [E58](../research/evidence.md#e58)

## Research coverage and reproducibility

The [Yellow comparison](../research/yellow-rules-review.md), [named hack comparison](../research/developer-hack-comparison.md), [tutorial inventory](../research/tutorial-library.md) and [species format study](../research/species-id-architecture.md) extend the pre-build review. They separate retail behavior, donor changes, developer requests and proposed shared implementations.

The curated inventory traces the most consequential boundaries to source. The intake covers all 94 headings in one pinned archived bug catalog. Broader completeness requires source-wide auditing, executable reproductions, donor comparison and normal-play reports. None of those remaining tasks is concealed by the count of entries.

To reproduce source research, fetch each repository in the source lock, check out the recorded revision, and inspect the paths and line ranges in the evidence index. Wiki source is available through `https://github.com/pret/pokered.wiki.git`; the human-readable wiki URL is mutable, so its Git revision and file hash are recorded separately.

The included arithmetic analysis can be regenerated locally. Its calculated probabilities assume uniform random-byte input and derive from the reviewed routines. It is research evidence for a test oracle, not a passing emulator regression suite.

## Menu-return findings

PC STATS does not directly close the box. It restores the selected-Pokémon action menu, whose B/CANCEL result sends the caller to the PC main menu. The accepted repair restores the list and cursor/scroll context. The [inventory](../research/menu-navigation.md) separates this from medicine's retained return-to-bag flow and from the accepted shop returns and overworld party action-menu cancellation. [E83–E86](../research/evidence.md#e83)

The original status pages use A/B waits; their callers execute both pages in sequence. Directional Pokémon/page navigation is new accepted Core behavior. The original display information remains; possible DV/stat EXP pages are developer extensions. Release safety is a caller-scoped default, and Repel renewal is an optional stretch goal. [E84–E87](../research/evidence.md#e84)

## Broad small-fix and usability review

The [audit](../research/usability-audit.md) and [63-case coverage table](../research/usability-coverage.csv) cover routine systems beyond menus. A separate [47-call gift screen](../research/gift-call-sites.csv) records direct script gift calls, with two unhandled delivery results flagged. A nearby carry check is not a passing game test.

[E88–E100](../research/evidence.md#e88) trace coin amounts, vending prices, gift completion, trade/Oak text, the introductory cry, Flute feedback, trainer status display, spin pointers, existing controls, Snorlax interaction, admission gates, and existing safeguards. Source revisions are unchanged. The report separates narrow correction recommendations, new usability proposals, already accepted requirements, and work that is important but not small.

The original 40-coin event reports and awards 20 after the wrong conversion; it does not display 40 while awarding 20. Vending underflow clamps to zero, rather than granting wrapped money. Flute's alternate response says “catchy tune,” omitting the wake-up confirmation; it does not literally say “no effect.” The source alone does not establish a permanent money-gate softlock or the original team's design intent. No ROM build, runtime regression, or personal-save operation was performed.

## Transaction review and later-game comparisons

[E101–E105](../research/evidence.md#e101) add the rooftop payment-loss path, existing move information, quantity/elevator comparisons, and current Expansion battle-information controls. Separate current Expansion and Gold/Silver reference pins retain earlier research revisions. The [comparison](../research/remake-usability-comparison.md) distinguishes source facts, project judgments, and missing original-intent evidence.

The 47-call gift screen checked nearby result branches, not every complete exchange. Rooftop calls pass that screen but remove payment before reward delivery. Their verified failure is now explicit. A final drink can free a slot; no duplicate TM award is established by the checked ordinary path. FireRed retains a remove-before-space-check ordering under different item-pocket rules.

Red/Blue already shows move type and PP during battle selection, and some NPCs identify gifted TMs. The absence of a general power/accuracy/description viewer must not be overstated as no move information anywhere. D61 adopts static INFO in both presets. Displaying both active battlers’ types remains optional. The current Expansion type display is configurable and disabled by default, independently of its enabled move-description feature. No claim of poor programming, a known time-pressure cause, or proven original intent follows from these sources.

## Item-list reset finding

[E106](../research/evidence.md#e106) verifies a separate state problem behind item-PC deposits: deleting a stack clears current and saved cursor/scroll fields in the shared removal helper. Shop loops also reset their visible row. The correct return destination in E86 did not prove position retention; MN06/MN09 now distinguish these checks. [PN-019](13-playthrough-intake.md#pn-019) adds the Core requirement while keeping earlier medicine and successful Pokémon-transfer decisions unchanged. This is source research at the retained pin, not a runtime repair or proof of original design intent.

## Larger bag feasibility

[E107](../research/evidence.md#e107) checks the upstream 50-slot bag tutorial against the retained Red/Blue allocation and save routines. The 128-byte reserve holds 60 entries plus count/terminator in 122 bytes; 63 is the arithmetic limit of that reserve alone. This supports a small optional allocation proposal without establishing a universal maximum, a tested 60-slot game, or unchanged saves. Bag and PC constants are separate; a PC alternative still needs its own allocation review. [PN-020](13-playthrough-intake.md#pn-020) records the Extension direction and exact verification boundary.

## Selected bag reserve

D36 selects the separate 134-byte reserve rather than shifting surrounding fields. [E108](../research/evidence.md#e108) and the [RAM allocation review](../research/bag-memory.md) verify that the original bag has no adjacent spare bytes and that the separate reserve can hold 64 entries with a four-byte format marker. Sixty-four is both the selected preset and the bound of this allocation; it is not a tested engine-wide maximum. The RAM-only audit keeps every other existing WRAM label fixed. Feature overlap, shared routines, and save conversion still need implementation evidence.

## Expanded-bag initialization

[E109](../research/evidence.md#e109) traces a required ordering change: `InitPlayerData` initializes the bag before clearing game-progress bytes. The clear covers the first 78 bytes of the selected reserve. Initialize the relocated bag and format marker after that clear while retaining all original field addresses. This is a source-verified requirement; new-game, save, and combination checks are still release work.

## Move cursor, box order, and Mansion trainers

[E110](../research/evidence.md#e110) traces SELECT redraws to an older saved move index. [E111](../research/evidence.md#e111) confirms the separate prepend/append paths, the boxed-gift caller, and the nickname's slot-one assumption. [E112](../research/evidence.md#e112) checks all six Mansion trainer settings and the shared sight path. The [review](../research/cursor-box-and-trainers.md) separates source facts, selected usability policies, and unknown original design reasons. No game patch or runtime reproduction is claimed.

## Mansion intent comparison

[E113](../research/evidence.md#e113) checks ordinary zero-range trainers in Red/Blue and Gold/Silver, the unchanged Mansion ranges in Yellow, and the positive Burglar ranges in FireRed/LeafGreen. The [comparison](../research/cursor-box-and-trainers.md#how-strong-is-the-evidence-for-intent) gives evidence for a valid Gen 1 encounter choice while retaining uncertainty about original intent and the remake's purpose. D39/PN-023 now selects a scoped Core correction; the source setting alone is not proof of intent.

[E114](../research/evidence.md#e114) adds spatial context: all four Route 21 Fishers stand at the edge of land and face immediately adjacent water. The [geometry record](../research/route21-fisher-geometry.json) and [review](../research/cursor-box-and-trainers.md#route-21-fisher-geometry) qualify the earlier analogy. Zero range is a supported mechanism; its use for Fishers does not establish the Mansion Burglars' rationale. Treat original Mansion intent as unproven. D39 separately accepts a scoped sight-engagement correction for these three Burglars.

## Viridian Forest star-grass recognition

[E115](../research/evidence.md#e115) checks Red/Blue encounter and sprite routines against Yellow, then decodes the identical map and blockset. The lower-right encounter check misses 114 grass squares that the lower-left sprite check recognizes. The [review](../research/forest-encounters.md) and [audit](../research/forest-encounter-audit.json) support a likely-oversight conclusion. D40/PN-024 accepts the scoped Core repair. Original intent is strongly inferred; no original developer statement or running-game test is established.

## Acid Armor picture visibility

[E116](../research/evidence.md#e116) traces the original picture erase and records single-player stock-ROM cases across Red, Blue, and Yellow. [E117](../research/evidence.md#e117) checks the original Japanese versions, the contemporary Nintendo guide, and the later official animations. [E118](../research/evidence.md#e118) compares hacks. [E119](../research/evidence.md#e119) verifies when the picture returns and how that differs from the Defense boost. D41 accepts the Core repair in [PN-025](13-playthrough-intake.md#pn-025). [Focused review](../research/acid-armor.md)
