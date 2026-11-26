DrawMoveInfoEffect:
	ld a, [wMoveInfoMove]
	ld b, a
	ld hl, MoveInfoSpecificDescriptions
.findMove
	ld a, [hli]
	and a
	jr z, .byEffect
	cp b
	jr nz, .nextMove
	ld a, [wMoveInfoData + MOVE_EFFECT]
	cp [hl]
	jr nz, .byEffect
	inc hl
	ld a, [hli]
	ld e, a
	ld d, [hl]
	jr .print
.nextMove
	inc hl
	inc hl
	inc hl
	jr .findMove
.byEffect
	ld a, [wMoveInfoData + MOVE_EFFECT]
	and a
	jr nz, .lookupEffect
	farcall ReadMoveInfoTraits
	ld a, e
	and a
	jr z, .lookupEffect
	ld de, MoveInfoHighCritical
	dec a
	jr z, .print
	ld de, MoveInfoPriority
	dec a
	jr z, .print
	ld de, MoveInfoBothTraits
	jr .print
.lookupEffect
	cp NUM_MOVE_EFFECTS + 1
	ld de, MoveInfoUnknownEffect
	jr nc, .print
	ld l, a
	ld h, 0
	add hl, hl
	ld de, MoveInfoDescriptions
	add hl, de
	ld a, [hli]
	ld e, a
	ld d, [hl]
.print
PrintInfoDescription:
	hlcoord 1, 13
	ld b, 3
.row
	push hl
	push bc
	ld c, SCREEN_WIDTH - 2
.char
	ld a, [de]
	inc de
	and a
	jr z, .done
	cp '@'
	jr z, .next
	ld [hli], a
	dec c
	jr nz, .char
.skipRestOfRow
	ld a, [de]
	inc de
	and a
	jr z, .done
	cp '@'
	jr nz, .skipRestOfRow
.next
	pop bc
	pop hl
	push de
	ld de, SCREEN_WIDTH
	add hl, de
	pop de
	dec b
	jr nz, .row
	ret
.done
	pop bc
	pop hl
	ret

MoveInfoSpecificDescriptions:
	db DRAGON_RAGE, SPECIAL_DAMAGE_EFFECT
	dw MoveInfoSpecific_DRAGON_RAGE
	db SONICBOOM, SPECIAL_DAMAGE_EFFECT
	dw MoveInfoSpecific_SONICBOOM
	db SEISMIC_TOSS, SPECIAL_DAMAGE_EFFECT
	dw MoveInfoSpecific_SEISMIC_TOSS
	db NIGHT_SHADE, SPECIAL_DAMAGE_EFFECT
	dw MoveInfoSpecific_NIGHT_SHADE
	db PSYWAVE, SPECIAL_DAMAGE_EFFECT
	dw MoveInfoSpecific_PSYWAVE
	db REST, HEAL_EFFECT
	dw MoveInfoSpecific_REST
	db TOXIC, POISON_EFFECT
	dw MoveInfoSpecific_TOXIC
	db COUNTER, NO_ADDITIONAL_EFFECT
	dw MoveInfoSpecific_COUNTER
	db STRUGGLE, RECOIL_EFFECT
	dw MoveInfoSpecific_STRUGGLE
	db 0

