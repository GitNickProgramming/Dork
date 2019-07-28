# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
from dork import repl

# pylint: disable=protected-access


def test_basic_command_functioning(game, repl_data):
    """Basic commands must not crash game"""

    assert repl._evaluate("go", game, repl_data)
    assert repl._evaluate("move", game, repl_data)
    assert repl._evaluate("walk", game, repl_data)
    assert repl._evaluate("travel", game, repl_data)
    assert repl._evaluate("run", game, repl_data)
    assert repl._evaluate("head", game, repl_data)
    assert repl._evaluate("look", game, repl_data)
    assert repl._evaluate("i", game, repl_data)
    assert repl._evaluate("inv", game, repl_data)
    assert repl._evaluate("inventory", game, repl_data)
    assert repl._evaluate("examine", game, repl_data)
    assert repl._evaluate("add", game, repl_data)
    assert repl._evaluate("grab", game, repl_data)
    assert repl._evaluate("take", game, repl_data)
    assert repl._evaluate("loot", game, repl_data)
    assert repl._evaluate("drop", game, repl_data)
    assert repl._evaluate("use", game, repl_data)
    assert repl._evaluate("activate", game, repl_data)
    assert repl._evaluate("points", game, repl_data)
