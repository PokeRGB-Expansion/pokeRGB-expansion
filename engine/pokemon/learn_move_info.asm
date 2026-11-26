; The normal learning question or forget list owns the regular screen backups.
; Keep its exact tilemap in the sprite workspace while browsing. No pictures
; are decompressed here. The original sprite tiles and shadow OAM stay intact.
ShowLearningMoveInfo:
	ld [wMoveInfoIncoming], a
	ld a, INFO_BROWSE_LEARN
	ld [wMoveInfoBrowse], a
	xor a
	ld [wMoveInfoPage], a
	call WaitForInfoKeysReleased
	ldh a, [hAutoBGTransferEnabled]
	push af
	xor a
	ldh [hAutoBGTransferEnabled], a
	ldh a, [rLCDC]
	push af
	res B_LCDC_OBJS, a
	ldh [rLCDC], a
	call SaveMoveInfoScreen
	call DrawLearningMoveList
.showMove
	ld a, [wMoveInfoIncoming]
	and a
	jr z, .known
	ld a, [wMoveNum]
	ld b, a
	ld c, INFO_UNKNOWN_PP
	jr .load
.known
	call SelectReplacementInfoMove
.load
	ld a, b
	ld [wMoveInfoMove], a
	ld a, c
	ld [wMoveInfoPP], a
.draw
	xor a
	ldh [hAutoBGTransferEnabled], a
	call DrawLearningMoveCursors
	call DrawMoveInfo
.wait
	call DelayFrame
	call ReadInfoButtons
	ldh a, [hJoyPressed]
	bit B_PAD_B, a
	jr nz, .close
	bit B_PAD_SELECT, a
	jr z, .checkSide
	ld hl, wMoveInfoPage
	ld a, [hl]
	xor 1
	ld [hl], a
	jr .draw
.checkSide
	and PAD_LEFT | PAD_RIGHT
	cp PAD_LEFT
	jr z, .changeSide
	cp PAD_RIGHT
	jr nz, .checkSlot
.changeSide
	ld hl, wMoveInfoIncoming
	ld a, [hl]
	xor 1
	ld [hl], a
	jr .showMove
.checkSlot
	ldh a, [hJoyFiltered]
	and PAD_UP | PAD_DOWN
	cp PAD_UP
	jr z, .up
	cp PAD_DOWN
	jr nz, .wait
	ld b, 1
	jr .step
.up
	ld b, -1
.step
	ld a, [wMoveInfoIncoming]
	and a
	jr z, .nextSlot
; From NEW, either direction first reveals the candidate shown by the outline.
	xor a
	ld [wMoveInfoIncoming], a
	jr .showMove
.nextSlot
	ld a, [wMoveInfoSlot]
	add b
	cp NUM_MOVES
	jr nc, .wait
	ld [wMoveInfoSlot], a
	jr .showMove
.close
	xor a
	ldh [hAutoBGTransferEnabled], a
	call RestoreMoveInfoScreen
	ld a, [wMoveInfoQuestion]
	and a
	jr nz, .restore ; preserve YES/NO, including NO if it was highlighted
	ld a, [wMoveInfoSlot]
	ld [wCurrentMenuItem], a
	call PlaceMenuCursor
.restore
	ld a, 1
	ldh [hAutoBGTransferEnabled], a
	call Delay3
	pop af
	ldh [rLCDC], a
	call WaitForInfoKeysReleased
	pop af
	ldh [hAutoBGTransferEnabled], a
	ret

SaveMoveInfoScreen:
	hlcoord 0, 0
	ld de, sMoveInfoScreen
	jr CopyMoveInfoScreen

RestoreMoveInfoScreen:
	ld hl, sMoveInfoScreen
	decoord 0, 0
CopyMoveInfoScreen:
	ld a, RAMG_SRAM_ENABLE
	ld [rRAMG], a
	ld a, BANK(sMoveInfoScreen)
	ld [rRAMB], a
	ld bc, SCREEN_AREA
	call CopyData
	xor a
	ld [rRAMG], a
	ret

DrawLearningMoveList:
	hlcoord 0, 0
	lb bc, 8, SCREEN_WIDTH - 2
	call TextBoxBorder
	hlcoord 2, 0
	ld de, wLearnMoveMonName
	call PlaceString
	hlcoord 1, 1
	ld de, .knownMoves
	call PlaceString
	ld hl, wPartyMon1Moves
	ld bc, PARTYMON_STRUCT_LENGTH
	ld a, [wWhichPokemon]
	call AddNTimes
	decoord 3, 2
	ld b, NUM_MOVES
.list
	ld a, [hli]
	push hl
	push bc
	push de
	ld [wMoveInfoMove], a
	farcall ReadMoveInfoName
	pop hl
	push hl
	ld de, wMoveInfoName
	call PlaceString
	pop hl
	ld de, SCREEN_WIDTH
	add hl, de
	ld d, h
	ld e, l
	pop bc
	pop hl
	dec b
	jr nz, .list
	hlcoord 1, 7
	ld de, .newMove
	call PlaceString
	ld a, [wMoveNum]
	ld [wMoveInfoMove], a
	farcall ReadMoveInfoName
	hlcoord 3, 8
	ld de, wMoveInfoName
	jp PlaceString
.knownMoves db "KNOWN MOVES@"
.newMove db "NEW MOVE@"

DrawLearningMoveCursors:
	hlcoord 1, 2
	ld de, SCREEN_WIDTH
	ld b, NUM_MOVES
.clear
	ld [hl], ' '
	add hl, de
	dec b
	jr nz, .clear
	hlcoord 1, 2
	ld bc, SCREEN_WIDTH
	ld a, [wMoveInfoSlot]
	call AddNTimes
	lb de, '▶', '▷' ; D = known marker, E = incoming marker
	ld a, [wMoveInfoIncoming]
	and a
	jr z, .markers
	lb de, '▷', '▶'
.markers
	ld [hl], d
	ld a, e
	ldcoord_a 1, 8
	ret
