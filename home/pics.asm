; uncompresses the front or back sprite of the specified mon
; assumes the corresponding mon header is already loaded
; hl contains offset to sprite pointer ($b for front or $d for back)
UncompressMonSprite::
	ld bc, wMonHeader
	add hl, bc
	ld a, [hli]
	ld [wSpriteInputPtr], a    ; fetch sprite input pointer
	ld a, [hl]
	ld [wSpriteInputPtr+1], a
; define (by index number) the bank that a pokemon's image is in
; index = MEW:             bank $1
; index = FOSSIL_KABUTOPS: bank $B
;       index < $1F:       bank $9 ("Pics 1")
; $1F ≤ index < $4A:       bank $A ("Pics 2")
; $4A ≤ index < $74:       bank $B ("Pics 3")
; $74 ≤ index < $99:       bank $C ("Pics 4")
; $99 ≤ index:             bank $D ("Pics 5")
	ld a, [wCurPartySpecies]
	ld b, a
	cp MEW
	ld a, BANK(MewPicFront)
	jr z, .GotBank
	ld a, b
	cp FOSSIL_KABUTOPS
	ld a, BANK(FossilKabutopsPic)
	jr z, .GotBank
	ld a, b
	cp TANGELA + 1
	ld a, BANK("Pics 1")
	jr c, .GotBank
	ld a, b
	cp MOLTRES + 1
	ld a, BANK("Pics 2")
	jr c, .GotBank
	ld a, b
	cp BEEDRILL + 2
	ld a, BANK("Pics 3")
	jr c, .GotBank
	ld a, b
	cp STARMIE + 1
	ld a, BANK("Pics 4")
	jr c, .GotBank
	ld a, BANK("Pics 5")
.GotBank
	jp UncompressSpriteData

; de: destination location
LoadMonFrontSprite::
	push de
	ld hl, wMonHFrontSprite - wMonHeader
	call UncompressMonSprite
	ld hl, wMonHSpriteDim
	ld a, [hli]
	ld c, a
	pop de
	; fall through

; de: destination in VRAM, a low: width, c high: height in tiles
LoadUncompressedSpriteData::
	and $f
	ld b, a
	ld a, c
	and $f0
	or b
	ldh [hSpriteWidth], a ; keep both dimensions through the bank switch
	farjp CenterAndLoadSprite

; combines the (7*7 tiles, 1bpp) sprite chunks in buffer 0 and 1 into a 2bpp sprite located in buffer 1 through 2
; in the resulting sprite, the rows of the two source sprites are interlaced
; de: output address
InterlaceMergeSpriteBuffers::
	xor a
	ld [rRAMB], a
	push de
	ld hl, sSpriteBuffer2 + (SPRITEBUFFERSIZE - 1) ; destination: end of buffer 2
	ld de, sSpriteBuffer1 + (SPRITEBUFFERSIZE - 1) ; source 2: end of buffer 1
	ld bc, sSpriteBuffer0 + (SPRITEBUFFERSIZE - 1) ; source 1: end of buffer 0
	ld a, SPRITEBUFFERSIZE / 2
	ldh [hSpriteInterlaceCounter], a
.interlaceLoop
	ld a, [de]
	dec de
	ld [hld], a   ; write byte of source 2
	ld a, [bc]
	dec bc
	ld [hld], a   ; write byte of source 1
	ld a, [de]
	dec de
	ld [hld], a   ; write byte of source 2
	ld a, [bc]
	dec bc
	ld [hld], a   ; write byte of source 1
	ldh a, [hSpriteInterlaceCounter]
	dec a
	ldh [hSpriteInterlaceCounter], a
	jr nz, .interlaceLoop
	ld a, [wSpriteFlipped]
	and a
	jr z, .notFlipped
	ld bc, 2 * SPRITEBUFFERSIZE
	ld hl, sSpriteBuffer1
.swapLoop
	swap [hl]    ; if flipped swap nybbles in all bytes
	inc hl
	dec bc
	ld a, b
	or c
	jr nz, .swapLoop
.notFlipped
	pop hl ; hl = output address
	ld de, sSpriteBuffer1
	ld c, PIC_SIZE ; tiles
	ldh a, [hLoadedROMBank]
	ld b, a
	jp CopyVideoData
