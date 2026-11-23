HiddenItemNear:
	ld hl, HiddenItemCoords
	ld b, 0
.loop
	ld de, 3
	ld a, [wCurMap]
	call IsInRestOfArray
	ret nc ; return if current map has no hidden items
	push bc
	push hl
	ld hl, wObtainedHiddenItemsFlags
	ld c, b
	ld b, FLAG_TEST
	predef FlagActionPredef
	ld a, c
	pop hl
	pop bc
	inc b
	and a
	inc hl
	ld d, [hl]
	inc hl
	ld e, [hl]
	inc hl
	jr nz, .loop ; if the item has already been obtained
; Measure distance before comparing so coordinate endpoints stay valid.
	ld a, [wYCoord]
	sub d
	jr nc, .compareVertical
	cpl
	inc a
.compareVertical
	cp 5
	jr nc, .loop
	ld a, [wXCoord]
	sub e
	jr nc, .west
	cpl
	inc a
	cp 6 ; east has a five-tile range
	jr .compareHorizontal
.west
	cp 5
.compareHorizontal
	jr nc, .loop
	scf
	ret
