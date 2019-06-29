# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
import dork.types
from tests.utils import has_many, is_a


def test_game_exist():
    """the dork module should define a Game
    """
    assert "Game" in vars(dork.types)
    is_a(dork.types.Game, type)


# def test_game_attributes():
#     """the Game needs attributes
#     """
#     player = dork.types.Player
#     assert dork.types.Game.player == player


def test_items_exist():
    """the dork module should define an Item
    """
    assert "Item" in vars(dork.types)
    is_a(dork.types.Item, type)


def test_holders_exist():
    """the dork module should define an Holder
    """
    assert "Holder" in vars(dork.types)
    is_a(dork.types.Holder, type)


def test_players_exist():
    """the dork module should define an Player
    """
    assert "Player" in vars(dork.types)
    is_a(dork.types.Player, type)


def test_rooms_exist():
    """the dork module should define an Room
    """
    assert "Room" in vars(dork.types)
    is_a(dork.types.Room, type)


def test_map_exists():
    """the dork module should define a Worldmap
    """
    assert "Worldmap" in vars(dork.types)
    is_a(dork.types.Worldmap, type)


# def test_holder_has_many_items():
#     """A Holder should have many Items
#     """
#     has_many(dork.types.Holder, "holder", dork.types.Item, "items")


# def test_game_elements(player):
#     """A Holder should have many Items
#     """
#     has_many(dork.types.Player, "inventory", dork.types.Holder, "holder")


# def test_map_exists():
#     """the dork module should define an Map
#     """
#     assert "WorldMap" in vars(dork.types)
#     is_a(dork.types.WorldMap, type)


def test_room_has_many_players():
    """A Room should have many players
    """
    has_many(dork.types.Room, "location", "players")


def test_map_has_many_rooms(worldmap):
    """A Map should have many Rooms
    """
    has_many(worldmap, "Worldmap", "rooms")
