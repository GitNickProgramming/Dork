"""Returns yaml data as a dict"""

import yaml

__all__ = ["load", "save"]

def load(file_name):
    """Loads yaml data from the given file_name"""

    file_path = f"./dork/dork_utils/yaml/{file_name}.yml"
    with open(file_path) as file:
        data = yaml.safe_load(file.read())
    return data

# TODO: FIGURE OUT HOW TO CONVERT BACK TO YAML
def save(data, file_name):
    """Saves 'data' to 'file_name'"""
