"""This is the REPL which parses commands and passes them to a Game object."""

from dork.game_utils import game_data
from dork.types import Gamebuilder
# pylint: disable=protected-access


_CMDS = game_data.CMDS
_MOVES = game_data.MOVES
_META = game_data.META
_ERRS = game_data.ERRS


def _new_game(player_name=None):
    """Starts a new game, based on player name

    Creates a new game based upon the name the user enters.

    Args:
        player_name (str): variable that holds user's player name
        dork (str): builds game based upon player's name
        repl_data (str): dictonary of game commands

    Returns:
        dork (str): returns a unique game based on player's name
        repl_data (str): returns an action based on user's input

    """
    if not player_name:
        player_name = input("What's your name, stranger? ")

    dork = Gamebuilder.build(player_name)
    print(f"\nGreetings, {dork.hero.name}! " + game_data.TITLE + "\n")

    return dork


def _read():
    """Get input from CLI"""

    return str.casefold(input("> "))


def _evaluate(cmd, dork):
    """Parse a cmd and run it

    Evaluates the input of the user into an action and runs it

    Args:
        method (str): the method depending on user's input executes an action
        arg (str): the argument depending on user's input

    Returns:
        method (str): returns the action based on the user's input
        arg (str): returns the argument based on the user's input

    """
    cmd = cmd.strip().split(" ", 1) if (cmd and not cmd.isspace()) else None
    if cmd:
        verb, *noun = cmd
        noun = noun[0] if noun else None
        call = _CMDS.get(verb, _MOVES.get(verb, _META.get(verb, _ERRS["u"])))
        if isinstance(call, dict):
            method, arg = call.get(noun, _ERRS["which way"])
        elif call not in _ERRS.values():
            if noun and len(call) > 1:
                method, arg = _ERRS["which way"]
            elif noun and len(call) == 1:
                method, arg = call[0], noun
            elif not noun and len(call) > 1:
                method, arg = call
            else:
                method, arg = call[0], None
        else:
            method, arg = call
    else:
        call = _ERRS["?"]
        method, arg = call
    dork._points(call)
    return dork(method, arg)


def repl():
    """read evaluate print loop

    Depending on the user's input prints an action, if input = .rq, quits game

    Args:
        output (str): If output is equal to new game, a new game is created

    Returns:
        output (str): returns a new game if equal to a new game, quit when .rq

    """
    dork = _new_game()
    should_exit = False

    while not should_exit:
        output, should_exit = _evaluate(cmd=_read(), dork=dork)
        if output == "new game":
            dork = _new_game()
        else:
            print(output + "\n")
