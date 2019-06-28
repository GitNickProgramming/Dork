# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
from tests.utils import has_a, is_a


def test_game_attributes(game):
    """the game should have attributes
    """
    has_a(game, "player")
    has_a(game, "worldmap")


def test_room_attributes(room):
    """the room should have attributes
    """

    has_a(room, "name")
    has_a(room, "adjacent")
    has_a(room, "description")
    has_a(room, "players")
    has_a(room, "items")
    has_a(room, "clues")


def test_player_attributes(player):
    """the player should have attributes
    """

    has_a(player, "name")
    has_a(player, "current_room")
    has_a(player, "inventory")
    has_a(player, "equipped")


def test_item_attributes(item):
    """item should have holder and capacity
    """

    has_a(item, "holder")
    has_a(item, "capacity")


def test_holder_attributes(holder):
    """holder should have items
    """

    has_a(holder, "items")


def test_worldmap_attributes(worldmap):
    """the worldmap should have a dict of rooms
    """

    has_a(worldmap, "rooms")
