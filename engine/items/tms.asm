; Legacy move-based lookup. A move alone identifies the first matching machine.
CanLearnTM:
	ld a, [wMoveNum]
	ld b, a
	ld c, 0
	ld hl, TechnicalMachines
.find
	ld a, [hli]
	cp b
	jr z, TestMachineLearnset
	inc c
	ld a, c
	cp NUM_TM_HM
	jr c, .find
	ld c, 0
	ret

; Use the selected machine's own learnset bit, even if another teaches the same move.
; Return the result in E across the bank switch.
CanLearnSelectedMachine::
	ld a, [wSelectedMachine]
	call GetMachineLearnsetIndex
	ld c, a
	call TestMachineLearnset
	ld e, c
	ret

TestMachineLearnset:
	ld a, [wCurPartySpecies]
	ld [wCurSpecies], a
	call GetMonHeader
	ld hl, wMonHLearnset
	ld b, FLAG_TEST
	predef_jump FlagActionPredef

; converts TM/HM number in [wTempTMHM] into move number
; HMs start at 51
TMToMove:
	ld a, [wTempTMHM]
	dec a
	ld hl, TechnicalMachines
	ld b, $0
	ld c, a
	add hl, bc
	ld a, [hl]
	ld [wTempTMHM], a
	ret

INCLUDE "data/moves/tmhm_moves.asm"

ReadMoveInfoMachine::
	ld a, [wMoveInfoMove]
	call GetMachineLearnsetIndex
	ld e, a
	ld d, 0
	ld hl, TechnicalMachines
	add hl, de
	ld a, [hl]
	ld [wMoveInfoMove], a
	ret

; The item list puts HMs first. The move table and species flags put TMs first.
GetMachineLearnsetIndex:
	sub TM01
	ret nc
	add NUM_TM_HM
	ret
