"""This is the REPL which runs the commands, and this is a lame docstring"""
# from functools import partial
import dork.game_utils.game_data as game_data
import dork.game_utils.world_loader as world_loader


CMDS = game_data.CMDS
MOVES = game_data.MOVES
ERRS = game_data.ERRS
META = game_data.META


def read():
    """get input from CLI"""
    return str.casefold(input("> "))


def evaluate(cmd, game):
    """parse a cmd and run it"""
    cmd = cmd.split()
    if cmd:
        noun, verb = cmd.pop() if len(cmd) > 1 else None, cmd.pop()
        action = CMDS.get(verb, MOVES.get(verb, META.get(verb, ERRS["u"])))
    else:
        action = ERRS["?"]

    if isinstance(action, dict):
        return action.get(noun, ERRS["u"])()
    return action() if not noun else action(noun)


def repl():
    """Read eval print loop
    """
    print("loading...")
    game = world_loader.main()
    print("starting repl...")
    while True:
        action, modifies_game, should_exit = evaluate(cmd=read(), game=game)
        if modifies_game:
            game = action(game=game)
        else:
            action()
        if should_exit:
            break
    print("ending repl...")
