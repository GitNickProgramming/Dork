# -*- coding: utf-8 -*-
"""Basic entity classes and methods for Dork.
"""

__all__ = ["Item", "Holder", "Player", "Room", "WorldMap"]


class Game:
    """A container for holding a game state"""

    def __init__(self, player, worldmap):
        self.player = player
        self.worldmap = worldmap


class Item:
    """A obtainable/holdable item
    """

    def __init__(self, capacity=0):
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

    def __init__(self, **kwargs):
        super(Player, self).__init__()
        self.name = kwargs["name"]
        self.current_room = kwargs["start"]
        self.inventory = Holder()
        self.equipped = None


class Room(Holder):
    """A room on the map
    """

    def __init__(self, **kwargs):
        super(Room, self).__init__()
        self.adjacent = kwargs["adjacent"]
        self.description = kwargs["description"]
        self.npcs = kwargs["npcs"]
        self.items = kwargs["items"]
        self.clues = kwargs["clues"]


class WorldMap:
    """A map relating the rooms connectivity
        as well as the players/items within
    """

    def __init__(self):
        self.rooms = dict()
