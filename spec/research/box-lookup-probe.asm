; Disposable stock-ROM experiment. See storage-policy-and-code.md for setup.
IF DEF(_READ_ONLY_BOX_PROBE)
; Test only. Caller has already found the active box full. Return a zero-based
; inactive box or $ff. This standalone probe has no capture or gift caller.
ProbeNextSavedBox::
	ld a, [wCurrentBoxNum]
	ld c, a
	and BOX_NUM_MASK
	ld e, a
	bit BIT_HAS_CHANGED_BOXES, c
	jr nz, .readSaved
	call .nextIndex
	ret
.readSaved
	ld a, RAMG_SRAM_ENABLE
	ld [rRAMG], a
	ld a, BMODE_ADVANCED
	ld [rBMODE], a
	ld d, NUM_BOXES - 1
.scan
	call .nextIndex
	push de
	ld hl, BoxSRAMPointerTable
	call LookupSavedBoxByIndex
	ld a, b
	ld [rRAMB], a
	ld a, [hl]
	pop de
	cp MONS_PER_BOX
	jr c, .found
	dec d
	jr nz, .scan
	ld e, $ff
.found
	xor a
	ld [rBMODE], a
	ld [rRAMG], a
	ld a, e
	ret
.nextIndex
	inc e
	ld a, e
	cp NUM_BOXES
	ret c
	xor a
	ld e, a
	ret
ProbeNextSavedBoxEnd::
ENDC
