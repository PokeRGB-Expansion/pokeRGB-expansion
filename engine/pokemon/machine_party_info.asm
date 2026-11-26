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

PUSHS
SECTION "TM party preview", ROMX

; The offer stays highlighted while this read-only view borrows its display.
; Preserve only presentation data in the existing decompression workspace.
; All machine-list callers enter here with cartridge RAM closed.
ShowMachinePartyPreview::
	ldh a, [hAutoBGTransferEnabled]
	push af
	ldh a, [hTileAnimations]
	push af
	ldh a, [rBGP]
	push af
	ldh a, [rOBP0]
	push af
	ld a, [wPokedexNum] ; party icons and level printing share this scratch byte
	push af
	ld a, [wUpdateSpritesEnabled]
	push af
	ld a, $ff ; VBlank must keep these static icons in shadow OAM.
	ld [wUpdateSpritesEnabled], a
	ld a, [wSymmetricSpriteOAMAttributes]
	push af
	ld a, [wOAMBaseTile]
	push af
	ld a, [wBuffer]
	push af
	ldh a, [hPartyMonIndex]
	push af
	xor a
	ldh [hAutoBGTransferEnabled], a
	ldh [hTileAnimations], a
	call DisableLCD
	call .openSpriteRAM
	ld hl, wTileMap
	ld de, sTMPreviewScreen
	ld bc, SCREEN_AREA
	call CopyData
	ld hl, wShadowOAM
	ld de, sTMPreviewOAM
	ld bc, OAM_COUNT * OBJ_SIZE
	call CopyData
	ld hl, vSprites
	ld de, sTMPreviewIconTiles
	ld bc, ((ICON_QUADRUPED + 1) * 4) tiles
	call CopyData
	xor a
	ld [rRAMG], a
	farcall LoadStaticPartyIconPatterns
	call ClearSprites
	farcall DrawStaticPartyIcons
	call DrawTMPreview
	call .showCompleteScreen
	ld b, SET_PAL_GENERIC
	call RunPaletteCommand
	call GBPalNormal
.show
	ld a, 1
	ldh [hAutoBGTransferEnabled], a
	call Delay3
.wait
	call DelayFrame
	farcall ReadInfoButtons
	ldh a, [hJoyPressed]
	bit B_PAD_B, a
	jr nz, .close
	ldh a, [hJoyFiltered]
	and PAD_UP | PAD_DOWN
	ld e, 1
	cp PAD_DOWN
	jr z, .move
	cp PAD_UP
	jr nz, .wait
	dec e
	dec e
.move
	farcall BrowsePartyOffer
	jr nc, .wait
	xor a
	ldh [hAutoBGTransferEnabled], a
	call DrawTMPreview
	jr .show
.close
	call DisableLCD
	xor a
	ldh [hAutoBGTransferEnabled], a
	call .openSpriteRAM
	ld hl, sTMPreviewScreen
	ld de, wTileMap
	ld bc, SCREEN_AREA
	call CopyData
	ld hl, sTMPreviewOAM
	ld de, wShadowOAM
	ld bc, OAM_COUNT * OBJ_SIZE
	call CopyData
	ld hl, sTMPreviewIconTiles
	ld de, vSprites
	ld bc, ((ICON_QUADRUPED + 1) * 4) tiles
	call CopyData
	xor a
	ld [rRAMG], a
	farcall RedrawMachineVendor
	call .showCompleteScreen
	call RunDefaultPaletteCommand
	; Wait for B to be released before the underlying list accepts input.
.release
	call DelayFrame
	call Joypad
	ldh a, [hJoyHeld]
	and PAD_B | PAD_UP | PAD_DOWN | PAD_A | PAD_START | PAD_SELECT
	jr nz, .release
	pop af
	ldh [hPartyMonIndex], a
	pop af
	ld [wBuffer], a
	pop af
	ld [wOAMBaseTile], a
	pop af
	ld [wSymmetricSpriteOAMAttributes], a
	pop af
	ld [wUpdateSpritesEnabled], a
	pop af
	ld [wPokedexNum], a
	pop af
	ldh [rOBP0], a
	pop af
	ldh [rBGP], a
	pop af
	ldh [hTileAnimations], a
	pop af
	ldh [hAutoBGTransferEnabled], a
	ret

; Install all three thirds of the window and its sprites before the first
; visible frame. The normal VBlank transfer borrows SP, so keep it atomic.
.showCompleteScreen
	ld a, 1
	ldh [hAutoBGTransferEnabled], a
	di
	REPT 3
		call AutoBgMapTransfer
	ENDR
	call hDMARoutine
	ei
	jp EnableLCD

.openSpriteRAM
	ld a, RAMG_SRAM_ENABLE
	ld [rRAMG], a
	xor a ; sprite buffers are in bank 0
	ld [rRAMB], a
	ret

; Use the teaching screen's two-line rows. Read levels, moves and nicknames
; straight from the party; a preview must not select a pupil or load a record
; into the caller's active Pokémon buffer.
DrawTMPreview:
	hlcoord 0, 0
	ld bc, SCREEN_AREA
	ld a, ' '
	call FillMemory
	hlcoord 0, 12
	lb bc, 4, 18
	call TextBoxBorder
	call DrawPreviewMachineOffer
	farcall HasOtherMachineOffer
	ld de, .back
	jr nc, .footer
	ld de, .browse
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_STONE_MART
	jr nz, .footer
	ld de, .browseStones
.footer
	hlcoord 1, 16
	call PlaceString
	ld a, [wPartyCount]
	and a
	jr nz, .roster
	hlcoord 2, 5
	ld de, .empty
	jp PlaceString
.roster
	farjp DrawTMPreviewRows

.empty db "No party #MON.@"
.back db "B:BACK@"
.browseStones db "UP/DN:STONE B:BACK@"
.browse db "UP/DOWN:TM  B:BACK@"

; The counter is hidden while browsing the party. Identify the exact machine
; even when two machines teach the same move and have different prices.
DrawPreviewMachineOffer:
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_STONE_MART
	jr nz, .machine
	hlcoord 1, 13
	ld de, wMoveInfoName
	call PlaceString
	ld a, [wCurItem]
	push af
	ld a, [wMoveInfoMove]
	ld [wCurItem], a
	call GetItemPrice
	hlcoord 1, 14
	ld c, MONEY_SIGN | LEADING_ZEROES | LEFT_ALIGN | 3
	call PrintBCDNumber
	pop af
	ld [wCurItem], a
	ret
.machine
	decoord 1, 13
	ld a, [wSelectedMachine]
	call WriteMachineName
	ld a, ' '
	ld [de], a
	hlcoord 6, 13
	ld de, wMoveInfoName
	call PlaceString
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_MART
	ret c
	jr nz, .prize
	ld a, [wSelectedMachine]
	ld e, a
	farcall ReadTMPrice
	ret c
	ld d, 0
	push de ; price as two BCD bytes, high byte first
	ld hl, sp + 0
	ld d, h
	ld e, l
	hlcoord 1, 14
	ld c, MONEY_SIGN | LEADING_ZEROES | LEFT_ALIGN | 2
	call PrintBCDNumber
	pop de
	ret
.prize
	ld a, [wCurrentMenuItem]
	add a
	ld e, a
	ld d, 0
	ld hl, wPrize1Price
	add hl, de
	ld d, h
	ld e, l
	hlcoord 1, 14
	ld c, LEADING_ZEROES | LEFT_ALIGN | 2
	call PrintBCDNumber
	ld de, .coins
	jp PlaceString
.coins db " COINS@"

POPS
