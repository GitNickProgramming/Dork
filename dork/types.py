# -*- coding: utf-8 -*-
"""Basic entity classes and methods for Dork.
"""
import dork.game_utils.world_loader as world_loader


__all__ = ["Item", "Holder", "Player", "Room", "Worldmap"]


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


class Holder:
    """A holder/container of items
    """
    def __init__(self):
        self.items = dict()


class Player(Holder):
    """A player or NPC in the game
    """
    def __init__(self):
        super().__init__()
        self.name = None
        self.location = None
        self.equipped = None

    def make(self, player, location):
        """Make a player
        """
        self.name = player["name"]
        self.equipped = player["equipped"]
        self.location = location
        for item in player["inventory"]:
            new_item = Item()
            new_item.make(item)
            self.items[new_item.name] = new_item


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
    def make(self, room):
        """Make a room
        """
        self.name = room["name"]
        self.description = room["description"]
        self.adjacent = room["adjacent"]
        self.clues = room["clues"]
        for item in room["items"]:
            new_item = Item()
            new_item.make(item)
            self.items[new_item.name] = new_item
        for player in room["players"]:
            new_player = Player()
            new_player.make(player, self)
            self.players[new_player.name] = new_player


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
        self.hero = Player()

    def _reset(self):
        self.__init__()

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

    def _build_game(self):
        player_name = input("What's your name, stranger? ")
        data = world_loader.main(player_name)
        self._build_world(rooms=data["rooms"], hero=player_name)

    def _build_world(self, rooms, hero):
        for room in rooms:
            new_room = Room()
            new_room.make(room)
            self.worldmap.rooms[new_room.name] = new_room
            self.hero = self.worldmap.players["hero"]
            if self.hero.name is None:
                self.hero.name = hero
