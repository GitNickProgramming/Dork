# -*- coding: utf-8 -*-
"""Basic tests for world loader
"""
import dork.game_utils.world_loader as world_loader
from tests.utils import is_a


def test_world_loader():
    """the game should have attributes
    """
    is_a(world_loader.main("player_name"), dict)
