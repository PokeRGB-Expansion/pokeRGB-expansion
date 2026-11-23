PRESET ?= core
ifeq (,$(filter $(PRESET),core minimal))
$(error PRESET must be core or minimal)
endif
ifneq ($(words $(PRESET)),1)
$(error Select one PRESET)
endif

.DEFAULT_GOAL := all
output := build/$(PRESET)
red_rom        := $(output)/pokered.gbc
blue_rom       := $(output)/pokeblue.gbc
green_rom      := $(output)/pokegreen.gbc
blue_debug_rom := $(output)/pokeblue_debug.gbc
red_vc_rom     := $(output)/pokered_vc.gbc
blue_vc_rom    := $(output)/pokeblue_vc.gbc

rom_obj := \
	audio.o \
	home.o \
	main.o \
	maps.o \
	ram.o \
	text.o \
	gfx/pics.o \
	gfx/sprites.o \
	gfx/tilesets.o

### Build tools

ifeq (,$(shell command -v sha1sum 2>/dev/null))
SHA1 := shasum
else
SHA1 := sha1sum
endif

RGBDS ?=
RGBASM  ?= $(RGBDS)rgbasm
RGBFIX  ?= $(RGBDS)rgbfix
RGBGFX  ?= $(RGBDS)rgbgfx
RGBLINK ?= $(RGBDS)rgblink

RGBASMFLAGS  ?= -Weverything -Wtruncation=1
RGBLINKFLAGS ?= -Weverything -Wtruncation=1
RGBFIXFLAGS  ?= -Weverything
RGBGFXFLAGS  ?= -Weverything


red_obj        := $(addprefix $(output)/red/,$(rom_obj))
blue_obj       := $(addprefix $(output)/blue/,$(rom_obj))
green_obj      := $(addprefix $(output)/green/,$(rom_obj))
blue_debug_obj := $(addprefix $(output)/blue_debug/,$(rom_obj))
red_vc_obj     := $(addprefix $(output)/red_vc/,$(rom_obj))
blue_vc_obj    := $(addprefix $(output)/blue_vc/,$(rom_obj))

.SUFFIXES:
.PRECIOUS:
.SECONDARY:
.PHONY: all red blue green blue_debug red_vc blue_vc clean tidy compare tools

all: red blue green
red: $(red_rom)
blue: $(blue_rom)
green: $(green_rom)
blue_debug: $(blue_debug_rom)
red_vc: $(output)/pokered.patch
blue_vc: $(output)/pokeblue.patch

clean: tidy
	find gfx \
	     \( -iname '*.1bpp' \
	        -o -iname '*.2bpp' \
	        -o -iname '*.pic' \) \
	     -delete

tidy:
	$(RM) -r $(output)
	$(MAKE) clean -C tools/

# The checksums describe pristine upstream outputs.
compare:
	@test -n "$(BASELINE_DIR)" || { echo "Set BASELINE_DIR to the verified upstream outputs." >&2; exit 1; }
	@cd "$(BASELINE_DIR)" && $(SHA1) -c "$(CURDIR)/roms.sha1"

tools:
	$(MAKE) -C tools/

# Export local labels in the symbol map for debugging and tests.
RGBASMFLAGS += -Q8 -P includes.asm -E
ifeq ($(PRESET),core)
RGBASMFLAGS += -D _POKERGB_CORE
endif

$(output)/rgbdscheck.o: rgbdscheck.asm
	@mkdir -p $(dir $@)
	$(RGBASM) -o $@ $<

$(red_obj):        RGBASMFLAGS += -D _RED
$(blue_obj):       RGBASMFLAGS += -D _BLUE
$(green_obj):      RGBASMFLAGS += -D _BLUE -D _GREEN_VISUALS
$(blue_debug_obj): RGBASMFLAGS += -D _BLUE -D _DEBUG
$(red_vc_obj):     RGBASMFLAGS += -D _RED -D _RED_VC
$(blue_vc_obj):    RGBASMFLAGS += -D _BLUE -D _BLUE_VC

$(output)/%.patch: $(output)/%_vc.gbc $(output)/%.gbc vc/%.patch.template
	tools/make_patch $(output)/$*_vc.sym $^ $@

ifeq (,$(filter clean tidy compare tools,$(MAKECMDGOALS)))

$(info $(shell $(MAKE) -C tools))

