# Donor review: Solus, Shin, and PureRGB

Checked on 2026-10-12 at the revisions in [source-lock.json](source-lock.json). A claim appearing in documentation is source evidence for what a project says. It does not verify the running implementation or safe integration into PokéRGB.

See the [Gen 1 bug-fix survey](donor-bugfix-survey.md) for a wider project comparison, stock-ROM checks, and Core recommendations.

## Selected findings

| Area | Checked evidence | Consequence for this foundation |
|---|---|---|
| Solus Focus Energy | Actual routine changes unpumped critical thresholds. [E22](evidence.md#e22) | Do not import unchanged; use the exhaustive contract and independent oracle. |
| Shin Lite mechanics | README lists changes to Hyper Beam, accuracy, critical damage, fixed-damage immunities, multi-hit calculations, sleep, trapping, X Accuracy, Rage, AI, and enemy PP. [E23](evidence.md#e23), [E52](evidence.md#e52) | “Lite” does not mean a faithful corrected baseline. Review individual implementations against the mechanics contract. |
| Burn/paralysis versus badges | Vanilla stat paths show penalty reapplication/erasure. Solus's checked stat-up tail retains the opposite-actor penalty calls. The badge guard is separate. [E50](evidence.md#e50) | Track RGB-027 independently; no wholesale stat-system import or incidental badge decision. |
| Solus status medicine | Its feature list claims a repair; the checked status-cure path copies party stats, recalculates modified stats, and calls the badge routine. [E52](evidence.md#e52) | This addresses a different path from RGB-027. Do not describe all status recalculation as fixed or missing. Runtime and neighboring cases still need testing. |
| Badge mapping and descriptions | PureRGB corrects the code; Shin Lite changes the text; Solus and Solid Red retain the mismatch at the checked branch heads. [E78–E81](evidence.md#e78) | D25 accepts Thunder→Speed and Soul→Defense. PureRGB also changes stacking; review only the mapping repair. Solus's TODO is not an implementation. This sample does not establish a community majority. |
| Healing and PP | Source review identifies missing-HP comparisons and Max Ether/Max Elixir's PP metadata test. [E15](evidence.md#e15), [E25](evidence.md#e25) | “Restored amount” and general “Ether/Elixir corruption” are too broad. Use RGB-003/004's precise triggers. |
| Itemfinder | Zero-coordinate exclusion is visible in code; no such coordinate occurs in the pinned hidden-item table. [E51](evidence.md#e51) | Useful expansion boundary; do not claim a reproduced ordinary vanilla failure. |
| Other claimed repairs | README/TODO lists cover Haze, Transform, EXP.ALL, softlocks, HUD, graphics, and audio. [E52](evidence.md#e52) | Leads for individual reproductions and donor diffs. Their listed status is not a passing test. |
| Solo play and remaster features | Solus documents consolidated availability, evolution alternatives, field-move changes, and altered game data. [E33](evidence.md#e33) | Later developer capabilities can reuse ideas. They do not enter the default core. No complete Shin Lite acquisition/evolution audit was performed. |

## Shin Master and Lite differ

The pinned Master branch has a Hyper Beam setting. With `EVENT_8C8` set and the target at zero HP, its checked handler returns before the recharge flag is set. Its Viridian NPC sets that event and describes skipping recharge after a KO. The game text agrees with the code. A README history entry instead says the clause causes recharge after a KO. [E60](evidence.md#e60)

The checked Lite branch has a different path. Its effect list includes Hyper Beam, calls that effect before the fainted-target return on either side, and sets recharge without Master's clause guard. A setting in Master does not establish that it exists in Lite. Record the branch and commit in each donor comparison.

This check covers the KO recharge path. It does not establish complete vanilla behavior for Master's misses, Substitute, sleep, trapping, or other rules. The earlier broad claim that every Shin build must recharge after a KO is too strong; the source-backed Lite finding remains valid.

## PureRGB's checked scope

PureRGB combines presentation and bug work with a substantial game redesign. The checked data contains Ninetales as Fire/Ghost, Golduck as Water/Psychic, Seadra as Water/Dragon, Marowak as Ground/Ghost, and Mr. Mime as Psychic/Ghost. Its move data and names replace Counter with Drain Punch and Razor Wind with Roost, and set Cut to Bug with 70 power. [E57](evidence.md#e57)

The checked battle code chooses physical or special Ghost damage by comparing the attacker's stored base Attack and Special, on both battle sides. Its trapping routine selects two or three turns. These are rule changes beyond corrections to misleading output.

Its feature document offers an NPC that restores selected original Pokémon types, plus several game options. The same document says that versions without its stat, move, learnset, TM, and trainer-party changes will not be offered. Restoring a type therefore does not restore the whole original game. This is a documented scope limit, not a runtime audit of every option.

Review any useful donor routine on its own. Cosmetic variants, retained Gen 1 rules, or an option menu do not make a full donor import compatible with PokéRGB's default contract.

## Review scope

No donor ROM was built or executed in this review. It does not establish that Solus has exactly a given number of unfixed defects or that Shin Lite is safe because its list is longer. Lists can mix corrections, design changes, developer features, and repeated entries.

The starting point remains `pret/pokered`. A game designed for solo completion and a reusable foundation have different default requirements. Selection of a donor fix requires its exact revision, root cause, dependent changes, failing-before/passing-after evidence, and tests for protected neighboring behavior.
