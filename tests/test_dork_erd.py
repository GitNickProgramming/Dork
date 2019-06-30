# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
import dork.types
from tests.utils import is_a


def test_game_exist():
    """the dork module should define a Game
    """
    assert "Game" in vars(dork.types)
    is_a(dork.types.Game, type)


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


def test_room_has_many_players(room):
    """A Room should have many players
    """
    has_many(clazz=room, obj_key="players")


def test_player_has_many_items(player):
    """A Player should have many items
    """
    has_many(clazz=player, obj_key="items")


def test_room_has_many_items(room):
    """A Room should have many items
    """
    has_many(clazz=room, obj_key="items")


def test_worldmap_has_many_rooms(worldmap):
    """A Worldmap should have many Rooms
    """
    has_many(clazz=worldmap, obj_key="rooms")


def test_room_has_many_adjacent(room):
    """A Room should have many adjacent rooms
    """
    has_many(clazz=room, obj_key="adjacent")


def test_room_has_many_clues(room):
    """A Room should have many clues
    """
    has_many(clazz=room, obj_key="clues")


def test_player_is_in_room(player):
    """A Player should contain a Room
    """
    assert isinstance(player.location, dork.types.Room)


def test_item_has_many_stats(item):
    """An item should have many stats
    """
    has_many(clazz=item, obj_key="stats")


def test_holder_has_many_items(holder):
    """A Holder should have many items
    """
    has_many(clazz=holder, obj_key="items")
