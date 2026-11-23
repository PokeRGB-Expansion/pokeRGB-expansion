DEF REGISTERED_ITEM_TAG EQU $d6

ShowBicycleActions::
; Carry means use the Bicycle. Registration and cancellation return to the bag.
	hlcoord 8, 10
	lb bc, 4, 10
	call TextBoxBorder
	call IsBicycleRegistered
	ld de, BicycleRegisterActions
	jr nz, .draw
	ld de, BicycleClearActions
.draw
	hlcoord 10, 11
	call PlaceString
	ld a, 11
	ld [wTopMenuItemY], a
	ld a, 9
	ld [wTopMenuItemX], a
	xor a
	ld [wCurrentMenuItem], a
	ld [wLastMenuItem], a
	ld [wMenuWatchMovingOutOfBounds], a
	inc a
	ld [wMaxMenuItem], a
	ld a, PAD_A | PAD_B
	ld [wMenuWatchedKeys], a
	call HandleMenuInput
	bit B_PAD_B, a
	jr nz, .back
	ld a, [wCurrentMenuItem]
	and a
	jr z, .use
	call IsBicycleRegistered
	jr z, .clear
	ld a, REGISTERED_ITEM_TAG
	ld [wRegisteredItemTag], a
	ld a, BICYCLE
	ld [wRegisteredItem], a
	jr .back
.clear
	xor a
	ld [wRegisteredItemTag], a
	ld [wRegisteredItem], a
.back
	and a
	ret
.use
	scf
	ret

BicycleRegisterActions:
	db "USE"
	next "REGISTER@"

BicycleClearActions:
	db "USE"
	next "CLEAR@"

IsBicycleRegistered:
	ld a, [wRegisteredItemTag]
	cp REGISTERED_ITEM_TAG
	ret nz
	ld a, [wRegisteredItem]
	cp BICYCLE
	ret

CanUseRegisteredBicycle::
; The overworld checks transitions and pending battles before calling here.
	ldh a, [hJoyPressed]
	bit B_PAD_SELECT, a
	jr z, .unavailable
	ld a, [wStatusFlags5]
	bit BIT_UNKNOWN_5_2, a
	jr nz, .unavailable
	call IsPlayerCharacterBeingControlledByGame
	jr nz, .unavailable
	ld a, [wLinkState]
	dec a ; match the bag's Cable Club restriction
	jr z, .unavailable
	call HasRegisteredBicycle
	ret
.unavailable
	and a
	ret

HasRegisteredBicycle:
	call IsBicycleRegistered
	jr nz, .unavailable
	ld b, BICYCLE
	call IsItemInBag
	jr z, .unavailable
	scf
	ret
.unavailable
	and a
	ret

UseRegisteredBicycle::
	call HasRegisteredBicycle
	ret nc
	xor a
	ld [wPseudoItemID], a
	ld a, BICYCLE
	ld [wCurItem], a
	call UseItem
.waitForRelease
	call DelayFrame
	call Joypad
	ldh a, [hJoyHeld]
	bit B_PAD_SELECT, a
	jr nz, .waitForRelease
	ret
