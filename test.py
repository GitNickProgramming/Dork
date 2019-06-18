from functools import partial
from dork import parser as dparse


def _hello():
    return "hello, world!", False


def _bye():
    return "goodbye, world!", True


def _help():
    return "try typing 'say hello'", False


def _gtfo():
    return "rude!", True


def _move(cardinal):
    return f"You moved to the {cardinal}", False


def read():
    return input("> ")


def evaluate(cmd):
    """parse a command and run it"""

    if " " in cmd:
        verb, noun = cmd.split(" ", 1)
        noun = noun.split()
    else:
        verb, noun = cmd, None

    action = cmds["cmds"][verb]
    args = cmds["args"]

    if noun is not None:
        if isinstance(action, dict):
            for word in noun:
                if word in action:
                    func_to_eval = eval(action[word])
                    return func_to_eval()
        else:
            for word in noun:
                if word in args:
                    func_to_eval = eval(action)
                    return func_to_eval(word)
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
    world_map = dparse.load("map")
    cmds = dparse.load("cmds")
    repl()
