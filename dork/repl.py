"""This is the REPL which runs the commands, and this is a lame docstring"""
import dork.game_utils.game_data as game_data
import dork.types as dork_types


def read():
    """get input from CLI"""
    return str.casefold(input("> "))


def evaluate(cmd, game_instance, repl_data):
    """parse a cmd and run it"""
    cmds, moves, meta, errs = repl_data
    cmd = cmd.split()
    if cmd:
        noun, verb = cmd.pop() if len(cmd) > 1 else None, cmd.pop()
<<<<<<< HEAD
        instruction = cmds.get(verb, moves.get(
            verb, meta.get(verb, errs["u"])))
=======
        instruction = cmds.get(
            verb, moves.get(
                verb, meta.get(
                    verb, errs["u"])))
>>>>>>> 611451d9783fd45d7d397675dffd023fcb048680
        if isinstance(instruction, dict):
            instruction = instruction.get(noun, errs["u"])
    else:
        instruction = errs["?"]

    method = instruction[0]
    arg = instruction[1] if len(instruction) > 1 else None

    if not arg:
        return getattr(game_instance, method)()
    return getattr(game_instance, method)(arg)


def repl():
    """Read eval print loop
    """
    game_instance = dork_types.Game()
    game_instance.build()
    repl_data = (
        game_data.CMDS,
        game_data.MOVES,
        game_data.META,
        game_data.ERRS
    )
    print(f"\nGreetings, {game_instance.hero.name}! " + game_data.TITLE + "\n")
    while True:
        output, should_exit = evaluate(
            cmd=read(), game_instance=game_instance, repl_data=repl_data
        )
        print("\n" + output + "\n")
        if should_exit:
            break
    print("shutting down...")
