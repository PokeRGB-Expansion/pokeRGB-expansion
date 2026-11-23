#!/usr/bin/env python3
"""Generate source-derived critical thresholds; this is not a ROM test runner."""

import csv
from pathlib import Path


def vanilla(speed, high, pumped):
    half = speed // 2
    value = half // 2 if pumped else 2 * half
    return min(4 * value, 255) if high else value // 2


def solus(speed, high, pumped):
    half = speed // 2
    value = 2 * half if pumped else half // 2
    return min(4 * value, 255) if high else value // 2


def proposed(speed, high, pumped):
    value = min(8 * (speed // 2), 255) if high else speed // 2
    return min(4 * value, 255) if pumped else value


def rotate_three(value):
    return ((value << 3) | (value >> 5)) & 255


def main():
    output = Path(__file__).resolve().parents[1] / "research/critical-hit-thresholds.csv"
    rows = []
    differences = 0
    rotated = [rotate_three(byte) for byte in range(256)]
    if sorted(rotated) != list(range(256)):
        raise AssertionError("The byte rotation must preserve the full byte set.")
    for speed in range(256):
        for high in (False, True):
            for pumped in (False, True):
                original = vanilla(speed, high, pumped)
                donor = solus(speed, high, pumped)
                correction = proposed(speed, high, pumped)
                if not pumped:
                    if correction != original:
                        raise AssertionError("The Core rule changed an unpumped threshold.")
                    differences += donor != original
                for threshold in (original, donor, correction):
                    if not 0 <= threshold <= 255:
                        raise AssertionError("A threshold is outside the byte range.")
                    if sum(byte < threshold for byte in rotated) != threshold:
                        raise AssertionError("The exact comparison count is wrong.")
                rows.append((speed, int(high), int(pumped), original, donor, correction))
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("base_speed", "high_critical", "pumped", "vanilla_threshold",
                         "solus_threshold", "proposed_threshold"))
        writer.writerows(rows)
    print(f"Generated {len(rows)} threshold rows.")
    print(f"Solus differs from vanilla in {differences}/512 unpumped inputs.")
    print("The Core rule preserves all 512 unpumped thresholds in this arithmetic model.")
    print("This result does not verify compiled game code.")


if __name__ == "__main__":
    main()
