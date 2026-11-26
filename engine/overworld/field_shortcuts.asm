; Find a first eligible party member without changing the party selection.
; Input A: move. Output carry on success, A: party index, C: the move.
FindFieldShortcutUser:
	ld c, a
	ld a, [wPartyCount]
	and a
	ret z
	ld d, a
	ld e, 0
	ld hl, wPartyMon1Moves
.nextMon
	ld b, NUM_MOVES
.nextMove
	ld a, [hli]
	cp c
	jr z, .found
	dec b
	jr nz, .nextMove
	push bc
	ld bc, PARTYMON_STRUCT_LENGTH - NUM_MOVES
	add hl, bc
	pop bc
	inc e
	dec d
	jr nz, .nextMon
	and a
	ret
.found
	ld a, e
	scf
	ret

FindTerrainShortcut::
; The caller has already checked ordinary interactions and scripted movement.
	predef GetTileAndCoordsInFrontOfPlayer
	lda_coord 8, 9
	ld [wTilePlayerStandingOn], a
	farcall GetCutTreeTile
	jr nc, .surf
	ld a, [wObtainedBadges]
	bit BIT_CASCADEBADGE, a
	jr z, .unavailable
	ld a, CUT
	jp FindFieldShortcutUser
.surf
	ld a, [wWalkBikeSurfState]
	cp 2 ; no A-button dismount
	jr z, .unavailable
	ld a, [wObtainedBadges]
	bit BIT_SOULBADGE, a
	jr z, .unavailable
	call IsSurfShortcutSurface
	jr nc, .unavailable
	farcall GetSurfMapRestriction
	jr c, .unavailable
	farcall CheckSurfBoardingCollision
	jr c, .unavailable
	ld a, SURF
	jp FindFieldShortcutUser
.unavailable
	and a
	ret

IsSurfShortcutSurface:
; A reused shore tile ID alone does not make a statue or floor a prompt.
; The existing boarding check also validates actual water tiles and collisions.
	ld a, [wTileInFrontOfPlayer]
	cp $14
	jr z, .surface
	cp $32
	jr nz, .tryEastSafariShore
	ld a, [wCurMapTileset]
	cp OVERWORLD
	jr z, .surface
	cp PLATEAU
	jr z, .surface
	jr .noSurface
.tryEastSafariShore
	cp $48
	jr nz, .noSurface
	ld a, [wCurMapTileset]
	cp FOREST ; Safari Zone shoreline
	jr nz, .noSurface
.surface
	scf
	ret
.noSurface
	and a
	ret

OfferOverworldShortcut::
	ld a, [wSpriteIndex]
	cp TEXT_REGISTERED_ITEM
	jp z, UseRegisteredItem

OfferTerrainShortcut::
	call FindTerrainShortcut
	ret nc
	push bc
	ld hl, CutShortcutPrompt
	ld a, c
	cp CUT
	jr z, .ask
	ld hl, SurfShortcutPrompt
.ask
	call ConfirmFieldShortcut
	pop de
	ret nz
	push de
	call FindTerrainShortcut
	pop de
	ret nc
	ld b, a
	ld a, c
	cp e ; reject a changed target
	ret nz
	ld a, b
	ld [wWhichPokemon], a
	ld a, c
	cp CUT
	jr nz, .board
	predef UsedCut
	ret
.board
	ld a, SURFBOARD
	ld [wCurItem], a
	ld [wPseudoItemID], a
	jp UseItem

BoulderShortcutText::
	text_asm
OfferBoulderShortcut::
	ld a, [wSpriteIndex]
	push af
	push bc ; keep the stock text's cursor
	call FindBoulderShortcut
	pop bc
	jr nc, .original
	ld hl, StrengthShortcutPrompt
	call ConfirmFieldShortcut
	pop bc
	jr nz, .finish
	ld a, b
	call FindBoulderShortcut
	jr nc, .finish
	ld [wWhichPokemon], a
	ld hl, wPartyMon1Species
	ld bc, PARTYMON_STRUCT_LENGTH
	call AddNTimes
	ld a, [hl]
	ld [wCurPartySpecies], a
	ld a, [wWhichPokemon]
	ld hl, wPartyMonNicks
	call GetPartyMonName
	predef PrintStrengthText
.finish
	ld a, 1
	ld [wDoNotWaitForButtonPressAfterDisplayingText], a
	jp TextScriptEnd
.original
	pop af
	ld hl, BoulderStockText
	ret

BoulderStockText:
	text_far _BoulderText
	text_end

FindBoulderShortcut:
; A is the sprite ID set during the normal boulder conversation.
	and a
	ret z
	ld b, a
	ld a, [wNumSprites]
	cp b
	jr c, .unavailable
	ld a, [wStatusFlags1]
	bit BIT_STRENGTH_ACTIVE, a
	jr nz, .unavailable
	ld a, [wObtainedBadges]
	bit BIT_RAINBOWBADGE, a
	jr z, .unavailable
	ld a, b
	ldh [hSpriteIndex], a
	call GetSpriteMovementByte2Pointer
	ld a, [hl]
	cp BOULDER_MOVEMENT_BYTE_2
	jr nz, .unavailable
	ld a, STRENGTH
	jp FindFieldShortcutUser
.unavailable
	and a
	ret

ConfirmFieldShortcut:
	call PrintText
.waitForRelease
	call DelayFrame
	call Joypad
	ldh a, [hJoyHeld]
	and PAD_A | PAD_B
	jr nz, .waitForRelease
	call YesNoChoice
	ld a, [wCurrentMenuItem]
	and a
	ret

CutShortcutPrompt:
	text "Use CUT?"
	done
SurfShortcutPrompt:
	text "Use SURF?"
	done
StrengthShortcutPrompt:
	text "Use STRENGTH?"
	done
