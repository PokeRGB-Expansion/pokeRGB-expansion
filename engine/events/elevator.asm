DisplayElevatorFloorMenu:
	call FindElevatorCurrentFloor
	ld hl, WhichFloorText
	jr nc, .ask
	ld [wNamedObjectIndex], a
	call GetItemName
	call CopyToStringBuffer
	ld hl, WhichFloorWithCurrentText
.ask
	call PrintText
	ld hl, wItemList
	ld a, l
	ld [wListPointer], a
	ld a, h
	ld [wListPointer + 1], a
	ld a, [wListScrollOffset]
	push af
	xor a
	ld [wCurrentMenuItem], a
	ld [wListScrollOffset], a
	ld [wPrintItemPrices], a
	ld a, SPECIALLISTMENU
	ld [wListMenuID], a
	call DisplayListMenuID
	pop bc
	ld a, b
	ld [wListScrollOffset], a
	ret c
	ld hl, wElevatorWarpMaps
	ld a, [wWhichPokemon]
	add a
	ld d, 0
	ld e, a
	add hl, de
	ld a, [hli]
	ld b, a
	ld a, [hl]
	ld c, a
	ld a, [wWarpEntries + 3]
	cp c
	ret z ; Already at this floor.
	ld hl, wCurrentMapScriptFlags
	set BIT_CUR_MAP_USED_ELEVATOR, [hl]
	ld hl, wWarpEntries
	call .UpdateWarp

.UpdateWarp
	inc hl
	inc hl
	ld a, b
	ld [hli], a ; destination warp ID
	ld a, c
	ld [hli], a ; destination map ID
	ret

FindElevatorCurrentFloor:
; Return the floor's list ID in A, with carry, if the current exit map matches.
	ld a, [wItemList]
	and a
	ret z
	ld b, a
	ld a, [wWarpEntries + 3]
	ld c, a
	ld de, wElevatorWarpMaps + 1
	ld hl, wItemList + 1
.loop
	ld a, [de]
	cp c
	jr z, .found
	inc de
	inc de
	inc hl
	dec b
	jr nz, .loop
	and a
	ret
.found
	ld a, [hl]
	scf
	ret

WhichFloorWithCurrentText:
	text "Current floor "
	text_ram wStringBuffer
	line "Choose a floor."
	done

WhichFloorText:
	text_far _WhichFloorText
	text_end