MoveInfoDescriptions:
	table_width 2
	dw MoveInfoEffect_NO_ADDITIONAL_EFFECT
	dw MoveInfoUnknownEffect
	dw MoveInfoEffect_POISON_SIDE_EFFECT1
	dw MoveInfoEffect_DRAIN_HP_EFFECT
	dw MoveInfoEffect_BURN_SIDE_EFFECT1
	dw MoveInfoEffect_FREEZE_SIDE_EFFECT1
	dw MoveInfoEffect_PARALYZE_SIDE_EFFECT1
	dw MoveInfoEffect_EXPLODE_EFFECT
	dw MoveInfoEffect_DREAM_EATER_EFFECT
	dw MoveInfoEffect_MIRROR_MOVE_EFFECT
	dw MoveInfoEffect_ATTACK_UP1_EFFECT
	dw MoveInfoEffect_DEFENSE_UP1_EFFECT
	dw MoveInfoEffect_SPEED_UP1_EFFECT
	dw MoveInfoEffect_SPECIAL_UP1_EFFECT
	dw MoveInfoEffect_ACCURACY_UP1_EFFECT
	dw MoveInfoEffect_EVASION_UP1_EFFECT
	dw MoveInfoEffect_PAY_DAY_EFFECT
	dw MoveInfoEffect_SWIFT_EFFECT
	dw MoveInfoEffect_ATTACK_DOWN1_EFFECT
	dw MoveInfoEffect_DEFENSE_DOWN1_EFFECT
	dw MoveInfoEffect_SPEED_DOWN1_EFFECT
	dw MoveInfoEffect_SPECIAL_DOWN1_EFFECT
	dw MoveInfoEffect_ACCURACY_DOWN1_EFFECT
	dw MoveInfoEffect_EVASION_DOWN1_EFFECT
	dw MoveInfoEffect_CONVERSION_EFFECT
	dw MoveInfoEffect_HAZE_EFFECT
	dw MoveInfoEffect_BIDE_EFFECT
	dw MoveInfoEffect_THRASH_PETAL_DANCE_EFFECT
	dw MoveInfoEffect_SWITCH_AND_TELEPORT_EFFECT
	dw MoveInfoEffect_TWO_TO_FIVE_ATTACKS_EFFECT
	dw MoveInfoUnknownEffect
	dw MoveInfoEffect_FLINCH_SIDE_EFFECT1
	dw MoveInfoEffect_SLEEP_EFFECT
	dw MoveInfoEffect_POISON_SIDE_EFFECT2
	dw MoveInfoEffect_BURN_SIDE_EFFECT2
	dw MoveInfoEffect_FREEZE_SIDE_EFFECT2
	dw MoveInfoEffect_PARALYZE_SIDE_EFFECT2
	dw MoveInfoEffect_FLINCH_SIDE_EFFECT2
	dw MoveInfoEffect_OHKO_EFFECT
	dw MoveInfoEffect_CHARGE_EFFECT
	dw MoveInfoEffect_SUPER_FANG_EFFECT
	dw MoveInfoEffect_SPECIAL_DAMAGE_EFFECT
	dw MoveInfoEffect_TRAPPING_EFFECT
	dw MoveInfoEffect_FLY_EFFECT
	dw MoveInfoEffect_ATTACK_TWICE_EFFECT
	dw MoveInfoEffect_JUMP_KICK_EFFECT
	dw MoveInfoEffect_MIST_EFFECT
	dw MoveInfoEffect_FOCUS_ENERGY_EFFECT
	dw MoveInfoEffect_RECOIL_EFFECT
	dw MoveInfoEffect_CONFUSION_EFFECT
	dw MoveInfoEffect_ATTACK_UP2_EFFECT
	dw MoveInfoEffect_DEFENSE_UP2_EFFECT
	dw MoveInfoEffect_SPEED_UP2_EFFECT
	dw MoveInfoEffect_SPECIAL_UP2_EFFECT
	dw MoveInfoEffect_ACCURACY_UP2_EFFECT
	dw MoveInfoEffect_EVASION_UP2_EFFECT
	dw MoveInfoEffect_HEAL_EFFECT
	dw MoveInfoEffect_TRANSFORM_EFFECT
	dw MoveInfoEffect_ATTACK_DOWN2_EFFECT
	dw MoveInfoEffect_DEFENSE_DOWN2_EFFECT
	dw MoveInfoEffect_SPEED_DOWN2_EFFECT
	dw MoveInfoEffect_SPECIAL_DOWN2_EFFECT
	dw MoveInfoEffect_ACCURACY_DOWN2_EFFECT
	dw MoveInfoEffect_EVASION_DOWN2_EFFECT
	dw MoveInfoEffect_LIGHT_SCREEN_EFFECT
	dw MoveInfoEffect_REFLECT_EFFECT
	dw MoveInfoEffect_POISON_EFFECT
	dw MoveInfoEffect_PARALYZE_EFFECT
	dw MoveInfoEffect_ATTACK_DOWN_SIDE_EFFECT
	dw MoveInfoEffect_DEFENSE_DOWN_SIDE_EFFECT
	dw MoveInfoEffect_SPEED_DOWN_SIDE_EFFECT
	dw MoveInfoEffect_SPECIAL_DOWN_SIDE_EFFECT
	dw MoveInfoUnknownEffect
	dw MoveInfoUnknownEffect
	dw MoveInfoUnknownEffect
	dw MoveInfoUnknownEffect
	dw MoveInfoEffect_CONFUSION_SIDE_EFFECT
	dw MoveInfoEffect_TWINEEDLE_EFFECT
	dw MoveInfoUnknownEffect
	dw MoveInfoEffect_SUBSTITUTE_EFFECT
	dw MoveInfoEffect_HYPER_BEAM_EFFECT
	dw MoveInfoEffect_RAGE_EFFECT
	dw MoveInfoEffect_MIMIC_EFFECT
	dw MoveInfoEffect_METRONOME_EFFECT
	dw MoveInfoEffect_LEECH_SEED_EFFECT
	dw MoveInfoEffect_SPLASH_EFFECT
	dw MoveInfoEffect_DISABLE_EFFECT
	assert_table_length NUM_MOVE_EFFECTS + 1

