# Move cursor, box insertion, and Mansion trainers

Source review checked on **2026-10-24** at the retained English Red/Blue revision. This review does not implement a game feature or claim a runtime test. Reconstructed source comments are not original developer records.

| Finding | Verified behavior | Core disposition |
|---|---|---|
| Move-swap cursor | Both SELECT phases redraw from an older saved move selection. | Retain the current row during the operation. PN-021. |
| New box arrivals | Captures and boxed gifts enter at the front; party deposits enter at the end. | Append new arrivals consistently and keep existing positions stable. PN-022. |
| Mansion trainers | Three Burglars have range zero; three Scientists have ordinary positive ranges. | Correct the Burglars' sight behavior in Core under D39; preserve other settings. PN-023. |

## Battle move swapping

`SwapMovesInMenu` records the source row on the first SELECT. On a later SELECT it swaps the source and destination, including their PP bytes, and updates the disabled-move index. Both paths redraw `MoveSelectionMenu`, which restores the cursor from `wPlayerMoveListIndex`. That index has not been updated by either SELECT path. The cursor therefore returns to an earlier selection, often move one. It is not an unconditional instruction to highlight the first move. [E110](evidence.md#e110)

Retain the current row when marking a move and after completing a swap. For moves three and four, SELECT on three must leave the cursor on three; SELECT on four must complete the swap and leave the cursor on four. Keep the source marker distinct from the cursor. Preserve move/PP data, Disable tracking, A/B behavior, and the restriction on SELECT in link battles. This extends the position-retention principle to a list that does not scroll. See [PN-021](../docs/13-playthrough-intake.md#pn-021).

## Box insertion order

The code uses two different storage paths. `SendNewMonToBox` shifts every existing boxed Pokémon down and writes the newcomer at the front. It also names slot one directly. Captures with a full party and gifts sent to a nonfull box share this routine. Party deposits use `_MoveMon`, which appends instead. [E111](evidence.md#e111)

The source establishes the behavior, but not its original purpose. Showing the newest catch first is a possible benefit; it is not a documented developer explanation. The different paths also do not prove that the inconsistency was an accidental defect.

Select append behavior as a usability policy: new captures and gifts placed in the current box go after its existing members, matching deposits. Existing box positions stay stable. Do not sort or reorder old saved boxes on load. The first empty slot in this packed list is its end; removals still compact the list in order.

Every component of a boxed Pokémon must use the same destination index: species, full record, original-trainer name, and nickname. Fix the nickname prompt's slot-one assumption too. Keep the append-order repair independent of capacity, gift eligibility and save format. D55 keeps manual destination selection by default. Automatic placement is an independent option. This needs no MOVE POKÉMON interface or automatic box switching. See [PN-022](../docs/13-playthrough-intake.md#pn-022).

## Mansion encounter settings

| Floor | Trainer class | View-range setting |
|---|---|---|
| 1F | Scientist | 3 |
| 2F | Burglar | 0 |
| 3F | Burglar | 0 |
| 3F | Scientist | 2 |
| B1F | Burglar | 0 |
| B1F | Scientist | 3 |

The object data identifies the two sprites named Super Nerd in some script labels as the Burglar trainer class. All four maps run the common trainer sight check. A range of zero cannot reach a player at a different position. Talking still starts an undefeated trainer's battle. Scientists can initiate normally when visible, facing the player, aligned, and within range. Defeated trainers do not initiate another battle. [E112](evidence.md#e112)

The original Burglars are configured as talk-to-battle encounters. D39 now selects sight-triggered engagement for these three as a scoped Core correction, treating the passive behavior as a likely oversight. Their original story or design reason remains unverified. Keep the original Scientist settings and other zero-range trainers. See [PN-023](../docs/13-playthrough-intake.md#pn-023).

## How strong is the evidence for intent?

Comparison checked on **2026-10-25** at existing reference pins. A zero range proves the configured behavior. It does not, on its own, prove what the original developers intended. [E113](evidence.md#e113)

| Comparison | Verified setting | What it adds |
|---|---|---|
| Red/Blue Route 6 | The facing Jr. Trainer pair both have range zero. Their dialogue describes a private conversation. | Ordinary talk-triggered encounters are part of the same game; the dialogue fits the arrangement. |
| Red/Blue Route 21 | All four Fishers have range zero and face adjacent water from the edge of land. | Valid zero-range examples, with a fishing context that makes them a weak analogy for the Mansion Burglars. |
| Gold/Silver | Bird Keeper Bryan on Route 35 and Cooltrainer Lois at the Lake of Rage have range zero. | Other Pokémon games also use this setting for ordinary trainers. |
| Yellow Mansion | All three Burglars retain range zero. | Continuity within Gen 1; shared code also makes this compatible with an inherited oversight. |
| FireRed/LeafGreen Mansion | Arnie, Simon, and Lewis are normal trainers with sight range one. | The remake changes the behavior. This could be a later correction or a design change; the data does not say which. |

These comparisons establish that zero range is a valid encounter mechanism. Their local context matters: the Route 21 Fishers face water, and the Route 6 pair are in a private conversation. Neither is direct evidence for the Mansion Burglars' rationale. The Mansion's original intent remains unresolved. Avoid describing the repeated zero values as conclusive intent evidence, or the remake as proof that the originals were wrong. No original developer explanation is established here.

D39/PN-023 explicitly selects a scoped Core correction despite the unresolved historical reason. This product decision is separate from what the source proves. The proposed range-one change follows the remake while preserving other encounter data. No game implementation or runtime result follows from this specification choice.

## Route 21 Fisher geometry

Checked on **2026-10-25** by decoding the retained map blocks and overworld blockset, then inspecting the rendered land patches. All four Fishers face immediately adjacent water. [E114](evidence.md#e114)

| Fisher object | Position | Facing | Square directly ahead |
|---|---|---|---|
| Fisher1 | (4, 24) | Left | (3, 24): water |
| Fisher2 | (6, 25) | Down | (6, 26): shoreline/water |
| Fisher3 | (14, 56) | Left | (13, 56): water |
| Fisher4 | (17, 57) | Right | (18, 57): water |

The [geometry record](route21-fisher-geometry.json) retains coordinates, forward graphic tiles, and source fingerprints. Fisher2 faces a shore lip over water; the other three forward squares are entirely water. This context fits fishing. Their passive behavior is therefore a poor analogy for the Burglars inside the Mansion. It supports the existence of the mechanism, without establishing the Mansion's original rationale. Keep the historical intent unresolved. D39 separately selects a Core correction for the three Burglars; this geometry result neither proves intent nor broadens that scope. No game code is implemented here.
