; checks if the mon in [wWhichPokemon] already knows the move in [wMoveNum]
CheckIfMoveIsKnown:
	call SelectedMonKnowsMove
	ret nc
	ld hl, AlreadyKnowsText
	call PrintText
	scf
	ret

SelectedMonKnowsMove::
	ld a, [wWhichPokemon]
	ld e, a
	ld a, [wMoveNum]
	ld d, a
; D = move, E = party slot. Return carry if the move is present.
PartySlotKnowsMove::
	ld a, e
	ld hl, wPartyMon1Moves
	ld bc, PARTYMON_STRUCT_LENGTH
	call AddNTimes
	ld b, NUM_MOVES
.loop
	ld a, [hli]
	cp d
	jr z, .found
	dec b
	jr nz, .loop
	and a
	ret
.found
	scf
	ret

AlreadyKnowsText:
	text_far _AlreadyKnowsText
	text_end
