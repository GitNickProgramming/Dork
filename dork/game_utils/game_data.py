"""Data and commands for REPL"""
from functools import partial
import dork.types as dork_types
import dork.game_utils.map_generator as map_gen


__all__ = ["CMDS", "MOVES", "ERRS", "META"]


GAME_STATE = None


def __initialize():
    # Check if save file is present in .\saves
    # If no save game present, game_instance = __new_game()
    # Else ask for desired save game, game_instance = __load_game()
    # global GAME_STATE = game_instance
    return "You definitely shouldn't be in here, this is a secret command.", False


# for testing purposes only, DO NOT SHIP WITH GAME
def __gtfo():
    return "rude!", True


def __new_game():
    # Prompt user for player name
    # game = Game(player=player_name, map=default)
    # Save game to new save file
    # return game
    return "I wish I could start over...", False


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
    return "You have successfully fast traveled to another planet.", False


def __load_game():
    # Warn player about unsaved data!
    # if want to save, call __save_game from here
    # Prompt user for file_name
    # game = game_loader(file_name)
    return "LOAD THIS!", False


def __save_game():
    return "Your secret is safe with me...", False

def __zork():
    return "Oh shit, you found an easter egg!", False


def __repl_error(arg):
    """return various errors"""
    return f"{arg}", False


def _inventory():
    return "Look at all this stuff!", False


def _drop_item():
    return "Oops, you dropped something!", False


def _use_item():
    return "You used the thing! It's super effective!", False


def _move(cardinal):
    # global GAME_STATE
    # player = GAME_STATE.player
    # worldmap = GAME_STATE.worldmap

    # adjacent_room = player.current_room.adjacent[cardinal]
    # move_allowed = adjacent_room[1]
    # if move_allowed:
    #     previous_room = player.current_room
    #     player.current_room = worldmap.rooms[adjacent_room[0]]
    #     out = (player.current_room["description"], False)
    # else:
    #     out = ("You cannot go that way", False)
    # return out
    return f"You moved to the {cardinal}! Good job!", False


def _take(): #_take(item="all")
    # Item defaults to "all", and adds all items in room to inventory
    return "You took the thing. You took it well.", False


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
    "inventory": _inventory,
    "grab": _take,
    "take": _take,
    "add": _take,
    "use": _use_item,
    "activate": _use_item,
    "drop": _drop_item
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


ERRS = {
    "u": partial(__repl_error, "Sorry, I don't know that one."),
    "?": partial(__repl_error, "Huh? Can you speak up?")
}
