"""Test two Game Boys connected through SameBoy's serial bit callbacks."""

import argparse
import ctypes as C
from pathlib import Path

from cartridge_smoke import Game


RIGHT, LEFT, UP, DOWN, A, B = range(6)
SELECT, START = 6, 7
VIRIDIAN_POKECENTER = 0x29
TRADE_CENTER, COLOSSEUM = 0xEF, 0xF0
INTERNAL_CLOCK, EXTERNAL_CLOCK = 2, 1
DMG_CYCLES_PER_FRAME = 2 * 456 * 154
SERIAL_START = C.CFUNCTYPE(None, C.c_void_p, C.c_bool)
SERIAL_END = C.CFUNCTYPE(C.c_bool, C.c_void_p)


class Cable:
    def __init__(self, left, right):
        self.players = (left, right)
        self.core = left.core
        self.peers = {left.gb: right.gb, right.gb: left.gb}
        self.outgoing = dict.fromkeys(self.peers, False)
        self.bits = dict.fromkeys(self.peers, 0)
        self.offset = 0
        signatures = {
            "set_serial_transfer_bit_start_callback": (None, SERIAL_START),
            "set_serial_transfer_bit_end_callback": (None, SERIAL_END),
            "serial_get_data_bit": (C.c_bool,),
            "serial_set_data_bit": (None, C.c_bool),
            "disconnect_serial": (None,),
        }
        for name, (result, *arguments) in signatures.items():
            function = getattr(self.core, "GB_" + name)
            function.restype = result
            function.argtypes = [C.c_void_p, *arguments]
        self.serial_start = SERIAL_START(self.send)
        self.serial_end = SERIAL_END(self.exchange)

    def __enter__(self):
        for game in self.players:
            self.core.GB_set_serial_transfer_bit_start_callback(game.gb, self.serial_start)
            self.core.GB_set_serial_transfer_bit_end_callback(game.gb, self.serial_end)
        return self

    def __exit__(self, *args):
        for game in self.players:
            self.core.GB_disconnect_serial(game.gb)

    def send(self, source, bit):
        self.outgoing[source] = bit

    def exchange(self, source):
        peer = self.peers[source]
        bit = self.core.GB_serial_get_data_bit(peer)
        self.core.GB_serial_set_data_bit(peer, self.outgoing[source])
        self.bits[source] += 1
        return bit

    def tick(self, frames):
        # Both endpoints use DMG clocks. Run the endpoint that is behind.
        run = self.core.GB_run
        left, right = (game.gb for game in self.players)
        remaining = frames * DMG_CYCLES_PER_FRAME
        offset = self.offset
        while remaining > 0:
            if offset <= 0:
                cycles = run(left)
                offset += cycles
                remaining -= cycles
            else:
                offset -= run(right)
        self.offset = offset

    def press(self, key, *players, hold=3):
        for game in players:
            self.core.GB_set_key_state(game.gb, key, True)
        self.tick(hold)
        for game in players:
            self.core.GB_set_key_state(game.gb, key, False)
        self.tick(3)

    def wait(self, predicate, description, *, frames=900, advance=None):
        while frames > 0:
            if predicate():
                return
            if advance is None:
                self.tick(6)
                frames -= 6
            else:
                self.press(A, *advance)
                self.tick(12)
                frames -= 18
        screens = "\n".join(
            f"Map {game.get('wCurMap'):02x}, link state {game.get('wLinkState'):02x}, "
            f"PC {game.cpu.pc:04x}\n{game.visible_text()}"
            for game in self.players
        )
        raise AssertionError(f"Timed out waiting for {description}.\n{screens}")


def name_bytes(name):
    return bytes(ord(letter) - ord("A") + 0x80 for letter in name).ljust(11, b"\x50")


