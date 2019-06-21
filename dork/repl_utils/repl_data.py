"""Data and commands for REPL"""
from functools import partial
# from dork.map_utils import map_generator
# import dork.types as dork_types


__all__ = ["CMDS", "ARGS", "MOVES"]


# for testing purposes only, DO NOT SHIP WITH GAME
def _gtfo():
    return "rude!", True


def _new_game():
    # Prompt user for player name
    # Instantiate Player, Map, and Game
    # Immediately save Game to new save file
    return "Oops, you found a stub!", False


def _load_map():
    # Prompt user for file name
    # We could get REALLY advanced with this later
    # create an instance of Map using the data found in provided file
    return "Oops, you found a stub!", False


def _load_game():
    # Warn player about unsaved data!
    # if want to save, call _save_game from here
    # Prompt user for file name
    # Clear game state
    # Restart CLI
    return "Oops, you found a stub!", False


def _save_game():
    return "Oops, you found a stub!", False


def _move(cardinal):
    return f"You moved to the {cardinal}", False


MOVES = {
    "n": partial(_move, "north"),
    "s": partial(_move, "south"),
    "e": partial(_move, "east"),
    "w": partial(_move, "west"),
    "north": partial(_move, "north"),
    "south": partial(_move, "south"),
    "east": partial(_move, "east"),
    "west": partial(_move, "west")
}


CMDS = {
    "load": {
        "map": _load_map,
        "game": _load_game
    },
    "save": _save_game,
    "q": _gtfo,
    "go": MOVES,
    "move": MOVES,
    "walk": MOVES,
    "travel": MOVES,
    "run": MOVES,
    "cartwheel": MOVES,
    "crabwalk": MOVES,
    "crawl": MOVES
}


# this could get hairy
ARGS = [
    "n", "s", "e", "w", "north", "south", "east", "west", "game", "map"
]
