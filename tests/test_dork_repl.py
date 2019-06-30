# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""

from tests.utils import has_method
import dork


def test_repl_method_read(mocker):
    """Dork.repl.read should always exist and runs
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = [
        "lEeTteXt", "UPPER", "   ", "", " SPACEUPPER", "UPPERSPACE "
    ]
    assert dork.repl.read() == "leettext"
    assert dork.repl.read() == "upper"
    assert dork.repl.read() == "   "
    assert dork.repl.read() == ""
    assert dork.repl.read() == " spaceupper"
    assert dork.repl.read() == "upperspace "
    assert mocked_input.call_count == 6


def test_repl_evaluate(game, repl_data):
    """Dork.repl.evaluate should deal with all input types
    """
    assert dork.repl.evaluate("", game, repl_data) == (
        'Huh? Can you speak up?', False)
    assert dork.repl.evaluate("     ", game, repl_data) == (
        'Huh? Can you speak up?', False)
    assert dork.repl.evaluate("Go", game, repl_data) == (
        "Sorry, I don't know that one.", False)
    assert dork.repl.evaluate("walk map", game, repl_data) == (
        "Sorry, I don't know that one.", False)
    assert "You have entered" or "You cannot go" in dork.repl.evaluate(
        "N", game, repl_data)
    assert "You have entered" or "You cannot go" in dork.repl.evaluate(
        "walk south", game, repl_data)


def test_repl_evaluate_various_functions(game, repl_data):
    """Dork.repl.evaluate has various functions
    """
    assert "Thanks for playing DORK", True in dork.repl.evaluate(
        ".rq", game, repl_data
    )
    assert dork.repl.evaluate(".z", game, repl_data) == (
        "Oh shit, you found an easter egg!", False)
    assert isinstance(dork.repl.evaluate("look", game, repl_data)[0], str)
    assert dork.repl.evaluate("i", game, repl_data) == (
        "    You ain't got shit, son!", False)


def test_game_build_methods_exist(game):
    """the game should have build methods
    """
    has_method(game, "build")
    has_method(game, "_build_players")
    has_method(game, "_build_world")
    has_method(game, "_build_hero")


def test_game_methods_exist(game):
    """the game should have control methods
    """
    has_method(game, "_gtfo")
    has_method(game, "_move")
    has_method(game, "_inventory")
    has_method(game, "_look")
    has_method(game, "_start_over")
    has_method(game, "_confirm")
    has_method(game, "_zork")
    has_method(game, "_repl_error")


def test_repl_method_repl(run, mocker):
    """Dork.repl.repl should output like this then end in these conditions
    """
    evaluate_values = [("FooBar", False), ("Bufarr", True)]
    mocked_evaluate = mocker.patch("dork.repl.evaluate")
    mocked_evaluate.side_effect = evaluate_values

    out, err, mocked_input = run(
        dork.repl.repl, input_return_value="42")
    assert "FooBar" in out
    assert "Bufarr" in out
    assert err == ""
    assert mocked_input.call_count == len(evaluate_values) + 1
