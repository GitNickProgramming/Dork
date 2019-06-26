"""Loads a game world from a yaml file
"""

import os
import dork.types as dork_types
import dork.game_utils.yaml_parser as yml_parse


__all__ = ["main"]


def _create_game(file_name="yaml/default_world"):
    data = yml_parse.load(file_name)
    new_worldmap = _create_worldmap(data["rooms"])
    new_player = _create_player(player=data["player character"], worldmap=new_worldmap)
    game = dork_types.Game(player=new_player, worldmap=new_worldmap)
    if not game.player.name:
        game.player.name = input("What's your name, stranger? ")
    return game


def _create_worldmap(data):
    worldmap = dork_types.Worldmap()
    for room in data:
        this_room = data[room]
        new_room = dork_types.Room(this_room)
        new_room.name = room
        worldmap.rooms[room] = new_room
    return worldmap


def _create_player(player, worldmap):
    new_player = dork_types.Player(
        name=player["name"],
        start=worldmap.rooms[player["location"]]
    )
    inventory = player["inventory"]
    for item in inventory:
        new_player.inventory.items[item] = inventory[item]
    new_player.equipped = new_player.inventory.items["equipped"]
    return new_player


def _get_saves():
    save_files = []
    with os.scandir('./dork/saves') as saves:
        for entry in saves:
            save_files.append(entry.name)
    return save_files


def _get_file(save_files):
    print("Which save game would you like to load?")
    for save in save_files:
        print(save)
    game_to_load = input("> ")
    if game_to_load + ".yml" in save_files:
        file_to_load = "saves/" + game_to_load
        out = file_to_load, True
    else:
        out = "", False
    return out


def main(new_game=True):
    """Returns an instance of a game
    """
    if new_game:
        game = _create_game()
    else:
        save_files = _get_saves()
        while True:
            file_to_load, should_exit = _get_file(save_files)
            if should_exit:
                break
            else:
                print("That file doesn't exist, please try again.")
        game = _create_game(file_to_load)
    return game
