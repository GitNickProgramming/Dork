"""saves a game world from a yaml file
"""
import yaml


def save_gamee(game):
    """Save a game instance.
    """

    data = game.dataaa

    current_room = game.hero.location.name

    current_name = game.hero.name

    players_items_list = game.hero.items

    list_of_rooms_in_game = game.worldmap.rooms

    for items in players_items_list:
        data["players"]["hero"]["inventory"] = items

    data["players"]["hero"]["name"] = current_name
    rooms_list = data["rooms"]

    data["players"]["hero"]["location"] = current_room

    if current_room != "entrance":
        data["rooms"][2]["players"] = []

    for room in rooms_list:
        if rooms_list[room]["name"] == current_room:
            data["rooms"][room]["players"] = [current_name]

    for roomm in list_of_rooms_in_game:
        rooms_item_list = roomm.items
        rooms_list

    #for room in rooms_list:
    #    rooms_item_list = room.items
    #    for itemm in rooms_item_list:
    #        data["rooms"][room]["items"] = itemm

    with open('./dork/saves/'+current_name+'.yml', 'w') as my_yaml_file:
        yaml.dump(data, my_yaml_file, default_flow_style=False)

    return "Your game was saved as: " + game.hero.name + ".yml"
