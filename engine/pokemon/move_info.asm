; A read-only panel. Its data lives outside the active menu and battle state.
DEF INFO_UNKNOWN_PP EQU $ff
DEF INFO_PANEL_FIRST_ROW EQU 11
DEF INFO_PANEL_ROWS EQU SCREEN_HEIGHT - INFO_PANEL_FIRST_ROW
; The battle and machine browsers use a second line for controls.
DEF BROWSE_PANEL_FIRST_ROW EQU INFO_PANEL_FIRST_ROW - 1
DEF BROWSE_PANEL_ROWS EQU SCREEN_HEIGHT - BROWSE_PANEL_FIRST_ROW

InspectFightMove:
	ld a, [wCurrentMenuItem]
	dec a
	cp NUM_MOVES
	ret nc
	ld [wMoveInfoSlot], a
	ld a, INFO_BROWSE_FIGHT
	ld [wMoveInfoBrowse], a
	call SelectInfoMoveSlot
	call ShowMoveInfo
	ld a, [wMoveInfoSlot]
	inc a ; FIGHT uses one-based rows
	ld [wCurrentMenuItem], a
	ret

InspectStatsMove:
	xor a
	ld [wMoveInfoSlot], a
	ld a, INFO_BROWSE_STATS
	ld [wMoveInfoBrowse], a
	call SelectInfoMoveSlot
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

SelectInfoMoveSlot:
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_FIGHT
	ld hl, wBattleMonMoves
	ld de, wBattleMonPP - wBattleMonMoves
	jr z, .read
	ld hl, wLoadedMonMoves
	ld de, wLoadedMonPP - wLoadedMonMoves
.read
	ld a, [wMoveInfoSlot]
	ld c, a
	ld b, 0
	add hl, bc
	ld b, [hl] ; move
	add hl, de
	ld c, [hl] ; PP including PP Ups
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
	xor a
	ld [wMoveInfoIncoming], a
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
	ld a, [wListMenuID]
	cp ITEMLISTMENU
	jr z, .inspectable
	cp PRICEDITEMLISTMENU
	jr z, .inspectable
	call HandleMenuInput
	ld [wMoveInfoNumber], a
	ret
.inspectable
	ld a, 1
	jr HandleListInfoInput

HandlePrizeMoveInfoInput:
	ld a, 2
HandleListInfoInput:
; Cover the whole bottom window so short names never leave old dialogue
; behind. CANCEL and items without INFO restore exactly what was underneath.
	ld [wMoveInfoHint], a
	add sp, -6 * SCREEN_WIDTH
	ld hl, sp + 0
	call ReadMenuWithInfoHint
	add sp, 6 * SCREEN_WIDTH
	jr FinishMenuWithInfoHint

HandleLearnerMoveInfoInput:
	ld a, 3
	ld [wMoveInfoHint], a
	add sp, -2 * SCREEN_WIDTH
	ld hl, sp + 0
	call ReadMenuWithInfoHint
	add sp, 2 * SCREEN_WIDTH
FinishMenuWithInfoHint:
	xor a
	ld [wMoveInfoHint], a
	ret

ReadMenuWithInfoHint:
	ld a, l
	ld [wMoveInfoData], a
	ld a, h
	ld [wMoveInfoData + 1], a
	push hl
	call GetInfoHintArea
	pop de
	call CopyData
	call HandleMenuInput
	ld [wMoveInfoNumber], a
RestoreMoveInfoHintRows:
	call GetInfoHintArea
	ld d, h
	ld e, l
	ld hl, wMoveInfoData
	ld a, [hli]
	ld h, [hl]
	ld l, a
	jp CopyData

GetInfoHintArea:
	ld a, [wMoveInfoHint]
	cp 3
	hlcoord 0, 14
	ld bc, 2 * SCREEN_WIDTH
	ret z
	hlcoord 0, 12
	ld bc, 6 * SCREEN_WIDTH
	ret

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
	call FindPrizeMachine
	ret nc
	jp DrawMachineHintName

