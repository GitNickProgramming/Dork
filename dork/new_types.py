"""Base types for the Dork game"""

import os
import yaml
import matplotlib.pyplot as plt
from dork.game_utils.maze_factory import main as MazeFactory


class Grandparent:
    """grandparent class of holder and adjacent"""


class Holder(Grandparent):
    """A holder/container of items"""

    def __init__(self):
        super().__init__()
        self.inventory = dict()

    def get_items(self, caller, verbose):
        """Print all inventory items"""

        if self.inventory:
            out = f"{caller}'s inventory:"
        else:
            out = f"There's nothing in {caller}'s inventory."

        for item in self.inventory:
            this = self.inventory[item]
            amt = this.stats.get("amount", None)
            desc = f":\n    {this.description}" if verbose else ""
            eqpd = " (equipped)" if hasattr(this, "equipped") else ""
            amt = f" ({amt})" if amt else ""
            out += f"\n  {item}{eqpd}{amt}{desc}"
        return out


class Stats:
    """stats for items"""


class Adjacent(Grandparent):
    """adjacency object for rooms"""

    def __init__(self):
        super().__init__()


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

    def __init__(self):
        self.maze = []

    def draw(self):
        """Show an image of the generated maze"""

        x_axis = len(self.maze[0])//2
        y_axis = len(self.maze)//2
        plt.figure(figsize=(x_axis, y_axis))
        plt.pcolormesh(self.maze, cmap=plt.cm.get_cmap("tab20b"))
        plt.axis("equal")
        plt.axis("off")
        plt.ion()
        plt.show()

    def update(self):
        """Update the map display"""

        x_axis = len(self.maze[0])//2
        y_axis = len(self.maze)//2
        plt.figure(figsize=(x_axis, y_axis))
        plt.pcolormesh(self.maze, cmap=plt.cm.get_cmap("tab20b"))
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
            hero_location = game_data["rooms"].get(
                list(game_data["rooms"].keys())[0]
            )
            hero = {
                "name": player_name,
                "description": "the hero of dork!",
                "location": hero_location,
                "items": {},
                "equipped": {}
            }
            hero_location["players"]["hero"] = hero
            self.save_game(player_name, game_data)

        self._build(game_data)

    def _build(self, data) -> Game:
        """recursively instantiate a game of Dork from dictionary"""

        factories = {
            "maze": Maze,
            "rooms": Room,
            "players": Player,
            "items": Item,
            "stats": Stats,
            "adjacent": Adjacent,
        }

        def _recursive_factory(inst, data):
            for field in data:
                if field not in factories:
                    setattr(inst, field, data[field])
                else:
                    setattr(
                        self.factory(
                            factories[field], **data[field]
                        ),
                        field, _recursive_factory(
                            factories[field], data[field]
                        )
                    )
        return _recursive_factory(Game, data)

    @staticmethod
    def factory(obj, **kwargs):
        """Instantiate and return a new game object of type {obj}"""

        new_obj = obj()
        # setattr(new_obj, "data", kwargs)
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
