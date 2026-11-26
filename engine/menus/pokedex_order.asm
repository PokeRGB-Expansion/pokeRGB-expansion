; Convert a zero-based row in the current list to its actual Pokédex number.
; List drawing needs BC, DE and HL unchanged.
GetDexNumberAtRank:
	push hl
	push bc
	ld c, a
	ld a, [wDexAlphaMode]
	and a
	ld a, c
	jr nz, .alphabetical
	inc a
	jr .done
.alphabetical
	ld b, 0
	ld hl, wDexAlphaOrder
	add hl, bc
	ld a, [hl]
.done
	pop bc
	pop hl
	ret

ToggleDexOrder:
	ld a, [wDexAlphaMode]
	and a
	jr nz, ReturnToNumericDex
	ld a, [wCurrentMenuItem]
	ld [wDexNumericRow], a
	ld b, a
	ld a, [wListScrollOffset]
	ld [wDexNumericOffset], a
	add b
	inc a
	push af ; current numeric entry
	ld a, [wDexMaxSeenMon]
	ld [wDexNumericMax], a
	ld a, [wDexAlphaCount]
	cp $ff
	call z, BuildSeenDexList
	ld a, 1
	ld [wDexAlphaMode], a
	ld a, [wDexAlphaCount]
	ld [wDexMaxSeenMon], a
	ld b, a
	ld hl, wDexAlphaOrder
	ld c, 0
	pop de ; D = old dex number
.find
	ld a, b
	and a
	jr z, .unseen
	ld a, [hli]
	cp d
	jr z, .seen
	inc c
	dec b
	jr .find
.unseen
	ld a, 1
	ld [wDexReturnToUnseen], a
	xor a
	jr SetDexCursorRank
.seen
	xor a
	ld [wDexReturnToUnseen], a
	ld a, c
	jr SetDexCursorRank

ReturnToNumericDex:
	xor a
	ld [wDexAlphaMode], a
	ld a, [wDexNumericMax]
	ld [wDexMaxSeenMon], a
	ld a, [wDexReturnToUnseen]
	and a
	jr z, .useSelectedSpecies
	ld a, [wDexNumericOffset]
	ld [wListScrollOffset], a
	ld a, [wDexNumericRow]
	jr SetDexCursorRank.storeRow
.useSelectedSpecies
	ld a, [wCurrentMenuItem]
	ld c, a
	ld a, [wListScrollOffset]
	add c
	ld c, a
	ld b, 0
	ld hl, wDexAlphaOrder
	add hl, bc
	ld a, [hl]
	dec a
; A = zero-based index; place this entry at the top, or as high as it will fit.
SetDexCursorRank:
	ld b, a
	ld a, [wDexMaxSeenMon]
	sub 7
	jr nc, .haveMax
	xor a
.haveMax
	cp b
	jr c, .storeOffset
	ld a, b
.storeOffset
	ld [wListScrollOffset], a
	ld c, a
	ld a, b
	sub c
.storeRow
	ld [wCurrentMenuItem], a
	ld [wLastMenuItem], a
	ret

BuildSeenDexList:
	; Map each Pokédex number to its fixed-width name in the names bank.
	ld hl, PokedexOrder
	ld de, MonsterNames
	ld b, NUM_POKEMON_INDEXES
.nameLoop
	ld a, [hli]
	and a
	jr z, .next
	push hl
	push bc
	dec a
	ld c, a
	ld b, 0
	ld hl, wDexNamePointers
	add hl, bc
	add hl, bc
	ld [hl], e
	inc hl
	ld [hl], d
	pop bc
	pop hl
.next
	push hl
	ld hl, NAME_LENGTH - 1
	add hl, de
	ld d, h
	ld e, l
	pop hl
	dec b
	jr nz, .nameLoop

	ld de, wDexAlphaOrder
	ld a, 1
.seenLoop
	ld [wPokedexNum], a
	push de
	ld hl, wPokedexSeen
	call IsPokemonBitSet
	pop de
	ld a, [wPokedexNum]
	jr z, .skip
	ld [de], a
	inc de
.skip
	inc a
	cp NUM_POKEMON + 1
	jr c, .seenLoop
	ld a, e
	sub LOW(wDexAlphaOrder)
	ld [wDexAlphaCount], a
	cp 2
	ret c
	farjp SortSeenDexNumbers
