SECTION "Sprite Buffers", SRAM

UNION
sSpriteBuffer0:: ds SPRITEBUFFERSIZE
sSpriteBuffer1:: ds SPRITEBUFFERSIZE
sSpriteBuffer2:: ds SPRITEBUFFERSIZE
NEXTU
; No sprite is decompressed during TM inspection. These three presentation
; buffers are outside the Hall of Fame, saved adventure, and stored boxes.
sMoveInfoScreen:: ; learning INFO borrows only this tilemap
sTMPreviewScreen:: ds SCREEN_AREA
sTMPreviewOAM:: ds OAM_COUNT * OBJ_SIZE
sTMPreviewIconTiles:: ds ((ICON_QUADRUPED + 1) * 4) tiles
	ASSERT @ - sTMPreviewScreen <= 3 * SPRITEBUFFERSIZE
ENDU

	ds $100

sHallOfFame:: ds HOF_TEAM * HOF_TEAM_CAPACITY


SECTION "Save Data", SRAM

	ds $598

sGameData::
sPlayerName::  ds NAME_LENGTH
sMainData::    ds wMainDataEnd - wMainDataStart
sSpriteData::  ds wSpriteDataEnd - wSpriteDataStart
sPartyData::   ds wPartyDataEnd - wPartyDataStart
sCurBoxData::  ds wBoxDataEnd - wBoxDataStart
sTileAnimations:: db
sGameDataEnd::
sMainDataCheckSum:: db

; Sidecar in previously unused SRAM. Keep the stock payload and checksum offsets.
sSaveTransactionTag:: ds 8
sSaveTransactionState:: db


; The PC boxes will not fit into one SRAM bank,
; so they use multiple SECTIONs
DEF box_n = 0
MACRO boxes
	REPT \1
		DEF box_n += 1
	sBox{d:box_n}:: ds wBoxDataEnd - wBoxDataStart
	ENDR
ENDM

SECTION "Saved Boxes 1", SRAM

; sBox1 - sBox6
	boxes 6
sBank2AllBoxesChecksum:: db
sBank2IndividualBoxChecksums:: ds 6

SECTION "Saved Boxes 2", SRAM

; sBox7 - sBox12
	boxes 6
sBank3AllBoxesChecksum:: db
sBank3IndividualBoxChecksums:: ds 6

; All 12 boxes fit within 2 SRAM banks
	ASSERT box_n == NUM_BOXES, \
		"boxes: Expected {d:NUM_BOXES} total boxes, got {d:box_n}"

ENDSECTION
