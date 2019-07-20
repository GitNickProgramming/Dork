# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
# pylint: disable=protected-access
from tests.utils import is_a
import dork.types as types


# def test_confirm_method_yes(capsys, mocker):
#     """confirm should do things
#     """
#     mocked_input = mocker.patch('builtins.input')
#     mocked_input.side_effect = ["y"]
#     assert types.Game._confirm()
#     captured = capsys.readouterr()
#     assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
#     assert mocked_input.call_count == 1


# def test_confirm_method_no(capsys, mocker):
#     """confirm should do things
#     """
#     mocked_input = mocker.patch('builtins.input')
#     mocked_input.side_effect = ["n"]
#     assert types.Game._confirm() is False
#     captured = capsys.readouterr()
#     assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
#     assert mocked_input.call_count == 1


# def test_confirm_method_blank(capsys, mocker):
#     """confirm should do things
#     """
#     mocked_input = mocker.patch('builtins.input')
#     mocked_input.side_effect = ["afk", "    ", "y"]
#     types.Game._confirm()
#     captured = capsys.readouterr()
#     assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
#     assert "That is not a valid response!" in captured.out
#     assert mocked_input.call_count == 3


# def test_start_over_no(capsys, mocker, game):
#     """confirm should do things
#     """
#     mocked_input = mocker.patch('builtins.input')
#     mocked_input.side_effect = ["n"]
#     assert game._start_over("the notification string") == (
#         "Guess you changed your mind!", False)
#     captured = capsys.readouterr()
#     assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
#     assert mocked_input.call_count == 1


# def test_start_over_yes(capsys, mocker, game):
#     """confirm should do things
#     """
#     # the call count here as 2 is a magic number need to document that
#     mocked_input = mocker.patch('builtins.input')
#     mocked_input.side_effect = ["y", "new player name", ".rq"]
#     game._start_over("the notification string")
#     captured = capsys.readouterr()
#     assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
#     assert mocked_input.call_count == 2


def test_player_location(game, player):
    """testing the get and set of player location
    """
    is_a(game.hero.location, types.Room)
    # types.Player.set_location(game.hero, "Arcterus")
    # assert types.Player.get_location(player) == "Arcterus"


def test_move_method(game, mocker, cardinals):
    """testing the move function for any map
    """

    for direction in cardinals:
        if getattr(game.hero.location, direction) is not None:
            move_return = game._move(direction)
            assert (game.hero.location.description, False) == move_return
        if not getattr(game.hero.location, direction):
            move_return = game._move(direction)
            assert (
                f"You cannot go {direction} from here.", False) == move_return
