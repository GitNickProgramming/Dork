"""Base types for the Dork game"""

import os
import yaml
import matplotlib.pyplot as plt
from dork.game_utils.maze_factory import main as MazeFactory


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


class Worldmap:
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
    def save_game(player, data):
        """Save a game instance to a yaml file if it exists, else create one"""

        data = {
            "maze": data.maze,
            "rooms": data.rooms,
            "players": data.players,
        }

        file_name = f"./dork/saves/{player}.yml"
        with open(file_name, "w") as save_file:
            yaml.safe_dump(data, save_file, default_flow_style=False, indent=4)

        return f"Your game was successfully saved as {player}.yml!"


class Game(Gamebuilder):
    """A container for holding a game state"""
    player_draw_color = -5
    verbose = False

    def __init__(self):
        super().__init__()
        player_name = input("What's your name, stranger? ")
        load_data = self.load_game(player_name)

        if not load_data:
            self.worldmap = self.factory(Worldmap, **MazeFactory())
            hero = {
                "name": player_name,
                "description": "the hero of dork!",
                "locataion": self.worldmap.rooms.get(
                    list(self.worldmap.rooms.keys())[0]
                ),
                "items": {},
                "equipped": {}
            }
            self.worldmap.data["hero"] = hero
            self.hero = self.factory(Hero, **hero)
            self.save_game(player_name, self.worldmap)
            # from pprint import pprint
            # pprint(self.worldmap.players)
            # pprint(self.worldmap.maze)
            # pprint(self.worldmap.rooms)
            # pprint(self.worldmap.data)
