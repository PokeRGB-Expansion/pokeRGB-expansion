DrawStorageListCapacity::
	ld a, [wListMenuID]
	cp ITEMLISTMENU
	jr z, .itemList
	cp PCPOKEMONLISTMENU
	ret nz
	ld hl, wBoxCount
	call .matchesList
	ret nz
	hlcoord 5, 3
	jr DrawBoxCapacity
.itemList
	ld hl, wNumBagItems
	call .matchesList
	jr z, .bag
	ld hl, wNumBoxItems
	call .matchesList
	ret nz
	hlcoord 5, 3
	jr DrawItemPCCapacity
.bag
	call DrawBagItemStates
	hlcoord 5, 3
	ld de, BagCapacityText
	ld b, BAG_ITEM_CAPACITY
	ld a, [wNumBagItems]
	jr DrawOccupiedSlots
.matchesList
	ld a, [wListPointer]
	cp l
	ret nz
	ld a, [wListPointer + 1]
	cp h
	ret

DrawItemPCMenuCapacity::
	hlcoord 2, 1
DrawItemPCCapacity:
	ld de, ItemPCCapacityText
	ld b, PC_ITEM_CAPACITY
	ld a, [wNumBoxItems]
	jr DrawOccupiedSlots

DrawBoxPCMenuCapacity::
	hlcoord 2, 1
DrawBoxCapacity:
	ld de, BoxCapacityText
	ld b, MONS_PER_BOX
	ld a, [wBoxCount]
	; fall through

DrawOccupiedSlots:
; Draw a label followed by occupied slots in a and total slots in b.
	push bc
	push af
	call PlaceString
	ld h, b
	ld l, c
	push hl
	ld hl, sp + 3 ; occupied slot count
	ld d, h
	ld e, l
	pop hl
	lb bc, 1, 2
	call PrintNumber
	ld a, '/'
	ld [hli], a
	push hl
	ld hl, sp + 5 ; total slot count
	ld d, h
	ld e, l
	pop hl
	lb bc, 1, 2
	call PrintNumber
	add sp, 4
	ret

BagCapacityText:    db "BAG @"
ItemPCCapacityText: db "ITEM PC @"
BoxCapacityText:    db "BOX @"

; The second line of a key item is free in the Bag. Keep sell prices clear.
DrawBagItemStates:
	ld a, [wPrintItemPrices]
	and a
	ret nz
	farcall GetRegisteredFieldItem
	jr nc, .noRegistration
	ld a, [wRegisteredItem]
	jr .start
.noRegistration
	xor a
.start
	ld b, a ; registered item, or zero
	ld a, [wListScrollOffset]
	add a
	ld hl, wBagItems
	add l
	ld l, a
	jr nc, .firstRow
	inc h
.firstRow
	decoord 6, 5
	ld c, 4
.row
	ld a, [hli]
	cp $ff
	ret z
	inc hl ; skip quantity
	push hl
	push de
	push bc
	ld h, d
	ld l, e
	cp b
	ld de, .selectText
	jr z, .label
IF DEF(_POKERGB_CORE)
	cp EXP_ALL
	jr nz, .next
	ld a, [wExpAllDisabled]
	and a
	ld de, .onText
	jr z, .label
	ld de, .offText
ELSE
	jr .next
ENDC
.label
	call PlaceString
.next
	pop bc
	pop hl
	ld de, 2 * SCREEN_WIDTH
	add hl, de
	ld d, h
	ld e, l
	pop hl
	dec c
	jr nz, .row
	ret
.selectText db "SELECT@"
IF DEF(_POKERGB_CORE)
.onText db "ON@"
.offText db "OFF@"

DrawExpAllActions::
	hlcoord 8, 10
	lb bc, 4, 10
	call TextBoxBorder
	ld a, [wExpAllDisabled]
	and a
	ld de, .turnOff
	jr z, .draw
	ld de, .turnOn
.draw
	hlcoord 10, 11
	jp PlaceString
.turnOff
	db "TURN OFF"
	next "TOSS@"
.turnOn
	db "TURN ON"
	next "TOSS@"
ENDC
