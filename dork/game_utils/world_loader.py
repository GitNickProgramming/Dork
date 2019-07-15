"""Loads a game world from a yaml file
"""
import os
import yaml


__all__ = ["main"]


def _load(file_name):
    file_path = f"./dork/saves/{file_name}"
    with open(file_path) as file:
        data = yaml.safe_load(file.read())
    return data


def main(player):
    """
    Loads yaml data from the file {player}.yml.

        Arguments:
            player {String}: file name to open (no extension)

        Returns:
            {dict}: containing all YAML data
    """

    save_files = []
    with os.scandir('./dork/saves') as saves:
        for entry in saves:
            save_files.append(entry.name.strip(".yml"))
    if player in save_files:
        file_to_load = player
    else:
        file_to_load = "generics"
    return _load(file_to_load + ".yml")
