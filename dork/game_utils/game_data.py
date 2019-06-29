"""Data and commands for REPL"""

__all__ = ["CMDS", "MOVES", "ERRS", "META", "TITLE"]

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
    "look": ["_look"],
    "i": ["_inventory"],
    "inv": ["_inventory"],
    "inventory": ["_inventory"],
    # "grab": _take,
    # "take": _take,
    # "add": _take,
    # "loot": _take,
    # "use": _use_item,
    # "activate": _use_item,
    # "drop": _drop_item
}


META = {
    ".new": ["_start_over"],
    ".load": ["_start_over"],
    # ".save":["_save_game"],
    ".rq": ["_gtfo"],
    ".z": ["_zork"],
}


ERRS = {
    "u": ["_repl_error", "Sorry, I don't know that one."],
    "?": ["_repl_error", "Huh? Can you speak up?"],
}
