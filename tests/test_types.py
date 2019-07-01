# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""

from unittest import mock
from tests.utils import has_a, has_method, is_a
import dork.types as types


# pylint: disable=protected-access



def test_game_attributes():
    """the game should have attributes
    """
    with mock.patch('builtins.input') as inp:
        inp.side_effect = ['devon']
        game = types.Game
        has_a(game, "players")
        has_a(game, "worldmap")
        has_a(game, "hero")
        has_method(game, "build")
        has_method(game, "_build_players")
        has_method(game, "_build_world")
        has_method(game, "_build_hero")
        has_method(game, "_gtfo")
        has_method(game, "_move")
        has_method(game, "_inventory")
        has_method(game, "_look")



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
    has_a(player, "items")
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
    """Tests set location for actual update"""
    player.set_location('running in the 90s')
    assert player.get_location() == 'running in the 90s'


def test_game_inventory():
    """Tests a game starts with inventory"""
    with mock.patch('builtins.input') as inp:
        inp.side_effect = ['steamed hams', '.rq']
        our_game = types.Game()
        assert 'got shit, son' in our_game.get_inventory()[0],\
            "game object failed to make inventory"
        our_game.hero = types.Player
        our_game.hero.items = dict()
        new_item = types.Item()
        new_item.name = 'ye flask'
        add = {'ye flask': new_item}
        our_game.hero.items.update(add)
        assert 'ye flask' in our_game.get_inventory()[0],\
            "game object inventory failed to store an item"


def test_confirm_yes():
    """Test confirm y functionality"""
    with mock.patch('builtins.input') as inp:
        inp.side_effect = ['gentlemen...', 'y']
        our_game = types.Game()
        assert our_game.get_confirm(), "failed to confirm"


def test_confirm_no():
    """Test confirm n functionality"""
    with mock.patch('builtins.input') as inp:
        inp.side_effect = ['gentlemen...', 'n']
        our_game = types.Game()
        assert not our_game.get_confirm(), "failed to confirm"


def test_confirm_unknown(run):
    """Test confirm when invalid input given"""
    out = run(types.Game.get_confirm, types.Game,
              input_side_effect=['my dudes', 'y'])
    assert 'not a valid response!' in out[0], 'failed on unknown progam'


def test_add_item_runs():
    """test adding items to player"""
    test_player = types.Player()
    test_item = types.Item()
    test_item.name = 'gloves of fire detection'
    test_player.add_item(test_item)
    items_count = len(test_player.inventory)
    assert items_count > 0,\
        "add_item fails to exist for testing"


def test_look():
    """test looking in empty map"""
    with mock.patch('builtins.input') as inp:
        inp.side_effect = ['steamed hams', '.rq']
        our_game = types.Game()
        assert 'you get in here?' in our_game.get_look()[0],\
            "failed to look in empty map"


def test_start_over():
    """test starting new game"""
    with mock.patch('builtins.input') as inp:
        inp.side_effect = ['steamed hams', 'y', '.rq']
        our_game = types.Game()
        assert our_game.get_start_over('my man')[0] == 'my man', 'failed redo'


def test_start_over_nope():
    """test undoing new game"""
    with mock.patch('builtins.input') as inp:
        inp.side_effect = ['steamed hams', 'n', '.rq']
        our_game = types.Game()
        assert 'Guess you changed your mind!' in\
            our_game.get_start_over('my man')[0], "failed undo reload"

   

def test_confirm_method_yes(capsys, mocker):
    """confirm should do things
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["y"]
    assert types.Game._confirm()
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert mocked_input.call_count == 1


def test_confirm_method_no(capsys, mocker):
    """confirm should do things
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["n"]
    assert types.Game._confirm() is False
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert mocked_input.call_count == 1


def test_confirm_method_blank(capsys, mocker):
    """confirm should do things
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["afk", "    ", "y"]
    types.Game._confirm()
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert "That is not a valid response!" in captured.out
    assert mocked_input.call_count == 3


def test_start_over_no(capsys, mocker, game):
    """confirm should do things
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["n"]
    assert game._start_over("the notification string") == (
        "Guess you changed your mind!", False)
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert mocked_input.call_count == 1


def test_start_over_yes(capsys, mocker, game):
    """confirm should do things
    """
    # the call count here as 2 is a magic number need to document that
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["y", "new player name", ".rq"]
    game._start_over("the notification string")
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert mocked_input.call_count == 2


def test_player_location(player):
    """testing the get and set of player location
    """
    is_a(player.location, types.Room)
    types.Player.set_location(player, "Arcterus")
    assert types.Player.get_location(player) == "Arcterus"


def test_move_method(game, mocker, cardinals):
    """testing the move function for any map
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["new player name"]
    types.Game.build(game)
    assert game.hero.location.name == "entrance"

    for direction in cardinals:
        if game.hero.location.adjacent[direction] is not None:
            move_return = game._move(direction)
            assert (game.hero.location.description, False) == move_return
        if game.hero.location.adjacent[direction] is None:
            move_return = game._move(direction)
            assert (
                f"You cannot go {direction} from here.", False) == move_return


def test_inventory_empty(game, mocker):
    """testing the inventory function
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["new player name"]
    types.Game.build(game)
    assert game._inventory() == ("    You ain't got shit, son!", False)


def test_inventory_has_item(game, mocker):
    """testing the inventory function
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["bobby b"]
    types.Game.build(game)
    assert game._inventory() == ("Inventory:\n\n    wobblelobbledobdob", False)
