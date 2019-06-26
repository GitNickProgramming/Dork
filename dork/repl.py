"""This is the REPL which runs the commands, and this is a lame docstring"""
# from functools import partial
import dork.game_utils.game_data as game_data


REPL_INSTANCE = game_data.REPL()
CMDS = REPL_INSTANCE.CMDS
MOVES = REPL_INSTANCE.MOVES
ERRS = REPL_INSTANCE.ERRS
META = REPL_INSTANCE.META


def read():
    """get input from CLI"""
    return str.casefold(input("> "))


def evaluate(cmd):
    """parse a cmd and run it"""
    cmd = cmd.split()
    if cmd:
        noun, verb = cmd.pop() if len(cmd) > 1 else None, cmd.pop()
        action = CMDS.get(verb, MOVES.get(verb, META.get(verb, ERRS["u"])))
    else:
        action = ERRS["?"]

    if isinstance(action, dict):
        return action.get(noun, ERRS["u"])()
    return action() if not noun else action(noun)


def repl():
    """Read eval print loop
    """
    print("starting repl...")
    while True:
        output, should_exit = evaluate(read())
        print(output)
        if should_exit:
            break
    print("ending repl...")
