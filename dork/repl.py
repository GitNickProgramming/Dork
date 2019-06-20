from functools import partial
# import dork.dork_utils.yaml_to_dict as parse
import dork.dork_utils.repl_data as repl_data


CMDS = repl_data.CMDS
ARGS = repl_data.ARGS


def read():
    """get input from CLI"""
    return input("> ")


def evaluate(command):
    """parse a command and run it"""

    if " " in command:
        verb, noun = command.split(" ", 1)
        
        for word in noun.split():
            if word in ARGS:
                noun = word
                break
                
    else:
        verb, noun = command, None

    if verb in CMDS:
        action = CMDS[verb]
    else:
        return "unknown command", False

    


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
