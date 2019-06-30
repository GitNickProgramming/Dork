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
