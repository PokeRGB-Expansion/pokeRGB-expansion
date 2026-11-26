_Route15Gate2FOaksAideExpAllText::
	text "EXP.ALL gives"
	line "EXP points to all"
	cont "the #MON with"
	cont "you, even if they"
	cont "don't fight."

	para "It does, however,"
	line "reduce the amount"
	cont "of EXP for each"
	cont "#MON."

IF DEF(_POKERGB_CORE)
	para "Use EXP.ALL in"
	line "your ITEM list to"
	cont "turn it on or off."
ELSE
	para "If you don't need"
	line "it, you should "
	cont "store it via PC."
ENDC
	done

_Route15Gate2FBinocularsText::
	text "Looked into the"
	line "binoculars."

	para "It looks like a"
	line "small island!"
	done
