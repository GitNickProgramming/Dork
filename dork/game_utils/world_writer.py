"""Save game data/state into repl && update start location
HAVENT DECIDED BETWEEN WHICH MAIN TO USE. TO CHANGE, GO TO game_data.py 
and change which main it calls within _save_game function"""
import yaml
#import dork.game_utils.world_loader as w_loader
import dork.game_utils.yaml_parser as yaml_parse
import dork.current_game as c_game

__all__ = ["main"]


def main(game):
    #gamee = game
    #namee = game.player.name

    with open('./dork/saves/'+game.player.name+'.yml', 'w') as my_yaml_file:
        yaml.dump(game, my_yaml_file, default_flow_style=False)

    print("The game data has been saved in a file called "+game.player.name+".yml")


def mainn(game):

    data = yaml_parse.load("/current_game/currentgame")
    # print(data)

    current_room = game.player.current_room

    current_inventory = game.player.inventory

    current_name = game.player.name

    data["players"]["hero"]["name"] = current_name
    data["players"]["hero"]["location"] = current_room.name
    # data["players"]["hero"]["inventory"] = current_inventory.items

    with open('./dork/saves/'+game.player.name+'.yml', 'w') as my_yaml_file:
        yaml.dump(data, my_yaml_file, default_flow_style=False)

    print("The game data has been saved in a file called "+game.player.name+".yml")
