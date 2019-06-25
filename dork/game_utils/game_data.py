"""Data and commands for REPL"""
from functools import partial
import dork.types as dork_types
import dork.game_utils.map_generator as map_gen


__all__ = ["CMDS", "MOVES", "ERRS", "META"]


GAME_STATE = None


class Game:
    """A container for holding a game state"""

    def __init__(self, **kwargs):
        if not kwargs:
            self.player = dork_types.Player()
            self.worldmap = dork_types.Map()
        else:
            self.player = kwargs["player"]
            self.worldmap = kwargs["map"]


def __initialize():
    # Check if save file is present in .\saves
    # If no save game present, game_instance = __new_game()
    # Else ask for desired save game, game_instance = __load_game()
    # global GAME_STATE = game_instance
    return "Oops, you found a stub!", False


# for testing purposes only, DO NOT SHIP WITH GAME
def __gtfo():
    return "rude!", True


def __new_game():
    # Prompt user for player name
    # game = Game(player=player_name, map=default)
    # Save game to new save file
    # return game
    return "Oops, you found a stub!", False


def __load_map():
    # THIS WILL DESTROY THE CURRENT WORLDMAP, WE PROBABLY SHOULDN'T LET PLAYERS
    # DO THIS CASUALLY; THIS FUNCTION SHOULD ONLY BE ACCESSIBLE THROUGH
    # __new_game() WHEREIN WE CAN LOAD A CUSTOM MAP IF WE DESIRE, NOT JUST
    # RANDOMLY IN THE MIDDLE OF A PLAYTHROUGH
    #
    # Prompt user for file name
    # file_name = str.casefold(input("Please input file name: "))
    # game_map = map_gen.generate_map(file_name)
    # We could get REALLY advanced with this later
    # create an instance of Map using the data found in provided file
    return "Oops, you found a stub!", False


def __load_game():
    # Warn player about unsaved data!
    # if want to save, call __save_game from here
    # Prompt user for file_name
    # game = game_loader(file_name)
    return "Oops, you found a stub!", False


def __save_game():
    return "Oops, you found a stub!", False

def __zork():
    return "Oh shit, you found an easter egg!", False


def __repl_error(arg):
    """return various errors"""
    return f"{arg}", False


def _inventory():
    return "Oops, you found a stub!", False


def _move(cardinal):
    global GAME_STATE
    player = GAME_STATE.player
    worldmap = GAME_STATE.worldmap

    adjacent_room = player.current_room.adjacent[cardinal]
    move_allowed = adjacent_room[1]
    if move_allowed:
        player.previous_room = player.current_room
        player.current_room = worldmap.rooms[adjacent_room[0]]
        out = (player.current_room["description"], False)
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
    "go": MOVES,
    "move": MOVES,
    "walk": MOVES,
    "travel": MOVES,
    "run": MOVES,
    "i": _inventory,
    "inv": _inventory,
    "inventory": _inventory
}


ERRS = {
    "u": partial(__repl_error, "Sorry, I don't know that one."),
    "?": partial(__repl_error, "Huh? Can you speak up?")
}


META = {
    ".init": __initialize,
    ".load": __load_game,
    ".map": __load_map,
    ".new": __new_game,
    ".save": __save_game,
    ".rq": __gtfo,
    ".z": __zork
}
