"""This is the REPL which parses commands and passes them to a Game object."""

from dork.game_utils import game_data
from dork import types as dork_types
# pylint: disable=protected-access


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

    dork = dork_types.Gamebuilder.build(player_name)
    print(f"\nGreetings, {dork.hero.name}! " + game_data.TITLE + "\n")

    repl_data = (
        game_data.CMDS,
        game_data.MOVES,
        game_data.META,
        game_data.ERRS
    )

    return dork, repl_data


def _read():
    """Get input from CLI"""

    return str.casefold(input("> "))


def _evaluate(cmd, dork, repl_data):
    """Parse a cmd and run it

    Evaluates the input of the user into an action and runs it

    Args:
        method (str): the method depending on user's input that executes an action
        arg (str): the argument depending on user's input

    Returns:
        method (str): returns the action based on the user's input
        arg (str): returns the argument based on the user's input

    """
    cmds, moves, meta, errs = repl_data
    cmd = cmd.strip().split(" ", 1) if (cmd and not cmd.isspace()) else None
    if cmd:
        verb, *noun = cmd
        noun = noun[0] if noun else None
        call = cmds.get(verb, moves.get(verb, meta.get(verb, errs["u"])))
        if isinstance(call, dict):
            method, arg = call.get(noun, errs["no go"])
        elif call not in errs.values():
            if noun and len(call) > 1:
                method, arg = errs["which way"]
            elif noun and len(call) == 1:
                method, arg = call[0], noun
            elif not noun and len(call) > 1:
                method, arg = call
            else:
                method, arg = call[0], None
        else:
            method, arg = call
    else:
        call = errs["?"]
        method, arg = call
    dork._points(call)
    return dork(method, arg)


def repl():
    """read evaluate print loop"""

    dork, repl_data = _new_game()

    while True:
        output, should_exit = _evaluate(
            cmd=_read(), dork=dork, repl_data=repl_data
        )
        if output == "new game":
            dork, repl_data = _new_game()
        else:
            print(output + "\n")

        if should_exit:
            break

    print("shutting down...")
