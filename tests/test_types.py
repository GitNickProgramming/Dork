# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
from tests.utils import is_a
import dork.types as types
import dork.game_utils.factory_data as factory_data
import dork.repl

# pylint: disable=protected-access


def test_confirm_method_yes(capsys, mocker):
    """confirm should do things"""

    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["y", "tester"]
    assert types.Game._confirm()
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert mocked_input.call_count == 1


def test_confirm_method_no(capsys, mocker):
    """confirm should do things"""

    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["n"]
    assert types.Game._confirm() is False
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert mocked_input.call_count == 1


def test_confirm_method_blank(capsys, mocker):
    """confirm should do things"""

    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["afk", "    ", "y", "tester"]
    types.Game._confirm()
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert "That is not a valid response!" in captured.out
    assert mocked_input.call_count == 3


def test_start_over_no(capsys, mocker, game):
    """confirm should do things"""

    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["n", ".rq"]
    assert game._start_over() == ("Guess you changed your mind!", False)
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert mocked_input.call_count == 1


def test_start_over_yes(capsys, mocker, game):
    """confirm should do things"""

    # the call count here as 2 is a magic number need to document that
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["y", "tester"]
    game._start_over()
    captured = capsys.readouterr()
    assert "\n!!!WARNING!!! You will lose unsaved data!\n" in captured.out
    assert mocked_input.call_count == 1


def test_player_location(game):
    """testing the get and set of player location"""

    is_a(game.hero.location, types.Room)


def test_move_method(game, cardinals):
    """testing the move function for any map"""

    for direction in cardinals:
        if getattr(game.hero.location, direction) is not None:
            move_return = game._move(direction)
            assert ("You have entered " +game.hero.location.name+"\n"\
                    +game.hero.location.description, False) == move_return
        if not getattr(game.hero.location, direction):
            move_return = game._move(direction)
            assert (
                f"You cannot go {direction} from here.", False) == move_return


def test_factory_data():
    """test factory data methods"""

    assert isinstance(factory_data.rules(0, 0), list)
    assert isinstance(factory_data.stats("magic"), dict)


def test_mazefactory():
    """builds all game types"""

    assert isinstance(types.MazeFactory.build(), dict)


def test_inventory_has_item(mocker):
    """testing the inventory function
    """
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["bobby b"]
    test_game = types.Gamebuilder.build('bobby b')
    test_item = dork.types.Item()
    test_item.name = "wobblelobbledobdob"
    test_game.hero.inventory[test_item.name] = test_item
    assert test_item.name in test_game.hero.inventory,\
        "Failed to store items in inventory"


def test_player_has_none(mocker):
    """Testing if None object populates inventory as None object pairing"""
    mocked_input = mocker.patch('builtins.input')
    mocked_input.side_effect = ["bobby b"]
    test_game = types.Gamebuilder.build('bobby b')
    test_item = None
    test_game.hero.inventory[test_item] = test_item
    assert None in test_game.hero.inventory,\
        "Failed to store items in inventory"


def test_look(run):
    """testing _look for display items and description"""
    out = run(dork.repl.repl, input_side_effect=["devon",
                                                 "look around",
                                                 ".rq"])
    assert "Items:\ndamaged note\nfragile leather greaves" in out[0],\
           "item are not found on entrance room"


def test_take(run):
    """testing _take the method takes all and specific item"""
    out = run(dork.repl.repl, input_side_effect=["name", "take", ".rq"])
    assert "You took all item. You took them well." in out[0],\
           "item are not found on entrance room"

# def test_take_single(run):
    # """testing _take the method takes all and specific item"""
    # test_game = dork.types.Gamebuilder().build("test")
    # gamee = dork.types.Gamebuilder.build("test")
    # lis = gamee.data["rooms"]["room 0"]["inventory"]
    # out = run(dork.repl.repl, input_side_effect=["name", "examine",\
    #  "take " + item, ".rq"])
    # assert "You took the " + item+". You took it well" in out[0],\
    #       "item are not found on entrance room"


def test_drop_item(run):
    """testing _drop_item the method takes all and specific item"""
    out = run(dork.repl.repl, input_side_effect=["name", "take",
                                                 "drop", ".rq"])
    assert "Oops, you can't hold all these items" in out[0],\
           "item are not found on entrance room"


def test_sword_can_swing(run):
    """Tests that a sword object calls swingable"""
    test_sword = types.Item()
    test_sword.make({"name": "test sword",
                     "description": '',
                     "amount": 0,
                     "attack": 18,
                     "equipable": True,
                     "luck": 9,
                     "strength": 0,
                     "weight": 10,
                     "type": 'weapon'})
    out = run(test_sword.use, "player", test_sword.name)
    assert out[0] == "You swing the test sword at player\n",\
                     "use method failed for sword items"


def test_key_can_open(run):
    """Tests that a key object calls openable"""
    test_key = types.Item()
    test_key.make({"name": "test key",
                   "description": "jingly keys",
                   "type": "key"})
    out = run(test_key.use, "rock", test_key.name)
    assert out[0] == "You insert the test key into rock\n",\
                     "use method failed for key items"


def test_potion_can_speed_up(run):
    """Tests that a stat changing object calls statable"""
    test_potion = types.Item()
    test_potion.make({"name": "test potion",
                      "description": "Looks like booze to me",
                      "type": "magic items"})
    out = run(test_potion.use, "player", test_potion.name)
    assert out[0] == "The test potion takes effect on player\n",\
                     "use method failed for stat changing items"


def test_gold_can_pay(run):
    """Checks that a gold object calls payable"""
    test_key = types.Item()
    test_key.make({"name": "bag 'o MOLTEN GOOOLD",
                   "description": "der bee gould een dem der bag",
                   "type": "gold"})
    out = run(test_key.use, "player", test_key.name)
    assert out[0] == "You use the bag 'o MOLTEN GOOOLD to pay player\n",\
                     "use method failed for gold items"


def test_none_item(run):
    """Checks that an object with none is unusable"""
    test_key = types.Item()
    test_key.make({"name": "empty thing",
                   "description": "nothin",
                   "type": None})
    out = run(test_key.use, "player", "player")
    assert out[0] == "You find no use of this item\n",\
                     "use method failed for gold items"


def test_only_stat(run):
    """Checks that an object with only a stat is unusable"""
    test_key = types.Item()
    test_key.make({"name": "empty thing",
                   "description": "nothin",
                   "type": 1})
    out = run(test_key.use, "player", "player")
    assert out[0] == "You find no use of this item\n",\
                     "use method failed for gold items"


def test_runtime_items(run):
    """Tests the functionality of items in runtime"""
    out = run(dork.repl.repl, input_side_effect=["tester",
                                                 "use sword", ".rq"])
    assert "You don't have that item...\n" in out[0],\
           "Failed to decline use on non-existant item"


def test_use_has_target_input(run):
    """Testing that use takes an input"""
    out = run(dork.repl.repl, input_side_effect=["tester",
                                                 "use sword", ".rq"])
    assert "You don't have that item...\n" in out[0],\
           "Failed to decline use on non-existant item"
    test_item = dork.types.Item()
    test_item.make({"name": "sword",
                    "description": "its made of foam",
                    "type": "weapon"})
    test_game = dork.types.Gamebuilder().build("test")
    test_game.hero.inventory[test_item.name] = test_item
    out = run(test_game._use_item, "sword", input_side_effect=["player"])
    assert "You swing the sword at player" in out[0],\
           "failed to contain a target argument"
