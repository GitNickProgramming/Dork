# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
from tests.utils import has_a


def test_game_attributes(game):
    """the game should have attributes
    """
    has_a(game, "player")
    has_a(game, "worldmap")
