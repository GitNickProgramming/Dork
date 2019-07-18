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

    def __init__(self):
        self.data = {}


class Adjacent(Grandparent):
    """adjacency object for rooms"""

    def __init__(self):
        super().__init__()
        self.data = {}
        self.adjacent = {}


class Item(Stats):
    """An obtainable/usable item"""

    def __init__(self):
        super().__init__()
        self.data = {}
        self.name = str
        self.description = str
        self.equipable = bool


class Player(Holder):
    """A player or npc in the game"""

    player_draw_color = -4

    def __init__(self):
        super().__init__()
        self.data = {}
        self.name = str
        self.description = str
        self.location = Room()
        self.equipped = {}

    def move(self, cardinal, maze):
        """walk this way"""

        location = self.location
        adjacent_room = getattr(location.adjacent, cardinal, None)
        if not adjacent_room:
            out = f"You cannot go {cardinal} from here."
        else:
            maze[location.x][location.y] = 2
            self.location = adjacent_room

            maze[location.x][location.y] = self.player_draw_color
            maze.update()

            out = self.location.description
        return out


class Room(Adjacent, Holder):
    """A room on the worldmap"""

    def __init__(self):
        super().__init__()
        self.data = {}
        self.name = str
        self.coordinates = list
        self.description = str
        self.coordinates = []


class Maze:
    """Generate a maze with rooms on intersections, corners, and dead-ends"""

    def __init__(self):
        self.maze = []
        self.rooms = {}

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
    """An instance of Dork"""

    verbose = False

    def __init__(self):
        super().__init__()
        self.data = {}
        self.hero = Player()

    def __call__(self, cmd, arg):
        return getattr(self, cmd)(arg) if arg else getattr(self, cmd)()

    def _gtfo(self):
        return f"Thanks for playing DORK, {self.hero.name}!", True

    def _draw_maze(self):
        self.draw()
        return "", False

    def _move(self, cardinal):
        return self.hero.move(cardinal, self.maze), False

    def _examine(self):
        return self.hero.location.get_items(
            self.hero.location.name, self.verbose
        ), False

    def _inventory(self):
        return self.hero.get_items(self.hero.name, self.verbose), False

    @staticmethod
    def _repl_error(arg):
        return f"{arg}", False


class Gamebuilder:
    """Build an instance of Game"""

    def __init__(self):
        player_name = input("What's your name, stranger? ")
        self.data = self._load_game(player_name)

        if not self.data:
            self.data = MazeFactory()
            hero_location = self.data["rooms"].get(
                list(self.data["rooms"].keys())[0]
            )
            hero = {
                "name": player_name,
                "description": "the hero of dork!",
                "location": hero_location,
                "items": {},
                "equipped": {}
            }
            hero_location["players"]["hero"] = hero
            self._save_game(player_name, self.data)

        self.game = self._build(**self.data)

    @staticmethod
    def _build(**data) -> Game:
        """recursively instantiate a game of Dork from dictionary"""

        factories = {
            "rooms": Room,
            "players": Player,
            "items": Item,
            "stats": Stats,
            "adjacent": Adjacent,
        }

        def rec_fac(clz, **data):
            new_obj = clz()
            setattr(new_obj, "data", data)
            print(new_obj)
            for key, val in data.items():
                if key in factories:
                    setattr(new_obj, key, rec_fac(factories[key], **val))
                else:
                    setattr(new_obj, key, val)
            return new_obj
        return rec_fac(Game, **data)

    @staticmethod
    def _load_game(player):
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
    def _save_game(player, data):
        """Save a game instance to a yaml file if it exists, else create one"""

        data = {
            "rooms": data["rooms"],
            "maze": data["maze"],
        }

        file_name = f"./dork/saves/{player}.yml"
        with open(file_name, "w") as save_file:
            yaml.safe_dump(
                data, save_file,
                indent=4, width=80,
                # default_flow_style=False
            )

        return f"Your game was successfully saved as {player}.yml!"
