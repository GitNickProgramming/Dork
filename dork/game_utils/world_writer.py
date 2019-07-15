"""saves a game world from a yaml file
"""
import yaml


def save_gamee(game):
    """Save a game instance.
    """

    data = game.dataaa

    current_room = game.hero.location.name

    # current_inventory = game.hero.inventory

    # current_equipped = game.hero.equipped

    current_name = game.hero.name

    data["players"]["hero"]["name"] = current_name
    rooms_list = data["rooms"]

    data["players"]["hero"]["location"] = current_room

    if current_room != "entrance":
        data["rooms"][2]["players"] = []


    for room in rooms_list:
        if rooms_list[room]["name"] == current_room:
            data["rooms"][room]["players"] = [current_name]

    # data["players"]["hero"]["inventory"] = current_inventory

    with open('./dork/saves/'+current_name+'.yml', 'w') as my_yaml_file:
        yaml.dump(data, my_yaml_file, default_flow_style=False)

    return "Your game was saved as: " + game.hero.name + ".yml"
