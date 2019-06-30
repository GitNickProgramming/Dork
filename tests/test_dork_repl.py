# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
from unittest import mock
import dork.repl
from dork import types


def test_repl_method_read(mocker):
    """Dork.repl.read should always exist and runs
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["lEeTteXt", "UPPER", "   ", ""]
    assert dork.repl.read() == "leettext"
    assert dork.repl.read() == "upper"
    assert dork.repl.read() == "   "
    assert dork.repl.read() == ""
    assert mocked_input.call_count == 4


def test_repl_evaluate(repl_data):
    """Dork.repl.evaluate should deal with all input types
    """
    assert dork.repl.evaluate("", types.Game, repl_data) == (
        'Huh? Can you speak up?', False)
    assert dork.repl.evaluate("     ", types.Game, repl_data) == (
        'Huh? Can you speak up?', False)
    assert dork.repl.evaluate("Go", types.Game, repl_data) == (
        "Sorry, I don't know that one.", False)
    assert dork.repl.evaluate("walk map", types.Game, repl_data) == (
        "Sorry, I don't know that one.", False)
    assert "You have entered" or "You cannot go" in dork.repl.evaluate(
        "N", types.Game, repl_data)
    assert "You have entered" or "You cannot go" in dork.repl.evaluate(
        "walk south", types.Game, repl_data)


def test_repl_evaluate_various_functions(repl_data):
    """Dork.repl.evaluate has various functions
    """
    with mock.patch('builtins.input') as inp:
        inp.side_effect = ['Saul Good Man', '']
        test_instance = dork.types.Game()
        assert dork.repl.evaluate(".rq", test_instance, repl_data) == (
            'Thanks for playing DORK, Saul Good Man!', True)
        assert dork.repl.evaluate(".z", test_instance, repl_data) == (
            "Oh shit, you found an easter egg!", False)


def test_repl_method_repl(run, mocker):
    """Dork.repl.repl should do things
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
