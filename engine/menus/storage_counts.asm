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