FindPrizeMachine:
	ld a, [wWhichPrizeWindow]
	cp 2
	jr nz, .absent
	ld a, [wCurrentMenuItem]
	cp 3
	jr nc, .absent
	ld e, a
	ld d, 0
	ld hl, wPrize1
	add hl, de
	ld a, [hl]
	cp HM01
	jr c, .absent
	cp TM01 + NUM_TMS ; carry if the prize is a valid machine
	ret
.absent
	and a
	ret

InspectPrizeMove:
	call FindPrizeMachine
	ret nc
	ld b, INFO_BROWSE_PRIZE
	jr InspectMachineMove

InspectListedMove::
	call FindListedInfoItem
	ret nc
	cp HM01
	jr c, .supply
	ld b, INFO_BROWSE_MACHINE
	ld c, a
	ld a, [wListMenuID]
	cp PRICEDITEMLISTMENU
	jr nz, .machine
	ld b, INFO_BROWSE_MART
.machine
	ld a, c
	jr InspectMachineMove
.supply
	ld [wMoveInfoMove], a
	ld a, INFO_BROWSE_SUPPLY
	ld [wMoveInfoBrowse], a
	jp OpenInfoPanel
InspectMachineMove:
	ld [wSelectedMachine], a
	ld a, b
	ld [wMoveInfoBrowse], a
	call LoadInspectedMachine
	ld a, [wMoveInfoMove]
	ld b, a
	ld c, INFO_UNKNOWN_PP
	jp ShowMoveInfo

LoadInspectedMachine:
	ld a, [wSelectedMachine]
	ld [wMoveInfoMove], a
	farjp ReadMoveInfoMachine

DrawMachineListHint:
	call FindListedInfoItem
	ret nc
	cp HM01
	jr nc, DrawMachineHintName
	ld [wMoveInfoMove], a
	farcall ReadSupplyInfoName
	jr DrawListInfoHint

DrawMachineHintName:
	ld [wMoveInfoMove], a
	farcall ReadMoveInfoMachine
	ld a, [wMoveInfoMove]
	and a
	ret z
	cp NUM_ATTACKS + 1
	ret nc
	farcall ReadMoveInfoName
DrawListInfoHint:
	hlcoord 0, 12
	lb bc, 4, SCREEN_WIDTH - 2
	call TextBoxBorder
	hlcoord 1, 14
	ld de, wMoveInfoName
	call PlaceString
	hlcoord 1, 16
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
OpenInfoPanel:
	call WaitForInfoKeysReleased
; Save only the tile rows used by the panel. Leave both caller buffers alone.
	ldh a, [hAutoBGTransferEnabled]
	push af
.saveBackground
	xor a
	ldh [hAutoBGTransferEnabled], a
	call GetInfoPanelRows
.saveRows
	ld a, [hli]
	ld d, a
	ld a, [hli]
	ld e, a
	push de
	dec b
	jr nz, .saveRows
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_FIGHT
	call z, UncoverBattleAboveMoveInfo
.redraw
	call DrawMoveInfo
.wait
	call DelayFrame
	call ReadInfoButtons
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
	cp INFO_BROWSE_MACHINE
	jr c, .otherKeys
	bit B_PAD_A, b
	jp nz, .party
	cp INFO_BROWSE_MART
	jr c, .wait
	ldh a, [hJoyFiltered]
	and PAD_UP | PAD_DOWN
	cp PAD_DOWN
	ld c, 1
	jr z, .browse
	cp PAD_UP
	jr nz, .wait
	ld c, -1
.browse
	call StepMachineOffer
	jr nc, .wait
	ld c, 2 ; restore the list before drawing its new selection
	jp .uncover
.otherKeys
	cp INFO_BROWSE_FIGHT
	jr nz, .checkStats
	ldh a, [hJoyFiltered]
	ld b, a
	jr .slotKeys
