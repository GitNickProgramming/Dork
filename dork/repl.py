"""This is the REPL which parses commands and passes them to a Game object."""

from dork.game_utils import game_data
from dork import types as dork_types
# pylint: disable=protected-access


def _read():
    """Get input from CLI"""

    return str.casefold(input("> "))


def _evaluate(cmd, dork, repl_data):
    """Parse a cmd and run it"""

    cmds, moves, meta, errs = repl_data
    cmd = cmd.strip().split(" ", 1) if (cmd and not cmd.isspace()) else None
    if cmd:
        verb, *noun = cmd
        noun = noun[0] if noun else None
        call = cmds.get(verb, moves.get(verb, meta.get(verb, errs["u"])))
        if isinstance(call, dict):
            method, arg = call.get(noun, errs["no go"])
        elif call not in errs.values():
            method, arg = call[0], noun if noun else (
                call[1] if len(call) > 1 else None
            )
        else:
            method, arg = call
    else:
        call = errs["?"]
        method, arg = call

    return dork(method, arg)


def repl():
    """read evaluate print loop"""
    def _new_game(player_name=None):
        if not player_name:
            player_name = input("What's your name, stranger? ")

        dork = dork_types.Gamebuilder.build(player_name)

        repl_data = (
            game_data.CMDS,
            game_data.MOVES,
            game_data.META,
            game_data.ERRS
        )

        return dork, repl_data

    dork, repl_data = _new_game()
    print(f"\nGreetings, {dork.hero.name}! " + game_data.TITLE + "\n")

    while True:
        output, should_exit = _evaluate(
            cmd=_read(), dork=dork, repl_data=repl_data
        )
        print(output + "\n")
        if should_exit:
            break

    print("shutting down...")
