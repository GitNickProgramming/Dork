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
    """Dork.repl.evaluate should deal with all input types
    """
    assert repl.evaluate("", game, repl_data) == (
        'Huh? Can you speak up?', False)
    assert repl.evaluate("     ", game, repl_data) == (
        'Huh? Can you speak up?', False)
    assert repl.evaluate("Go", game, repl_data) == (
        "Sorry, I don't know that one.", False)
    assert repl.evaluate("walk map", game, repl_data) == (
        "You can't go that way", False)
    assert "You have entered" or "You cannot go" in repl.evaluate(
        "N", game, repl_data)
    assert "You have entered" or "You cannot go" in repl.evaluate(
        "walk south", game, repl_data)


# def test_repl_evaluate_various_functions(game, repl_data):
#     """Dork.repl.evaluate has various functions
#     """

#     assert repl.evaluate(".rq", game, repl_data) == (
#         'Thanks for playing DORK, None!', True)

#     assert repl.evaluate(".z", game, repl_data) == (
#         "Oh shit, you found an easter egg!", False)

#     assert "dummy description" in repl.evaluate("look", game, repl_data)[0]

#     assert repl.evaluate("i", game, repl_data) == (
#         "    You ain't got shit, son!", False)


# def test_repl_evaluate_move(game, repl_data):
#     """Testing simple repl functions
#     """
#     assert repl.evaluate(".rq", game, repl_data) == (
#         'Thanks for playing DORK, None!', True)
#     assert repl.evaluate(".z", game, repl_data) == (
#         "Oh shit, you found an easter egg!", False)


# def test_repl_method_repl(run, mocker):
#     """Dork.repl.repl should output like this then end in these conditions
#     """
#     evaluate_values = [("FooBar", False), ("Bufarr", True)]
#     mocked_evaluate = mocker.patch("evaluate")
#     mocked_evaluate.side_effect = evaluate_values

#     out, err, mocked_input = run(
#         repl.repl, input_return_value="42")
#     assert "FooBar" in out
#     assert "Bufarr" in out
#     assert err == ""
#     assert mocked_input.call_count == len(evaluate_values) + 1
