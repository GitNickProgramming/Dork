# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
# pylint: disable=protected-access
from tests.utils import is_a
import dork.types as types
import dork.game_utils.factory_data as factory_data


def test_confirm_method_yes(capsys, mocker):
    """confirm should do things"""

    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["y", "tester"]
    assert types.Game._confirm()
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert mocked_input.call_count == 1


def test_confirm_method_no(capsys, mocker):
    """confirm should do things"""

    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["n"]
    assert types.Game._confirm() is False
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert mocked_input.call_count == 1


def test_confirm_method_blank(capsys, mocker):
    """confirm should do things"""

    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["afk", "    ", "y", "tester"]
    types.Game._confirm()
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert "That is not a valid response!" in captured.out
    assert mocked_input.call_count == 3


def test_start_over_no(capsys, mocker, game):
    """confirm should do things"""

    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["n", ".rq"]
    assert game._start_over() == ("Guess you changed your mind!", False)
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert mocked_input.call_count == 1


def test_start_over_yes(capsys, mocker, game):
    """confirm should do things"""

    # the call count here as 2 is a magic number need to document that
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["y", "tester"]
    game._start_over()
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert mocked_input.call_count == 2


def test_player_location(game):
    """testing the get and set of player location"""

    is_a(game.hero.location, types.Room)


def test_move_method(game, cardinals):
    """testing the move function for any map"""

    for direction in cardinals:
        if getattr(game.hero.location, direction) is not None:
            move_return = game._move(direction)
            assert (game.hero.location.description, False) == move_return
        if not getattr(game.hero.location, direction):
            move_return = game._move(direction)
            assert (
                f"You cannot go {direction} from here.", False) == move_return


def test_factory_data():
    """test factory data methods"""

    assert isinstance(factory_data.rules(0, 0), list)
    assert isinstance(factory_data.stats("magic"), dict)