preinclude_deps := Makefile includes.asm $(shell tools/scan_includes includes.asm)
define DEP
$1: $2 $$(shell tools/scan_includes $2) $(preinclude_deps) | $(output)/rgbdscheck.o
	@mkdir -p $$(dir $$@)
	$$(RGBASM) $$(RGBASMFLAGS) -o $$@ $$<
endef

define COLOR_DEPS
$(foreach obj,$($(1)_obj),$(eval $(call DEP,$(obj),$(patsubst $(output)/$(1)/%.o,%.asm,$(obj)))))
endef
$(foreach color,red blue green blue_debug red_vc blue_vc,$(call COLOR_DEPS,$(color)))

endif

RGBLINKFLAGS += -d
RGBFIXFLAGS += -jsv -n 0 -k 01 -l 0x33 -m MBC3+RAM+BATTERY -r 03

define CARTRIDGE
$1: $2 layout.link
	$$(RGBLINK) $$(RGBLINKFLAGS) -p $3 -l layout.link -m $$(@:.gbc=.map) -n $$(@:.gbc=.sym) -o $$@ $$(filter %.o,$$^)
	$$(RGBFIX) $$(RGBFIXFLAGS) -p $3 -t "$4" $$@
endef
$(eval $(call CARTRIDGE,$(red_rom),$(red_obj),0x00,POKEMON RED))
$(eval $(call CARTRIDGE,$(blue_rom),$(blue_obj),0x00,POKEMON BLUE))
$(eval $(call CARTRIDGE,$(green_rom),$(green_obj),0x00,POKEMON GREEN))
$(eval $(call CARTRIDGE,$(blue_debug_rom),$(blue_debug_obj),0xff,POKEMON BLUE))
$(eval $(call CARTRIDGE,$(red_vc_rom),$(red_vc_obj),0x00,POKEMON RED))
$(eval $(call CARTRIDGE,$(blue_vc_rom),$(blue_vc_obj),0x00,POKEMON BLUE))


### Misc file-specific graphics rules

gfx/battle/move_anim_0.2bpp: tools/gfx += --trim-whitespace
gfx/battle/move_anim_1.2bpp: tools/gfx += --trim-whitespace

gfx/intro/blue_jigglypuff_1.2bpp: RGBGFXFLAGS += --columns
gfx/intro/blue_jigglypuff_2.2bpp: RGBGFXFLAGS += --columns
gfx/intro/blue_jigglypuff_3.2bpp: RGBGFXFLAGS += --columns
gfx/intro/red_nidorino_1.2bpp: RGBGFXFLAGS += --columns
gfx/intro/red_nidorino_2.2bpp: RGBGFXFLAGS += --columns
gfx/intro/red_nidorino_3.2bpp: RGBGFXFLAGS += --columns
gfx/intro/gengar.2bpp: RGBGFXFLAGS += --columns
gfx/intro/gengar.2bpp: tools/gfx += --remove-duplicates --preserve=0x19,0x76

gfx/credits/the_end.2bpp: tools/gfx += --interleave --png=$<

gfx/slots/red_slots_1.2bpp: tools/gfx += --trim-whitespace
gfx/slots/blue_slots_1.2bpp: tools/gfx += --trim-whitespace

gfx/tilesets/%.2bpp: tools/gfx += --trim-whitespace
gfx/tilesets/reds_house.2bpp: tools/gfx += --preserve=0x48

gfx/trade/game_boy.2bpp: tools/gfx += --remove-duplicates


### Catch-all graphics rules

%.2bpp: %.png
	$(RGBGFX) --colors dmg $(RGBGFXFLAGS) -o $@ $<
	$(if $(tools/gfx),\
		tools/gfx $(tools/gfx) -o $@ $@ || $$($(RM) $@ && false))

%.1bpp: %.png
	$(RGBGFX) --colors dmg $(RGBGFXFLAGS) --depth 1 -o $@ $<
	$(if $(tools/gfx),\
		tools/gfx $(tools/gfx) --depth 1 -o $@ $@ || $$($(RM) $@ && false))

%.pic: %.2bpp
	tools/pkmncompress $< $@


### File extensions that are never generated and should be manually created

%.asm: ;
%.inc: ;
%.png: ;
%.pal: ;
%.bin: ;
%.blk: ;
%.bst: ;
%.rle: ;