.checkStats
	cp INFO_BROWSE_STATS
	jr z, .slotKeys
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
.slotKeys
	ld a, b
	and PAD_UP | PAD_DOWN
	cp PAD_UP
	jr z, .previousSlot
	cp PAD_DOWN
	jp nz, .wait
	ld a, [wMoveInfoSlot]
	inc a
	cp NUM_MOVES
	jp nc, .wait
	jr .trySlot
.previousSlot
	ld a, [wMoveInfoSlot]
	and a
	jp z, .wait
	dec a
.trySlot
	ld hl, wMoveInfoSlot
	ld d, [hl]
	ld [hl], a
	push de
	call SelectInfoMoveSlot
	pop de
	ld a, b
	and a
	jr z, .invalidSlot
	cp NUM_ATTACKS + 1
	jr c, .refreshMove
.invalidSlot
	ld a, d
	ld [wMoveInfoSlot], a
	jp .wait
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
.party
	ld c, 1
	jr .uncover
.close
	ld c, 0
.uncover
	xor a
	ldh [hAutoBGTransferEnabled], a
	call GetInfoPanelRows
	ld hl, wTileMap + SCREEN_AREA - 1
.restoreRows
	pop de
	ld a, e
	ld [hld], a
	ld a, d
	ld [hld], a
	dec b
	jr nz, .restoreRows
	bit 1, c
	jr nz, .newOffer
	bit 0, c
	jr nz, .showParty
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_FIGHT
	jr nz, .showList
; FIGHT redraws its cursor and type/PP box together before accepting input.
	pop af
	ret
.showList
	ld a, 1
	ldh [hAutoBGTransferEnabled], a
	call Delay3
	call WaitForInfoKeysReleased
.restoreTransfer
	pop af
	ldh [hAutoBGTransferEnabled], a
	ret
.showParty
; The restored list is the return destination. Keep it off screen during
; this transition so PARTY opens directly, even while A is still held.
	call CacheMachinePartyEligibility
	farcall ShowMachinePartyPreview
	jr .restoreTransfer

.newOffer
; Reuse the list renderer with its original background restored. Saving these
; rows again keeps the new item and price intact when the player closes INFO.
	call RedrawMachineVendor
	call LoadInspectedMachine
	jp .saveBackground

ReadInfoButtons::
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_FIGHT
	jr z, .repeat
	cp INFO_BROWSE_MART
	jp c, Joypad
.repeat
; Use the normal menu repeat delay for browsing. Action
; buttons still use hJoyPressed and never repeat into a sale.
	ldh a, [hJoy7]
	push af
	ld a, 1
	ldh [hJoy7], a
	call JoypadLowSensitivity
	pop af
	ldh [hJoy7], a
	ret

GetInfoPanelRows:
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_FIGHT
	jr z, .large
	cp INFO_BROWSE_MACHINE
	hlcoord 0, INFO_PANEL_FIRST_ROW
	ld b, SCREEN_WIDTH * INFO_PANEL_ROWS / 2
	ret c
.large
	hlcoord 0, BROWSE_PANEL_FIRST_ROW
	ld b, SCREEN_WIDTH * BROWSE_PANEL_ROWS / 2
	ret

WaitForInfoKeysReleased:
	call DelayFrame
	call Joypad
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_FIGHT
	jr z, .allKeys
	cp INFO_BROWSE_MART
	jr nc, .allKeys
	ldh a, [hJoyHeld]
	and PAD_A | PAD_B | PAD_START | PAD_SELECT
	jr .check
.allKeys
	ldh a, [hJoyHeld]
.check
	and a
	jr nz, WaitForInfoKeysReleased
	xor a
	ldh [hJoyFiltered], a
	ret

DrawMoveInfo:
	xor a
	ldh [hAutoBGTransferEnabled], a
	call GetInfoPanelRows
	ld b, INFO_PANEL_ROWS - 2
	jr c, .frame
	ld b, BROWSE_PANEL_ROWS - 2
.frame
	ld c, SCREEN_WIDTH - 2
	call TextBoxBorder
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_SUPPLY
	jp z, .supply
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
	ld de, MoveInfoEffectText
	jr .controls
