"""Loads a game world from a yaml file
"""
import os
import yaml


__all__ = ["main"]


def _load(file_name):
    """Loads yaml data from the given file_name.
    \nArguments:
        file_name {String} -- [format: file_name (no extension)]
    \nReturns:
        {dict} -- [Returns a dictionary object holding YAML data]
    """

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
    return _load(file_to_load + ".yml"), _load(file_to_load + ".yml")
