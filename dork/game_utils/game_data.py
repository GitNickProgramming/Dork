"""Data and commands for REPL"""
from functools import partial
import dork.game_utils.world_loader as world_loader
# import dork.game_utils.world_writer as world_writer


class REPL:
    """REPL object to hold and modify an instance of Game"""

    def __init__(self):
        self._reset()
    def _reset(self, new_game=True):
        self._game = world_loader.main(new_game)

    @staticmethod
    def _gtfo():
        return "rude!", True

    @staticmethod
    def _zork():
        return "Oh shit, you found an easter egg!", False

    @staticmethod
    def _repl_error(arg):
        return f"{arg}", False

    @staticmethod
    def _confirm():
        print("WARNING: you will lose any unsaved data!")
        conf = False
        while True:
            conf = str.casefold(input("Would you like to proceed? Y/N: "))
            conf = {
                "y": True,
                "n": False
            }.get(conf, None)
            if not conf:
                print("That is not a valid response!")
            else:
                break
        return conf

    def _new_game(self):
        if self._confirm():
            self._reset()
        return "", False

    def _load_game(self):
        if self._confirm():
            self._reset(new_game=False)
        return "", False

    # def _save_game(self):
    #     world_writer(self.game)
    #     return "Save successful!", False

    # def _inventory(self):
    #     return self.game.player.inventory, False

    # def _take(self, item="all"):
    #     # Item defaults to "all", and adds all items in room to inventory
    #     return "You took the thing. You took it well.", False

    # def _drop_item(self, item):
    #     return "Oops, you dropped something!", False

    # def _use_item(self, item):
    #     return "You used the thing! It's super effective!", False

    def _move(self, cardinal):
        worldmap = self._game.worldmap.rooms
        player = self._game.player
        current_room = player.current_room
        adjacent_room = current_room.adjacent
        if not adjacent_room:
            out = f"You cannot go {cardinal} from here."
        else:
            player.current_room = worldmap[current_room.adjacent[cardinal]]
            print(player.current_room.description)
            out = f"You moved to the {cardinal}! Good job!"
        return out, False

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
        # "i": _inventory,
        # "inv": _inventory,
        # "inventory": _inventory,
        # "grab": _take,
        # "take": _take,
        # "add": _take,
        # "use": _use_item,
        # "activate": _use_item,
        # "drop": _drop_item
    }

    META = {
        ".new": _new_game,
        ".load": _load_game,
        # ".save": _save_game,
        ".rq": _gtfo,
        ".z": _zork
    }

    ERRS = {
        "u": partial(_repl_error, arg="Sorry, I don't know that one."),
        "?": partial(_repl_error, arg="Huh? Can you speak up?")
    }
