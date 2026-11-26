; A read-only panel. Its data lives outside the active menu and battle state.
DEF INFO_BROWSE_STATS EQU 1
DEF INFO_BROWSE_LEARN EQU 2
DEF INFO_BROWSE_SUPPLY EQU 3
DEF INFO_UNKNOWN_PP EQU $ff
DEF INFO_PANEL_FIRST_ROW EQU 11
DEF INFO_PANEL_ROWS EQU SCREEN_HEIGHT - INFO_PANEL_FIRST_ROW

InspectFightMove:
	ld a, [wCurrentMenuItem]
	dec a
	cp NUM_MOVES
	ret nc
	ld e, a
	ld d, 0
	ld hl, wBattleMonPP
	add hl, de
	ld c, [hl]
	ld hl, wBattleMonMoves
	add hl, de
	ld b, [hl]
	xor a
	ld [wMoveInfoBrowse], a
	jp ShowMoveInfo

InspectStatsMove:
	xor a
	ld [wMoveInfoSlot], a
	ld a, INFO_BROWSE_STATS
	ld [wMoveInfoBrowse], a
	call SelectStatsInfoMove
	jp ShowMoveInfo

WaitForStatsMoveInfo:
	ld a, [wLinkState]
	and a
	jp nz, WaitForTextScrollButtonPress
	ld a, [wMonDataLocation]
	and a
	jr z, .allow
	cp BOX_DATA
	jp nz, WaitForTextScrollButtonPress
.allow
	ld a, [wLoadedMonMoves]
	and a
	jp z, WaitForTextScrollButtonPress
	hlcoord 1, 7
	ld de, MoveInfoStartText
	call PlaceString
.wait
	call DelayFrame
	call JoypadLowSensitivity
	ldh a, [hJoyFiltered]
	bit B_PAD_START, a
	jr nz, .view
	and PAD_A | PAD_B
	jr z, .wait
	ret
.view
	call InspectStatsMove
	jr .wait

SelectStatsInfoMove:
	ld a, [wMoveInfoSlot]
	ld e, a
	ld d, 0
	ld hl, wLoadedMonPP
	add hl, de
	ld c, [hl]
	ld hl, wLoadedMonMoves
	add hl, de
	ld b, [hl]
	ret

InspectIncomingMove:
	xor a
	ld [wMoveInfoBrowse], a
	ld a, [wMoveNum]
	ld b, a
	ld c, INFO_UNKNOWN_PP
	jp ShowMoveInfo

InspectReplacementMove:
	ld a, [wCurrentMenuItem]
	cp NUM_MOVES
	ret nc
	push af
	ld a, INFO_BROWSE_LEARN
	ld [wMoveInfoBrowse], a
	pop af
	ld [wMoveInfoSlot], a
	call SelectReplacementInfoMove
	jp ShowMoveInfo

SelectReplacementInfoMove:
	ld hl, wPartyMon1Moves
	ld bc, PARTYMON_STRUCT_LENGTH
	ld a, [wWhichPokemon]
	call AddNTimes
	ld a, [wMoveInfoSlot]
	ld e, a
	ld d, 0
	add hl, de
	ld a, [hl]
	ld bc, MON_PP - MON_MOVES
	add hl, bc
	ld c, [hl]
	ld b, a
	ret


HandleItemMoveInfoInput::
	ld a, 1
	jr HandleMoveInfoInput
HandlePrizeMoveInfoInput:
	ld a, 2
	jr HandleMoveInfoInput
HandleLearnerMoveInfoInput:
	ld a, 3
HandleMoveInfoInput:
	ld [wMoveInfoHint], a
	add sp, -2 * SCREEN_WIDTH
	ld hl, sp + 0
	ld a, l
	ld [wMoveInfoData], a
	ld e, l
	ld a, h
	ld [wMoveInfoData + 1], a
	ld d, h
	hlcoord 0, 14
	ld bc, 2 * SCREEN_WIDTH
	call CopyData
	call HandleMenuInput
	ld [wMoveInfoNumber], a
	call RestoreMoveInfoHintRows
	add sp, 2 * SCREEN_WIDTH
	xor a
	ld [wMoveInfoHint], a
	ret

RestoreMoveInfoHintRows:
	ld a, [wMoveInfoData]
	ld l, a
	ld a, [wMoveInfoData + 1]
	ld h, a
	decoord 0, 14
	ld bc, 2 * SCREEN_WIDTH
	jp CopyData

DrawMoveInfoCursorHint::
	call RestoreMoveInfoHintRows
	ld a, [wMoveInfoHint]
	cp 1
	jp z, DrawMachineListHint
	cp 2
	jr z, ReadPrizeInfoName
	hlcoord 1, 15
	ld de, MoveInfoStartText
	jp PlaceString

