GetMonName::
	push hl
	ldh a, [hLoadedROMBank]
	push af
	ld a, BANK(MonsterNames)
	ldh [hLoadedROMBank], a
	ld [rROMB], a
	ld a, [wNamedObjectIndex]
	dec a
	ld hl, MonsterNames
	ld c, NAME_LENGTH - 1
	ld b, 0
	call AddNTimes
	ld de, wNameBuffer
	push de
	ld bc, NAME_LENGTH - 1
	call CopyData
	ld hl, wNameBuffer + NAME_LENGTH - 1
	ld [hl], '@'
	pop de
	pop af
	ldh [hLoadedROMBank], a
	ld [rROMB], a
	pop hl
	ret

GetItemName::
; given an item ID at [wNamedObjectIndex], store the name of the item in wNameBuffer
	push hl
	push bc
	ld a, [wNamedObjectIndex]
	cp HM01 ; is this a TM/HM?
	jr nc, .Machine

	ld [wNameListIndex], a
	ld a, ITEM_NAME
	ld [wNameListType], a
	ld a, BANK(ItemNames)
	ld [wPredefBank], a
	call GetName
	jr .Finish

.Machine
	call GetMachineName
.Finish
	ld de, wNameBuffer
	pop bc
	pop hl
	ret

GetMachineName::
; copies the name of the TM/HM in [wNamedObjectIndex] to wNameBuffer
	push hl
	push de
	push bc
	ld a, [wNamedObjectIndex]
	push af
	ld de, wNameBuffer
	call WriteMachineName
	pop af
	pop bc
	pop de
	pop hl
	ret

; Write TMnn or HMnn and a terminator at DE for the item ID in A.
; Leave DE on the terminator so a caller can append the move name.
WriteMachineName::
	ld hl, TechnicalPrefix
	cp TM01
	jr nc, .prefix
	add NUM_HMS
	ld hl, HiddenPrefix
.prefix
	sub TM01 - 1
	push af
	ld bc, 2
	call CopyData
	pop af
	ld b, '0'
.tens
	sub 10
	jr c, .ones
	inc b
	jr .tens
.ones
	add 10
	add '0'
	ld c, a
	ld a, b
	ld [de], a
	inc de
	ld a, c
	ld [de], a
	inc de
	ld a, '@'
	ld [de], a
	ret

TechnicalPrefix::
	db "TM"
HiddenPrefix::
	db "HM"

; sets carry if item is HM, clears carry if item is not HM
; Input: a = item ID
IsItemHM::
	cp HM01
	jr c, .notHM
	cp TM01
	ret
.notHM
	and a
	ret

; sets carry if move is an HM, clears carry if move is not an HM
; Input: a = move ID
IsMoveHM::
	ld hl, HMMoves
	ld de, 1
	jp IsInArray

HMMoves::
INCLUDE "data/moves/hm_moves.asm"

GetMoveName::
	push hl
	ld a, MOVE_NAME
	ld [wNameListType], a
	ld a, [wNamedObjectIndex]
	ld [wNameListIndex], a
	ld a, BANK(MoveNames)
	ld [wPredefBank], a
	call GetName
	ld de, wNameBuffer
	pop hl
	ret
