VendingMachineMenu::
	ld hl, VendingMachineText1
	call PrintText
	ld a, MONEY_BOX
	ld [wTextBoxID], a
	call DisplayTextBoxID
	xor a
	ld [wCurrentMenuItem], a
	ld [wLastMenuItem], a
	ld a, PAD_A | PAD_B | PAD_START
	ld [wMenuWatchedKeys], a
	ld a, 3
	ld [wMaxMenuItem], a
	ld a, 5
	ld [wTopMenuItemY], a
	ld a, 1
	ld [wTopMenuItemX], a
	ld hl, wStatusFlags5
	set BIT_NO_TEXT_DELAY, [hl]
	hlcoord 0, 3
	ld b, 8
	ld c, 12
	call TextBoxBorder
	call UpdateSprites
	call DrawVendingOffers
	ld hl, wStatusFlags5
	res BIT_NO_TEXT_DELAY, [hl]
.input
	farcall HandleVendingInfoInput
	ld a, [wMoveInfoNumber]
	bit B_PAD_B, a
	jr nz, .notThirsty
	bit B_PAD_START, a
	jr z, .choose
	ld a, [wCurrentMenuItem]
	cp 3
	jr nc, .input
	call LoadVendingMachineItem
	farcall InspectVendingDrink
	jr .input
.choose
	ld a, [wCurrentMenuItem]
	cp 3 ; chose Cancel?
	jr z, .notThirsty
IF DEF(_POKERGB_CORE)
	call LoadVendingMachineItem
; Check the same selected price that will be deducted after delivery.
	ld hl, hVendingMachinePrice
	ld de, wPlayerMoney
	ld c, 3
	call StringCmp
ELSE
	xor a
	ldh [hMoney], a
	ldh [hMoney + 2], a
	ld a, $2
	ldh [hMoney + 1], a
	call HasEnoughMoney
ENDC
	jr nc, .enoughMoney
	ld hl, VendingMachineText4
	jp PrintText
.enoughMoney
IF !DEF(_POKERGB_CORE)
	call LoadVendingMachineItem
ENDC
	ldh a, [hVendingMachineItem]
	ld b, a
	ld c, 1
	call GiveItem
	jr nc, .BagFull

	ld b, 60 ; number of times to play the "brrrrr" sound
.playDeliverySound
	ld c, 2
	call DelayFrames
	push bc
	ld a, SFX_PUSH_BOULDER
	call PlaySound
	pop bc
	dec b
	jr nz, .playDeliverySound

	ld hl, VendingMachineText5
	call PrintText
	ld hl, hVendingMachinePrice + 2
	ld de, wPlayerMoney + 2
	ld c, $3
	predef SubBCDPredef
	ld a, MONEY_BOX
	ld [wTextBoxID], a
	jp DisplayTextBoxID
.BagFull
	ld hl, VendingMachineText6
	jp PrintText
.notThirsty
	ld hl, VendingMachineText7
	jp PrintText

VendingMachineText1:
	text_far _VendingMachineText1
	text_end

DrawVendingOffers:
	ld hl, VendingPrices
	decoord 2, 5
	ld c, (VendingPrices.end - VendingPrices) / 4
.row
	ld a, [hli]
	ld [wMoveInfoMove], a
	push bc
	push hl ; price
	push de ; name position
	farcall ReadSupplyInfoName
	pop hl
	push hl
	ld de, wMoveInfoName
	call PlaceString
	pop hl
	ld bc, SCREEN_WIDTH + 4
	add hl, bc ; right-align the price at column 12
	pop de
	push hl
	ld c, MONEY_SIGN | LEADING_ZEROES | 3
	call PrintBCDNumber
	pop hl
	ld bc, SCREEN_WIDTH - 4
	add hl, bc ; the next name
	pop bc
	dec c
	jr z, .cancel
	; PrintBCDNumber advanced DE to the next offer.
	push de
	ld d, h
	ld e, l
	pop hl
	jr .row
.cancel
	ld de, .cancelText
	jp PlaceString
.cancelText db "CANCEL@"

VendingMachineText4:
	text_far _VendingMachineText4
	text_end

VendingMachineText5:
	text_far _VendingMachineText5
	text_end

VendingMachineText6:
	text_far _VendingMachineText6
	text_end

VendingMachineText7:
	text_far _VendingMachineText7
	text_end

LoadVendingMachineItem:
	ld hl, VendingPrices
	ld a, [wCurrentMenuItem]
	add a
	add a
	ld d, 0
	ld e, a
	add hl, de
	ld a, [hli]
	ldh [hVendingMachineItem], a
	ld a, [hli]
	ldh [hVendingMachinePrice], a
	ld a, [hli]
	ldh [hVendingMachinePrice + 1], a
	ld a, [hl]
	ldh [hVendingMachinePrice + 2], a
	ret

INCLUDE "data/items/vending_prices.asm"
