"""Save game data/state into repl && update start location"""
import yaml

__all__ = ["main"]

def main(game):
    #gamee = game
    #namee = game.player.name
    with open('./dork/saves/'+game.player.name+'.yml', 'w') as my_yaml_file:
        yaml.dump(game, my_yaml_file, default_flow_style=False)

    print("The game data has been saved in a file called "+game.player.name+".yml")