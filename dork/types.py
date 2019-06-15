# -*- coding: utf-8 -*-
"""Basic entity classes and methods for Dork.
"""

__all__ = ["Item", "Holder", "Player", "Room", "Path", "Map"]


class Item:
    """A obtainable/holdable item
    """

    def __init__(self):
        self.holder = Holder()


class Holder:
    """A holder/container of items
    """

    def __init__(self):
        self.items = list()


class Player(Holder):
    """A player or NPC in the game
    """

    def __init__(self):
        super(Player, self).__init__()
        self.room = Room()
        self.prev_loc = None


class Room(Holder):
    """A room on the map

    Note: can only be entered through entraces
        or exited through exits.
    """

    def __init__(self):
        super(Room, self).__init__()
        self.map = Map()
        self.entrances = list()
        self.exits = list()
        self.players = list()


class Path:
    """A path between two rooms (i.e. a door or hallway)
    """

    def __init__(self):
        self.entrance = Room()
        self.exit = Room()


class Map:
    """A map relating the rooms connectivity
        as well as the players/items within
    """

    def __init__(self):
        self.rooms = list()
