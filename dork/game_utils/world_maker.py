"""Loads a game world from a yaml file
"""
import os
import yaml


def load_game(player_name):
    """Loads a save file if present
    """
    save_files = []

    with os.scandir('./dork/saves') as saves:
        for entry in saves:
            save_files.append(entry.name)
    if player_name + ".yml" in save_files:
        print(f"{player_name}'s game was loaded successfully!")
        file_name = player_name + ".yml"
    else:
        print(
            f"\nThat file didn't exist! Creating new player: {player_name}"
        )
        file_name = "default_world.yml"

    with open(f"./dork/saves/{file_name}") as file:
        data = yaml.safe_load(file.read())

    return data


def save_game(game):
    """Save a game instance. If the save file is not present, one is created
    """
    with open("./dork/saves/" + game.hero.name + ".yml", "w") as save_file:
        yaml.dump(game, save_file, default_flow_style=False)

    return "Your game was saved as: " + game.hero.name + ".yml"
