DEF BOX_PREVIEW_ROWS EQU 4

PreviewBox:
	ld a, [wBoxPreviewNumber]
	dec a
	ld c, a
	ld b, 0
	ld hl, wBoxMonCounts
	add hl, bc
	ld a, [hl]
	cp MONS_PER_BOX
	jr c, .countReady
	ld a, MONS_PER_BOX
.countReady
	ld [wBoxPreviewCount], a
	xor a
	ld [wBoxPreviewFirstSlot], a
.draw
	call DrawBoxPreview
.input
	call DelayFrame
	call JoypadLowSensitivity
	ldh a, [hJoyFiltered]
	bit B_PAD_B, a
	ret nz
	ld b, a
	and PAD_UP | PAD_LEFT
	jr z, .next
	ld a, [wBoxPreviewFirstSlot]
	sub BOX_PREVIEW_ROWS
	jr c, .input
	jr .setPage
.next
	ld a, b
	and PAD_DOWN | PAD_RIGHT
	jr z, .input
	ld a, [wBoxPreviewFirstSlot]
	add BOX_PREVIEW_ROWS
	ld b, a
	ld a, [wBoxPreviewCount]
	cp b
	jr z, .input
	jr c, .input
	ld a, b
.setPage
	ld [wBoxPreviewFirstSlot], a
	jr .draw

DrawBoxPreview:
	xor a
	ldh [hAutoBGTransferEnabled], a
	hlcoord 0, 0
	lb bc, SCREEN_HEIGHT - 2, SCREEN_WIDTH - 2
	call TextBoxBorder
	hlcoord 1, 1
	ld de, .box
	call PlaceString
	hlcoord 5, 1
	ld de, wBoxPreviewNumber
	lb bc, 1 | LEFT_ALIGN, 2
	call PrintNumber
	hlcoord 13, 16
	ld de, .back
	call PlaceString
	ld a, [wBoxPreviewCount]
	and a
	jr nz, .hasMons
; An unopened box in a new adventure is empty even if an older save used it.
	hlcoord 2, 7
	ld de, .empty
	call PlaceString
	jr .show
.hasMons
	cp BOX_PREVIEW_ROWS + 1
	jr c, .drawNames
	hlcoord 11, 1
	ld de, .page
	call PlaceString
	ld a, [wBoxPreviewFirstSlot]
	call .pageDigit
	ldcoord_a 16, 1
	ld a, [wBoxPreviewCount]
	dec a
	call .pageDigit
	ldcoord_a 18, 1
	hlcoord 1, 16
	ld de, .directions
	call PlaceString
.drawNames
	ld a, [wCurrentBoxNum]
	and BOX_NUM_MASK
	inc a
	ld b, a
	ld a, [wBoxPreviewNumber]
	cp b
	ld hl, wBoxDataStart
	jr z, .sourceReady
; Read only the saved box. The active copy always comes from working memory.
	dec a
	call GetBoxSRAMLocationByIndex
	ld a, RAMG_SRAM_ENABLE
	ld [rRAMG], a
	ld a, BMODE_ADVANCED
	ld [rBMODE], a
	ld a, b
	ld [rRAMB], a
.sourceReady
	ld d, h
	ld e, l
	hlcoord 1, 3
	ld a, [wBoxPreviewFirstSlot]
	ld c, a
	ld b, BOX_PREVIEW_ROWS
.loop
	push bc
	push de
	push hl
	ld a, c
	call DrawBoxPreviewMon
	pop hl
	ld de, SCREEN_WIDTH * 3
	add hl, de
	pop de
	pop bc
	inc c
	ld a, [wBoxPreviewCount]
	cp c
	jr z, .done
	dec b
	jr nz, .loop
.done
	xor a
	ld [rBMODE], a
	ld [rRAMG], a
.show
	ld a, 1
	ldh [hAutoBGTransferEnabled], a
	ret

.pageDigit
	ASSERT BOX_PREVIEW_ROWS == 4 && MONS_PER_BOX <= BOX_PREVIEW_ROWS * 9
	srl a
	srl a
	add '1'
	ret

.box        db "BOX @"
.back       db "B:BACK@"
.empty      db "This BOX is empty.@"
.page       db "PAGE  /@"
.directions db "D-PAD:PAGE@"

; A = slot, DE = box base, HL = tile for the nickname.
DrawBoxPreviewMon:
	push hl
	push af
	ld h, d
	ld l, e
	inc hl ; species list follows the count
	ld c, a
	ld b, 0
	add hl, bc
	ld a, [hl]
	ld [wNamedObjectIndex], a
	ld hl, wBoxMonNicks - wBoxDataStart
	add hl, de
	pop af
	ld bc, NAME_LENGTH
	call AddNTimes
	ld d, h
	ld e, l
	pop hl
	push hl
	ld b, NAME_LENGTH - 1
.copyNick
	ld a, [de]
	cp '@'
	jr z, .species
	ld [hli], a
	inc de
	dec b
	jr nz, .copyNick
.species
	pop hl
	ld de, SCREEN_WIDTH + 2
	add hl, de
	ld [hl], '('
	inc hl
	call GetMonName
	call PlaceString
	ld a, ')'
	ld [bc], a
	ret
