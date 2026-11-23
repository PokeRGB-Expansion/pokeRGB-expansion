PrintStrengthText:
	ld hl, wStatusFlags1
	set BIT_STRENGTH_ACTIVE, [hl]
	ld hl, UsedStrengthText
	call PrintText
	ld hl, CanMoveBouldersText
	jp PrintText

UsedStrengthText:
	text_far _UsedStrengthText
	text_asm
	ld a, [wCurPartySpecies]
	call PlayCry
	call Delay3
	jp TextScriptEnd

CanMoveBouldersText:
	text_far _CanMoveBouldersText
	text_end

IsSurfingAllowed:
; Report a refusal through the same text and status bit as the party action.
	call GetSurfMapRestriction
	jr c, .refuse
	ld hl, wStatusFlags1
	set BIT_SURF_ALLOWED, [hl]
	ret
.refuse
	push hl
	ld hl, wStatusFlags1
	res BIT_SURF_ALLOWED, [hl]
	pop hl
	jp PrintText

GetSurfMapRestriction::
; Carry indicates that Surf is prohibited here. HL points to the reason.
	ld a, [wStatusFlags6]
	bit BIT_ALWAYS_ON_BIKE, a
	jr nz, .forcedBike
	ld a, [wCurMap]
	cp SEAFOAM_ISLANDS_B4F
	jr nz, .allowed
	CheckBothEventsSet EVENT_SEAFOAM4_BOULDER1_DOWN_HOLE, EVENT_SEAFOAM4_BOULDER2_DOWN_HOLE
	jr z, .allowed
	ld hl, SeafoamIslandsB4FStairsCoords
	call ArePlayerCoordsInArray
	ret nc
	ld hl, CurrentTooFastText
	ret
.forcedBike
	ld hl, CyclingIsFunText
	scf
	ret
.allowed
	and a
	ret

SeafoamIslandsB4FStairsCoords:
	dbmapcoord  7, 11
	db -1 ; end

CurrentTooFastText:
	text_far _CurrentTooFastText
	text_end

CyclingIsFunText:
	text_far _CyclingIsFunText
	text_end
