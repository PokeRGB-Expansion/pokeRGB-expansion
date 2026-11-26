DEF _NUM_TRAINER_MOVESETS = 0

; Write a regular trainer team and remember its address and size for trainer_moves.
; Accept the same level and species values as a db row, without its terminator.
MACRO trainer_party
	ASSERT FATAL, _NARG >= 2, "A trainer team needs a level and a Pokemon."
	REDEF _trainerPartyIndividualLevels = (\1) == $ff
	IF _trainerPartyIndividualLevels
		ASSERT FATAL, _NARG % 2 == 1, "Use one level per Pokemon after $ff."
		REDEF _trainerPartyCount = (_NARG - 1) / 2
	ELSE
		REDEF _trainerPartyCount = _NARG - 1
	ENDC
	ASSERT FATAL, _trainerPartyCount <= PARTY_LENGTH, "Too many Pokemon in this trainer team."
	REDEF _trainerPartyLabel EQUS "TrainerParty\@"
	REDEF _trainerPartyBytes = _NARG + 1
	REDEF _trainerMovesSlots = 0
_trainerPartyLabel:
	ASSERT FATAL, (\1) >= 1 && (\1) <= $ff, "Trainer levels must fit in one nonzero byte."
	db \1
	SHIFT
	REPT _trainerPartyCount
		IF _trainerPartyIndividualLevels
			ASSERT FATAL, (\1) >= 1 && (\1) <= $ff, "Trainer levels must fit in one nonzero byte."
			db \1
			SHIFT
		ENDC
		ASSERT FATAL, (\1) >= 1 && (\1) <= NUM_POKEMON_INDEXES, "Invalid trainer species. Omit the terminator."
		db \1
		SHIFT
	ENDR
	db 0
ENDM

; Replace the moves of one party member in the preceding trainer_party.
MACRO trainer_moves
	ASSERT FATAL, DEF(_trainerPartyCount), "Put trainer_moves immediately after trainer_party."
	ASSERT FATAL, @ - _trainerPartyLabel == _trainerPartyBytes, "Put trainer_moves immediately after its team."
	ASSERT FATAL, _NARG >= 2 && _NARG <= 1 + NUM_MOVES, "Give the party slot and one to four moves."
	ASSERT FATAL, (\1) >= 1 && (\1) <= _trainerPartyCount, "This trainer team has no such party slot."
	ASSERT FATAL, (_trainerMovesSlots & (1 << ((\1) - 1))) == 0, "This party slot already has a moveset."
	REDEF _trainerMovesSlots |= 1 << ((\1) - 1)
	PUSHS
	SECTION FRAGMENT "Trainer movesets", ROMX
	IF !_NUM_TRAINER_MOVESETS
TrainerMovesets:
	ENDC
	REDEF _NUM_TRAINER_MOVESETS += 1
	dw _trainerPartyLabel
	db (\1) - 1
	SHIFT
	REPT NUM_MOVES
		IF _NARG
			move_id \1
			SHIFT
		ELSE
			db NO_MOVE
		ENDC
	ENDR
	POPS
ENDM
