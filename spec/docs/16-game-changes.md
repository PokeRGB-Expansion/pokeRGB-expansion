# What changes when you play?

Minimal preserves Red/Blue’s battle outcomes and team-building choices. Core also repairs mechanics and adds a few choices for players. Both include the menu, information and display improvements below. [Full scope and release checks](09-roadmap.md#what-counts-toward-core)

## Battle examples

| Change | What players will notice | Why |
|---|---|---|
| Focus Energy and Dire Hit | They raise the user’s critical-hit chance. Red/Blue can make it lower. | The original effect runs in the wrong direction. Ordinary critical hits keep their Gen 1 rules. |
| Blaine’s Super Potion | Blaine no longer spends a potion use and a turn healing a Pokémon at full HP. | At full HP the item restores nothing. His other item rules stay the same. |
| Damage feedback on two-type targets | The message and sound reflect both types. A weakness and a resistance that cancel give neutral feedback. | Red/Blue can report the effect of only one type even when the damage already accounts for both. |
| Gust and Ghost attacks | Core makes Gust Flying and Ghost attacks strong against Psychic. Minimal keeps the original type data. | The early Japanese guide supports those two changes. [Evidence](../research/core-rule-precedents.md) |
| Disable and Struggle | Core forces Struggle when no enabled move has usable PP, including PP Up cases. | An empty counter can retain upgrade bits. Those bits do not grant extra uses. |
| Thunder and Soul Badges | Thunder boosts Speed. Soul boosts Defense. | This matches what the Gym Leaders tell the player. The original size of the boosts and their stacking rules still apply. |

Minimal includes the feedback correction. It keeps the original critical-hit, badge and trainer-item outcomes. A level-one Pokémon on the Medium Slow growth curve also keeps its original experience in Minimal. Core starts it at zero, so a small first award cannot take it straight to level 100. [Battle evidence and acceptance tests](04-bug-triage.md#battle-calculation-and-trainer-repairs)

## Battle displays

In Minimal and Core, a small Poké Ball beside an identified wild opponent means your Pokédex already records that species as owned. Trading for a species counts, and releasing your last copy keeps the mark. It also works on ordinary Safari encounters. A hidden Tower ghost and the Old Man’s demonstration show no ball.

Below your Pokémon’s HP, the EXP bar shows how far it has progressed from its current level to the next. Switching Pokémon changes the bar. A knockout updates it during the existing EXP message. At maximum level the track is empty. [Display rules and author settings](../research/battle-hud-displays.md)

Both presets reserve the final HP-bar pixel for full health. At 258/259 HP you can now see the gap in battle, in the party and in STATS. [HP and level-one experience checks](../../tests/hp_and_level_one.py)

Core also adds **BATTLE PACE** to OPTION. NORMAL is the default. QUICK shortens four pauses in ordinary battles, including the pause when recalling a Pokémon. Music, controls and the game clock keep their normal speed. Link battles, the Safari Zone and catching demonstrations use normal pacing. [Pace checks](../../tests/battle_pace.py)

## Field moves, storage and team building

| When you… | What happens |
|---|---|
| Face a cuttable tree, a usable shore or a pushable boulder | Press A and confirm Cut, Surf or Strength if a party member can use it here. Fly and Flash keep their existing menu commands. |
| Register a Bicycle or a fishing rod from the Bag | Press SELECT in the field to use the registered item. All three rods work. The shortcut follows the same fishing and riding rules as USE. There is one registration slot. |
| Reorder a party of two or more in the field | Press SELECT on one Pokémon, move to the other and confirm. B cancels. The explicit SWITCH command also works. |
| Fill the selected box with six Pokémon in the party | Change boxes at a PC before catching another Pokémon. The box chooser shows how many spaces are occupied. |
| Leave the first box change without choosing a box | Your previous save keeps its party and its stored Pokémon. Retail Red/Blue can mark its inactive boxes empty. |
| Want to forget a move, including an HM | In Core, visit the Move Deleter in the Fuchsia house between the Pokémon Center and Bill’s family. He asks which Pokémon and move, confirms the choice and refuses to remove the last move. Minimal keeps the original HM commitment. |

Passing up Recover at level 31 still matters for Alakazam in both presets. A party-menu Move Reminder, direct moves between boxes and automatic placement of catches are planned extensions. [Field eligibility](../research/field-shortcut-contract.md) · [Storage design](../research/storage-policy-and-code.md) · [Move services](../research/exp-pacing-and-move-services.md)

## Menus and travel

- Press SELECT in the Pokédex to switch from number order to an alphabetical list of species you have seen. A seen species stays selected across the two views. If you started on an unseen number, returning to number order restores that row. Seen-only entries still conceal owned-only data.
- The Bag and item PC show the item and chosen quantity when you confirm TOSS. You can cancel before losing anything.
- In an unlit Rock Tunnel, OPTION is readable and the map is dark again when you close it. On the Town Map, the first directional press advances from Route 1 and the Power Plant.
- In Core, both Cycling Road guards turn you back if you have no Bicycle, even when you hold Left through the warning. Minimal keeps the original gate behavior.

[Field and Town Map checks](../../tests/field_sweep.py) · [Pokédex, TOSS, party and fishing checks](../../tests/field_menu_features.py)

## Protecting EXP. ALL

Oak’s aide gives EXP. ALL once. Both presets refuse to toss or sell it and still let you deposit or withdraw it at the item PC. Core starts with sharing on. Choose USE on EXP. ALL in the field to switch it off or back on. While it is on and in the Bag, Core calculates the participants’ share and the party’s share separately. Minimal uses the original awards whenever the item is in the Bag. [Item protection](13-playthrough-intake.md#pn-001) · [Experience awards](../research/foundation-audit.md#exp-all-gives-too-little-to-a-party-with-multiple-participants)

## Inspect a move

Highlight a machine in the bag, item PC, shop or prize list. The row identifies both number and move, for example **TM24 Thunderbolt**. Press **START — INFO** to see type, power, listed accuracy, PP and effect. Press **B** to return to the same row. You can also inspect moves from STATS or FIGHT. When a Pokémon with four moves is offered a new one, you can read the new move and compare the old ones before choosing what to forget. Move INFO also marks moves with priority or a high critical-hit chance. If Slash is changed in a hack, its label follows that hack’s battle rules. For ordinary supplies, START in the Bag, Mart or item PC shows the item’s effect, such as a Potion’s healing amount. B returns to the same selection. [Move and supply INFO](15-battle-information.md)

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
| Information and menu changes | [Preset decisions and player effects](../research/sweep-decisions.md) and [v0.2.0 findings](../research/v020-feature-sweep.md) |
| Day Care and prize redemption | [Why Day Care keeps its original rules and dialogue](../research/day-care-history.md) · [Buying Porygon at the Game Corner](../research/game-corner-redemption.md) |
| Developer choices and their limits | [Feature catalog](14-features-and-extensions.md), [tutorial coverage](../research/tutorial-library.md) and [engine changes by size](../research/refactor-scope.md) |

## Recording a change in the game repository

Every difference from upstream needs a record, including intentional preservation of an old result on one path of a shared fix. Give it one home. Reuse an existing playthrough or bug ID. Link the same entry from the release notes and from related fixes. A group of changes can share one entry when it describes every affected behavior explicitly. Before tagging a release, compare it with the preceding release and the upstream baseline. Match each changed rule, default, data set, interface, save format and asset choice to its entry. A code-only refactor can have one technical note covering all affected callers.

Start with what a player does and what happens. State what stock does, which builds change it, and why. Give an example where the difference matters. For a simple typo, the old and corrected wording can be the whole example. For a developer feature, show how to select it once the setting exists. Record the first game release containing the change; until then say planned, tested in a prototype, or implemented as appropriate.

Keep the main entry short. Link the source, the before-and-after check and any remaining uncertainty underneath. Describe save files, link play or other options only where they are affected. For an internal change with identical play, name the shared routine and the comparison that verified the old result. Readers should be able to tell what their players will notice and how to verify it in their own build.
