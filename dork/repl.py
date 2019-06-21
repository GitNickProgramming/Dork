"""This is the REPL which runs the commands, and this is a lame docstring"""
# import dork.dork_utils.yaml_to_dict as parse
import dork.repl_utils.repl_data as repl_data


CMDS = repl_data.CMDS
ARGS = repl_data.ARGS
MOVES = repl_data.MOVES


def read():
    """get input from CLI"""
    return str.casefold(input("> "))


def evaluate(command):
    """parse a command and run it"""

    if " " in command:
        verb, noun = command.split(" ", 1)
        if isinstance(noun, list):
            noun = set(noun) & (set(ARGS) | set(MOVES))
            if len(noun) > 1:
                return "Unknown command", False
            noun = noun.pop()
        if noun not in (ARGS or MOVES):
            return "Unknown command", False

    else:
        verb, noun = command, None

    if verb in CMDS:
        action = CMDS[verb]
    elif verb in MOVES:
        return MOVES[verb]()
    else:
        return "Unknown command", False

    if isinstance(action, dict):
        if noun is not None:
            return action[noun]()
        return "I think you forgot something", False
    return action()


def repl():
    """Read eval print loop
    A common idea in terminal command programs
    """
    print("starting repl...")
    while True:
        command = read()
        print(command)
        output, should_exit = evaluate(command)
        print(output)
        if should_exit:
            break
    print("ending repl...")
