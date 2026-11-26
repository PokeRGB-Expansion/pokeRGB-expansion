; GetMonHeader loads a shared species record. Inspect every member before
; opening the panel and restore the caller's record, including in a battle Bag.
CacheMachinePartyEligibility:
	xor a
	ld [wMachineInfoAble], a
	ld a, [wPartyCount]
	and a
	ret z
	ld a, [wCurPartySpecies]
	push af
	ld a, [wCurSpecies]
	push af
	ld a, [wBuffer] ; GetMonHeader reads Mew's data from another bank
	push af
	add sp, -BASE_DATA_SIZE
	ld hl, sp + 0
	ld d, h
	ld e, l
	ld hl, wMonHeader
	ld bc, BASE_DATA_SIZE
	call CopyData
	ld a, [wPartyCount]
	ld c, a
	ld b, 0
	ld hl, wPartySpecies - 1
	add hl, bc
	ld b, c
.loop
	ld a, [hld]
	ld [wCurPartySpecies], a
	push hl
	push bc
	farcall CanLearnSelectedMachine
	ld a, e
	and a
	jr z, .store
	scf
.store
	ld hl, wMachineInfoAble
	rl [hl]
	pop bc
	pop hl
	dec b
	jr nz, .loop
	ld hl, sp + 0
	ld de, wMonHeader
	ld bc, BASE_DATA_SIZE
	call CopyData
	add sp, BASE_DATA_SIZE
	pop af
	ld [wBuffer], a
	pop af
	ld [wCurSpecies], a
	pop af
	ld [wCurPartySpecies], a
	ret

; Draw up to three full nicknames per page. Return the next-page hint in DE.
DrawMachineInfoParty:
	ld c, 0
	ld a, [wMoveInfoPage]
	cp 3
	jr nz, .firstRow
	ld c, 3
.firstRow
	hlcoord 1, 13
	ld a, [wPartyCount]
	and a
	jr nz, .rowCount
	ld de, .emptyText
	call PlaceString
	jr .lastPage
.rowCount
	sub c
	cp 4
	jr c, .draw
	ld a, 3
.draw
	ld b, a ; B = remaining rows, C = party slot
.row
	push bc
	push hl
	ld hl, wPartyMonNicks
	ld a, c
	call SkipFixedLengthTextEntries
	ld d, h
	ld e, l
	pop hl
	push hl
	call PlaceString
	pop hl
	pop bc
	push bc
	push hl
	call .status
	pop hl
	push hl
	ld bc, 11
	add hl, bc
	call PlaceString
	pop hl
	ld bc, SCREEN_WIDTH
	add hl, bc
	pop bc
	inc c
	dec b
	jr nz, .row
	ld a, [wPartyCount]
	cp c
	ld de, .moreText
	ret nz
.lastPage
	ld de, MoveInfoStatsText
	ret

.status
	push bc
	ld e, c
	ld a, [wMoveInfoMove]
	ld d, a
	farcall PartySlotKnowsMove
	pop bc
	ld de, .knowsText
	ret c
	ld hl, wMachineInfoAble
	ld b, FLAG_TEST
	predef FlagActionPredef
	ld a, c
	and a
	ld de, .unableText
	ret z
	ld de, .ableText
	ret

.emptyText db "No party #MON.@"
.ableText  db "ABLE@"
.unableText db "UNABLE@"
.knowsText db "KNOWS@"
.moreText  db "SELECT MORE    B@"
