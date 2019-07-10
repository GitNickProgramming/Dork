"""This test verifies items are able to
swap between room and player inventories"""
import dork.types


def test_items_are_swappable():
    """As it says on the tin, tests if items can
    transfer between player and room"""

    test_player = dork.types.Player()
    test_room = dork.types.Room()
    test_item = dork.types.Item()
    test_item.name = "squeaky hammer of valor"
    test_room.items[test_item.name] = test_item
    assert test_room.items["squeaky hammer of valor"],\
    "failed to make room items"
    transfer = test_room.items.pop("squeaky hammer of valor")
    test_player.items[transfer.name] = transfer
    assert isinstance(test_player.items["squeaky hammer of valor"],
                      dork.types.Item), "failed to swap items"
    assert test_room.items == dict(), "Failed to make items poppable"
