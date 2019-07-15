"""This is the REPL which parses commands and passes them to a Game object.
"""
from dork.game_utils import game_data
from dork import types as dork_types


def read():
    """Get input from CLI
    """
    return str.casefold(input("> "))


def evaluate(cmd, game_instance, repl_data):
    """Parse a cmd and run it
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
            method, arg = call[0], noun if noun else (
                call[1] if len(call) > 1 else None
            )
        else:
            method, arg = call
    else:
        call = errs["?"]
        method, arg = call

    return game_instance(method, arg)


def repl():
    """Read eval print loop
    """
    game_instance = dork_types.Game()
    game_instance.build()

    repl_data = (
        game_data.CMDS,
        game_data.MOVES,
        game_data.META,
        game_data.ERRS
    )

    print(f"\nGreetings, {game_instance.hero.name}! " + game_data.TITLE + "\n")

    while True:
        output, should_exit = evaluate(
            cmd=read(), game_instance=game_instance, repl_data=repl_data
        )
        print(output + "\n")
        if should_exit:
            break

    print("shutting down...")
