"""Returns yaml data as a dict"""
import yaml


__all__ = ["load"]


def load(file_name):
    """Loads yaml data from the given file_name.
    \nArguments:
        file_name {String} -- [format: file_name (no extension)]
    \nReturns:
        {dict} -- [Returns a dictionary object holding YAML data]
    """

    file_path = f"./dork/{file_name}"
    with open(file_path) as file:
        data = yaml.safe_load(file.read())
    return data
