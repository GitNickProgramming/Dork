"""saves a game world from a yaml file
"""
import yaml


def save_gamee(game):
    """Save a game instance.
    """

    data = game.dataaa

    current_room = game.hero.location.name

    current_name = game.hero.name

    player_inventory = game.hero.items

    data["players"]["hero"]["name"] = current_name
    rooms_list = data["rooms"]

    data["players"]["hero"]["location"] = current_room

    numb = 0

    if player_inventory is not None:
        for item in player_inventory:
            if item is not None:
                if numb == 0:
                    continue
                data["players"]["hero"]["inventory"][numb]["name"] \
                    = player_inventory[item].name
                data["players"]["hero"]["inventory"][numb]["description"]\
                    = player_inventory[item].description
                data["players"]["hero"]["inventory"][numb]["stats"] \
                    = player_inventory[item].stats
            if numb < len(player_inventory)-1:
                numb += 1

    if current_room != "entrance":
        data["rooms"][2]["players"] = []

    for room in rooms_list:
        if rooms_list[room]["name"] == current_room:
            data["rooms"][room]["players"] = [current_name]

    with open('./dork/saves/'+current_name+'.yml', 'w') as my_yaml_file:
        yaml.dump(data, my_yaml_file, default_flow_style=False)

    return "Your game was saved as: " + game.hero.name + ".yml"
