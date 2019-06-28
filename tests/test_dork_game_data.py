# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
from tests.utils import is_a, has_a
import dork.game_utils.game_data as game_data
import dork


def test_game_data_repl_exists():
    """the dork module should define a Game
    """
    assert "Hero" in vars(game_data)
    is_a(game_data.Hero, type)


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

def test_game_data_repl_methods(hero):
    """the dork module should define a Game
    """
    has_a(hero, "_reset")
    has_a(hero, "_printgame")
    has_a(hero, "_printname")
    has_a(hero, "_make_game")
    has_a(hero, "_move")
    has_a(hero, "_gtfo")
    has_a(hero, "_zork")
    has_a(hero, "_repl_error")
    has_a(hero, "_confirm")

