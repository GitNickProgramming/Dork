"""Test_Dork_Command_Parser I have to describe
 that this tests parser for lint """
import dork.command_parser as _mp
import dork.types as _tp
import tests.daves_mock


def test_hello_world():
    """Testing the hello world function of parser """
    assert _mp.get_hello_world()[0] == "hello, world!", """Hello world
     method failed"""


def test_goodbye_world():
    """Testing the goodbye function of parser """
    assert _mp.get_goodbye_world()[0] == """goodbye, world!""", """Goodbye
    world method failed"""


def test_show_help():
    """Testing the help method of parser """
    assert _mp.get_show_help()[0] == "try typing 'say hello'"


def test_player_instance():
    """Testing the instantiation of Player class """
    player = _mp.create_player()
    assert player is not None, "Typing error, Player is None"
    assert isinstance(player, _tp.Player), """Typing error,
    player is not Player class"""


def test_evaluate_hello():
    """Testing the eval function of Repl """
    assert _mp.evaluate("say hello")[0] == "hello, world!", """Hello world"
    evalutation failed"""


def test_evaluate_empty():
    """Testing the eval function of Repl """
    assert _mp.evaluate("")[0] == "Unknown Command", """Input Type Handling"
    Error, empty string"""


def test_evaluate_other_type():
    """Testing the eval function of Repl """
    assert _mp.evaluate(None)[0] == "Unknown Command", """Input Mismatch,"
    unable to handle"""


def test_evaluate_goodbye():
    """Testing the eval function of Repl """
    assert _mp.evaluate("say goodbye")[0] == "goodbye, world!", """Goodbye world
    evaluation failed"""


def test_evaluate_help():
    """Testing the eval function of Repl """
    assert _mp.evaluate("help say")[0] == "try typing 'say hello'", """help say
    command failed"""


def test_read_string():
    """Testing the read function of Repl """
    inp = tests.daves_mock.MockInput()

    inp.change_input("a string")
    _mp.input = inp.make_input
    assert _mp.read() == "a string", "Failed to read"


def test_read_empty():
    """Testing the read function of Repl """
    inp = tests.daves_mock.MockInput()
    inp.change_input("")
    _mp.input = inp.make_input
    assert _mp.read() == "", "Unable to read empty strings"


def test_read_escape_char():
    """Testing the read function of Repl """
    inp = tests.daves_mock.MockInput()
    inp.change_input("\n")
    _mp.input = inp.make_input
    assert _mp.read() == "\n", "Unable to read special characters"
    _mp.input = input


def test_repl():
    """Testing repl's existance """
    assert isinstance(_mp.repl, object), "Repl doesn't exist"
