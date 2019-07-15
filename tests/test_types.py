# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
# pylint: disable=protected-access
import unittest.mock as mock
from tests.utils import is_a
import dork.types as types
import dork.repl



def test_confirm_method_yes(capsys, mocker):
    """confirm should do things
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["y"]
    assert types.Game._confirm()
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert mocked_input.call_count == 1


def test_confirm_method_no(capsys, mocker):
    """confirm should do things
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["n"]
    assert types.Game._confirm() is False
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert mocked_input.call_count == 1


def test_confirm_method_blank(capsys, mocker):
    """confirm should do things
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["afk", "    ", "y"]
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
    assert game._start_over("the notification string") == (
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
    game._start_over("the notification string")
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
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["bobby b"]
    types.Game.build(game)
    assert game._inventory() == (
        "Inventory:\n\n    wobblelobbledobdob", False
    )


def test_player_has_none(player):
    """Tests race case where player contains None"""
    test_dict = {"name": "leather belt",
                 "equipped": "leather belt", "inventory": [None, None]}
    test_player = player
    test_player.make(test_dict)
    assert test_player.items == dict(),\
        "Player copied None object as item"


def test_look(run):
    """testing _look for display items and description"""
    out = run(dork.repl.repl, input_side_effect=["name", "look around", ".rq"])
    assert "Items:\nsoggy waffle\ntorn parchment\nbroken quill" in out[0],\
           "item are not found on entrance room"
    test_game = types.Game()
    assert test_game._look() == (None, False)


def test_take(run):
    """testing _take the method takes all and specific item"""
    out = run(dork.repl.repl, input_side_effect=["name", "take", ".rq"])
    assert "You took all item. You took them well." in out[0],\
           "item are not found on entrance room"
