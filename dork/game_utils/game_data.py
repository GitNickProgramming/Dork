"""Data and commands for REPL"""
from functools import partial
import dork.game_utils.world_loader as world_loader


__all__ = ["CMDS", "MOVES", "ERRS", "META"]


# for testing purposes only, DO NOT SHIP WITH GAME
def _gtfo():
    return "rude!", False, True


def _zork():
    return "Oh shit, you found an easter egg!", False, False


def _repl_error(**kwargs):
    """return various errors"""
    return f"{kwargs['arg']}", False, False


def _new_game(**kwargs):
    return world_loader.main(), True, False


def _load_game(**kwargs):
    return world_loader.main(new_game=False), True, False


def _save_game(**kwargs):
    return "Your secret is safe with me...", True, False


def _inventory(**kwargs):
    return "Look at all this stuff!", True, False


def _take(**kwargs): #_take(item="all")
    # Item defaults to "all", and adds all items in room to inventory
    return "You took the thing. You took it well.", True, False


def _drop_item(**kwargs):
    return "Oops, you dropped something!", True, False


def _use_item(**kwargs):
    return "You used the thing! It's super effective!", True, False


def _move(**kwargs):
    return f"You moved to the {kwargs['cardinal']}! Good job!", True, False


MOVES = {
    "n": partial(_move, cardinal="north"),
    "s": partial(_move, cardinal="south"),
    "e": partial(_move, cardinal="east"),
    "w": partial(_move, cardinal="west"),
    "north": partial(_move, cardinal="north"),
    "south": partial(_move, cardinal="south"),
    "east": partial(_move, cardinal="east"),
    "west": partial(_move, cardinal="west")
}


CMDS = {
    "go": MOVES,
    "move": MOVES,
    "walk": MOVES,
    "travel": MOVES,
    "run": MOVES,
    "i": _inventory,
    "inv": _inventory,
    "inventory": _inventory,
    "grab": _take,
    "take": _take,
    "add": _take,
    "use": _use_item,
    "activate": _use_item,
    "drop": _drop_item
}


META = {
    ".new": _new_game,
    ".load": _load_game,
    ".save": _save_game,
    ".rq": _gtfo,
    ".z": _zork
}


ERRS = {
    "u": partial(_repl_error, arg="Sorry, I don't know that one."),
    "?": partial(_repl_error, arg="Huh? Can you speak up?")
}
