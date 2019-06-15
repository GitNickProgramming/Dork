"""
Python Yaml parser using dictionaries and iterators.
https://www.w3schools.com/python/python_dictionaries.asp -- dictionaries info
https://www.w3schools.com/python/ref_keyword_in.asp -- info on keyword `in'

This code will be heavily commented for descriptive learning purposes.
DO NOT DO THIS in production code. You will be shamed.
"""

from pprint import pprint  # more formatted data "pretty" printing.
import yaml

CARDINALS = ["north", "east", "south", "west"]
PATHS = ["entrances", "exits"]
# DESC = ["description"]


def _load_data(file_name_and_path="./parsers/yaml/dork.yml"):  # lookup default args
    with open(file_name_and_path) as file:  # with keyword is a context manager
        data = yaml.safe_load(file.read())  # ./yaml/dork.yml is a valid file

    # data is now available in the current scope.
    # file is removed after the with (closed) for record keeping

    return data


def _check_path(rooms, name, direction, path):
    room = rooms[name][path]
    if direction not in room:
        print(f"{name} does not have {direction} as a key.")
    elif room[direction] is None:
        print(f"There is no {path.strip('s')} {direction} of {name}.")
    elif room[direction] not in rooms:
        print(f"Going {direction} of {name} leads to an error!")
    else:
        other = room[direction]
        print(f"{other} is an {path.strip('s')} {direction} of {name}.")


def main():
    """Main point of entry.
    Loads data. Checks if it is valid. And Parses it.
    """
    data = _load_data()
    print("loaded this data: ")
    pprint(data)

    print("\nChecking that 'data' contains a dictionary of rooms... \n")
    if "Rooms" not in data:
        print("No Rooms found.")
        return

    if not isinstance(data["Rooms"], dict):
        print("Rooms in data was not proper data.")
        return

    rooms = data["Rooms"]
    for name in rooms:  # this is a dictionary key iterator
        for path in PATHS:
            for direction in CARDINALS:
                _check_path(rooms, name, direction, path)
        print("")


if __name__ == "__main__":
    main()
