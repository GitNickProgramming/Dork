# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork"""

from dork import repl, cli, types
# pylint: disable=protected-access


def test_repl_evaluate(game, repl_data):
    """Dork.repl._evaluate should deal with all input types"""

    assert repl._evaluate("", game, repl_data) == (
        'Huh? Can you speak up?', False)

    assert repl._evaluate("     ", game, repl_data) == (
        'Huh? Can you speak up?', False)

    assert repl._evaluate("Go", game, repl_data) == (
        "Sorry, I don't know that one.", False)

    assert repl._evaluate("walk map", game, repl_data) == (
        "You can't go that way", False)


def test_all_moves_and_others(game, repl_data):
    """tests that movement is successful and meta methods"""

    assert repl._evaluate(".m", game, repl_data) == ("", False)

    for _ in range(4):
        if "description" in repl._evaluate("n", game, repl_data):
            break

        if "description" in repl._evaluate("s", game, repl_data):
            break

        if "description" in repl._evaluate("e", game, repl_data):
            break

        if "description" in repl._evaluate("w", game, repl_data):
            break

    assert repl._evaluate(".z", game, repl_data) == (
        "holy *%&#@!!! a wild zork appeared!", False
    )

    assert repl._evaluate("look david", game, repl_data) == (
        "This command takes no arguments", False
    )

    assert repl._evaluate("north north", game, repl_data) == (
        "Uh. Which way are you trying to go?", False
    )

    assert repl._evaluate(".m", game, repl_data) == ("", False)

    assert repl._evaluate(".v", game, repl_data) == (
        "verbose inventory: ON", False)

    assert "There's nothing here." in repl._evaluate("i", game, repl_data)
    assert "inventory:" in repl._evaluate("examine", game, repl_data)[0]

    assert repl._evaluate(".v", game, repl_data) == (
        "verbose inventory: OFF", False)

    assert "There's nothing here." in repl._evaluate("i", game, repl_data)

    assert "inventory:" in repl._evaluate("examine", game, repl_data)[0]

    assert "t" in repl._evaluate("look", game, repl_data)[0]

    assert repl._evaluate(".rq", game, repl_data) == (
        "Thanks for playing DORK, tester!", True)

    repl._evaluate(".rq", game, repl_data)


def test_repl_new_game():
    """test repl new player function"""

    game, repl_data = repl._new_game("tester")
    assert isinstance(game, types.Game)
    assert isinstance(repl_data, tuple)


def test_new_game_command(run):
    """test repl with new player command"""

    _, _, mocked_input = run(
        cli.main, '-?', input_side_effect=[
            'tester', '.new', 'y', 'tester', '.rq'
        ]
    )
    assert mocked_input.call_count == 5


def test_repl_load_game():
    """test repl with existing save file"""

    game, repl_data = repl._new_game("devon")
    assert isinstance(game, types.Game)
    assert isinstance(repl_data, tuple)


def test_repl_save_game():
    """test save function"""

    game, repl_data = repl._new_game("devon")
    repl._evaluate(".save", game, repl_data)


def test_repl_evaluate_safety(game, repl_data):
    """testing ways to break the repl"""

    assert repl._evaluate("n LARSEN", game, repl_data)
    assert repl._evaluate("north LARSEN", game, repl_data)
    assert repl._evaluate("i LARSEN", game, repl_data)
    assert repl._evaluate("examine LARSEN", game, repl_data)
    assert repl._evaluate(".new LARSEN", game, repl_data)
    assert repl._evaluate(".load LARSEN", game, repl_data)
    assert repl._evaluate(".save LARSEN", game, repl_data)
    assert repl._evaluate(".m LARSEN", game, repl_data)
    assert repl._evaluate(".v LARSEN", game, repl_data)
    assert repl._evaluate(".rq LARSEN", game, repl_data)
    assert repl._evaluate("points LARSEN", game, repl_data)


# def test_repl_bad_keys(game, repl_data):
#     """these are bad keys for take and drop commands"""

    # assert repl._evaluate("drop LARSEN", game, repl_data)
    # assert repl._evaluate("take LARSEN", game, repl_data)
    # assert repl._evaluate("loot LARSEN", game, repl_data)
