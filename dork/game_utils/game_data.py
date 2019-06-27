"""Data and commands for REPL"""
import dork.game_utils.world_loader as world_loader
# import dork.game_utils.world_writer as world_writer


__all__ = ["CMDS", "MOVES", "ERRS", "META", "TITLE"]


class REPL:
    """REPL object to hold and modify an instance of Game"""

    def __init__(self):
        self._reset()
    def _reset(self, new_game=True):
        self.game = world_loader.main(new_game)
        self.name = self.game.player.name

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
            if conf is None:
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

    def _move(self, cardinal):
        worldmap = self.game.worldmap
        player = self.game.player
        current_room = player.current_room
        adjacent_room = current_room.adjacent.get(cardinal, None)
        if not adjacent_room:
            out = f"You cannot go {cardinal} from here."
        else:
            player.current_room = worldmap.rooms[adjacent_room]
            print(f"You have entered {player.current_room.name}")
            out = player.current_room.description
        return out, False

    # def _save_game(self):
    #     world_writer.main(self.game)
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


TITLE = r"""Welcome to...

__/\\\\\\\\\\\\__________/\\\\\_________/\\\\\\\\\______/\\\________/\\\_
 _\/\\\////////\\\______/\\\///\\\_____/\\\///////\\\___\/\\\_____/\\\//__
  _\/\\\______\//\\\___/\\\/__\///\\\__\/\\\_____\/\\\___\/\\\__/\\\//_____
   _\/\\\_______\/\\\__/\\\______\//\\\_\/\\\\\\\\\\\/____\/\\\\\\//\\\_____
    _\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\//////\\\____\/\\\//_\//\\\____
     _\/\\\_______\/\\\_\//\\\______/\\\__\/\\\____\//\\\___\/\\\____\//\\\___
      _\/\\\_______/\\\___\///\\\__/\\\____\/\\\_____\//\\\__\/\\\_____\//\\\__
       _\/\\\\\\\\\\\\/______\///\\\\\/_____\/\\\______\//\\\_\/\\\______\//\\\_
        _\////////////__________\/////_______\///________\///__\///________\///__

...A game of mystery and intrigue, but most importantly, memes!"""


MOVES = {
    "n": ["_move", "north"],
    "s": ["_move", "south"],
    "e": ["_move", "east"],
    "w": ["_move", "west"],
    "north": ["_move", "north"],
    "south": ["_move", "south"],
    "east": ["_move", "east"],
    "west": ["_move", "west"]
}


CMDS = {
    "go": MOVES,
    "move": MOVES,
    "walk": MOVES,
    "travel": MOVES,
    "run": MOVES,
    "head": MOVES
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
    ".new": ["_new_game"],
    ".load": ["_load_game"],
    # ".save":[" _save_game"],
    ".rq": ["_gtfo"],
    ".z": ["_zork"]
}


ERRS = {
    "u": ["_repl_error", "Sorry, I don't know that one."],
    "?": ["_repl_error", "Huh? Can you speak up?"]
}
