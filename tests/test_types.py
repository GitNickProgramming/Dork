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
