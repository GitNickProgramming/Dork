# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
from tests.utils import is_a, has_a
import dork.game_utils.game_data as game_data


def test_game_data_vars_exist():
    """the dork module should define a Game
    """
    assert "CMDS" in vars(game_data)
    assert "MOVES" in vars(game_data)
    assert "ERRS" in vars(game_data)
    assert "META" in vars(game_data)
    assert "TITLE" in vars(game_data)


def test_game_data_dictionaries_exist():
    """the game_data should contain dictionaries
    """
    is_a(game_data.CMDS, dict)
    is_a(game_data.MOVES, dict)
    is_a(game_data.ERRS, dict)
    is_a(game_data.META, dict)
    is_a(game_data.TITLE, str)
