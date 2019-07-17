"""saves a game world from a yaml file
"""
import dork.repl as repl
import dork.types

def test_world_writer(run):
    """Tests save print string
    """
    out = run(repl.repl, input_side_effect=["nobody", "take", ".save", ".rq"])
    assert "Your game was saved as" in out[0], "Unable to save game data"

def test_world_writer_data(run):
    """Builds game then tests saved
    """
    gamee = dork.types.Game()
    run(gamee.build, input_side_effect=["default_world"])
    gamee.hero = dork.types.Player()
    gamee.hero.location.name = "a"
    gamee.hero.name = "b"
    gamee.hero.items = {"c": None, "d": dork.types.Item()}
    gamee.worldmap.rooms = {"e": None, "f": dork.types.Room()}
    gamee.players = {"g": "h"}

    assert gamee._save_game() == ("Your game was saved as: b.yml", False)
