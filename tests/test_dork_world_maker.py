# -*- coding: utf-8 -*-
"""Basic tests for world loader
"""
import dork.game_utils.world_maker as world_maker
from tests.utils import is_a


def test_world_loader():
    """world_maker.load_game should return a dict
    """
    nobody = world_maker.load_game("nobody")
    is_a(nobody, dict)

    keys = ["rooms", "players"]
    for key in keys:
        assert key in nobody.keys()

    rooms = [
        "boss",
        "gold",
        "armory",
        "cave",
        "rock ledge",
        "entrance"
    ]
    for room in nobody["rooms"]:
        assert nobody["rooms"][room]["name"] in rooms

    players = [
        "troll",
        "ghost",
        "hero"
    ]
    for player in nobody["players"]:
        assert player in players


# Mock to get the successful load message
def test_load_existing_file():
    """world_maker.load_game should successfully load a save file
    """
    bobby_b = world_maker.load_game("bobby b")
    is_a(bobby_b, dict)

    keys = ["rooms", "players"]
    for key in keys:
        assert key in bobby_b.keys()

    rooms = [
        "boss",
        "gold",
        "armory",
        "cave",
        "rock ledge",
        "entrance"
    ]
    for room in bobby_b["rooms"]:
        assert bobby_b["rooms"][room]["name"] in rooms

    players = [
        "troll",
        "ghost",
        "hero"
    ]
    for player in bobby_b["players"]:
        assert player in players


# Need to delete file after running test.
# Maybe also check that file now exists?
def test_save_file(game):
    """Save the default world to ''.yml
    """
    world_maker.save_game(game)
