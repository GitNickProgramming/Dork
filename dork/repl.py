"""This is the REPL which runs the commands, and this is a lame docstring"""
# import dork.yaml_parser as parse
import dork.repl_utils.repl_data as repl_data


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
            verb, noun = command.pop(), None
    else:
        return "Huh? Can you speak up?", False
    if verb in CMDS:
        action = CMDS[verb]
    elif verb in MOVES:
        return MOVES[verb]()
    else:
        return "Unknown command", False
    if isinstance(action, dict):
        if noun is not None and noun in action:
            return action[noun]()
        return "Unknown command", False
    return action()


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
