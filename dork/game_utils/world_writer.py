"""saves a game world from a yaml file
"""
import yaml


def save_gamee(game):
    """Save a game instance.
    """

    data = game.dataaa

    current_room = game.hero.location.name #PLAYER LOCATION

    current_name = game.hero.name #PLAYER NAME

    player_inventory = game.hero.items #PLAYER INVENTORY (DICT OF ITEMS)

    data["players"]["hero"]["name"] = current_name
    rooms_list = data["rooms"]

    data["players"]["hero"]["location"] = current_room

    print(player_inventory)
    if player_inventory is not None:
        for item in player_inventory:
            for number in range(1, len(player_inventory)):
                data["players"]["hero"]["inventory"][number]["name"] = item.name
                data["players"]["hero"]["inventory"][number]["description"] = item.description
                data["players"]["hero"]["inventory"][number]["stats"] = item.stats
                number += 1

    if current_room != "entrance":
        data["rooms"][2]["players"] = []


    for room in rooms_list:
        if rooms_list[room]["name"] == current_room:
            data["rooms"][room]["players"] = [current_name]

    with open('./dork/saves/'+current_name+'.yml', 'w') as my_yaml_file:
        yaml.dump(data, my_yaml_file, default_flow_style=False)

    return "Your game was saved as: " + game.hero.name + ".yml"
