# -*- coding: utf-8 -*-
"""Basic tests for world loader
"""
import dork.game_utils.world_loader as world_loader
import dork.game_utils.maze_generator as maze_gen
from tests.utils import is_a


def test_world_loader():
    """the game should have attributes
    """
    is_a(world_loader.main("player_name"), tuple)


def test_main_with_existing_save():
    """Tests loading an existing save file
    """
    assert isinstance(world_loader.main("bobby b"), tuple)


def test_main_without_same_name():
    """Tests loading a non-existing save file
    """
    assert isinstance(world_loader.main("nobody"), tuple)


def test_maze_generator():
    """run the maze generator
    """
    maze_gen.main()
    maze_gen.main(debug=True)
