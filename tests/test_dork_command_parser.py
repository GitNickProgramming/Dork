"""Test_Dork_Command_Parser I have to describe that this tests parser for lint """
import map_parser.command_parser as _mp
import dork.types as _tp
import tests.daves_mock

def test_hello_world():
    """Testing the hello world function of parser """
    assert _mp.get_hello_world()[0] == "hello, world!", "Hello world method failed"

def test_goodbye_world():
    """Testing the goodbye function of parser """
    assert _mp.get_goodbye_world()[0] == "goodbye, world!", "Goodby world method failed"

def test_show_help():
    """Testing the help method of parser """
    assert _mp.get_show_help()[0] == "try typing 'say hello'"

def test_player_instance():
    """Testing the instantiation of Player class """
    player = _mp.create_player()
    assert player is not None, "Typing error, Player is None"
    assert isinstance(player ,_tp.Player), "Typing error, player is not Player class"

def test_evaluate():
    """Testing the eval function of Repl """
    assert _mp.evaluate("say hello")[0] == "hello, world!", "Hello world evalutation failed"
    assert _mp.evaluate("")[0] == "Unknown Command", "Input Type Handling Error, empty string"
    assert _mp.evaluate(None)[0] == "Unknown Command", "Input Mismatch, unable to handle"
    assert _mp.evaluate("say goodbye")[0] == "goodbye, world!", "Goodbye world evaluation failed"
    assert _mp.evaluate("help say")[0] == "try typing 'say hello'", "help say command failed"
def test_read():
    """Testing the read function of Repl """
    inp = tests.daves_mock.mock_input()

    inp.change_input("a string")
    _mp.input = inp.make_input
    assert _mp.read() == "a string", "Failed to read"


    inp.change_input("")
    _mp.input = inp.make_input
    assert _mp.read() == "", "Unable to read empty strings"
    inp.change_input("\n")
    _mp.input = inp.make_input
    assert _mp.read() == "\n", "Unable to read special characters"
    _mp.input = input
