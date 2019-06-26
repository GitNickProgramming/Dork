"""This is the REPL which runs the commands, and this is a lame docstring"""
# from functools import partial
import dork.game_utils.game_data as game_data


REPL_INSTANCE = game_data.REPL()
TITLE = game_data.TITLE
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
        instruction = CMDS.get(verb, MOVES.get(verb, META.get(verb, ERRS["u"])))
        if isinstance(instruction, dict):
            instruction = instruction.get(noun, ERRS["u"])
    else:
        instruction = ERRS["?"]

    method = instruction[0]
    arg = instruction[1] if len(instruction) > 1 else None

    if not arg:
        return getattr(REPL_INSTANCE, method)()
    return getattr(REPL_INSTANCE, method)(arg)


def repl():
    """Read eval print loop
    """
    print(f"\n\nGreetings, {REPL_INSTANCE.name}! " + TITLE + "\n\n")
    while True:
        output, should_exit = evaluate(read())
        print(output)
        if should_exit:
            break
    print("ending repl...")
