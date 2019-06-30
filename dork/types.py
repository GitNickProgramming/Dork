# -*- coding: utf-8 -*-
"""Basic entity classes and methods for Dork.
"""
# from pprint import pprint
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

    def make(self, item):
        """Make an item
        """
        self.name = item["name"]
        self.description = item["description"]
        self.stats = item["stats"]


class Player(Holder):
    """A player or NPC in the game
    """
    inventory = dict()
    items = dict()

    def __init__(self):
        super().__init__()
        self.name = None
        self.location = Room()
        self.equipped = None
        self.inventory = dict()
        self.items = self.inventory

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

    def add_item(self, item):
        """adding an item for test purposes"""
        self.inventory[item] = item.name


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
    players = {}
    hero = None
    worldmap = None

    def __init__(self):
        self.worldmap = Worldmap()
        self.players = dict()
        self.hero = Player()
        self.__build_game()

    def __build_game(self):
        """Make a new game
        """
        player_name = input("What's your name, stranger? ")
        data = world_loader.main(player_name)
        self.__build_players(players=data["players"])
        self.__build_world(rooms=data["rooms"])
        self.__build_hero(hero=player_name)

    def __build_players(self, players):
        for player in players:
            new_player = Player()
            new_player.make(players[player])
            self.players[new_player.name] = new_player

    def __build_world(self, rooms):
        self.worldmap.players = self.players
        for room in rooms:
            new_room = Room()
            new_room.make(rooms[room], self.players)
            self.worldmap.rooms[new_room.name] = new_room

    def __build_hero(self, hero):
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
        if item_count == 0.:
            out = " "*4 + "You ain't got shit, son!"
        return out, False

    def get_inventory(self):
        """public method call for inventory"""
        return self._inventory()

    def _look(self):
        return self.hero.location.description, False

    def get_look(self):
        """public method call for look"""
        return self._look()

    # def _save_game(self):
    #     world_writer.main(self)
    #     return "Save successful!", False

    # def _take(self, item="all"):
    #     # Item defaults to "all", and adds all items in room to inventory
    #     return "You took the thing. You took it well.", False

    # def _drop_item(self, item):
    #     return "Oops, you dropped something!", False

    # def _use_item(self, item):
    #     return "You used the thing! It's super effective!", False

    def _start_over(self, load_or_save):
        if self._confirm():
            self.__build_game()
            out = load_or_save
        else:
            out = "Guess you changed your mind!"
        return out, False

    def get_start_over(self, load_or_save):
        """public method call for start over"""
        return self._start_over(load_or_save)

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

    def get_confirm(self):
        """public method call for confirm"""
        return self._confirm()

    @staticmethod
    def _zork():
        return "Oh shit, you found an easter egg!", False

    @staticmethod
    def _repl_error(arg):
        return f"{arg}", False
