; Return the item ID in A, its description in DE, and carry on success.
FindSupplyDescription:
	ld hl, SupplyInfoEntries
	ld de, 3
	call IsInArray
	ret nc
	ld a, [hli]
	ld e, [hl]
	inc hl
	ld d, [hl]
	scf
	ret

SupplyInfoBackText: db "B BACK@"

SupplyInfoEntries:
	dbw POKE_BALL, .POKE_BALL
	dbw GREAT_BALL, .GREAT_BALL
	dbw ULTRA_BALL, .ULTRA_BALL
	dbw POTION, .POTION
	dbw SUPER_POTION, .SUPER_POTION
	dbw HYPER_POTION, .HYPER_POTION
	dbw FRESH_WATER, .FRESH_WATER
	dbw SODA_POP, .SODA_POP
	dbw LEMONADE, .LEMONADE
	dbw MAX_POTION, .MAX_POTION
	dbw FULL_RESTORE, .FULL_RESTORE
	dbw ANTIDOTE, .ANTIDOTE
	dbw BURN_HEAL, .BURN_HEAL
	dbw ICE_HEAL, .ICE_HEAL
	dbw AWAKENING, .AWAKENING
	dbw PARLYZ_HEAL, .PARLYZ_HEAL
	dbw FULL_HEAL, .FULL_HEAL
	dbw REVIVE, .REVIVE
	dbw MAX_REVIVE, .MAX_REVIVE
	dbw REPEL, .REPEL
	dbw SUPER_REPEL, .SUPER_REPEL
	dbw MAX_REPEL, .MAX_REPEL
	dbw ESCAPE_ROPE, .ESCAPE_ROPE
	dbw POKE_DOLL, .POKE_DOLL
	dbw X_ACCURACY, .X_ACCURACY
	dbw GUARD_SPEC, .GUARD_SPEC
	dbw PP_UP, .PP_UP
	dbw ETHER, .ETHER
	dbw MAX_ETHER, .MAX_ETHER
	dbw ELIXER, .ELIXER
	dbw MAX_ELIXER, .MAX_ELIXER
	dbw RARE_CANDY, .RARE_CANDY
	dbw HP_UP, .HP_UP
	dbw PROTEIN, .PROTEIN
	dbw IRON, .IRON
	dbw CARBOS, .CARBOS
	dbw CALCIUM, .CALCIUM
	dbw X_ATTACK, .X_ATTACK
	dbw X_DEFEND, .X_DEFEND
	dbw X_SPEED, .X_SPEED
	dbw X_SPECIAL, .X_SPECIAL
	dbw FIRE_STONE, .FIRE_STONE
	dbw WATER_STONE, .FIRE_STONE
	dbw THUNDER_STONE, .FIRE_STONE
	dbw LEAF_STONE, .FIRE_STONE
	dbw MOON_STONE, .FIRE_STONE
	dbw DIRE_HIT, .DIRE_HIT
	db -1

.POKE_BALL
	db "For catching wild@", "#MON.@", 0

.GREAT_BALL
	db "A stronger ball@", "for wild #MON.@", 0

.ULTRA_BALL
	db "A strong ball for@", "wild #MON.@", 0

.POTION
	db "Restores up to@", "{d:POTION_HP} HP.@", 0

.SUPER_POTION
	db "Restores up to@", "{d:SUPER_POTION_HP} HP.@", 0

.HYPER_POTION
	db "Restores up to@", "{d:HYPER_POTION_HP} HP.@", 0

.FRESH_WATER
	db "Restores up to@", "{d:FRESH_WATER_HP} HP.@", 0

.SODA_POP
	db "Restores up to@", "{d:SODA_POP_HP} HP.@", 0

.LEMONADE
	db "Restores up to@", "{d:LEMONADE_HP} HP.@", 0

.MAX_POTION
	db "Restores all HP.@", "Use on a conscious@", "#MON.@", 0

.FULL_RESTORE
	db "Restores all HP@", "and cures status.@", 0

.ANTIDOTE
	db "Cures poisoning.@", 0

.BURN_HEAL
	db "Heals a burn.@", 0

.ICE_HEAL
	db "Thaws a frozen@", "#MON.@", 0

.AWAKENING
	db "Wakes a sleeping@", "#MON.@", 0

.PARLYZ_HEAL
	db "Cures paralysis.@", 0

.FULL_HEAL
	db "Cures a status@", "condition.@", 0

.REVIVE
	db "Revives a fainted@", "#MON with half@", "its max HP.@", 0

.MAX_REVIVE
	db "Revives a fainted@", "#MON with full HP.@", 0

.REPEL
	db "Repels wild #MON@", "below the lead's@", "Lv for {d:REPEL_STEPS} steps.@", 0

.SUPER_REPEL
	db "Repels wild #MON@", "below the lead's@", "Lv for {d:SUPER_REPEL_STEPS} steps.@", 0

.MAX_REPEL
	db "Repels wild #MON@", "below the lead's@", "Lv for {d:MAX_REPEL_STEPS} steps.@", 0

.ESCAPE_ROPE
	db "Returns you from@", "certain dungeons@", "to a healing spot.@", 0

.POKE_DOLL
	db "Lets you escape@", "a wild battle.@", 0

.X_ACCURACY
	db "Skips the usual@", "accuracy check.@", 0

.GUARD_SPEC
	db "Guards against@", "enemy stat drops@", "in battle.@", 0

.PP_UP
	db "Raises one move's@", "maximum PP.@", 0

.ETHER
	db "Restores up to@", "{d:ETHER_RESTORE_PP} PP for one@", "move.@", 0

.MAX_ETHER
	db "Restores all PP@", "for one move.@", 0

.ELIXER
	db "Restores up to@", "{d:ETHER_RESTORE_PP} PP for each@", "move.@", 0

.MAX_ELIXER
	db "Restores all PP@", "for every move.@", 0

.RARE_CANDY
	db "Raises a #MON@", "by one level.@", 0

.HP_UP
	db "Helps raise@", "HP through@", "stat experience.@", 0

.PROTEIN
	db "Helps raise@", "Attack through@", "stat experience.@", 0

.IRON
	db "Helps raise@", "Defense through@", "stat experience.@", 0

.CARBOS
	db "Helps raise@", "Speed through@", "stat experience.@", 0

.CALCIUM
	db "Helps raise@", "Special through@", "stat experience.@", 0

.X_ATTACK
	db "Raises Attack@", "in battle.@", 0

.X_DEFEND
	db "Raises Defense@", "in battle.@", 0

.X_SPEED
	db "Raises Speed@", "in battle.@", 0

.X_SPECIAL
	db "Raises Special@", "in battle.@", 0

.FIRE_STONE
	db "Evolves certain@", "#MON.@", 0

.DIRE_HIT
IF DEF(_POKERGB_CORE)
	db "Raises critical@", "hit odds.@", 0
ELSE
	db "Lowers critical@", "hit odds.@", 0
ENDC
