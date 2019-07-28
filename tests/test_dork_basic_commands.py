# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork"""

from dork import repl
# pylint: disable=protected-access


def test_basic_command_functioning(game):
    """Basic commands must not crash game"""

    assert repl._evaluate("go", game)
    assert repl._evaluate("move", game)
    assert repl._evaluate("walk", game)
    assert repl._evaluate("travel", game)
    assert repl._evaluate("run", game)
    assert repl._evaluate("head", game)
    assert repl._evaluate("look", game)
    assert repl._evaluate("i", game)
    assert repl._evaluate("inv", game)
    assert repl._evaluate("inventory", game)
    assert repl._evaluate("examine", game)
    assert repl._evaluate("add", game)
    assert repl._evaluate("grab", game)
    assert repl._evaluate("take", game)
    assert repl._evaluate("loot", game)
    assert repl._evaluate("drop", game)
    assert repl._evaluate("use", game)
    assert repl._evaluate("activate", game)
    assert repl._evaluate("points", game)
