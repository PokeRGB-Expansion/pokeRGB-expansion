# What changes when you play?

This guide describes the reference builds. Core includes the accepted Core changes and shared fixes. The examples below explain how the presets differ. The [full scope and release checks](09-roadmap.md#what-counts-toward-core) link the detailed records.

## Battle examples

| Change | What players will notice | Why |
|---|---|---|
| Focus Energy and Dire Hit | They raise the user’s critical-hit chance. Red/Blue can make it lower. | The original effect runs in the wrong direction. Ordinary critical hits keep their Gen 1 rules. |
| Blaine’s Super Potion | Blaine no longer spends a potion use and a turn healing a Pokémon at full HP. | At full HP the item restores nothing. His other item rules stay the same. |
| Damage feedback on two-type targets | The message and sound reflect both types. A weakness and a resistance that cancel give neutral feedback. | Red/Blue can report the effect of only one type even when the damage already accounts for both. |
| Gust and Ghost attacks | Core makes Gust Flying and Ghost attacks strong against Psychic. Minimal keeps the original type data. | The early Japanese guide supports those two changes. [Evidence](../research/core-rule-precedents.md) |
| Disable and Struggle | Core forces Struggle when no enabled move has usable PP, including PP Up cases. | An empty counter can retain upgrade bits. Those bits do not grant extra uses. |
| Thunder and Soul Badges | Thunder boosts Speed. Soul boosts Defense. | This matches what the Gym Leaders tell the player. The original size of the boosts and their stacking rules still apply. |

Minimal includes the feedback correction and retains stock critical-hit, badge and trainer-item outcomes. [Battle evidence and acceptance tests](04-bug-triage.md#battle-calculation-and-trainer-repairs)

## Field moves, storage and team building

| When you… | Minimal and Core | Other developer choices |
|---|---|---|
| Face a cuttable tree, a usable shore or a pushable boulder | Press A and confirm Cut, Surf or Strength if a party member can already use it here. You can still use the party menu. | Keep the manual controls in a custom build. Fly and Flash keep their existing menu commands. |
| Fill the selected box with six Pokémon in the party | Change boxes at a PC before catching another Pokémon. The box chooser shows the highlighted box’s occupancy. | Enable automatic placement to use the next box with room. Enable direct MOVE POKÉMON separately. |
| Leave a first box change without choosing a box | The previous save must stay intact. Stock Red/Blue can mark its inactive boxes empty. | The same protection applies with optional storage features enabled. |
| Forget a move | If Alakazam passes up Recover at level 31, the player cannot simply add it before the next fight. | Add a move relearner, with the location, cost and eligible moves chosen by the author. |

An author can opt into automatic placement or a relearner on any compatible base. The build then has its own rules. [Minimal’s decision criteria](../research/minimal-action-review.md) · [Field eligibility](../research/field-shortcut-contract.md) · [Storage evidence](../research/storage-policy-and-code.md)

## Inspect a move

Highlight a machine in the bag, item PC, shop or prize list. The row identifies both number and move, for example **TM24 Thunderbolt**. Press **START — INFO** to see type, power, listed accuracy, PP and effect. Press **B** to return to the same row. You can also inspect moves from STATS or FIGHT. When a Pokémon with four moves is offered a new one, you can read the new move and compare the old ones before choosing what to forget. Both presets include these controls. [Move INFO and examples](15-battle-information.md)

## Hidden coins at the Game Corner

The Coin Case holds 9,999 coins. In original Red and Blue, finding a hidden pile with the Coin Case credits what fits and marks the whole pile collected. The game reports the size of the pile. If the resulting balance is 9,999, it adds “Oops! Dropped some coins!” It tests the ending balance, so it can give that warning when every coin fit.

| Before finding 10 | Kept | Lost | Original warning | Minimal and Core warning |
|---:|---:|---:|---|---|
| 9,988 | 10 | 0 | No | No |
| 9,989 | 10 | 0 | Yes | No |
| 9,990 | 9 | 1 | Yes | Yes |
| 9,999 | 0 | 10 | Yes | Yes |

Surplus coins cannot be collected on a later visit. Without the Coin Case the pile stays available. The project changes only the false warning in this example. The distinct Core repair for a pile encoded as 40 and the paid clerk’s original transaction have their own records. [Pickup and collection flag](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/events/hidden_items.asm#L52-L132) · [Original text](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/data/text/text_2.asm#L764-L783) · [Paid clerk](../research/game-corner-redemption.md)

## Finding a specific change

| Subject | Maintained record |
|---|---|
| Battle rules, including Ghost against Psychic, Gust, Charizard and retained Gen 1 mechanics | [Mechanics contract](05-mechanics-contract.md) and [case-specific evidence](../research/core-rule-precedents.md) |
| Pokémon, items, field actions, menus, shops, the PC and the playthrough findings | [Playthrough change register](13-playthrough-intake.md) |
| Battle, map, text, audio, display and save defects | [Curated repair register](04-bug-triage.md) and [94 individual catalog decisions](../research/catalog-decisions.md) |
| Additional confirmed faults in the PC and field menus | [Box chooser](../research/box-picker-safety.md) and [Surf refusal](../research/field-shortcut-contract.md) |
| Information and menu changes | [Preset decisions and player effects](../research/sweep-decisions.md) |
| Day Care and prize redemption | [Why Day Care keeps its original rules and dialogue](../research/day-care-history.md) · [Buying Porygon at the Game Corner](../research/game-corner-redemption.md) |
| Developer choices and their limits | [Feature catalog](14-features-and-extensions.md), [tutorial coverage](../research/tutorial-library.md) and [engine changes by size](../research/refactor-scope.md) |

## Recording a change in the game repository

Every difference from upstream needs a record, including intentional preservation of an old result on one path of a shared fix. Give it one home. Reuse an existing playthrough or bug ID. Link the same entry from the release notes and from related fixes. A group of changes can share one entry when it describes every affected behavior explicitly. Before tagging a release, compare it with the preceding release and the upstream baseline. Match each changed rule, default, data set, interface, save format and asset choice to its entry. A code-only refactor can have one technical note covering all affected callers.

Start with what a player does and what happens. State what stock does, which builds change it, and why. Give an example where the difference matters. For a simple typo, the old and corrected wording can be the whole example. For a developer feature, show how to select it once the setting exists. Record the first game release containing the change; until then say planned, tested in a prototype, or implemented as appropriate.

Keep the main entry short. Link the source, the before-and-after check and any remaining uncertainty underneath. Describe save files, link play or other options only where they are affected. For an internal change with identical play, name the shared routine and the comparison that verified the old result. Readers should be able to tell what their players will notice and how to verify it in their own build.
