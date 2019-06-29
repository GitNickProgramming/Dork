# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""

import dork.game_utils.game_data as game_data
from tests.utils import has_method
import dork


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
    assert dork.repl.evaluate(".rq", game, repl_data) == (
        'Thanks for playing DORK, None!', True)
    assert dork.repl.evaluate(".z", game, repl_data) == (
        "Oh shit, you found an easter egg!", False)
    assert dork.repl.evaluate("look", game, repl_data) == (
        None, False)
    assert dork.repl.evaluate("i", game, repl_data) == (
        "    You ain't got shit, son!", False)


def test_repl_evaluate_move(game, repl_data):
    """Dork.repl.evaluate has various functions
    """
    assert dork.repl.evaluate(".rq", game, repl_data) == (
        'Thanks for playing DORK, None!', True)
    assert dork.repl.evaluate(".z", game, repl_data) == (
        "Oh shit, you found an easter egg!", False)


def test_game_methods_exist(game):
    """the dork module should define a Game
    """
    has_method(game, "build")
    has_method(game, "_build_players")
    has_method(game, "_build_world")
    has_method(game, "_build_hero")
    has_method(game, "_gtfo")
    has_method(game, "_move")
    has_method(game, "_inventory")
    has_method(game, "_look")
    has_method(game, "_start_over")
    has_method(game, "_confirm")
    has_method(game, "_zork")
    has_method(game, "_repl_error")


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


# def test_mocked_evals(run, mocker, game, repl_data):
#     """Dork.repl.read should always exist and runs
#     """
#     new = dork.repl.evaluate(".new", game, repl_data)
#     after_new = dork.repl.evaluate("n", game, repl_data)
#     after_cancel = dork.repl.evaluate(".rq", game, repl_data)

# def test_repl_call_to_build(run, mocker):
#     """Dork.repl.read should always exist and runs
#     """


#     out, err, mocked_input = run(
#         dork.types.Game.build, input_side_effect="player name")
#     assert "What's your name, stranger? " in out
#     assert err == ""
#     assert mocked_input.call_count == 1

    # game_data.REPL()
    # captured = capsys.readouterr()
    # assert captured.out == "What's your name, stranger? "

    # def test_say_the_truth():
    # with mock.patch('builtins.input') as mocked_input:
    #     mocked_input.side_effect = ["", "the streets"]
    #     test_say_the_truth()
    # assert say_the_truth() == "the truth"
    # assert say_the_truth() == "the truth about the streets"
    # assert mocked_input.call_count == 2

    # arguments_sent = ["lEeTeXt", "UPPER", "lower"]
    # out, err, mocked_input = run(dork.repl.read, arguments_sent, input_side_effect=['first', 'second', 'last'])

    # assert out is None

    # # assert isinstance(dork.cli.main, FunctionType)


# def test_repl_read():
#     with mock.patch('builtins.input') as mocked_input:
#         mocked_input.side_effect = ["", "UPPER", "lower", "098", "    ", "lEEtTeXt"]

#     assert dork.repl.read() == ""
#     assert dork.repl.read() == "upper"
#     assert dork.repl.read() == "lower"
#     assert dork.repl.read() == "098"
#     assert dork.repl.read() == "    "
#     assert dork.repl.read() == "leettext"
#     assert mocked_input.call_count == 6


# def test_repl_eval():
#     assert dork.repl.repl() == "What's your name, stranger?"
#     with mock.patch('builtins.input') as mocked_input:
#         mocked_input.side_effect = ["", "Name"]

#     assert dork.repl.repl() == dork.game_utils.game_data.TITLE
#     assert dork.repl.repl() == ""
#     assert mocked_input.call_count == 2
