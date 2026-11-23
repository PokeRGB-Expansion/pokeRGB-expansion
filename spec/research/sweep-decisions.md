# What the preset review changes for a player

The following placements are settled for the public Core, the later Minimal preset and the Extended base that inherits Core. The tables keep the player effects and origins of the decisions. The [move INFO contract](../docs/15-battle-information.md) covers every screen and its tests.

## Decisions already in place

| Decision or direction | What it means in play |
|---|---|
| Minimal preserves team strength, available strategies, costs and opponents. Equivalent controls can be shorter. | Pressing A to use Cut, Surf or Strength still needs an eligible party member, the badge and a valid target. Restoring the selected item in the same list saves scrolling. Neither decision implies remembering a cursor after an entirely new visit. |
| Keep manual boxes in both presets. Show the highlighted box’s count in CHANGE BOX and protect the existing save on cancellation (D53–D55). | A player can check room at a PC. With a full party and selected box, an empty box elsewhere still cannot take the catch. A reminder while out catching Pokémon would arrive at a different point in play. |
| Keep the agreed messages, menu repairs and battle changes. | The case-specific PC, STATS, shop, release, elevator, quantity, trade and Flute changes apply to their named actions. Acid Armor restores the picture. Effectiveness feedback and the Tower ghost disguise can change what the player sees in Minimal. Focus Energy, badge mapping and Blaine’s full-HP potion change actual battle outcomes in Core. The new catalog labels for Focus Energy, effectiveness feedback and Blaine (CAT-003/005/018) only reflect the complete Core release. [Playthrough cases](../docs/13-playthrough-intake.md) · [Battle decisions](../docs/01-decisions.md) |
| Allow authors to publish paired editions from one source revision. Ship the complete agreed Core first. | A downstream author can share maps and story while selecting different rosters or mechanics. A wider roster, generated adventure, new difficulty or separate Special stats are all independent of playing reference Core. The specific example, filenames, and build checks are engineering proposals. [Edition comparison](emerald-rogue-builds.md) |
| Preserve the paid coin clerk and Day Care (D60, UC-14/71/72). | A player can still buy Red’s Porygon entirely with cash. The attendant quotes the fee at pickup and a newly learned move displaces slot one when all four are occupied. Neither the extra lesson nor the last-conscious-member warning is a default. [Prize checks](game-corner-redemption.md) · [Day Care](day-care-history.md) |

## Information the playthrough identified

The playthrough introduced machine names and details and visible storage counts. The same rule now covers every TM/HM the game shows a player and every move the player can inspect before learning or using it.

| What the player sees | Player effect | Placement |
|---|---|---|
| Number, name and INFO for a TM or HM in the bag or item PC | A stored machine can be identified without making bag space or withdrawing it. Neither screen teaches the move through INFO. | Minimal and Core |
| Number, name and INFO at a shop or prize counter | Players can compare moves before committing money or coins. In 24 original Red/Blue checkout checks the confirmation showed only the machine number. Prices and prize access stay the same. | Minimal and Core |
| INFO for a known or offered move | Read the effect at STATS or FIGHT. Compare the incoming level-up or TM move with possible replacements before committing a slot. Descriptions follow the current preset. | Minimal and Core |
| Occupied places in the bag, item PC, active box and highlighted box in CHANGE BOX | Count item stacks or individual Pokémon. The active and highlighted boxes can differ. A full list can still have room in a matching item stack. | Minimal and Core |

