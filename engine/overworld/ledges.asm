HandleLedges::
	ld a, [wMovementFlags]
	bit BIT_LEDGE_OR_FISHING, a
	ret nz
	ld a, [wCurMapTileset]
	and a ; OVERWORLD
	ret nz
	predef GetTileAndCoordsInFrontOfPlayer
	ld a, [wSpritePlayerStateData1FacingDirection]
	ld b, a
	lda_coord 8, 9
	ld c, a
	ld a, [wTileInFrontOfPlayer]
	ld d, a
	ld hl, LedgeTiles
.loop
	ld a, [hli]
	cp $ff
	ret z
	cp b
	jr nz, .nextLedgeTile1
	ld a, [hli]
	cp c
	jr nz, .nextLedgeTile2
	ld a, [hli]
	cp d
	jr nz, .nextLedgeTile3
	ld a, [hl]
	ld e, a
	jr .foundMatch
.nextLedgeTile1
	inc hl
.nextLedgeTile2
	inc hl
.nextLedgeTile3
	inc hl
	jr .loop
.foundMatch
	ldh a, [hJoyHeld]
	and e
	ret z
IF DEF(_POKERGB_CORE)
	push de
	call CheckLedgeLanding
	pop de
	ret c
ENDC
	ld a, PAD_BUTTONS | PAD_CTRL_PAD
	ld [wJoyIgnore], a
	ld hl, wMovementFlags
	set BIT_LEDGE_OR_FISHING, [hl]
	call StartSimulatingJoypadStates
	ld a, e
	ld [wSimulatedJoypadStatesEnd], a
	ld [wSimulatedJoypadStatesEnd + 1], a
	ld a, $2
	ld [wSimulatedJoypadStatesIndex], a
	call LoadHoppingShadowOAM
	ld a, SFX_LEDGE
	call PlaySound
	ret

IF DEF(_POKERGB_CORE)
CheckLedgeLanding:
; Compare map positions so an NPC walking toward the landing counts as
; occupying it before the sprite finishes moving.
	ld a, [wYCoord]
	add 4
	ld b, a
	ld a, [wXCoord]
	add 4
	ld c, a
	ld a, e
	cp PAD_DOWN
	jr nz, .horizontal
	inc b
	inc b
	jr .findSprite
.horizontal
	ld a, c
	sub 2
	bit B_PAD_LEFT, e
	jr nz, .setX
	add 4
.setX
	ld c, a
.findSprite
	ld a, [wNumSprites]
	and a
	jr z, .reserve
	ld d, a
	ld hl, wSprite01StateData2MapY
.nextSprite
	ld a, [hli]
	cp b
	jr nz, .advance
	ld a, [hl]
	cp c
	jr nz, .advance
	push hl
	dec h
	ld a, l
	and $f0
	add SPRITESTATEDATA1_IMAGEINDEX
	ld l, a
	ld a, [hl]
	pop hl
	inc a
	jr z, .advance ; ignore hidden sprites
	scf
	ret
.advance
	ld a, l
	add SPRITESTATEDATA2_LENGTH - 1
	ld l, a
	dec d
	jr nz, .nextSprite
.reserve
	ld a, b
	ld [wLedgeLandingY], a
	ld a, c
	ld [wLedgeLandingX], a
	and a
	ret
ENDC

INCLUDE "data/tilesets/ledge_tiles.asm"

LoadHoppingShadowOAM:
	ld hl, vChars1 tile $7f
	ld de, LedgeHoppingShadow
	lb bc, BANK(LedgeHoppingShadow), (LedgeHoppingShadowEnd - LedgeHoppingShadow) / TILE_1BPP_SIZE
	call CopyVideoDataDouble
	ld a, $9
	lb bc, $54, $48 ; b, c = y, x coordinates of shadow
	ld de, LedgeHoppingShadowOAMBlock
	call WriteOAMBlock
	ret

LedgeHoppingShadow:
	INCBIN "gfx/overworld/shadow.1bpp"
LedgeHoppingShadowEnd:

LedgeHoppingShadowOAMBlock:
; tile ID, attributes
	db $ff, OAM_PAL1
	db $ff, OAM_XFLIP
	db $ff, OAM_YFLIP
	db $ff, OAM_XFLIP | OAM_YFLIP
