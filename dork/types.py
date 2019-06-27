# -*- coding: utf-8 -*-
"""Basic entity classes and methods for Dork.
"""

__all__ = ["Item", "Holder", "Player", "Room", "Worldmap"]


class Game:
    """A container for holding a game state"""

    def __init__(self, player, worldmap):
        self.player = player
        self.worldmap = worldmap


class Item:
    """A obtainable/holdable item
    """

    def __init__(self, name, capacity=0):
        self.name = name
        self.holder = Holder()
        self.capacity = capacity


class Holder:
    """A holder/container of items
    """

    def __init__(self):
        self.items = dict()


class Player(Holder):
    """A player or NPC in the game
    """

    def __init__(self, name, start):
        super(Player, self).__init__()
        self.name = name
        self.current_room = start
        self.inventory = Holder()
        self.equipped = None


class Room(Holder):
    """A room on the map
    """

    def __init__(self, room, name):
        super(Room, self).__init__()
        self.name = name
        self.adjacent = room.get("adjacent", None)
        self.description = room.get("description", None)
        self.players = room.get("players", None)
        self.items = room.get("items", None)
        self.clues = room.get("clues", None)


class Worldmap:
    """A map relating the rooms connectivity
        as well as the players/items within
    """

    def __init__(self):
        self.rooms = dict()
