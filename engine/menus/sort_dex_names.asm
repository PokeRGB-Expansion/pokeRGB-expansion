; Shell sort the seen Pokédex numbers by their names. Compare the numerical
; IDs as a tie-breaker so equal or case-equivalent names have a stable order.
SortSeenDexNumbers::
	ld a, 40
	call .pass
	ld a, 13
	call .pass
	ld a, 4
	call .pass
	ld a, 1
.pass
	ld [wDexSortGap], a
	ld c, a
	ld a, [wDexAlphaCount]
	cp c
	ret c
	ret z
.outer
	ld hl, wDexAlphaOrder
	ld b, 0
	add hl, bc
	push bc ; outer index
	ld a, [hl]
	ld [wDexSortKey], a
	push hl
	call .namePointer
	ld d, h
	ld e, l
	pop hl
	ld b, c ; index of the current insertion point
	ld a, [wDexSortGap]
	ld c, a
.insertLoop
	ld a, b
	sub c
	jr c, .insert
	ld b, a
	ld a, l
	sub c
	ld l, a
	jr nc, .comparePrevious
	dec h
.comparePrevious
	push hl
	push de
	push bc
	ld a, [hl]
	call .namePointer
	ld b, NAME_LENGTH - 1
.compare
	ld a, [de]
	inc de
	call .foldCase
	ld c, a
	ld a, [hli]
	call .foldCase
	cp c
	jr nz, .compared
	dec b
	jr nz, .compare
.compared
	pop bc
	pop de
	pop hl
	jr c, .afterPrevious
	jr nz, .shiftPrevious
	ld a, [wDexSortKey]
	cp [hl]
	jr nc, .afterPrevious
.shiftPrevious
	ld a, [hl]
	push bc
	push hl
	ld b, 0
	add hl, bc
	ld [hl], a
	pop hl
	pop bc
	jr .insertLoop
.afterPrevious
	ld b, 0
	add hl, bc
.insert
	ld a, [wDexSortKey]
	ld [hl], a
	pop bc
	inc c
	ld a, [wDexAlphaCount]
	cp c
	jr nz, .outer
	ret

.namePointer
	push bc
	dec a
	ld c, a
	ld b, 0
	ld hl, wDexNamePointers
	add hl, bc
	add hl, bc
	ld a, [hli]
	ld h, [hl]
	ld l, a
	pop bc
	ret

.foldCase
	cp 'a'
	ret c
	cp 'z' + 1
	ret nc
	sub 'a' - 'A'
	ret

	ASSERT BANK(SortSeenDexNumbers) == BANK(MonsterNames)
