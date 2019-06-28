"""Data and commands for REPL"""
import dork.types as dork_types
import dork.game_utils.world_loader as world_loader
# import dork.game_utils.world_writer as world_writer


__all__ = ["CMDS", "MOVES", "ERRS", "META", "TITLE"]


class Hero:
    """Holds an instance of Game and modifies its state"""

    def __init__(self):
        self._reset()
    def _reset(self):
        player_name = input("What's your name, stranger? ")
        data = world_loader.main(player_name)
        self.game = dork_types.Game(data=data, player_name=player_name)
        self.name = self.game.hero.name

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
        print("\n!!!WARNING!!! You will lose unsaved data!\n")
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

    def _make_game(self):
        if self._confirm():
            self._reset()
        return "", False

    def _move(self, cardinal):
        hero = self.game.hero
        location = hero.location
        adjacent_room = location.adjacent.get(cardinal, None)
        if not adjacent_room:
            out = f"You cannot go {cardinal} from here."
        else:
            hero.location = self.game.worldmap.rooms[adjacent_room]
            print(f"You have entered {hero.location.name}")
            out = hero.location.description
        return out, False

    # def _save_game(self):
    #     world_writer.main(self.game)
    #     return "Save successful!", False

    # def _inventory(self):
    #     return self.game.hero.inventory, False

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
    "head": MOVES,
    # "look": _look,
    # "i": _inventory,
    # "inv": _inventory,
    # "inventory": _inventory,
    # "grab": _take,
    # "take": _take,
    # "add": _take,
    # "loot": _take,
    # "use": _use_item,
    # "activate": _use_item,
    # "drop": _drop_item
}


META = {
    ".new": ["_make_game"],
    ".load": ["_make_game"],
    # ".save":[" _save_game"],
    ".rq": ["_gtfo"],
    ".z": ["_zork"]
}


ERRS = {
    "u": ["_repl_error", "Sorry, I don't know that one."],
    "?": ["_repl_error", "Huh? Can you speak up?"]
}