MoveInfoUnknownEffect:
	db "No effect notes.@", 0
MoveInfoEffect_NO_ADDITIONAL_EFFECT:
	db "Deals damage.@", 0
MoveInfoEffect_POISON_SIDE_EFFECT1:
	db "May poison.@", 0
MoveInfoEffect_DRAIN_HP_EFFECT:
	db "Heals the user for@", "half its damage.@", 0
MoveInfoEffect_BURN_SIDE_EFFECT1:
	db "May burn.@", 0
MoveInfoEffect_FREEZE_SIDE_EFFECT1:
	db "May freeze.@", 0
MoveInfoEffect_PARALYZE_SIDE_EFFECT1:
	db "May paralyze.@", 0
MoveInfoEffect_EXPLODE_EFFECT:
	db "User faints. Uses@", "half the target@", "DEF.@", 0
MoveInfoEffect_DREAM_EATER_EFFECT:
	db "Hits a sleeping@", "foe. Heals the@", "user.@", 0
MoveInfoEffect_MIRROR_MOVE_EFFECT:
	db "Uses the last move@", "used by the foe.@", 0
MoveInfoEffect_PAY_DAY_EFFECT:
	db "Scatters money@", "you collect on@", "win.@", 0
MoveInfoEffect_SWIFT_EFFECT:
	db "Skips the usual@", "hit check.@", 0
MoveInfoEffect_CONVERSION_EFFECT:
	db "Copies the foe's@", "current types.@", 0
MoveInfoEffect_HAZE_EFFECT:
	db "Clears stat stages@", "and other effects.@", 0
MoveInfoEffect_BIDE_EFFECT:
	db "Stores damage.@", "Hits@", "back for double.@", 0
MoveInfoEffect_THRASH_PETAL_DANCE_EFFECT:
	db "Repeats the@", "attack, then@", "confuses user.@", 0
MoveInfoEffect_SWITCH_AND_TELEPORT_EFFECT:
	db "User flees from a@", "wild battle.@", 0
MoveInfoEffect_TWO_TO_FIVE_ATTACKS_EFFECT:
	db "Hits 2 to 5 times.@", 0
MoveInfoEffect_FLINCH_SIDE_EFFECT1:
	db "May make the foe@", "flinch.@", 0
MoveInfoEffect_SLEEP_EFFECT:
	db "Makes the foe@", "fall asleep.@", 0
MoveInfoEffect_POISON_SIDE_EFFECT2:
	db "May poison.@", 0
MoveInfoEffect_BURN_SIDE_EFFECT2:
	db "May burn.@", 0
MoveInfoEffect_FREEZE_SIDE_EFFECT2:
	db "May freeze.@", 0
MoveInfoEffect_PARALYZE_SIDE_EFFECT2:
	db "May paralyze.@", 0
MoveInfoEffect_FLINCH_SIDE_EFFECT2:
	db "May make the foe@", "flinch.@", 0
MoveInfoEffect_OHKO_EFFECT:
	db "Knocks out the foe@", "on a hit. Fails if@", "the foe is faster.@", 0
MoveInfoEffect_CHARGE_EFFECT:
	db "Charges on turn 1.@", "Attacks on turn 2.@", 0
