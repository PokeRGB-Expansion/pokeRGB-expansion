"""Check full-party box browsing and menu returns through a Pokémon Center PC."""

import argparse
from pathlib import Path

from cartridge_smoke import Game, seed_party


UP, DOWN, A, B = 2, 3, 4, 5
NO_SCROLL = (0, 0)
FULL_PARTY, FULL_BOX = 6, 20


def name_bytes(name):
    return bytes(ord(letter) - 65 + 0x80 for letter in name).ljust(11, b"\x50")


def box_name(index):
    return "BOXA" + chr(65 + index)


def party_name(index):
    return "PARTY" + chr(65 + index)


def data_block(game, first, last):
    return game.get_bytes(first, game.addresses[last][1] - game.addresses[first][1])


def rosters(game):
    return (data_block(game, "wPartyDataStart", "wPartyDataEnd"),
            data_block(game, "wBoxDataStart", "wBoxDataEnd"))


def stock_pc(game):
    seed_party(game)
    party_length = game.addresses["wPartyMon2Species"][1] - game.addresses["wPartyMon1Species"][1]
    box_length = game.addresses["wBoxMon2Species"][1] - game.addresses["wBoxMon1Species"][1]
    first = game.get_bytes("wPartyMon1Species", party_length)
    game.put("wPartyCount", (FULL_PARTY,))
    game.put("wPartySpecies", (0x69,) * FULL_PARTY + (0xFF,))
    for number in range(1, FULL_PARTY + 1):
        game.put(f"wPartyMon{number}Species", first)
        game.put(f"wPartyMon{number}OT", name_bytes("BLUE"))
        game.put(f"wPartyMon{number}Nick", name_bytes(party_name(number - 1)))
    game.put("wBoxCount", (FULL_BOX,))
    game.put("wCurrentBoxNum", (0x80,))
    species = tuple(0x69 if number % 2 else 0x1B for number in range(1, FULL_BOX + 1))
    game.put("wBoxSpecies", species + (0xFF,))
    for number, kind in enumerate(species, 1):
        mon = f"wBoxMon{number}"
        game.put(mon + "Species", first[:box_length])
        game.put(mon + "Species", (kind,))
        game.put(mon + "HP", (0, 10))
        game.put(mon + "Type", (0x15, 0x15))
        game.put(mon + "Exp", (0, 0x40, 0))
        game.put(mon + "OTID", (0x12, number))
        game.put(mon + "OT", name_bytes("GREEN"))
        game.put(mon + "Nick", name_bytes(box_name(number - 1)))
    game.put("wOptions", (1,))


def shows(game, *words, accept=False):
    game.wait(lambda: all(word in game.visible_text() for word in words), accept=accept)
    game.tick(16)


def open_bill(game):
    game.enter_map(0x29, 7, 13, 4)  # Face the Viridian Pokémon Center's PC.
    game.put("wSpritePlayerStateData1FacingDirection", (4,))
    game.press(A)
    shows(game, "SOMEONE", "LOG OFF", accept=True)
    game.press(A)
    shows(game, "CHANGE BOX", "WITHDRAW", "DEPOSIT", accept=True)


def list_view(game):
    return game.get("wListScrollOffset"), game.get("wCurrentMenuItem")


def wait_list(game, view, name):
    game.wait(lambda: game.get("wTopMenuItemY") == 4 and list_view(game) == view
              and name in game.visible_text() and "STATS" not in game.visible_text())
    game.tick(18)
    assert list_view(game) == view


def scroll_list(game, steps, name):
    start = sum(list_view(game))
    for current in range(start, start + steps):
        game.press(DOWN)
        game.wait(lambda: sum(list_view(game)) == current + 1)
        game.tick(15)
    assert name in game.visible_text()
    return list_view(game)


def open_action(game, action):
    game.press(A)
    shows(game, action, "STATS", "CANCEL")
    assert game.get("wTopMenuItemY") == 12


def view_stats(game, name):
    game.press(DOWN)
    game.wait(lambda: game.get("wLastMenuItem") == 1)
    game.press(A)
    shows(game, "ATTACK", "D PAD NAV", name)
    game.tick(90)


