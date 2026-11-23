#!/usr/bin/env python3
"""Check the prize tables and possible cash-only purchases in English Red and Blue."""

import argparse
import hashlib
import json
import re
from pathlib import Path

from check_foundation_tables import linked_offset, read_symbols


MAX_COINS = 9999
LOT_SIZE = 50
LOT_PRICE = 1000
# First balance at which the clerk refuses a sale.
CUTOFFS = {"retail": 9990, "withdrawn_full_lot": 9950}
ROM_HASHES = {
    "red": "ea9bcae617fdf159b045185467ae58b2e4a48b9a",
    "blue": "d7037c83e1ae5b39bde3c30787637ba1d4c48ce2",
}


def next_balance(balance, cutoff):
    if balance >= cutoff:
        return balance
    return min(MAX_COINS, balance + LOT_SIZE)


def final_balances(cutoff):
    """Follow repeated purchases until the first refusal, from every balance."""
    results = list(range(MAX_COINS + 1))
    for balance in reversed(range(cutoff)):
        results[balance] = results[next_balance(balance, cutoff)]
    return results


def buy_from_zero(price, cutoff):
    balance = purchases = 0
    while balance < price:
        after = next_balance(balance, cutoff)
        if after == balance:
            break
        balance = after
        purchases += 1
    return {
        "purchases": purchases,
        "money_spent": purchases * LOT_PRICE,
        "balance_at_prize_counter": balance,
        "coins_after_redemption": balance - price if balance >= price else None,
    }


def name_lookup(checkout, filename, declaration):
    contents = (checkout / "constants" / filename).read_text()
    pattern = rf"^\s*{declaration}\s+(\w+)\s*;\s*\$([A-Fa-f0-9]+)\b"
    return {int(code, 16): name for name, code in re.findall(pattern, contents, re.M)}


def prize_rows(checkout, color, finals):
    stem = checkout / f"poke{color}"
    rom = stem.with_suffix(".gbc").read_bytes()
    if hashlib.sha1(rom).hexdigest() != ROM_HASHES[color]:
        raise ValueError(f"Expected the stock English {color} ROM.")
    symbols = read_symbols(stem.with_suffix(".sym"))
    species = name_lookup(checkout, "pokemon_constants.asm", "const")
    machines = name_lookup(checkout, "item_constants.asm", "add_tm")
    rows = []
    for group in ("Mon1", "Mon2", "TMs"):
        ids = linked_offset(symbols[f"PrizeMenu{group}Entries"])
        costs = linked_offset(symbols[f"PrizeMenu{group}Cost"])
        if (rom[ids + 3], rom[costs + 6]) != (0x50, 0x50):
            raise ValueError(f"Unexpected end of the {color} {group} table.")
        for index in range(3):
            key = rom[ids + index]
            name = "TM_" + machines[key] if group == "TMs" else species[key]
            start = costs + 2 * index
            price = int(rom[start:start + 2].hex(), 10)
            rows.append({
                "window": group,
                "row": index + 1,
                "entry": name,
                "entry_id": key,
                "price": price,
                "starting_balances_that_can_afford": {
                    policy: sum(value >= price for value in balances)
                    for policy, balances in finals.items()
                },
                "route_from_zero": {
                    policy: buy_from_zero(price, cutoff)
                    for policy, cutoff in CUTOFFS.items()
                },
            })
    return rows


def measure(checkout):
    finals = {policy: final_balances(cutoff) for policy, cutoff in CUTOFFS.items()}
    totals = {"both": 0, "retail_only": 0, "withdrawn_only": 0, "neither": 0}
    changes = []
    for balance, (retail, withdrawn) in enumerate(zip(*finals.values())):
        outcome = {
            (True, True): "both", (True, False): "retail_only",
            (False, True): "withdrawn_only", (False, False): "neither",
        }[(retail == MAX_COINS, withdrawn == MAX_COINS)]
        totals[outcome] += 1
        if next_balance(balance, CUTOFFS["retail"]) != next_balance(balance, CUTOFFS["withdrawn_full_lot"]):
            changes.append(balance)
    if changes != list(range(9950, 9990)):
        raise ValueError("Unexpected range of changed single purchases.")
    return {
        "balance_model": {
            "valid_initial_balances": MAX_COINS + 1,
            "lot_size": LOT_SIZE,
            "lot_price": LOT_PRICE,
            "first_refusal": CUTOFFS,
            "changed_single_purchase": {"first": changes[0], "last": changes[-1], "count": len(changes)},
            "can_reach_or_already_hold_9999": {
                policy: balances.count(MAX_COINS) for policy, balances in finals.items()
            },
            "can_reach_or_already_hold_9999_comparison": totals,
        },
        "prize_tables": {color: prize_rows(checkout, color, finals) for color in ROM_HASHES},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path, help="Built stock pokered checkout with both .gbc and .sym files")
    parser.add_argument("--print", action="store_true", dest="print_json", help="Print the linked rows and model as JSON")
    args = parser.parse_args()
    result = measure(args.checkout)
    if args.print_json:
        print(json.dumps(result, indent=2))
        return
    path = Path(__file__).resolve().parents[1] / "research/game-corner-route-checks.json"
    saved = json.loads(path.read_text())
    for key, value in result.items():
        if saved[key] != value:
            raise SystemExit(f"The {key} results differ from {path.name}.")
    print("Verified 18 prize rows and both purchase rules at all 10,000 starting balances.")


if __name__ == "__main__":
    main()
