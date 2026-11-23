# Viridian Forest star-grass encounters

Checked on **2026-10-25** at the retained Red/Blue and Yellow revisions. [E115](evidence.md#e115) records source paths, ranges, and fingerprints. The [map audit](forest-encounter-audit.json) records the derived positions.

## Finding

The evidence strongly supports a coding oversight. Red/Blue recognizes grass for encounters by reading the lower-right 8-pixel graphic tile of the player's 16-pixel walking square. Forest grass is tile `0x20`. Some grass squares use decorative star tile `0x34` in that corner and `0x20` at lower-left. They fail the grass comparison, fail the water comparison, and are rejected by the Forest-specific fallback before an encounter roll.

The player sprite code reads the lower-left tile for grass priority, which makes the grass cover the lower part of the sprite. It therefore treats those same squares as grass. This is an internal mismatch between grass display and encounter recognition.

The source map is 17 by 24 blocks. Each block contains four walking squares. It has 365 squares with grass at lower-left: 251 also have grass at lower-right, while 114 have star grass there. The patterned grass block uses a star in the lower-right corner of each of its two right-hand squares. Its 57 placements account for all 114 missed squares. These counts describe static source geometry; other encounter guards still apply.

## Yellow comparison and intent

Yellow changes the encounter gate to read lower-left. Its Viridian Forest map bytes and Forest blockset bytes are identical to Red/Blue's, and its Forest grass ID is still `0x20`. The same squares therefore pass Yellow's grass check. This supports a recognition repair without a map redesign.

No original developer statement was found. The source is a disassembly; its modern labels and comments are not original design notes. The conclusion rests on the instructions, shared map data, and separate sprite behavior. Historical intent is strongly inferred, not documented directly.

## Accepted Core scope

D40/[PN-024](../docs/13-playthrough-intake.md#pn-024) accepts making the affected grass eligible for the existing encounter rule. Retain the map, graphics, species, levels, slot weights, encounter-rate data, Repel rules, and ordinary safe paths. This repairs recognition; it does not select a higher base rate. Walking through the formerly missed squares will have a new chance of battle, which is the selected effect of the accepted repair.

Choose the implementation after reviewing neighboring cases. Yellow's global corner change also changes shore handling, including the separately cataloged Cinnabar case, CAT-027. Do not include that broader change without its own scope and tests. A Forest-specific grass-recognition repair is one narrower candidate. Test all Forest maps, including the Safari Zone, and their water and boundary tiles before accepting it. The archived wiki's suggested code is a lead, not a verified patch.

## Required checks

- Every affected Viridian Forest square passes the grass gate at the existing rate. Ordinary grass and non-grass paths retain their behavior.
- Use controlled random inputs around the encounter threshold. Retain encounter-slot selection, species, levels, Repel handling, and unrelated random-number use.
- Check entry from all directions, map boundaries, doors, warps, scripted movement, and post-battle return.
- Check Forest water, shore, and Safari Zone cases. Any effect outside the selected repair needs an explicit decision.
- Verify Red, Blue, and cosmetic Green. No save format change is proposed.

No game patch or running-game check was performed in this review.
