"""saves a game world from a yaml file
"""
import yaml


def save_gamee(game):
    """Save a game instance.
    """

    #print(game.hero.items.keys())

    data = game.dataaa

    current_room = game.hero.location.name #PLAYER LOCATION

    current_name = game.hero.name #PLAYER NAME

    player_inventory = game.hero.items #PLAYER INVENTORY (DICT OF ITEMS)

    #list_of_rooms = game.worldmap.rooms #ALL ROOMS IN GAME

    data["players"]["hero"]["name"] = current_name
    rooms_list = data["rooms"] #ALL ROOMS IN YAML TO DICT

    data["players"]["hero"]["location"] = current_room

    number = 0

    if player_inventory is not None:
        for item in player_inventory:
            if item is not None:
                if number == 0:
                    continue
                data["players"]["hero"]["inventory"][number]\
                    ["name"] = player_inventory[item].name
                data["players"]["hero"]["inventory"][number]\
                    ["description"] = player_inventory[item].description
                data["players"]["hero"]["inventory"][number]\
                    ["stats"] = player_inventory[item].stats
            if number < len(player_inventory)-1:
                 number += 1 



    if current_room != "entrance":
        data["rooms"][2]["players"] = []


    for room in rooms_list:
        if rooms_list[room]["name"] == current_room:
            data["rooms"][room]["players"] = [current_name]

    with open('./dork/saves/'+current_name+'.yml', 'w') as my_yaml_file:
        yaml.dump(data, my_yaml_file, default_flow_style=False)


    #print(game.hero.items.keys())

    return "Your game was saved as: " + game.hero.name + ".yml"



