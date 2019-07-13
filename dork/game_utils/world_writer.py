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
    data["players"]["hero"]["location"] = current_room
    # data["players"]["hero"]["inventory"] = current_inventory
    # data["players"]["hero"][]

    with open('./dork/saves/'+current_name+'.yml', 'w') as my_yaml_file:
        yaml.dump(data, my_yaml_file, default_flow_style=False)

    return "Your game was saved as: " + game.hero.name + ".yml"