MoveInfoEffect_SUPER_FANG_EFFECT:
	db "Takes half the@", "foe's remaining@", "HP.@", 0
MoveInfoEffect_SPECIAL_DAMAGE_EFFECT:
	db "Uses fixed or@", "variable damage.@", 0
MoveInfoEffect_TRAPPING_EFFECT:
	db "Traps the foe for@", "several turns.@", 0
MoveInfoEffect_FLY_EFFECT:
	db "User hides for one@", "turn, then@", "strikes.@", 0
MoveInfoEffect_ATTACK_TWICE_EFFECT:
	db "Hits twice.@", 0
MoveInfoEffect_JUMP_KICK_EFFECT:
	db "Missing causes@", "crash damage.@", 0
MoveInfoEffect_MIST_EFFECT:
	db "Shields the user@", "from stat drops.@", 0
MoveInfoEffect_FOCUS_ENERGY_EFFECT:
	IF DEF(POKERGB_FOCUS_ENERGY_FIXED)
		db "Raises the user's@", "critical hit rate.@", 0
	ELSE
	db "Lowers the user's@", "critical hit rate.@", 0
	ENDC
MoveInfoEffect_RECOIL_EFFECT:
	db "User loses 1/4 of@", "the damage dealt,@", "at least 1 HP.@", 0
MoveInfoEffect_CONFUSION_EFFECT:
	db "Confuses the foe.@", 0
MoveInfoEffect_HEAL_EFFECT:
	db "Restores up to@", "half@", "the user's max HP.@", 0
MoveInfoEffect_TRANSFORM_EFFECT:
	db "Copies the foe's@", "form and moves.@", 0
MoveInfoEffect_LIGHT_SCREEN_EFFECT:
	db "Raises effective@", "Special defense.@", 0
MoveInfoEffect_REFLECT_EFFECT:
	db "Doubles physical@", "Defense. Critical@", "hits ignore it.@", 0
MoveInfoEffect_POISON_EFFECT:
	db "Poisons the foe.@", 0
MoveInfoEffect_PARALYZE_EFFECT:
	db "Paralyzes the foe.@", 0
MoveInfoEffect_CONFUSION_SIDE_EFFECT:
	db "May confuse.@", 0
MoveInfoEffect_TWINEEDLE_EFFECT:
	db "Hits twice.@", "May poison.@", 0
MoveInfoEffect_SUBSTITUTE_EFFECT:
	db "Uses 1/4 of max HP@", "to make a decoy@", "that takes hits.@", 0
MoveInfoEffect_HYPER_BEAM_EFFECT:
	db "Rest a turn after@", "a hit. Skip on KO@", "or a broken decoy.@", 0
MoveInfoEffect_RAGE_EFFECT:
	db "Locks in the move.@", "Hits raise Attack.@", 0
MoveInfoEffect_MIMIC_EFFECT:
	db "Copies one of the@", "foe's moves.@", 0
MoveInfoEffect_METRONOME_EFFECT:
	db "Calls a random@", "move.@", 0
MoveInfoEffect_LEECH_SEED_EFFECT:
	db "Drains HP each@", "turn and heals the@", "user.@", 0
MoveInfoEffect_SPLASH_EFFECT:
	db "Has no effect.@", 0
MoveInfoEffect_DISABLE_EFFECT:
	db "Temporarily blocks@", "a move.@", 0
MoveInfoEffect_ATTACK_UP1_EFFECT:
	db "Raises Attack@", "by 1 stage.@", 0
MoveInfoEffect_ATTACK_DOWN1_EFFECT:
	db "Lowers foe's@", "Attack 1 stage.@", 0
MoveInfoEffect_ATTACK_UP2_EFFECT:
	db "Raises Attack@", "by 2 stages.@", 0
MoveInfoEffect_ATTACK_DOWN2_EFFECT:
	db "Lowers foe's@", "Attack 2 stages.@", 0
MoveInfoEffect_ATTACK_DOWN_SIDE_EFFECT:
	db "May lower foe's@", "Attack.@", 0
MoveInfoEffect_DEFENSE_UP1_EFFECT:
	db "Raises Defense@", "by 1 stage.@", 0
MoveInfoEffect_DEFENSE_DOWN1_EFFECT:
	db "Lowers foe's@", "Defense 1 stage.@", 0
