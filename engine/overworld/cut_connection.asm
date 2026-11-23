LoadConnectedTileBlockMap::
	call FindCutTreeOnRouteConnection
	push de
	push hl
	ld a, [wCurMap]
	call LoadTileBlockMapPreservingBank
	pop hl
	pop de
	ld a, d
	and a
	ret z
	ld a, [hl]
	cp $35 ; the block before cutting
	ret nz
	ld [hl], d
	ret

FindCutTreeOnRouteConnection:
; The screen scrolls without reloading tiles at a route border. Carry the
; cut tree at Route 14 (3, 42) into the new map's block buffer so it agrees
; with the screen. A full map load still restores the tree from ROM.
; Output: D is zero or the cut block ID. HL points to the new block if cut.
	ld d, 0
	ld a, [wCurMap] ; the destination map, with the previous map still in WRAM
	cp ROUTE_14
	jr z, .enteringRoute14
	cp ROUTE_15
	ret nz
	ld a, [wXCoord]
	cp ROUTE_15_WIDTH * 2 - 1 ; entering from the east
	ret nz
	owcoord hl, 1, 21, ROUTE_14_WIDTH
	ld a, [hl]
	owcoord hl, ROUTE_15_WIDTH + 1, 3, ROUTE_15_WIDTH
	jr .checkCutTree

.enteringRoute14
	ld a, [wXCoord]
	and a ; entering from the west
	ret nz
	owcoord hl, ROUTE_15_WIDTH + 1, 3, ROUTE_15_WIDTH
	ld a, [hl]
	owcoord hl, 1, 21, ROUTE_14_WIDTH
.checkCutTree
	cp $4c ; the cut form of block $35
	ret nz
	ld d, a
	ret
