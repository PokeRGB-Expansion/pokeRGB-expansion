FuchsiaMoveDeletersHouse_Script:
	jp EnableAutoTextBoxDrawing

FuchsiaMoveDeletersHouse_TextPointers:
	def_text_pointers
	dw_const FuchsiaMoveDeleterText, TEXT_FUCHSIAMOVEDELETERSHOUSE_DELETER

FuchsiaMoveDeleterText:
	text_asm
	call SaveScreenTilesToBuffer2
	ld hl, .offerText
	call PrintText
	call YesNoChoice
	ld a, [wCurrentMenuItem]
	and a
	jp nz, .cancel
.chooseMon
	ld a, [wPartyCount]
	and a
	jp z, .cancel
	ld hl, .whichMonText
	call PrintText
	xor a
	ld [wUpdateSpritesEnabled], a
	ld [wPartyMenuTypeOrMessageID], a
	ld [wMenuItemToSwap], a
	call DisplayPartyMenu
	push af
	call GBPalWhiteOutWithDelay3
	call RestoreScreenTilesAndReloadTilePatterns
	call LoadGBPal
	pop af
	jr c, .cancel
	call GetPartyMonName2
	call CopyToStringBuffer
	call .partyMoves
	inc hl
	ld a, [hl]
	and a
	ld hl, .onlyMoveText
	jr z, .done
	ld hl, .whichMoveText
	call PrintText
	ld a, 2 ; party member's move list with PP and B to cancel
	ld [wMoveMenuType], a
	xor a
	ld [wPlayerMoveListIndex], a
	callfar MoveSelectionMenu
	push af
	call LoadScreenTilesFromBuffer2
	pop af
	jr nz, .chooseMon
	ld a, [wPlayerMoveListIndex]
	push af
	xor a
	ld [wPlayerMoveListIndex], a
	call GetPartyMonName2
	call CopyToStringBuffer
	call .partyMoves
	pop af
	ld c, a
	ld b, 0
	add hl, bc
	ld a, [hl]
	ld [wNamedObjectIndex], a
	push hl
	push bc
	call GetMoveName
	ld hl, .confirmText
	call PrintText
	call SaveScreenTilesToBuffer1
	call InitYesNoTextBoxParameters
	ld a, 1 << BIT_SECOND_MENU_OPTION_DEFAULT
	ld [wTwoOptionMenuID], a
	call DisplayYesNoChoice
	pop bc
	pop hl
	ld a, [wCurrentMenuItem]
	and a
	jr nz, .cancel
	ld a, NUM_MOVES - 1
	sub c
	ld c, a
	push hl
	call .removeSlot
	pop hl
	ld de, MON_PP - MON_MOVES
	add hl, de
	call .removeSlot
	ld hl, .successText
	jr .done
.cancel
	ld hl, .comeAgainText
.done
	call PrintText
	jp TextScriptEnd

.partyMoves
	ld a, [wWhichPokemon]
	ld hl, wPartyMon1Moves
	ld bc, PARTYMON_STRUCT_LENGTH
	jp AddNTimes

; Shift C later move IDs or complete PP bytes left, then clear the last slot.
.removeSlot
	ld b, c
.shift
	ld a, b
	and a
	jr z, .clear
	inc hl
	ld a, [hld]
	ld [hli], a
	dec b
	jr .shift
.clear
	ld [hl], 0
	ret

.offerText
	text "Uh… Oh, yes! I'm"
	line "the MOVE DELETER."
	para "Shall I help your"
	line "#MON forget"
	cont "a move?"
	done
.whichMonText
	text "Which #MON"
	line "should forget"
	cont "a move?"
	prompt
.whichMoveText
	text "Which move should"
	line "be forgotten?"
	prompt
.onlyMoveText
	text_ram wStringBuffer
	text_start
	line "only knows one"
	cont "move!"
	done
.confirmText
	text_ram wStringBuffer
	text ", forget"
	line "@"
	text_ram wNameBuffer
	text "?"
	done
.successText
	text "It worked!"
	para "@"
	text_ram wStringBuffer
	text " forgot"
	line "@"
	text_ram wNameBuffer
	text "!"
	done
.comeAgainText
	text "Come again if you"
	line "want a move"
	cont "forgotten."
	done
