# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""

from tests.utils import has_a, has_method, is_a
import dork.types as types


# pylint: disable=protected-access


def test_game_attributes(game):
    """the game should have attributes
    """
    has_a(game, "players")
    has_a(game, "worldmap")
    has_a(game, "hero")


def test_game_methods(game):
    """the game should have these methods
    """
    has_method(game, "build")
    has_method(game, "_build_players")
    has_method(game, "_build_world")
    has_method(game, "_build_hero")
    has_method(game, "_gtfo")
    has_method(game, "_move")
    has_method(game, "_inventory")
    has_method(game, "_look")
    has_method(game, "_start_over")
    has_method(game, "_save_game")
    has_method(game, "_confirm")


def test_room_attributes(room):
    """the room should have attributes
    """
    has_a(room, "name")
    has_a(room, "adjacent")
    has_a(room, "description")
    has_a(room, "players")
    has_a(room, "items")
    has_a(room, "clues")


def test_player_attributes(player):
    """the player should have attributes
    """
    has_a(player, "name")
    has_a(player, "location")
    has_a(player, "items")
    has_a(player, "equipped")


def test_item_attributes(item):
    """item should have holder and capacity
    """
    has_a(item, "name")
    has_a(item, "description")
    has_a(item, "stats")


def test_holder_attributes(holder):
    """holder should have items
    """
    has_a(holder, "items")


def test_worldmap_attributes(worldmap):
    """the worldmap should have a dict of rooms
    """
    has_a(worldmap, "rooms")
    has_a(worldmap, "players")


def test_confirm_method(capsys, mocker):
    """confirm should do things
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["y", "n"]

    assert types.Game._confirm()
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out

    assert not types.Game._confirm()
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out

    assert mocked_input.call_count == 2


def test_confirm_method_blank(capsys, mocker):
    """confirm should do things
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["2543", "    ", "y"]
    
    types.Game._confirm()
    captured = capsys.readouterr()
    
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert "That is not a valid response!" in captured.out
    assert mocked_input.call_count == 3


def test_start_over_no(capsys, mocker, game):
    """confirm should do things
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["n"]
    assert game._start_over() == (
        "Guess you changed your mind!", False)
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert mocked_input.call_count == 1


def test_start_over_yes(capsys, mocker, game):
    """confirm should do things
    """
    # the call count here as 2 is a magic number need to document that
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["y", "new player name", ".rq"]
    game._start_over()
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert mocked_input.call_count == 2


def test_player_location(player):
    """testing the get and set of player location
    """
    is_a(player.location, types.Room)
    types.Player.set_location(player, "Arcterus")
    assert types.Player.get_location(player) == "Arcterus"


def test_move_method(game, mocker, cardinals):
    """testing the move function for any map
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["new player name"]
    types.Game.build(game)
    is_a(game.hero.location, types.Room)
    assert game.hero.location.name == "entrance"

    for direction in cardinals:
        if game.hero.location.adjacent[direction] is not None:
            move_return = game._move(direction)
            assert (game.hero.location.description, False) == move_return
        if game.hero.location.adjacent[direction] is None:
            move_return = game._move(direction)
            assert (
                f"You cannot go {direction} from here.", False) == move_return


def test_inventory_empty(game, mocker):
    """testing the inventory function
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["new player name"]
    types.Game.build(game)
    assert game._inventory() == ("    You ain't got shit, son!", False)


def test_inventory_has_item(game, mocker):
    """testing the inventory function
    """
    bobby_b_inventory = \
        "Inventory:\n\n    wobblelobbledobdob\n    bow of purposelessness"
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["bobby b"]
    types.Game.build(game)
    assert game._inventory() == (bobby_b_inventory, False)
