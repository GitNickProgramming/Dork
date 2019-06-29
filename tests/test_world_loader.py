"""This file tests the loading of the world loader"""
import dork.game_utils.world_loader

def test_main_with_same_name():
    assert isinstance(dork.game_utils.world_loader.main('bobby b'),dict), "failed to load same name save"

def test_main_without_same_name():
    assert isinstance(dork.game_utils.world_loader.main('nobody'),dict)