MoveInfoEffect_DEFENSE_UP2_EFFECT:
	db "Raises Defense@", "by 2 stages.@", 0
MoveInfoEffect_DEFENSE_DOWN2_EFFECT:
	db "Lowers foe's@", "Defense 2 stages.@", 0
MoveInfoEffect_DEFENSE_DOWN_SIDE_EFFECT:
	db "May lower foe's@", "Defense.@", 0
MoveInfoEffect_SPEED_UP1_EFFECT:
	db "Raises Speed@", "by 1 stage.@", 0
MoveInfoEffect_SPEED_DOWN1_EFFECT:
	db "Lowers foe's@", "Speed 1 stage.@", 0
MoveInfoEffect_SPEED_UP2_EFFECT:
	db "Raises Speed@", "by 2 stages.@", 0
MoveInfoEffect_SPEED_DOWN2_EFFECT:
	db "Lowers foe's@", "Speed 2 stages.@", 0
MoveInfoEffect_SPEED_DOWN_SIDE_EFFECT:
	db "May lower foe's@", "Speed.@", 0
MoveInfoEffect_SPECIAL_UP1_EFFECT:
	db "Raises Special@", "by 1 stage.@", 0
MoveInfoEffect_SPECIAL_DOWN1_EFFECT:
	db "Lowers foe's@", "Special 1 stage.@", 0
MoveInfoEffect_SPECIAL_UP2_EFFECT:
	db "Raises Special@", "by 2 stages.@", 0
MoveInfoEffect_SPECIAL_DOWN2_EFFECT:
	db "Lowers foe's@", "Special 2 stages.@", 0
MoveInfoEffect_SPECIAL_DOWN_SIDE_EFFECT:
	db "May lower foe's@", "Special.@", 0
MoveInfoEffect_ACCURACY_UP1_EFFECT:
	db "Raises Accuracy@", "by 1 stage.@", 0
MoveInfoEffect_ACCURACY_DOWN1_EFFECT:
	db "Lowers foe's@", "Accuracy 1 stage.@", 0
MoveInfoEffect_ACCURACY_UP2_EFFECT:
	db "Raises Accuracy@", "by 2 stages.@", 0
MoveInfoEffect_ACCURACY_DOWN2_EFFECT:
	db "Lowers foe's@", "Accuracy 2 stages.@", 0
MoveInfoEffect_EVASION_UP1_EFFECT:
	db "Raises Evasion@", "by 1 stage.@", 0
MoveInfoEffect_EVASION_DOWN1_EFFECT:
	db "Lowers foe's@", "Evasion 1 stage.@", 0
MoveInfoEffect_EVASION_UP2_EFFECT:
	db "Raises Evasion@", "by 2 stages.@", 0
MoveInfoEffect_EVASION_DOWN2_EFFECT:
	db "Lowers foe's@", "Evasion 2 stages.@", 0
MoveInfoSpecific_DRAGON_RAGE:
	db "Deals 40 damage@", "when it hits.@", 0
MoveInfoSpecific_SONICBOOM:
	db "Deals 20 damage@", "when it hits.@", 0
MoveInfoSpecific_SEISMIC_TOSS:
	db "Damage equals the@", "user's level.@", 0
MoveInfoSpecific_NIGHT_SHADE:
	db "Damage equals the@", "user's level.@", 0
MoveInfoSpecific_PSYWAVE:
	db "Random damage@", "based on the@", "user's level.@", 0
MoveInfoSpecific_REST:
	db "Fully heals the@", "user, then sleeps.@", 0
MoveInfoSpecific_TOXIC:
	db "Inflicts poison@", "that gets worse.@", 0
MoveInfoSpecific_COUNTER:
	db "Returns double@", "Normal or Fighting@", "physical damage.@", 0

MoveInfoSpecific_STRUGGLE:
	db "User loses half of@", "the damage dealt,@", "at least 1 HP.@", 0

MoveInfoHighCritical:
	db "High chance of a@", "critical hit.@", 0
MoveInfoPriority:
	db "Goes before most@", "other attacks.@", 0
MoveInfoBothTraits:
	db "Goes before most@", "attacks. High@", "critical-hit odds.@", 0
