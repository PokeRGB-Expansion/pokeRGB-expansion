; The full-party renderer keeps the vendor's menu state while covering its
; tilemap. Change its selection now and redraw the vendor only on return.
; E = +1 or -1. Return carry when the party view needs its new machine.
BrowsePartyOffer::
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_MART
	jr nc, .vendor
	and a
	ret
.vendor
	ld c, e
	call StepMachineOffer
	ret nc
	call LoadInspectedMachine
	call CacheMachinePartyEligibility
	farcall ReadMoveInfoName
	scf
	ret

RedrawMachineVendor::
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_MART
	ret c
	call z, PrintListMenuEntries
	jp PlaceMenuCursor

; The vendor may sell just one machine among ordinary supplies. Only show
; the comparison control when another machine can actually be reached.
HasOtherMachineOffer::
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_MART
	jr nc, .vendor
	and a
	ret
.vendor
	ld c, 1
	call FindAdjacentMachineOffer
	ret c
	ld c, -1
	jp FindAdjacentMachineOffer

; C = +1 or -1. Return carry only when the selection changes.
StepMachineOffer:
	call FindAdjacentMachineOffer
	ret nc
	ld [wSelectedMachine], a
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_PRIZE
	ld a, e
	jr z, .setRow
; Scroll only when the new item falls outside the selectable rows.
	ld hl, wListScrollOffset
	sub [hl]
	jr nc, .atOrBelowTop
	ld [hl], e
	xor a
	jr .setRow
.atOrBelowTop
	ld b, a
	ld a, [wMaxMenuItem]
	cp b
	jr c, .scrollDown
	ld a, b
	jr .setRow
.scrollDown
	ld b, a
	ld a, e
	sub b
	ld [hl], a
	ld a, b
.setRow
	ld [wCurrentMenuItem], a
	scf
	ret

; Search without moving the cursor. Carry means A is the machine ID and E is
; its zero-based index. Entries outside the machine range are not previewed.
FindAdjacentMachineOffer:
	ld a, [wCurrentMenuItem]
	ld e, a
	ld hl, wPrize1
	ld b, 3
	ld a, [wMoveInfoBrowse]
	cp INFO_BROWSE_PRIZE
	jr z, .pointAtSelection
	ld a, [wListScrollOffset]
	add e
	ld e, a
	ld a, [wListPointer]
	ld l, a
	ld a, [wListPointer + 1]
	ld h, a
	ld a, [hli]
	ld b, a
.pointAtSelection
	ld d, 0
	add hl, de
.scan
	ld a, e
	add c
	cp b
	ret nc
	ld e, a
	bit 7, c
	jr nz, .previous
	inc hl
	jr .checkItem
.previous
	dec hl
.checkItem
	ld a, [hl]
	cp HM01
	jr c, .scan
	cp TM01 + NUM_TMS
	jr nc, .scan
	scf
	ret