ReadPrizeInfoName:
	ld a, [wWhichPrizeWindow]
	cp 2
	ret nz
	ld a, [wCurrentMenuItem]
	cp 3
	ret nc
	ld e, a
	ld d, 0
	ld hl, wPrize1
	add hl, de
	ld a, [hl]
	ld [wMoveInfoMove], a
	farcall ReadMoveInfoMachine
	ld a, [wMoveInfoMove]
	and a
	ret z
	cp NUM_ATTACKS + 1
	ret nc
	farcall ReadMoveInfoName
	hlcoord 1, 14
	ld de, wMoveInfoName
	call PlaceString
	hlcoord 1, 15
	ld de, MoveInfoStartText
	jp PlaceString

InspectPrizeMove:
	ld a, [wWhichPrizeWindow]
	cp 2
	ret nz
	ld a, [wCurrentMenuItem]
	cp 3
	ret nc
	ld e, a
	ld d, 0
	ld hl, wPrize1
	add hl, de
	ld a, [hl]
	jr InspectMachineMove

InspectListedMove::
	call FindListedInfoItem
	ret nc
	cp HM01
	jr nc, InspectMachineMove
	ld [wMoveInfoMove], a
	ld a, INFO_BROWSE_SUPPLY
	ld [wMoveInfoBrowse], a
	jp OpenInfoPanel
InspectMachineMove:
	ld [wMoveInfoMove], a
	farcall ReadMoveInfoMachine
	ld a, [wMoveInfoMove]
	ld b, a
	ld c, INFO_UNKNOWN_PP
	xor a
	ld [wMoveInfoBrowse], a
	jp ShowMoveInfo

DrawMachineListHint:
	call FindListedInfoItem
	ret nc
	cp HM01
	jr c, .hint
	ld [wMoveInfoMove], a
	farcall ReadMoveInfoMachine
	ld a, [wMoveInfoMove]
	and a
	ret z
	cp NUM_ATTACKS + 1
	ret nc
	farcall ReadMoveInfoName
	hlcoord 1, 14
	ld de, wMoveInfoName
	call PlaceString
.hint
	hlcoord 1, 15
	ld de, MoveInfoStartText
	jp PlaceString

FindListedInfoItem:
	ld a, [wListMenuID]
	cp ITEMLISTMENU
	jr z, .itemList
	cp PRICEDITEMLISTMENU
	jr nz, .absent
.itemList
	ld a, [wListPointer]
	ld l, a
	ld a, [wListPointer + 1]
	ld h, a
	ld b, [hl]
	inc hl
	ld a, [wListScrollOffset]
	ld c, a
	ld a, [wCurrentMenuItem]
	add c
	cp b
	jr nc, .absent
	ld e, a
	ld d, 0
	add hl, de
	ld a, [wListMenuID]
	cp ITEMLISTMENU
	jr nz, .getItem
	add hl, de
.getItem
	ld a, [hl]
	cp HM01
	jp c, FindSupplyDescription
	cp TM01 + NUM_TMS
	jr nc, .absent
	scf
	ret
.absent
	and a
	ret

ShowMoveInfo:
	ld a, b
	and a
	ret z
	cp NUM_ATTACKS + 1
	ret nc
	ld [wMoveInfoMove], a
	ld a, c
	ld [wMoveInfoPP], a
	xor a
	ld [wMoveInfoPage], a
	ld [wMoveInfoIncoming], a
OpenInfoPanel:
; Save only the tile rows used by the panel. Leave both caller buffers alone.
	ldh a, [hAutoBGTransferEnabled]
	push af
	xor a
	ldh [hAutoBGTransferEnabled], a
	hlcoord 0, INFO_PANEL_FIRST_ROW
	ld b, SCREEN_WIDTH * INFO_PANEL_ROWS / 2
.saveRows
	ld a, [hli]
	ld d, a
	ld a, [hli]
	ld e, a
	push de
	dec b
	jr nz, .saveRows
	call WaitForInfoKeysReleased
.redraw
	call DrawMoveInfo
.wait
	call DelayFrame
	call Joypad
	ldh a, [hJoyPressed]
	bit B_PAD_B, a
	jp nz, .close
	ld b, a
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_SUPPLY
	jr z, .wait
	ld a, b
	bit B_PAD_SELECT, a
	jp nz, .changePage
	ld b, a
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_STATS
	jr z, .statsKeys
	cp INFO_BROWSE_LEARN
	jr nz, .wait
	ld a, b
	and PAD_LEFT | PAD_RIGHT
	jr z, .wait
	ld a, [wMoveInfoIncoming]
	xor 1
	ld [wMoveInfoIncoming], a
	jr z, .knownMove
	ld a, [wMoveNum]
	ld b, a
	ld c, INFO_UNKNOWN_PP
	jr .refreshMove
