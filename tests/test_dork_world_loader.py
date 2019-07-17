# -*- coding: utf-8 -*-
"""Basic tests for world loader"""

from dork.game_utils.world_loader import main as load


def test_world_loader():
    """load an existing save, and one that doesn't exist"""

    assert isinstance(load("bobby b"), dict)
    assert isinstance(load("awigahwgh"), dict)


def test_maze_generator(maze):
    """run the maze generator"""

    maze.draw()
    maze.update()
