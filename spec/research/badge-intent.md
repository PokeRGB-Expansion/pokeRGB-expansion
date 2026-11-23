# Badge boosts: shipped behavior and likely intent

The [original Japanese badge dialogue and its relationship to other disputed rules](core-rule-precedents.md) add independent support for the badge mapping below.

Checked **2026-10-14**. The mismatch is already tracked as **RGB-010a**. D25 accepts a Core code correction: Thunder boosts Speed and Soul boosts Defense, matching the original descriptions. This replaces the earlier text-only preservation policy. Badge stacking remains protected.

## What the evidence establishes

| Badge | English Red/Blue dialogue | Original US manual | English Red/Blue calculation | FireRed/LeafGreen calculation |
|---|---|---|---|---|
| Thunder, awarded by Lt. Surge | Speed | Speed | Defense | Speed |
| Soul, awarded by Koga | Defense | Defense | Speed | Defense |

The Red/Blue routine walks the Attack, Defense, Speed, and Special fields in memory, applying bonuses for badge bits 0, 2, 4, and 6. Thunder is bit 2; Soul is bit 4. The instructions and field layout establish the mapping independently of the disassembly's explanatory comments. The gym dialogue and Cerulean badge house say the reverse for Thunder and Soul. [E12](evidence.md#e12), [E42](evidence.md#e42)

Printed page **27** of the original US instruction booklet assigns Speed to Thunder and Defense to Soul. This is PDF page **29**, counting the cover as page 1. The inspected cover identifies the booklet as the Pokémon Trainer's Guide, code `U/DMG-APAE-USA`; the opening page carries Nintendo of America and 1998 copyright information. The linked copy is a third-party scan of that booklet. [E76](evidence.md#e76)

The licensed Prima guide also gives Thunder Speed on printed page 26 and Soul Defense on printed page 47. It could share an information source with the dialogue or manual, so it is not independent evidence of an internal design decision. [E77](evidence.md#e77)

In the checked FireRed/LeafGreen reconstruction, Surge awards badge flag 3, which increases the player's Speed. Koga awards flag 5, which increases the player's Defense. These are calculation paths and award scripts, rather than just remake dialogue. This later mapping agrees with the original English dialogue and manual. It does not establish what was decided during the original 1996 development. [E75](evidence.md#e75)

## Best-supported interpretation

**Inference:** Thunder was likely meant to boost Speed and Soul to boost Defense. The agreement between the original English text, contemporary US manual, and later remake makes a calculation mix-up the stronger explanation.

The memory order offers a plausible cause: a loop that follows Attack, Defense, Speed, Special does not implement the advertised badge order Attack, Speed, Defense, Special. This explains how a swap could arise; it does not prove how it happened.

No interview or authenticated internal design record settling this specific mismatch was found in the searches for this review. English and Japanese searches covered the badge/stat terms and developer interviews. The reviewed [2000 Sugimori interview translation](https://shmuplations.com/pokemon/) contains no explanation of this swap. This is a search limit, not a claim that no relevant record exists. Original Japanese badge text and manuals were not verified here.

## What the reconstructed source can tell us

`pret/pokered` identifies itself as a disassembly and publishes hashes for its matching ROM outputs. `pret/pokefirered` identifies itself as a decompilation with matching output hashes. Neither is presented in these references as an authenticated original Game Freak source archive. No build was run in this review. [E01](evidence.md#e01), [E75](evidence.md#e75)

A matching reconstruction can recover the shipped instructions and data exactly. Original source comments, variable names, and design history are not recovered from ROM bytes. Treat the projects' labels and comments as reconstruction annotations unless a separate source establishes their original provenance. A comment explaining a mismatch is not evidence that the original team recognized it.

## What other ROM hacks do

The checked remote branch heads still match the pinned revisions on 2026-10-14. This is a targeted comparison, not evidence of what most ROM hacks do.

| Project | Checked implementation | Evidence |
|---|---|---|
| PureRGB | Corrects code: Thunder→Speed, Soul→Defense; retains those descriptions | [E78](evidence.md#e78) |
| Shin Lite | Retains Thunder→Defense, Soul→Speed; changes gym and badge-house text | [E79](evidence.md#e79) |
| Solus | Retains the original code/text mismatch; its TODO is a candidate, not an implemented fix | [E80](evidence.md#e80) |
| Solid Red | Retains the original code/text mismatch | [E81](evidence.md#e81) |

These findings come from the calculation and text files, not feature-list wording alone. No donor ROM was built or executed. PureRGB's separate stat helper also changes stacking; it is not a complete donor patch for PokéRGB's narrower repair.

## Project consequence

Core corrects the calculation to Thunder→Speed and Soul→Defense. Keep the original English gym and badge-house descriptions. The original dialogue, original US manual, and FireRed/LeafGreen's changed calculation all point to the descriptions as the original intention. That is the reason for this code correction. Original intent cannot be established with certainty from the available evidence. Another hack's choice does not decide the requirement. See [D25](../docs/01-decisions.md), [RGB-010a](../docs/04-bug-triage.md), and [MC15](../docs/05-mechanics-contract.md).

Keep the 1/8 bonus, integer rounding, 999 cap, Boulder/Volcano assignments, link-battle exclusion, and original stacking. The approved mapping change can alter ordinary single-player turn order and physical damage. [Focused regressions](../docs/07-testing-ci.md#badge-mapping-regression-coverage) must verify that scope before implementation ships.

It is plausible that a hidden numerical mismatch escaped playtesting while the descriptions were read. This review provides no evidence of what the original testers noticed. That hypothesis is not needed to support the accepted correction.
