"""This is the REPL which runs the commands, and this is a lame docstring"""
import dork.game_utils.game_data as game_data
import dork.types as dork_types


def read():
    """Get input from CLI
    """
    return str.casefold(input("> "))


def evaluate(cmd, game_instance, repl_data):
    """Parse a cmd and run it
    """
    cmds, moves, meta, errs = repl_data
    cmd = cmd.split()
    if cmd:
        noun, verb = cmd.pop() if len(cmd) > 1 else None, cmd.pop()
        call = cmds.get(verb, moves.get(verb, meta.get(verb, errs["u"])))

        if isinstance(call, dict):
            call = call.get(noun, errs["u"])
    else:
        call = errs["?"]

    method = call[0]
    arg = call[1] if len(call) > 1 else None

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
        print("\n" + " "*4 + output + "\n")
        if should_exit:
            break
    print("shutting down...")
