# -*- coding: utf-8 -*-
"""Basic tests for world loader
"""
import dork.game_utils.world_loader as world_loader
from tests.utils import is_a


def test_world_loader():
    """the game should have attributes
    """
    is_a(world_loader.main("player_name"), dict)


def test_main_with_same_name():
    """Tests loading with player name"""
    assert isinstance(world_loader.main('bobby b'), dict)


def test_main_without_same_name():
    """Tests loading with unknown name"""
    assert isinstance(world_loader.main('nobody'), dict)
