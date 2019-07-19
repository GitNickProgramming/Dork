# """This test verifies items are able to
# swap between room and player inventories"""
# import unittest.mock as mock
# import dork.types


# def test_items_are_swappable_runtime():
#     """Tests items can be swapped in
#     room and player in game instance"""

#     test_game = dork.types.Game()
#     with mock.patch('builtins.input') as inp:
#         inp.side_effect = ["sparticus"]
#         test_game.build()
#         item_a = dork.types.Item()
#         item_a.name = "Bepis"
#         test_game.worldmap.rooms["entrance"].items[item_a.name] = item_a
#         assert test_game.worldmap.rooms["entrance"].items != dict(),\
#             "Room cannot contain items"
#         yanked_item = test_game.worldmap.rooms[
#             "entrance"].items.pop("Bepis")
#         test_game.hero.items[yanked_item.name] = yanked_item
#         assert test_game.hero.items != dict(),\
#             "Player failed to add item"
#         assert test_game.hero.items[yanked_item.name] == yanked_item,\
#             "Player failed to move item"
#         test_room = test_game.worldmap.rooms["entrance"]
#         assert "Bepis" not in test_room.items.keys(),\
#             "Room failed to pop item"


# def test_items_are_swappable():
#     """As it says on the tin, tests if items can
#     transfer between player and room"""

#     test_player = dork.types.Player()
#     test_room = dork.types.Room()
#     test_item = dork.types.Item()
#     test_item.name = "squeaky hammer of valor"
#     test_room.items[test_item.name] = test_item
#     assert test_room.items["squeaky hammer of valor"],\
#         "failed to make room items"
#     transfer = test_room.items.pop("squeaky hammer of valor")
#     test_player.items[transfer.name] = transfer
#     assert isinstance(test_player.items["squeaky hammer of valor"],
#                       dork.types.Item), "failed to swap items"
#     assert test_room.items == dict(), "Failed to make items poppable"
