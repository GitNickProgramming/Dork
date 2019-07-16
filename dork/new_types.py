"""Base types for the Dork game"""

import os
import yaml
import matplotlib.pyplot as plt
from dork.game_utils.maze_factory import main as MazeFactory
# from dork.game_utils.item_factory import main as ItemFactory
# from dork.game_utils.npc_factory import main as NPCFactory
# from dork.game_utils.room_factory import main as RoomFactory


class Holder:
    """A holder/container of items"""

    def __init__(self):
        self.items = dict()

    def get_items(self, verbose):
        """Print all inventory items"""

        out = "Inventory:" if self.items else "There's nothing in here."
        for item in self.items:
            this = self.items[item]
            desc = f":\n    {this.description}" if verbose else ""
            eqpd = " (equipped)" if hasattr(this, "equipped") else ""
            amt = this.stats.get("amount", None)
            amt = f" ({amt})" if amt else ""
            out += f"\n  {item}{eqpd}{amt}{desc}"
        return out


class Item:
    """An obtainable/usable item"""

    def __init__(self):
        self.name = str
        self.description = str
        self.location = Holder


class Player(Holder):
    """A player or npc in the game"""

    def __init__(self):
        super().__init__()
        self.name = str
        self.description = str
        self.location = Room


class Room(Holder):
    """A room on the worldmap"""

    def __init__(self):
        super().__init__()
        self.name = str
        self.description = str
        self.location = tuple


class Hero(Player):
    """The hero of the game"""

    # def __init__(self):
    #     super().__init__()


class Maze:
    """Generate a maze with rooms on intersections, corners, and dead-ends"""

    @staticmethod
    def draw(maze):
        """Show an image of the generated maze"""

        x_axis = len(maze[0])//2
        y_axis = len(maze)//2
        plt.figure(figsize=(x_axis, y_axis))
        plt.pcolormesh(maze, cmap=plt.cm.get_cmap("tab20b"))
        plt.axis("equal")
        plt.axis("off")
        plt.ion()
        plt.show()

    @staticmethod
    def update(maze):
        """Update the map display"""

        x_axis = len(maze[0])//2
        y_axis = len(maze)//2
        plt.figure(figsize=(x_axis, y_axis))
        plt.pcolormesh(maze, cmap=plt.cm.get_cmap("tab20b"))
        plt.axis("equal")
        plt.axis("off")
        plt.draw()


class Worldmap:
    """Contains a maze and the rooms within"""


class Gamebuilder:
    """Gamebuilder"""

    @staticmethod
    def factory(obj, **kwargs):
        """Instantiate and return a new game object of type {obj}"""

        new_obj = obj()
        setattr(new_obj, "data", kwargs)
        for key, val in kwargs.items():
            setattr(new_obj, key, val)
        return new_obj

    @staticmethod
    def load_game(player):
        """Load the save file associated with player"""

        save_files = []
        with os.scandir("./dork/saves") as saves:
            for entry in saves:
                save_files.append(entry.name.strip(".yml"))
        if player in save_files:
            file_path = f"./dork/saves/{player}.yml"
            with open(file_path) as file:
                data = yaml.safe_load(file.read())
        else:
            data = dict()
        return data

    @staticmethod
    def save_game(data):
        """Save a game instance to a yaml file if it exists, else create one"""
        game_state = {
            "maze": data.maze.maze,
            "worldmap": data.worldmap,
            "hero": {
                "location": data.hero.location,
                "equipped": data.hero.equipped,
                "items": data.hero.items,
            }
        }

        file_name = f"./dork/saves/{data.hero.name}.yml"
        with open(file_name, "w") as save_file:
            yaml.dump(game_state, save_file, default_flow_style=False)

        return f"Your game was successfully saved as {data.hero.name}.yml!"


class Game(Gamebuilder, Worldmap):
    """A container for holding a game state"""
    player_draw_color = -5
    verbose = False

    def __init__(self):
        super().__init__(Gamebuilder, Maze)
        player_name = input("What's your name, stranger? ")
        self.game_data = self.load_game(player_name)

        if not self.game_data:
            self.maze = self.factory(Maze, **MazeFactory())



            # base_type, type_factory = val
            # this_type = self.factory(base_type, **type_factory)
            # self.game_data[key] = this_type

        # else:
        #     pass








# godhusher = {
#     "name": "godhusher",
#     "type": "legendary",
#     "stats": {
#         "attack": 113,
#         "weight": 14,
#         "luck": 24,
#     },
# }

# boss = {
#     "name": "boss",
#     "description": "OMG THERE"S A TROLL IN HERE!",
#     "items": {
#         "only friend": "sword",
#         "wobblelobbledobdob": "wobbly sword"
#     },
#     "adjacent": {
#         "north": "gold",
#         "south": "entrance",
#         "east": "cave",
#         "west": "armory"
#     }
# }

# gamebuilder = Gamebuilder()

# exist_item = gamebuilder.factory(Item, **godhusher)
# boss_room = gamebuilder.factory(Room, **boss)

# file_name = "./dork/saves/test.yml"
# with open(file_name, "w") as save_file:
#     for obj in [exist_item, boss_room]:
#         name = obj.data.pop("name")
#         obj_dict = {name: obj.data}
#         yaml.dump(obj_dict, save_file, default_flow_style=False)
