Version_GFX:
IF DEF(_RED) || DEF(_GREEN_VISUALS)
	INCBIN "gfx/title/red_version.1bpp" ; contains both Red and Green lettering
ELIF DEF(_BLUE)
	INCBIN "gfx/title/blue_version.1bpp" ; 8 tiles
ENDC
Version_GFXEnd:
