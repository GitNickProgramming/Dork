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


class Stats:
    """stats for items"""


class Adjacent:
    """adjacency object for rooms"""


class Item(Stats):
    """An obtainable/usable item"""
    def __init__(self):
        super().__init__()


class Player(Holder):
    """A player or npc in the game"""
    def __init__(self):
        super().__init__()


class Room(Adjacent, Holder):
    """A room on the worldmap"""
    def __init__(self):
        super().__init__()


class Hero(Player):
    """The hero of the game"""
    def __init__(self):
        super().__init__()


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


class Game(Maze):
    """A container for holding a game state"""
    player_draw_color = -5
    verbose = False

    def __init__(self):
        super().__init__()


class Gamebuilder:
    """Gamebuilder"""

    def __init__(self):
        player_name = input("What's your name, stranger? ")
        game_data = self.load_game(player_name)

        if not game_data:
            game_data = MazeFactory()
            hero = {
                "name": player_name,
                "description": "the hero of dork!",
                "location": game_data["rooms"].get(
                    list(game_data["rooms"].keys())[0]
                ),
                "items": {},
                "equipped": {}
            }
            hero_location = hero["location"]
            hero_location["players"][player_name] = hero
            self.save_game(player_name, game_data)

        from pprint import pprint
        pprint(game_data["maze"])
        Maze.draw(game_data["maze"])

    # def build(self) -> Game:

    #     factories = {
    #         "hero": Hero,
    #         "rooms": Room,
    #         "players": Player,
    #         "items": Item,
    #         "stats": Stats,
    #         "adjacent": Adjacent,
    #     }


    #     return new_game

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
            "rooms": data["rooms"],
            "maze": data["maze"],
            # "hero": data["hero"],
            # "players": data["players"],
        }

        file_name = f"./dork/saves/{player}.yml"
        with open(file_name, "w") as save_file:
            yaml.safe_dump(
                data, save_file,
                indent=4, width=80,
                default_flow_style=False
            )

        return f"Your game was successfully saved as {player}.yml!"
