DrawPartyMenu_::
	xor a
	ldh [hAutoBGTransferEnabled], a
	call ClearScreen
	call UpdateSprites
	farcall LoadMonPartySpriteGfxWithLCDDisabled ; load pokemon icon graphics

RedrawPartyMenu_::
	ld a, [wPartyMenuTypeOrMessageID]
	cp SWAP_MONS_PARTY_MENU
	jp z, .printMessage
	call ErasePartyMenuCursors
	farcall InitPartyMenuBlkPacket
	hlcoord 3, 0
	ld de, wPartySpecies
	xor a
	ld c, a
	ldh [hPartyMonIndex], a
	ld [wWhichPartyMenuHPBar], a
.loop
	ld a, [de]
	cp $FF ; reached the terminator?
	jp z, .afterDrawingMonEntries
	push bc
	push de
	push hl
	ld a, c
	push hl
	ld hl, wPartyMonNicks
	call GetPartyMonName
	pop hl
	call PlaceString ; print the pokemon's name
	farcall WriteMonPartySpriteOAMByPartyIndex ; place the appropriate pokemon icon
	ldh a, [hPartyMonIndex]
	ld [wWhichPokemon], a
	inc a
	ldh [hPartyMonIndex], a
	call LoadMonData
	pop hl
	push hl
	ld a, [wMenuItemToSwap]
	and a ; is the player swapping pokemon positions?
	jr z, .skipUnfilledRightArrow
; if the player is swapping pokemon positions
	dec a
	ld b, a
	ld a, [wWhichPokemon]
	cp b ; is the player swapping the current pokemon in the list?
	jr nz, .skipUnfilledRightArrow
; the player is swapping the current pokemon in the list
	dec hl
	dec hl
	dec hl
	ld a, '▷' ; unfilled right arrow menu cursor
	ld [hli], a ; place the cursor
	inc hl
	inc hl
.skipUnfilledRightArrow
	ld a, [wPartyMenuTypeOrMessageID] ; menu type
	cp TMHM_PARTY_MENU
	jr z, .teachMoveMenu
	cp EVO_STONE_PARTY_MENU
	jr z, .evolutionStoneMenu
	push hl
	ld bc, 14 ; 14 columns to the right
	add hl, bc
	ld de, wLoadedMonStatus
	call PrintStatusCondition
	pop hl
	push hl
	ld bc, SCREEN_WIDTH + 1 ; down 1 row and right 1 column
	ldh a, [hUILayoutFlags]
	set BIT_PARTY_MENU_HP_BAR, a
	ldh [hUILayoutFlags], a
	add hl, bc
	predef DrawHP2 ; draw HP bar and prints current / max HP
	ldh a, [hUILayoutFlags]
	res BIT_PARTY_MENU_HP_BAR, a
	ldh [hUILayoutFlags], a
	call SetPartyMenuHPBarColor ; color the HP bar (on SGB)
	pop hl
	jr .printLevel
.teachMoveMenu
	push hl
	farcall SelectedMonKnowsMove
	ld a, 2
	jr c, .moveStatus
	farcall CanLearnSelectedMachine
	ld a, e
	and a
	jr z, .moveStatus
	ld a, 1
.moveStatus
	pop hl
	push hl
	call PlaceTMPartyStatus
	pop hl
	jr .printLevel
.placeMoveLearnabilityString
	ld bc, SCREEN_WIDTH + 9 ; 1 row down and 9 columns right
	push hl
	add hl, bc
	call PlaceString
	pop hl
.printLevel
	ld bc, 10 ; move 10 columns to the right
	add hl, bc
	call PrintLevel
	pop hl
	pop de
	inc de
	ld bc, 2 * SCREEN_WIDTH
	add hl, bc
	pop bc
	inc c
	jp .loop
.evolutionStoneMenu
	push hl
	ld a, [wWhichPokemon]
	ld e, a
	ld a, [wEvoStoneItemID]
	ld d, a
	farcall CanPartyMonEvolveWithStone
	ld a, 0
	rla
	jr .moveStatus
.afterDrawingMonEntries
	ld b, SET_PAL_PARTY_MENU
	call RunPaletteCommand
.printMessage
	ld hl, wStatusFlags5
	ld a, [hl]
	push af
	push hl
	set BIT_NO_TEXT_DELAY, [hl]
	ld a, [wPartyMenuTypeOrMessageID] ; message ID
	cp FIRST_PARTY_MENU_TEXT_ID
	jr nc, .printItemUseMessage
	add a
	ld hl, PartyMenuMessagePointers
	ld b, 0
	ld c, a
	add hl, bc
	ld a, [hli]
	ld h, [hl]
	ld l, a
	call PrintText
.done
	pop hl
	pop af
	ld [hl], a
	ld a, 1
	ldh [hAutoBGTransferEnabled], a
	call Delay3
	jp GBPalNormal
