# Evidence index

Exact repository revisions are in [source-lock.json](source-lock.json). Source review is not runtime verification. Wiki links are mutable; use the recorded wiki Git commit and file hash to recover the reviewed text.

<a id="e01"></a>

## E01 — English reference outputs

**Status:** source-verified. The upstream README identifies English Red/Blue, Blue debug and VC patch hashes.

- [pret/pokered · README.md · lines 1–23](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/README.md#L1-L23)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `84a3c89fc54d7e5bedf8f2c8b61a6c4a9efccde611de2235f626dc43c347d243`.
- [pret/pokered · roms.sha1 · lines 1–5](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/roms.sha1#L1-L5)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `5c1e4c3e2e599c5f5f3e8da150f6c132b55dd209ff824b7ae18fd9c749326350`.

<a id="e02"></a>

## E02 — Build selection and cartridge header

**Status:** source-verified. Targets use separate objects and _RED/_BLUE flags. The header selects MBC3 with RAM/battery.

- [pret/pokered · Makefile · lines 1–25](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/Makefile#L1-L25)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `ae29c23b88a65bc5a734296ebb45cee2e1fb6cba2663e3d29c81e3e1461cfec7`.
- [pret/pokered · Makefile · lines 50–110](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/Makefile#L50-L110)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `ae29c23b88a65bc5a734296ebb45cee2e1fb6cba2663e3d29c81e3e1461cfec7`.
- [pret/pokered · Makefile · lines 150–173](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/Makefile#L150-L173)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `ae29c23b88a65bc5a734296ebb45cee2e1fb6cba2663e3d29c81e3e1461cfec7`.

<a id="e03"></a>

## E03 — Pinned tools and fork CI behavior

**Status:** source-verified. The tool pin is RGBDS 1.0.4. Hash comparison is conditional on repository owner pret; forks build without compare.

- [pret/pokered · .rgbds-version · lines 1–1](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/.rgbds-version#L1-L1)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `d1b77b88f4b9f675a900e4143ac768a21218623cfe1703ca43162388c3271bd6`.
- [pret/pokered · .github/workflows/main.yml · lines 1–102](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/.github/workflows/main.yml#L1-L102)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `34cffd69dc6e573949f1e5b615e63528acb45431b76128c198babd03a451ec94`.

<a id="e04"></a>

## E04 — Critical thresholds

**Status:** source-verified. CriticalHitTest shifts base Speed, branches on GETTING_PUMPED, saturates high-critical shifts, rotates RNG three bits, and compares strictly less than.

- [pret/pokered · engine/battle/core.asm · lines 4478–4543](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L4478-L4543)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.
- [pret/pokered · data/battle/critical_hit_moves.asm · lines 1–6](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/battle/critical_hit_moves.asm#L1-L6)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `9f9c575d73cefa61e7267fc12688ace25c7022a000c3131d939d9546a5412a8b`.

<a id="e05"></a>

## E05 — Original type chart

**Status:** source-verified. The data includes Ghost/Psychic immunity, reciprocal Bug/Poison weaknesses, and no Ice/Fire resistance entry.

- [pret/pokered · data/types/type_matchups.asm · lines 1–79](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/types/type_matchups.asm#L1-L79)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f7f2286029d4fe64c80ed6cc5f5c75ec1f1b8903a9eabd171deab49e23228d39`.

<a id="e06"></a>

## E06 — Original move typings

**Status:** source-verified. Karate Chop, Gust and Sand-Attack use NORMAL in the pinned move table.

- [pret/pokered · data/moves/moves.asm · lines 13–42](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/moves/moves.asm#L13-L42)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `a2cf3e1ec6bf4b5caaeeec974967691c9eb47923d1e7432fb0267ba7d3a5931f`.

<a id="e07"></a>

## E07 — Set-damage path and interrupted invulnerability

**Status:** source-verified. SetDamageEffects skip ordinary damage/type adjustment. Fixed effects set explicit damage later. Charging completion clears invulnerability; interruption can skip that reset.

- [pret/pokered · engine/battle/core.asm · lines 3098–3158](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L3098-L3158)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.
- [pret/pokered · engine/battle/core.asm · lines 4612–4681](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L4612-L4681)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.
- [pret/pokered · engine/battle/core.asm · lines 4731–4801](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L4731-L4801)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.

<a id="e08"></a>

## E08 — Hyper Beam effect dispatch

**Status:** source-verified. After damage, fainted-target return precedes the late effect handler that sets Hyper Beam recharge. Substitute breaking can clear the move effect.

- [pret/pokered · engine/battle/core.asm · lines 3225–3269](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L3225-L3269)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.
- [pret/pokered · engine/battle/effects.asm · lines 1169–1191](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/effects.asm#L1169-L1191)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `6e7650408de33069aae9521473f62a1078697f7b539a3978daa49a0e6df825d3`.
- [pret/pokered · engine/battle/core.asm · lines 4849–4907](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L4849-L4907)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.

<a id="e09"></a>

## E09 — Partial trapping

**Status:** source-verified. Trapping sets a multi-turn state before the hit check; duration uses the documented RNG branches. The main loop suppresses the trapped move.

- [pret/pokered · engine/battle/effects.asm · lines 1080–1107](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/effects.asm#L1080-L1107)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `6e7650408de33069aae9521473f62a1078697f7b539a3978daa49a0e6df825d3`.
- [pret/pokered · engine/battle/core.asm · lines 311–340](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L311-L340)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.
- [pret/pokered · engine/battle/core.asm · lines 3365–3384](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L3365-L3384)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.

<a id="e10"></a>

## E10 — Sleep and freeze flow

**Status:** source-verified. Sleep chooses a nonzero 1-7 counter and waking consumes the move turn. Freeze has no spontaneous thaw path in the status check; burn-effect Fire attacks have a defrost path.

- [pret/pokered · engine/battle/effects.asm · lines 26–71](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/effects.asm#L26-L71)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `6e7650408de33069aae9521473f62a1078697f7b539a3978daa49a0e6df825d3`.
- [pret/pokered · engine/battle/core.asm · lines 3330–3367](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L3330-L3367)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.
- [pret/pokered · engine/battle/effects.asm · lines 312–340](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/effects.asm#L312-L340)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `6e7650408de33069aae9521473f62a1078697f7b539a3978daa49a0e6df825d3`.

<a id="e11"></a>

## E11 — Accuracy and bypasses

**Status:** source-verified. Swift and X Accuracy have distinct bypasses. The scaled threshold is compared with a random byte using a strict less-than test.

- [pret/pokered · engine/battle/core.asm · lines 5240–5260](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L5240-L5260)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.
- [pret/pokered · engine/battle/core.asm · lines 5285–5345](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L5285-L5345)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.

<a id="e12"></a>

## E12 — Badge mapping and link exclusion

**Status:** source-verified. The bonus routine exits for link battles. Even badge bits apply Attack, Defense, Speed and Special bonuses in that order.

- [pret/pokered · engine/battle/core.asm · lines 6454–6505](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L6454-L6505)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.

Field layout and badge-bit assignments rechecked on 2026-10-14: [battle structure](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/macros/ram.asm#L39-L59) and [badge constants](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/constants/ram_constants.asm#L54-L64). Their file fingerprints are recorded in the evidence index.

<a id="e13"></a>

## E13 — Badge reapplication sites

**Status:** source-verified. Stat-up/down paths can reapply badge boosts to every stat; the called routine still excludes link battles.

- [pret/pokered · engine/battle/effects.asm · lines 480–507](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/effects.asm#L480-L507)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `6e7650408de33069aae9521473f62a1078697f7b539a3978daa49a0e6df825d3`.
- [pret/pokered · engine/battle/effects.asm · lines 678–696](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/effects.asm#L678-L696)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `6e7650408de33069aae9521473f62a1078697f7b539a3978daa49a0e6df825d3`.

<a id="e14"></a>

## E14 — Effectiveness output

**Status:** source-verified. Type adjustment overwrites the display multiplier on a matching pair while applying each damage factor. DisplayEffectiveness reads the retained multiplier; sound also uses it.

- [pret/pokered · engine/battle/core.asm · lines 5127–5189](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L5127-L5189)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.
- [pret/pokered · engine/battle/display_effectiveness.asm · lines 1–18](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/display_effectiveness.asm#L1-L18)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `502d2bcf9f7abf45b78173a54abd2feed13e9814978d19818546092ca0bb0752`.
- [pret/pokered · engine/battle/animations.asm · lines 2635–2663](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/animations.asm#L2635-L2663)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `188abd046daf4f1c8482ed5cc541ffa85edf0681b5205f08dea0e1344b017e4b`.

<a id="e15"></a>

## E15 — Healing HP comparison

**Status:** source-verified. The routine ignores the high-byte comparison result and can reject healing for missing HP of 255 or 511.

- [pret/pokered · engine/battle/move_effects/heal.asm · lines 1–24](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/move_effects/heal.asm#L1-L24)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `dc3f6c255c657d43904e427c6ef9e8c10176641d451a26896e9cf4d66f97e87b`.

<a id="e16"></a>

## E16 — Substitute invalid activation and wrong-target lead

**Status:** source-verified. Activation rejects subtraction carry but not exact zero. AttackSubstitute describes self-damage turn swaps and clears the move effect on break.

- [pret/pokered · engine/battle/move_effects/substitute.asm · lines 1–47](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/move_effects/substitute.asm#L1-L47)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `ea5aa29ba72af4b92abaaf02b1673af83c2589111de9db0157aa50240bcd3421`.
- [pret/pokered · engine/battle/core.asm · lines 4849–4907](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L4849-L4907)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.

<a id="e17"></a>

## E17 — Stored IDs and stats

**Status:** source-verified. Box, party and battle structures use one-byte species/move fields and retain unified Special, DVs and stat-experience fields.

- [pret/pokered · macros/ram.asm · lines 7–59](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/macros/ram.asm#L7-L59)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `cfb685afd3d00f3f4ee083014424e185f40250bf508579e007e686117a6b2a30`.
- [pret/pokered · constants/pokemon_constants.asm · lines 1–18](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/constants/pokemon_constants.asm#L1-L18)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `0914f9edb2bb72788d0e7b1e4ae7dedef2bb2f29533363375f8d874fec41e604`.

<a id="e18"></a>

## E18 — Bank tracking

**Status:** source-verified. The bank helpers save/restore a one-byte value and write the ROM-bank register; MBC5 ninth-bit support requires more than a header edit.

- [pret/pokered · home/bankswitch.asm · lines 1–35](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/bankswitch.asm#L1-L35)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `11785e4b177bfef3bc9ba9511b3ae74a75aae9134593f9c534643335a3ffa94e`.

<a id="e19"></a>

## E19 — Game Boy memory windows

**Status:** source-verified. The DMG memory map has 8 KiB each of work/video RAM and 16 KiB ROM windows; CGB banking is shown separately.

- [gbdev/pandocs · src/Memory_Map.md · lines 1–18](https://github.com/gbdev/pandocs/blob/0191af06ac49661587dcde3d57a241a626b8df75/src/Memory_Map.md#L1-L18)
  Revision: `0191af06ac49661587dcde3d57a241a626b8df75`. File SHA-256: `e0985f5404374390963332088251bbf7fea19ca3114dafcc1ec2f06a6123ebb9`.

<a id="e20"></a>

## E20 — MBC5 capacity and registers

**Status:** source-verified. MBC5 maps up to 8 MiB ROM and 128 KiB RAM. The ROM-bank register uses a separate ninth bit; rumble uses a RAM selection bit.

- [gbdev/pandocs · src/MBC5.md · lines 1–61](https://github.com/gbdev/pandocs/blob/0191af06ac49661587dcde3d57a241a626b8df75/src/MBC5.md#L1-L61)
  Revision: `0191af06ac49661587dcde3d57a241a626b8df75`. File SHA-256: `42c3356319009bafd67cc7ba793b263104c5a02399b0f09023439a4ccd1f259c`.

<a id="e21"></a>

## E21 — MBC3 capacity

**Status:** source-verified. Pan Docs documents MBC3 ROM-bank selection and ordinary 2 MiB ROM/32 KiB RAM capacity.

- [gbdev/pandocs · src/MBC3.md · lines 1–53](https://github.com/gbdev/pandocs/blob/0191af06ac49661587dcde3d57a241a626b8df75/src/MBC3.md#L1-L53)
  Revision: `0191af06ac49661587dcde3d57a241a626b8df75`. File SHA-256: `3537e900afd71d7377a3c9585e3672d1538bf25e35ef1b708c6d0c3079d1c105`.

<a id="e22"></a>

## E22 — Solus critical-hit donor mismatch

**Status:** source-verified. The checked routine halves an already-halved Speed on the unpumped path, then divides ordinary moves again; this lowers unpumped rates.

- [Dechrissen/poke-solus-rgb · engine/battle/core.asm · lines 4630–4699](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/engine/battle/core.asm#L4630-L4699)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `e594a5249813e75e609be18d60193d7d64e72e56d3cc08057a832f0c37b31e46`.

<a id="e23"></a>

## E23 — Shin Lite behavior changes

**Status:** source-verified. The donor lists changes to accuracy, critical damage, fixed-damage immunities, Hyper Beam, AI and other mechanics. Its name alone does not imply baseline compatibility.

- [jojobear13/shinpokered · README.md · lines 143–241](https://github.com/jojobear13/shinpokered/blob/b35c2a536a1605841c8fb662aad18b0dbfd2a900/README.md#L143-L241)
  Revision: `b35c2a536a1605841c8fb662aad18b0dbfd2a900`. File SHA-256: `7bd63bcd79280856c607980cc9f2f305350c795033f8b4c042ec64f5f935e8d9`.

<a id="e24"></a>

## E24 — Archived catalog and alternative critical patches

**Status:** reported / source-review of patch text. The catalog is expressly unvetted. Its Focus alternatives have distinct rounding/cap order and are candidate patches rather than approved specifications.

- [pret/pokered.wiki · [ARCHIVED]-Bugs-and-Glitches.md · lines 1–15](https://github.com/pret/pokered/wiki/%5BARCHIVED%5D-Bugs-and-Glitches)
  Revision: `727fc7788550c4b279501c17ee177681f7366077`. File SHA-256: `377b09bedf6cc8905ef254a329d02d367ed5f1ad07cfd400f1f3d87212fbda29`.
- [pret/pokered.wiki · [ARCHIVED]-Bugs-and-Glitches.md · lines 171–331](https://github.com/pret/pokered/wiki/%5BARCHIVED%5D-Bugs-and-Glitches)
  Revision: `727fc7788550c4b279501c17ee177681f7366077`. File SHA-256: `377b09bedf6cc8905ef254a329d02d367ed5f1ad07cfd400f1f3d87212fbda29`.

<a id="e25"></a>

## E25 — Full PP-restore comparison

**Status:** source-verified. Max Ether/Max Elixir compare stored PP without masking the upper PP Up bits when checking no effect.

- [pret/pokered · engine/items/item_effects.asm · lines 2045–2088](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L2045-L2088)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.

<a id="e26"></a>

## E26 — Multi-level move learning

**Status:** source-verified. Battle experience assigns the final level and calls the learn routine once; that routine matches the current level exactly.

- [pret/pokered · engine/battle/experience.asm · lines 155–174](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/experience.asm#L155-L174)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `a78649d30822cf9735a1669f29c82115099d450810796a6716b30a9a699259af`.
- [pret/pokered · engine/battle/experience.asm · lines 251–265](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/experience.asm#L251-L265)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `a78649d30822cf9735a1669f29c82115099d450810796a6716b30a9a699259af`.
- [pret/pokered · engine/pokemon/evos_moves.asm · lines 323–351](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/evos_moves.asm#L323-L351)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `b54c8d1fd73c332e75406882a52a0762ce630256f27cf1434c75a0831f2b3f24`.

<a id="e27"></a>

## E27 — Bide asymmetric damage reset

**Status:** source-verified. Enemy-faint cleanup clears only the high byte; the source explains why link endpoints can disagree.

- [pret/pokered · engine/battle/core.asm · lines 741–762](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L741-L762)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.

<a id="e28"></a>

## E28 — Psywave rejection ranges

**Status:** source-verified. The player loop rejects zero while the enemy loop accepts it, changing results and RNG consumption.

- [pret/pokered · engine/battle/core.asm · lines 4657–4681](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L4657-L4681)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.
- [pret/pokered · engine/battle/core.asm · lines 4776–4801](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L4776-L4801)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.

<a id="e29"></a>

## E29 — Medicine stat rebuild

**Status:** source-verified. Status cure copies party stats to battle stats and calls DoubleOrHalveSelectedStats instead of reapplying ordinary stage calculations.

- [pret/pokered · engine/items/item_effects.asm · lines 898–917](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L898-L917)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.

<a id="e30"></a>

## E30 — Inventory splitting lead

**Status:** source path identified / reported consequence. A full-stack split returns to the inventory scan before a terminator check; the catalog proposes a narrower loop target. Memory corruption still needs a runtime trace.

- [pret/pokered · engine/items/inventory.asm · lines 7–103](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/inventory.asm#L7-L103)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `410632e0a82e3491fd6d2898c337eb4a8e83ce6a1b31dad0a12bf887a27a3f7e`.
- [pret/pokered.wiki · [ARCHIVED]-Bugs-and-Glitches.md · lines 1012–1047](https://github.com/pret/pokered/wiki/%5BARCHIVED%5D-Bugs-and-Glitches)
  Revision: `727fc7788550c4b279501c17ee177681f7366077`. File SHA-256: `377b09bedf6cc8905ef254a329d02d367ed5f1ad07cfd400f1f3d87212fbda29`.

<a id="e31"></a>

## E31 — GetName list dispatch

**Status:** source-verified. GetName selects TM/HM names before checking the name-list type, with assertions documenting current limits.

- [pret/pokered · home/names2.asm · lines 11–42](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/names2.asm#L11-L42)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `cf3079bae91aa90c0e83cca17015b989abdcd31d5b38c8c34192a68efb465e63`.

<a id="e32"></a>

## E32 — Partial-save report

**Status:** reported; proposed patch not runtime-verified. The catalog reports interrupted-save corruption and suggests delaying the write. It does not establish transactional recovery.

- [pret/pokered.wiki · [ARCHIVED]-Bugs-and-Glitches.md · lines 3164–3181](https://github.com/pret/pokered/wiki/%5BARCHIVED%5D-Bugs-and-Glitches)
  Revision: `727fc7788550c4b279501c17ee177681f7366077`. File SHA-256: `377b09bedf6cc8905ef254a329d02d367ed5f1ad07cfd400f1f3d87212fbda29`.

<a id="e33"></a>

## E33 — Solus variant and design scope

**Status:** source-verified. Solus states cosmetic RGB differences and describes gameplay consolidation and changed types/move typings; the source critique of Focus is separate.

- [Dechrissen/poke-solus-rgb · README.md · lines 45–54](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/README.md#L45-L54)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `c267f54742a9b9661efc3cd577f1b058b6e4d1347de874cc31a8b02eb2f85fed`.
- [Dechrissen/poke-solus-rgb · docs/FEATURES.md · lines 117–136](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/docs/FEATURES.md#L117-L136)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `c0707122d9e9952f6303ad205057690805e73c7a84fa2a6a33223fd6197b5907`.
- [Dechrissen/poke-solus-rgb · docs/FEATURES.md · lines 239–254](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/docs/FEATURES.md#L239-L254)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `c0707122d9e9952f6303ad205057690805e73c7a84fa2a6a33223fd6197b5907`.

<a id="e34"></a>

## E34 — PureRGB variant scope

**Status:** source-verified. PureRGB states cosmetic variant differences and availability of all 151; its README also describes broader gameplay/data changes.

- [Vortyne/pureRGB · FEATURES.md · lines 1–7](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/FEATURES.md#L1-L7)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `188a80502ad92b3f4201cfbd3c8a840c1a23e8ddab03770cc572df4b570da271`.
- [Vortyne/pureRGB · README.md · lines 1–33](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/README.md#L1-L33)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `45fae9594f30802f868237baf8e4dcb9053dab44ec75b3601fe5390c89c4632f`.

<a id="e35"></a>

## E35 — Expansion role and capabilities

**Status:** source-verified. RHH describes a developer base, lists modern systems, and asks users to credit RHH/contributors. These are not Game Boy implementations.

- [rh-hideout/pokeemerald-expansion · README.md · lines 7–28](https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/README.md#L7-L28)
  Revision: `7b4344c7ee867c98c8fb9d6026791df4f8eaecf7`. File SHA-256: `d582524c553dcc66c4dcb37dd02c6e1d639ff794aa7c90f4110f99857fe0d5eb`.
- [rh-hideout/pokeemerald-expansion · FEATURES.md · lines 15–43](https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/FEATURES.md#L15-L43)
  Revision: `7b4344c7ee867c98c8fb9d6026791df4f8eaecf7`. File SHA-256: `8bf44e2b6a01f00cb31450284f80784f618001117531eeecb588732b3d7c4774`.

<a id="e36"></a>

## E36 — Expansion configuration example

**Status:** source-verified. The Pokémon configuration has distinct choices for updated types, stats, abilities and learnsets.

- [rh-hideout/pokeemerald-expansion · include/config/pokemon.h · lines 1–24](https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/include/config/pokemon.h#L1-L24)
  Revision: `7b4344c7ee867c98c8fb9d6026791df4f8eaecf7`. File SHA-256: `e476277d082276ac078452c44482cf9b3b6fb076159fe4745f0774bc276b85ba`.

<a id="e37"></a>

## E37 — Expansion testing example

**Status:** source-verified. The donor has compiled battle tests for Focus Energy and a test runner; this is design inspiration, not proof of all feature combinations.

- [rh-hideout/pokeemerald-expansion · test/battle/move_effect/focus_energy.c · lines 1–90](https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/test/battle/move_effect/focus_energy.c#L1-L90)
  Revision: `7b4344c7ee867c98c8fb9d6026791df4f8eaecf7`. File SHA-256: `67e077671ad1ec936ab89eb2fd0de6f6de4f0127be000a006a55bc840885db98`.
- [rh-hideout/pokeemerald-expansion · test/test_runner.c · lines 1–35](https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/test/test_runner.c#L1-L35)
  Revision: `7b4344c7ee867c98c8fb9d6026791df4f8eaecf7`. File SHA-256: `a4831705ddde43b4bcb2e2b14c93d354a41a201dd95e169398810b09363e670d`.

<a id="e38"></a>

## E38 — Repository notice inventory

**Status:** tracked-tree observation. The source lock records tracked notice files. No checked game repository has a root file matching LICENSE/COPYING/NOTICE; Expansion has several tool-level files.

- [Tracked notice-file inventory](source-lock.json). Inspect notices before making a rights claim; a root-file check is not a complete license audit.

<a id="e39"></a>

## E39 — Heart & Soul foundation

**Status:** source-verified. The developer README identifies the Expansion base and states that pre-2.0 saves are incompatible.

- [PokemonHnS-Development/pokehns-expansion · README.md · lines 9–20](https://github.com/PokemonHnS-Development/pokehns-expansion/blob/167aa6d537b109bb229c231ddce4616974c4da71/README.md#L9-L20)
  Revision: `167aa6d537b109bb229c231ddce4616974c4da71`. File SHA-256: `e7cbe665ac3e3fb4cc2a40df0c606d01fb4e3390f101dadea83c3692e3b3f391`.

<a id="e40"></a>

## E40 — Official Japanese Blue date

**Status:** official page verified. The official product page records October 15, 1996 as the release date. A first-delivery date was not established.

- [Primary reference](https://www.pokemon.co.jp/game/other/gb-blue/) — checked 2026-10-11.

<a id="e41"></a>

## E41 — Radical Red remake announcement

**Status:** developer announcement; completion unverified. The announcement says the game is being remade on Expansion with incompatible saves and was far from release; it does not prove a completed migration.

- [Primary reference](https://www.reddit.com/r/pokemonradicalred/comments/1uc1hof/huge_update_on_radical_red_from_yours_truly/) — checked 2026-10-11.

<a id="e42"></a>

## E42 — Badge dialogue mismatch

**Status:** source-verified. Surge/Thunder text names Speed and Koga/Soul text names Defense; the badge house repeats these claims, opposite to the code mapping.

- [pret/pokered · text/VermilionGym_2.asm · lines 13–21](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/text/VermilionGym_2.asm#L13-L21)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `4124c8f028bdba194822cb4ab35b3a3eb0d26abe178d2a18fb6ae3d878a0c709`.
- [pret/pokered · text/FuchsiaGym_2.asm · lines 12–21](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/text/FuchsiaGym_2.asm#L12-L21)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `7dc8feb3e895161b0fe1a13845905a7d994676e5764dde1dac80e51db75bea14`.
- [pret/pokered · text/CeruleanBadgeHouse.asm · lines 48–77](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/text/CeruleanBadgeHouse.asm#L48-L77)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `ee0aa7e0a723efcba8f78991d253c4db7f3eb780df84ad73fded4d1989262f35`.

<a id="e43"></a>

## E43 — Focus Energy and Dire Hit state

**Status:** source-verified. Focus Energy and the Dire Hit item both set GETTING_PUMPED in battle state.

- [pret/pokered · engine/battle/move_effects/focus_energy.asm · lines 1–17](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/move_effects/focus_energy.asm#L1-L17)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `28effca9c9702dd5ee7a854612f1fc8e212dae5a2e5a9a662cdfeda316e57d29`.
- [pret/pokered · engine/items/item_effects.asm · lines 1622–1641](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L1622-L1641)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.

<a id="e44"></a>

## E44 — Original critical damage selection

**Status:** source-verified. Critical hits restore unmodified attack/defense and double the level input; preserve that treatment instead of importing donor formula changes.

- [pret/pokered · engine/battle/core.asm · lines 4031–4135](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L4031-L4135)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.

<a id="e45"></a>

## E45 — Toxic and residual damage

**Status:** source-verified. The poison/burn/seed residual flow uses the badly-poisoned counter; preserve the original combined behavior pending separately identified invalid states.

- [pret/pokered · engine/battle/core.asm · lines 470–619](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L470-L619)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.

<a id="e46"></a>

## E46 — AI effectiveness distinction

**Status:** source-verified. AIGetTypeEffectiveness is a separate routine; it initializes to hexadecimal 10 and returns one matching entry. A display fix must not accidentally modernize it.

- [pret/pokered · engine/battle/core.asm · lines 5190–5232](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L5190-L5232)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.

<a id="e47"></a>

## E47 — Transformed capture species

**Status:** source-verified. Capture logic replaces a transformed wild species with Ditto; the comment notes the Metronome Transform path.

- [pret/pokered · engine/items/item_effects.asm · lines 466–483](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L466-L483)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.

<a id="e48"></a>

## E48 — GetName dependent menu repair

**Status:** reported patch dependency. The archived patch notes a subsequent bag-menu crash unless the name-list state is also reset.

- [pret/pokered.wiki · [ARCHIVED]-Bugs-and-Glitches.md · lines 2027–2070](https://github.com/pret/pokered/wiki/%5BARCHIVED%5D-Bugs-and-Glitches)
  Revision: `727fc7788550c4b279501c17ee177681f7366077`. File SHA-256: `377b09bedf6cc8905ef254a329d02d367ed5f1ad07cfd400f1f3d87212fbda29`.

<a id="e49"></a>

## E49 — Secondary effects and repeated-hit calculation

**Status:** source-verified. The secondary-effect routine exits for matching move/target types, including Body Slam versus Normal. Multi-hit moves reuse the first hit calculation.

- [pret/pokered · engine/battle/effects.asm · lines 194–278](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/effects.asm#L194-L278)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `6e7650408de33069aae9521473f62a1078697f7b539a3978daa49a0e6df825d3`.
- [pret/pokered · engine/battle/core.asm · lines 3244–3262](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L3244-L3262)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.


<a id="e50"></a>

## E50 — Burn/paralysis stat recalculation paths

**Status:** source-verified paths; runtime reproduction pending. Stat-up recalculation can erase its own status penalty and reapply the opposite actor’s penalty. Stat-down paths also reapply penalties. Badge link exclusion is separate. Solus retains the checked stat-up tail.

- [pokered · engine/battle/effects.asm · lines 351–444](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/effects.asm#L351-L444)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `6e7650408de33069aae9521473f62a1078697f7b539a3978daa49a0e6df825d3`.
- [pokered · engine/battle/effects.asm · lines 495–506](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/effects.asm#L495-L506)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `6e7650408de33069aae9521473f62a1078697f7b539a3978daa49a0e6df825d3`.
- [pokered · engine/battle/effects.asm · lines 633–698](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/effects.asm#L633-L698)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `6e7650408de33069aae9521473f62a1078697f7b539a3978daa49a0e6df825d3`.
- [pokered · engine/battle/core.asm · lines 6283–6363](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L6283-L6363)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.
- [solus · engine/battle/effects.asm · lines 492–504](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/engine/battle/effects.asm#L492-L504)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `9e41db3a42c188c27538b05ce75c5df113e6863a8e7df9a9dbcd552cc7f78035`.


<a id="e51"></a>

## E51 — Itemfinder zero-coordinate exclusion and reference data

**Status:** source-verified conditional defect; vanilla reachability unproven. The clamped lower bound excludes a hidden item at coordinate zero. None of the 54 pinned coordinate entries uses zero. The catalog’s report is conditional, not proof of a normal-play trigger.

- [pokered · engine/items/itemfinder.asm · lines 1–52](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/itemfinder.asm#L1-L52)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `d487555fd8534d86bad79c8138781a601df052cfefd2323a552019f6061b0090`.
- [pokered · data/events/hidden_item_coords.asm · lines 1–63](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/events/hidden_item_coords.asm#L1-L63)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `baa4d7c094c5d1b00d9971b130d93e6d89915299b4f3d2fcf2bc1d8ca6018ea4`.
- [pokered-wiki · [ARCHIVED]-Bugs-and-Glitches.md · lines 1350–1392](https://github.com/pret/pokered.wiki/blob/727fc7788550c4b279501c17ee177681f7366077/[ARCHIVED]-Bugs-and-Glitches.md#L1350-L1392)
  Revision: `727fc7788550c4b279501c17ee177681f7366077`. File SHA-256: `377b09bedf6cc8905ef254a329d02d367ed5f1ad07cfd400f1f3d87212fbda29`.


<a id="e52"></a>

## E52 — Donor documentation and distinct medicine path

**Status:** documentation verified; selected code path checked. Solus lists three battle repairs, proposes a badge swap in TODO, and rebuilds stages in its checked status-cure path. Shin Lite documents broad rule changes. These observations do not certify every listed implementation.

- [solus · docs/FEATURES.md · lines 350–365](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/docs/FEATURES.md#L350-L365)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `c0707122d9e9952f6303ad205057690805e73c7a84fa2a6a33223fd6197b5907`.
- [solus · TODO.md · lines 193–200](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/TODO.md#L193-L200)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `de7e89e25da89461dd59af21b308d59a258ed32392ac7dd80a573bb597512071`.
- [solus · TODO.md · lines 293–326](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/TODO.md#L293-L326)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `de7e89e25da89461dd59af21b308d59a258ed32392ac7dd80a573bb597512071`.
- [solus · engine/items/item_effects.asm · lines 895–916](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/engine/items/item_effects.asm#L895-L916)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `f046383a7a9b623680ad99756d05c10eb755ea395083025d6578f8e7af3af591`.
- [shin-lite · README.md · lines 534–543](https://github.com/jojobear13/shinpokered/blob/b35c2a536a1605841c8fb662aad18b0dbfd2a900/README.md#L534-L543)
  Revision: `b35c2a536a1605841c8fb662aad18b0dbfd2a900`. File SHA-256: `7bd63bcd79280856c607980cc9f2f305350c795033f8b4c042ec64f5f935e8d9`.
- [shin-lite · README.md · lines 573–606](https://github.com/jojobear13/shinpokered/blob/b35c2a536a1605841c8fb662aad18b0dbfd2a900/README.md#L573-L606)
  Revision: `b35c2a536a1605841c8fb662aad18b0dbfd2a900`. File SHA-256: `7bd63bcd79280856c607980cc9f2f305350c795033f8b4c042ec64f5f935e8d9`.


- [shin-lite · README.md · lines 241–362](https://github.com/jojobear13/shinpokered/blob/b35c2a536a1605841c8fb662aad18b0dbfd2a900/README.md#L241-L362)
  Revision: `b35c2a536a1605841c8fb662aad18b0dbfd2a900`. File SHA-256: `7bd63bcd79280856c607980cc9f2f305350c795033f8b4c042ec64f5f935e8d9`.

<a id="e53"></a>

## E53 — Prima guide publication and Sabrina advice

**Status:** scan visually verified; design intent unresolved. The cover bears a Nintendo licensing seal and the publication page a 1998 copyright. Printed page 39 recommends Bug/Ghost Pokémon; it does not specify a Ghost attack multiplier.

- [Archived guide scan](https://archive.org/download/PokemonOfficialPrimaStrategyGuide/Pokemon%20Official%20Prima%20Strategy%20Guide_text.pdf)
  Checked: 2026-10-12. PDF pages (one-based): 1, 2, 42. Relevant printed page: 39.
  Downloaded PDF SHA-256: `b6163bb943f68abb4247221103ee785079ae108e17a65977d6331d651c350dfd`. The scan is not included in the package.


<a id="e54"></a>

## E54 — Nintendo Power advice checked against game code

**Status:** scan and source verified. Printed page 41 incorrectly says Dream Eater induces sleep and omits Haunter’s trade requirement. The checked game requires a sleeping target and uses trade evolution.

- [Archived guide scan](https://archive.org/download/NintendoPower1998PokemonRedBlue/%28Nintendo%20Power%201998%29%20-%20Pokemon%20Red%20%26%20Blue.pdf)
  Checked: 2026-10-12. PDF pages (one-based): 43. Relevant printed page: 41.
  Downloaded PDF SHA-256: `b2170223366d34499c2876963bcf761f543b642a76e2b9d25adc53cd3866a789`. The scan is not included in the package.
- [pokered · engine/battle/core.asm · lines 5230–5247](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L5230-L5247)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.
- [pokered · data/pokemon/evos_moves.asm · lines 1694–1701](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/pokemon/evos_moves.asm#L1694-L1701)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `1a4c475c47134440a4a4e54265314638d8c6953da558d7d6a7b7f7bc206c2f30`.
- [pokered · data/moves/moves.asm · lines 151–151](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/moves/moves.asm#L151-L151)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `a2cf3e1ec6bf4b5caaeeec974967691c9eb47923d1e7432fb0267ba7d3a5931f`.


<a id="e55"></a>

## E55 — Official Stadium interoperability descriptions

**Status:** official descriptions verified; no modified-game test. Official descriptions confirm RBY Pokémon transfer through the Transfer Pak and playing the Game Boy games on a TV. They do not establish why a type chart was retained.

- [Official description](https://www.pokemon.com/uk/pokemon-video-games/pokemon-stadium/) — checked 2026-10-12.
- [Official description](https://www.nintendo.com/en-gb/Games/Nintendo-64/Pokemon-Stadium-269679.html) — checked 2026-10-12.


<a id="e56"></a>

## E56 — OHKO Speed gate and X Accuracy boundary

**Status:** source-verified; runtime fixtures pending. The OHKO routine rejects a slower user and accepts equal or greater current Speed. It runs before the hit test. X Accuracy skips the ordinary accuracy roll without clearing the Speed failure.

- [pokered · engine/battle/move_effects/one_hit_ko.asm · lines 1–38](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/move_effects/one_hit_ko.asm#L1-L38)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `3a68e62784b992f4e1b0c20bbf5e29f1c6ccce9373f7f3711627886507f89e5c`.
- [pokered · engine/battle/core.asm · lines 3135–3158](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L3135-L3158)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.
- [pokered · engine/battle/core.asm · lines 4323–4335](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L4323-L4335)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.
- [pokered · engine/battle/core.asm · lines 4467–4471](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L4467-L4471)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.
- [pokered · engine/battle/core.asm · lines 5287–5312](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L5287-L5312)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.

<a id="e57"></a>

## E57 — PureRGB redesign examples and configuration limits

**Status:** selected source and documentation verified; no runtime audit. Selected species data uses changed types. Move data and names replace Counter/Razor Wind with Drain Punch/Roost and give Cut Bug type with 70 power. Ghost damage selection compares stored base Attack and Special on both sides; trapping selects two or three turns. Documentation offers type restoration while retaining broader stat, move, learnset, TM, and trainer changes.

- [Vortyne/pureRGB · FEATURES.md · lines 465–535](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/FEATURES.md#L465-L535)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `188a80502ad92b3f4201cfbd3c8a840c1a23e8ddab03770cc572df4b570da271`.
- [Vortyne/pureRGB · FEATURES.md · lines 589–597](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/FEATURES.md#L589-L597)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `188a80502ad92b3f4201cfbd3c8a840c1a23e8ddab03770cc572df4b570da271`.
- [Vortyne/pureRGB · data/pokemon/base_stats/ninetales.asm · lines 1–6](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/data/pokemon/base_stats/ninetales.asm#L1-L6)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `9f47b44ec8163e7859e660a784a3f17c9c26c5a1a597ddfb7921286cf222e242`.
- [Vortyne/pureRGB · data/pokemon/base_stats/golduck.asm · lines 1–6](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/data/pokemon/base_stats/golduck.asm#L1-L6)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `a8aebcd8cc711e7989e32ce0a7a436eb98c8e678f4fed1364903de2ed3e75e5f`.
- [Vortyne/pureRGB · data/pokemon/base_stats/seadra.asm · lines 1–6](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/data/pokemon/base_stats/seadra.asm#L1-L6)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `77a74ca1b9f69e8b6de52c82c6fcc62de0d5ead966a63faf019f7005e5199ce8`.
- [Vortyne/pureRGB · data/pokemon/base_stats/marowak.asm · lines 1–6](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/data/pokemon/base_stats/marowak.asm#L1-L6)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `05d0e1550a4ab298687e687dd99891958141f60b992e8fbceca9f0d94f30111c`.
- [Vortyne/pureRGB · data/pokemon/base_stats/mrmime.asm · lines 1–6](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/data/pokemon/base_stats/mrmime.asm#L1-L6)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `8bea595d8469b4e97176caed2ccfa4cc3f5d36106aad09a9482653f8728552e9`.
- [Vortyne/pureRGB · data/moves/moves.asm · lines 28–31](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/data/moves/moves.asm#L28-L31)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `78a0a52a4ae690370689d983cace600bda94f2f6b03968e14df6217e60ddc5e0`.
- [Vortyne/pureRGB · data/moves/moves.asm · lines 83–83](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/data/moves/moves.asm#L83-L83)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `78a0a52a4ae690370689d983cace600bda94f2f6b03968e14df6217e60ddc5e0`.
- [Vortyne/pureRGB · data/moves/names.asm · lines 195–197](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/data/moves/names.asm#L195-L197)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `c843263293cf872dc50ba0509087de15a326c5883e4501444a9f4c15847e41f2`.
- [Vortyne/pureRGB · data/moves/names.asm · lines 306–307](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/data/moves/names.asm#L306-L307)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `c843263293cf872dc50ba0509087de15a326c5883e4501444a9f4c15847e41f2`.
- [Vortyne/pureRGB · engine/battle/core.asm · lines 4260–4285](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/engine/battle/core.asm#L4260-L4285)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `a58c9db113890c70e7928672559ab35520993d9cbf43a304d719730da742bd68`.
- [Vortyne/pureRGB · engine/battle/core.asm · lines 4387–4412](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/engine/battle/core.asm#L4387-L4412)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `a58c9db113890c70e7928672559ab35520993d9cbf43a304d719730da742bd68`.
- [Vortyne/pureRGB · engine/battle/effects.asm · lines 1264–1279](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/engine/battle/effects.asm#L1264-L1279)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `c7f43426497436a1d9a0032b53237d91ffca7e7e72b414a05eee503c4a76b45f`.

<a id="e58"></a>

## E58 — Convenience changes as a game-design question

**Status:** primary opinion essay checked; project application is a design proposal. Kayin argues that convenience features can change encouraged behavior and rewarded choices. This informs feature review, not proof of a Gen 1 defect, developer intent, or measured player response.

- [Kayin · Quality of Life](https://kayin.moe/quality-of-life)
  Published: 2025-01-18. Checked: 2026-10-12. Source: author opinion essay.

<a id="e59"></a>

## E59 — Stadium move descriptions in pret text notes

**Status:** repository text notes verified; executable mechanics unverified. Ordered Stadium 1 text notes describe Night Shade as ignoring target type and Karate Chop/Gust as Normal. The source is an oldnotes extraction record, not a compiled-engine check or evidence of internal design intent.

- [pret/pokestadium · README.md · lines 1–8](https://github.com/pret/pokestadium/blob/6995f32445e344c03f9b0c774eabcd157559f867/README.md#L1-L8)
  Revision: `6995f32445e344c03f9b0c774eabcd157559f867`. File SHA-256: `26debed7f38ed1b630fb6a160c7e13e7de3a96598c9c58d2e2abe528bb0682b9`.
- [pret/pokestadium · oldnotes/stadium1/text/moves.txt · lines 1–33](https://github.com/pret/pokestadium/blob/6995f32445e344c03f9b0c774eabcd157559f867/oldnotes/stadium1/text/moves.txt#L1-L33)
  Revision: `6995f32445e344c03f9b0c774eabcd157559f867`. File SHA-256: `efdddafcdb7bda61220fa821f7435714e4fe5385cb8050b20e01fe8c174735a4`.
- [pret/pokestadium · oldnotes/stadium1/text/moves.txt · lines 197–203](https://github.com/pret/pokestadium/blob/6995f32445e344c03f9b0c774eabcd157559f867/oldnotes/stadium1/text/moves.txt#L197-L203)
  Revision: `6995f32445e344c03f9b0c774eabcd157559f867`. File SHA-256: `efdddafcdb7bda61220fa821f7435714e4fe5385cb8050b20e01fe8c174735a4`.
- [pret/pokestadium · oldnotes/stadium1/text/movedescriptions.txt · lines 5–7](https://github.com/pret/pokestadium/blob/6995f32445e344c03f9b0c774eabcd157559f867/oldnotes/stadium1/text/movedescriptions.txt#L5-L7)
  Revision: `6995f32445e344c03f9b0c774eabcd157559f867`. File SHA-256: `9e2b1fbb56895a5bb8e28757b23481c68e8c8718bb9b3edde34f2c7fcfad7d6b`.
- [pret/pokestadium · oldnotes/stadium1/text/movedescriptions.txt · lines 61–63](https://github.com/pret/pokestadium/blob/6995f32445e344c03f9b0c774eabcd157559f867/oldnotes/stadium1/text/movedescriptions.txt#L61-L63)
  Revision: `6995f32445e344c03f9b0c774eabcd157559f867`. File SHA-256: `9e2b1fbb56895a5bb8e28757b23481c68e8c8718bb9b3edde34f2c7fcfad7d6b`.
- [pret/pokestadium · oldnotes/stadium1/text/movedescriptions.txt · lines 401–403](https://github.com/pret/pokestadium/blob/6995f32445e344c03f9b0c774eabcd157559f867/oldnotes/stadium1/text/movedescriptions.txt#L401-L403)
  Revision: `6995f32445e344c03f9b0c774eabcd157559f867`. File SHA-256: `9e2b1fbb56895a5bb8e28757b23481c68e8c8718bb9b3edde34f2c7fcfad7d6b`.

<a id="e60"></a>

## E60 — Shin Hyper Beam clause is branch-specific

**Status:** selected source paths and text verified; no donor game execution. Master checks EVENT_8C8 and target HP before setting recharge. Its NPC sets that event and describes skipping KO recharge, matching the handler. A README history line conflicts. Lite calls the recharge effect before the KO return on both sides and has no Master clause guard in its effect routine.

- [jojobear13/shinpokered (shin-master) · custom_functions/func_battle.asm · lines 401–427](https://github.com/jojobear13/shinpokered/blob/a7a9b1361e55aaa5afed6b5d14b5e7bd44002179/custom_functions/func_battle.asm#L401-L427)
  Revision: `a7a9b1361e55aaa5afed6b5d14b5e7bd44002179`. File SHA-256: `34574d71863987aad5c2b2b6f57b16af7b891aba7833dca48ce2eeb45445795f`.
- [jojobear13/shinpokered (shin-master) · engine/battle/core.asm · lines 9564–9574](https://github.com/jojobear13/shinpokered/blob/a7a9b1361e55aaa5afed6b5d14b5e7bd44002179/engine/battle/core.asm#L9564-L9574)
  Revision: `a7a9b1361e55aaa5afed6b5d14b5e7bd44002179`. File SHA-256: `060d56cac38b835410e646859e4422fc3ec4141f1b50f982b8621efd6b1e848d`.
- [jojobear13/shinpokered (shin-master) · scripts/viridianhouse.asm · lines 181–203](https://github.com/jojobear13/shinpokered/blob/a7a9b1361e55aaa5afed6b5d14b5e7bd44002179/scripts/viridianhouse.asm#L181-L203)
  Revision: `a7a9b1361e55aaa5afed6b5d14b5e7bd44002179`. File SHA-256: `92b28a697c61b4e476a8abc35c89fc5352ed343604cedfa3577a874178475a05`.
- [jojobear13/shinpokered (shin-master) · text/maps/viridian_house.asm · lines 75–86](https://github.com/jojobear13/shinpokered/blob/a7a9b1361e55aaa5afed6b5d14b5e7bd44002179/text/maps/viridian_house.asm#L75-L86)
  Revision: `a7a9b1361e55aaa5afed6b5d14b5e7bd44002179`. File SHA-256: `fec7211bdca892aca19d967fbc615125d171279399795a84635b561cd7a50a11`.
- [jojobear13/shinpokered (shin-master) · README.md · lines 1154–1167](https://github.com/jojobear13/shinpokered/blob/a7a9b1361e55aaa5afed6b5d14b5e7bd44002179/README.md#L1154-L1167)
  Revision: `a7a9b1361e55aaa5afed6b5d14b5e7bd44002179`. File SHA-256: `be9bc853c1792011dccd5d8bd8ba5478751b293db5ebe91be0a435fe29c6eb30`.
- [jojobear13/shinpokered (shin-lite) · engine/battle/core.asm · lines 61–74](https://github.com/jojobear13/shinpokered/blob/b35c2a536a1605841c8fb662aad18b0dbfd2a900/engine/battle/core.asm#L61-L74)
  Revision: `b35c2a536a1605841c8fb662aad18b0dbfd2a900`. File SHA-256: `12c421b7e8bf81d658aa2c0845f8e3c0cacd8f60bf79cfc4ff27c9ff46ac3bf4`.
- [jojobear13/shinpokered (shin-lite) · engine/battle/core.asm · lines 3722–3732](https://github.com/jojobear13/shinpokered/blob/b35c2a536a1605841c8fb662aad18b0dbfd2a900/engine/battle/core.asm#L3722-L3732)
  Revision: `b35c2a536a1605841c8fb662aad18b0dbfd2a900`. File SHA-256: `12c421b7e8bf81d658aa2c0845f8e3c0cacd8f60bf79cfc4ff27c9ff46ac3bf4`.
- [jojobear13/shinpokered (shin-lite) · engine/battle/core.asm · lines 6662–6672](https://github.com/jojobear13/shinpokered/blob/b35c2a536a1605841c8fb662aad18b0dbfd2a900/engine/battle/core.asm#L6662-L6672)
  Revision: `b35c2a536a1605841c8fb662aad18b0dbfd2a900`. File SHA-256: `12c421b7e8bf81d658aa2c0845f8e3c0cacd8f60bf79cfc4ff27c9ff46ac3bf4`.
- [jojobear13/shinpokered (shin-lite) · engine/battle/core.asm · lines 9477–9485](https://github.com/jojobear13/shinpokered/blob/b35c2a536a1605841c8fb662aad18b0dbfd2a900/engine/battle/core.asm#L9477-L9485)
  Revision: `b35c2a536a1605841c8fb662aad18b0dbfd2a900`. File SHA-256: `12c421b7e8bf81d658aa2c0845f8e3c0cacd8f60bf79cfc4ff27c9ff46ac3bf4`.

<a id="e61"></a>

## E61 — Eevee Focus Energy and Jolteon evolution access

**Status:** learnsets and evolution data flow verified; no gameplay or trade test. English Yellow and Solus give Eevee Focus Energy at level 36 and a Thunder Stone evolution into Jolteon. Their checked evolution data flow retains current moves. Jolteon has base Speed 130. The pinned Red/Blue Eevee level-up list lacks Focus Energy. Obtainability and the critical-threshold calculation are separate claims.

- [pret/pokeyellow (pokeyellow) · README.md · lines 1–9](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/README.md#L1-L9)
  Revision: `e89ead154b9968aa50eed9328ff2b38b6c194382`. File SHA-256: `32ba99712866b4e3a1e2d2287d86be519248a9cd4bbaeb21f6e2c735cc31cc4f`.
- [pret/pokeyellow (pokeyellow) · data/pokemon/evos_moves.asm · lines 1268–1281](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/data/pokemon/evos_moves.asm#L1268-L1281)
  Revision: `e89ead154b9968aa50eed9328ff2b38b6c194382`. File SHA-256: `7e72c0e034ce7f895d604cf0d3cd9f4ada2f3312ed75c57fa23c16a70d55b0ef`.
- [pret/pokeyellow (pokeyellow) · data/pokemon/base_stats/jolteon.asm · lines 1–6](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/data/pokemon/base_stats/jolteon.asm#L1-L6)
  Revision: `e89ead154b9968aa50eed9328ff2b38b6c194382`. File SHA-256: `dd7f9cdbfb35b0622ad47dc77df910a8dd0fa3ca5d1b9b091673c30d523debc4`.
- [pret/pokeyellow (pokeyellow) · engine/pokemon/load_mon_data.asm · lines 25–50](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/engine/pokemon/load_mon_data.asm#L25-L50)
  Revision: `e89ead154b9968aa50eed9328ff2b38b6c194382`. File SHA-256: `27359a563c304ff8375f6bcc151d76c4e33a72f5d245b4733f9756d45a817503`.
- [pret/pokeyellow (pokeyellow) · engine/pokemon/evos_moves.asm · lines 176–214](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/engine/pokemon/evos_moves.asm#L176-L214)
  Revision: `e89ead154b9968aa50eed9328ff2b38b6c194382`. File SHA-256: `a0d204e615ca1e692b1a842c4f25e18c98769384a7527b6cb2dad409113e51b5`.
- [pret/pokeyellow (pokeyellow) · constants/pokemon_data_constants.asm · lines 26–49](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/constants/pokemon_data_constants.asm#L26-L49)
  Revision: `e89ead154b9968aa50eed9328ff2b38b6c194382`. File SHA-256: `69edbf30b07a0cbcba55911fa3bd1eae8e625daab61413b3e8e0e4706d4ba013`.
- [Dechrissen/poke-solus-rgb (solus) · data/pokemon/evos_moves.asm · lines 1304–1317](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/data/pokemon/evos_moves.asm#L1304-L1317)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `ffd13368e52bcae20a19e4fb7ca2f2855d078543eed918da67c975ac3140623d`.
- [Dechrissen/poke-solus-rgb (solus) · data/pokemon/base_stats/jolteon.asm · lines 1–6](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/data/pokemon/base_stats/jolteon.asm#L1-L6)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `7ee1037688d0580d75de7b6d1a96dafa1a88a28de1e1a2ce17b1655d33aa2c51`.
- [Dechrissen/poke-solus-rgb (solus) · engine/pokemon/load_mon_data.asm · lines 25–49](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/engine/pokemon/load_mon_data.asm#L25-L49)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `a268aa12ebde097236d44f5e9a8d9269fad1967f89fe964a73f6e5c31abf3596`.
- [Dechrissen/poke-solus-rgb (solus) · engine/pokemon/evos_moves.asm · lines 172–210](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/engine/pokemon/evos_moves.asm#L172-L210)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `9b2ed863d91a6d04487ab55bd359daf6c705f2e96400a74f65f4faae0c443105`.
- [pret/pokered (pokered) · data/pokemon/evos_moves.asm · lines 1252–1264](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/pokemon/evos_moves.asm#L1252-L1264)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `1a4c475c47134440a4a4e54265314638d8c6953da558d7d6a7b7f7bc206c2f30`.

<a id="e62"></a>

## E62 — Sabrina gym advice and Ghost damage evidence

**Status:** source-verified text and data; original intent unresolved. English gym text says Psychic Pokémon fear ghosts and bugs. The checked attack table records Ghost/Psychic immunity and Lick has 20 power. The fixed-damage path skips ordinary type adjustment. These observations do not establish an internal developer specification or a required default chart change.

- [pret/pokered (pokered) · text/SaffronGym.asm · lines 135–139](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/text/SaffronGym.asm#L135-L139)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `3e45009b2f1082bccd099d8a9ff8f491e3a9bf5f34e54cf839523e332c0788d0`.
- [pret/pokered (pokered) · data/types/type_matchups.asm · lines 77–78](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/types/type_matchups.asm#L77-L78)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f7f2286029d4fe64c80ed6cc5f5c75ec1f1b8903a9eabd171deab49e23228d39`.
- [pret/pokered (pokered) · data/moves/moves.asm · lines 135–135](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/moves/moves.asm#L135-L135)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `a2cf3e1ec6bf4b5caaeeec974967691c9eb47923d1e7432fb0267ba7d3a5931f`.
- [pret/pokered (pokered) · engine/battle/core.asm · lines 3134–3150](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L3134-L3150)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.

<a id="e63"></a>

## E63 — Emerald Expansion species controls and separate encounters

**Status:** source-verified configuration and selected guarded data; no configured build. Checked 2026-10-12. The checked defaults enable species generations 1 through 9. Generations, families, later forms, and cross-generation evolutions have developer controls. Turtwig's family depends on the Gen 4 control and guards its species record. Route 101 encounter data is separate and lists Wurmple, Poochyena, and Zigzagoon; species support does not require using every species in encounters.

- [pokeemerald-expansion · include/config/species_enabled.h · lines 4–57](https://github.com/rh-hideout/pokeemerald-expansion/blob/8fb02c6f2b81271e795d3f6aca61733fec739016/include/config/species_enabled.h#L4-L57)
  Revision: `8fb02c6f2b81271e795d3f6aca61733fec739016`. File SHA-256: `86a829d83a344bf23440a586706bf3c91ccef9a02c145afa0d1844c8824374eb`.
- [pokeemerald-expansion · include/config/species_enabled.h · lines 261–261](https://github.com/rh-hideout/pokeemerald-expansion/blob/8fb02c6f2b81271e795d3f6aca61733fec739016/include/config/species_enabled.h#L261-L261)
  Revision: `8fb02c6f2b81271e795d3f6aca61733fec739016`. File SHA-256: `86a829d83a344bf23440a586706bf3c91ccef9a02c145afa0d1844c8824374eb`.
- [pokeemerald-expansion · src/data/pokemon/species_info/gen_4_families.h · lines 6–28](https://github.com/rh-hideout/pokeemerald-expansion/blob/8fb02c6f2b81271e795d3f6aca61733fec739016/src/data/pokemon/species_info/gen_4_families.h#L6-L28)
  Revision: `8fb02c6f2b81271e795d3f6aca61733fec739016`. File SHA-256: `3b6b6c30d7b1aa12e0576fc530e37b3885131fd601fcd9e4353ca19c1b0e3cae`.
- [pokeemerald-expansion · src/data/wild_encounters.json · lines 78–147](https://github.com/rh-hideout/pokeemerald-expansion/blob/8fb02c6f2b81271e795d3f6aca61733fec739016/src/data/wild_encounters.json#L78-L147)
  Revision: `8fb02c6f2b81271e795d3f6aca61733fec739016`. File SHA-256: `e0f695fc6cbd6bb8ceddf83c76ad69ca2a4f529d8c95167e228dc5e9812b9f18`.

<a id="e64"></a>

## E64 — Emerald Expansion modern defaults and older-rule configuration

**Status:** source-verified settings and documented policy; whole-game equivalence untested. Checked 2026-10-12. GEN_LATEST defaults to GEN_9 and can change defaults that refer to it. Separate battle and Pokemon data controls select critical rules, damage categories, types, stats, and learnsets. The documented policy enables developer improvements and modern-game emulation by default, with a separate rule for save-changing additions. Boolean graphics defaults are independent of GEN_LATEST, so setting GEN_LATEST to GEN_3 alone does not establish a vanilla Emerald configuration.

- [pokeemerald-expansion · include/config/general.h · lines 61–77](https://github.com/rh-hideout/pokeemerald-expansion/blob/8fb02c6f2b81271e795d3f6aca61733fec739016/include/config/general.h#L61-L77)
  Revision: `8fb02c6f2b81271e795d3f6aca61733fec739016`. File SHA-256: `270073678c6849e9d16816bc6dcaecdd1124988353a1e7d0dc2552e13e187fd5`.
- [pokeemerald-expansion · include/config/battle.h · lines 5–10](https://github.com/rh-hideout/pokeemerald-expansion/blob/8fb02c6f2b81271e795d3f6aca61733fec739016/include/config/battle.h#L5-L10)
  Revision: `8fb02c6f2b81271e795d3f6aca61733fec739016`. File SHA-256: `7600c4622f7d154aef50f74bb8fd20fbd5aa84a928557fa1feadd14bda34861a`.
- [pokeemerald-expansion · include/config/battle.h · lines 23–26](https://github.com/rh-hideout/pokeemerald-expansion/blob/8fb02c6f2b81271e795d3f6aca61733fec739016/include/config/battle.h#L23-L26)
  Revision: `8fb02c6f2b81271e795d3f6aca61733fec739016`. File SHA-256: `7600c4622f7d154aef50f74bb8fd20fbd5aa84a928557fa1feadd14bda34861a`.
- [pokeemerald-expansion · include/config/battle.h · lines 73–76](https://github.com/rh-hideout/pokeemerald-expansion/blob/8fb02c6f2b81271e795d3f6aca61733fec739016/include/config/battle.h#L73-L76)
  Revision: `8fb02c6f2b81271e795d3f6aca61733fec739016`. File SHA-256: `7600c4622f7d154aef50f74bb8fd20fbd5aa84a928557fa1feadd14bda34861a`.
- [pokeemerald-expansion · include/config/pokemon.h · lines 4–19](https://github.com/rh-hideout/pokeemerald-expansion/blob/8fb02c6f2b81271e795d3f6aca61733fec739016/include/config/pokemon.h#L4-L19)
  Revision: `8fb02c6f2b81271e795d3f6aca61733fec739016`. File SHA-256: `e476277d082276ac078452c44482cf9b3b6fb076159fe4745f0774bc276b85ba`.
- [pokeemerald-expansion · include/config/pokemon.h · lines 41–58](https://github.com/rh-hideout/pokeemerald-expansion/blob/8fb02c6f2b81271e795d3f6aca61733fec739016/include/config/pokemon.h#L41-L58)
  Revision: `8fb02c6f2b81271e795d3f6aca61733fec739016`. File SHA-256: `e476277d082276ac078452c44482cf9b3b6fb076159fe4745f0774bc276b85ba`.
- [pokeemerald-expansion · docs/STYLEGUIDE.md · lines 459–471](https://github.com/rh-hideout/pokeemerald-expansion/blob/8fb02c6f2b81271e795d3f6aca61733fec739016/docs/STYLEGUIDE.md#L459-L471)
  Revision: `8fb02c6f2b81271e795d3f6aca61733fec739016`. File SHA-256: `55c506edc985799759e4b80512b2567eeae7d21420e9d99b30a24cb44aefc863`.

<a id="e65"></a>

## E65 — Emerald Expansion replaces the original random-number generator

**Status:** source-verified functions; generation-setting consequence derived; no runtime comparison. Checked 2026-10-12. Original Emerald updates one 32-bit state value using ISO_RANDOMIZE1 and returns its upper 16 bits. Expansion uses SFC32 state, a different seed procedure, and different update functions. The checked Random and SeedRng paths do not select the original algorithm through GEN_LATEST; choosing Gen 3 rule defaults does not restore the original random sequence.

- [pret/pokeemerald · include/random.h · lines 7–20](https://github.com/pret/pokeemerald/blob/731ad5bfd6e6f265508d0efcca0ba42f9dcf5881/include/random.h#L7-L20)
  Revision: `731ad5bfd6e6f265508d0efcca0ba42f9dcf5881`. File SHA-256: `566ab9be0a0840b31465faf3df5c529445a9c6d08959fd4f7f1f0ec7e637c941`.
- [pret/pokeemerald · src/random.c · lines 11–32](https://github.com/pret/pokeemerald/blob/731ad5bfd6e6f265508d0efcca0ba42f9dcf5881/src/random.c#L11-L32)
  Revision: `731ad5bfd6e6f265508d0efcca0ba42f9dcf5881`. File SHA-256: `71d7335fde4c0c7dd8c3245560defa2e23124b8ba8ec5d50bf1295ebc24bdcdf`.
- [rh-hideout/pokeemerald-expansion · include/random.h · lines 24–62](https://github.com/rh-hideout/pokeemerald-expansion/blob/8fb02c6f2b81271e795d3f6aca61733fec739016/include/random.h#L24-L62)
  Revision: `8fb02c6f2b81271e795d3f6aca61733fec739016`. File SHA-256: `fb4f0f9e9e288001c33c1c40c720eb98d0f91df7a89e5eec7852deefd23a964a`.
- [rh-hideout/pokeemerald-expansion · src/random.c · lines 18–85](https://github.com/rh-hideout/pokeemerald-expansion/blob/8fb02c6f2b81271e795d3f6aca61733fec739016/src/random.c#L18-L85)
  Revision: `8fb02c6f2b81271e795d3f6aca61733fec739016`. File SHA-256: `6eca2a3ca6b089d01e6772aa154400124597eff578682b8a2c5b5db1eff27c3f`.

<a id="e66"></a>

## E66 — Emerald Expansion basic trainer AI and stated multiplayer boundary

**Status:** documented behavior/support claims with source-verified flag group; no AI or link execution. Checked 2026-10-12. The guide shows developers selecting AI flags in trainer records. Expansion documents that some AI functions retain vanilla names but change their behavior. Its basic trainer group is documented as choosing moves better than vanilla; the constants define it as CheckBadMove, TryToFaint, and CheckViability. Its README supports multiplayer between Expansion games, excludes official-game compatibility, and recommends the original decompilation when that compatibility matters. These documented claims are not executable equivalence or link tests.

- [rh-hideout/pokeemerald-expansion · docs/tutorials/ai_flags.md · lines 23–34](https://github.com/rh-hideout/pokeemerald-expansion/blob/8fb02c6f2b81271e795d3f6aca61733fec739016/docs/tutorials/ai_flags.md#L23-L34)
  Revision: `8fb02c6f2b81271e795d3f6aca61733fec739016`. File SHA-256: `f9b22e8868a119577cfca4da1b88606c1035cd56190ac09171b9ce902da2c686`.
- [rh-hideout/pokeemerald-expansion · include/constants/battle_ai.h · lines 48–50](https://github.com/rh-hideout/pokeemerald-expansion/blob/8fb02c6f2b81271e795d3f6aca61733fec739016/include/constants/battle_ai.h#L48-L50)
  Revision: `8fb02c6f2b81271e795d3f6aca61733fec739016`. File SHA-256: `bb8b05f67f74d82b068fc20329774df4efae9d93636d1aaec9840736268b63fa`.
- [rh-hideout/pokeemerald-expansion · README.md · lines 25–29](https://github.com/rh-hideout/pokeemerald-expansion/blob/8fb02c6f2b81271e795d3f6aca61733fec739016/README.md#L25-L29)
  Revision: `8fb02c6f2b81271e795d3f6aca61733fec739016`. File SHA-256: `d582524c553dcc66c4dcb37dd02c6e1d639ff794aa7c90f4110f99857fe0d5eb`.

<a id="e67"></a>

## E67 — Original Emerald decompilation identifies its reconstruction target

**Status:** source-verified published target identity; build not executed. Checked 2026-10-12. The original pret/pokeemerald README identifies its output as pokeemerald.gba with SHA-1 f3ae088181bf583e55daf962a92bb46f4f1d07b7. It is the direct original-game source reference for small edits or behavior comparisons. This review did not build that ROM or establish a complete restoration profile for Expansion.

- [pret/pokeemerald · README.md · lines 3–9](https://github.com/pret/pokeemerald/blob/731ad5bfd6e6f265508d0efcca0ba42f9dcf5881/README.md#L3-L9)
  Revision: `731ad5bfd6e6f265508d0efcca0ba42f9dcf5881`. File SHA-256: `5ed60cb1aaa9ec6f7c01bea7f166a8208d287799d566dec550d2ed5d067426dd`.

<a id="e68"></a>

## E68 — EXP. ALL discard path and one-time reward

**Status:** source-verified loss path and related item behavior; no executable reproduction. Checked 2026-10-14. EXP_ALL has a false key-item flag. TossItem_ rejects HMs and key items before the discard confirmation/removal path; both bag and PC toss menus call that routine. The Route 15 aide checks EVENT_GOT_EXP_ALL and sets it after a successful reward, so discarding the item does not make that scripted reward repeat. PC deposit and withdrawal allow key items with a one-item transfer. Key-item status also blocks selling. Battle experience checks whether EXP_ALL is in the bag. Original intent is not established; discard protection is a separately accepted default safeguard.

- [pret/pokered · data/items/key_items.asm · lines 69–80](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/items/key_items.asm#L69-L80)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f50153804248ef659ca5eadb3978eabd2489aeda6c747d9a12e98c4d6cb8d955`.
- [pret/pokered · engine/items/item_effects.asm · lines 2547–2595](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L2547-L2595)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.
- [pret/pokered · scripts/Route15Gate2F.asm · lines 9–31](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/Route15Gate2F.asm#L9-L31)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `35c5ac0f9b8d5897d9740d1fd367000f90d407cee9e88cdb625d308f6eaf739b`.
- [pret/pokered · engine/menus/start_sub_menus.asm · lines 424–437](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/start_sub_menus.asm#L424-L437)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `cce764b4234f1f2a97c8062654061a7af759e5ed9567ddb9c980776166c0c8d5`.
- [pret/pokered · engine/menus/players_pc.asm · lines 110–241](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/players_pc.asm#L110-L241)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f6b13c32e7bde9ccf0036e4ce42a78b4ae8d2e8a83bfe607b807f4410905ae59`.
- [pret/pokered · engine/events/pokemart.asm · lines 70–77](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/pokemart.asm#L70-L77)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `94c0f7c02cb6d5d1b8e6adf98b49eb8848561f1225cc6b95bb426ce9db9e5abc`.
- [pret/pokered · engine/battle/core.asm · lines 818–831](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L818-L831)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.

<a id="e69"></a>

## E69 — Overworld controls and Bicycle shortcut boundaries

**Status:** source-verified handlers and restrictions; registration feature not implemented. Checked 2026-10-14. The checked overworld handler tests START and A before directional input, without a registered-item action. SELECT swaps item-list entries. ItemUseBicycle rejects battle use, surfing, and riding where map rules forbid it. The item menu separately rejects Bicycle use when BIT_ALWAYS_ON_BIKE is set; the shortcut cannot rely on the effect routine alone to retain forced-riding behavior. Door-exit movement masks SELECT among ignored inputs. These are source findings, not executable shortcut tests.

- [pret/pokered · home/overworld.asm · lines 41–83](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/overworld.asm#L41-L83)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `04683d520f775876f8ec050cbc20e145ef4e596293393d0cb2e7ccd0657cc11a`.
- [pret/pokered · home/overworld.asm · lines 842–869](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/overworld.asm#L842-L869)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `04683d520f775876f8ec050cbc20e145ef4e596293393d0cb2e7ccd0657cc11a`.
- [pret/pokered · home/list_menu.asm · lines 172–176](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/list_menu.asm#L172-L176)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `43f046e47dfa086a753dc9843d00e8fa69c07da226baa3b4cd7ed80476f187ac`.
- [pret/pokered · engine/items/item_effects.asm · lines 638–666](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L638-L666)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.
- [pret/pokered · engine/menus/start_sub_menus.asm · lines 330–379](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/start_sub_menus.asm#L330-L379)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `cce764b4234f1f2a97c8062654061a7af759e5ed9567ddb9c980776166c0c8d5`.
- [pret/pokered · engine/overworld/auto_movement.asm · lines 1–16](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/overworld/auto_movement.asm#L1-L16)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `51132df663914861ac176733a764788e1db1d96f27d830952279338cc7633379`.

<a id="e70"></a>

## E70 — Bill’s PC blocks the box list before checking the selected action

**Status:** source-verified menu flow and capacity error; no executable reproduction. Checked 2026-10-14. BillsPCWithdraw checks party capacity before DisplayMonListMenu. The selected-Pokemon menu supports withdrawal, STATS, and cancellation; it returns carry for the withdrawal action. The successful path calls MoveMon then RemovePokemon. PARTY_LENGTH is six. CantTakeMonText uses the existing message asking the player to deposit Pokemon first. These findings support relocating the guard to the actual withdrawal action, not removing it.

- [pret/pokered · engine/pokemon/bills_pc.asm · lines 256–291](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/bills_pc.asm#L256-L291)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f123f75a572c33887a28637eab894588f04a546593f61f07f4716ff9ae361ccf`.
- [pret/pokered · engine/pokemon/bills_pc.asm · lines 382–447](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/bills_pc.asm#L382-L447)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f123f75a572c33887a28637eab894588f04a546593f61f07f4716ff9ae361ccf`.
- [pret/pokered · engine/pokemon/bills_pc.asm · lines 487–489](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/bills_pc.asm#L487-L489)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f123f75a572c33887a28637eab894588f04a546593f61f07f4716ff9ae361ccf`.
- [pret/pokered · constants/pokemon_data_constants.asm · lines 58–60](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/constants/pokemon_data_constants.asm#L58-L60)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `69edbf30b07a0cbcba55911fa3bd1eae8e625daab61413b3e8e0e4706d4ba013`.
- [pret/pokered · data/text/text_2.asm · lines 1594–1600](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/text/text_2.asm#L1594-L1600)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `ba97e54e9feafb22816b449841181b64234537bac9ccdef6aa3d79f4153e23b9`.

<a id="e71"></a>

## E71 — Full active box prevents ball use with a full party

**Status:** source-verified entry guard and failure message; no executable reproduction. Checked 2026-10-14. The checked ball-use routine permits a ball when the party has room. With a full party it compares the current box count with MONS_PER_BOX and rejects the item when that box is full, without checking other boxes at this guard. The old-man demonstration skips the capacity check. The failure path clears wActionResultOrTookBattleTurn and shows the existing full-box text. This establishes the active-box restriction at ball-use entry, not an end-to-end capture/storage or interrupted-write audit.

- [pret/pokered · engine/items/item_effects.asm · lines 105–125](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L105-L125)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.
- [pret/pokered · engine/items/item_effects.asm · lines 2309–2322](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L2309-L2322)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.
- [pret/pokered · data/text/text_6.asm · lines 227–231](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/text/text_6.asm#L227-L231)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `780a4113660b6ed4c3fa54ddd2a984e1dc7d6bea7f423a00d5a476dfaf5f80ec`.

<a id="e72"></a>

## E72 — Bag capacity, allocation, enforcement, and saved-data boundary

**Status:** source-verified implementation; no executable reproduction or original-intent finding. Checked 2026-10-14. The constants set bag capacity to 20 slots and PC item capacity to 50. AddItemToInventory_ selects the destination capacity and refuses adding a new slot when it is full. The bag allocates two bytes per slot plus its terminator in wMainData. The main-data region is allocated and copied into cartridge save memory. A capacity change therefore affects allocation and saved-data layout, not just the comparison at item insertion. These facts do not establish why the original team chose 20, prove that increasing capacity was impossible, or show that it had no technical cost.

- [pret/pokered · constants/menu_constants.asm · lines 1–2](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/constants/menu_constants.asm#L1-L2)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `fbd0e91bd6ac5f8a491a4d5df3ccbc4438f34c234ce9be684f82b2537c6022ac`.
- [pret/pokered · engine/items/inventory.asm · lines 7–53](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/inventory.asm#L7-L53)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `410632e0a82e3491fd6d2898c337eb4a8e83ce6a1b31dad0a12bf887a27a3f7e`.
- [pret/pokered · ram/wram.asm · lines 1747–1762](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/ram/wram.asm#L1747-L1762)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `00683cd430a9ef30794d2aeaee51f3a5440e4bb14dca13e9f9cb5fa88f130e34`.
- [pret/pokered · ram/sram.asm · lines 12–24](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/ram/sram.asm#L12-L24)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `de4bb57acb8d9c06a087ce2c5c85be78a2790160521ce5807c10008d0769f66a`.
- [pret/pokered · engine/menus/save.asm · lines 208–225](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/save.asm#L208-L225)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `54f98d6e16733c593376da81d4bebe2fad7d4408b4a93aa163e167c09d5fa6fb`.

<a id="e73"></a>

## E73 — Field-move eligibility and checks span the party menu and effects

**Status:** source-verified implementation; no executable reproduction or original-intent finding. Checked 2026-10-14. GetMonFieldMoves reads the selected party Pokemon's learned moves. The menu dispatch checks Cascadebadge for Cut, Thunderbadge for Fly, Soulbadge for Surf, Rainbowbadge for Strength, and Boulderbadge for Flash. Surf additionally checks field-map permissions and its item-effect path checks shore/water and tile-pair collisions. Cut checks tileset and facing tile. Strength sets an active bit; the push routine separately checks boulder identity, repeated pushing, input, and collision. Map entry has a conditional Strength reset. The overworld A path already dispatches hidden events, objects, and signs. Fly chooses a destination and Flash changes the map palette; neither is a facing-target dispatcher in the checked menu. These source findings support shared validation for the new contextual shortcut; they do not establish a working A-button HM implementation.

- [pret/pokered · engine/menus/text_box.asm · lines 509–561](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/text_box.asm#L509-L561)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `fe5e3f320fd2e0fa1a5eb38eef21166f26d8c929da22cf73a5344ac16365c636`.
- [pret/pokered · engine/menus/start_sub_menus.asm · lines 109–194](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/start_sub_menus.asm#L109-L194)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `cce764b4234f1f2a97c8062654061a7af759e5ed9567ddb9c980776166c0c8d5`.
- [pret/pokered · engine/overworld/cut.asm · lines 1–65](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/overworld/cut.asm#L1-L65)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `9062c09d8a39fc0be5abccc6cd35ac422e18c9ab477464d9c91b8316bea57693`.
- [pret/pokered · engine/overworld/field_move_messages.asm · lines 1–58](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/overworld/field_move_messages.asm#L1-L58)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `2dfecbe4f37e901f9601beaa5f3d247fc6927ff77f1e1f6a5d9e2135aa6006f2`.
- [pret/pokered · engine/items/item_effects.asm · lines 669–722](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L669-L722)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.
- [pret/pokered · engine/overworld/push_boulder.asm · lines 1–44](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/overworld/push_boulder.asm#L1-L44)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `970dd0a9c45f5252817cd50f468551214660c35854d0a022cc4789110da8c153`.
- [pret/pokered · home/overworld.asm · lines 81–107](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/overworld.asm#L81-L107)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `04683d520f775876f8ec050cbc20e145ef4e596293393d0cb2e7ccd0657cc11a`.
- [pret/pokered · home/overworld.asm · lines 6–22](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/overworld.asm#L6-L22)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `04683d520f775876f8ec050cbc20e145ef4e596293393d0cb2e7ccd0657cc11a`.
- [pret/pokered · home/overworld.asm · lines 2383–2386](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/overworld.asm#L2383-L2386)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `04683d520f775876f8ec050cbc20e145ef4e596293393d0cb2e7ccd0657cc11a`.

<a id="e74"></a>

## E74 — EXP. ALL sale path and important-item refusal

**Status:** source-verified flags, sale path, and message; no executable reproduction. Checked 2026-10-14. EXP_ALL has a zero listed price and a false key-item flag; BICYCLE has a true key-item flag. The shop checks key-item status and then HM status before quantity and sale-price confirmation. A confirmed sale calls AddAmountSoldToMoney followed by RemoveItemFromInventory. The key-item/HM refusal uses PokemartUnsellableItemText, whose English text is I can't put a price on that. The checked menu has no zero-price refusal replacing those status checks. This supports the reported loss path and the proposed key-item protection; no executable sale reproduction or applied patch is claimed.

- [pret/pokered · data/items/key_items.asm · lines 1–10](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/items/key_items.asm#L1-L10)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f50153804248ef659ca5eadb3978eabd2489aeda6c747d9a12e98c4d6cb8d955`.
- [pret/pokered · data/items/key_items.asm · lines 69–80](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/items/key_items.asm#L69-L80)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f50153804248ef659ca5eadb3978eabd2489aeda6c747d9a12e98c4d6cb8d955`.
- [pret/pokered · data/items/prices.asm · lines 69–80](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/items/prices.asm#L69-L80)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f5c70cea9cf59239ddb2deceda59e577cfe30cf2bc36c80e5e2a8834af788d60`.
- [pret/pokered · engine/events/pokemart.asm · lines 69–117](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/pokemart.asm#L69-L117)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `94c0f7c02cb6d5d1b8e6adf98b49eb8848561f1225cc6b95bb426ce9db9e5abc`.
- [pret/pokered · engine/events/pokemart.asm · lines 262–264](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/pokemart.asm#L262-L264)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `94c0f7c02cb6d5d1b8e6adf98b49eb8848561f1225cc6b95bb426ce9db9e5abc`.
- [pret/pokered · data/text/text_4.asm · lines 70–73](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/text/text_4.asm#L70-L73)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `eb9287b4d4e40679a916747d5ab7f6fb97ae7d6aabbfd7c2dc9ccabd2dcf5311`.

<a id="e75"></a>

## E75 — FireRed/LeafGreen badge award and stat mappings

**Status:** source-verified reconstruction; no executable test or original-intent proof. Checked 2026-10-14. The English FireRed/LeafGreen decompilation publishes matching ROM output hashes. Surge awards FLAG_BADGE03_GET and Koga FLAG_BADGE05_GET. Battle turn-order calculation applies badge 3 to player Speed; damage calculation applies badge 5 to player Defense. This later implementation agrees with the original English dialogue and manual, but does not prove the original developers intent.

- [firered-reference · README.md · lines 1–14](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/README.md#L1-L14)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `ab59004406fa7c682aed5f7d034e527ac9b9c8cf4a0257920b1340bc25e99f3d`.
- [firered-reference · data/maps/VermilionCity_Gym/scripts.inc · lines 214–229](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/VermilionCity_Gym/scripts.inc#L214-L229)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `3341fb187215a9b961bde55465491fb3b24772fe11b0f801d840dcea3888ed7c`.
- [firered-reference · data/maps/FuchsiaCity_Gym/scripts.inc · lines 4–22](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/FuchsiaCity_Gym/scripts.inc#L4-L22)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `5af256d09bf8768431c502381d40543a3bbf136e2cf3feacebe3bf85a2b62502`.
- [firered-reference · src/battle_main.c · lines 3442–3471](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/src/battle_main.c#L3442-L3471)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `c290d325761d68c059f02dc21cc6178d4bbefa0d06ffddc8879341c090d37928`.
- [firered-reference · src/pokemon.c · lines 2379–2385](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/src/pokemon.c#L2379-L2385)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `116a470cd9ebfa226aa8d85c2eb63591e176d726837c67baaa1ac6260d50f2ec`.
- [firered-reference · src/pokemon.c · lines 2440–2447](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/src/pokemon.c#L2440-L2447)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `116a470cd9ebfa226aa8d85c2eb63591e176d726837c67baaa1ac6260d50f2ec`.

<a id="e76"></a>

## E76 — Original US manual Thunder and Soul badge descriptions

**Status:** scan visually verified; original internal design intent unproven. Checked 2026-10-14. The original US instruction booklet scan identifies a Pokemon Trainers Guide, U/DMG-APAE-USA, with Nintendo of America and 1998 copyright information. Printed page 27 assigns Speed to the Thunder Badge and Defense to the Soul Badge. The scan is hosted by a third party; it is not an internal Game Freak design record.

- [Scanned publication](https://www.videogamemanual.com/gameboy/Pokemon%20-%20Red%20Version%20%28USA%29.pdf). PDF pages (one-based): 1, 2, 29. Printed page(s): 27. File SHA-256: `5b75ad6eb949d383b899287cdfe13631da0f61f8edd66144f83a5ff6e9f72f10`.

<a id="e77"></a>

## E77 — Prima 1998 Thunder and Soul badge descriptions

**Status:** scan visually verified; not independent proof of internal intent. Checked 2026-10-14. Printed page 26 assigns Speed to the Thunder Badge and printed page 47 assigns Defense to the Soul Badge. The guide is additional contemporary published evidence, but may repeat dialogue or shared reference material.

- [Scanned publication](https://archive.org/download/PokemonOfficialPrimaStrategyGuide/Pokemon%20Official%20Prima%20Strategy%20Guide_text.pdf). PDF pages (one-based): 29, 50. Printed page(s): [26, 47]. File SHA-256: `b6163bb943f68abb4247221103ee785079ae108e17a65977d6331d651c350dfd`.

<a id="e78"></a>

## E78 — PureRGB corrects the Thunder/Soul code mapping

**Status:** source-verified at current branch head; no donor ROM build or runtime test. Checked 2026-10-14. PureRGB explicitly tests the Thunder badge bit before boosting Speed and the Soul badge bit before boosting Defense. Its separate stat-recalculation helper uses the same mapping. The gym and badge-house text retain Thunder Speed and Soul Defense, and FEATURES describes this code correction. The helper also changes stacking behavior; importing the whole routine would exceed PokéRGB's approved mapping repair.

- [pure · engine/battle/core.asm · lines 6785–6850](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/engine/battle/core.asm#L6785-L6850)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `a58c9db113890c70e7928672559ab35520993d9cbf43a304d719730da742bd68`.
- [pure · text/VermilionGym_2.asm · lines 12–21](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/text/VermilionGym_2.asm#L12-L21)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `946bdf7d6ca018023037b2283cfc6c5e08d15689020719ec4165daadc29a7abf`.
- [pure · text/FuchsiaGym_2.asm · lines 12–21](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/text/FuchsiaGym_2.asm#L12-L21)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `14b539fd2ced2c36319d432239e3c1e31def95d18b49106029cf33aa2147639f`.
- [pure · text/CeruleanBadgeHouse.asm · lines 41–55](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/text/CeruleanBadgeHouse.asm#L41-L55)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `396c56db66bacd5881cf2bf3499beea45943bef25a8f33423a8682f7f217b46b`.
- [pure · FEATURES.md · lines 397–402](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/FEATURES.md#L397-L402)
  Revision: `231abdfcf52e2d1c0ef44f96d497b9b1b1369049`. File SHA-256: `188a80502ad92b3f4201cfbd3c8a840c1a23e8ddab03770cc572df4b570da271`.

<a id="e79"></a>

## E79 — Shin Lite changes badge text and retains the original mapping

**Status:** source-verified at current branch head; no donor ROM build or runtime test. Checked 2026-10-14. Shin Lite retains the sequential Attack, Defense, Speed, Special badge mapping and changes Surge, Koga, and the Cerulean badge-house descriptions to Thunder Defense and Soul Speed. Its separate hard-mode and selective-recalculation changes do not make this a stat-mapping correction.

- [shin-lite · engine/battle/core.asm · lines 7576–7612](https://github.com/jojobear13/shinpokered/blob/b35c2a536a1605841c8fb662aad18b0dbfd2a900/engine/battle/core.asm#L7576-L7612)
  Revision: `b35c2a536a1605841c8fb662aad18b0dbfd2a900`. File SHA-256: `12c421b7e8bf81d658aa2c0845f8e3c0cacd8f60bf79cfc4ff27c9ff46ac3bf4`.
- [shin-lite · wram.asm · lines 44–65](https://github.com/jojobear13/shinpokered/blob/b35c2a536a1605841c8fb662aad18b0dbfd2a900/wram.asm#L44-L65)
  Revision: `b35c2a536a1605841c8fb662aad18b0dbfd2a900`. File SHA-256: `7c88869aad88deca44ee1d21f4b21e70d6f980ffd9283cbf9994535b0cdb9171`.
- [shin-lite · text/maps/vermilion_gym_2.asm · lines 12–21](https://github.com/jojobear13/shinpokered/blob/b35c2a536a1605841c8fb662aad18b0dbfd2a900/text/maps/vermilion_gym_2.asm#L12-L21)
  Revision: `b35c2a536a1605841c8fb662aad18b0dbfd2a900`. File SHA-256: `7f0f5966bc7b6de413599fb41d17b407a49bf10e810e316af1b79b0ec7ba3aed`.
- [shin-lite · text/maps/fuchsia_gym_2.asm · lines 12–21](https://github.com/jojobear13/shinpokered/blob/b35c2a536a1605841c8fb662aad18b0dbfd2a900/text/maps/fuchsia_gym_2.asm#L12-L21)
  Revision: `b35c2a536a1605841c8fb662aad18b0dbfd2a900`. File SHA-256: `caac8de6e17967e45545e41adf4e2e74867d3fc5b5772e8a1edfbf3f7191ea88`.
- [shin-lite · text/maps/cerulean_badge_house.asm · lines 48–77](https://github.com/jojobear13/shinpokered/blob/b35c2a536a1605841c8fb662aad18b0dbfd2a900/text/maps/cerulean_badge_house.asm#L48-L77)
  Revision: `b35c2a536a1605841c8fb662aad18b0dbfd2a900`. File SHA-256: `5d5e25ef76b012adc9d950accae33570f778d029ec5e18debae48f42587b355c`.

<a id="e80"></a>

## E80 — Solus retains the badge mismatch in checked code and text

**Status:** source-verified at current branch head; no donor ROM build or runtime test. Checked 2026-10-14. Solus retains the sequential Thunder Defense and Soul Speed mapping while its Surge, Koga, and badge-house text still says Thunder Speed and Soul Defense. Its TODO candidate wording is not evidence that the mapping correction was implemented.

- [solus · engine/battle/core.asm · lines 6602–6624](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/engine/battle/core.asm#L6602-L6624)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `e594a5249813e75e609be18d60193d7d64e72e56d3cc08057a832f0c37b31e46`.
- [solus · macros/ram.asm · lines 41–61](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/macros/ram.asm#L41-L61)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `336a9de7ec46eaf2a768f9ec7ad7de1911c43a70a73cc26c02ce1d47c8fe8090`.
- [solus · constants/ram_constants.asm · lines 27–37](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/constants/ram_constants.asm#L27-L37)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `376ee332edc56d7ba6a04b98646b0d31f1e3a20862608bb110548a6716983566`.
- [solus · text/VermilionGym_2.asm · lines 12–21](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/text/VermilionGym_2.asm#L12-L21)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `4124c8f028bdba194822cb4ab35b3a3eb0d26abe178d2a18fb6ae3d878a0c709`.
- [solus · text/FuchsiaGym_2.asm · lines 12–21](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/text/FuchsiaGym_2.asm#L12-L21)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `fbe4cb2a66b5842123b70b1ba837ff3838566be7c13d64cd26890085654dbbfd`.
- [solus · text/CeruleanBadgeHouse.asm · lines 48–77](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/text/CeruleanBadgeHouse.asm#L48-L77)
  Revision: `95e157191e920162a24908cc95c358e73d294689`. File SHA-256: `ee0aa7e0a723efcba8f78991d253c4db7f3eb780df84ad73fded4d1989262f35`.

<a id="e81"></a>

## E81 — Solid Red retains the badge mismatch in checked code and text

**Status:** source-verified at current branch head; no donor ROM build or runtime test. Checked 2026-10-14. Solid Red retains the sequential Thunder Defense and Soul Speed mapping while its Surge, Koga, and badge-house text still says Thunder Speed and Soul Defense. This is an observed source state, not evidence of why the maintainer retained it.

- [solidred · engine/battle/core.asm · lines 6667–6689](https://github.com/tustin2121/solidred/blob/18a901695e6d79aafca8e4b793ce70be1fa22853/engine/battle/core.asm#L6667-L6689)
  Revision: `18a901695e6d79aafca8e4b793ce70be1fa22853`. File SHA-256: `551e688140e9d3551ba02fb31b64cb1168088cfa90194c7b52a3f504ee62602f`.
- [solidred · wram.asm · lines 40–60](https://github.com/tustin2121/solidred/blob/18a901695e6d79aafca8e4b793ce70be1fa22853/wram.asm#L40-L60)
  Revision: `18a901695e6d79aafca8e4b793ce70be1fa22853`. File SHA-256: `d4e9993972e37b92d47af380b1b7eb6ea3d1222d918c25b8505ebdb7b05fc769`.
- [solidred · text/maps/VermilionGym_2.asm · lines 12–21](https://github.com/tustin2121/solidred/blob/18a901695e6d79aafca8e4b793ce70be1fa22853/text/maps/VermilionGym_2.asm#L12-L21)
  Revision: `18a901695e6d79aafca8e4b793ce70be1fa22853`. File SHA-256: `2df59f98ff15788fedae08a0874689625d40b5b0dc2a9f6c6fc8b86482813647`.
- [solidred · text/maps/FuchsiaGym_2.asm · lines 12–21](https://github.com/tustin2121/solidred/blob/18a901695e6d79aafca8e4b793ce70be1fa22853/text/maps/FuchsiaGym_2.asm#L12-L21)
  Revision: `18a901695e6d79aafca8e4b793ce70be1fa22853`. File SHA-256: `df9e432564a871bcc1fc6a5e9c8fbb862ad943c4dee09ac2d76977af1eb8c4f0`.
- [solidred · text/maps/CeruleanBadgeHouse.asm · lines 48–77](https://github.com/tustin2121/solidred/blob/18a901695e6d79aafca8e4b793ce70be1fa22853/text/maps/CeruleanBadgeHouse.asm#L48-L77)
  Revision: `18a901695e6d79aafca8e4b793ce70be1fa22853`. File SHA-256: `bbc65e5e922e9b3a909542b49edaa1febe8c151df017fce1de130753c1b748c7`.

<a id="e82"></a>

## E82 — Oak Pokedex rating spelling error and shared callers

**Status:** source-verified text and selection; display correction not implemented. Checked 2026-10-14. The 60–69-owned-species rating contains the misspelling geting. The rating routine counts owned species and selects this entry below the threshold 70, after the threshold 60. Oak PC, Oaks Lab, and the Hall of Fame invoke the shared rating routine. Correct spelling is getting; the original first line has 18 characters and the direct replacement has 19, so layout needs review in each display path. No cause for the original spelling or successful rendering fix is established.

- [pret/pokered · text/pokedex_ratings.asm · lines 58–61](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/text/pokedex_ratings.asm#L58-L61)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `80ab618001df91ac33dd104cbe71777dcc7616679e4592651be230b1672b0ec7`.
- [pret/pokered · engine/events/pokedex_rating.asm · lines 1–34](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/pokedex_rating.asm#L1-L34)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `0578a69883db4172405130ad3401a9143f3e0357e25bd8a72b4216a73aee67ec`.
- [pret/pokered · engine/events/pokedex_rating.asm · lines 58–67](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/pokedex_rating.asm#L58-L67)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `0578a69883db4172405130ad3401a9143f3e0357e25bd8a72b4216a73aee67ec`.
- [pret/pokered · engine/events/pokedex_rating.asm · lines 96–106](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/pokedex_rating.asm#L96-L106)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `0578a69883db4172405130ad3401a9143f3e0357e25bd8a72b4216a73aee67ec`.
- [pret/pokered · engine/menus/oaks_pc.asm · lines 1–15](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/oaks_pc.asm#L1-L15)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `0373241e916807e7a8a09436d1a91743fe137b8e3c9930039e0e89cbd01f3318`.
- [pret/pokered · scripts/OaksLab.asm · lines 976–983](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/OaksLab.asm#L976-L983)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `4c3d62602ef212c2c16d10fa46f27e246b6ac954afc8670feae82f0181e53bbe`.
- [pret/pokered · engine/movie/hall_of_fame.asm · lines 209–215](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/movie/hall_of_fame.asm#L209-L215)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `dd0e29c1f9968e2934a9abd96a5881b85727bb37d7a92df6e96977c340aa8e0b`.

<a id="e83"></a>

## E83 — PC STATS and selected-Pokemon cancellation return paths

**Status:** source-verified control flow; no executable menu regression. Checked 2026-10-14. The PC STATS branch restores the selected-Pokemon action menu and loops there. B or CANCEL clears carry; the deposit and withdrawal callers jump to BillsPCMenu on that result, bypassing their Pokemon list. The shared action menu also clears the saved list index and scroll offset. Successful transfers separately return to the PC main menu. This supports a scoped browsing-return repair, not a claim that STATS immediately exits the PC.

- [pret/pokered · engine/pokemon/bills_pc.asm · lines 135–146](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/bills_pc.asm#L135-L146)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f123f75a572c33887a28637eab894588f04a546593f61f07f4716ff9ae361ccf`.
- [pret/pokered · engine/pokemon/bills_pc.asm · lines 207–226](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/bills_pc.asm#L207-L226)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f123f75a572c33887a28637eab894588f04a546593f61f07f4716ff9ae361ccf`.
- [pret/pokered · engine/pokemon/bills_pc.asm · lines 250–291](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/bills_pc.asm#L250-L291)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f123f75a572c33887a28637eab894588f04a546593f61f07f4716ff9ae361ccf`.
- [pret/pokered · engine/pokemon/bills_pc.asm · lines 324–339](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/bills_pc.asm#L324-L339)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f123f75a572c33887a28637eab894588f04a546593f61f07f4716ff9ae361ccf`.
- [pret/pokered · engine/pokemon/bills_pc.asm · lines 382–447](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/bills_pc.asm#L382-L447)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f123f75a572c33887a28637eab894588f04a546593f61f07f4716ff9ae361ccf`.

<a id="e84"></a>

## E84 — STATS input and party, PC, battle, and trade callers

**Status:** source-verified control flow; no executable menu regression. Checked 2026-10-14. Each original status page waits for A or B through WaitForTextScrollButtonPress. The party, PC, battle, and trade paths call StatusScreen and StatusScreen2 in sequence. The party caller returns to its party menu after both pages. These checked paths provide no directional page/Pokemon controller; the proposed common controller must preserve each callers context and constraints.

- [pret/pokered · engine/pokemon/status_screen.asm · lines 64–77](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/status_screen.asm#L64-L77)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f147e9ccd9fc4c71534f73139921efd9c2e134408f13a5dee84a0691d1bfd77a`.
- [pret/pokered · engine/pokemon/status_screen.asm · lines 165–176](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/status_screen.asm#L165-L176)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f147e9ccd9fc4c71534f73139921efd9c2e134408f13a5dee84a0691d1bfd77a`.
- [pret/pokered · engine/pokemon/status_screen.asm · lines 421–432](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/status_screen.asm#L421-L432)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f147e9ccd9fc4c71534f73139921efd9c2e134408f13a5dee84a0691d1bfd77a`.
- [pret/pokered · home/joypad2.asm · lines 55–83](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/joypad2.asm#L55-L83)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `c6168008e870799b849de0e663280a9946c2e694818fbe48d9389afa24c9f709`.
- [pret/pokered · engine/menus/start_sub_menus.asm · lines 9–30](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/start_sub_menus.asm#L9-L30)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `cce764b4234f1f2a97c8062654061a7af759e5ed9567ddb9c980776166c0c8d5`.
- [pret/pokered · engine/menus/start_sub_menus.asm · lines 96–103](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/start_sub_menus.asm#L96-L103)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `cce764b4234f1f2a97c8062654061a7af759e5ed9567ddb9c980776166c0c8d5`.
- [pret/pokered · engine/pokemon/bills_pc.asm · lines 432–447](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/bills_pc.asm#L432-L447)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f123f75a572c33887a28637eab894588f04a546593f61f07f4716ff9ae361ccf`.
- [pret/pokered · engine/battle/core.asm · lines 2365–2375](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L2365-L2375)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.
- [pret/pokered · engine/link/cable_club.asm · lines 625–633](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/link/cable_club.asm#L625-L633)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `2d2148185a0548d9e3b2f994afc55d47a47739cdb5e7e49427ae625beac4e5af`.

<a id="e85"></a>

## E85 — Release confirmation default and removal order

**Status:** source-verified control flow; no executable menu regression. Checked 2026-10-14. BillsPCRelease calls the standard YesNoChoice. That initializer selects YES_NO_MENU without setting the second-option-default bit, and DisplayTwoOptionMenu initializes selection zero unless that bit is set. Release checks the result before calling RemovePokemon. Declining returns to the release list. The accepted safeguard can change this caller without globally changing Yes/No defaults.

- [pret/pokered · engine/pokemon/bills_pc.asm · lines 293–318](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/bills_pc.asm#L293-L318)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f123f75a572c33887a28637eab894588f04a546593f61f07f4716ff9ae361ccf`.
- [pret/pokered · home/yes_no.asm · lines 1–18](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/yes_no.asm#L1-L18)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `4411c6348297140339fdd758ef72811384cb308ae618ef37182d3fc7ae29c9b2`.
- [pret/pokered · engine/menus/text_box.asm · lines 217–235](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/text_box.asm#L217-L235)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `fe5e3f320fd2e0fa1a5eb38eef21166f26d8c929da22cf73a5344ac16365c636`.
- [pret/pokered · engine/menus/text_box.asm · lines 316–336](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/text_box.asm#L316-L336)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `fe5e3f320fd2e0fa1a5eb38eef21166f26d8c929da22cf73a5344ac16365c636`.

<a id="e86"></a>

## E86 — Selected menu cancellation, failure, and completed-action returns

**Status:** source-verified control flow; no executable menu regression. Initially checked 2026-10-14; cited files rechecked against pinned Git bytes on 2026-10-15. Outside-battle party action CANCEL exits to the Start menu while B returns to the party list. Medicine returns through its caller to the bag. Mart quantity cancellation and price refusal return to BUY/SELL lists, but an unsellable-item refusal or purchase failure for money/bag space returns to BUY/SELL/QUIT. Player PC item deposit and withdrawal quantity cancellation, failure, and success return to their item lists. These different paths require individual decisions; none proves a global keep-open rule.

- [pret/pokered · engine/menus/start_sub_menus.asm · lines 60–81](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/start_sub_menus.asm#L60-L81)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `cce764b4234f1f2a97c8062654061a7af759e5ed9567ddb9c980776166c0c8d5`.
- [pret/pokered · engine/menus/start_sub_menus.asm · lines 408–423](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/start_sub_menus.asm#L408-L423)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `cce764b4234f1f2a97c8062654061a7af759e5ed9567ddb9c980776166c0c8d5`.
- [pret/pokered · engine/items/item_effects.asm · lines 1226–1253](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L1226-L1253)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.
- [pret/pokered · engine/events/pokemart.asm · lines 69–94](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/pokemart.asm#L69-L94)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `94c0f7c02cb6d5d1b8e6adf98b49eb8848561f1225cc6b95bb426ce9db9e5abc`.
- [pret/pokered · engine/events/pokemart.asm · lines 113–121](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/pokemart.asm#L113-L121)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `94c0f7c02cb6d5d1b8e6adf98b49eb8848561f1225cc6b95bb426ce9db9e5abc`.
- [pret/pokered · engine/events/pokemart.asm · lines 150–178](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/pokemart.asm#L150-L178)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `94c0f7c02cb6d5d1b8e6adf98b49eb8848561f1225cc6b95bb426ce9db9e5abc`.
- [pret/pokered · engine/events/pokemart.asm · lines 199–219](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/pokemart.asm#L199-L219)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `94c0f7c02cb6d5d1b8e6adf98b49eb8848561f1225cc6b95bb426ce9db9e5abc`.
- [pret/pokered · engine/menus/players_pc.asm · lines 108–138](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/players_pc.asm#L108-L138)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f6b13c32e7bde9ccf0036e4ce42a78b4ae8d2e8a83bfe607b807f4410905ae59`.
- [pret/pokered · engine/menus/players_pc.asm · lines 162–192](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/players_pc.asm#L162-L192)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f6b13c32e7bde9ccf0036e4ce42a78b4ae8d2e8a83bfe607b807f4410905ae59`.

<a id="e87"></a>

## E87 — Repel expiry and use baseline for an optional renewal prompt

**Status:** source-verified control flow; no executable menu regression. Checked 2026-10-14. The original last-Repel-step path stores zero, displays the expiry text, and returns without another item prompt. Repel item use sets the counter and removes one item; ordinary, Super, and Max Repel use 100, 200, and 250 respectively. The encounter gate compares the wild level with the leading party Pokemon. A same-kind renewal prompt is a separate optional feature; changing Max Repel to suppress every wild encounter would exceed it.

- [pret/pokered · engine/battle/wild_encounters.asm · lines 19–24](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/wild_encounters.asm#L19-L24)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `5d1522885ae5a67fc4e077e8ee8ff2bac76f7011360d02a7354599326209f16d`.
- [pret/pokered · engine/battle/wild_encounters.asm · lines 81–102](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/wild_encounters.asm#L81-L102)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `5d1522885ae5a67fc4e077e8ee8ff2bac76f7011360d02a7354599326209f16d`.
- [pret/pokered · engine/items/item_effects.asm · lines 1532–1541](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L1532-L1541)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.
- [pret/pokered · engine/items/item_effects.asm · lines 1622–1628](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L1622-L1628)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.

<a id="e88"></a>

## E88 — Hidden 40-coin event and award conversion

The Game Corner event passes COIN + 40, but its conversion selects the 20-coin branch. Both the award and printed converted amount use 20; the 40 branch exists but is not selected.

Status: source-verified. Checked 2026-10-15; no executable regression is claimed.

- [pret/pokered · data/events/hidden_events.asm · lines 282–298](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/events/hidden_events.asm#L282-L298)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `1ca366dcbba1be0f4b19696be8aeb9eed8158e75bd852d4faf2119231a836877`.
- [pret/pokered · engine/events/hidden_items.asm · lines 52–142](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/hidden_items.asm#L52-L142)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `0489317c55b1488c02a58f1518f221df6b6b0eda79dd9b4828852a8fd55809a3`.
- [pret/pokered · data/text/text_2.asm · lines 764–783](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/text/text_2.asm#L764-L783)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `ba97e54e9feafb22816b449841181b64234537bac9ccdef6aa3d79f4153e23b9`.

<a id="e89"></a>

## E89 — Vending check uses the wrong price

The vending menu checks 200 before loading the selected drink price of 200, 300, or 350. Successful item insertion precedes subtraction of the actual price. Shared BCD subtraction clamps an underflow to zero; this is an underpayment path, not a wrapped-money reward.

Status: source-verified. Checked 2026-10-15; no executable regression is claimed.

- [pret/pokered · engine/events/vending_machine.asm · lines 33–82](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/vending_machine.asm#L33-L82)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `172f768af47b74de79a2f09d46b69ac7ef87c119b9f9a74ed334bb3c353dadf8`.
- [pret/pokered · engine/events/vending_machine.asm · lines 115–133](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/vending_machine.asm#L115-L133)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `172f768af47b74de79a2f09d46b69ac7ef87c119b9f9a74ed334bb3c353dadf8`.
- [pret/pokered · data/items/vending_prices.asm · lines 1–10](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/items/vending_prices.asm#L1-L10)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `55556209d5dcf801187b558dac99b24fbc2fb7c4158d5a41e0ebca86eb9e7925`.
- [pret/pokered · home/money.asm · lines 1–8](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/money.asm#L1-L8)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `1551c37e27bf0b9b206c596a267b1aef3b8c2029b5cc689e02ca126af84e9af9`.
- [pret/pokered · engine/math/bcd.asm · lines 166–218](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/math/bcd.asm#L166-L218)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `66d3c45fa971cb429f633cc49a2a644d718348d032237b12388512423991199f`.

<a id="e90"></a>

## E90 — Oak gift and conditional Parcel delivery failure

Oak sets the five-ball gift flag before GiveItem and does not branch on failure; the gift has distinct ownership, rival, and item conditions. The Parcel script also ignores the result. GiveItem propagates inventory failure. Full-bag reachability must be assessed separately; an ordinary early-game Parcel softlock is not established.

Status: source-verified. Checked 2026-10-15; no executable regression is claimed.

- [pret/pokered · scripts/OaksLab.asm · lines 967–1034](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/OaksLab.asm#L967-L1034)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `4c3d62602ef212c2c16d10fa46f27e246b6ac954afc8670feae82f0181e53bbe`.
- [pret/pokered · scripts/ViridianMart.asm · lines 47–64](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/ViridianMart.asm#L47-L64)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `be36a6b0486b28d81c7f5ad61759561a750b674568963d3895d83818ec808c0a`.
- [pret/pokered · home/give.asm · lines 1–17](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/give.asm#L1-L17)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `8cfb75843694f5f32294534b766ce3c0dec1272c8cc00755050348ad38604b07`.
- [pret/pokered · engine/items/inventory.asm · lines 7–103](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/inventory.asm#L7-L103)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `410632e0a82e3491fd6d2898c337eb4a8e83ce6a1b31dad0a12bf887a27a3f7e`.

<a id="e91"></a>

## E91 — Trade evolution follow-up and its users

The Poliwhirl and Raichu trade entries use the evolution dialogue set. Its follow-up says the given Pokemon evolved. The Raichu statement conflicts with the retained species rules; comments about Japanese localization are reconstruction notes rather than original developer testimony.

Status: source-verified. Checked 2026-10-15; no executable regression is claimed.

- [pret/pokered · data/events/trades.asm · lines 1–28](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/events/trades.asm#L1-L28)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `e3c374712f6eb119bda9097d1d08ffdb9447b1691b4f8b3e9042fde4c5563fb4`.
- [pret/pokered · engine/events/in_game_trades.asm · lines 255–269](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/in_game_trades.asm#L255-L269)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `4d96264f01a6888e5fd1d5faaaf9997691b0a05bf6f178d4283a1fcb7860afae`.
- [pret/pokered · engine/events/in_game_trades.asm · lines 326–328](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/in_game_trades.asm#L326-L328)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `4d96264f01a6888e5fd1d5faaaf9997691b0a05bf6f178d4283a1fcb7860afae`.
- [pret/pokered · data/text/text_7.asm · lines 140–147](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/text/text_7.asm#L140-L147)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `8fcfc31197c3c75c248474eab47378573ffb4546406cc957c7e913cf0eb07cfe`.

<a id="e92"></a>

## E92 — Oak gift instruction line commands

Oak throwing instructions use two successive bottom-line commands. The line macro writes at the bottom line while cont scrolls; the string sequence therefore overwrites a line rather than scrolling it.

Status: source-verified. Checked 2026-10-15; no executable regression is claimed.

- [pret/pokered · text/OaksLab.asm · lines 123–150](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/text/OaksLab.asm#L123-L150)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `004c4c4e0bdd47c1d8024f53439e7d0e03ab3d94d0b7ea4e72f817558b22fafa`.
- [pret/pokered · macros/scripts/text.asm · lines 1–23](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/macros/scripts/text.asm#L1-L23)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `4caac5f525b936d1db4dbd4af400fa26643c549c314d05b87491d98558ba7d46`.

<a id="e93"></a>

## E93 — Nidorino picture and Nidorina cry

Oak speech loads the Nidorino picture but issues sound_cry_nidorina. The shared sound command maps to Nidorina. A corrected command needs a caller and listening check.

Status: source-verified. Checked 2026-10-15; no executable regression is claimed.

- [pret/pokered · engine/movie/oak_speech/oak_speech.asm · lines 75–85](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/movie/oak_speech/oak_speech.asm#L75-L85)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `c41bc3cfd25612d683eae8b95f6e9ba2ef37792c2bfe28ccfbadb15aee8f7b77`.
- [pret/pokered · engine/movie/oak_speech/oak_speech.asm · lines 172–177](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/movie/oak_speech/oak_speech.asm#L172-L177)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `c41bc3cfd25612d683eae8b95f6e9ba2ef37792c2bfe28ccfbadb15aee8f7b77`.
- [pret/pokered · home/text.asm · lines 507–557](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/text.asm#L507-L557)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `1d04789b7fea0f80374b7f8efaf97e1bfdf5f374201a3dd102a21957bcd69f89`.
- [pret/pokered · macros/scripts/text.asm · lines 153–158](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/macros/scripts/text.asm#L153-L158)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `4caac5f525b936d1db4dbd4af400fa26643c549c314d05b87491d98558ba7d46`.

<a id="e94"></a>

## E94 — Poke Flute wild-opponent feedback

Poke Flute clears active opponent sleep after party scans, but its response flag is set by those scans. In a wild battle with only the opponent asleep and all scanned slots awake, the opponent can wake while the catchy-tune response is selected and the wake-up confirmation is omitted. The literal words no effect are not displayed; the waking effect itself succeeds.

Status: source-verified. Checked 2026-10-15; no executable regression is claimed.

- [pret/pokered · engine/items/item_effects.asm · lines 1706–1775](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L1706-L1775)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.
- [pret/pokered · data/text/text_6.asm · lines 94–110](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/text/text_6.asm#L94-L110)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `780a4113660b6ed4c3fa54ddd2a984e1dc7d6bea7f423a00d5a476dfaf5f80ec`.

<a id="e95"></a>

## E95 — Trainer item status clearing and display paths

Full Heal and Full Restore clear enemy status through AICureStatus. Item output prints text; the restoration display helper updates HP, without a status-area redraw in these paths. The timing and visible stale status still need an executable capture; no AI replacement is implied.

Status: source-verified. Checked 2026-10-15; no executable regression is claimed.

- [pret/pokered · engine/battle/trainer_ai.asm · lines 463–485](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/trainer_ai.asm#L463-L485)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `12f090abd33e3f227cdc4f24d165ad35b6abaf694ea3f5f1a526f9d7505e140d`.
- [pret/pokered · engine/battle/trainer_ai.asm · lines 546–552](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/trainer_ai.asm#L546-L552)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `12f090abd33e3f227cdc4f24d165ad35b6abaf694ea3f5f1a526f9d7505e140d`.
- [pret/pokered · engine/battle/trainer_ai.asm · lines 619–637](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/trainer_ai.asm#L619-L637)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `12f090abd33e3f227cdc4f24d165ad35b6abaf694ea3f5f1a526f9d7505e140d`.
- [pret/pokered · engine/battle/trainer_ai.asm · lines 727–742](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/trainer_ai.asm#L727-L742)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `12f090abd33e3f227cdc4f24d165ad35b6abaf694ea3f5f1a526f9d7505e140d`.

<a id="e96"></a>

## E96 — Spin animation pointer mismatch

The up/down spin callers store animation state and enter PlayerSpinWhileMovingUpOrDown without restoring the facing-list pointer. SpinPlayerSprite initially reads HL as the image index source. The pointer mismatch is source-confirmed; DMG/SGB appearance and the correction need display checks.

Status: source-verified. Checked 2026-10-15; no executable regression is claimed.

- [pret/pokered · engine/overworld/player_animations.asm · lines 83–111](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/overworld/player_animations.asm#L83-L111)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `73aa2824e0340db2b54aa38f3dd2200f72ace80428770b70e0f5ff6ddf04a0e7`.
- [pret/pokered · engine/overworld/player_animations.asm · lines 274–299](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/overworld/player_animations.asm#L274-L299)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `73aa2824e0340db2b54aa38f3dd2200f72ace80428770b70e0f5ff6ddf04a0e7`.
- [pret/pokered · engine/overworld/player_animations.asm · lines 319–348](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/overworld/player_animations.asm#L319-L348)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `73aa2824e0340db2b54aa38f3dd2200f72ace80428770b70e0f5ff6ddf04a0e7`.

<a id="e97"></a>

## E97 — Existing list controls and machine information

Bag and item-PC capacities are 20 and 50. List rendering uses machine number names; machine use reveals the move before teaching and the party screen shows learnability. Invalid or known targets return without consuming a TM. Quantity controls use up/down with wrap; Pokedex already pages left/right. The checked floor menu lists destinations without a current-floor marker. Move replacement selects and commits a non-HM move with B available to cancel.

Status: source-verified. Checked 2026-10-15; no executable regression is claimed.

- [pret/pokered · constants/menu_constants.asm · lines 1–2](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/constants/menu_constants.asm#L1-L2)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `fbd0e91bd6ac5f8a491a4d5df3ccbc4438f34c234ce9be684f82b2537c6022ac`.
- [pret/pokered · home/names.asm · lines 27–90](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/names.asm#L27-L90)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `8a6f1d06f7a658417cb6b5e4d0d75915c53a77326d4a3bbc281b45096d1e1ced`.
- [pret/pokered · home/list_menu.asm · lines 40–67](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/list_menu.asm#L40-L67)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `43f046e47dfa086a753dc9843d00e8fa69c07da226baa3b4cd7ed80476f187ac`.
- [pret/pokered · home/list_menu.asm · lines 197–270](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/list_menu.asm#L197-L270)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `43f046e47dfa086a753dc9843d00e8fa69c07da226baa3b4cd7ed80476f187ac`.
- [pret/pokered · home/list_menu.asm · lines 338–400](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/list_menu.asm#L338-L400)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `43f046e47dfa086a753dc9843d00e8fa69c07da226baa3b4cd7ed80476f187ac`.
- [pret/pokered · engine/items/item_effects.asm · lines 2154–2253](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L2154-L2253)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.
- [pret/pokered · engine/menus/party_menu.asm · lines 59–113](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/party_menu.asm#L59-L113)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `7f8f73f570f013c61f64291bf25e4fc7f3c252acb9ee4bb28f77cfa069c3a33c`.
- [pret/pokered · engine/menus/pokedex.asm · lines 314–344](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/pokedex.asm#L314-L344)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `4f42306e04786f5030259e44c0f2599107bf49cf0851e64f532032b24a0601e1`.
- [pret/pokered · engine/events/elevator.asm · lines 1–48](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/elevator.asm#L1-L48)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `7665819f6a4f7667d4cf268a45e28a2142d83b70ff14ddbdb52fe99e8b04af6f`.
- [pret/pokered · data/text/text_2.asm · lines 1356–1359](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/text/text_2.asm#L1356-L1359)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `ba97e54e9feafb22816b449841181b64234537bac9ccdef6aa3d79f4153e23b9`.
- [pret/pokered · engine/pokemon/learn_move.asm · lines 90–190](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/learn_move.asm#L90-L190)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f4e7973a87e6c0e74a2ce819eb6096121aca5ce7de7d4c040e8a5049cd31d8b6`.

<a id="e98"></a>

## E98 — Snorlax interaction and manual Flute event

The Route 12/16 Snorlax interaction prints sleeping-Pokemon text. Manual Poke Flute use checks map, event, and adjacent coordinates before setting the respective fight event. A contextual prompt is a proposed shorter route to the same owned-item action, not existing behavior.

Status: source-verified. Checked 2026-10-15; no executable regression is claimed.

- [pret/pokered · scripts/Route12.asm · lines 99–102](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/Route12.asm#L99-L102)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `1b937c27e470eae534a15360de17f9955d9ba93f2207fbfe0f65ab4a68b0bc99`.
- [pret/pokered · scripts/Route16.asm · lines 203–205](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/Route16.asm#L203-L205)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f126da884812271d59f245011f909db0ce67132b71068cdfc5d4eb2b18eccf4d`.
- [pret/pokered · text/Route12.asm · lines 1–4](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/text/Route12.asm#L1-L4)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `45261377911e2802a9429f19e957bad7c8d81a3cbc14d3051475bbcb5e3ca1d9`.
- [pret/pokered · engine/items/item_effects.asm · lines 1671–1705](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L1671-L1705)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.

<a id="e99"></a>

## E99 — Money gates and Yellow Safari alternatives

English Red/Blue rejects Safari admission below 500 and Saffron guard routes require a carried drink. English Yellow includes positive low-balance admission and repeated zero-balance dialogue ending in one ball with the ordinary step budget. These source paths do not by themselves prove a permanent Red/Blue deadlock or settle a recovery design.

Status: source-verified. Checked 2026-10-15; no executable regression is claimed.

- [pret/pokered · scripts/SafariZoneGate.asm · lines 148–208](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/SafariZoneGate.asm#L148-L208)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `8dda5c961d7c69b6b43d60896154b6239da5bb5792fbd00c4bed31a6f081f21b`.
- [pret/pokered · scripts/Route5Gate.asm · lines 19–45](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/Route5Gate.asm#L19-L45)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `6872a5bcf34643acba02adc3d159551e30b932da6ee25b127c687c0e491f9af3`.
- [pret/pokered · engine/events/saffron_guards.asm · lines 1–15](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/saffron_guards.asm#L1-L15)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `919336e3f646a11482ac96a85ea913ba6aca44b75bea7fe4efb32594e5600f29`.
- [pret/pokered · data/items/guard_drink_items.asm · lines 1–5](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/items/guard_drink_items.asm#L1-L5)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `131066a067a0c0225ebb56acc3447892b7fcabde5f1284395c0f7adc6ced74c4`.
- [pret/pokeyellow · scripts/SafariZoneGate_2.asm · lines 1–75](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/scripts/SafariZoneGate_2.asm#L1-L75)
  Revision: `e89ead154b9968aa50eed9328ff2b38b6c194382`. File SHA-256: `981945fadb3d1042c80dc0bdd6dd054c5c8b6ed077e79cc085deb80180cad857`.
- [pret/pokeyellow · scripts/SafariZoneGate_2.asm · lines 182–208](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/scripts/SafariZoneGate_2.asm#L182-L208)
  Revision: `e89ead154b9968aa50eed9328ff2b38b6c194382`. File SHA-256: `981945fadb3d1042c80dc0bdd6dd054c5c8b6ed077e79cc085deb80180cad857`.

<a id="e100"></a>

## E100 — Existing capacity, naming, and Day Care safeguards

Ordinary object and hidden-item pickups check delivery before hiding/setting completion. Oak aide rewards report bag failure. Pokemon gifts check party and current-box capacity. Selected game-corner prizes subtract coins only after delivery. The Name Rater can cancel and checks original owner; Day Care rejects a last party member or HM user and checks return room, price confirmation, and funds.

Status: source-verified. Checked 2026-10-15; no executable regression is claimed.

- [pret/pokered · engine/events/pick_up_item.asm · lines 24–54](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/pick_up_item.asm#L24-L54)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `8fc66f26679af548c850da55e71eb2c66cb2b985d49b3bebff4b6807d6bb8f7a`.
- [pret/pokered · engine/events/hidden_items.asm · lines 22–49](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/hidden_items.asm#L22-L49)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `0489317c55b1488c02a58f1518f221df6b6b0eda79dd9b4828852a8fd55809a3`.
- [pret/pokered · engine/events/oaks_aide.asm · lines 20–49](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/oaks_aide.asm#L20-L49)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `12a41675113518037f1b06fcaa95500cbe90511fff55b685d98da85c4ea60c2d`.
- [pret/pokered · engine/events/give_pokemon.asm · lines 1–55](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/give_pokemon.asm#L1-L55)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `99789f756812f8db1c99f3142126bc2f27cae3f8ee9144d8c5cd3326f6a3e50b`.
- [pret/pokered · engine/events/prize_menu.asm · lines 198–249](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/prize_menu.asm#L198-L249)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `fcc20f1fd9cae5963935420293a4ba7bd585ea3f427f2a6d412f35e26cd8bc26`.
- [pret/pokered · scripts/BluesHouse.asm · lines 38–70](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/BluesHouse.asm#L38-L70)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `7c3a981b70074127febffbc7a4b4db512abd30739a07f46294b1dbc51debbcf1`.
- [pret/pokered · scripts/NameRatersHouse.asm · lines 12–89](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/NameRatersHouse.asm#L12-L89)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `4fa2b867072cad028c96d99c9bb1d5a22d6ed5a9f58122d2d68bbb3c1214e316`.
- [pret/pokered · scripts/Daycare.asm · lines 18–46](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/Daycare.asm#L18-L46)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `ba236f94460202ac5c1033ee524ba47e9fa8d3eee13f44bbeefac5aff58d52f8`.
- [pret/pokered · scripts/Daycare.asm · lines 110–158](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/Daycare.asm#L110-L158)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `ba236f94460202ac5c1033ee524ba47e9fa8d3eee13f44bbeefac5aff58d52f8`.

<a id="e101"></a>

## E101 — Rooftop drink payment precedes TM delivery

All three Red/Blue rooftop exchanges remove a drink before GiveItem. A refusal leaves the reward flag clear but does not restore the drink. Removing a final unit frees its slot; a remaining drink stack does not. The checked ordinary path does not show a duplicate TM award. FireRed also removes the drink before its TM-space check, under different pocket rules. The FireRed vending paths check the selected price of 200, 300, or 350 before the common delivery path.

Status: source-verified. Checked 2026-10-15; no executable regression or proof of original intent is claimed.

- [pokered · scripts/CeladonMartRoof.asm · lines 72–135](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/CeladonMartRoof.asm#L72-L135)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `e1d6d3b5c7e72d4883e16cf1110e7f76435dda75c1cdea00d4c0e557a8020460`.
- [pokered · engine/menus/pc.asm · lines 117–141](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/pc.asm#L117-L141)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `c9fcc183298831a6ee0584556a0ceacc974d56466337b67a2e15483848a92052`.
- [pokered · engine/items/inventory.asm · lines 7–149](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/inventory.asm#L7-L149)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `410632e0a82e3491fd6d2898c337eb4a8e83ce6a1b31dad0a12bf887a27a3f7e`.
- [pokered · home/give.asm · lines 1–17](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/give.asm#L1-L17)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `8cfb75843694f5f32294534b766ce3c0dec1272c8cc00755050348ad38604b07`.
- [firered-reference · data/maps/CeladonCity_DepartmentStore_Roof/scripts.inc · lines 110–175](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/CeladonCity_DepartmentStore_Roof/scripts.inc#L110-L175)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `9b789b64abc864565c382faef027f3c94e1cc6158aee37870e6abd8f5a8ace42`.
- [firered-reference · data/maps/CeladonCity_DepartmentStore_Roof/scripts.inc · lines 219–260](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/CeladonCity_DepartmentStore_Roof/scripts.inc#L219-L260)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `9b789b64abc864565c382faef027f3c94e1cc6158aee37870e6abd8f5a8ace42`.

<a id="e102"></a>

## E102 — Move information in Red/Blue, Gold/Silver, and FireRed

Red/Blue machine names use numbers; teaching reveals the move, some gift dialogue names it, and battle move selection already displays type and PP. The checked original interfaces lack a general power/accuracy/description viewer. Gold/Silver TM browsing prints move names and descriptions. FireRed TM Case displays name, description, type, power, accuracy, and PP; its TM shop displays the move name before purchase. Original Rock Slide and Tri Attack records use NO_ADDITIONAL_EFFECT; descriptions must not import their later secondary effects.

Status: source-verified. Checked 2026-10-15; no executable regression or proof of original intent is claimed.

- [pokered · engine/battle/core.asm · lines 2885–2920](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L2885-L2920)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.
- [pokered · engine/items/item_effects.asm · lines 2154–2198](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L2154-L2198)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.
- [pokered · text/CeladonMartRoof.asm · lines 24–34](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/text/CeladonMartRoof.asm#L24-L34)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `eac729872eb23f00fac43380437aa0d1ad4615326453dd345ce4edb8870373db`.
- [pokegold-reference · engine/items/tmhm.asm · lines 241–254](https://github.com/pret/pokegold/blob/ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8/engine/items/tmhm.asm#L241-L254)
  Revision: `ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8`. File SHA-256: `055705349e83d655b010362cf87443c3cf60ca9c0632592bcfdd70145d977332`.
- [pokegold-reference · engine/items/tmhm.asm · lines 375–385](https://github.com/pret/pokegold/blob/ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8/engine/items/tmhm.asm#L375-L385)
  Revision: `ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8`. File SHA-256: `055705349e83d655b010362cf87443c3cf60ca9c0632592bcfdd70145d977332`.
- [firered-reference · src/tm_case.c · lines 649–746](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/src/tm_case.c#L649-L746)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `3dad9224df99f5432f37ca80b752da0f41a0d60dabeddc839309588c188a324c`.
- [firered-reference · src/tm_case.c · lines 1531–1584](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/src/tm_case.c#L1531-L1584)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `3dad9224df99f5432f37ca80b752da0f41a0d60dabeddc839309588c188a324c`.
- [firered-reference · src/shop.c · lines 616–631](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/src/shop.c#L616-L631)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `d326d1498cad7fc610f483237a3ff17b0d27836dcf8213960b41bbd2b58844f8`.
- [pokered · data/moves/moves.asm · lines 169–175](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/moves/moves.asm#L169-L175)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `a2cf3e1ec6bf4b5caaeeec974967691c9eb47923d1e7432fb0267ba7d3a5931f`.

<a id="e103"></a>

## E103 — Quantity shortcuts, capacities, and elevator comparisons

Red/Blue quantity input has unit steps and wrapping, not tens; its shared elevator menu does not exclude the entered floor. Constants distinguish bag 20 slots, item PC 50 slots, party six, and box 20 Pokemon. Gold/Silver and FireRed implement left/right minus/plus ten with clamping. FireRed draws the current floor and bypasses travel animation for a same-floor selection in the Department Store elevator.

Status: source-verified. Checked 2026-10-15; no executable regression or proof of original intent is claimed.

- [pokered · home/list_menu.asm · lines 197–270](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/list_menu.asm#L197-L270)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `43f046e47dfa086a753dc9843d00e8fa69c07da226baa3b4cd7ed80476f187ac`.
- [pokered · engine/events/elevator.asm · lines 1–48](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/elevator.asm#L1-L48)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `7665819f6a4f7667d4cf268a45e28a2142d83b70ff14ddbdb52fe99e8b04af6f`.
- [pokered · constants/menu_constants.asm · lines 1–2](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/constants/menu_constants.asm#L1-L2)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `fbd0e91bd6ac5f8a491a4d5df3ccbc4438f34c234ce9be684f82b2537c6022ac`.
- [pokered · constants/pokemon_data_constants.asm · lines 58–60](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/constants/pokemon_data_constants.asm#L58-L60)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `69edbf30b07a0cbcba55911fa3bd1eae8e625daab61413b3e8e0e4706d4ba013`.
- [pokegold-reference · engine/items/buy_sell_toss.asm · lines 45–123](https://github.com/pret/pokegold/blob/ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8/engine/items/buy_sell_toss.asm#L45-L123)
  Revision: `ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8`. File SHA-256: `a246d8c9476133e00bdc800036ddb00864c80aff6076b207e6e41a1c5ee692a8`.
- [firered-reference · src/menu_helpers.c · lines 169–234](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/src/menu_helpers.c#L169-L234)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `ac404f7061de3041529435f0a5012f263846ed9514e6c39575aa9bc0654191c7`.
- [firered-reference · data/maps/CeladonCity_DepartmentStore_Elevator/scripts.inc · lines 4–115](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/CeladonCity_DepartmentStore_Elevator/scripts.inc#L4-L115)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `b385c9a3ea17406633bb03d3bad860adfd9762e97445772a45eb2af9c850cc6a`.
- [firered-reference · src/field_specials.c · lines 1094–1116](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/src/field_specials.c#L1094-L1116)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `9c49d3702f0f4dcba61ae26bccefce1c26fbd1247475289dd821780bc537d1d9`.

<a id="e104"></a>

## E104 — Expansion battle information and original Game Boy inputs

Current Emerald Expansion enables the move-description feature with L as its default button. Rendering includes category, power, accuracy, and description. A separate type-display setting defaults to never, with always/seen/caught alternatives; enabled type icons cover living battlers and use a public-type policy. Game Boy input has directions, A, B, Start, and Select, with no L/R shoulders. A PokéRGB port needs its own controls and information policy. Red/Blue VBlank calls Random and its generator reads the divider; different elapsed inspection time can change background randomness even if the panel makes no battle-random call.

Status: source-verified. Checked 2026-10-15; no executable regression or proof of original intent is claimed.

- [expansion-info · include/config/battle.h · lines 321–322](https://github.com/rh-hideout/pokeemerald-expansion/blob/73b3fbeb574327cd9420c89e56bef5aa3c08fead/include/config/battle.h#L321-L322)
  Revision: `73b3fbeb574327cd9420c89e56bef5aa3c08fead`. File SHA-256: `7600c4622f7d154aef50f74bb8fd20fbd5aa84a928557fa1feadd14bda34861a`.
- [expansion-info · include/config/battle.h · lines 360–361](https://github.com/rh-hideout/pokeemerald-expansion/blob/73b3fbeb574327cd9420c89e56bef5aa3c08fead/include/config/battle.h#L360-L361)
  Revision: `73b3fbeb574327cd9420c89e56bef5aa3c08fead`. File SHA-256: `7600c4622f7d154aef50f74bb8fd20fbd5aa84a928557fa1feadd14bda34861a`.
- [expansion-info · include/config/battle.h · lines 429–433](https://github.com/rh-hideout/pokeemerald-expansion/blob/73b3fbeb574327cd9420c89e56bef5aa3c08fead/include/config/battle.h#L429-L433)
  Revision: `73b3fbeb574327cd9420c89e56bef5aa3c08fead`. File SHA-256: `7600c4622f7d154aef50f74bb8fd20fbd5aa84a928557fa1feadd14bda34861a`.
- [expansion-info · src/battle_controller_player.c · lines 881–906](https://github.com/rh-hideout/pokeemerald-expansion/blob/73b3fbeb574327cd9420c89e56bef5aa3c08fead/src/battle_controller_player.c#L881-L906)
  Revision: `73b3fbeb574327cd9420c89e56bef5aa3c08fead`. File SHA-256: `9a5c8c1ce7db906526ae176ce7b389be46cafafe17724afa2b5e2e82a65f6bb3`.
- [expansion-info · src/battle_controller_player.c · lines 1750–1800](https://github.com/rh-hideout/pokeemerald-expansion/blob/73b3fbeb574327cd9420c89e56bef5aa3c08fead/src/battle_controller_player.c#L1750-L1800)
  Revision: `73b3fbeb574327cd9420c89e56bef5aa3c08fead`. File SHA-256: `9a5c8c1ce7db906526ae176ce7b389be46cafafe17724afa2b5e2e82a65f6bb3`.
- [expansion-info · src/type_icons.c · lines 235–277](https://github.com/rh-hideout/pokeemerald-expansion/blob/73b3fbeb574327cd9420c89e56bef5aa3c08fead/src/type_icons.c#L235-L277)
  Revision: `73b3fbeb574327cd9420c89e56bef5aa3c08fead`. File SHA-256: `abe23acf382e4540aa0aaa08365170b13119487d6a5326883e6133562b042a03`.
- [expansion-info · src/type_icons.c · lines 294–335](https://github.com/rh-hideout/pokeemerald-expansion/blob/73b3fbeb574327cd9420c89e56bef5aa3c08fead/src/type_icons.c#L294-L335)
  Revision: `73b3fbeb574327cd9420c89e56bef5aa3c08fead`. File SHA-256: `abe23acf382e4540aa0aaa08365170b13119487d6a5326883e6133562b042a03`.
- [pandocs · src/Joypad_Input.md · lines 3–14](https://github.com/gbdev/pandocs/blob/0191af06ac49661587dcde3d57a241a626b8df75/src/Joypad_Input.md#L3-L14)
  Revision: `0191af06ac49661587dcde3d57a241a626b8df75`. File SHA-256: `516fe8be99da1a33e12e34be5477f8bdaa1232203c1dc6589d0b572a0065e7c3`.
- [pokered · engine/battle/core.asm · lines 2553–2570](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L2553-L2570)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.
- [pokered · home/vblank.asm · lines 29–40](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/vblank.asm#L29-L40)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `8ec851d6eadb1137352f42312068cebc26b28d188bc63358c53c22086e83a8ca`.
- [pokered · home/random.asm · lines 1–12](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/random.asm#L1-L12)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `34a706de61f4ac1178a82773c0e45dfcf656eb1b12ee5c0754b5cec221f493e6`.
- [pokered · engine/math/random.asm · lines 1–13](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/math/random.asm#L1-L13)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `2c22bd5a75dd0adb7cae5ba2e65d8bb8767219bf76df3a7f2094b8bb60398f9d`.

<a id="e105"></a>

## E105 — Selected remake clues and their limits

FireRed has an interaction-triggered Flute prompt at Snorlax after the acquisition flag. Its Game Corner map encodes a 40-coin floor entry at different coordinates. Oak instructions use paged text. The intro uses Nidoran female for both picture and cry, not Red/Blue Nidorino. The optional five-ball gift calls an add-item/message macro and then sets completion, without a caller failure branch. These selected paths neither prove 1996 intent nor establish every remake path as safe.

Status: source-verified. Checked 2026-10-15; no executable regression or proof of original intent is claimed.

- [firered-reference · data/maps/Route12/scripts.inc · lines 13–50](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/Route12/scripts.inc#L13-L50)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `ea70631fa17e3042cf08b32c94fbc26fbb128936b61c00e61127b79af780368e`.
- [firered-reference · data/maps/CeladonCity_GameCorner/map.json · lines 295–305](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/CeladonCity_GameCorner/map.json#L295-L305)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `e0924467ae57d2fce051f3959bf1526bcb0befce6a6c39a51162aa2089f555ee`.
- [firered-reference · data/maps/PalletTown_ProfessorOaksLab/text.inc · lines 189–196](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/PalletTown_ProfessorOaksLab/text.inc#L189-L196)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `fb03a0a75876da386c54137e2eeed0dfb0da0d6fdaf3bc8c66cd83d36c2d724f`.
- [firered-reference · src/oak_speech.c · lines 20–20](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/src/oak_speech.c#L20-L20)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `859bbe7637670a663a089c198d1519ac833145306d1c4b8a1ae83e754eb9be53`.
- [firered-reference · src/oak_speech.c · lines 1193–1196](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/src/oak_speech.c#L1193-L1196)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `859bbe7637670a663a089c198d1519ac833145306d1c4b8a1ae83e754eb9be53`.
- [firered-reference · src/oak_speech.c · lines 1887–1889](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/src/oak_speech.c#L1887-L1889)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `859bbe7637670a663a089c198d1519ac833145306d1c4b8a1ae83e754eb9be53`.
- [firered-reference · data/maps/PalletTown_ProfessorOaksLab/scripts.inc · lines 918–938](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/PalletTown_ProfessorOaksLab/scripts.inc#L918-L938)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `ed6e02fdd179af05159f27288ef9b5226ce7917c03ae54e8fb8d83c853fc311d`.
- [firered-reference · asm/macros/event.inc · lines 1818–1822](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/asm/macros/event.inc#L1818-L1822)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `848e5e791adeddbe7ae7fe2717729af666a8d8aa163ab7781c74bfd49ce58671`.

<a id="e106"></a>

## E106 — Item-list cursor resets after stack removal and shop returns

PC deposits and withdrawals return to their corresponding item-list loop. When removal empties a stack, the shared inventory routine zeros current and saved row/scroll state; its partial-stack branch skips those writes. PC withdrawals, shop sales, and bag/PC tossing also use this helper. Shop buy/sell list loops separately zero the current visible row, including after quantity cancellation or a declined price. A correct return destination therefore does not establish cursor or viewport preservation. List selection combines row and scroll offset, so restoring a stale index after deletion is unsafe.

Status: source-verified at the retained English Red/Blue reference. Checked 2026-10-20; no game implementation or executable reproduction is claimed.

- [pokered · engine/menus/players_pc.asm · lines 86–138](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/players_pc.asm#L86-L138)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f6b13c32e7bde9ccf0036e4ce42a78b4ae8d2e8a83bfe607b807f4410905ae59`.
- [pokered · engine/menus/players_pc.asm · lines 140–241](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/players_pc.asm#L140-L241)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f6b13c32e7bde9ccf0036e4ce42a78b4ae8d2e8a83bfe607b807f4410905ae59`.
- [pokered · engine/items/inventory.asm · lines 95–149](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/inventory.asm#L95-L149)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `410632e0a82e3491fd6d2898c337eb4a8e83ce6a1b31dad0a12bf887a27a3f7e`.
- [pokered · engine/events/pokemart.asm · lines 53–112](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/pokemart.asm#L53-L112)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `94c0f7c02cb6d5d1b8e6adf98b49eb8848561f1225cc6b95bb426ce9db9e5abc`.
- [pokered · engine/events/pokemart.asm · lines 134–172](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/pokemart.asm#L134-L172)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `94c0f7c02cb6d5d1b8e6adf98b49eb8848561f1225cc6b95bb426ce9db9e5abc`.
- [pokered · engine/menus/start_sub_menus.asm · lines 310–324](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/start_sub_menus.asm#L310-L324)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `cce764b4234f1f2a97c8062654061a7af759e5ed9567ddb9c980776166c0c8d5`.
- [pokered · engine/menus/start_sub_menus.asm · lines 424–439](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/start_sub_menus.asm#L424-L439)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `cce764b4234f1f2a97c8062654061a7af759e5ed9567ddb9c980776166c0c8d5`.
- [pokered · engine/items/item_effects.asm · lines 2547–2588](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L2547-L2588)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.
- [pokered · home/list_menu.asm · lines 98–112](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/list_menu.asm#L98-L112)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `43f046e47dfa086a753dc9843d00e8fa69c07da226baa3b4cd7ed80476f187ac`.

<a id="e107"></a>

## E107 — Bag relocation, 60-slot arithmetic, and save layout

The retained source has separate bag 20 and item-PC 50 capacities, two bytes per entry, a count byte, and a terminator. It contains a 128-byte reserved span within saved main data. The upstream wiki tutorial relocates a 50-slot bag into that span while retaining 42 bytes at the original location. Applying the same representation, 60 slots need 122 bytes and leave six; 63 is the arithmetic capacity of that particular 128-byte span, not a verified engine-wide limit. Item insertion already reads separate destination capacities. The main-data block is saved/loaded as bytes, so relocating the bag changes where its contents live in a save even if surrounding offsets and total block size are preserved. The tutorial warns of save/editor incompatibility. No 60-slot game build, runtime test, safe migration, or complete PC-expansion design is established here.

Status: source-verified allocation/tutorial and derived arithmetic, checked 2026-10-20. A small allocation proposal is not a passing 60-slot implementation.

- [pokered · constants/menu_constants.asm · lines 1–2](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/constants/menu_constants.asm#L1-L2)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `fbd0e91bd6ac5f8a491a4d5df3ccbc4438f34c234ce9be684f82b2537c6022ac`.
- [pokered · ram/wram.asm · lines 1747–1762](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/ram/wram.asm#L1747-L1762)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `00683cd430a9ef30794d2aeaee51f3a5440e4bb14dca13e9f9cb5fa88f130e34`.
- [pokered · ram/wram.asm · lines 1831–1839](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/ram/wram.asm#L1831-L1839)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `00683cd430a9ef30794d2aeaee51f3a5440e4bb14dca13e9f9cb5fa88f130e34`.
- [pokered · ram/wram.asm · lines 1893–1899](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/ram/wram.asm#L1893-L1899)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `00683cd430a9ef30794d2aeaee51f3a5440e4bb14dca13e9f9cb5fa88f130e34`.
- [pokered · engine/items/inventory.asm · lines 7–93](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/inventory.asm#L7-L93)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `410632e0a82e3491fd6d2898c337eb4a8e83ce6a1b31dad0a12bf887a27a3f7e`.
- [pokered · ram/sram.asm · lines 12–24](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/ram/sram.asm#L12-L24)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `de4bb57acb8d9c06a087ce2c5c85be78a2790160521ce5807c10008d0769f66a`.
- [pokered · engine/menus/save.asm · lines 59–67](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/save.asm#L59-L67)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `54f98d6e16733c593376da81d4bebe2fad7d4408b4a93aa163e167c09d5fa6fb`.
- [pokered · engine/menus/save.asm · lines 216–240](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/menus/save.asm#L216-L240)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `54f98d6e16733c593376da81d4bebe2fad7d4408b4a93aa163e167c09d5fa6fb`.
- [pokered-wiki · Increase-Bag-Space.md · lines 1–48](https://github.com/pret/pokered/wiki/Increase-Bag-Space)
  Revision: `727fc7788550c4b279501c17ee177681f7366077`. File SHA-256: `31041ba434507c04609f08fb0c4167d2dc1b824d19c40cd12f77e9f53733deae`.
- [pokered-wiki · Increase-Bag-Space.md · lines 79–88](https://github.com/pret/pokered/wiki/Increase-Bag-Space)
  Revision: `727fc7788550c4b279501c17ee177681f7366077`. File SHA-256: `31041ba434507c04609f08fb0c4167d2dc1b824d19c40cd12f77e9f53733deae`.

<a id="e108"></a>

## E108 — Separate bag reserve with fixed surrounding addresses

The original bag count is at D31D, entries start at D31E, its terminator is at D346, and money starts at D347: no adjacent spare bytes exist. Increasing only the capacity to 21 keeps the bag start but moves money to D349; 40 and 60 exceed the fixed stack boundary in a RAM-only link. The retained source also has adjacent 78- and 56-byte reserves after wRoute18Gate1FCurScript. Overlaying those 134 bytes with a four-byte format marker, count, entries, and terminator supports 60 and 64 entries while preserving all other existing WRAM labels, including wGameProgressFlagsEnd. A 65-entry variant fails the explicit allocation assertion. The 64-entry bound applies to this allocation and marker, not the whole engine. This audit links RAM objects with RGBDS 1.0.4, omits the OAM DMA section defined in a game-code object, and compares WRAM addresses only. It does not implement a playable feature or verify saves, runtime callers, bulk reserve access, or optional-feature combinations. D36 separately accepts the allocation design.

Status: source-verified and RAM-allocation checked; no full ROM or gameplay test. Checked 2026-10-23. See the [method](bag-memory.md) and [recorded result](bag-memory-audit.json).

- [pokered · ram/wram.asm · lines 1757–1763](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/ram/wram.asm#L1757-L1763)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `00683cd430a9ef30794d2aeaee51f3a5440e4bb14dca13e9f9cb5fa88f130e34`.
- [pokered · ram/wram.asm · lines 2035–2048](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/ram/wram.asm#L2035-L2048)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `00683cd430a9ef30794d2aeaee51f3a5440e4bb14dca13e9f9cb5fa88f130e34`.
- [pokered · layout.link · lines 180–193](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/layout.link#L180-L193)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `70c20fcaa2fb04b007589c8fc512fdf3e9141d90b05bab955f39582f12ac9bf9`.
- [pokered · Makefile · lines 146–161](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/Makefile#L146-L161)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `ae29c23b88a65bc5a734296ebb45cee2e1fb6cba2663e3d29c81e3e1461cfec7`.
- [pokered · ram/sram.asm · lines 12–24](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/ram/sram.asm#L12-L24)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `de4bb57acb8d9c06a087ce2c5c85be78a2790160521ce5807c10008d0769f66a`.

<a id="e109"></a>

## E109 — Expanded-bag initialization after game-progress clearing

InitPlayerData initializes the bag count and end marker before clearing the game-progress range with FillMemory. The selected 134-byte reserve begins after wRoute18Gate1FCurScript and spans 78 bytes before wGameProgressFlagsEnd plus 56 after it. The existing clear therefore includes the first 78 bytes of the relocated bag allocation. With a four-byte format marker followed by the count and entries, that clear would erase the initial marker, count, and end marker if their initialization remained before it. FillMemory writes the supplied byte across the requested range. The expanded bag and its format marker must be initialized after that clear while retaining the original progress boundary and disabled path. This is source and allocation reasoning, not a reproduced game failure, tested repair, or feature-combination result.

Status: source-verified initializer order and allocation overlap; no runtime test. Checked 2026-10-23.

- [pokered · engine/movie/oak_speech/init_player_data.asm · lines 15–55](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/movie/oak_speech/init_player_data.asm#L15-L55)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `57293a3865b842621d69429577b22cc272062ee4a66384acb05a6c5bbbc3f1e3`.

- [pokered · ram/wram.asm · lines 2035–2048](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/ram/wram.asm#L2035-L2048)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `00683cd430a9ef30794d2aeaee51f3a5440e4bb14dca13e9f9cb5fa88f130e34`.

- [pokered · home/tilemap.asm · lines 1–13](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/tilemap.asm#L1-L13)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f54f294c75f9c824c9f6a2178cba39ff53da47e59c5e397998e268d36a88010b`.

<a id="e110"></a>

## E110 — Battle move-swap cursor reloads the previous selection

The regular move menu initializes wCurrentMenuItem from the zero-based wPlayerMoveListIndex plus one. SELECT goes to SwapMovesInMenu. Its first-SELECT branch stores the current row in wMenuItemToSwap and jumps back to MoveSelectionMenu; its completed-swap branch clears the swap marker and makes the same jump. Neither branch updates wPlayerMoveListIndex first, so the redraw restores an earlier menu selection, often the first move, rather than necessarily a hard-coded first row. The swap itself exchanges battle and party move/PP bytes and remaps the disabled-move slot. Link battle input excludes SELECT. PN-021 changes cursor retention only; the existing swap, battle state, and input restrictions require regression tests.

Status: source-verified redraw and swap state; no runtime reproduction. Checked 2026-10-24.

- [pokered · engine/battle/core.asm · lines 2534–2578](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L2534-L2578)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.

- [pokered · engine/battle/core.asm · lines 2608–2636](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L2608-L2636)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.

- [pokered · engine/battle/core.asm · lines 2762–2836](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L2762-L2836)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `36d8ff785fe642d61f6917156e70b78c36fd7cde6c0b8fb582e02f6552e786d0`.

<a id="e111"></a>

## E111 — New boxed Pokemon prepend while party deposits append

A successful capture with a full party calls SendNewMonToBox. That routine increments the box count, shifts species, OT names, nicknames, and records, then writes the newcomer and its nickname into slot one. GivePokemon calls the same routine when the party is full and the box has space. Bill's PC deposits instead call MoveMon with PARTY_TO_BOX; _MoveMon writes at the former box count, appending the species, record, OT, and nickname. This confirms the reported ordering difference, but does not establish the original design reason or prove the insertion behavior was an accident. PN-022 selects consistent append behavior as a Core usability choice. Any change must update the destination for every associated record component and the nickname prompt, including the shared gift caller.

Status: source-verified insertion paths and shared callers; no runtime test or original-intent proof. Checked 2026-10-24.

- [pokered · engine/items/item_effects.asm · lines 548–567](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L548-L567)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.

- [pokered · engine/items/item_effects.asm · lines 2648–2824](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L2648-L2824)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.

- [pokered · engine/pokemon/add_mon.asm · lines 341–391](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/add_mon.asm#L341-L391)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `4a0c02fbbfdd6dc1e9357069be2b4b94342777de94efb2a67bd4e25ca62bddfe`.

- [pokered · engine/pokemon/add_mon.asm · lines 428–472](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/add_mon.asm#L428-L472)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `4a0c02fbbfdd6dc1e9357069be2b4b94342777de94efb2a67bd4e25ca62bddfe`.

- [pokered · engine/pokemon/bills_pc.asm · lines 207–235](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/bills_pc.asm#L207-L235)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f123f75a572c33887a28637eab894588f04a546593f61f07f4716ff9ae361ccf`.

- [pokered · engine/events/give_pokemon.asm · lines 1–43](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/give_pokemon.asm#L1-L43)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `99789f756812f8db1c99f3142126bc2f27cae3f8ee9144d8c5cd3326f6a3e50b`.

<a id="e112"></a>

## E112 — Mansion Burglars have zero sight range; Scientists retain sight checks

The Mansion has three Burglar objects, on 2F, 3F, and B1F, whose trainer headers all set view range zero. The Scientist objects on 1F, 3F, and B1F instead have view ranges three, two, and three. All four maps use CheckFightingMapTrainers in their normal script paths, and their trainer text handlers call TalkToTrainer. The trainer macro encodes its range argument as a shifted byte; CheckForEngagingTrainers passes that byte to TrainerEngage. The sight check rejects nonzero player distance beyond the configured range. Thus the zero-range Burglars require talking, while undefeated Scientists can initiate when the normal visibility, direction, alignment, and distance conditions hold. This is specific trainer data rather than an absent Mansion-wide sight routine. The pattern does not prove the original developers' reason or rule out an authoring mistake. D39/PN-023 separately selects the current scoped Core correction.

Status: source-verified six trainer settings and engagement paths; original design reason unverified. Checked 2026-10-24.

- [pokered · scripts/PokemonMansion1F.asm · lines 58–81](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/PokemonMansion1F.asm#L58-L81)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `d53baf06e11c15389c029c4df48fc96138ce33106047a37015969a37e710bc76`.

- [pokered · scripts/PokemonMansion2F.asm · lines 55–78](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/PokemonMansion2F.asm#L55-L78)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `d97470b6268f8aaf6f40f66e463598d451bdb908235c1ca3581b27160cf30a95`.

- [pokered · scripts/PokemonMansion3F.asm · lines 1–108](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/PokemonMansion3F.asm#L1-L108)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `7dc1ec6550e44cb5547bfacab735ece88310f9d9d9ff0ae758c17d13c552bde7`.

- [pokered · scripts/PokemonMansionB1F.asm · lines 54–92](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/PokemonMansionB1F.asm#L54-L92)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `6f1f73b30bded5a8cef8b5ce6191eaaeb8b4a0b2398955bec024d4f8a376a551`.

- [pokered · data/maps/objects/PokemonMansion1F.asm · lines 21–24](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/maps/objects/PokemonMansion1F.asm#L21-L24)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `8ca114b2e8ca7bd2e3f939cb25b6b5d02c3d28228832ad0e5e1b505f9e3ec0d2`.

- [pokered · data/maps/objects/PokemonMansion2F.asm · lines 18–22](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/maps/objects/PokemonMansion2F.asm#L18-L22)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `e318e9cc7e598be3d508487041e3cce83bcdeead98048fbd6ea67bc3ab3bbaa2`.

- [pokered · data/maps/objects/PokemonMansion3F.asm · lines 18–23](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/maps/objects/PokemonMansion3F.asm#L18-L23)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `cc04594eb9682dfdf33c57076a4919d1ca989a0a126d0aaaa0cab46cf0d724f1`.

- [pokered · data/maps/objects/PokemonMansionB1F.asm · lines 19–26](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/maps/objects/PokemonMansionB1F.asm#L19-L26)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `eff8c91005e5e952dafd48258637e326ef2fbd6b4067041f38bd3663d2e8ae44`.

- [pokered · macros/scripts/maps.asm · lines 112–126](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/macros/scripts/maps.asm#L112-L126)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `9e072d8990debe2e919ef22b161636cbd12c8b061671c7f58f08fcc4668cdb21`.

- [pokered · home/trainers.asm · lines 84–120](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/trainers.asm#L84-L120)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `12357588c651ca94b54375f0adb436806a8e83beb277cccbc5e3700060d7785b`.

- [pokered · home/trainers.asm · lines 257–301](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/trainers.asm#L257-L301)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `12357588c651ca94b54375f0adb436806a8e83beb277cccbc5e3700060d7785b`.

- [pokered · engine/overworld/trainer_sight.asm · lines 164–232](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/overworld/trainer_sight.asm#L164-L232)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `46b748a6c991ec7a7bb6fb65ca217d4fb6b8ebdb274c6105d2991c7b92c099fd`.

- [pokered · engine/overworld/trainer_sight.asm · lines 254–283](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/overworld/trainer_sight.asm#L254-L283)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `46b748a6c991ec7a7bb6fb65ca217d4fb6b8ebdb274c6105d2991c7b92c099fd`.

<a id="e113"></a>

## E113 — Ordinary zero-range trainers and the Mansion remake comparison

Zero sight range is used for ordinary optional trainers outside the Mansion. In Red/Blue the facing Jr. Trainer pair on Route 6 and all four Route 21 Fishers have range zero. The Route 6 dialogue describes a private conversation, providing context consistent with talking to interrupt it. At the retained Gold/Silver reference, Bird Keeper Bryan on Route 35 and Cooltrainer Lois at the Lake of Rage are normal trainer objects with sight range zero; their script headers identify ordinary battles, and the common sight routine compares distance with the configured range. Yellow retains zero for all three Mansion Burglars. FireRed/LeafGreen instead assigns Arnie, Simon, and Lewis normal trainer type and sight range one, with their scripts identifying them as Burglars; its normal trainer-sight path consumes that range. This establishes that ordinary talk-to-battle encounters exist beyond these three NPCs and that the remake changes their behavior. It does not identify the original reason for the Mansion settings or establish whether the later change was a correction or a redesign. The Gen 1 pattern plausibly reflects an intentional encounter choice, but the range value and Yellow continuity alone cannot prove original intent. D39/PN-023 separately sets the current Core disposition; this comparison does not prove original intent. These are source comparisons without runtime tests or original development records.

Status: source-verified cross-game settings; original intent remains an inference. Checked 2026-10-25. See the [intent comparison](cursor-box-and-trainers.md#how-strong-is-the-evidence-for-intent).

- [pokered · scripts/Route6.asm · lines 26–39](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/Route6.asm#L26-L39)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `c5a87742f56da7b865b3cc0997bcdcdb8a35d0802ff08b69b45688e17cad6158`.

- [pokered · data/maps/objects/Route6.asm · lines 21–27](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/maps/objects/Route6.asm#L21-L27)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `eb56bea8e58d1c3c9bbac519ac93c5a8349378d0e997e918d0fd4b67a9b04ec1`.

- [pokered · text/Route6.asm · lines 1–25](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/text/Route6.asm#L1-L25)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `f9069589e7213acce191afe22fc795d57a414153511abaceca9b9f921a78b3aa`.

- [pokered · scripts/Route21.asm · lines 28–47](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/Route21.asm#L28-L47)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `6d73124abb625ad3d9be8c34851e11d613de6b9b5e727b89e076d406ce71276a`.

- [pokered · data/maps/objects/Route21.asm · lines 19–28](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/maps/objects/Route21.asm#L19-L28)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `9001ae6f965c477a5e476daeb4e2b7e4c2d239d52a8379251cabb2ed80f0ec74`.

- [pokeyellow · scripts/PokemonMansion2F.asm · lines 68–72](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/scripts/PokemonMansion2F.asm#L68-L72)
  Revision: `e89ead154b9968aa50eed9328ff2b38b6c194382`. File SHA-256: `d97470b6268f8aaf6f40f66e463598d451bdb908235c1ca3581b27160cf30a95`.

- [pokeyellow · scripts/PokemonMansion3F.asm · lines 95–101](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/scripts/PokemonMansion3F.asm#L95-L101)
  Revision: `e89ead154b9968aa50eed9328ff2b38b6c194382`. File SHA-256: `7dc1ec6550e44cb5547bfacab735ece88310f9d9d9ff0ae758c17d13c552bde7`.

- [pokeyellow · scripts/PokemonMansionB1F.asm · lines 74–80](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/scripts/PokemonMansionB1F.asm#L74-L80)
  Revision: `e89ead154b9968aa50eed9328ff2b38b6c194382`. File SHA-256: `6f1f73b30bded5a8cef8b5ce6191eaaeb8b4a0b2398955bec024d4f8a376a551`.

- [pokegold-reference · maps/Route35.asm · lines 19–27](https://github.com/pret/pokegold/blob/ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8/maps/Route35.asm#L19-L27)
  Revision: `ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8`. File SHA-256: `e993e99e601e1e6deb55bfb3c42d7f4c957ac8473948eecc9d3c117944142648`.

- [pokegold-reference · maps/Route35.asm · lines 455–463](https://github.com/pret/pokegold/blob/ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8/maps/Route35.asm#L455-L463)
  Revision: `ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8`. File SHA-256: `e993e99e601e1e6deb55bfb3c42d7f4c957ac8473948eecc9d3c117944142648`.

- [pokegold-reference · maps/LakeOfRage.asm · lines 179–187](https://github.com/pret/pokegold/blob/ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8/maps/LakeOfRage.asm#L179-L187)
  Revision: `ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8`. File SHA-256: `075e549f48de35908372840db3962f208e0f32ec84bf9ea58a5fa22860e21237`.

- [pokegold-reference · maps/LakeOfRage.asm · lines 515–518](https://github.com/pret/pokegold/blob/ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8/maps/LakeOfRage.asm#L515-L518)
  Revision: `ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8`. File SHA-256: `075e549f48de35908372840db3962f208e0f32ec84bf9ea58a5fa22860e21237`.

- [pokegold-reference · home/trainers.asm · lines 13–58](https://github.com/pret/pokegold/blob/ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8/home/trainers.asm#L13-L58)
  Revision: `ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8`. File SHA-256: `3f669be4d255b4fecb4e23df60cebe4a0d5442c51b013e726868dbc400bfc5dd`.

- [firered-reference · data/maps/PokemonMansion_2F/map.json · lines 19–31](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/PokemonMansion_2F/map.json#L19-L31)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `5dd26a290a4a605e280049c57c41d72d4043063234fea346c143fcdd9b3f48ce`.

- [firered-reference · data/maps/PokemonMansion_2F/scripts.inc · lines 27–30](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/PokemonMansion_2F/scripts.inc#L27-L30)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `562a72b9965ec681851f0095ece4d7153131792cc972389fb0446bac4de7432e`.

- [firered-reference · data/maps/PokemonMansion_3F/map.json · lines 19–31](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/PokemonMansion_3F/map.json#L19-L31)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `fcea30babbe644b0e71b3cda5ce34a4359719c15564a4350a5df40de9dec0ff4`.

- [firered-reference · data/maps/PokemonMansion_3F/scripts.inc · lines 23–26](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/PokemonMansion_3F/scripts.inc#L23-L26)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `da06fb1af43eecb922cdf5b70e8776366397b7b6456cd855871f182e00bc3ec7`.

- [firered-reference · data/maps/PokemonMansion_B1F/map.json · lines 33–45](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/PokemonMansion_B1F/map.json#L33-L45)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `4c4c7322e422d1a1fcf39d0bd86e10c0ee01eb6ea1e02f32c3c7824860fab1e2`.

- [firered-reference · data/maps/PokemonMansion_B1F/scripts.inc · lines 23–26](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/PokemonMansion_B1F/scripts.inc#L23-L26)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `7ac39b6051667cd7eb05c05bb0c4b47483445080f4fc36560cee96d35676cd26`.

- [firered-reference · src/trainer_see.c · lines 88–145](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/src/trainer_see.c#L88-L145)
  Revision: `037335f4c725d7c9aecdac87066f2002b4bd7e14`. File SHA-256: `a76f1c34613e7badbe4beffa4dbc31f6e7233f3e33a0d03e4a3ebc64d2746a9c`.

<a id="e114"></a>

## E114 — Route 21 Fishermen face adjacent water

All four Route 21 Fisher objects stand at a water edge and face the immediately adjacent water/shore square. Fisher1 is at (4,24), faces left toward (3,24); Fisher2 is at (6,25), faces down toward (6,26); Fisher3 is at (14,56), faces left toward (13,56); Fisher4 is at (17,57), faces right toward (18,57). The retained 10-by-45 block map and overworld blockset place water graphic tile 0x14 in the forward squares. Fisher2 faces a shoreline square with a shore lip in its top row and water in its bottom row; the other three forward squares are entirely water. The source water helper identifies 0x14 as water. Rendering the source map confirms both land-patch edges. This is source/geometry evidence without a running-game test. The fishing context supplies a plausible reason for their passivity, so these Fishers should not be used to infer the Mansion Burglars' original intent. E113's zero-range data remains valid, while the analogy is qualified by this context. Original Mansion intent remains unproven; D39/PN-023 separately selects the current Core correction.

Status: source geometry decoded and visually checked; original intent unproven. Checked 2026-10-25. See the [recorded geometry](route21-fisher-geometry.json).

- [pokered · data/maps/objects/Route21.asm · lines 19–28](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/maps/objects/Route21.asm#L19-L28)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `9001ae6f965c477a5e476daeb4e2b7e4c2d239d52a8379251cabb2ed80f0ec74`.

- [pokered · constants/map_constants.asm · lines 62–62](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/constants/map_constants.asm#L62-L62)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `4129ef4e6908267e554c0308254f2269f1fb8f75b5c529faad6fd14c92119271`.

- [pokered · engine/items/item_effects.asm · lines 2826–2851](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/items/item_effects.asm#L2826-L2851)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `76b570b5216bbbcf6d9528c4704d931744a3740cce88afdc4f4f8f700449dda1`.

- [pokered · maps/Route21.blk · 450 bytes, binary](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/maps/Route21.blk)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `fa7abd7efe3f9d2332da34f5f31774d6984555fc9dbc808ea164b43dc5f5a1fa`.

- [pokered · gfx/blocksets/overworld.bst · 2048 bytes, binary](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/gfx/blocksets/overworld.bst)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `c4f6d88cc7dea8196aa51d3aa059c6d1da0ea45718dd12870fcddee9f9304d50`.

- [pokered · gfx/tilesets/overworld.png · 1309 bytes, binary](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/gfx/tilesets/overworld.png)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `580a310bef9f446c62d75994db3197b3f511aeed5f055ded9f38c36c8a152bdb`.

- [pokered · data/maps/headers/Route21.asm · lines 1–4](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/maps/headers/Route21.asm#L1-L4)
  Revision: `af519899719f0754965776faac0e836a3b906e6d`. File SHA-256: `cb8638c60b2875827519242f1e02f7dcdccc0973a77d7b0ce005701ef75bbd88`.

<a id="e115"></a>

## E115 — Viridian Forest star grass fails the encounter gate

Red/Blue's encounter gate samples the lower-right 8-pixel tile of a 16-pixel walking square, while player grass priority samples the lower-left. The Forest grass ID is 0x20. Decoding the 17-by-24 block Viridian Forest map finds 365 walking squares with lower-left grass; 114 have decorative star tile 0x34 at lower-right and fail the Red/Blue grass gate. The other 251 match at both corners. The FOREST fallback rejects the affected squares before the encounter roll. Yellow samples lower-left, with identical Viridian Forest map bytes and Forest blockset bytes and the same grass ID. Source graphics show 0x34 as the alternate grass pattern. These facts strongly support a missed grass-recognition case. No original developer statement or running-game test was established. D40/PN-024 accepts a scoped Core repair; code choice and neighboring-case checks remain engineering work.

Status: source-verified; map decoded and graphics inspected; intent strongly inferred. Checked 2026-10-25. See the [focused review](forest-encounters.md) and [map audit](forest-encounter-audit.json).

- [pokered · engine/battle/wild_encounters.asm · lines 25–53](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/wild_encounters.asm#L25-L53)
- [pokered · engine/battle/wild_encounters.asm · lines 63–72](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/wild_encounters.asm#L63-L72)
- [pokered · engine/overworld/movement.asm · lines 10–17](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/overworld/movement.asm#L10-L17)
- [pokered · engine/overworld/movement.asm · lines 86–99](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/overworld/movement.asm#L86-L99)
- [pokered · data/tilesets/tileset_headers.asm · lines 1–15](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/tilesets/tileset_headers.asm#L1-L15)
- [pokered · constants/map_constants.asm · lines 83–90](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/constants/map_constants.asm#L83-L90)
- [pokeyellow · engine/battle/wild_encounters.asm · lines 25–38](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/engine/battle/wild_encounters.asm#L25-L38)
- [pokeyellow · data/tilesets/tileset_headers.asm · lines 9–15](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/data/tilesets/tileset_headers.asm#L9-L15)
- [pokered · maps/ViridianForest.blk · 408 bytes, binary](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/maps/ViridianForest.blk)
- [pokered · gfx/blocksets/forest.bst · 2048 bytes, binary](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/gfx/blocksets/forest.bst)
- [pokered · gfx/tilesets/forest.png · 1414 bytes, binary](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/gfx/tilesets/forest.png)
- [pokeyellow · maps/ViridianForest.blk · 408 bytes, binary](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/maps/ViridianForest.blk)
- [pokeyellow · gfx/blocksets/forest.bst · 2048 bytes, binary](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/gfx/blocksets/forest.bst)
- [pokeyellow · gfx/tilesets/forest.png · 1414 bytes, binary](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/gfx/tilesets/forest.png)

<a id="e116"></a>

## E116 — Acid Armor erases the active picture in English Red, Blue, and Yellow

Acid Armor uses the normal two-stage Defense increase. The successful move plays a dedicated animation that sinks the user and overwrites the displayed battle picture with blank graphics. The animation can hide the ordinary picture, Minimize picture, or Substitute. The user remains active and susceptible to attacks. SameBoy ran 48 cases across Red and Blue in Game Boy mode and Yellow in Game Boy and Game Boy Color modes. Tests checked both sides, animations on and off, use at the Defense stage limit, Minimize, Substitute, and follow-up hits. In 18 additional cases, the picture stayed absent for three ordinary turns and reappeared after Transform or when the hidden Substitute broke.

Checked on 2026-11-22. See the [Acid Armor review](acid-armor.md).

The [baseline test results](acid-armor-baseline.json) record the 66 stock-ROM cases.

- [pokered · data/moves/moves.asm · lines 164–164](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/moves/moves.asm#L164)
- [pokered · data/moves/effects_pointers.asm · lines 53–58](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/moves/effects_pointers.asm#L53-L58)
- [pokered · engine/battle/effects.asm · lines 351–386](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/effects.asm#L351-L386)
- [pokered · engine/battle/effects.asm · lines 457–498](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/effects.asm#L457-L498)
- [pokered · engine/battle/effects.asm · lines 998–1022](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/effects.asm#L998-L1022)
- [pokered · data/moves/animations.asm · lines 1074–1076](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/moves/animations.asm#L1074-L1076)
- [pokered · engine/battle/animations.asm · lines 421–437](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/animations.asm#L421-L437)
- [pokered · engine/battle/animations.asm · lines 1757–1782](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/animations.asm#L1757-L1782)
- [pokered · engine/battle/animations.asm · lines 1864–1873](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/animations.asm#L1864-L1873)
- [pokered · engine/battle/animations.asm · lines 1980–2008](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/animations.asm#L1980-L2008)
- [pokered · engine/battle/animations.asm · lines 2022–2057](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/animations.asm#L2022-L2057)
- [pokeyellow · data/moves/animations.asm · lines 1069–1071](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/data/moves/animations.asm#L1069-L1071)
- [pokeyellow · engine/battle/animations.asm · lines 436–449](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/engine/battle/animations.asm#L436-L449)
- [pokeyellow · engine/battle/animations.asm · lines 1843–1868](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/engine/battle/animations.asm#L1843-L1868)

<a id="e117"></a>

## E117 — Acid Armor animation history and evidence for intent

The checked Japanese Red, Green, and Blue sources use the same sink-and-erase path. The move name means melt or dissolve. The Japanese Red and Green Pokédex describes Vaporeon disappearing when it dissolves in water. The Acid Armor entry on printed page 106 of the Nintendo Red & Blue Player’s Guide describes a temporary Defense boost and leaves sprite duration unspecified. Gold and Silver explicitly show the battler again after the effect. FireRed and LeafGreen fade the picture back in and restore the sprite. The original melt is deliberate. The shared erase routine explains how the picture stays blank in Gen I. The intended duration remains unproven. The timing and reload tests in E119 favor a missing restoration after the melt.

Checked on 2026-11-22. See the [Acid Armor review](acid-armor.md).

- [pokegreen-jp · README.md · lines 1–12](https://github.com/Narishma-gb/pokegreen/blob/953f41b34108621b2bf13c3b1e53abfc9c3e5aec/README.md#L1-L12)
- [pokegreen-jp · data/moves/names.asm · lines 153–153](https://github.com/Narishma-gb/pokegreen/blob/953f41b34108621b2bf13c3b1e53abfc9c3e5aec/data/moves/names.asm#L153)
- [pokegreen-jp · data/pokemon/dex_entries.asm · lines 888–894](https://github.com/Narishma-gb/pokegreen/blob/953f41b34108621b2bf13c3b1e53abfc9c3e5aec/data/pokemon/dex_entries.asm#L888-L894)
- [pokegreen-jp · data/moves/animations.asm · lines 1074–1076](https://github.com/Narishma-gb/pokegreen/blob/953f41b34108621b2bf13c3b1e53abfc9c3e5aec/data/moves/animations.asm#L1074-L1076)
- [pokegreen-jp · engine/battle/animations.asm · lines 1747–1772](https://github.com/Narishma-gb/pokegreen/blob/953f41b34108621b2bf13c3b1e53abfc9c3e5aec/engine/battle/animations.asm#L1747-L1772)
- [pokeblue-jp · data/moves/animations.asm · lines 1074–1076](https://github.com/Narishma-gb/pokeblue/blob/69cd1814203dd24533c46af383d7cff5591aea90/data/moves/animations.asm#L1074-L1076)
- [pokeblue-jp · engine/battle/animations.asm · lines 1345–1370](https://github.com/Narishma-gb/pokeblue/blob/69cd1814203dd24533c46af383d7cff5591aea90/engine/battle/animations.asm#L1345-L1370)
- [pokered · data/moves/animations.asm · lines 786–796](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/moves/animations.asm#L786-L796)
- [pokered · engine/battle/animations.asm · lines 1722–1744](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/animations.asm#L1722-L1744)
- [pokegold-reference · data/moves/animations.asm · lines 1995–2003](https://github.com/pret/pokegold/blob/ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8/data/moves/animations.asm#L1995-L2003)
- [pokegold-reference · data/moves/animations.asm · lines 4797–4803](https://github.com/pret/pokegold/blob/ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8/data/moves/animations.asm#L4797-L4803)
- [pokegold-reference · data/moves/moves.asm · lines 167–167](https://github.com/pret/pokegold/blob/ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8/data/moves/moves.asm#L167)
- [firered-reference · data/battle_anim_scripts.s · lines 3063–3072](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/battle_anim_scripts.s#L3063-L3072)
- [firered-reference · src/battle_anim_effects_3.c · lines 3367–3395](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/src/battle_anim_effects_3.c#L3367-L3395)
- [firered-reference · src/battle_anim.c · lines 754–783](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/src/battle_anim.c#L754-L783)
- [Nintendo Player’s Guide, Pokémon Red & Blue, page 106](https://www.docdroid.net/file/download/h250/nintendo-power-1998-pokemon-red-blue-pdf.pdf)

<a id="e118"></a>

## E118 — Gen I hacks make different Acid Armor presentation choices

Shin Pokémon Red Lite and Master keep the sinking frames, blink the picture, and show it again. PureRGB v2.7.8 pauses while hidden and restores the picture. Its Acid Armor also uses a separate Reflect and Light Screen effect. Solus 1.5 and its checked master branch, Solid Red, and Yellow Legacy 1.0.10 retain picture erasure. Pokémon Brown 6.0 and CreamElDudJafar’s Yellow Kaizo report changing the animation. Comet PR #55 proposes reusing the existing picture after a short pause. The PR was open when checked. These comparisons show different presentation choices.

Checked on 2026-11-22. See the [Acid Armor review](acid-armor.md).

- [shin-lite · engine/battle/animations.asm · lines 2019–2049](https://github.com/jojobear13/shinpokered/blob/b35c2a536a1605841c8fb662aad18b0dbfd2a900/engine/battle/animations.asm#L2019-L2049)
- [shin-master · engine/battle/animations.asm · lines 2019–2049](https://github.com/jojobear13/shinpokered/blob/a7a9b1361e55aaa5afed6b5d14b5e7bd44002179/engine/battle/animations.asm#L2019-L2049)
- [pure-v2.7.8 · engine/battle/animations.asm · lines 2267–2291](https://github.com/Vortyne/pureRGB/blob/c45336e2874d45e48d571ee92a5ce587cca05d65/engine/battle/animations.asm#L2267-L2291)
- [pure-v2.7.8 · data/moves/moves.asm · lines 166–166](https://github.com/Vortyne/pureRGB/blob/c45336e2874d45e48d571ee92a5ce587cca05d65/data/moves/moves.asm#L166)
- [pure · engine/battle/animations.asm · lines 2267–2291](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/engine/battle/animations.asm#L2267-L2291)
- [solus-1.5 · engine/battle/animations.asm · lines 1759–1784](https://github.com/Dechrissen/poke-solus-rgb/blob/a82621b152044134536811247a9a3a01b0231bcb/engine/battle/animations.asm#L1759-L1784)
- [solus · engine/battle/animations.asm · lines 1759–1784](https://github.com/Dechrissen/poke-solus-rgb/blob/95e157191e920162a24908cc95c358e73d294689/engine/battle/animations.asm#L1759-L1784)
- [solidred · engine/battle/animations.asm · lines 1870–1895](https://github.com/tustin2121/solidred/blob/18a901695e6d79aafca8e4b793ce70be1fa22853/engine/battle/animations.asm#L1870-L1895)
- [yellow-legacy-1.0.10 · engine/battle/animations.asm · lines 1862–1867](https://github.com/cRz-Shadows/Pokemon_Yellow_Legacy/blob/3a5358e8c9d3d0889f38cdb39a208120fea37a31/engine/battle/animations.asm#L1862-L1867)
- [yellow-kaizo-notes · README.md · lines 128–132](https://github.com/CreamElDudJafar/Yellow-Kaizo/blob/b4a84d770e0fecff8687f2a9c5cd4d0d273b3275/README.md#L128-L132)
- [RainbowDevs Pokémon Brown 6.0 changelog](https://rainbowdevs.com/2024/09/07/changelog-version-6-0/#visual-changes)
- [Star Beasts: Comet Version PR #55](https://github.com/StarBeasts/Star-Beasts-Comet/pull/55)

<a id="e119"></a>

## E119 — Acid Armor picture reload and redraw paths

SameBoy ran 76 more single-player cases in English Red, Blue, and Yellow. Viewing STATS from the party menu in battle reloads the enemy graphics while the same battler keeps its +2 Defense stage. It reappears on return if the battle screen already draws those tiles. Otherwise, the next draw of that picture shows it. The same menu leaves a hidden player picture blank. Canceling the party list or switching the player's Pokémon leaves the hidden enemy picture blank. Haze resets the Defense stage without restoring the picture. Substitute and Minimize can create new pictures. A successful attack by the hidden Substitute's user can redraw the doll. Sending the player's hidden Pokémon out again loads its normal picture.

Checked on 2026-11-22. See the [picture return paths](acid-armor.md#what-brings-the-picture-back) and the [stock-ROM records](acid-armor-baseline.json).

- [pokered · engine/battle/core.asm · lines 1723–1733](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L1723-L1733)
- [pokered · engine/battle/core.asm · lines 2313–2328](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L2313-L2328)
- [pokered · engine/battle/core.asm · lines 2365–2395](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L2365-L2395)
- [pokered · engine/battle/core.asm · lines 2419–2436](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L2419-L2436)
- [pokered · engine/battle/core.asm · lines 3165–3182](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L3165-L3182)
- [pokered · engine/battle/core.asm · lines 5565–5582](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L5565-L5582)
- [pokered · engine/battle/move_effects/haze.asm · lines 1–47](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/move_effects/haze.asm#L1-L47)
- [pokered · engine/battle/move_effects/substitute.asm · lines 41–58](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/move_effects/substitute.asm#L41-L58)
- [pokered · engine/battle/effects.asm · lines 471–495](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/effects.asm#L471-L495)
- [pokered · engine/battle/animations.asm · lines 1391–1402](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/animations.asm#L1391-L1402)
- [pokeyellow · engine/battle/core.asm · lines 2470–2501](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/engine/battle/core.asm#L2470-L2501)

<a id="e120"></a>

## E120 — Battle STATS can redraw the wrong side or reveal a ghost

The 28 stock-ROM cases confirm that Red/Blue can redraw the player side after canceling FIGHT with an enemy Substitute or Minimize active. Yellow corrects the side. Both Red/Blue and Yellow reload the hidden species picture when returning from STATS against an unidentified ghost. The ghost name stays the same.

Checked on 2026-11-22. [Donor survey](donor-bugfix-survey.md)

- [pokered · engine/battle/core.asm · lines 2365–2395](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L2365-L2395)
- [pokered · engine/battle/core.asm · lines 2848–2870](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L2848-L2870)
- [pokered · engine/battle/core.asm · lines 6695–6727](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L6695-L6727)
- [pokeyellow · engine/battle/core.asm · lines 2475–2501](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/engine/battle/core.asm#L2475-L2501)
- [shin-lite · engine/battle/core.asm · lines 2725–2755](https://github.com/jojobear13/shinpokered/blob/b35c2a536a1605841c8fb662aad18b0dbfd2a900/engine/battle/core.asm#L2725-L2755)
- [pure · engine/battle/moved_battle_code.asm · lines 13–38](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/engine/battle/moved_battle_code.asm#L13-L38)

<a id="e121"></a>

## E121 — Trainer items at full HP and the empty SHIFT prompt

Stock Red and Blue allow Blaine to use a Super Potion at full HP. Official Yellow, Shin Lite, PureRGB, and Yellow Legacy take different approaches to selecting the item. Red and Blue also offer a SHIFT switch when every reserve has fainted. The proposed fixes check full HP and reserve eligibility at these points.

Checked on 2026-11-22. [Donor survey](donor-bugfix-survey.md)

- [pokered · engine/battle/trainer_ai.asm · lines 382–398](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/trainer_ai.asm#L382-L398)
- [pokered · engine/battle/trainer_ai.asm · lines 493–552](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/trainer_ai.asm#L493-L552)
- [pokeyellow · engine/battle/trainer_ai.asm · lines 396–407](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/engine/battle/trainer_ai.asm#L396-L407)
- [yellow-legacy-1.0.10 · engine/battle/trainer_ai.asm · lines 800–808](https://github.com/cRz-Shadows/Pokemon_Yellow_Legacy/blob/3a5358e8c9d3d0889f38cdb39a208120fea37a31/engine/battle/trainer_ai.asm#L800-L808)
- [pokered · engine/battle/core.asm · lines 1364–1407](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L1364-L1407)
- [pure · engine/battle/core.asm · lines 1537–1565](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/engine/battle/core.asm#L1537-L1565)
- [pure · engine/battle/move_effects/teleport.asm · lines 98–125](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/engine/battle/move_effects/teleport.asm#L98-L125)

<a id="e122"></a>

## E122 — Replacing a move can use the wrong sound bank

Red/Blue use SFX_SWAP through the active audio bank during the move replacement dialogue. Yellow and Yellow Legacy temporarily select the bank containing the intended sound and restore the previous bank. PureRGB also routes the in-battle sound separately. A listening check remains part of patch validation.

Checked on 2026-11-22. [Donor survey](donor-bugfix-survey.md)

- [pokered · engine/pokemon/learn_move.asm · lines 208–220](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/pokemon/learn_move.asm#L208-L220)
- [pokered · home/audio.asm · lines 168–197](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/home/audio.asm#L168-L197)
- [pokered · constants/music_constants.asm · lines 155–157](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/constants/music_constants.asm#L155-L157)
- [pokeyellow · engine/pokemon/learn_move.asm · lines 207–239](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/engine/pokemon/learn_move.asm#L207-L239)
- [yellow-legacy-1.0.10 · engine/pokemon/learn_move.asm · lines 207–239](https://github.com/cRz-Shadows/Pokemon_Yellow_Legacy/blob/3a5358e8c9d3d0889f38cdb39a208120fea37a31/engine/pokemon/learn_move.asm#L207-L239)
- [pure · engine/pokemon/learn_move.asm · lines 296–318](https://github.com/Vortyne/pureRGB/blob/231abdfcf52e2d1c0ef44f96d497b9b1b1369049/engine/pokemon/learn_move.asm#L296-L318)

<a id="e123"></a>

## E123 — Transform tests the wrong battler for Fly and Dig

On both English cartridges and on both sides, Transform succeeded while its target had the invulnerable bit set by Fly or Dig. A grounded control also succeeded. The move contains its own failure branch for this exact flag. [Methods and scope](core-scope-review.md)

- [engine/battle/move_effects/transform.asm](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/move_effects/transform.asm#L1-L24)

<a id="e124"></a>

## E124 — Recover and Struggle boundary cases

Recover failed at 600 max HP with 255 or 511 HP missing, but succeeded at 511 max HP with 255 missing. With Disable active and all usable moves empty, PP Up bits in another slot sent the player into the move list instead of forcing Struggle. The ordinary Struggle check masks those bits. [Methods and scope](core-scope-review.md)

- [engine/battle/move_effects/heal.asm](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/move_effects/heal.asm#L1-L22)
- [engine/battle/core.asm](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L2716-L2756)

<a id="e125"></a>

## E125 — Vermilion second-switch adjacency

The gym clue promises an adjacent second lock. The selector treats a row length as a mask and can index 255 bytes past the first neighbor. At reachable first can 4, half the byte inputs select nonadjacent can 0 and half select can 7. The row lists four legal neighbors. [Methods and scope](core-scope-review.md)

- [text/VermilionGym_2.asm](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/text/VermilionGym_2.asm#L106-L114)
- [scripts/VermilionCity.asm](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/scripts/VermilionCity.asm#L16-L21)
- [engine/events/hidden_events/vermilion_gym_trash.asm](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/hidden_events/vermilion_gym_trash.asm#L38-L93)
- [engine/events/hidden_events/vermilion_gym_trash.asm](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/events/hidden_events/vermilion_gym_trash.asm#L107-L128)

<a id="e126"></a>

## E126 — Trainer AI neutral value and its caller

The AI routine initializes to 16 and its move-scoring caller compares against 16. Stock table entries return 0, 5, or 20. On this path an unmatched move already gets neutral treatment. Changing only the initializer to decimal 10 would send it down the resistance branch. [Methods and scope](core-scope-review.md)

- [engine/battle/core.asm](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L5192-L5226)
- [engine/battle/trainer_ai.asm](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/trainer_ai.asm#L193-L248)
- [data/types/type_matchups.asm](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/data/types/type_matchups.asm#L1-L80)

<a id="e127"></a>

## E127 — Unidentified ghosts mark the underlying Pokédex species seen

An unseen Gastly acquired its seen bit at battle entry even when its name displayed as GHOST. Ordinary and scoped controls also acquired the bit. This precedes any STATS-menu action. [Methods and scope](core-scope-review.md)

- [engine/battle/core.asm](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L6124-L6140)
- [engine/battle/core.asm](https://github.com/pret/pokered/blob/af519899719f0754965776faac0e836a3b906e6d/engine/battle/core.asm#L6695-L6727)

<a id="e128"></a>

## E128 — EXP. ALL reuses divided award data

Both healthy participants received 156 XP and 45 HP stat experience each in the EXP. ALL fixture. Independent half awards yield 210 and 60 each. Both games agreed with each other across all four input combinations. [Review and methods](foundation-audit.md)

- [engine/battle/core.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/core.asm#L819-L857)
- [engine/battle/experience.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/experience.asm#L294-L325)

<a id="e129"></a>

## E129 — Draining moves can bypass the Substitute guard

The intermediate helper overwrites the move effect before both failure branches. Mega Drain healed its user while the doll took damage in all four active-doll fixtures. The Japanese routine retains a move-effect read. [Review and methods](foundation-audit.md)

- [engine/battle/core.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/core.asm#L5228-L5263)
- [engine/battle/core.asm](https://github.com/Narishma-gb/pokegreen/blob/953f41b34108621b2bf13c3b1e53abfc9c3e5aec/engine/battle/core.asm#L5348-L5367)

<a id="e130"></a>

## E130 — Rest leaves the bad-poison marker

Both stock games set sleep and retained the previously set bad-poison bit for either actor. The ordinary residual damage path consults the independent bit. [Review and methods](foundation-audit.md)

- [engine/battle/move_effects/heal.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/move_effects/heal.asm#L23-L47)
- [engine/battle/core.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/core.asm#L530-L597)

<a id="e131"></a>

## E131 — Transformed move reordering writes to the permanent move set

After a genuine Transform, the stock move menu reordered both the copied moves and two different original moves and PP values in party data. Ordinary swaps reordered the expected records. [Review and methods](foundation-audit.md)

- [engine/battle/core.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/core.asm#L2762-L2819)

<a id="e132"></a>

## E132 — Trainer move comparison can count its own slot

The alternative search includes the current move. Against a Psychic target, the four-move Sabrina-class fixture left only Recover eligible. Replacing Psywave with a second Psybeam or changing the target to Normal changed the score pattern. [Review and methods](foundation-audit.md)

- [engine/battle/trainer_ai.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/trainer_ai.asm#L187-L252)

<a id="e133"></a>

## E133 — Damage scaling can wrap or produce a zero divisor

Both actor paths scale stats into single bytes. A low defense can become zero and a doubled defense above 1023 can wrap. Explosion already applies a minimum to its separate halving step. [Review and methods](foundation-audit.md)

- [engine/battle/core.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/core.asm#L4043-L4134)
- [engine/battle/core.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/core.asm#L4155-L4243)
- [engine/battle/core.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/core.asm#L4297-L4320)

<a id="e134"></a>

## E134 — One-time rewards and refusal paths

The Route 1 sample and Oak’s five balls mark receipt before attempting delivery. The parcel event advances after an unchecked delivery. The Warden preserves a separate debt to the player. [Review and methods](foundation-audit.md)

- [scripts/Route1.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/scripts/Route1.asm#L10-L27)
- [scripts/OaksLab.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/scripts/OaksLab.asm#L1019-L1031)
- [scripts/ViridianMart.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/scripts/ViridianMart.asm#L50-L62)
- [scripts/WardensHouse.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/scripts/WardensHouse.asm#L18-L60)

<a id="e135"></a>

## E135 — Tower data and lucky-machine boundary

Tower 2F scans 46 pairs. Two distinct extra in-bounds locations are impassable. A separate model shows one of 256 source bytes selects a lucky index of zero, which cannot match the one-based comparison. [Review and methods](foundation-audit.md)

- [scripts/PokemonTower2F.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/scripts/PokemonTower2F.asm#L23-L65)
- [home/map_objects.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/home/map_objects.asm#L107-L131)
- [data/tilesets/collision_tile_ids.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/data/tilesets/collision_tile_ids.asm#L43-L44)
- [scripts/GameCorner.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/scripts/GameCorner.asm#L9-L24)
- [engine/slots/game_corner_slots.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/slots/game_corner_slots.asm#L1-L24)

<a id="e136"></a>

## E136 — Boundary and safety claims in Red/Blue DX

The same developer list covers independently supported repairs and deliberate later-generation rules. Use individual stock evidence to classify each entry. [Review and methods](foundation-audit.md)

- [FEATURES.md](https://github.com/DunhamGitHub/pokereddx/blob/24d35ad318df6bc1573dd4fc8801ea9293d3099e/FEATURES.md#L5-L42)

<a id="e137"></a>

## E137 — Yellow changes machine permissions without changing move types

Yellow changes eight species’ machine permissions. Charizard gains Fly and Mewtwo loses Pay Day. All 165 move rows and 82 ordered chart rows match English Red and Blue. [Evidence and scope](yellow-rules-review.md)

- [data/pokemon/base_stats/charizard.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/data/pokemon/base_stats/charizard.asm#L13-L25)
- [data/pokemon/base_stats/charizard.asm](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/data/pokemon/base_stats/charizard.asm#L13-L25)
- [data/moves/moves.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/data/moves/moves.asm#L14-L41)

<a id="e138"></a>

## E138 — Ghost and Psychic across languages and releases

The two published charts are preserved as scan references. [Japanese illustrated guide, p. 106](https://archive.org/details/pokemon-illustrated-book-of-pocket-monsters-character-art-book-encyclopedia-poke/page/n107/mode/1up) · [US Red instruction booklet, p. 33](https://www.videogamemanual.com/gameboy/Pokemon%20-%20Red%20Version%20%28USA%29.pdf#page=35)

The Japanese illustrated guide explicitly marks Ghost attacks as very effective against Psychic. The US Red booklet puts the same matchup in its BAD category. English Yellow removes ghosts from the gym hint. Japanese Yellow retains the older hint and the immunity. The change to the type rule is documented in the Stadium 2 Academy text. [Evidence and scope](yellow-rules-review.md)

- [data/types/type_matchups.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/data/types/type_matchups.asm#L73-L84)
- [text/SaffronGym.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/text/SaffronGym.asm#L135-L140)
- [scripts/SaffronGym.asm](https://github.com/Narishma-gb/pokeyellow-jp/blob/f282e72ae26232790fdb780aa5a5db7ec8ebf572/scripts/SaffronGym.asm#L306-L310)
- [oldnotes/stadiumgs/text/academy/class.txt](https://github.com/pret/pokestadium/blob/6995f32445e344c03f9b0c774eabcd157559f867/oldnotes/stadiumgs/text/academy/class.txt#L329-L336)

<a id="e139"></a>

## E139 — A wandering NPC can return south in Yellow

After five northward steps the stock Red/Blue movement routine rejects a passable return to the south. Yellow accepts it. Four north steps and an impassable tile serve as controls. [Evidence and scope](yellow-rules-review.md)

- [engine/overworld/movement.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/overworld/movement.asm#L639-L669)
- [engine/overworld/movement.asm](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/engine/overworld/movement.asm#L630-L670)

<a id="e140"></a>

## E140 — Donor move types and Ghost matchup choices

The four sampled hack families use a Ghost weakness. Individual move retypings vary, including between Star Beasts’ changes and those in Solus or Shin. [Evidence and scope](developer-hack-comparison.md)

- [data/types/type_matchups.asm](https://github.com/StarBeasts/Star-Beasts-Comet/blob/7fa2f616979ab73525c9389e63215d67aa39758e/data/types/type_matchups.asm#L98-L104)
- [data/moves/moves.asm](https://github.com/StarBeasts/Star-Beasts-Comet/blob/7fa2f616979ab73525c9389e63215d67aa39758e/data/moves/moves.asm#L15-L41)
- [data/moves/moves.asm](https://github.com/Dechrissen/poke-solus-rgb/blob/a82621b152044134536811247a9a3a01b0231bcb/data/moves/moves.asm#L15-L41)
- [data/type_effects.asm](https://github.com/jojobear13/shinpokered/blob/b35c2a536a1605841c8fb662aad18b0dbfd2a900/data/type_effects.asm#L80-L85)

<a id="e141"></a>

## E141 — Guard Spec. and Safari East signs

Guard Spec. blocked Growl and retained the damage taken from Flamethrower and Water Gun in stock controls. The East Safari map is mislabeled Center. Both are presentation repairs. [Evidence and scope](developer-hack-comparison.md)

- [text/SafariZoneEast.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/text/SafariZoneEast.asm#L13-L16)
- [data/maps/objects/SafariZoneEast.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/data/maps/objects/SafariZoneEast.asm#L10-L20)
- [engine/battle/core.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/core.asm#L5265-L5307)

<a id="e142"></a>

## E142 — The AREA display counts duplicates before removing them

Pidgey uses 35 bytes including the terminator in a 30-byte work area. Its encounter slots represent 14 distinct maps. Gastly and Tentacool also exceed the declared size. [Evidence and scope](developer-hack-comparison.md)

- [engine/items/item_effects.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/items/item_effects.asm#L2910-L2955)
- [engine/items/town_map.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/items/town_map.asm#L373-L401)
- [ram/wram.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/ram/wram.asm#L936-L940)

<a id="e143"></a>

## E143 — Species widths affect stored and exchanged party records

The stock full party section is 404 bytes. The wide branch produces 417. The requested donor cable party length omits seven bytes under its widened layout. Successful exchange is a distinct test. [Evidence and scope](species-id-architecture.md)

- [macros/ram.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/macros/ram.asm#L7-L58)
- [macros/ram.asm](https://github.com/Rangi42/pokered/blob/b507db6f4fe6f98ff295d72a57f91fef6b87ac8f/macros/ram.asm#L7-L58)
- [engine/link/cable_club.asm](https://github.com/Rangi42/pokered/blob/b507db6f4fe6f98ff295d72a57f91fef6b87ac8f/engine/link/cable_club.asm#L125-L143)

<a id="e144"></a>

## E144 — Tutorial index distinguishes features from author requests

There are 108 linked subjects across the ten editing, feature and debug sections and nine to-do lines. They include both new engine capabilities and simple author-owned data edits. [Evidence and scope](tutorial-library.md)

- [Tutorials.md](https://github.com/pret/pokered/wiki/Tutorials/e11cd15f002f1387a52c086bd7c36038a5b0ca14)

<a id="e145"></a>

## E145 — Three narrow changes to Core’s game data

A three-byte gameplay edit changes the Ghost/Psychic matchup, Gust’s type and Charizard’s Fly permission. The paired comparison comprised 136 type-adjustment calls and 48 battle turns, equally divided between stock and experimental builds. [Methods and scope](core-rule-precedents.md)

- [data/types/type_matchups.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/data/types/type_matchups.asm#L73-L84)
- [data/moves/moves.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/data/moves/moves.asm#L14-L41)
- [data/pokemon/base_stats/charizard.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/data/pokemon/base_stats/charizard.asm#L13-L25)
- [data/pokemon/dex_entries.asm](https://github.com/Narishma-gb/pokegreen/blob/953f41b34108621b2bf13c3b1e53abfc9c3e5aec/data/pokemon/dex_entries.asm#L1352-L1358)

<a id="e146"></a>

## E146 — Ordinary Surf eligibility and a refused dismount

Eight Red/Blue field routes cover boarding, badge and terrain refusals, a fainted move holder and a rejected dismount. The latter keeps Surf active while dismissing the party menu. [Methods and scope](field-shortcut-contract.md)

- [engine/items/item_effects.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/items/item_effects.asm#L669-L746)
- [engine/menus/start_sub_menus.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/menus/start_sub_menus.asm#L160-L176)

<a id="e147"></a>

## E147 — Storage refusal and PC transfer behavior

The full selected box and full party prevent an ordinary throw before its catch rolls. Red/Blue battle-menu controls kept the Master Ball on refusal. Deposit and withdrawal preserved current HP, poison and depleted PP in all three tested English games. [Methods and scope](box-overflow-contract.md)

- [engine/items/item_effects.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/items/item_effects.asm#L106-L137)
- [engine/menus/save.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/menus/save.asm#L358-L402)
- [text/Route3.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/text/Route3.asm#L67-L78)

<a id="e148"></a>

## E148 — Cancelled first box change modifies a previous adventure

In a new unsaved game, first-use CHANGE BOX can initialize the previous save’s inactive boxes before a destination is selected. In both Red and Blue the prior save reloaded but its two occupied inactive boxes read empty after B. Deferring initialization until selection preserved the entire prior save. [Methods and scope](box-picker-safety.md)

- [engine/menus/save.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/menus/save.asm#L358-L402)
- [engine/menus/save.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/menus/save.asm#L529-L573)
- [data/text/text_3.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/data/text/text_3.asm#L22-L33)

<a id="e149"></a>

## E149 — Box choice already has numeric occupancy data

The twelve-box chooser reads all counts, substitutes the live active count and draws the same icon for every nonempty box. Showing the selected count needs no new persistent field. [Methods and scope](box-picker-safety.md)

- [engine/menus/save.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/menus/save.asm#L487-L506)
- [engine/menus/save.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/menus/save.asm#L575-L617)

<a id="e150"></a>

## E150 — Field controls and active-box preparation in the Red booklet

Printed page 28 teaches Cut and Surf as field actions. On the same page it directs a player with a full selected box back to a Pokémon Center. Route 3 repeats the box advice. The manual documents the requirement; it supplies no account of why the team first chose it. [Methods and scope](storage-policy-and-code.md)

- [text/Route3.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/text/Route3.asm#L73-L78)
- [text/CeruleanGym.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/text/CeruleanGym.asm#L33-L44)
- [US Red manual, p. 28](https://www.videogamemanual.com/gameboy/Pokemon%20-%20Red%20Version%20%28USA%29.pdf#page=30)

<a id="e151"></a>

## E151 — A marked move can change Counter after the player cancels

Marking Water Gun with SELECT can reset the cursor and substitute Tackle in the recorded move history. After cancellation and the same switch, Counter removed 38 HP in a Red fixture and 34 in Blue. Cancelling without marking gave zero damage to the entering Pokémon. [Methods and scope](minimal-action-review.md)

- [engine/battle/core.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/core.asm#L2858-L2886)
- [engine/battle/core.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/core.asm#L4546-L4595)

<a id="e152"></a>

## E152 — Full saves and completed trades write different data

A full save kept the new party, Pokédex, money and live box. The post-trade save kept the new party and Pokédex while restoring the earlier money and live box on reload. Neither routine alone updated the two numbered-box banks. [Methods and scope](storage-policy-and-code.md)

- [engine/menus/save.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/menus/save.asm#L266-L296)
- [engine/link/cable_club.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/link/cable_club.asm#L852-L869)
- [engine/menus/save.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/menus/save.asm#L377-L400)

<a id="e153"></a>

## E153 — Separating the selected box from its address calculation

Naming the common lookup step produced stock Red and Blue ROMs byte for byte. A separate 69-byte search passed 336 saved-count cases and 24 original address checks. The probe used no new saved fields and did not perform a capture or store an arrival. [Methods and scope](storage-policy-and-code.md)

- [engine/menus/save.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/menus/save.asm#L329-L356)
- [engine/menus/save.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/menus/save.asm#L575-L617)

<a id="e154"></a>

## E154 — Using a received field move differs from local HM teaching

In Red, Blue and Yellow an incoming Charizard record carrying Fly kept the move and offered it in the field menu. Only Yellow allowed HM02 to teach it locally. Removing Fly from the incoming moves removed the field command. [Methods and scope](minimal-action-review.md)

- [engine/link/cable_club.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/link/cable_club.asm#L805-L823)
- [engine/menus/text_box.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/menus/text_box.asm#L509-L545)
- [engine/items/item_effects.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/items/item_effects.asm#L2201-L2248)

<a id="e155"></a>

## E155 — Emerald Rogue publishes two editions of one adventure

The six GitHub release labels each have EX and Vanilla editions. The v2.1 tags share adventure code while selecting different rosters and battle data. The author also directs players to Hackdex. [Methods and scope](emerald-rogue-builds.md)

- [Makefile](https://github.com/Pokabbie/pokeemerald-rogue/blob/c33212ebcda821d78aa8d9b69a5e06c6995c212b/Makefile#L1-L6)
- [Makefile](https://github.com/Pokabbie/pokeemerald-rogue/blob/559792325f500d480b892799218ee015962f93a2/Makefile#L1-L6)
- [include/constants/rogue.h](https://github.com/Pokabbie/pokeemerald-rogue/blob/c33212ebcda821d78aa8d9b69a5e06c6995c212b/include/constants/rogue.h#L388-L413)
- [include/config/battle.h](https://github.com/Pokabbie/pokeemerald-rogue/blob/559792325f500d480b892799218ee015962f93a2/include/config/battle.h#L63-L70)

<a id="e156"></a>

## E156 — Global preset review of archived reports

A fourth approach to one route sign and the New Game forced-bicycle case qualify for both presets. The model and stock controls separate world-state changes from shared bounds repairs. [Methods and scope](catalog-decisions.md)

- [data/maps/objects/Route17.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/data/maps/objects/Route17.asm#L16-L26)
- [engine/movie/oak_speech/oak_speech.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/movie/oak_speech/oak_speech.asm#L5-L25)
- [home/overworld.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/home/overworld.asm#L1307-L1340)

<a id="e157"></a>

## E157 — SHIFT prompt with no usable reserve

Stock can offer a switch with no living reserve. The prototype removed the zero-HP prompt, kept the prompt at 1 HP, and matched the tested next-turn state. [Methods and scope](player-experience-sweep.md)

- [engine/battle/core.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/core.asm#L1364-L1443)

<a id="e158"></a>

## E158 — Sold and hidden coins at the cap

The clerk can charge for a partial lot while promising 50. An unrelated 10-coin hidden pickup at 9,989 credits all ten while taking the dropped-coins message branch. [Methods and scope](final-scope-audit.md)

- [scripts/GameCorner.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/scripts/GameCorner.asm#L140-L211)
- [text/GameCorner.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/text/GameCorner.asm#L10-L25)
- [engine/events/hidden_items.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/events/hidden_items.asm#L73-L119)

<a id="e159"></a>

## E159 — TM names at checkout versus teaching

All nine retail shop TMs and all three prize TMs produced only their machine numbers in the abortable purchase confirmations in each color. An owned machine reveals its move before teaching is confirmed. [Methods and scope](player-experience-sweep.md)

- [home/names.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/home/names.asm#L27-L97)
- [engine/events/pokemart.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/events/pokemart.asm#L159-L172)
- [engine/events/prize_menu.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/events/prize_menu.asm#L180-L204)

<a id="e160"></a>

## E160 — Battle flash and alarm behavior

Battle Scene off retains a hit response and encounter transition flashing. Low-HP status can also bypass unrelated sound waits. Two independently selectable presentation features must preserve those cues and timing. [Methods and scope](accessibility-scope.md)

- [engine/battle/battle_transitions.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/battle_transitions.asm#L49-L119)
- [engine/battle/animations.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/animations.asm#L403-L438)
- [home/delay.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/home/delay.asm#L15-L31)
- [engine/battle/core.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/core.asm#L1851-L1874)

<a id="e161"></a>

## E161 — Core Focus Energy threshold and cap order

All tested threshold and comparison inputs matched the selected arithmetic in experimental Red and Blue. The unpumped branch matched stock. The model and two separately exercised compiled sections define the release tests. [Methods and scope](critical-hit-analysis.md)

- [engine/battle/core.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/core.asm#L4477-L4543)

<a id="e162"></a>

## E162 — Day Care and deposits can silently affect move or party availability

In both stock games, a new Day Care move could remove Dig from slot one. The PC and Day Care also allowed a deposit that left only a fainted Pokémon in the party. [Methods and scope](final-scope-audit.md)

- [scripts/Daycare.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/scripts/Daycare.asm#L21-L56)
- [scripts/Daycare.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/scripts/Daycare.asm#L103-L183)
- [engine/pokemon/evos_moves.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/pokemon/evos_moves.asm#L416-L494)
- [engine/pokemon/bills_pc.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/pokemon/bills_pc.asm#L206-L236)

<a id="e163"></a>

## E163 — A fresh Pokédex visit resets the cursor

Exiting from the ninth list position restored the caller’s scroll offset. Reopening in the same play session returned to the first position in both versions. [Methods and scope](final-scope-audit.md)

- [engine/menus/pokedex.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/menus/pokedex.asm#L1-L45)

<a id="e164"></a>

## E164 — Red’s Porygon and the final coin purchase

Starting with no coins, 199 purchases of 50 reach 9,950. The stock clerk accepts another ¥1,000 and credits the remaining 49. Red’s prize counter can then exchange all 9,999 for Porygon. The full-lot-only prototype refuses the 200th purchase. It blocks this cash-only route from zero. Blue’s Porygon costs 6,500 coins. [Coin purchases and prize redemption](game-corner-redemption.md) · [Recorded cashier checks](scope-sweep-checks.json)

- [Clerk and payment](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/scripts/GameCorner.asm#L140-L192)
- [Sale threshold](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/scripts/GameCorner.asm#L532-L537)
- [Coin cap](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/math/bcd.asm#L169-L190)
- [Porygon prices by version](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/data/events/prizes.asm#L32-L55)
- [Prize delivery and payment](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/events/prize_menu.asm#L197-L244)

<a id="e165"></a>

## E165 — Day Care move order in Red/Blue and their remakes

Red/Blue and FireRed/LeafGreen fill an empty move slot first. When a new level-up move needs space, they drop the first move in the current order. The original Route 5 attendant and both remake attendants quote the price at pickup. Their deposit speeches do not teach the move rule or give the fee formula. Gold/Silver also shifts the first move out. [Day Care comparison, including Platinum and later games](day-care-history.md) · [Recorded Red and Blue checks](scope-sweep-checks.json)

- [Red/Blue attendant](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/text/Daycare.asm#L1-L46)
- [Red/Blue move order](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/pokemon/evos_moves.asm#L409-L494)
- [FireRed/LeafGreen Route 5 attendant](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/Route5_PokemonDayCare/text.inc#L1-L60)
- [Four Island attendant](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/text/day_care.inc#L50-L110)
- [Remake Day Care withdrawal](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/src/daycare.c#L478-L548)
- [Route 5 withdrawal](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/src/daycare.c#L1587-L1591)
- [Remake move order](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/src/pokemon.c#L2320-L2345)
- [Gold/Silver move order](https://github.com/pret/pokegold/blob/ef0201d8daf47e8b3ea1518eacf890f37d4cd5e8/engine/pokemon/evolve.asm#L520-L561)

<a id="e166"></a>

## E166 — Move learning before the choice to replace a move

At level 31, an Alakazam with four moves reaches the learn/replace question with all moves and PP intact. An empty slot receives Recover with 20 PP automatically. A duplicate move or a level with no new move gives no offer. The level-up and forget menus provide separate places to inspect the incoming and existing moves. [Fixture inputs and results](move-info-stock-checks.json) · [INFO design](../docs/15-battle-information.md)

- [engine/pokemon/evos_moves.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/pokemon/evos_moves.asm#L323-L375)
- [engine/pokemon/learn_move.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/pokemon/learn_move.asm#L11-L74)
- [engine/pokemon/learn_move.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/pokemon/learn_move.asm#L98-L184)
- [engine/battle/core.asm](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/battle/core.asm#L2554-L2639)
