# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
# import dork.game_utils.game_data as game_data

import dork.game_utils.game_data as game_data
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


def test_repl_evaluate():
    """Dork.repl.evaluate should deal with all input types
    """
    repl_instance = dork.game_utils.game_data.REPL
    repl_data = (
        game_data.CMDS,
        game_data.MOVES,
        game_data.META,
        game_data.ERRS
    )
    assert dork.repl.evaluate("", repl_instance, repl_data) == (
        'Huh? Can you speak up?', False)
    assert dork.repl.evaluate("     ", repl_instance, repl_data) == (
        'Huh? Can you speak up?', False)
    assert dork.repl.evaluate("Go", repl_instance, repl_data) == (
        "Sorry, I don't know that one.", False)
    assert dork.repl.evaluate("walk map", repl_instance, repl_data) == (
        "Sorry, I don't know that one.", False)
    assert "You have entered" or "You cannot go" in dork.repl.evaluate(
        "N", repl_instance, repl_data)
    assert "You have entered" or "You cannot go" in dork.repl.evaluate(
        "walk south", repl_instance, repl_data)


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
