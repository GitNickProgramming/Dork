# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
from tests.utils import has_a, is_a
from unittest import mock
from dork import types

def test_game_attributes():
    """the game should have attributes
    """
    with mock.patch('builtins.input') as inp:
        inp.side_effect = ['devon']
        game = types.Game
        has_a(game, "players")
        has_a(game, "worldmap")
        has_a(game, "hero")

def test_room_attributes(room):
    """the room should have attributes
    """
    has_a(room, "name")
    has_a(room, "adjacent")
    has_a(room, "description")
    has_a(room, "players")
    has_a(room, "items")
    has_a(room, "clues")


def test_player_attributes(player):
    """the player should have attributes
    """
    has_a(player, "name")
    has_a(player, "location")
    has_a(player, "inventory")
    has_a(player, "equipped")


def test_item_attributes(item):
    """item should have holder and capacity
    """
    has_a(item, "name")
    has_a(item, "description")
    has_a(item, "stats")


def test_holder_attributes(holder):
    """holder should have items
    """
    has_a(holder, "items")


def test_worldmap_attributes(worldmap):
    """the worldmap should have a dict of rooms
    """
    has_a(worldmap, "rooms")

def test_player_set_location(player):
    player.set_location('running in the 90s')
    assert player.get_location() == 'running in the 90s'


def test_game_inventory(player):
    """Tests a game starts with inventory"""
    with mock.patch('builtins.input') as inp:
        inp.side_effect = ['steamed hams','.rq']
        our_game = types.Game()
        assert 'got shit, son' in our_game._inventory()[0], "game object failed to make inventory"
        our_game.hero = types.Player
        our_game.hero.items = dict()
        new_item = types.Item()
        new_item.name = 'ye flask'
        d = {'ye flask': new_item}
        our_game.hero.items.update(d)
        assert 'ye flask' in our_game._inventory()[0], "game object inventory failed to store an item"

def test_confirm_yes(run):
    with mock.patch('builtins.input') as inp:
        inp.side_effect = ['gentlemen...','y']
        our_game = types.Game()
        assert our_game._confirm(), "failed to confirm"
        

def test_confirm_no(run):
    with mock.patch('builtins.input') as inp:
        inp.side_effect = ['gentlemen...','n']
        our_game = types.Game()
        assert not our_game._confirm(), "failed to confirm"
        


def test_confirm_unknown(run):
    out = run(types.Game._confirm,input_side_effect=['my dudes','y'])
    assert 'not a valid response!' in out[0], 'failed on unknown progam'


def test_add_item_runs():
    test_player = types.Player()
    test_item = types.Item()
    test_item.name = 'gloves of fire detection'
    test_player.add_item(test_item)
    assert len(test_player.inventory) > 0 , "add_item fails to exist for testing"

def test_look():
    with mock.patch('builtins.input') as inp:
        inp.side_effect = ['steamed hams','.rq']
        our_game = types.Game()
        assert 'you get in here?' in our_game._look()[0], "failed to look in empty map"

def test_start_over():
    with mock.patch('builtins.input') as inp:
        inp.side_effect = ['steamed hams','y','.rq']
        our_game = types.Game()
        assert our_game._start_over('my man')[0] == 'my man', 'failed redo'

def test_start_over_nope():
    with mock.patch('builtins.input') as inp:
        inp.side_effect = ['steamed hams','n','.rq']
        our_game = types.Game()
        assert  our_game._start_over('my man')[0] == 'Guess you changed your mind!', "failed undo reload"