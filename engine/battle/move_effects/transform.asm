TransformEffect_:
IF DEF(_POKERGB_CORE)
	ld hl, wEnemyMonSpecies
	ld de, wBattleMonSpecies
	ldh a, [hWhoseTurn]
	and a
	jr nz, .enemyTurn
	ld [wPlayerMoveListIndex], a
	ld a, [wEnemyBattleStatus1]
	jr .hitTest
.enemyTurn
ENDC
	ld hl, wBattleMonSpecies
	ld de, wEnemyMonSpecies
IF !DEF(_POKERGB_CORE)
	ld bc, wEnemyBattleStatus3
	; bug: on enemy's turn, a is overloaded with hWhoseTurn,
	; before the check for INVULNERABLE
	ld a, [wEnemyBattleStatus1]
	ldh a, [hWhoseTurn]
	and a
	jr nz, .hitTest
; player's turn
	ld hl, wEnemyMonSpecies
	ld de, wBattleMonSpecies
	ld bc, wPlayerBattleStatus3
	ld [wPlayerMoveListIndex], a
	; bug: this should be target's BattleStatus1 (i.e. wEnemyBattleStatus1)
ENDC
	ld a, [wPlayerBattleStatus1]
.hitTest
IF DEF(_POKERGB_CORE)
	bit INVULNERABLE, a
ELSE
	bit INVULNERABLE, a ; is mon invulnerable to typical attacks? (fly/dig)
	                    ; this check doesn't work due to above bugs
ENDC
	jp nz, .failed
	push hl
	push de
IF !DEF(_POKERGB_CORE)
	push bc
ENDC
	ld hl, wPlayerBattleStatus2
	ldh a, [hWhoseTurn]
	and a
	jr z, .transformEffect
	ld hl, wEnemyBattleStatus2
.transformEffect
; animation(s) played are different if target has Substitute up
	bit HAS_SUBSTITUTE_UP, [hl]
	push af
	ld hl, HideSubstituteShowMonAnim
	ld b, BANK(HideSubstituteShowMonAnim)
	call nz, Bankswitch
	ld a, [wOptions]
	add a
	ld hl, PlayCurrentMoveAnimation
	ld b, BANK(PlayCurrentMoveAnimation)
	jr nc, .gotAnimToPlay
	ld hl, AnimationTransformMon
	ld b, BANK(AnimationTransformMon)
.gotAnimToPlay
	call Bankswitch
	ld hl, ReshowSubstituteAnim
	ld b, BANK(ReshowSubstituteAnim)
	pop af
	call nz, Bankswitch
IF !DEF(_POKERGB_CORE)
	pop bc
	ld a, [bc]
	set TRANSFORMED, a ; mon is now transformed
	ld [bc], a
ENDC
	pop de
	pop hl
	push hl
; transform user into opposing Pokemon
; species
	ld a, [hl]
	ld [de], a
; type 1, type 2, catch rate, and moves
	ld bc, $5
	add hl, bc
	inc de
	inc de
	inc de
	inc de
	inc de
	inc bc
	inc bc
	call CopyData
	ldh a, [hWhoseTurn]
	and a
IF DEF(_POKERGB_CORE)
	ld bc, wPlayerBattleStatus3
	jr z, .markTransformed
	ld bc, wEnemyBattleStatus3
	ld a, [bc]
	bit TRANSFORMED, a
	jr nz, .next
; Save the enemy's original DVs on its first successful Transform.
ELSE
	jr z, .next
; save enemy mon DVs at wTransformedEnemyMonOriginalDVs
ENDC
	ld a, [de]
	ld [wTransformedEnemyMonOriginalDVs], a
	inc de
	ld a, [de]
	ld [wTransformedEnemyMonOriginalDVs + 1], a
	dec de
IF DEF(_POKERGB_CORE)
.markTransformed
	ld a, [bc]
	set TRANSFORMED, a
	ld [bc], a
ENDC
.next
; DVs
	ld a, [hli]
	ld [de], a
	inc de
	ld a, [hli]
	ld [de], a
	inc de
; Skip level and max HP
	inc hl
	inc hl
	inc hl
	inc de
	inc de
	inc de
; Attack, Defense, Speed, and Special stats
	ld bc, (NUM_STATS - 1) * 2
	call CopyData
	ld bc, wBattleMonMoves - wBattleMonPP
	add hl, bc ; ld hl, wBattleMonMoves
	ld b, NUM_MOVES
.copyPPLoop
; 5 PP for all moves
	ld a, [hli]
	and a
	jr z, .lessThanFourMoves
	ld a, 5
	ld [de], a
	inc de
	dec b
	jr nz, .copyPPLoop
	jr .copyStats
.lessThanFourMoves
; 0 PP for blank moves
	xor a
	ld [de], a
	inc de
	dec b
	jr nz, .lessThanFourMoves
.copyStats
; original (unmodified) stats and stat mods
	pop hl
	ld a, [hl]
	ld [wNamedObjectIndex], a
	call GetMonName
	ld hl, wEnemyMonUnmodifiedAttack
	ld de, wPlayerMonUnmodifiedAttack
	call .copyBasedOnTurn ; original (unmodified) stats
	ld hl, wEnemyMonStatMods
	ld de, wPlayerMonStatMods
	call .copyBasedOnTurn ; stat mods
IF DEF(_POKERGB_CORE)
	ldh a, [hWhoseTurn]
	and a
	jr nz, .printTransformed
	callfar RecordStatsBeforeStatusPenalties
.printTransformed
ENDC
	ld hl, TransformedText
	jp PrintText

.copyBasedOnTurn
	ldh a, [hWhoseTurn]
	and a
	jr z, .gotStatsOrModsToCopy
	push hl
	ld h, d
	ld l, e
	pop de
.gotStatsOrModsToCopy
	ld bc, (NUM_STATS - 1) * 2
	jp CopyData

.failed
	ld hl, PrintButItFailedText_
	jp EffectCallBattleCore

TransformedText:
	text_far _TransformedText
	text_end
