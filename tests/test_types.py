# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""

from tests.utils import has_a, has_method, is_a
import dork.types as types


# pylint: disable=protected-access


def test_game_attributes(game):
    """the game should have attributes
    """
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
    has_a(worldmap, "players")


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
    assert game._inventory() == (
        "Inventory:\n\n    wobblelobbledobdob", False
    )


def test_player_has_none(player):
    """Tests race case where player contains None"""
    test_dict = {"name": "leather belt",
                 "equipped": "leather belt", "inventory": [None, None]}
    test_player = player
    test_player.make(test_dict)
    assert test_player.items == dict(),\
        "Player copied None object as item"


def test_sword_can_swing(run):
    """Tests that a sword object calls swingable"""
    test_sword = types.Item()
    test_sword.make({"name": "test sword",
                     "description": "sword of boring",
                     "stats": [+1, "attack"]})
    out = run(test_sword.use)
    assert out[0] == "You swing the item\n",\
                     "use method failed for sword items"


def test_key_can_open(run):
    """Tests that a key object calls openable"""
    test_key = types.Item()
    test_key.make({"name": "test key",
                   "description": "jingly keys",
                   "stats": [+1, "key"]})
    out = run(test_key.use)
    assert out[0] == "You insert the item\n",\
                     "use method failed for key items"


def test_potion_can_speed_up(run):
    """Tests that a stat changing object calls statable"""
    test_potion = types.Item()
    test_potion.make({"name": "test potion",
                      "description": "Looks like booze to me",
                      "stats": [-100, "speed"]})
    out = run(test_potion.use)
    assert out[0] == "The item takes effect\n",\
                     "use method failed for stat changing items"


def test_gem_can_be_inserted(run):
    """Calls that a gem object calls puzzleable"""
    test_emerald = types.Item()
    test_emerald.make({"name": "shiny emerald",
                       "description": "POWERFUL",
                       "stats": [+1, "emerald"]})
    out = run(test_emerald.use)
    assert out[0] == "You try to fit the item in\n",\
                     "use method failed for puzzle items"


def test_gold_can_pay(run):
    """Checks that a gold object calls payable"""
    test_key = types.Item()
    test_key.make({"name": "bag 'o MOLTEN GOOOLD",
                   "description": "der bee gould een dem der bag",
                   "stats": [+100, "gold"]})
    out = run(test_key.use)
    assert out[0] == "You use the gold to pay\n",\
                     "use method failed for gold items"