.knownMove
	call SelectReplacementInfoMove
	jr .refreshMove
.statsKeys
	bit B_PAD_UP, b
	jr nz, .previousSlot
	bit B_PAD_DOWN, b
	jr z, .wait
	ld a, [wMoveInfoSlot]
	inc a
	cp NUM_MOVES
	jr nc, .wait
	jr .trySlot
.previousSlot
	ld a, [wMoveInfoSlot]
	and a
	jr z, .wait
	dec a
.trySlot
	ld hl, wMoveInfoSlot
	ld d, [hl]
	ld [hl], a
	push de
	call SelectStatsInfoMove
	pop de
	ld a, b
	and a
	jr nz, .refreshMove
	ld a, d
	ld [wMoveInfoSlot], a
	jr .wait
.refreshMove
	ld a, b
	ld [wMoveInfoMove], a
	ld a, c
	ld [wMoveInfoPP], a
	jp .redraw
.changePage
	ld hl, wMoveInfoPage
	ld a, [hl]
	xor 1
	ld [hl], a
	jp .redraw
.close
	xor a
	ldh [hAutoBGTransferEnabled], a
	ld hl, wTileMap + SCREEN_AREA - 1
	ld b, SCREEN_WIDTH * INFO_PANEL_ROWS / 2
.restoreRows
	pop de
	ld a, e
	ld [hld], a
	ld a, d
	ld [hld], a
	dec b
	jr nz, .restoreRows
	ld a, 1
	ldh [hAutoBGTransferEnabled], a
	call Delay3
	call WaitForInfoKeysReleased
	pop af
	ldh [hAutoBGTransferEnabled], a
	ret

WaitForInfoKeysReleased:
	call DelayFrame
	call Joypad
	ldh a, [hJoyHeld]
	and PAD_A | PAD_B | PAD_START | PAD_SELECT
	jr nz, WaitForInfoKeysReleased
	xor a
	ldh [hJoyFiltered], a
	ret

DrawMoveInfo:
	xor a
	ldh [hAutoBGTransferEnabled], a
	hlcoord 0, INFO_PANEL_FIRST_ROW
	lb bc, INFO_PANEL_ROWS - 2, SCREEN_WIDTH - 2
	call TextBoxBorder
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_SUPPLY
	jr z, .supply
	farcall ReadMoveInfoName
	call ReadMoveInfoData
	hlcoord 1, 12
	ld de, wMoveInfoName
	call PlaceString
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_LEARN
	jr nz, .choosePage
	hlcoord 14, 12
	ld de, MoveInfoKnownText
	ld a, [wMoveInfoIncoming]
	and a
	jr z, .compareHeading
	ld de, MoveInfoNewText
.compareHeading
	call PlaceString
.choosePage
	ld a, [wMoveInfoPage]
	and a
	jr nz, .effect
	farcall DrawMoveInfoType
	call DrawMoveInfoTraitLabel
	call DrawMoveInfoPower
	call DrawMoveInfoAccuracy
	call DrawMoveInfoPP
	hlcoord 1, 16
	ld de, MoveInfoEffectText
	jr .show
.effect
	call DrawMoveInfoEffect
	hlcoord 1, 16
	ld de, MoveInfoStatsText
	jr .show
.supply
	farcall ReadSupplyInfoName
	hlcoord 1, 12
	ld de, wMoveInfoName
	call PlaceString
	ld a, [wMoveInfoMove]
	call FindSupplyDescription
	call PrintInfoDescription
	hlcoord 1, 16
	ld de, SupplyInfoBackText
.show
	call PlaceString
	ld a, 1
	ldh [hAutoBGTransferEnabled], a
	jp Delay3

ReadMoveInfoData:
	ld a, [wMoveInfoMove]
	dec a
	ld hl, Moves
	ld bc, MOVE_LENGTH
	call AddNTimes
	ld a, [wBuffer]
	push af
	ld de, wMoveInfoData
	ld a, BANK(Moves)
	call FarCopyData
	pop af
	ld [wBuffer], a
	ret

DrawPPRestoreTargetInfo:
	ld a, [wCurrentMenuItem]
	dec a
	cp NUM_MOVES
	ret nc
	ld [wMoveInfoSlot], a
	call SelectReplacementInfoMove
	ld a, b
	and a
	ret z
	cp NUM_ATTACKS + 1
	ret nc
	ld [wMoveInfoMove], a
	ld a, c
	ld [wMoveInfoPP], a
	call ReadMoveInfoData
	hlcoord 1, 15
	ld bc, SCREEN_WIDTH - 2
	ld a, ' '
	call FillMemory
	call DrawMoveInfoPP
	jp Delay3

