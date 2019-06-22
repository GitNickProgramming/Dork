"""This is the REPL which runs the commands, and this is a lame docstring"""
# import dork.yaml_parser as parse
import dork.repl_utils.repl_data as repl_data
from functools import partial


CMDS = repl_data.CMDS
MOVES = repl_data.MOVES


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
        return repl_error("?")
    if verb in CMDS:
        action = CMDS[verb]
    elif verb in MOVES:
        action = MOVES[verb]
    else:
        return repl_error("u")
    if isinstance(action, dict):
        if noun is not None and noun in action:
            return action[noun]()
        return repl_error("u")
    return action()


def repl_error(arg):
    """return various errors"""
    return {
        "u": ("Unknown command", False),
        "?": ("Huh? Can you speak up?", False)
    }[arg]


def repl():
    """Read eval print loop
    A common idea in terminal command programs
    """
    print("starting repl...")
    while True:
        command = read()
        output, should_exit = evaluate(command)
        print(output)
        if should_exit:
            break
    print("ending repl...")
