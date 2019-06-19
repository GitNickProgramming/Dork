import map_parser.command_parser as mp
import dork.types as tp
import tests.daves_mock

def test_hello_world(run):
    assert mp._hello_world()[0] == "hello, world!", "Hello world method failed"

def test_goodbye_world(run):
    assert mp._goodbye_world()[0] == "goodbye, world!", "Goodby world method failed"

def test_show_help(run):
    assert mp._show_help()[0] == "try typing 'say hello'"

def test_player_instance(run):
    player = mp.create_player()
    assert player is not None, "Typing error, Player is None"
    assert isinstance(player ,tp.Player), "Typing error, player is not Player class"

def test_evaluate(run):
    assert mp.evaluate("say hello")[0] == "hello, world!", "Hello world evalutation failed"
    assert mp.evaluate("")[0] == "Unknown Command", "Input Type Handling Error, empty string"
    assert mp.evaluate(None)[0] == "Unknown Command", "Input Mismatch, unable to handle"
    assert mp.evaluate("say goodbye")[0] == "goodbye, world!", "Goodbye world evaluation failed"
    assert mp.evaluate("help say")[0] == "try typing 'say hello'", "help say command failed"
   
def test_read(run):
    inp = tests.daves_mock.mock_input()

    inp.change_input("a string")
    mp.input = inp.make_input
    assert mp.read() == "a string", "Failed to read"


    inp.change_input("")
    mp.input = inp.make_input
    assert mp.read() == "", "Unable to read empty strings"
    inp.change_input("\n")
    mp.input = inp.make_input
    assert mp.read() == "\n", "Unable to read special characters"
    mp.input = input
