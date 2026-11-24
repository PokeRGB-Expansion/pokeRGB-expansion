; The caller has loaded the real party member's header, including its growth
; rate. D is the level the party record has reached. No save data is needed.
CacheBattleExpPixels:
	ld a, [wLinkState]
	cp LINK_STATE_BATTLING
	ret z
	ld a, [wBattleType]
	and a
	ret nz ; no player-owned active battler in Safari or the Old Man demonstration

	xor a
	ld [wBattleExpPixels], a
	ld a, d
	and a
	ret z
	cp MAX_LEVEL
	ret nc ; empty track at the level cap

	; The growth and multiplication routines share scratch with battle code.
	ld hl, hDividend
	ld e, 5
.saveMath
	ld a, [hli]
	ld b, a
	ld c, [hl]
	inc hl
	push bc
	dec e
	jr nz, .saveMath
	call .calculate
	ld a, e
	ld [wBattleExpPixels], a
	ld hl, hDivideBuffer + 4
	ld e, 5
.restoreMath
	pop bc
	ld a, c
	ld [hld], a
	ld a, b
	ld [hld], a
	dec e
	jr nz, .restoreMath
	ret

.calculate
	ld a, [wPlayerMonNumber]
	ld hl, wPartyMon1Exp + 2
	ld bc, PARTYMON_STRUCT_LENGTH
	call AddNTimes
	push hl
	call CalcExperience
	ldh a, [hExperience]
	ld b, a
	ldh a, [hExperience + 1]
	ld c, a
	; Some Gen 1 curves produce a negative threshold at level one. At higher
	; levels, the same high bit can represent valid unsigned EXP in a hack.
	ld a, d
	cp 1
	jr nz, .unsignedLowerBound
	bit 7, b
	jr z, .unsignedLowerBound
	ld bc, 0
	xor a
	jr .haveLowerBound
.unsignedLowerBound
	ldh a, [hExperience + 2]
.haveLowerBound
	push bc
	push af
	inc d
	call CalcExperience
	pop af
	ld d, a
	pop bc

	; The next threshold minus the current one is the level's width.
	ldh a, [hExperience + 2]
	sub d
	ld e, a
	ldh a, [hExperience + 1]
	sbc c
	ld l, a
	ldh a, [hExperience]
	sbc b
	ld h, a
	push hl
	push de
	ld hl, sp + 4 ; original party EXP pointer below the saved width
	ld a, [hli]
	ld h, [hl]
	ld l, a
	; Subtract the same lower bound from the party member's total EXP.
	ld a, [hld]
	sub d
	ldh [hMultiplicand + 2], a
	ld a, [hld]
	sbc c
	ldh [hMultiplicand + 1], a
	ld a, [hl]
	sbc b
	ldh [hMultiplicand], a
	pop de
	pop bc
	pop hl
	ld d, e ; B:C:D = width, in big-endian order
	ld e, 0
	ret c ; below the current level's threshold
	ld a, b
	or c
	or d
	ret z ; an empty interval has no progress
	ld a, EXP_TRACK_WIDTH
	ldh [hMultiplier], a
	call Multiply

	; Divide a four-byte numerator by a three-byte width. At most 48
	; subtractions are needed, even for a party record beyond the next level.
.countPixels
	ld hl, hProduct + 3
	ld a, [hl]
	sub d
	ld [hld], a
	ld a, [hl]
	sbc c
	ld [hld], a
	ld a, [hl]
	sbc b
	ld [hld], a
	ld a, [hl]
	sbc 0
	ret c
	ld [hl], a
	inc e
	ld a, e
	cp EXP_TRACK_WIDTH
	jr nz, .countPixels
	ret

; The active party member has received its EXP. Keep the battle menu
; backup consistent so restoring it after a party member's level-up retains
; the new fill. A fainted battler may already have lost its entire HUD.
RefreshAwardedBattleExp:
	call CacheBattleExpPixels
	hlcoord 10, 11
	ld a, [hl]
	cp EXP_LABEL_TILE
	ret nz
	call DrawBattleExpMeter
	hlcoord 10, 11, wTileMapBackup
	ld a, [hl]
	cp EXP_LABEL_TILE
	ret nz
	decoord 10, 11, wTileMapBackup
	hlcoord 10, 11
	ld bc, 8
	jp CopyData

DrawBattleExpMeter:
	ld a, [wLinkState]
	cp LINK_STATE_BATTLING
	ret z
	ld a, [wBattleType]
	and a
	ret nz
	hlcoord 10, 11
	ld a, EXP_LABEL_TILE
	ld [hli], a
	inc a
	ld [hli], a
	ld a, [wBattleExpPixels]
	ld b, EXP_TRACK_WIDTH / TILE_WIDTH
.tile
	sub TILE_WIDTH
	jr nc, .full
	add TILE_WIDTH
	add EXP_TRACK_TILE
	ld [hli], a
	xor a
	jr .next
.full
	ld c, a
	ld a, EXP_TRACK_TILE + TILE_WIDTH
	ld [hli], a
	ld a, c
.next
	dec b
	jr nz, .tile
	ret