def setup_player(game, name, species, nickname, player_id, second_move, second_pp):
    game.new_game()
    game.put("wPlayerName", name_bytes(name))
    game.put("wPlayerID", player_id)
    game.put("wPartyCount", (1,))
    game.put("wPartySpecies", (species, 0xFF))
    game.put("wPartyMon1Species", (species,))
    game.put("wPartyMon1Moves", (0x81, second_move, 0, 0))  # Swift always hits.
    game.put("wPartyMon1PP", (20, second_pp, 0, 0))
    game.put("wPartyMon1Type", (0x15, 0x15))
    game.put("wPartyMon1BoxLevel", (45,))
    game.put("wPartyMon1Level", (45,))
    for stat in ("HP", "MaxHP", "Attack", "Defense", "Speed", "Special"):
        game.put(f"wPartyMon1{stat}", (0, 160 if stat in ("HP", "MaxHP") else 84))
    game.put("wPartyMon1OTID", player_id)
    game.put("wPartyMon1OT", name_bytes(name))
    game.put("wPartyMon1Nick", name_bytes(nickname))
    game.put("wOptions", (0x81,))

    # Place the test player directly in front of the Viridian receptionist.
    # The normal map loader, NPC, save prompt and room entry all run afterward.
    x, y, width = 11, 3, 7
    view = game.addresses["wOverworldMap"][1] + 7 + width + (width + 6) * (y // 2) + x // 2
    game.put("wCurMap", (VIRIDIAN_POKECENTER,))
    game.put("wDefaultMap", (VIRIDIAN_POKECENTER,))
    game.put("wCurrentTileBlockMapViewPointer", view.to_bytes(2, "little"))
    game.put("wYCoord", (y,))
    game.put("wXCoord", (x,))
    game.put("wYBlockCoord", (y % 2,))
    game.put("wXBlockCoord", (x % 2,))
    game.put("wDestinationWarpID", (0xFF,))
    event = 0x25  # EVENT_GOT_POKEDEX.
    offset, bit = divmod(event, 8)
    address = game.addresses["wEventFlags"][1] + offset
    game.write(address, (game.get("wEventFlags", offset) | (1 << bit),))
    game.invoke("EnterMap")
    game.wait(lambda: game.get("wCurMapWidth") == width and not game.get("wJoyIgnore"))
    game.put("wSpritePlayerStateData1FacingDirection", (4,))  # Up.
    game.put("hSerialConnectionStatus", (0xFF,))
    game.write(0xFFFF, (0x0D,))  # Enable serial, timer and VBlank interrupts.
    game.tick(10)


def has_text(game, text):
    return text.casefold() in game.visible_text().casefold()


def choose_room(cable, room):
    first, second = cable.players
    cable.press(A, first)
    cable.wait(lambda: has_text(first, "Cable Club"), "the first receptionist's greeting")
    cable.tick(24)
    cable.press(A, first)
    cable.wait(
        lambda: first.get("hSerialConnectionStatus") == INTERNAL_CLOCK
        and second.get("hSerialConnectionStatus") == EXTERNAL_CLOCK,
        "the two Game Boys to establish opposite clock roles",
    )
    cable.press(A, second)
    cable.wait(lambda: has_text(second, "Cable Club"), "the second receptionist's greeting")
    cable.tick(24)
    cable.press(A, second)
    for game in cable.players:
        cable.wait(lambda: has_text(game, "YES") and has_text(game, "NO"),
                   "the save choice", advance=(game,))
    cable.press(A, first, second)
    cable.wait(lambda: all(has_text(game, "TRADE CENTER") and has_text(game, "COLOSSEUM")
                           for game in cable.players), "the two room choices")
    cable.tick(24)
    if room == COLOSSEUM:
        cable.press(DOWN, first, second)
        cable.wait(lambda: all(game.get("wLastMenuItem") == 1 for game in cable.players),
                   "both Colosseum choices")
        cable.tick(24)
        # The room menu polls input once between serial exchanges.
        cable.press(A, first, second, hold=12)
    else:
        cable.press(A, first)
    cable.wait(lambda: all(game.get("wCurMap") == room and game.get("wLinkState") == 1
                           for game in cable.players), "both players to enter the chosen room")
    cable.tick(90)
    assert cable.bits[first.gb] > 0
    assert [game.get("wXCoord") for game in cable.players] == [3, 6]
    assert [game.get("wYCoord") for game in cable.players] == [4, 4]


def use_table_game_boys(cable):
    left, right = cable.players
    cable.press(RIGHT, left)
    cable.press(LEFT, right)
    cable.wait(lambda: left.get("wSpritePlayerStateData1FacingDirection") == 12
               and right.get("wSpritePlayerStateData1FacingDirection") == 8,
               "both players to face the table")
    cable.tick(18)
    cable.press(A, left, right)
    cable.wait(lambda: all(has_text(game, "Just a moment") for game in cable.players),
               "both games to start the table session")
    cable.tick(24)
    cable.press(A, left, right)


def trade_member(game):
    return (
        game.get("wPartyMon1Species"),
        game.get_bytes("wPartyMon1OTID", 2),
        game.get_bytes("wPartyMon1OT", 11),
        game.get_bytes("wPartyMon1Nick", 11),
        game.get_bytes("wPartyMon1Moves", 4),
        game.get_bytes("wPartyMon1PP", 4),
    )


def check_party_save(game):
    bank, address = game.addresses["sPartyData"]
    start = bank * 0x2000 + address - 0xA000
    size = game.addresses["wPartyDataEnd"][1] - game.addresses["wPartyDataStart"][1]
    assert bytes(game.battery()[start:start + size]) == game.get_bytes("wPartyDataStart", size)


def check_trade(cable):
    left, right = cable.players
    original = [trade_member(game) for game in cable.players]
    choose_room(cable, TRADE_CENTER)
    use_table_game_boys(cable)
    cable.wait(lambda: all(game.get("wLinkState") == 0x32 and has_text(game, "CANCEL")
                           for game in cable.players),
               "the two trade lists", frames=1800)
    for game, peer in ((left, right), (right, left)):
        assert game.get_bytes("wLinkEnemyTrainerName", 11) == peer.get_bytes("wPlayerName", 11)
        assert game.get("wEnemyPartyCount") == 1
        assert game.get("wEnemyMon1Species") == peer.get("wPartyMon1Species")
        assert game.get_bytes("wEnemyMon1OTID", 2) == peer.get_bytes("wPartyMon1OTID", 2)
    cable.tick(24)
    cable.press(A, left, right)
    cable.wait(lambda: all(has_text(game, "STATS     TRADE") for game in cable.players),
               "both Pokémon action menus")
    cable.press(RIGHT, left, right)
    cable.wait(lambda: all(game.get("wTopMenuItemX") == 11 for game in cable.players),
               "both trade action cursors")
    cable.tick(12)
    cable.press(A, left, right)
    for game in cable.players:
        cable.wait(lambda: has_text(game, "CANCEL") and has_text(game, "be traded")
                   and game.get("wTopMenuItemY") == 8, "the trade confirmation", advance=(game,))
    cable.tick(12)
    cable.press(A, left, right)
    cable.wait(lambda: all(has_text(game, "Trade completed") for game in cable.players),
               "the trade to finish", frames=3600)
    cable.tick(24)
    assert [trade_member(game) for game in cable.players] == original[::-1]
    assert [game.get("wPartyCount") for game in cable.players] == [1, 1]
    for game in cable.players:
        check_party_save(game)


def in_battle_commands(game):
    return game.get("wLinkState") == 4 and game.get("wTopMenuItemY") == 14 and has_text(game, "FIGHT")


def hp(game, mon):
    return int.from_bytes(game.get_bytes(mon + "HP", 2), "big")


def finish_battle(cable):
    left, right = cable.players
    cable.tick(24)
    cable.press(RIGHT, left)
    cable.wait(lambda: left.get("wTopMenuItemX") == 15, "the right battle command column")
    cable.tick(12)
    cable.press(DOWN, left)
    cable.wait(lambda: left.get("wLastMenuItem") == 1, "RUN to be selected")
    cable.press(A, left)
    cable.wait(lambda: left.get("wPlayerMoveListIndex") == 15, "the left player to run")
    cable.press(A, right)
    cable.wait(lambda: right.get("wTopMenuItemY") == 12 and has_text(right, "SWIFT"),
               "the other player's FIGHT menu")
    cable.tick(18)
    cable.press(A, right)
    cable.wait(lambda: all(game.get("wLinkState") == 1 and game.get("wCurMap") == COLOSSEUM
                           and not game.get("wIsInBattle") for game in cable.players),
               "both players to return to the Colosseum", frames=1200)
    assert [game.get("wBattleResult") for game in cable.players] == [1, 0]
    assert all(hp(game, "wPartyMon1") == 160 and game.get("wPartyMon1PP") == 20
               for game in cable.players)


def battle_resources(game):
    return (hp(game, "wBattleMon"), hp(game, "wEnemyMon"),
            game.get_bytes("wBattleMonPP", 4), game.get("wLinkBattleRandomNumberListIndex"))


def compare_while_peer_waits(cable, reader, peer, second_move, effect, *, use_second):
    cable.tick(36)
    cable.press(A, reader, peer)
    cable.wait(lambda: all(game.get("wTopMenuItemY") == 12 and has_text(game, "SWIFT")
                           for game in cable.players), "the two FIGHT move lists")
    cable.tick(24)
    cable.press(SELECT, reader, peer)
    assert all(game.get("wMenuItemToSwap") == 0 for game in cable.players)

    cable.press(START, reader)
    cable.wait(lambda: has_text(reader, "SWIFT") and has_text(reader, "POW"), "Swift's INFO")
    cable.press(A, peer)
    cable.wait(lambda: has_text(peer, "Waiting"), "the other player to submit Swift")
    resources = [battle_resources(game) for game in cable.players]
    selected = reader.get("wPlayerSelectedMove")
    index = reader.get("wPlayerMoveListIndex")
    cable.press(SELECT, reader)
    cable.wait(lambda: has_text(reader, "Skips the usual"), "Swift's effect")
    cable.press(DOWN, reader)
    cable.wait(lambda: has_text(reader, second_move) and has_text(reader, effect),
               f"{second_move}'s effect")
    cable.press(A, reader)
    assert has_text(reader, effect) and has_text(peer, "Waiting")
    if not use_second:
        cable.press(UP, reader)
        cable.wait(lambda: has_text(reader, "Skips the usual"), "Swift's effect again")

    cable.press(B, reader)
    cable.wait(lambda: has_text(reader, "SWIFT") and has_text(reader, second_move),
               "the reader to return to the two FIGHT moves")
    cable.tick(24)
    assert reader.get("wCurrentMenuItem") == (2 if use_second else 1)
    assert (reader.get("wPlayerSelectedMove"), reader.get("wPlayerMoveListIndex")) == (selected, index)
    assert has_text(peer, "Waiting")
    assert [battle_resources(game) for game in cable.players] == resources
    slot = int(use_second)
    reader_pp = reader.get("wBattleMonPP", slot)
    peer_pp = peer.get("wBattleMonPP")
    cable.press(A, reader)
    cable.wait(lambda: all(in_battle_commands(game) for game in cable.players)
               and reader.get("wBattleMonPP", slot) == reader_pp - 1
               and peer.get("wBattleMonPP") == peer_pp - 1,
               "both confirmed attacks to resolve", frames=2400)


def check_battle(cable):
    left, right = cable.players
    choose_room(cable, COLOSSEUM)
    use_table_game_boys(cable)
    cable.wait(lambda: all(in_battle_commands(game) for game in cable.players),
               "the live Colosseum battle commands", frames=2400)
    for game, peer in ((left, right), (right, left)):
        assert game.get("wBattleMonSpecies") == game.get("wPartyMon1Species")
        assert game.get("wEnemyMonSpecies") == peer.get("wPartyMon1Species")
        assert hp(game, "wBattleMon") == hp(peer, "wEnemyMon") == 160
    compare_while_peer_waits(cable, right, left, "WATER GUN", "Deals damage", use_second=False)
    for game, peer in ((left, right), (right, left)):
        assert 0 < hp(game, "wBattleMon") == hp(peer, "wEnemyMon") < 160
        assert game.get("wBattleMonPP") == 19

    # The internal-clock player now confirms Splash from the second slot.
    left_hp, right_hp = hp(left, "wBattleMon"), hp(right, "wBattleMon")
    compare_while_peer_waits(cable, left, right, "SPLASH", "Has no effect", use_second=True)
    assert left.get_bytes("wBattleMonPP", 2) == bytes((19, 36))
    assert right.get_bytes("wBattleMonPP", 2) == bytes((18, 0x57))
    assert 0 < hp(left, "wBattleMon") == hp(right, "wEnemyMon") < left_hp
    assert hp(right, "wBattleMon") == hp(left, "wEnemyMon") == right_hp
    finish_battle(cable)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True, help="SameBoy DMG boot file.")
    parser.add_argument("--room", choices=("trade", "battle"), required=True)
    args = parser.parse_args()
    with Game(args.sameboy, args.boot, args.left) as left, Game(
        args.sameboy, args.boot, args.right
    ) as right:
        setup_player(left, "BLUE", 0x69, "RIVER", (0x12, 0x34), 0x96, 37)
        # The link protocol escapes FE bytes in party records.
        setup_player(right, "GREEN", 0x1B, "STAR", (0xFE, 0x78), 0x37, 0x57)
        with Cable(left, right) as cable:
            check = check_trade if args.room == "trade" else check_battle
            check(cable)
            print(f"{args.left.name} and {args.right.name}: link {args.room} passed "
                  f"after {sum(cable.bits.values())} cable bits.")


if __name__ == "__main__":
    main()
