# Acid Armor and battle sprite visibility

Review date **2026-11-22**. See [E116–E119](evidence.md#e116) for source revisions and file fingerprints.

D41 accepts the Core display repair. Keep the original melt and restore the same sprite at animation end. The return-path tests point to a missing redraw in the original animation. [PN-025](../docs/13-playthrough-intake.md#pn-025)

## What the original game does

Acid Armor raises its user's Defense by two stages up to the stage limit. A successful use plays a move-specific animation. It draws fewer rows of the user, clears its display area, and copies blank tiles over the picture in video memory. A later draw can put those blank tiles back in the usual position. A routine that reloads or replaces the picture can make it visible again. The cleared picture is local display state. Fly and Dig use a separate battle flag that affects whether attacks can hit. [E116](evidence.md#e116)

With battle animations off, the game skips the sinking animation and still applies the Defense increase. With animations on, the user's picture can stay absent between turns. Ordinary attacks could damage the invisible battler. An invisible Substitute could still absorb damage, and an invisible user could keep its Minimize state.

## What brings the picture back

The game needs fresh picture tiles and a draw that puts them on screen. The tests read both the stored graphics and the rendered picture. Replacing the picture and drawing the existing tiles are separate operations. [E119](evidence.md#e119)

| Action after Acid Armor | Result in the stock games |
|---|---|
| View one of your Pokémon's STATS from the battle party menu and leave the menu | Reloads the enemy picture. It can appear on return if the screen already refers to those tiles. If the screen still has an empty spot, the next animation that draws the enemy reveals it. In the tests, the same opponent kept its +2 Defense stage. The player picture stayed blank when the player was the Acid Armor user. |
| Open and cancel the party list without viewing STATS, or switch your Pokémon while the enemy is hidden | The enemy picture stayed blank. |
| Use Transform, put up a new Substitute, or use Minimize with the hidden battler | The move replaces the affected battler's picture. |
| The hidden Substitute breaks, or its user performs an attack that shows the doll again afterward | The break redraws the battler. The attack can redraw the doll while it is still active. |
| Switch the hidden player Pokémon out and send it back later | The returning Pokémon loads its normal picture and starts at the neutral Defense stage. |
| Take an ordinary hit or use Haze | An ordinary hit can leave the picture absent. Haze can reset the Defense stage to neutral while the picture stays absent. |

## Evidence for original intent

| Evidence | What it establishes |
|---|---|
| Japanese Red and Green, Japanese Blue, English Red and Blue, and English Yellow | They use the same sink and erase sequence. The erase explains why later draws can stay blank. These versions share the relevant routine. [E116](evidence.md#e116), [E117](evidence.md#e117) |
| Japanese move name and Vaporeon entry | The name means *Melt* or *Dissolve*. The original Japanese Pokédex describes Vaporeon vanishing when it dissolves in water. That supports the visual idea. The entry covers one species and says nothing about battle duration. [E117](evidence.md#e117) |
| Battle redraws and stat changes | Minimize tracks its small picture for later redraws. Acid Armor leaves blank picture tiles without an equivalent visibility flag. STATS can bring the picture back with the boost intact. Haze can clear the boost while leaving the picture blank. [E117](evidence.md#e117), [E119](evidence.md#e119) |
| Nintendo's 1998 Red & Blue Player's Guide, printed page 106 | It describes the Defense increase and leaves the animation duration unspecified. [Guide scan](https://www.docdroid.net/file/download/h250/nintendo-power-1998-pokemon-red-blue-pdf.pdf) |
| Gold and Silver, then FireRed and LeafGreen | Gold and Silver show the battler again at the end of the effect. FireRed and LeafGreen keep a brief disappearance and fade the picture back in. [E117](evidence.md#e117) |

The graphics reload tests favor a missing restoration at the end of the animation. The later official animations support a brief disappearance as the design. The exact timing Game Freak wanted in Gen I remains unknown.

## What other hacks do

| Hack | Checked behavior |
|---|---|
| Shin Pokémon Red Lite and Master | Both keep the sinking frames, blink the picture, and show it again. [Lite source](https://github.com/jojobear13/shinpokered/blob/b35c2a536a1605841c8fb662aad18b0dbfd2a900/engine/battle/animations.asm#L2019-L2049), [Master source](https://github.com/jojobear13/shinpokered/blob/a7a9b1361e55aaa5afed6b5d14b5e7bd44002179/engine/battle/animations.asm#L2019-L2049) |
| PureRGB 2.7.8 | Keeps the sink, briefly hides the picture, and shows it again. PureRGB gives Acid Armor both Reflect and Light Screen effects. Its move rules are a separate design. [Animation](https://github.com/Vortyne/pureRGB/blob/c45336e2874d45e48d571ee92a5ce587cca05d65/engine/battle/animations.asm#L2267-L2291), [move data](https://github.com/Vortyne/pureRGB/blob/c45336e2874d45e48d571ee92a5ce587cca05d65/data/moves/moves.asm#L166) |
| Pokémon Solus 1.5 | Retains picture erasure. The checked master branch does too. [Release source](https://github.com/Dechrissen/poke-solus-rgb/blob/a82621b152044134536811247a9a3a01b0231bcb/engine/battle/animations.asm#L1759-L1784) |
| Solid Red and Pokémon Yellow Legacy 1.0.10 | Retain picture erasure. [Solid Red source](https://github.com/tustin2121/solidred/blob/18a901695e6d79aafca8e4b793ce70be1fa22853/engine/battle/animations.asm#L1870-L1895), [Yellow Legacy source](https://github.com/cRz-Shadows/Pokemon_Yellow_Legacy/blob/3a5358e8c9d3d0889f38cdb39a208120fea37a31/engine/battle/animations.asm#L1862-L1867) |
| Pokémon Brown 6.0 and CreamElDudJafar's Yellow Kaizo | The authors report changing the visuals so the battler no longer seems to disappear. [Brown changelog](https://rainbowdevs.com/2024/09/07/changelog-version-6-0/#visual-changes), [Yellow Kaizo notes](https://github.com/CreamElDudJafar/Yellow-Kaizo/blob/b4a84d770e0fecff8687f2a9c5cd4d0d273b3275/README.md#L128-L132) |
| Star Beasts: Comet Version | PR #55 keeps the sink, preserves the current picture tiles, and shows them again after a short pause. The pull request reports SameBoy checks for both sides, Minimize, and Substitute. It was open when checked. [Comet patch](https://github.com/StarBeasts/Star-Beasts-Comet/pull/55) |

## Stock ROM checks

SameBoy 1.0.5 ran 48 cases using unmodified English cartridge ROMs. Red and Blue ran in Game Boy mode. Yellow also ran in Game Boy Color mode. Each version and model covered both sides of a controlled wild battle. The harness seeded a disposable party after a fresh boot and used the normal Fight menu. It checked the Defense stage, flags, picture bytes, and screen output.

| Scenario | Result |
|---|---|
| Normal successful use, animations on | The current picture sank and stayed absent at the next command. The user gained two Defense stages. |
| Normal successful use, animations off | The picture stayed visible. The user gained two Defense stages. |
| Additional use at +6 Defense | The sinking routine did not run again. The stage and current picture state stayed as they were. |
| Use while minimized or behind Substitute | The small picture or doll disappeared. Its battle state survived. A later hit could damage the invisible battler or be absorbed by its Substitute. |

In 18 additional cases across all three English versions and both battle sides, the picture stayed absent after three ordinary turns with an attack landing. Separate cases brought the picture back with Transform or by breaking the hidden Substitute. The [recorded results](acid-armor-baseline.json) include cartridge fingerprints and case outcomes. The measured results cover single-player emulation.

The 76 return-path cases exercised STATS, party cancellation, switching, Haze, and moves that replace or redraw the picture. Each case ran with the same stock ROM setup. The tests recorded whether the picture's tiles held graphics, whether the battle screen drew those tiles, and whether the Defense stage changed. [E119](evidence.md#e119)

## Core correction

Keep the original sinking frames and sound. Hide the picture briefly, then use the existing draw path to show it before the animation returns. Preserve the current picture tiles so Acid Armor shows the correct Pokémon, transformed form, Minimize picture, or active Substitute. A fresh species picture would lose those distinctions.

Test both battle sides, successful and capped use, animations off, repeated use, Minimize, Substitute and its break, Transform, party redraws, switching, and fainting. Preserve the two-stage Defense effect, PP, RNG calls, damage rules, and link protocol. Check Fly and Dig as controls. The implementation and its regression results are pending. [Test plan](../docs/07-testing-ci.md#acid-armor-picture-checks)
