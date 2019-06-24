"""Data and commands for REPL"""
from functools import partial
# import dork.types as dork_types
import dork.repl as dork_
import dork.map_utils.map_generator as map_gen


__all__ = ["CMDS", "MOVES"]


PLAYER, WORLDMAP = dork_.GAME


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
    file_name = str.casefold(input("Please input file name: "))
    game_map = map_gen.generate_map(file_name)
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
    adjacent_room = PLAYER.current_room.adjacent[cardinal]
    move_allowed = adjacent_room[1]
    if move_allowed:
        PLAYER.previous_room = PLAYER.current_room
        PLAYER.current_room = WORLDMAP.rooms[adjacent_room[0]]
        out = (PLAYER.current_room["description"], False)
    else:
        out = ("You cannot go that way", False)
    return out


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
    "quit": _gtfo,
    "exit": _gtfo,
    "go": MOVES,
    "move": MOVES,
    "walk": MOVES,
    "travel": MOVES,
    "run": MOVES
}
