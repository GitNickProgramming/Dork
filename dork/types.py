# -*- coding: utf-8 -*-
"""Basic entity classes and methods for Dork.
"""


__all__ = ["Item", "Holder", "Player", "Room", "Worldmap"]


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


class Player:
    """A player or NPC in the game
    """

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.inventory = dict()
        self.equipped = None


class Room:
    """A room on the map
    """

    def __init__(self, room, name):
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

    def __init__(self, rooms=None):
        self.rooms = dict()
        for room in rooms:
            self.rooms[room] = Room(room=rooms[room], name=room)


class Game:
    """A container for holding a game state"""

    def __init__(self, data, player_name):
        rooms = data.get("rooms", None)
        players = data.get("players", None)
        self.players = dict()
        self.worldmap = Worldmap(rooms)
        for player in players:
            new_player_name = players[player]["name"]
            new_player_location = players[player]["location"]
            self.players[player] = Player(
                name=new_player_name,
                location=self.worldmap.rooms[new_player_location],
            )
        self.hero = self.players.get("hero", None)
        if self.hero.name is None:
            self.hero.name = player_name