.printItemUseMessage
	and $0F
	ld hl, PartyMenuItemUseMessagePointers
	add a
	ld c, a
	ld b, 0
	add hl, bc
	ld a, [hli]
	ld h, [hl]
	ld l, a
	push hl
	ld a, [wUsedItemOnWhichPokemon]
	ld hl, wPartyMonNicks
	call GetPartyMonName
	pop hl
	call PrintText
	jr .done

DrawTMPreviewRows::
	xor a
	ldh [hPartyMonIndex], a
	hlcoord 3, 0
.row
	push hl
	ldh a, [hPartyMonIndex]
	ld hl, wPartyMonNicks
	call SkipFixedLengthTextEntries
	ld d, h
	ld e, l
	pop hl
	push hl
	call PlaceString
	ldh a, [hPartyMonIndex]
	ld hl, wPartyMon1Level
	ld bc, PARTYMON_STRUCT_LENGTH
	call AddNTimes
	ld a, [hl]
	pop hl
	push hl
	ld bc, 10
	add hl, bc
	call PrintPartyLevelFromA
	call .status
	pop hl
	push hl
	call PlaceTMPartyStatus
	pop hl
	ld de, 2 * SCREEN_WIDTH
	add hl, de
	ldh a, [hPartyMonIndex]
	inc a
	ldh [hPartyMonIndex], a
	ld b, a
	ld a, [wPartyCount]
	cp b
	jr nz, .row
	ret

.status
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_STONE_MART
	jr nz, .machine
	ldh a, [hPartyMonIndex]
	ld e, a
	ld a, [wMoveInfoMove]
	ld d, a
	farcall CanPartyMonEvolveWithStone
	ld a, 0
	rla
	ret
.machine
	ldh a, [hPartyMonIndex]
	ld e, a
	ld a, [wMoveInfoMove]
	ld d, a
	farcall PartySlotKnowsMove
	ld a, 2
	ret c
	ldh a, [hPartyMonIndex]
	ld c, a
	ld hl, wMachineInfoAble
	ld b, FLAG_TEST
	predef FlagActionPredef
	ld a, c
	and a
	ret z
	ld a, 1
	ret

; Both party screens use the same status words and row layout.
; A = 0 for unable, 1 for able, 2 for known. HL = nickname position.
PlaceTMPartyStatus:
	ld bc, SCREEN_WIDTH + 9
	add hl, bc
	and a
	ld de, PartyNotAbleText
	jr z, .print
	dec a
	ld de, PartyAbleText
	jr z, .print
	ld de, PartyKnowsMoveText
.print
	jp PlaceString

PartyKnowsMoveText:: db "KNOWS@"
PartyAbleText:: db "ABLE@"
PartyNotAbleText:: db "NOT ABLE@"

PartyMenuItemUseMessagePointers:
	dw AntidoteText
	dw BurnHealText
	dw IceHealText
	dw AwakeningText
	dw ParlyzHealText
	dw PotionText
	dw FullHealText
	dw ReviveText
	dw RareCandyText

PartyMenuMessagePointers:
	dw PartyMenuNormalText
	dw PartyMenuItemUseText
	dw PartyMenuBattleText
	dw PartyMenuUseTMText
	dw PartyMenuSwapMonText
	dw PartyMenuItemUseText
	dw FieldPartyMenuText

FieldPartyMenuText:
	text "Choose a #MON."
	line "SELECT to switch."
	done

PartyMenuNormalText:
	text_far _PartyMenuNormalText
	text_end

PartyMenuItemUseText:
	text_far _PartyMenuItemUseText
	text_end

PartyMenuBattleText:
	text_far _PartyMenuBattleText
	text_end

PartyMenuUseTMText:
	text_far _PartyMenuUseTMText
	text_end

PartyMenuSwapMonText:
	text_far _PartyMenuSwapMonText
	text_end

PotionText:
	text_far _PotionText
	text_end

AntidoteText:
	text_far _AntidoteText
	text_end

ParlyzHealText:
	text_far _ParlyzHealText
	text_end

BurnHealText:
	text_far _BurnHealText
	text_end

IceHealText:
	text_far _IceHealText
	text_end

AwakeningText:
	text_far _AwakeningText
	text_end

FullHealText:
	text_far _FullHealText
	text_end

ReviveText:
	text_far _ReviveText
	text_end

RareCandyText:
	text_far _RareCandyText
	sound_get_item_1 ; probably supposed to play SFX_LEVEL_UP but the wrong music bank is loaded
	text_promptbutton
	text_end

SetPartyMenuHPBarColor:
	ld hl, wPartyMenuHPBarColors
	ld a, [wWhichPartyMenuHPBar]
	ld c, a
	ld b, 0
	add hl, bc
	call GetHealthBarColor
	ld b, SET_PAL_PARTY_MENU_HP_BARS
	call RunPaletteCommand
	ld hl, wWhichPartyMenuHPBar
	inc [hl]
	ret
