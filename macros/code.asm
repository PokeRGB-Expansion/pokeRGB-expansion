; Syntactic sugar macros

MACRO? lb ; r, hi, lo
	ld \1, ((\2) & $ff) << 8 + ((\3) & $ff)
ENDM

MACRO? ldpal
	ld \1, \2 << 6 | \3 << 4 | \4 << 2 | \5
ENDM

; Design patterns

MACRO ld_hli_a_string
	FOR n, CHARLEN(\1) - 1
		ld a, CHARVAL(STRCHAR(\1, n))
		ld [hli], a
	ENDR
	ld [hl], CHARVAL(STRCHAR(\1, CHARLEN(\1) - 1))
ENDM

MACRO dict
	IF \1 == 0
		and a
	ELSE
		cp \1
	ENDC
	jp z, \2
ENDM

; Each ROM bank reads its own variable-length name table.
MACRO read_info_name
	ld a, [wMoveInfoMove]
	ld hl, \1
	dec a
	ld b, a
	jr z, .copy
.skipName
	ld a, [hli]
	cp '@'
	jr nz, .skipName
	dec b
	jr nz, .skipName
.copy
	ld de, wMoveInfoName
	ld c, MOVE_NAME_LENGTH - 1
.copyLetter
	ld a, [hli]
	ld [de], a
	inc de
	cp '@'
	ret z
	dec c
	jr nz, .copyLetter
	ld a, '@'
	ld [de], a
	ret
ENDM
