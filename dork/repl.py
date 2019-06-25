"""This is the REPL which runs the commands, and this is a lame docstring"""
import dork.game_utils.game_data as game_data


CMDS = game_data.CMDS
MOVES = game_data.MOVES
ERRS = game_data.ERRS
META = game_data.META


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
    return action()


def repl():
    """Read eval print loop
    A common idea in terminal cmd programs
    """
    print("starting repl...")

    # call game_data.META["init"]()

    while True:
        cmd = read()
        output, should_exit = evaluate(cmd)
        print(output)
        if should_exit:
            break
    print("ending repl...")
