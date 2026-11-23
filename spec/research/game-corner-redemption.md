# Buying Porygon with cash in Red and Blue

**Minimal and Core keep the original coin sale, including its price, limits, offer and receipt.** From zero coins, Red lets a player buy Porygon without playing slots or saving a hidden pickup. The clerk charges ¥1,000 for the last 49 coins. Requiring room for all 50 removes that route. Green follows Blue’s prices and rules. [Clerk script](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/scripts/GameCorner.asm#L140-L201) · [Prize tables](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/data/events/prizes.asm#L9-L67)

## Where the rules differ

| Coins before purchase | Original Red and Blue | Withdrawn full-lot rule |
|---|---|---|
| 0–9,949 | Pay ¥1,000, receive 50. | Same. |
| 9,950–9,989 | Pay ¥1,000 and fill the case to 9,999. The credit ranges from 49 coins down to 10. | Clerk refuses. The player keeps the money. |
| 9,990–9,999 | Clerk refuses. The player keeps the money. | Same. |

The original clerk updates the visible balance, then gives the fixed 50-coin receipt. At 9,970 the player receives 29. Earlier checks confirmed the mismatch, the refusal boundary, and the outcomes for declining, missing the Coin Case or lacking ¥1,000. Those tests ended at the clerk. The same threshold also controls three one-time NPC gifts. [Clerk dialogue](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/text/GameCorner.asm#L10-L39) · [Threshold and gift calls](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/scripts/GameCorner.asm#L238-L391) · [Earlier single-purchase results](scope-sweep-checks.json)

## What ran in the emulator

Each Porygon purchase run started with a Coin Case, zero coins, two party members and exactly enough money for the original route. Each attempt entered the clerk script immediately after the Yes/No prompt and carried its resulting balances forward. The test then selected Porygon in the prize menu and confirmed the exchange. The original ROMs matched their English retail hashes. [Recorded inputs, hashes and results](game-corner-route-checks.json) · [Delivery and debit](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/events/prize_menu.asm#L200-L251)

| Build | Cash route | Prize result |
|---|---|---|
| Red | Purchase 199 left 9,950 coins and ¥1,000. Purchase 200 reached 9,999. | Level 26 Porygon joined the party. Zero coins remained. |
| Red, withdrawn rule | Purchase 200 was refused at 9,950. | Prize counter refused Porygon. All 9,950 coins and ¥1,000 remained. |
| Blue, both builds | 130 purchases reached 6,500. | Level 18 Porygon joined the party. Zero coins remained. |

Blue’s most expensive prize is TM50 Substitute at 7,700 coins. In separate runs on original Red and Blue, 154 clerk purchases from zero bought exactly 7,700. Confirming TM50 at the third prize window added one copy to the bag and left zero coins. [TM50 purchase and redemption](game-corner-route-checks.json)

In each original color the player kept every coin after declining, trying one coin short, or trying with a full party and full current box. With a full party and space in the current box, it delivered Porygon there and deducted the exact price. [Eight prize checks](game-corner-route-checks.json)

Other coin sources explain why the full-lot rule made Red Porygon harder to obtain without making it unobtainable. On both tested Red builds, collecting the hidden 100 coins at (15, 8) raised 9,950 to 9,999. Revisiting an already collected pile left 9,950 unchanged. Slots can also change the balance by one. For example, losing a one-coin bet at 9,950 would leave room to buy exactly 50. [Four pickup checks](game-corner-route-checks.json) · [Hidden pile](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/data/events/hidden_events.asm#L286-L298) · [Slot bets and payouts](https://github.com/pret/pokered/blob/ba9c0568f64ae602fadda577a08c66639f93082a/engine/slots/slot_machine.asm#L635-L692)

## What the model checked

We read all nine prize entries and prices from each original ROM. Then we checked both purchase rules at every starting balance from 0 to 9,999. The player has a Coin Case, can afford each purchase, and uses the clerk only. A balance already high enough to redeem a prize counts as a success.

Of the 10,000 possible starting balances, original Red can reach or already holds Porygon’s price from **8,200**. The full-lot rule can do so from **200**, all ending in a remainder of 49 when divided by 50. The other 17 prize entries, including all nine in Blue, remain affordable from every starting balance under both rules. These counts describe possible balances, not how often players hold them. Run `python3 tools/check_game_corner_routes.py /path/to/built/pokered` to verify the figures against both ROMs. [Full price and route results](game-corner-route-checks.json) · [Verification tool](../tools/check_game_corner_routes.py)

Yellow also prices Porygon at 9,999. FireRed and LeafGreen keep the respective prices of 9,999 and 6,500, but their clerk insists on room for a full purchase of 50 or 500 coins. Copying that rule changes an original Red strategy. [Yellow prizes](https://github.com/pret/pokeyellow/blob/e89ead154b9968aa50eed9328ff2b38b6c194382/data/events/prizes.asm#L18-L28) · [Remake prices](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/CeladonCity_GameCorner_PrizeRoom/scripts.inc#L93-L111) · [Remake clerk](https://github.com/pret/pokefirered/blob/037335f4c725d7c9aecdac87066f2002b4bd7e14/data/maps/CeladonCity_GameCorner/scripts.inc#L44-L68)