**Stored TM check.** Six tests in the original English Red and Blue ran the PC withdrawal routine after selecting one stored TM50. With 19 occupied bag slots, withdrawal succeeded. With 20 occupied and no TM50 in the bag, withdrawal failed and the copy stayed in the PC. With 20 occupied and one TM50 already in the bag, withdrawal succeeded and the stack grew to two. Thus a PC label can reveal the name without the inventory rearrangement the original game sometimes requires. The tests exercised transfer and refusal, using the stock ROM hashes and SameBoy 1.0.5. They did not draw a proposed label. [Withdrawal and refusal](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/menus/players_pc.asm#L164-L192)

Sources and test cases cover the original teaching and purchase prompts, all three storage limits, and the remake comparison. [Machine and capacity checks](player-experience-sweep.md#counted-items-and-named-machines) · [Player PC commands](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/menus/players_pc.asm) · [Remake evidence](remake-usability-comparison.md)

## Decisions on the other interface changes

| Feature | What changes for a player | Placement and test |
|---|---|---|
| Show the quantity already carried at a Mart (UC-67) | The player can see they have 102 Balls without backing out and adding two stacks. They may buy fewer. This reveals their own inventory and says nothing about free slots or how many more they can afford. | Minimal and Core. Count bag units across stacks, exclude PC items, and compare the actual price, purchase, refusal and cancellation. |
| Show current/max PP when choosing a move for Ether, Max Ether or PP Up (UC-68) | A player choosing between two depleted moves can see which will benefit more before spending an item or a battle turn. Their own STATS already shows these numbers. A transformed active Pokémon may have different battle moves from its stored party moves. Reading the wrong set could give advice about a move the item never touches. | Minimal and Core. Read the same party member and slot as the item. Test a benched target, Transform, PP Ups, and backing out before the next enemy Counter. PP Up retains its out-of-battle restriction. Elixir has no single-move selection. |
| Say when a catch or gift fills the selected box (UC-69) | The player learns the box is full **before the next encounter**, away from the PC. They can return to town and avoid losing a rare catch. Keeping the cap and the manual switch still leaves a real change to preparation. | Core only. Minimal keeps the original transfer message. Change only a successful transfer from 19 to 20, identify only that box, and add no dialogue or extra confirmation. |
| Remember the Pokédex row after closing and reopening it (UC-70) | Easier to revisit the same entry or compare neighbors. Someone who wants the first entry now starts farther away. This is a fresh visit, distinct from the agreed return to the same list. | Minimal and Core. Remember only the browsing row during the session. A new game or reload starts at the top. Automatic catch entries and the calling menu must keep their own positions and discovery rules. |
| Correct the hidden-coin spill text (UC-73) | At 9,989, finding ten credits all ten but stock reports a spill. At 9,990 only nine fit and the warning is true. Both pickups still set the one-time flag. | Minimal and Core. This was a new finding, not a separate playthrough request. Select the existing correct line. Keep the clerk, amount, cap and flag intact. The Core-only 40-coin amount repair has its own tests. |
| Reduced battle flashing and a shorter low-HP alarm (UC-55) | Changing a flash can hide a wild opponent’s level cue. Stopping the alarm can change when cries and jingles play because the game checks the same flag while waiting for sound. | Two independent author options, off in the reference builds. Keep both originals in the reference games. Test the encounter shapes, hit feedback and sound timing before offering them. |

The paid coin sale and the hidden floor pickup use different rules. The project keeps the original sale. For an unclaimed hidden pile, keep all the coins that fit and use the stock spill line only when the pile exceeds the available space. [Coin examples](../docs/16-game-changes.md#hidden-coins-at-the-game-corner) · [Original pickup checks](final-scope-audit.md) · [Accessibility checks](accessibility-scope.md)

## Earlier repairs reclassified or clarified

These are engineering judgments under the agreed preset rules. An inventory entry or successful prototype alone is not evidence of individual playthrough approval.

| Cases | Player effect and boundary |
|---|---|
| Empty SHIFT question (D43) | With only fainted reserves, there is no legal switch. The ordinary send-out text still identifies the next opponent before the player acts. Both presets skip the empty question. One living reserve, even at 1 HP, keeps it. The two STATS redraws and move-replacement sound also change presentation alone. [Tested next turns](player-experience-sweep.md#skip-a-switch-prompt-that-offers-no-legal-switch) |
| Route 16 sign and Cycling Road on New Game (CAT-032/061) | Reading the same route label from its fourth side saves walking around the sign. It opens no path. A fresh adventure should start independently of the prior save’s forced-bike flag. Both stock tests started the new player walking. The observed defect was the stale restriction bit. Both repairs fit both presets. Continue retains the old adventure’s own state. |
| Itemfinder, collisions and the Tower rival (CAT-038/065/091) | The checked stock hidden-item and passability results match. The Itemfinder correction matters for authors placing an item on a zero coordinate. The Tower reader’s two extra in-map matches are on impassable squares. Stop the invalid reads while preserving actual movement, item range and rival triggers. |
| Slot reels and healing monitor (CAT-054/059) | The routines copy 64 and 16 bytes respectively past their source graphics per transfer. Bound the copies in shared code. Stock graphics within the asset remain intact. A different reel payout or a new monitor blink is outside this repair. Check rendered screens and animation timing. |
| Inventory and save safety (CAT-030/048/093) | Protect adjacent data on a failed insertion and avoid mixing old and new save data after interruption. Minimal preserves legitimate stack and payment outcomes. Core changes valid outcomes only for a proven defect. Check normal saves, box changes and trades before advertising recovery. |
| Trainer text, move bounds and name lookup (CAT-044/049/060) | Stock trainers use matching end-text fields and stock tables stay in range. These issues chiefly affect authors using distinct end speeches, invalid move references or larger tables. They add no trainer lines, moves or names to reference Kanto. |
| Fifteenth map sprite (CAT-075) | A speculative redraw could change an NPC’s movement delay or trainer sight. Keep it on hold until the fault is reproduced. |
| Ghost seen flag and roaming NPCs (CAT-020/039) | The sweep clarified earlier placements. Preventing an unidentified ghost from registering its real species changes later Pokédex access. A wandering NPC’s return step can change when a tile is free. Preserve both stock results in Minimal. Core keeps its existing scoped repairs. |
| Focus Energy algorithm (CAT-003, Q01) | Fixing Focus Energy was an explicit Core decision. The exact rounding and cap order are a documented engineering selection. At base Speed 55 an ordinary move goes from 27/256 to 108/256 after using Focus in Core. Minimal keeps 6/256 after Focus. Unpumped odds stay 27/256 in both. The original developers’ exact preferred formula is unknown. [Arithmetic and compiled checks](critical-hit-analysis.md) |

The archive retains each report’s acceptance tests, including evidence limits where only routine calls or data comparisons have run. [Catalog and measured comparisons](catalog-decisions.md#evidence-from-the-full-preset-review) · [Stock and prototype results](scope-sweep-checks.json)

## What needs a decision

**Every display in this review has a preset decision.** Core implementation can proceed. Layout, integrated game tests and the release checks below remain.

Before publication, settle Green’s actual art and credits, and publish only the save, trade, battle and hardware support that integrated tests establish. The emulator, interface layouts, matching-build tests and interrupted-save design are implementation work. If preserving saves or an original link feature proves incompatible with an accepted change, bring back the specific tradeoff before dropping support. [Open work](../docs/10-open-decisions.md) · [Release requirements](../docs/09-roadmap.md#public-release-checks)
