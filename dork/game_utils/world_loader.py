"""Loads a game world from a yaml file
"""
import os


__all__ = ["main"]


def main(player_name):
    """Returns an instance of a game
    """
    save_files = []
    with os.scandir('./dork/saves') as saves:
        for entry in saves:
            save_files.append(entry.name)
    if player_name + ".yml" in save_files:
        file_to_load = "saves/" + player_name
    else:
        file_to_load = "yaml/default_world"
    return file_to_load + ".yml"
