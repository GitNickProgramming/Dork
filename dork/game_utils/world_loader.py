"""Loads a game world from a yaml file
"""
import os
<<<<<<< HEAD
import dork.types as dork_types
import dork.game_utils.yaml_parser as yml_parse
=======
>>>>>>> 611451d9783fd45d7d397675dffd023fcb048680
import yaml


__all__ = ["main"]


<<<<<<< HEAD
dataa = dict()


def _create_game(file_name="yaml/default_world"):
    data = yml_parse.load(file_name)
    new_worldmap = _create_worldmap(data["rooms"])
    new_player = _create_player(
        player=data["players"]["hero"], worldmap=new_worldmap
    )
    game = dork_types.Game(player=new_player, worldmap=new_worldmap)
    if not game.player.name:
        game.player.name = input("What's your name, stranger? ")
    current_game(data)
    return game


def current_game(data):
    #gamee = game
    #namee = game.player.name

    with open('./dork/current_game/'+"currentgame"+'.yml', 'w') as my_yaml_file:
        yaml.dump(data, my_yaml_file, default_flow_style=False)
    print("worked")
    return ""


def _create_worldmap(data):
    worldmap = dork_types.Worldmap()
    for room in data:
        new_room = dork_types.Room(room=data[room], name=room)
        worldmap.rooms[room] = new_room
    return worldmap

=======
def _load(file_name):
    """Loads yaml data from the given file_name.
    \nArguments:
        file_name {String} -- [format: file_name (no extension)]
    \nReturns:
        {dict} -- [Returns a dictionary object holding YAML data]
    """
>>>>>>> 611451d9783fd45d7d397675dffd023fcb048680

    file_path = f"./dork/saves/{file_name}"
    with open(file_path) as file:
        data = yaml.safe_load(file.read())
    return data


def main(player_name):
    """Returns an instance of a game
    """
    save_files = []
    with os.scandir('./dork/saves') as saves:
        for entry in saves:
            save_files.append(entry.name)
    if player_name + ".yml" in save_files:
        file_to_load = player_name
    else:
        file_to_load = "default_world"
    return _load(file_to_load + ".yml")
