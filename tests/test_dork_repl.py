# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
from dork import repl


def test_repl_method_read(mocker):
    """Dork.repl.read should always exist and runs
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = [
        "lEeTteXt", "UPPER", "   ", "", " SPACEUPPER", "UPPERSPACE "
    ]
    assert repl.read() == "leettext"
    assert repl.read() == "upper"
    assert repl.read() == "   "
    assert repl.read() == ""
    assert repl.read() == " spaceupper"
    assert repl.read() == "upperspace "
    assert mocked_input.call_count == 6


def test_repl_evaluate(game, repl_data):
    """Dork.repl.evaluate should deal with all input types"""

    assert repl.evaluate(".v", game, repl_data) == (
        "verbose inventory: ON", False)

    assert repl.evaluate(".v", game, repl_data) == (
        "verbose inventory: OFF", False)

    assert repl.evaluate(".m", game, repl_data) == ("", False)

    assert repl.evaluate("", game, repl_data) == (
        'Huh? Can you speak up?', False)

    assert repl.evaluate("     ", game, repl_data) == (
        'Huh? Can you speak up?', False)

    assert repl.evaluate("Go", game, repl_data) == (
        "Sorry, I don't know that one.", False)

    assert repl.evaluate("walk map", game, repl_data) == (
        "You can't go that way", False)

    assert "dummy description" or "You cannot go" in repl.evaluate(
        "n", game, repl_data)

    assert "dummy description" or "You cannot go" in repl.evaluate(
        "s", game, repl_data)

    assert "dummy description" or "You cannot go" in repl.evaluate(
        "e", game, repl_data)

    assert "dummy description" or "You cannot go" in repl.evaluate(
        "w", game, repl_data)

    for _ in range(4):
        if "dummy description" in repl.evaluate("n", game, repl_data):
            break

        if "dummy description" in repl.evaluate("s", game, repl_data):
            break

        if "dummy description" in repl.evaluate("e", game, repl_data):
            break

        if "dummy description" in repl.evaluate("w", game, repl_data):
            break

    assert repl.evaluate(".z", game, repl_data) == (
        "Oh shit, you found an easter egg!", False)

    assert "There's nothing in here." in repl.evaluate("i", game, repl_data)

    repl.evaluate(".v", game, repl_data)
    assert "There's nothing in here." in repl.evaluate("i", game, repl_data)

    assert "Inventory:" in repl.evaluate("examine", game, repl_data)[0]

    assert "dummy description" in repl.evaluate("look", game, repl_data)[0]
