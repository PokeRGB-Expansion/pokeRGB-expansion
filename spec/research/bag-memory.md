# Bag memory allocation

## Accepted design

The optional larger bag uses the separate 134-byte reserve at `$D66A–$D6EF`. Move the live bag there and retain the original 42-byte footprint. Keep all other existing fields and block boundaries at their original addresses, including `wGameProgressFlagsEnd`. Core retains its original allocation when this Extension is disabled. The selected capacity is 64 slots. Four marker bytes, one count byte, 128 entry bytes, and one end marker use all 134 bytes.

Assign the whole reserve to this feature. Declare its address range and build conditions in the project's memory map. Check for overlapping allocations when features are combined. No second Extension may treat the same bytes as free space. Check the disabled layout and each supported combination against their declared layouts. Keeping surrounding addresses fixed reduces feature conflicts. Shared inventory, initialization, and save routines still need combination tests. The block has no unused tail at 64 slots; any later format growth needs a reviewed allocation.

## Verified allocation

At the retained `pret/pokered` revision, the original bag has no free space immediately after it. Its 42 bytes contain one count byte, 20 two-byte entries, and an end marker. Money follows immediately. [E108](evidence.md#e108)

| Address | Original contents |
|---|---|
| `$D31D` | Bag item count |
| `$D31E–$D345` | 20 entries: item ID and quantity |
| `$D346` | End marker |
| `$D347–$D349` | Money |

Increasing only the capacity constant to 21 leaves the bag start fixed but shifts money from `$D347` to `$D349`. Forty and sixty fail the RAM link because later data reaches the fixed stack area. These results do not prevent a separate allocation.

The source also has adjacent reserves of 78 and 56 bytes after `wRoute18Gate1FCurScript`, totaling 134 bytes. Preserve the intervening boundary label through an allocation overlay. With a four-byte format marker, a count byte, and an end marker, the capacity equation is:

```text
4 + 1 + (2 × capacity) + 1 ≤ 134
capacity ≤ 64
```

The RAM-only audit assembles and links 60 and 64 slots in that reserve. Every other existing WRAM label retains its address. The 65-slot case fails the explicit allocation assertion. The selected 64-slot preset uses all 134 bytes including the format marker. Sixty-four is the limit of this allocation and format. RAM allocation evidence does not establish gameplay support or an engine-wide maximum.

The earlier [128-byte tutorial allocation](evidence.md#e107) is a different reserve. Its 63-slot calculation excludes a format marker. It does not describe the selected 134-byte allocation.

## Save and runtime checks

The live bag changes location, so original saves need explicit import or a stated fresh-save boundary. Keeping other offsets fixed makes that work smaller; it does not by itself make the bag formats interchangeable. Keep the original footprint available for supported import or a legacy copy. Define the format marker, import direction, save behavior, and disabled-feature behavior before release.

The original new-game routine initializes the bag before clearing game-progress flags. That later clear covers the first 78 bytes of this reserve. Initialize the enabled bag and its format marker after the clear; otherwise the count and end marker are erased. Retain the original progress boundary and disabled path. [E109](evidence.md#e109)

Audit other access to the former reserves, including bulk clearing and copying, initialization, and game-progress flag ranges. Check insertion, removal, list indexing, save/load, and the feature combinations advertised as supported. The [PN-020 acceptance cases](../docs/13-playthrough-intake.md#pn-020) remain required.

## Repeat the allocation check

Use RGBDS 1.0.0 or newer and a checkout at `af519899719f0754965776faac0e836a3b906e6d`:

```sh
python3 tools/audit_bag_memory.py \
  --source-checkout /path/to/pokered \
  --rgbds-bin /path/to/rgbds/bin \
  --output /tmp/bag-memory-audit.json
```

The tool reads Git objects and works in a temporary directory. It does not edit the source checkout. It links RAM objects, omitting the OAM DMA section defined in a game-code object. Only WRAM addresses are compared. The [recorded result](bag-memory-audit.json) used RGBDS 1.0.4. No ROM gameplay, save import, or optional-feature combination was tested by this audit.
