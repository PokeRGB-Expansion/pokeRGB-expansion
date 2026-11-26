; The party, box and Move Deleter use the same list and detail card.
InspectStatsMove:
	ld a, INFO_BROWSE_STATS
	ld [wMoveInfoBrowse], a
	xor a
	ld [wMoveInfoSlot], a
	call WaitForInfoKeysReleased
	ldh a, [hAutoBGTransferEnabled]
	push af
	xor a
	ldh [hAutoBGTransferEnabled], a
	call SaveMoveInfoScreen
	ld hl, wPartyMonNicks
	ld a, [wMonDataLocation]
	cp BOX_DATA
	jr nz, .nickname
	ld hl, wBoxMonNicks
.nickname
	call DrawKnownMoveList
	call ShowKnownSlotInfo
	call RestoreMoveInfoScreen
	ld a, 1
	ldh [hAutoBGTransferEnabled], a
	call Delay3
	call WaitForInfoKeysReleased
	pop af
	ldh [hAutoBGTransferEnabled], a
	ret

; HL = nickname list. STATS and the Deleter both prepare wMovesString.
DrawKnownMoveList:
	ld a, [wWhichPokemon]
	call SkipFixedLengthTextEntries
	push hl
	hlcoord 0, 0
	lb bc, 8, SCREEN_WIDTH - 2
	call TextBoxBorder
	pop de
	hlcoord 2, 0
	call PlaceString
	hlcoord 1, 1
	ld de, .heading
	call PlaceString
	hlcoord 3, 2
	ld de, wMovesString
	jp PlaceString
.heading db "KNOWN MOVES@"

DrawKnownMoveCursor:
	hlcoord 1, 2
	ld de, 2 * SCREEN_WIDTH
	ld b, NUM_MOVES
.clear
	ld [hl], ' '
	add hl, de
	dec b
	jr nz, .clear
	hlcoord 1, 2
	ld bc, 2 * SCREEN_WIDTH
	ld a, [wMoveInfoSlot]
	call AddNTimes
	ld [hl], '▶'
	ret

ShowKnownSlotInfo:
	call SelectInfoMoveSlot
	jp ShowMoveInfo

IF DEF(_MOVE_DELETER)
; Return carry on cancel, or the zero-based selected slot in wMoveInfoSlot.
ChooseMoveToDelete:
	ld a, INFO_BROWSE_DELETER
	ld [wMoveInfoBrowse], a
	call WaitForInfoKeysReleased
	ld a, [wLetterPrintingDelayFlags]
	push af
	res BIT_TEXT_DELAY, a
	ld [wLetterPrintingDelayFlags], a
	ldh a, [rLCDC]
	push af
	res B_LCDC_OBJS, a
	ldh [rLCDC], a
	xor a
	ldh [hAutoBGTransferEnabled], a
	ld [wMoveInfoSlot], a
	ld hl, wPartyMon1Moves
	ld bc, PARTYMON_STRUCT_LENGTH
	ld a, [wWhichPokemon]
	call AddNTimes
	ld de, wMoves
	ld bc, NUM_MOVES
	call CopyData
	farcall FormatMovesString
	ld hl, wPartyMonNicks
	call DrawKnownMoveList
.draw
	call .render
.wait
	call DelayFrame
	call ReadInfoButtons
	ldh a, [hJoyPressed]
	bit B_PAD_B, a
	jr nz, .leave
	bit B_PAD_START, a
	jr z, .checkA
	call ShowKnownSlotInfo
	call .render
	call WaitForInfoKeysReleased
	jr .wait
.checkA
	bit B_PAD_A, a
	jr nz, .leave
	ldh a, [hJoyFiltered]
	and PAD_UP | PAD_DOWN
	ld hl, wMoveInfoSlot
	cp PAD_UP
	jr z, .up
	cp PAD_DOWN
	jr nz, .wait
	ld a, [wNumMovesMinusOne]
	cp [hl]
	jr z, .wrapTop
	inc [hl]
	jr .draw
.wrapTop
	ld [hl], 0
	jr .draw
.up
	ld a, [hl]
	and a
	jr nz, .previous
	ld a, [wNumMovesMinusOne]
	ld [hl], a
	jr .draw
.previous
	dec [hl]
	jr .draw
.leave
	push af
	ld a, SFX_PRESS_AB
	call PlaySound
	call WaitForInfoKeysReleased
	call LoadScreenTilesFromBuffer2
	call Delay3
	pop bc
	pop af
	ldh [rLCDC], a
	pop af
	ld [wLetterPrintingDelayFlags], a
	and a
	bit B_PAD_B, b
	ret z
	scf
	ret

.render
	xor a
	ldh [hAutoBGTransferEnabled], a
	call DrawKnownMoveCursor
	hlcoord 0, 10
	lb bc, 6, SCREEN_WIDTH - 2
	call TextBoxBorder
	hlcoord 1, 11
	ld de, .question
	call PlaceString
	call SelectReplacementInfoMove
	ld a, b
	ld [wMoveInfoMove], a
	ld a, c
	ld [wMoveInfoPP], a
	call ReadMoveInfoData
	hlcoord 1, 13
	call DrawMoveInfoPPAt
	hlcoord 1, 15
	ld de, MoveInfoStartText
	call PlaceString
	hlcoord 1, 16
	ld de, .buttons
	call PlaceString
	ld a, 1
	ldh [hAutoBGTransferEnabled], a
	jp Delay3

.question db "Forget which move?@"
.buttons db "A:CHOOSE    B:BACK@"
ENDC
