"""Returns yaml data as a dict"""
import yaml


__all__ = ["load"]


def load(file_name):
    """Loads yaml data from the given file_name.
    \nArguments:
        file_name {String} -- [format: folder_name/file_name]
    \nReturns:
        {dict} -- [Returns a dictionary object holding YAML data]
    """

    file_path = f"./{file_name}.yml"
    with open(file_path) as file:
        data = yaml.safe_load(file.read())
    return data