def check_full_box(game):
    before = rosters(game)
    game.invoke("SaveGameData")
    game.return_to_stub()
    saved = bytes(game.battery()[8192:])
    open_bill(game)
    game.press(A)
    wait_list(game, NO_SCROLL, box_name(0))
    open_action(game, "WITHDRAW")
    view_stats(game, box_name(0))
    game.press(B)
    wait_list(game, NO_SCROLL, box_name(0))
    index = 7
    view = scroll_list(game, index, box_name(index))
    assert view == (5, 2)

    open_action(game, "WITHDRAW")
    view_stats(game, box_name(index))
    game.press(B)
    wait_list(game, view, box_name(index))

    open_action(game, "WITHDRAW")
    view_stats(game, box_name(index))
    game.press(DOWN)
    shows(game, "ATTACK", box_name(index + 1))
    game.tick(90)
    index += 1
    view = (6, 2)
    game.press(B)
    wait_list(game, view, box_name(index))

    open_action(game, "WITHDRAW")
    game.press(B)
    wait_list(game, view, box_name(index))
    open_action(game, "WITHDRAW")
    game.press(DOWN)
    game.tick(12)
    game.press(DOWN)
    game.wait(lambda: game.get("wLastMenuItem") == 2)
    game.press(A)
    wait_list(game, view, box_name(index))

    open_action(game, "WITHDRAW")
    game.press(A)
    shows(game, "You can", "any more")
    shows(game, "Deposit", "first", accept=True)
    game.press(A)
    wait_list(game, view, box_name(index))

    last = FULL_BOX - 1
    view = scroll_list(game, last - index, box_name(last))
    open_action(game, "WITHDRAW")
    view_stats(game, box_name(last))
    game.press(DOWN)
    game.tick(28)
    assert game.get("wWhichPokemon") == last
    game.press(B)
    wait_list(game, view, box_name(last))
    assert rosters(game) == before
    assert bytes(game.battery()[8192:]) == saved

    game.press(B)
    shows(game, "CHANGE BOX", accept=True)
    game.press(B)
    shows(game, "LOG OFF", accept=True)
    game.press(B)
    game.tick(20)
    game.invoke("TryLoadSaveFile")
    game.return_to_stub()
    assert game.get("wSaveFileStatus") == 2
    assert rosters(game) == before


def check_transfer(game, index):
    stock_pc(game)
    game.put("wPartyCount", (FULL_PARTY - 1,))
    game.put("wPartySpecies", (0x69,) * (FULL_PARTY - 1) + (0xFF,))
    open_bill(game)
    game.press(A)
    wait_list(game, NO_SCROLL, box_name(0))
    scroll_list(game, index, box_name(index))
    label = f"wBoxMon{index + 1}"
    species = game.get(label + "Species")
    original_id = game.get_bytes(label + "OTID", 2)
    original_moves = game.get_bytes(label + "Moves", 4)
    original_pp = game.get_bytes(label + "PP", 4)
    open_action(game, "WITHDRAW")
    game.press(A)
    shows(game, "taken out")
    assert game.get("wPartyCount") == FULL_PARTY
    assert game.get("wBoxCount") == FULL_BOX - 1
    assert game.get("wPartyMon6Species") == species
    assert game.get_bytes("wPartyMon6Nick", 11) == name_bytes(box_name(index))
    assert game.get_bytes("wPartyMon6OTID", 2) == original_id
    assert game.get_bytes("wPartyMon6OT", 11) == name_bytes("GREEN")
    assert game.get_bytes("wPartyMon6Moves", 4) == original_moves
    assert game.get_bytes("wPartyMon6PP", 4) == original_pp
    remaining = [name_bytes(box_name(slot)) for slot in range(FULL_BOX) if slot != index]
    assert [game.get_bytes(f"wBoxMon{slot}Nick", 11) for slot in range(1, FULL_BOX)] == remaining


def check_deposit_browsing(game):
    stock_pc(game)
    game.put("wBoxCount", (FULL_BOX - 1,))
    species = game.get_bytes("wBoxSpecies", FULL_BOX - 1)
    game.put("wBoxSpecies", species + b"\xFF")
    before = rosters(game)
    open_bill(game)
    game.press(DOWN)
    game.wait(lambda: game.get("wLastMenuItem") == 1)
    game.press(A)
    wait_list(game, NO_SCROLL, party_name(0))
    index = 3
    view = scroll_list(game, index, party_name(index))
    open_action(game, "DEPOSIT")
    view_stats(game, party_name(index))
    game.press(B)
    wait_list(game, view, party_name(index))
    open_action(game, "DEPOSIT")
    game.press(B)
    wait_list(game, view, party_name(index))
    assert rosters(game) == before
    open_action(game, "DEPOSIT")
    game.press(A)
    shows(game, "stored")
    assert game.get("wPartyCount") == FULL_PARTY - 1
    assert game.get("wBoxCount") == FULL_BOX
    assert game.get_bytes("wBoxMon20Nick", 11) == name_bytes(party_name(index))


def check_empty_box(game):
    stock_pc(game)
    game.put("wBoxCount", (0, 0xFF))
    before = rosters(game)
    open_bill(game)
    game.press(A)
    shows(game, "There are", "here")
    assert rosters(game) == before


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sameboy", type=Path, required=True)
    parser.add_argument("--boot", type=Path, required=True)
    parser.add_argument("--color", choices=("red", "blue", "green"), nargs="+")
    args = parser.parse_args()
    for color in args.color or ("red", "blue", "green"):
        fixture = (args.sameboy, args.boot, args.directory / f"poke{color}.gbc")
        with Game(*fixture) as game:
            game.new_game()
            stock_pc(game)
            check_full_box(game)
        for index in (0, 7, FULL_BOX - 1):
            with Game(*fixture) as game:
                game.new_game()
                check_transfer(game, index)
        for check in (check_deposit_browsing, check_empty_box):
            with Game(*fixture) as game:
                game.new_game()
                check(game)
        print(f"{args.directory.name} {color}: full-party box browsing and withdrawal passed",
              flush=True)


if __name__ == "__main__":
    main()
