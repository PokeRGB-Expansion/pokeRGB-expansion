GetMachinePrice::
; Input:  [wCurItem] = Item ID of a TM
; Output: Stores the TM price at hItemPrice
	ld a, [wCurItem]
	ld e, a
	call ReadTMPrice
	ret c
	ld a, e
	ldh [hItemPrice + 1], a
	xor a
	ldh [hItemPrice], a
	ldh [hItemPrice + 2], a
	ret

; E = machine ID. Return the packed thousands digit in E, or carry for an HM.
ReadTMPrice::
	ld a, e
	sub TM01 ; underflows below 0 for HM items (before TM items)
	ret c ; HMs are priceless
	ld d, a
	ld hl, TechnicalMachinePrices
	srl a
	ld c, a
	ld b, 0
	add hl, bc
	ld a, [hl] ; a contains byte whose high or low nybble is the TM price (in thousands)
	srl d
	jr nc, .highNybbleIsPrice ; is TM id odd?
	swap a
.highNybbleIsPrice
	and $f0
	ld e, a
	ret

INCLUDE "data/items/tm_prices.asm"
