# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
from tests.utils import is_a
import dork.game_utils.game_data as game_data


def test_game_data_main_dictionaries_exist():
    """the dork module should define a Game
    """
    assert "CMDS" in vars(game_data)
    is_a(game_data.CMDS, dict)
    assert "MOVES" in vars(game_data)
    is_a(game_data.CMDS, dict)
    assert "ERRS" in vars(game_data)
    is_a(game_data.CMDS, dict)
    assert "META" in vars(game_data)
    is_a(game_data.CMDS, dict)
    assert "TITLE" in vars(game_data)
    is_a(game_data.CMDS, dict)