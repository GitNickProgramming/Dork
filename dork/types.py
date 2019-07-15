# -*- coding: utf-8 -*-
"""Basic entity classes and methods for Dork.
"""
# from pprint import pprint
from abc import ABC, abstractmethod
import dork.game_utils.world_loader as world_loader


__all__ = ["Game"]


class Holder:
    """A holder/container of items
    """

    def __init__(self):
        self.items = dict()


class Item:
    """A obtainable/holdable item
    """

    def __init__(self):
        self.name = None
        self.description = None
        self.stats = dict()
        self.usable = NotUsable

    def make(self, item):
        """Make an item
        """
        self.name = item["name"]
        self.description = item["description"]
        self.stats = item["stats"]
        if self.stats is None:
            self.usable = NotUsable

        elif len(self.stats) > 1:
            self.set_usable(self.stats[1])
        else:
            self.usable = NotUsable

    def set_usable(self, new_use):
        """This method changes the use behavior,
        provide usable class as argument"""
        uses = {"attack": Attackable, "key": Openable,
                "gold": Payable,
                "emerald" or "diamond": Puzzleable,
                "speed" or "strength": Statable}
        if new_use is None or new_use not in uses:
            self.usable = NotUsable
        else:
            self.usable = uses[new_use]

    def use(self, target, name):
        """Strategy pattern call"""
        self.usable.use(target, name)


class Usable(ABC):
    """Abstract class of use behavior in items use method"""

    @staticmethod
    @abstractmethod
    def use(target, name):
        """Strategy pattern inspired by refactoring.guru
        use method defaults to doing nothing"""


class Attackable(Usable):
    """Any object that can be swung will say it was swung"""

    @staticmethod
    def use(target, name):
        """Swing use method"""
        print("You swing the " + name + " at " + target)


class NotUsable(Usable):
    """Any object that cannot be used"""

    @staticmethod
    def use(target, name):
        """Useless use method"""
        print("You find no use of this item")


class Openable(Usable):
    """Object opening behavior class"""

    @staticmethod
    def use(target, name):
        """Opens object targeted if possible"""
        print("You insert the " + name + " into " + target)


class Payable(Usable):
    """Any object that can be used as gold"""

    @staticmethod
    def use(target, name):
        """Gold use method"""
        print("You use the " + name + " to pay " + target)


class Puzzleable(Usable):
    """Any object that can be used in a puzzle"""

    @staticmethod
    def use(target, name):
        """Puzzle use method"""
        print("You try to fit the " + name + " into the " + target)


class Statable(Usable):
    """Any object that can change stats"""

    @staticmethod
    def use(target, name):
        """Stat change use method"""
        print("The " + name + " takes effect on " + target)


class Player(Holder):
    """A player or NPC in the game
    """

    def __init__(self):
        super().__init__()
        self.name = None
        self.location = Room()
        self.equipped = None

    def make(self, player):
        """Make a player
        """
        self.name = player["name"]
        self.equipped = player["equipped"]
        inventory = player["inventory"]
        for item in inventory:
            if item is not None:
                new_item = Item()
                new_item.make(inventory[item])
                self.items[new_item.name] = new_item

    def set_location(self, location):
        """Set player's location
        """
        self.location = location

    def get_location(self):
        """Get Player's location
        """
        return self.location


class Room(Holder):
    """A room on the map
    """

    def __init__(self):
        super().__init__()
        self.name = None
        self.description = None
        self.adjacent = dict()
        self.players = list()
        self.clues = dict()

    def make(self, room, players):
        """Make a room
        """
        self.name = room["name"]
        self.description = room["description"]
        self.adjacent = room["adjacent"]
        self.clues = room["clues"]
        items = room["items"]
        for item in items:
            new_item = Item()
            new_item.make(items[item])
            self.items[new_item.name] = new_item
        for player in players:
            if players[player].name in room["players"]:
                self.players.append(players[player])
                players[player].location = self


class Worldmap:
    """A map relating the rooms connectivity
        as well as the players/items within
    """

    def __init__(self):
        self.rooms = dict()
        self.players = dict()


class Game:
    """A container for holding a game state
    """

    def __init__(self):
        self.worldmap = Worldmap()
        self.players = dict()
        self.hero = Player()

    def __call__(self, cmd, arg):
        return getattr(self, cmd)(arg) if arg else getattr(self, cmd)()

    def build(self):
        """Make a new game
        """
        player_name = input("What's your name, stranger? ")
        data = world_loader.main(player_name)
        self._build_players(players=data["players"])
        self._build_world(rooms=data["rooms"])
        self._build_hero(hero=player_name)

    def _build_players(self, players):
        for player in players:
            new_player = Player()
            new_player.make(players[player])
            self.players[new_player.name] = new_player

    def _build_world(self, rooms):
        self.worldmap.players = self.players
        for room in rooms:
            new_room = Room()
            new_room.make(rooms[room], self.players)
            self.worldmap.rooms[new_room.name] = new_room

    def _build_hero(self, hero):
        self.hero = self.players.get(
            hero, self.players.get("new_player")
        )
        self.hero.name = hero

    def _gtfo(self):
        return f"Thanks for playing DORK, {self.hero.name}!", True

    def _move(self, cardinal):
        location = self.hero.get_location()
        adjacent_room = location.adjacent.get(cardinal, None)
        if not adjacent_room:
            out = f"You cannot go {cardinal} from here."
        else:
            self.hero.set_location(self.worldmap.rooms[adjacent_room])
            print(f"You have entered {self.hero.location.name}")
            out = self.hero.location.description
        return out, False

    def _inventory(self):
        items = self.hero.items
        item_count = 0
        out = "Inventory:\n"
        for item in items:
            if item is not None:
                out += "\n" + " "*4 + items[item].name
                item_count += 1
        if item_count == 0:
            out = " "*4 + "You ain't got shit, son!"
        return out, False

    def _look(self):
        return self.hero.location.description, False

    # def _save_game(self):
    #     world_writer.main(self)
    #     return "Save successful!", False

    # def _take(self, item="all"):
    #     # Item defaults to "all", and adds all items in room to inventory
    #     return "You took the thing. You took it well.", False

    # def _drop_item(self, item):
    #     return "Oops, you dropped something!", False

    def _use_item(self, item):
        if item in self.hero.items.keys():
            target = input("What do you want to use it on? ")
            self.hero.items[item].use(target, item)
            return "You used the thing! It's super effective!", False
        return "You don't have that item...", False

    def _start_over(self, load_or_save):
        if self._confirm():
            self.build()
            out = load_or_save
        else:
            out = "Guess you changed your mind!"
        return out, False

    @staticmethod
    def _confirm():
        print("\n!!!WARNING!!! You will lose unsaved data!\n")
        conf = False
        while True:
            conf = str.casefold(
                input("Would you like to proceed? Y/N: ")
            )
            conf = {
                "y": True,
                "n": False
            }.get(conf, None)
            if conf is None:
                print("That is not a valid response!")
            else:
                break
        return conf

    @staticmethod
    def _zork():
        return "Oh shit, you found an easter egg!", False

    @staticmethod
    def _repl_error(arg):
        return f"{arg}", False
