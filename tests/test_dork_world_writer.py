"""Basic tests for world writer
"""
import dork.game_utils.world_writer as world_writer
import dork.types as game
from tests.utils import is_a


def test_world_writer():
    """the game should have attributes
    """
    # is_a(world_writer.save_gamee(game), dict)
    world_writer.save_gamee(game)
