# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork
"""
from tests.utils import is_a
from dork import repl, types
import dork.game_utils.factory_data as factory_data

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
            assert ("You have entered " +
                    game.hero.location.description, False) == move_return
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
    test_item = types.Item()
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


def test_look(game, repl_data):
    """testing _look for room description"""
    assert "the beginning" in repl._evaluate("look", game, repl_data)[0]


def test_points():
    """testing _points for: add, remove, and no points"""
    game = types.Game()
    result = game._points('_get_points')
    assert result == 10, "points where not added"
    result = game._points('_take')
    assert result == 11, "points where not added"
    result = game._points('_repl_error')
    assert result == 0, "points where not added"


def test_get_points(game, repl_data):
    """prints points"""
    assert "you have:" in repl._evaluate("points", game, repl_data)[0]
    game = types.Game()
    game.points = 0
    result = game._get_points()
    assert "Booooooo! you suck.\nYou have 0 points." in result


def test_take_all(run):
    """testing _take the method takes all items"""
    out = run(repl.repl, input_side_effect=["name", "take", ".rq"])
    assert "You took" in out[0], "No item was taken"


def test_drop_all(run):
    """testing _drop_item the method takes all items"""
    out = run(repl.repl, input_side_effect=["name", "take",
                                            "drop", ".rq"])
    assert "You dropped" in out[0],\
           "item are not found on entrance room"


def test_sword_can_swing():
    """Tests that a sword object calls swingable"""
    test_sword = types.Item()
    test_player = types.Player()
    test_player.name = "player"
    test_sword.name = "sword"
    test_sword.type = "weapon "
    test_sword.usable = types.Attackable
    assert "You swing the sword at player"\
        in test_sword.use(test_player, "sword"),\
           "use method failed for sword items"


def test_key_can_open():
    """Tests that a key object calls openable"""
    test_key = types.Item()
    test_door = types.Item()
    test_door.name = "rock"
    test_key.make({"name": "test key",
                   "description": "jingly keys",
                   "type": "key "})
    test_key.set_usable(test_key.type)
    out = test_key.use(test_door, test_key.name)
    assert "You insert the test key into rock" in out,\
           "use method failed for key items"


def test_potion_can_speed_up():
    """Tests that a stat changing object calls statable"""
    test_potion = types.Item()
    test_player = types.Player()
    test_player.name = "player"
    test_potion.make({"name": "test potion",
                      "description": "Looks like booze to me",
                      "type": "magic items "})
    test_potion.set_usable(test_potion.type)
    out = test_potion.use(test_player, test_potion.name)
    assert "The test potion takes effect on player" in out,\
           "use method failed for stat changing items"


def test_gold_can_pay():
    """Checks that a gold object calls payable"""
    test_key = types.Item()
    test_player = types.Player()
    test_player.name = "player"
    test_key.make({"name": "bag 'o MOLTEN GOOOLD",
                   "description": "der bee gould een dem der bag",
                   "type": "gold "})
    test_key.set_usable(test_key.type)
    out = test_key.use(test_player, test_key.name)
    assert "You use the bag 'o MOLTEN GOOOLD to pay player" in out,\
           "use method failed for gold items"


def test_none_item():
    """Checks that an object with none is unusable"""
    test_key = types.Item()
    test_key.make({"name": "empty thing",
                   "description": "nothin",
                   "type": None})
    out = test_key.use("player", "player")
    assert "You find no use of this item" in out,\
           "use method failed for gold items"


def test_only_stat(mocker):
    """Checks that an object with only a stat is unusable"""
    with mocker.patch('builtins.input') as inpt:
        inpt.side_effect = ["player"]
        test_key = types.Item()
        test_player = types.Player()
        test_player.name = "player"
        test_key.make({"name": "empty thing",
                       "description": "nothin",
                       "type": 1})
        out = test_key.use(test_player, "empty thing")
        assert out == ("You find no use of this item"),\
            "use method failed for gold items"


def test_runtime_items(run):
    """Tests the functionality of items in runtime"""
    out = run(repl.repl, input_side_effect=["tester",
                                            "use sword", ".rq"])
    assert "You don't have that item...\n" in out[0],\
           "Failed to decline use on non-existant item"


def test_type_not_str_item_make():
    """Tests that empty dict creates unusable filler item"""
    test_item = types.Item()
    test_item.make({"type": {}})
    assert test_item.usable == types.NotUsable,\
        "Failed to set empty string item to NotUsable"


def test_set_use_not_str():
    """Tests that unkown object becomes filled in usable"""
    test_item = types.Item()
    test_item.set_usable(object)
    assert test_item.usable == types.NotUsable,\
        "Failed to set unknown object use to notusable"


def test_npc_can_talk(player):
    """Tests that players have a talk method"""
    test_player = types.Player()
    assert hasattr(player, "talk") and callable(player.talk),\
        "failed to have talk method"
    out = test_player.talk()
    assert "Hello" in out, "Failed to talk to calm pc"
    test_player.damage()
    out = test_player.talk()
    assert "I guess you are" in out, "Failed to talk to hostile pc"


def test_npc_can_be_damaged(player):
    """Tests that npc's can be called by damage()"""
    test_player = types.Player()
    assert hasattr(player, "damage") and callable(player.damage),\
        "failed to have damage method"
    out = test_player.damage()
    assert out == "Ouch..Your gonna get it!",\
        "calm state failed to get hurt"
    out = test_player.damage()
    assert "UGH" in out, "hostile state failed to die"
