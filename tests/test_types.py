# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
# pylint: disable=protected-access
from tests.utils import is_a
import dork.types as types
import dork.repl


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


def test_none_item(run):
    """Checks that an object with none is unusable"""
    test_key = types.Item()
    test_key.make({"name": "empty thing",
                   "description": "nothin",
                   "stats": None})
    out = run(test_key.use)
    assert out[0] == "You find no use of this item\n",\
                     "use method failed for gold items"


def test_only_stat(run):
    """Checks that an object with only a stat is unusable"""
    test_key = types.Item()
    test_key.make({"name": "empty thing",
                   "description": "nothin",
                   "stats": [+1]})
    out = run(test_key.use)
    assert out[0] == "You find no use of this item\n",\
                     "use method failed for gold items"

def test_look(run):
    """testing _look for display items and description"""
    out = run(dork.repl.repl, input_side_effect=["name","look around", ".rq"])
    assert "Items:\nsoggy waffle\ntorn parchment\nbroken quill" in out[0],\
           "item are not found on entrance room"
    test_game = types.Game()
    assert test_game._look() == (None , False)




