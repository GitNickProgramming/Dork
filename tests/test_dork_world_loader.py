# -*- coding: utf-8 -*-
"""Basic tests for world loader
"""
from dork.game_utils.world_loader import main as load
from tests.utils import is_a


def test_world_loader():
    assert isinstance(load("bobby b"), dict)
    assert isinstance(load("awigahwgh"), dict)


def test_maze_generator(maze):
    """run the maze generator
    """
    maze.draw()
    maze.update()
