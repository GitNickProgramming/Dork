# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
from dork import repl


def test_repl_evaluate(game, repl_data):
    """Dork.repl.evaluate should deal with all input types"""

    assert repl.evaluate("", game, repl_data) == (
        'Huh? Can you speak up?', False)

    assert repl.evaluate("     ", game, repl_data) == (
        'Huh? Can you speak up?', False)

    assert repl.evaluate("Go", game, repl_data) == (
        "Sorry, I don't know that one.", False)

    assert repl.evaluate("walk map", game, repl_data) == (
        "You can't go that way", False)


def test_all_moves_and_others(game, repl_data):
    """tests that movement is successful and meta methods"""

    assert repl.evaluate(".m", game, repl_data) == ("", False)

    for _ in range(4):
        if "description" in repl.evaluate("n", game, repl_data):
            break

        if "description" in repl.evaluate("s", game, repl_data):
            break

        if "description" in repl.evaluate("e", game, repl_data):
            break

        if "description" in repl.evaluate("w", game, repl_data):
            break

    assert repl.evaluate(".z", game, repl_data) == (
        "holy *%&#@!!! a wild zork appeared!", False)

    assert repl.evaluate(".v", game, repl_data) == (
        "verbose inventory: ON", False)

    assert "There's nothing here." in repl.evaluate("i", game, repl_data)

    assert repl.evaluate(".v", game, repl_data) == (
        "verbose inventory: OFF", False)

    assert "There's nothing here." in repl.evaluate("i", game, repl_data)

    assert "inventory:" in repl.evaluate("examine", game, repl_data)[0]

    assert "description" in repl.evaluate("look", game, repl_data)[0]

    assert repl.evaluate(".rq", game, repl_data) == (
        "Thanks for playing DORK, tester!", True)

    repl.evaluate(".rq", game, repl_data)
