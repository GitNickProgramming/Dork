from functools import partial
import yaml_to_dict as parse


def _hello():
    return "hello, world!", False


def _bye():
    return "goodbye, world!", True


def _help():
    return "try typing 'say hello'", False


def _gtfo():
    return "rude!", True


def _move(cardinal):
    if len(cardinal) == 1:
        cardinal = {"n": "north", "s": "south", "e": "east", "w": "west"}[cardinal]
    return f"You moved to the {cardinal}", False


def read():
    """get input from CLI"""
    return input("> ")


def evaluate(cmd):
    """parse a command and run it"""

    if " " in cmd:
        verb, noun = cmd.split(" ", 1)
        noun = noun.split()
    else:
        verb, noun = cmd, None

    if verb in CMDS["cmds"]:
        action = CMDS["cmds"][verb]
        args = CMDS["args"]
    else:
        return "unknown command", False

    if noun:
        for word in noun:
            if word in action:
                func_to_eval = eval(action[word])
            elif word in args:
                func_to_eval = partial(eval(action), word)
            return func_to_eval()
    else:
        func_to_eval = eval(action)
        return func_to_eval()


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


# https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    WORLD_MAP = parse.load("map")
    CMDS = parse.load("cmds")
    repl()
