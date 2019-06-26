"""Loads a game world from a yaml file
"""

import os
import dork.types as dork_types
import dork.game_utils.yaml_parser as yml_parse


__all__ = ["main"]


def _create_game(file_name="yaml/default_world"):
    data = yml_parse.load(file_name)
    game = dork_types.Game()
    game.worldmap = _create_worldmap(data["rooms"])
    game.player = _create_player(data)
    if not game.player.name:
        game.player.name = input("What's your name, stranger?\n")
    return game


def _create_worldmap(data):
    worldmap = {}
    for room in data:
        new_room = dork_types.Room(
            adjacent=room["adjacent"],
            description=room["description"],
            npcs=room["npcs"],
            items=room["items"],
            clues=room["clues"]
        )
        worldmap[room] = new_room
    return worldmap


def _create_player(data):
    rooms = data["rooms"]
    player = data["player"]
    new_player = dork_types.Player(
        name=player["name"],
        start=rooms[player["location"]]
    )
    inventory = data["inventory"]
    for item in inventory:
        new_player.inventory.items[item] = inventory[item]
    new_player.equipped = new_player.inventory.items["equipped"]
    return new_player


def _get_saves():
    save_files = []
    with os.scandir('../../../saves') as saves:
        for entry in saves:
            save_files.append(entry.name)
    return save_files


def _get_file(save_files):
    print("Which save game would you like to load?")
    for save in save_files:
        print(save)
    game_to_load = input("> ")
    if game_to_load in save_files:
        file_to_load = "../../../saves/" + game_to_load
        out = file_to_load, True
    else:
        out = "", False
    return out


def main():
    """Returns an instance of a game
    """
    save_files = _get_saves()
    if save_files:
        while True:
            file_to_load, should_exit = _get_file(save_files)
            if should_exit:
                break
            else:
                print("That file doesn't exist, please try again.")
        game = _create_game(file_to_load)
    else:
        game = _create_game()
    return game
