"""This is the REPL which runs the commands, and this is a lame docstring"""
import dork.game_utils.game_data as game_data


def read():
    """get input from CLI"""
    return str.casefold(input("> "))


def evaluate(cmd, repl_instance, repl_data):
    """parse a cmd and run it"""
    cmds, moves, meta, errs = repl_data
    cmd = cmd.split()
    if cmd:
        noun, verb = cmd.pop() if len(cmd) > 1 else None, cmd.pop()
        instruction = cmds.get(verb, moves.get(verb, meta.get(verb, errs["u"])))
        if isinstance(instruction, dict):
            instruction = instruction.get(noun, errs["u"])
    else:
        instruction = errs["?"]

    method = instruction[0]
    arg = instruction[1] if len(instruction) > 1 else None

    if not arg:
        return getattr(repl_instance, method)()
    return getattr(repl_instance, method)(arg)


def repl():
    """Read eval print loop
    """
    repl_instance = game_data.Hero()
    repl_data = (
        game_data.CMDS,
        game_data.MOVES,
        game_data.META,
        game_data.ERRS
    )
    print(f"\nGreetings, {repl_instance.name}! " + game_data.TITLE + "\n")
    while True:
        output, should_exit = evaluate(
            cmd=read(), repl_instance=repl_instance, repl_data=repl_data
        )
        print(output + "\n")
        if should_exit:
            break
    print("Until next time!")
