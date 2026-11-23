# Critical-hit arithmetic audit

The [evidence index](evidence.md#e04) pins the original routine; [E22](evidence.md#e22) pins the Solus implementation. Read the actual routines before selecting a donor correction.

Let `H = floor(base_speed / 2)`. Each threshold below is compared against one rotated random byte. Probability under uniform input is the threshold divided by 256.

| System | Ordinary, unpumped | Ordinary, pumped | High-critical, unpumped | High-critical, pumped |
|---|---|---|---|---|
| Vanilla source | H | floor(H/4) | min(8H,255) | min(4 × floor(H/2),255) |
| Pinned Solus source | floor(H/4) | H | 4 × floor(H/2) | min(8H,255) |
| Selected Core rule | H | min(4H,255) | min(8H,255) | min(32H,255) |

The first two rows are **source-derived**, not sampled game measurements. The third is the selected Core design. A disposable assembly build exercises it below. For Speed values 0–255, Solus's high-critical unpumped threshold cannot exceed 252.

## Selected ordinary-move examples

| Base Speed | Vanilla unpumped | Vanilla pumped | Solus unpumped | Solus pumped | Core pumped |
|---|---:|---:|---:|---:|---:|
| 55 | 27/256 | 6/256 | 6/256 | 27/256 | 108/256 |
| 95 | 47/256 | 11/256 | 11/256 | 47/256 | 188/256 |
| 130 | 65/256 | 16/256 | 16/256 | 65/256 | 255/256 |
| 140 | 70/256 | 17/256 | 17/256 | 70/256 | 255/256 |

These input values alone do not imply obtainable movesets. The comparison demonstrates an engine formula difference: Solus raises its own reduced rate, but does not retain vanilla unpumped rates.

## Jolteon's move access

The pinned English Yellow and Solus learnsets give Eevee Focus Energy at level 36 and a Thunder Stone evolution into Jolteon. Their checked evolution paths keep the existing move record. A player can learn Focus Energy before evolving and keep it. Jolteon's base Speed is 130 in both checked tables. This is a source-supported example, not a played evolution or trade test. [E61](evidence.md#e61)

The pinned Red/Blue Eevee learnset has no Focus Energy entry. The Yellow/Solus finding does not authorize changing the default learnset or claim tested trade interoperability. It also does not validate the older Solus probability example: the checked Solus rates remain 16/256 before Focus and 65/256 after it.

## Why alternative patches need review

The archived wiki's first approach computes a regular threshold from Speed/2 and a high-critical threshold from four times the full Speed before applying Focus. The ordinary unpumped value matches vanilla; odd-Speed high-critical values can differ. Speed 55 gives 220 instead of 216.

Another approach multiplies/caps the full Speed before the ordinary division. If that value caps at 255, dividing afterward gives 127. An apparent ×4 operation is not enough to establish the intended final threshold. Treat the wiki's commentary as a report and its operations as the evidence. [E24](evidence.md#e24)

## Reproduce this table

Run from this specification repository:

```sh
python3 tools/analyze_critical_hits.py
```

It regenerates [critical-hit-thresholds.csv](critical-hit-thresholds.csv) for all 1,024 combinations of Speed byte, high-critical flag and pumped flag. It also checks the rotated-byte comparison across all 256 byte values, computes the count of unpumped differences, and verifies unchanged unpumped rates under the Core rule.

The calculator is an arithmetic model. Its historical column name `proposed_threshold` contains the values now selected for Core.

## Compiled threshold check

A disposable build of each color calculated the stock unpumped threshold first, then applied two doubling steps with saturation only when the pumped bit was set. The original high-critical table and random comparison stayed in place. SameBoy 1.0.5 ran the stock and edited routines for both actors, base Speed 0–255, two move classes (Tackle and Karate Chop) and both pumped states. All 8,192 observed thresholds matched the stock or selected Core model as appropriate. This test starts after the species header read so every possible Speed byte can be supplied. A second check supplied every threshold and random byte to the original three rotations and comparison in each build. All 262,144 comparator cases returned the expected critical flag.

These two checks cover the arithmetic and final decision separately. Test both real ways to enter the pumped state, ordinary damage, protected move eligibility, the combat RNG and link outcomes in the integrated release. [Recorded results and hashes](scope-sweep-checks.json) · [Stock routine](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/core.asm#L4477-L4543)
