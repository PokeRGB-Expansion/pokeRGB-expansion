DEF REGISTERED_ITEM_TAG EQU $d6

ShowRegisteredItemActions::
; Carry means use the item. Registration and cancellation return to the bag.
	hlcoord 8, 10
	lb bc, 4, 10
	call TextBoxBorder
	call IsCurrentItemRegistered
	ld de, ItemRegisterActions
	jr nz, .draw
	ld de, ItemClearActions
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
	call IsCurrentItemRegistered
	jr z, .clear
	ld a, REGISTERED_ITEM_TAG
	ld [wRegisteredItemTag], a
	ld a, [wCurItem]
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

ItemRegisterActions:
	db "USE"
	next "REGISTER@"

ItemClearActions:
	db "USE"
	next "CLEAR@"

IsCurrentItemRegistered:
	ld a, [wRegisteredItemTag]
	cp REGISTERED_ITEM_TAG
	ret nz
	ld a, [wRegisteredItem]
	ld hl, wCurItem
	cp [hl]
	ret

IsCurrentFieldItemRegistrable::
	ld a, [wCurItem]
IsRegistrableFieldItem:
	cp BICYCLE
	jr z, .allowed
	cp OLD_ROD
	jr c, .unavailable
	cp SUPER_ROD + 1
	jr nc, .unavailable
	ASSERT GOOD_ROD == OLD_ROD + 1 && SUPER_ROD == GOOD_ROD + 1
.allowed
	scf
	ret
.unavailable
	and a
	ret

CanUseRegisteredItem::
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
	call HasRegisteredItem
	ret
.unavailable
	and a
	ret

HasRegisteredItem:
	call GetRegisteredFieldItem
	ret nc
	ld b, a
	call IsItemInBag
	jr z, .unavailable
	scf
	ret
.unavailable
	and a
	ret

GetRegisteredFieldItem::
	ld a, [wRegisteredItemTag]
	cp REGISTERED_ITEM_TAG
	jr nz, .unavailable
	ld a, [wRegisteredItem]
	jp IsRegistrableFieldItem
.unavailable
	and a
	ret

UseRegisteredItem::
	call HasRegisteredItem
	ret nc
	xor a
	ld [wPseudoItemID], a
	ld a, [wRegisteredItem]
	ld [wCurItem], a
	call UseItem
.waitForRelease
	call DelayFrame
	call Joypad
	ldh a, [hJoyHeld]
	bit B_PAD_SELECT, a
	jr nz, .waitForRelease
	ret
