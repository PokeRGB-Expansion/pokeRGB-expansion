; The two EXP tiles and nine fill patterns occupy blank English font slots.
; One-bit graphics keep the rail readable under all three HP palettes.
	db %00000000, %00111010, %00100010, %00110001
	db %00100010, %00111010, %00000000, %00000000
	db %00000000, %10110000, %10101000, %00110000
	db %10100000, %10100000, %00000000, %00000000

	FOR filled, 0, TILE_WIDTH + 1
		DEF fill_mask = ($ff << (TILE_WIDTH - filled)) & $ff
		db 0, 0, 0, fill_mask | %10101010, fill_mask, 0, 0, 0
	ENDR
	PURGE fill_mask
