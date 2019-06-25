# -*- coding: utf-8 -*-
"""Basic entity classes and methods for Dork.
"""

__all__ = ["Item", "Holder", "Player", "Room", "Map"]


class Game:
    """A container for holding a game state"""

    def __init__(self, **kwargs):
        if not kwargs:
            self.state = {
                "player": Player(), "worldmap": Map()
            }
        else:
            self.state = {
                "player": kwargs["player"], "worldmap": kwargs["map"]
            }


class Item:
    """A obtainable/holdable item
    """

    def __init__(self):
        self.holder = Holder()


class Holder:
    """A holder/container of items
    """

    def __init__(self):
        self.items = dict()


class Player(Holder):
    """A player or NPC in the game
    """

    def __init__(self):
        super(Player, self).__init__()
        self.current_room = Room()
        self.previous_room = None


class Room(Holder):
    """A room on the map
    """

    def __init__(self):
        super(Room, self).__init__()
        self.map = Map()
        self.adjacent = dict()
        self.players = dict()
        self.items = dict()


class Map:
    """A map relating the rooms connectivity
        as well as the players/items within
    """

    def __init__(self):
        self.rooms = dict()
