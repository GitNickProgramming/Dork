"""This is the REPL which runs the commands, and this is a lame docstring"""
import dork.game_utils.game_data as game_data


CMDS = game_data.CMDS
MOVES = game_data.MOVES
ERRS = game_data.ERRS
META = game_data.META


def read():
    """get input from CLI"""
    return str.casefold(input("> "))


def evaluate(command):
    """parse a command and run it"""
    command = command.split()
    if command:
        if len(command) > 1:
            noun, verb = command.pop(), command.pop()
        else:
            noun, verb = None, command.pop()
    else:
        action = ERRS["?"]

    # TODO: fix this nonsense
    if verb in CMDS:
        action = CMDS[verb]
    elif verb in MOVES:
        action = MOVES[verb]
    else:
        action = ERRS["u"]

    if isinstance(action, dict):
        if noun is not None and noun in action:
            return action[noun]()
        action = ERRS["u"]
    return action()


def repl():
    """Read eval print loop
    A common idea in terminal command programs
    """
    print("starting repl...")

    # call game_data.META["init"]()

    while True:
        command = read()
        output, should_exit = evaluate(command)
        print(output)
        if should_exit:
            break
    print("ending repl...")
