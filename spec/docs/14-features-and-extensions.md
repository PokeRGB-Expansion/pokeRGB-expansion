# Core and extensions

Core and Minimal build from the same source tree in English Red, Blue and Green. Green shares Blue’s gameplay. Extended is a planned set of options for hack authors. The tables distinguish current defaults from those designs. [Build instructions](../../README.md#build)

## Product presets

A preset chooses the game’s defaults at build time. Authors can edit shared data such as encounters and move rules, or use an available build option. Document the rules and save format of a custom build. [Tutorials and configuration contract](../research/tutorial-library.md)

| Feature or behavior | Minimal | Core | Extended design |
|---|---|---|---|
| Dual-type effectiveness feedback and unidentified Tower ghosts after STATS | Correct the message and sound. Restore the ghost disguise. | Same repairs | Inherit the repairs. Feedback follows the selected rules. |
| Acid Armor melt, wrong-side Substitute/Minimize redraw, move-replacement sound | Apply the presentation repairs | Same | Inherit the repairs |
| Charizard learns HM02 Fly | Stock permission excludes Fly | Add Fly to Charizard only | Inherit Core. The complete Yellow machine pack is independent |
| Ghost attacks against Psychic | Stock 0× chart entry | 2× chart entry | Inherit Core. A developer can select either chart row independently |
| Gust, Karate Chop and Sand-Attack | All Normal | Gust is Flying. Karate Chop and Sand-Attack are Normal | Inherit Core. Other move retypings are independent |
| Contextual Cut, Surf and Strength | A prompt and original party commands | Same | Inherit. Preserve field prerequisites |
| Space in another PC box | Only the selected box accepts arrivals | Same | Manual by default. Enable automatic placement or direct MOVE independently |
| Machine names and move INFO | Read details in the bag, PC, shop, prize list, STATS, FIGHT and when choosing what to learn or forget | Same, with Core’s move data and effects | Inherit Core and read the configured move tables |
| Storage counts, Mart quantity, PP item readout and Pokédex row | Show counts, show the targeted move’s PP, and remember the Dex row until reload | Same | Inherit Core |
| Selected box just filled | Original transfer notice | Identify the just-filled box at the end of a successful transfer | Inherit Core |
| Box chooser | Show occupancy and preserve saved data on cancellation | Same | Same |
| Species ID storage | Stock format | Stock format | Compact by default. Select a wider format when the roster needs it |
| Transform against a hidden Fly/Dig target | Can copy the target | Fail while the target has the invulnerable flag | Inherit Core |
| Swift against that target | Can hit | Can hit | Inherit Core |
| Special stat | Unified | Unified | Unified Special is the preferred starting point for new Gen 1-style games |
| Focus Energy and Dire Hit | Use the cartridge's reversed effect | Correct the pumped critical-hit chance | Inherit Core unless a developer selects different critical-hit rules |
| Blaine at full HP | His successful item roll can still spend a turn and a potion use | Skip that use and allow his normal action | Inherit the guard. A selected trainer AI can supply another policy. |
| Thunder and Soul badges, Mansion Burglar sight, Forest star grass | Original badge mapping, sight ranges, and encounter eligibility | Apply the accepted corrections | Inherit Core |
| EXP. ALL toss/sale | Protect the one-time reward through the existing key-item safeguards | Same | Inherit Core |
| EXP. ALL experience | Always active while carried. Original awards. | Starts on. USE in the field switches sharing on or off. Calculate the two shares independently while active. | Inherit Core |
| Level-one experience and Cycling Road | Original growth and gate behavior | Valid initial EXP at level one. Both gate guards enforce the Bicycle requirement. | Inherit Core |
| Forgetting a move | Original rules | Fuchsia’s Move Deleter can remove a known move, including an HM, if another move remains. | Inherit Core. A party-menu Move Reminder requires separate work. |
| Battle pace | Original timing | NORMAL by default. QUICK shortens four presentation waits in ordinary battles. | Inherit Core |
| Vending prices and rooftop TM payment | Original transactions | Apply the accepted corrections | Inherit Core |
| Hyper Beam on KO, trapping, fixed damage, and badge stacking | Original rules | Original rules | Inherit Core unless explicitly overridden |
| Improved trainer AI, added types and later Pokémon | Original systems | Original systems | Developer selects each supported capability |
| Double and triple battles | Singles | Singles | Possible future designs. Feasibility and delivery are open. |

For a new proposal, record what a player can do, what the opponent can do, and the result in each preset. **Minimal** preserves the outcome of the same gameplay choices from the same state with the same random inputs. Keep the original generator, roll triggers, and interpretation of each roll. Text and animation timing may differ during play. Correcting information a player sees can qualify even if it influences their next choice.

**Core** accepts evidenced repairs and selected improvements that keep the character of Gen 1. **Extended** is the planned set of additional systems for authors. Minimal also includes eligible action shortcuts such as contextual HMs and a registered Bicycle or fishing rod. For a disputed shortcut, compare what the player can do, when, at what cost, and how the opponent can respond. [Minimal examples](../research/minimal-action-review.md)

## Core

Core follows the [decisions](01-decisions.md) and [mechanics contract](05-mechanics-contract.md). It keeps defining Gen 1 behavior, corrects accepted defects, and includes explicitly accepted safety and interface improvements that preserve meaningful constraints and choices.

Authors can start a small hack with Core and change only the content they need. For an accepted safeguard or interface change, add a separate author switch when there is a clear use and it can be maintained independently.

## Extensions

The planned extensions cover larger changes to player choices, storage and battle rules. Each supported option needs source, documentation and tests in the shared repository. Keep unrelated choices independent and document genuine dependencies.

## Preserve constraints and choices

All three presets can contain features described as quality of life or basic usability. Those labels do not decide default inclusion. Ask what a change does to player actions, information, costs, preparation, progression, and existing limits. Removing menu steps can preserve a requirement; removing the requirement changes the game. Each accepted default still needs an explicit scope and review of its effects.

Keep the **20-slot bag** in Core. Choosing what to carry and when to use storage remains part of this project's game experience. A larger bag or a separate key-item pocket would be an optional design change, not an incidental interface repair.

The checked source defines and enforces 20 bag slots. Its inventory also occupies working memory and saved data. This does not establish why the original team chose 20, or prove that a larger bag would have had no technical cost. Do not present the inventory-management interpretation as a verified statement of original intent. [E72](../research/evidence.md#e72)

Contextual HM use illustrates an accepted improvement within the constraints. Pressing A at a tree can replace the route through the party menu while still requiring a party Pokémon that knows Cut, its move slot, the badge, and a valid target. This does not grant field abilities without teaching their moves. See [PN-004](13-playthrough-intake.md#pn-004).

Patch size, coding difficulty, and whether a later game has the feature do not decide its layer. When core inclusion is uncertain, retain the existing default and document the proposed alternative.

## Feature catalog

Rows marked **Included** describe the reference games. Rows marked **Planned** describe designs that authors cannot enable in these builds. The [bug register](04-bug-triage.md) and [mechanics contract](05-mechanics-contract.md) give the evidence for individual corrections.

| Feature | Layer | Default | Accepted scope |
|---|---|---|---|
| Focus Energy correction and other approved defect repairs | Core | Included | Apply the bug policy and protect unrelated mechanics; verify the Q01 threshold and both actor paths in the integrated build |
| Unambiguous typo corrections | Minimal and Core | Included | Preserve meaning and voice; check line layout and shared uses; Oak's rating is [PN-005](13-playthrough-intake.md#pn-005) |
| Thunder/Soul stat mapping | Core | Included | Thunder→Speed and Soul→Defense; original descriptions, bonus amount, rounding, cap, other badges, link exclusion, and stacking retained; [D25](01-decisions.md) |
| EXP. ALL toss and sale protection | Minimal and Core | Included | Protect the one-time reward with the existing important-item messages. Keep acquisition and item PC storage. RGB-017 specifies the Core award correction. [PN-001](13-playthrough-intake.md#pn-001) |
| SELECT item registration | Minimal and Core | Included | Register one Bicycle or fishing rod. Keep the normal riding, shore, bite and encounter rules. [PN-002](13-playthrough-intake.md#pn-002) |
| Box browsing and return context | Minimal and Core | Included | Browse and view STATS with a full party; return to the list after STATS/action cancellation; preserve cursor/scroll; reject only an actual withdrawal when the party is full; [PN-003](13-playthrough-intake.md#pn-003) |
| STATS navigation | Minimal and Core | Included | Up/down changes Pokémon, left/right changes page, B restores browsing context; support later developer pages; [PN-006](13-playthrough-intake.md#pn-006) |
| Safer release confirmation | Minimal and Core | Included | Show nickname/species, default to No, remove only after explicit Yes; [PN-007](13-playthrough-intake.md#pn-007) |
| Shop refusal return context | Minimal and Core | Included | Unsellable items return to SELL; money/space failures return to BUY, retaining selection/scroll and transaction rules; [PN-008](13-playthrough-intake.md#pn-008) |
| Party action-menu cancellation | Minimal and Core | Included | CANCEL and B both restore the overworld party list with the same Pokémon selected; keep the normal party-list exit and other caller rules; [PN-009](13-playthrough-intake.md#pn-009) |
| Vending price checks | Core | Included | Check and charge the selected price; refused delivery changes no money/items; [PN-010](13-playthrough-intake.md#pn-010) |
| Flute wake-up feedback | Minimal and Core | Included | Report actual wake-ups without changing effects or turn costs; [PN-011](13-playthrough-intake.md#pn-011) |
| Trade follow-up text | Minimal and Core | Included | Remove the false evolved-Raichu claim without changing trades/evolution; [PN-012](13-playthrough-intake.md#pn-012) |
| Elevator floor and same-floor handling | Minimal and Core | Included | Mark the current floor; prevent false travel and destination changes; [PN-013](13-playthrough-intake.md#pn-013) |
| Quantity shortcuts | Minimal and Core | Included | Left/right ten, up/down one with original wrap; bounds and transactions retained; [PN-014](13-playthrough-intake.md#pn-014) |
| Item-list position | Minimal and Core | Included | Retain selection/scroll through same-list returns; choose the adjacent entry after removal and clamp safely; [PN-019](13-playthrough-intake.md#pn-019) |
| Move-swap cursor | Core | Included | Retain the current row through marking/completing SELECT swaps; preserve battle/input rules; [PN-021](13-playthrough-intake.md#pn-021) |
| Consistent box insertion | Core | Included | Append captures and boxed gifts, matching deposits; keep existing positions, limits, and complete records; [PN-022](13-playthrough-intake.md#pn-022) |
| Mansion Burglar sight | Core | Included | Restore normal sight-triggered battles for these three Burglars; preserve Scientists and other zero-range trainers; original intent unproven; [PN-023](13-playthrough-intake.md#pn-023) |
| Star-grass encounter recognition | Core | Included | Affected Forest grass uses the existing encounter rule and data; preserve other surfaces; [PN-024](13-playthrough-intake.md#pn-024) |
| Acid Armor sprite restoration | Minimal and Core | Included | Keep the original melt and restore the same sprite at animation end. Preserve move mechanics. [PN-025](13-playthrough-intake.md#pn-025) |
| Battle STATS, move-replacement sound, and empty SHIFT prompt | Minimal and Core | Included | Correct both enemy redraws and the sound. Skip a switch prompt with no eligible reserve. [D43 repair scopes](04-bug-triage.md#donor-survey-dispositions) |
| Rooftop drink/TM exchange | Core | Included | Payment and reward succeed together or stay unchanged; [PN-015](13-playthrough-intake.md#pn-015) |
| Medicine menu flow | Minimal and Core | Preserve | Return to the bag after use; no repeated target selector |
| Repel renewal prompt | Extension | Planned | Future stretch goal: offer another of the same kind on expiry, consuming one only on confirmation; preserve duration and encounter rules |
| Contextual HM prompts | Minimal and Core | Included | Press A at a suitable target and confirm; preserve learned moves, badges, and use restrictions; [PN-004](13-playthrough-intake.md#pn-004) |
| Day Care and the Game Corner clerk | Minimal and Core | Preserve stock | Keep the Day Care’s move order, fees and character dialogue, and the coin clerk’s rules and lines. Test the top-prize purchase through redemption. [Day Care](../research/day-care-history.md) · [Game Corner](../research/game-corner-redemption.md) |
| MOVE POKÉMON interface | Extension | Planned | Future storage interface for moving Pokémon; does not require automatic capture overflow |
| Automatic capture storage in another available box | Extension | Planned | Use remaining storage independently of direct MOVE. [Contract and tests](../research/box-overflow-contract.md) |
| Larger item capacity | Extension | Planned | 64-slot bag target; keep PC capacity independent and Core at 20 bag/50 PC slots; verify allocation and saves; [PN-020](13-playthrough-intake.md#pn-020) |
| Battle type indicators | Extension | Planned | Both active Pokémon; separate from move reference; [design](15-battle-information.md) |
| Static move INFO | Minimal and Core | Included | Inspect the selected player move on demand. Developer type indicators remain independent. [Controls](15-battle-information.md) |
| Caught marker and battle EXP bar | Minimal and Core | Both on | Author switches are independent. The marker uses the Pokédex owned record and the meter reads the active party slot. [Display and visibility rules](../research/battle-hud-displays.md) |
| TOSS quantity, party reordering and Pokédex A–Z | Minimal and Core | Included | TOSS shows the chosen count in the Bag and item PC. SELECT reorders the field party or toggles a seen-only alphabetical Pokédex. [Cartridge checks](../../tests/field_menu_features.py) |
| OPTIONS in dark caves and Town Map input | Minimal and Core | Included | Read OPTIONS in unlit Rock Tunnel. Darkness returns on exit. The first directional press at Route 1 and the Power Plant advances the map. [Field checks](../../tests/field_sweep.py) |
| HP bar | Minimal and Core | Included | Even with high max HP, losing one HP leaves a visible gap. [Battle, party and STATS checks](../../tests/hp_and_level_one.py) |
| Supply INFO and move properties | Minimal and Core | Included | Read a supported supply’s effect before using or buying it. Move INFO identifies priority and high critical-hit rates. [Controls](15-battle-information.md) |
| Level-one EXP and Bicycle gate checks | Core | Included | Repair initial EXP when the growth curve would wrap. A player holding Left still needs a Bicycle at either gate. Minimal keeps the stock outcomes. [Original cases](../research/v020-feature-sweep.md) |
| EXP. ALL switch, Fuchsia Move Deleter and battle pace | Core | Included | Turn EXP sharing off between battles, choose a known move to forget, or shorten selected waits in ordinary battles. [Behavior and evidence](../research/exp-pacing-and-move-services.md) |
| Party-menu Move Reminder | Extension | Planned | Decide eligibility separately for a species’ learnset and an individual Pokémon’s move history. Earlier saves cannot supply a complete history. |
| Later Pokémon, types, and mechanics | Extensions | Planned | Long-term capability, with separate supported choices and explicit dependencies |
| Alternative trainer AI | Extended feature | Planned | Develop and test improved move and item decisions. Core includes only individually accepted changes such as Blaine's guard. |
| Replacement random-number generator | Extension | Planned | Keep it independent of trainer AI and test the original generator when disabled |

For each implemented feature, link its developer guide and executable tests. Record changed behavior, dependencies, supported combinations, memory/performance cost, save/link effects, and release status. Do not label an option available until its implementation and advertised behavior pass the relevant checks.

<a id="storage-extensions"></a>

## Storage extensions

### MOVE POKÉMON

**Accepted direction:** provide a direct way to move Pokémon through the storage interface. This is a larger interface feature than allowing the current WITHDRAW list to open with a full party.

**Proposed scope:** move Pokémon between party and boxes and between boxes, with clear destination selection and normal capacity rules. The exact interface and whether a full party permits a swap require a feature design. This is not a default party-capacity increase, expanded storage system, or automatic-capture feature.

Before release, demonstrate ordinary transfers, full destinations, cancellation, and the rule against leaving the party empty. Preserve every transferred Pokémon's data without loss or duplication. Check first, middle, and last entries, repeated transfers, box changes, and save/reload. Review save-format effects before implementation; do not promise vanilla save compatibility from the feature name alone.

### Automatic capture storage

Both reference presets require room in the party or the selected box. The planned automatic placement option would use the next non-full box for a catch or gift that already allows PC delivery. Preserve all twelve boxes of twenty, the active selection and the player’s last saved adventure. [Selection and recovery](../research/box-overflow-contract.md)

Design the two options to work independently. Direct moves between boxes need no automatic placement of catches. Capture overflow should work with the existing PC interface, box limits and battle rules.

Support the default, each feature alone, and both together. Test each before advertising that configuration. If a real technical dependency prevents a promised combination, resolve or document it explicitly rather than quietly bundling the features.

## Optional interface work

Repel renewal is an accepted optional extension and stretch goal. When enabled by a developer, expiry can offer another of the same Repel kind if one remains. Confirmation consumes one item; cancellation leaves the expired state. Preserve the original durations, leading-Pokémon level rule, and expiry timing. Remember the kind used rather than guessing from the remaining counter, and verify save/reload behavior for that state. No new player setting or Core requirement follows from this extension. [E87](../research/evidence.md#e87)

Authors can append a STATS page in either preset. A downstream page could show DVs or stat experience. The reference games keep the two original pages. [Adding a page](02-architecture.md#stats-view-and-return-context)

## Build and documentation structure

Use one central developer configuration with clear names and disabled defaults for Extensions. Group choices by purpose, such as storage, battle, content, and presentation. Keep Red/Blue/Green identity separate from feature selection.

Each extension gets a short guide with its purpose, exact behavior change, how to enable it, dependencies, compatibility effects, example, and test status. Its disabled state must preserve Core behavior. Share helpers where useful, while keeping the entry points and data changes reviewable.

The reference game uses Core. A small customization example uses Core plus a small content edit. Additional examples show particular extensions. Player controls such as registering an item remain normal game controls; build choices do not create a player menu of competing rules.

Each independently selectable extension needs an author example and tests. [Architecture](02-architecture.md)

<a id="further-candidates"></a>

## Inventory and move displays

The [player-impact review](../research/sweep-decisions.md) records the adopted display placements, the Core-only full-box reminder and optional author features. Both reference presets give the usual hidden-coin receipt when every coin fits.

<a id="item-capacity"></a>

## Larger item capacity

Core and Minimal keep 20 Bag slots and 50 item-PC slots. The planned larger Bag targets 64 stacks with the original stack limits and item rules. It needs no change to the item PC, pockets, sorting, Pokémon storage or battle systems.

In the upstream layout, 64 entries, four format-marker bytes, a count and a terminator fill the 134-byte block at `$D66A–$D6EF`. Current builds keep the registered SELECT item in two of those bytes. A build using the whole block must move the registration fields safely and preserve them on supported save imports. The original 42-byte Bag footprint and the other field addresses stay fixed. [Memory study](../research/bag-memory.md) · [Source evidence](../research/evidence.md#e108) · [Save and test requirements](13-playthrough-intake.md#pn-020)