.effect
	call DrawMoveInfoEffect
	ld de, MoveInfoStatsText
.controls
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_FIGHT
	jr z, .browseControls
	cp INFO_BROWSE_MACHINE
	hlcoord 1, 16
	jp c, .show
.browseControls
; The shared move renderer lays out four rows (name, then stats or effect).
; Shift them up together in browsing views to fit both lines of controls.
	hlcoord 0, 12
	decoord 0, 11
	ld bc, 4 * SCREEN_WIDTH
	call CopyData
	hlcoord 1, 15
	ld bc, SCREEN_WIDTH - 2
	ld a, ' '
	call FillMemory
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_FIGHT
	jr nz, .machineControls
	call DrawFightBrowseHint
	jr .shortPageHint
.machineControls
	cp INFO_BROWSE_MACHINE
	ld de, .bagControls
	jr z, .machineHint
	call HasOtherMachineOffer
	ld de, .oneOfferControls
	jr nc, .machineHint
	ld de, .shopControls
.machineHint
	hlcoord 1, 15
	call PlaceString
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_MACHINE
	ld de, .selectEffect
	jr z, .nextPage
.shortPageHint
	ld de, .shopEffect
.nextPage
	ld a, [wMoveInfoPage]
	and a
	jr z, .placePage
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_MACHINE
	ld de, .selectStats
	jr z, .placePage
	ld de, .shopStats
.placePage
	hlcoord 1, 16
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

.bagControls  db "A:PARTY     B:BACK@"
.oneOfferControls db "A:PARTY@"
.shopControls db "UP/DOWN:TM A:PARTY@"
.selectEffect db "SELECT:EFFECT@"
.selectStats  db "SELECT:STATS@"
.shopEffect   db "SEL:EFFECT B:BACK@"
.shopStats    db "SEL:STATS  B:BACK@"

UncoverBattleAboveMoveInfo:
	ld a, [wStatusFlags7]
	bit BIT_TEST_BATTLE, a ; this mode omits the ordinary FIGHT hover box
	ret nz
; Restore just the controls above the card from the original battlefield.
; FIGHT redraws them for the last inspected move when the card closes.
	hlcoord 9, 7, wTileMapBackup
	decoord 9, 7
	ld bc, CHARLEN("START INFO")
	call CopyData
	hlcoord 0, 8, wTileMapBackup
	decoord 0, 8
	ld bc, 11
	call CopyData
	hlcoord 0, 9, wTileMapBackup
	decoord 0, 9
	ld bc, 11
	jp CopyData

DrawFightBrowseHint:
	ld a, [wNumMovesMinusOne]
	and a
	jr z, .position
	hlcoord 1, 15
	ld de, .directions
	call PlaceString
.position
	ld a, [wMoveInfoSlot]
	add "1"
	ldcoord_a 16, 15
	ld a, "/"
	ldcoord_a 17, 15
	ld a, [wNumMovesMinusOne]
	add "1"
	ldcoord_a 18, 15
	ret
.directions db "UP/DOWN:MOVE@"

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
	ld a, [wMoveInfoMove]
	cp COUNTER ; its normal damage rule doubles the previous hit
	jr nz, .byEffect
	ld a, [wMoveInfoData + MOVE_EFFECT]
	and a
	jr z, .dash
.byEffect
	ld a, [wMoveInfoData + MOVE_EFFECT]
	cp SPECIAL_DAMAGE_EFFECT
	jr z, .dash
	cp SUPER_FANG_EFFECT
	jr z, .dash
	cp OHKO_EFFECT
	jr z, .dash
	ld a, [wMoveInfoData + MOVE_POWER]
	and a
	jr z, .dash
	ld de, wMoveInfoData + MOVE_POWER
	lb bc, 1, 3
	jp PrintNumber
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

INCLUDE "engine/pokemon/machine_party_info.asm"

INCLUDE "data/moves/info_effects.asm"
INCLUDE "data/items/supply_info.asm"

INCLUDE "engine/pokemon/tm_offer_browsing.asm"
