# -*- coding: utf-8 -*-
"""Pytest Fixtures for Dork unit-tests"""
import pytest
import dork


pytest_plugins = ["pytester"]  # pylint: disable=invalid-name


@pytest.fixture
def player():
    """A basic dork player fixture"""
    player = dork.types.Player("player name", "player room")
    return player


@pytest.fixture
def item():
    """A basic dork player fixture"""
    return dork.types.Item()


@pytest.fixture
def room():
    """A basic dork room fixture"""
    return dork.types.Room({}, "test room name")


@pytest.fixture
def game():
    """A basic dork room fixture"""
    game = dork.types.Game(player, worldmap)
    return game


@pytest.fixture
def worldmap():
    """A basic dork room fixture"""
    return dork.types.Worldmap()


@pytest.fixture
def holder():
    """A basic dork room fixture"""
    return dork.types.Holder()


@pytest.fixture
def repl():
    """A basic dork player fixture"""
    repl = dork.game_utils.game_data.REPL
    return repl



@pytest.fixture
def run(capsys, mocker):
    """CLI run method fixture

    To use:
        run(meth, *args, input_side_effect=['first', 'second', 'last'])
        run(meth, *args, input_return_value='42')
    This would run the method `meth` with arguments `*args`.

    In the first every time `builtins.input()` is called by `meth`, the next
    element of input_side_effect will be returned

    In the second every invokation of 'buitins.input()' returns '42'.

    Both return a tuple of three items, mocked-input, stdout, and stderr.
    """
    def _do_run(method, *args, **kwargs):
        mocked_input = mocker.patch('builtins.input')
        if 'input_side_effect' in kwargs:
            mocked_input.side_effect = kwargs['input_side_effect']
            del kwargs['input_side_effect']

        if 'input_return_value' in kwargs:
            mocked_input.return_value = kwargs['input_return_value']
            del kwargs['input_return_value']
        method(*args, **kwargs)
        captured = capsys.readouterr()
        return captured.out, captured.err, mocked_input

    return _do_run
