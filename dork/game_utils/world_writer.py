"""Save game data/state into repl && update default location"""
import yaml

__all__ = ["main"]

def main(game):
    gamee = game
    namee = gamee.player.name
    with open('myNewestGame.yml', 'w') as yaml_file:
        yaml.dump(gamee, yaml_file, default_flow_style=False)
    print ("The game data has been saved in a file called "+namee+".yaml")