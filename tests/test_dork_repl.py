# -*- coding: utf-8 -*-
"""Basic tests for state and entity relationships in dork"""

from dork import repl, cli, types
# pylint: disable=protected-access


def test_repl_evaluate(game):
    """Dork.repl._evaluate should deal with all input types"""

    assert repl._evaluate("", game) == (
        'Huh? Can you speak up?', False)
    assert repl._evaluate("     ", game) == (
        'Huh? Can you speak up?', False)
    assert repl._evaluate("Go", game) == (
        "Sorry, I don't know that one.", False)
    assert repl._evaluate("walk map", game) == (
        "You can't go that way", False)


def test_all_moves_and_others(game):
    """tests that movement is successful and meta methods"""

    assert repl._evaluate(".m", game) == ("", False)

    for _ in range(4):
        if "description" in repl._evaluate("n", game):
            break
        if "description" in repl._evaluate("s", game):
            break
        if "description" in repl._evaluate("e", game):
            break
        if "description" in repl._evaluate("w", game):
            break

    assert repl._evaluate(".z", game) == (
        "holy *%&#@!!! a wild zork appeared!", False
    )

    assert repl._evaluate("look david", game) == (
        "This command takes no arguments", False
    )

    assert repl._evaluate(".z david", game) == (
        "This command takes no arguments", False
    )

    assert repl._evaluate("north north", game) == (
        "Uh. Which way are you trying to go?", False
    )

    assert "t" in repl._evaluate("look", game)[0]
    assert repl._evaluate(".m", game) == ("", False)

    assert repl._evaluate(".v", game) == (
        "verbose inventory: ON", False
    )
    assert "There's nothing here." in repl._evaluate("i", game)
    assert "inventory:" in repl._evaluate("examine", game)[0]

    assert repl._evaluate(".v", game) == (
        "verbose inventory: OFF", False
    )
    assert "There's nothing here." in repl._evaluate("i", game)
    assert "inventory:" in repl._evaluate("examine", game)[0]

    assert repl._evaluate(".rq", game) == (
        "Thanks for playing DORK, tester!", True)

    repl._evaluate(".rq", game)


def test_repl_new_game():
    """test repl new player function"""

    game = repl._new_game("tester")
    assert isinstance(game, types.Game)


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

    game = repl._new_game("devon")
    assert isinstance(game, types.Game)


def test_repl_save_game():
    """test save function"""

    game = repl._new_game("devon")
    repl._evaluate(".save", game)


def test_repl_evaluate_safety(game):
    """testing ways to break the repl"""

    assert repl._evaluate("n LARSEN", game)
    assert repl._evaluate("north LARSEN", game)
    assert repl._evaluate("i LARSEN", game)
    assert repl._evaluate("examine LARSEN", game)
    assert repl._evaluate(".new LARSEN", game)
    assert repl._evaluate(".load LARSEN", game)
    assert repl._evaluate(".save LARSEN", game)
    assert repl._evaluate(".m LARSEN", game)
    assert repl._evaluate(".v LARSEN", game)
    assert repl._evaluate(".rq LARSEN", game)
    assert repl._evaluate("points LARSEN", game)


def test_repl_bad_keys(game):
    """these are bad keys for take and drop commands"""

    assert repl._evaluate("drop LARSEN", game)
    assert repl._evaluate("take LARSEN", game)
    assert repl._evaluate("loot LARSEN", game)
