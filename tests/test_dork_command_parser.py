"""Test_Dork_Command_Parser I have to describe
 that this tests parser for lint """
from unittest import mock
import dork.command_parser as _mp
import dork.types as _tp


def test_hello_world():
    """Testing the hello world function of parser """
    assert _mp.get_hello_world() == ("hello, world!", False),\
        """Hello world method failed"""


def test_goodbye_world():
    """Testing the goodbye function of parser """
    assert _mp.get_goodbye_world() == ("""goodbye, world!""", True),\
        """Goodbye world method failed"""


def test_show_help():
    """Testing the help method of parser """
    assert _mp.get_show_help() == ("try typing 'say hello'", False)


def test_player_instance():
    """Testing the instantiation of Player class """
    player = _mp.create_player()
    assert player is not None, "Typing error, Player is None"
    assert isinstance(player, _tp.Player), """Typing error,
        player is not Player class"""


def test_evaluate_hello():
    """Testing the eval function of Repl """
    assert _mp.evaluate("say hello") == ("hello, world!", False),\
        """Hello world evalutation failed"""


def test_evaluate_empty():
    """Testing the eval function of Repl """
    assert _mp.evaluate("") == ("Unknown Command", False),\
        """Input Type Handling Error, empty string"""


def test_evaluate_other_type():
    """Testing the eval function of Repl """
    assert _mp.evaluate(None) == ("Unknown Command", False),\
        """Input Mismatch, unable to handle"""


def test_evaluate_goodbye():
    """Testing the eval function of Repl """
    assert _mp.evaluate("say goodbye") == ("goodbye, world!", True),\
        """Goodbye world evaluation failed"""


def test_evaluate_help():
    """Testing the eval function of Repl """
    assert _mp.evaluate("help say") == ("try typing 'say hello'", False),\
        """help say command failed"""


def test_read_string():
    """Testing the read function of Repl """
    with mock.patch('builtins.input') as inp:
        inp.side_effect = ["a string"]
        result = _mp.read()
        assert result == "a string", "Failed to read"


def test_read_empty():
    """Testing the read function of Repl """
    with mock.patch('builtins.input') as inp:
        inp.side_effect = [""]
        result = _mp.read()
        assert result == "", "Unable to read empty strings"


def test_read_escape_char():
    """Testing the read function of Repl """
    with mock.patch('builtins.input') as inp:
        inp.side_effect = '\n'
        result = _mp.read()
        assert '\n' in result, "Unable to read special characters"


def test_repl():
    """Testing repl's existance """
    assert isinstance(_mp.repl, object), "Repl doesn't exist"


def test_eval_verb_only():
    """Testing subject non-existant"""
    assert _mp.evaluate("say dog") == ("Unknown Command", False),\
        "verb failed to process"


def test_eval_subject_only():
    """Testing verb non-existant """
    assert _mp.evaluate("dog help") == ("Unknown Command", False),\
        "subject failed to process"


def test_eval_three_words():
    """Testing 3 input words"""
    assert _mp.evaluate("say help help") == ("try typing 'say hello'", False),\
        "Failed to ignore 3rd word in input"


def test_repl_running(run):
    """Testing repl running at all"""
    result = run(_mp.repl, input_side_effect=["say goodbye"])
    assert "starting repl..." in result[0], "repl failed to run"
