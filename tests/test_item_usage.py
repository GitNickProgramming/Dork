"""Test the various usable items"""


from random import choice
from dork import repl
# pylint: disable=protected-access


def test_take_drop_all(game):
    """
        1. take all items
        2. confirm they are now in player inventory
        3. confirm room inventory is empty
        4. drop all items
        5. confirm player inventory empty
        6. confirm all items now in room inventory
    """

    hero = game.hero
    room_0 = game.rooms["room 0"]
    room_inventory = room_0.get_items("", room_0.data, False)

    repl._evaluate("take", game)
    assert hero.get_items("", hero.data, False) == room_inventory
    assert room_0.get_items("", room_0.data, False) == "There's nothing here."

    repl._evaluate("drop", game)
    assert hero.get_items("", hero.data, False) == "There's nothing here."
    assert room_0.get_items("", room_0.data, False) == room_inventory


def test_take_drop_single(game):
    """
        1. take a random item from the room
        2. confirm it is in player inventory
        3. confirm it is not in room inventory
        4. drop item
        5. confirm no longer in player inventory
        6. confirm item in room inventory
    """

    hero = game.hero
    room_0 = game.rooms["room 0"]
    random_item = choice(list(room_0.inventory.keys()))

    repl._evaluate(f"take {random_item}", game)
    assert random_item in hero.inventory
    assert random_item not in room_0.inventory

    repl._evaluate(f"drop {random_item}", game)
    assert random_item not in hero.inventory
    assert random_item in room_0.inventory


def test_drop_item_not_in_inv(game):
    """try to drop an item that is not in your inventory"""

    no_drop = repl._evaluate("drop larsen", game)
    assert no_drop == ("There is no larsen in your inventory.", False)


def test_take_item_not_in_room(game):
    """try to take an item that is not in the room"""

    no_take = repl._evaluate(f"take larsen", game)
    assert no_take == ("There is no larsen here.", False)


# def test_player_has_none(player):
#     """Tests race case where player contains None"""
#
#     test_dict = {"name": "leather belt",
#                  "equipped": "leather belt", "inventory": [None, None]}
#     test_player = player
#     test_player.make(test_dict)
#     assert test_player.items == dict(),\
#         "Player copied None object as item"


# def test_look(run):
#     """testing _look for display items and description"""

#     out = run(dork.repl.repl, \
# input_side_effect=["name", "look around", ".rq"])
#     assert "Items:\nsoggy waffle\ntorn parchment\nbroken quill" in out[0],\
#            "item are not found on entrance room"
#     test_game = types.Game()
#     assert test_game._look() == (None, False)


# def test_take(run):
#     """testing _take the method takes all and specific item"""

#     out = run(dork.repl.repl, input_side_effect=["name", "take", ".rq"])
#     assert "You took all item. You took them well." in out[0],\
#            "item are not found on entrance room"
#     out = run(dork.repl.repl, input_side_effect=["name",
#                                                  "take soggy waffle",
#                                                  ".rq"])
#     assert "You took the soggy waffle. You took it well." in out[0],\
#            "item are not found on entrance room"


# def test_drop_item(run):
#     """testing _drop_item the method takes all and specific item"""

#     out = run(dork.repl.repl, input_side_effect=["name", "take soggy waffle",
#                                                  "drop soggy waffle", ".rq"])
#     assert "Oops, you dropped something!" in out[0],\
#            "item are not found on entrance room"


# def test_sword_can_swing(run):
#     """Tests that a sword object calls swingable"""

#     test_sword = types.Item()
#     test_sword.make({"name": "test sword",
#                      "description": "sword of boring",
#                      "stats": [+1, "attack"]})
#     out = run(test_sword.use, "player", test_sword.name)
#     assert out[0] == "You swing the test sword at player\n",\
#                      "use method failed for sword items"


# def test_key_can_open(run):
#     """Tests that a key object calls openable"""

#     test_key = types.Item()
#     test_key.make({"name": "test key",
#                    "description": "jingly keys",
#                    "stats": [+1, "key"]})
#     out = run(test_key.use, "rock", test_key.name)
#     assert out[0] == "You insert the test key into rock\n",\
#                      "use method failed for key items"


# def test_potion_can_speed_up(run):
#     """Tests that a stat changing object calls statable"""

#     test_potion = types.Item()
#     test_potion.make({"name": "test potion",
#                       "description": "Looks like booze to me",
#                       "stats": [-100, "speed"]})
#     out = run(test_potion.use, "player", test_potion.name)
#     assert out[0] == "The test potion takes effect on player\n",\
#                      "use method failed for stat changing items"


# def test_gem_can_be_inserted(run):
#     """Calls that a gem object calls puzzleable"""

#     test_emerald = types.Item()
#     test_emerald.make({"name": "shiny emerald",
#                        "description": "POWERFUL",
#                        "stats": [+1, "emerald"]})
#     out = run(test_emerald.use, "rock", test_emerald.name)
#     assert out[0] == "You try to fit the shiny emerald into the rock\n",\
#                      "use method failed for puzzle items"


# def test_gold_can_pay(run):
#     """Checks that a gold object calls payable"""

#     test_key = types.Item()
#     test_key.make({"name": "bag 'o MOLTEN GOOOLD",
#                    "description": "der bee gould een dem der bag",
#                    "stats": [+100, "gold"]})
#     out = run(test_key.use, "player", test_key.name)
#     assert out[0] == "You use the bag 'o MOLTEN GOOOLD to pay player\n",\
#                      "use method failed for gold items"


# def test_none_item(run):
#     """Checks that an object with none is unusable"""

#     test_key = types.Item()
#     test_key.make({"name": "empty thing",
#                    "description": "nothin",
#                    "stats": None})
#     out = run(test_key.use, "player", "player")
#     assert out[0] == "You find no use of this item\n",\
#                      "use method failed for gold items"


# def test_only_stat(run):
#     """Checks that an object with only a stat is unusable"""

#     test_key = types.Item()
#     test_key.make({"name": "empty thing",
#                    "description": "nothin",
#                    "stats": [+1]})
#     out = run(test_key.use, "player", "player")
#     assert out[0] == "You find no use of this item\n",\
#                      "use method failed for gold items"


# def test_runtime_items(run):
#     """Tests the functionality of items in runtime"""

#     out = run(dork.repl.repl, input_side_effect=["tester",
#                                                  "use sword", ".rq"])
#     assert "You don't have that item...\n" in out[0],\
#            "Failed to decline use on non-existant item"
#     test_item = dork.types.Item()
#     test_item.make({"name": "sword",
#                     "description": "its made of foam",
#                     "stats": [+0, "attack"]})
#     test_game = dork.types.Game()
#     test_game.hero.items["sword"] = test_item
#     out = run(test_game._use_item, "sword", input_side_effect=["player"])
#     assert "You swing the sword at player" in out[0],\
#            "Failed to use item in runtime"


# def test_use_has_target_input(run):
#     """Testing that use takes an input"""

#     out = run(dork.repl.repl, input_side_effect=["tester",
#                                                  "use sword", ".rq"])
#     assert "You don't have that item...\n" in out[0],\
#            "Failed to decline use on non-existant item"
#     test_item = dork.types.Item()
#     test_item.make({"name": "sword",
#                     "description": "its made of foam",
#                     "stats": [+0, "attack"]})
#     test_game = dork.types.Game()
#     test_game.hero.items["sword"] = test_item
#     out = run(test_game._use_item, "sword", input_side_effect=["player"])
#     assert "You swing the sword at player" in out[0],\
#            "failed to contain a target argument"