DrawMoveInfoPower:
	hlcoord 1, 14
	ld de, MoveInfoPowerText
	call PlaceString
	hlcoord 5, 14
	ld a, [wMoveInfoData + MOVE_EFFECT]
	cp SPECIAL_DAMAGE_EFFECT
	jr z, .variable
	cp SUPER_FANG_EFFECT
	jr z, .variable
	cp OHKO_EFFECT
	jr z, .variable
	ld a, [wMoveInfoData + MOVE_POWER]
	and a
	jr z, .dash
	ld de, wMoveInfoData + MOVE_POWER
	lb bc, 1, 3
	jp PrintNumber
.variable
	ld de, MoveInfoVariableText
	jp PlaceString
.dash
	ld [hl], '-'
	ret

DrawMoveInfoAccuracy:
	hlcoord 9, 14
	ld de, MoveInfoAccuracyText
	call PlaceString
	ld a, [wMoveInfoData + MOVE_EFFECT]
	cp SWIFT_EFFECT
	jr z, .bypass
	ld a, [wMoveInfoData + MOVE_ACC]
	ld c, a
	ld b, 0
	ld hl, MoveInfoAccuracyPercent
	add hl, bc
	ld d, h
	ld e, l
	hlcoord 12, 14
	lb bc, 1, 3
	call PrintNumber
	hlcoord 15, 14
	ld de, MoveInfoAccuracyScale
	jp PlaceString
.bypass
	hlcoord 13, 14
	ld de, MoveInfoNoCheckText
	jp PlaceString

DrawMoveInfoPP:
	hlcoord 1, 15
	ld de, MoveInfoPPText
	call PlaceString
	ld a, [wMoveInfoPP]
	cp INFO_UNKNOWN_PP
	jr nz, .known
	hlcoord 4, 15
	ld de, wMoveInfoData + MOVE_PP
	lb bc, 1, 2
	jp PrintNumber
.known
	and PP_MASK
	ld [wMoveInfoNumber], a
	hlcoord 4, 15
	ld de, wMoveInfoNumber
	lb bc, 1, 2
	call PrintNumber
	hlcoord 6, 15
	ld [hl], '/'
	call CalculateMoveInfoMaxPP
	ld [wMoveInfoNumber], a
	hlcoord 7, 15
	ld de, wMoveInfoNumber
	lb bc, 1, 2
	call PrintNumber
	hlcoord 10, 15
	ld de, MoveInfoBasePPText
	call PlaceString
	hlcoord 15, 15
	ld de, wMoveInfoData + MOVE_PP
	lb bc, 1, 2
	jp PrintNumber

CalculateMoveInfoMaxPP:
	ld a, [wMoveInfoPP]
	and PP_UP_MASK
	swap a
	srl a
	srl a
	ld c, a
	ld a, [wMoveInfoData + MOVE_PP]
	ld d, a
	ret z
	ld b, 0
.perUpgrade
	sub 5
	jr c, .countUpgrades
	ld e, a
	inc b
	ld a, b
	cp 7
	jr z, .countUpgrades
	ld a, e
	jr .perUpgrade
.countUpgrades
	ld a, d
.total
	add b
	dec c
	jr nz, .total
	ret

MoveInfoAccuracyPercent:
FOR raw, 256
	db (raw * 100 + 254) / 255
ENDR

MoveInfoStartText:    db "START INFO@"
MoveInfoKnownText:    db "KNOWN@"
MoveInfoNewText:      db "NEW@"
MoveInfoPowerText:    db "POW@"
MoveInfoAccuracyText: db "ACC@"
MoveInfoVariableText: db "VAR@"
MoveInfoNoCheckText:  db "NONE@"
MoveInfoAccuracyScale: db "/100@"
MoveInfoPPText:       db "PP@"
MoveInfoBasePPText:   db "BASE@"
MoveInfoEffectText:   db "SELECT EFFECT  B@"
MoveInfoStatsText:    db "SELECT STATS   B@"

DrawMoveInfoTraitLabel:
	farcall ReadMoveInfoTraits
	ld a, e
	and a
	ret z
	ld de, .high
	dec a
	jr z, .print
	ld de, .priority
	dec a
	jr z, .print
	ld de, .both
.print
	hlcoord 10, 13
	jp PlaceString
.high db "HIGH CRIT@"
.priority db "PRIORITY@"
.both db "PRIO/CRIT@"

INCLUDE "data/moves/info_effects.asm"
INCLUDE "data/items/supply_info.asm"
