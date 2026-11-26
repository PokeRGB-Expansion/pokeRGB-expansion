FuchsiaMoveDeletersHouse_Object:
	db $a ; border block

	def_warp_events
	warp_event 2, 7, LAST_MAP, 10
	warp_event 3, 7, LAST_MAP, 10

	def_bg_events

	def_object_events
	object_event 5, 5, SPRITE_GAMBLER, STAY, DOWN, TEXT_FUCHSIAMOVEDELETERSHOUSE_DELETER

	def_warps_to FUCHSIA_MOVE_DELETERS_HOUSE
