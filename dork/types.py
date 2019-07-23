"""Base types for the Dork game"""
# -*- coding: utf-8 -*-

import os
from abc import ABC, abstractmethod
from copy import deepcopy
from random import choices, choice, randint, shuffle
from operator import add
import yaml
import matplotlib.pyplot as plt
from numpy import full as npf
import dork.game_utils.factory_data as factory_data
# pylint: disable=protected-access


class Grandparent:
    """common parent of holder, adjacent, and coord"""


class Holder(Grandparent):
    """A holder/container of items"""

    def __init__(self):
        super().__init__()
        self.inventory = {}

    def get_items(self, verbose):
        """Print all inventory items"""

        if self.inventory:
            out = f"\nInventory"
        else:
            out = f"There's nothing here."

        for name, item in self.inventory.items():
            out += f"\n    {name}"
            if verbose:
                out += Game._verbose_print(vars(item))
            else:
                out += Game._brief_print(vars(item))
        return out


class Usable(ABC):
    """Abstract class of use behavior in items use method"""

    @staticmethod
    @abstractmethod
    def use(target, name):
        """Strategy pattern inspired by refactoring.guru
        use method defaults to doing nothing"""


class Attackable(Usable):
    """Any object that can be swung will say it was swung"""

    @staticmethod
    def use(target, name):
        """Swing use method"""
        print("You swing the " + name + " at " + target)


class NotUsable(Usable):
    """Any object that cannot be used"""

    @staticmethod
    def use(target, name):
        """Useless use method"""
        print("You find no use of this item")


class Openable(Usable):
    """Object opening behavior class"""

    @staticmethod
    def use(target, name):
        """Opens object targeted if possible"""
        print("You insert the " + name + " into " + target)


class Payable(Usable):
    """Any object that can be used as gold"""

    @staticmethod
    def use(target, name):
        """Gold use method"""
        print("You use the " + name + " to pay " + target)


class Puzzleable(Usable):
    """Any object that can be used in a puzzle"""

    @staticmethod
    def use(target, name):
        """Puzzle use method"""
        print("You try to fit the " + name + " into the " + target)


class Statable(Usable):
    """Any object that can change stats"""

    @staticmethod
    def use(target, name):
        """Stat change use method"""
        print("The " + name + " takes effect on " + target)


class Stats:
    """stats for items"""

    def __init__(self):
        self.attack = int
        self.strength = int
        self.weight = int
        self.luck = int
        self.equipable = bool


class Adjacent(Grandparent):
    """adjacency object for rooms"""

    def __init__(self):
        super().__init__()
        self.north = str
        self.south = str
        self.east = str
        self.west = str


class Coord(Grandparent):
    """coordinate object for rooms"""

    def __init__(self):
        super().__init__()
        self.x = int
        self.y = int


class Item(Stats):
    """An obtainable/usable item"""

    def __init__(self):
        super().__init__()
        self.description = str
        self.type = str


class Player(Holder):
    """A player or npc in the game"""

    instances = []

    def __init__(self):
        super().__init__()
        self.name = str
        self.description = str
        self.location = Room
        self.equipped = list
        self.instances.append(self)

    def move(self, cardinal, maze):
        """walk this way"""

        adjacent_room = getattr(self.location, cardinal)

        if not adjacent_room:
            out = f"You cannot go {cardinal} from here."
        else:
            maze[self.location.x][self.location.y] = MazeFactory.room_color

            adjacent_room.players[self.name] = \
                self.location.players.pop(self.name)
            self.location = adjacent_room
            maze[self.location.x][self.location.y] = MazeFactory.player_color

            out = self.location.description
            MazeFactory.update(maze)
        return out


class Room(Adjacent, Coord, Holder):
    """A room on the worldmap"""

    instances = []

    def __init__(self):
        super().__init__()
        self.description = str
        self.players = {}
        self.instances.append(self)


class Gamebuilder:
    """Build an instance of Game"""

    attr_factories = {
        "adjacent": Adjacent,
        "coordinates": Coord,
        "stats": Stats,
    }

    dict_factories = {
        "players": Player,
        "inventory": Item,
    }

    @staticmethod
    def build(player_name):
        """Instantiate a game of Dork from dictionary"""

        data = Gamebuilder.load_game(player_name)

        if not data:
            data = MazeFactory.build()

            hero_data = {
                "name": player_name,
                "description": "the hero of dork!",
                "location": "room 0",
                "inventory": {},
                "equipped": []
            }

            data["rooms"]["room 0"]["players"][player_name] = hero_data

        game = Game()
        setattr(game, "maze", data["maze"])
        setattr(game, "rooms", Gamebuilder._make_rooms(data["rooms"]))

        Gamebuilder._place_players(game)
        Gamebuilder._make_paths(game)

        for player in Player.instances:
            if player.name == player_name:
                hero = player

        game.hero = hero
        game.maze[hero.location.x][hero.location.y] = MazeFactory.player_color
        return game

    @staticmethod
    def _place_players(game):
        for _, room in game.rooms.items():
            for _, player in room.players.items():
                player.location = room

    @staticmethod
    def _make_paths(game):
        adj = ["north", "south", "east", "west"]
        for _, room in game.rooms.items():
            for direction in adj:
                this_adj = getattr(room, direction)
                setattr(room, direction, game.rooms.get(this_adj, None))

    @staticmethod
    def _make_rooms(rooms):
        for name, room in rooms.items():
            new_room = Gamebuilder._rec_inst(Room, **room)
            rooms[name] = new_room
        return rooms

    @staticmethod
    def _set_attrs(obj, **data):
        for key, val in data.items():
            setattr(obj, key, val)
        return obj

    @staticmethod
    def _rec_inst(clz, **data):
        new_obj = clz()
        for key, val in data.items():
            if key in Gamebuilder.dict_factories:
                for sub in val:
                    new_sub = Gamebuilder._rec_inst(
                        Gamebuilder.dict_factories[key], **val[sub]
                    )
                    getattr(new_obj, key)[sub] = new_sub
            elif key in Gamebuilder.attr_factories:
                for sub_key, sub_val in val.items():
                    setattr(new_obj, sub_key, sub_val)
            else:
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
            data = {}
        return data

    @staticmethod
    def save_game(player, data):
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
            )

        return f"Your game was successfully saved as {player}.yml!"


class Game:
    """An instance of Dork"""

    verbose = False

    def __init__(self):
        self.maze = []
        self.rooms = {}
        self.hero = Player()

    def __call__(self, cmd, arg):
        return getattr(self, cmd)(arg) if arg else getattr(self, cmd)()

    def _toggle_verbose(self) -> (str, bool):
        self.verbose = not self.verbose
        out = {
            True: "verbose inventory: ON",
            False: "verbose inventory: OFF"
        }[self.verbose]
        return out, False

    def _gtfo(self):
        return f"Thanks for playing DORK, {self.hero.name}!", True

    def _draw_maze(self):
        MazeFactory.draw(self.maze)
        return "", False

    def _move(self, cardinal):
        return self.hero.move(cardinal, self.maze), False

    def _examine(self):
        return self.hero.location.get_items(self.verbose), False

    def _inventory(self):
        return self.hero.get_items(self.verbose), False

    def _look(self, x="n"):
        if x == "around":
            items = self.hero.location.items
            print("\nItems:")
            for item in items:
                print(item)
            print()
        return self.hero.location.description, False

    def _start_over(self):
        if self._confirm():
            out = ""
        else:
            out = "Guess you changed your mind!"
        return out, False

    @staticmethod
    def _verbose_print(data, calls=2):
        out = ""
        spc = "    "
        for key, val in data.items():
            if isinstance(val, dict):
                out += "\n" + spc*calls + \
                    f"{key}:{Game._verbose_print(val, calls+1)}"
            elif val:
                out += "\n" + spc*calls + f"{key}: {val}"
        return out

    @staticmethod
    def _brief_print(data, calls=2):
        out = ""
        col = ""
        spc = "    "
        for key, val in data.items():
            if isinstance(val, dict) and calls < 3:
                if calls < 2:
                    col = ":"
                out += "\n" + spc*calls + \
                    f"{key}{col}{Game._brief_print(val, calls+1)}"
        return out

    @staticmethod
    def _confirm():
        print("\n!!!WARNING!!! You will lose unsaved data!\n")
        conf = False
        while True:
            conf = str.casefold(
                input("Would you like to proceed? Y/N: ")
            )
            conf = {
                "y": True,
                "n": False
            }.get(conf, None)
            if conf is None:
                print("That is not a valid response!")
            else:
                break
        return conf

    @staticmethod
    def _repl_error(arg):
        return f"{arg}", False

    @staticmethod
    def _zork():
        return "holy *%&#@!!! a wild zork appeared!", False


class ItemFactory:
    """Generates a random named item with randomized stats"""

    items = factory_data.ITEMS
    names = factory_data.NAMES
    sequence = factory_data.SEQUENCE

    types = items["types"]
    condition = items["condition"]
    material = items["material"]

    posessive = names["posessive"]
    nonposessive = names["nonposessive"]
    suffixes = names["suffixes"]
    abstract = names["abstract"]
    adjectives = names["adjectives"]

    @staticmethod
    def build(weights=None):
        """generate a random item"""

        weights = {
            "player": [8, 0, 0, 7, 5, 10]
        }.get(weights, [8, 35, 3, 7, 5, 10])

        item_type = choice(choices(
            population=list(ItemFactory.types.keys()),
            weights=weights,
            k=len(list(ItemFactory.types.keys()))
        ))

        item_name = choice(choices(
            population=ItemFactory.types[item_type],
            k=len(ItemFactory.types[item_type])
        ))

        return ItemFactory._forge(item_name, item_type)

    @staticmethod
    def _generate(stats, item_name, item_type):
        return {
            "name": item_name,
            "type": item_type,
            "description": "",
            "stats": stats
        }

    @staticmethod
    def _stats(item_name, item_type):
        stats = factory_data.stats(item_type.split()[0])
        return ItemFactory._generate(stats, item_name, item_type)

    @staticmethod
    def _forge(item_name, item_type):
        new_name = []
        build = ItemFactory.sequence[item_type]

        seq = choice(choices(
            population=build["seq"],
            weights=build["w"],
            k=len(build["seq"])
        ))

        for lists in seq:
            if isinstance(lists, dict):
                this_list = lists.get(
                    item_type, lists.get("usable", ['']))
            elif lists:
                this_list = lists
            else:
                this_list = ['']

            this_word = choice(choices(
                population=this_list,
                k=len(this_list)
            ))

            if this_word:
                if this_word in ItemFactory.suffixes:
                    new_name[-1] += this_word
                    item_type = f"legendary {item_name}"
                else:
                    new_name.append(this_word)
            else:
                new_name.append(item_name)

        item_name = " ".join(new_name)
        return ItemFactory._stats(item_name, item_type)


class PlayerFactory:
    """Generate players for a room"""

    @staticmethod
    def build(i, room):
        """Make a player, give them items"""

        new_player = {
            "name": f"player {i}",
            "description": f"player {i} description",
            "location": room["name"],
            "inventory": {},
            "equipped": []
        }

        for _ in range(randint(1, 3)):
            new_item = ItemFactory.build("player")
            new_player["inventory"][new_item.pop("name")] = new_item

        for key, val in new_player["inventory"].items():
            if val["stats"]["equipable"]:
                new_player["equipped"].append(key)

        return new_player


class RoomFactory:
    """Generate rooms for a given maze"""

    #  N, S and E, W are backwards because numpy uses column-order
    moves = {
        "north": (1, 0), "south": (-1, 0),
        "east": (0, 1), "west": (0, -1),
    }

    @staticmethod
    def build(maze, rooms):
        """build a room"""

        RoomFactory.maze = maze
        RoomFactory.rooms = rooms
        RoomFactory.worldmap = {}
        return RoomFactory._make_rooms()

    @staticmethod
    def _make_rooms():
        i = 0
        for room in RoomFactory.rooms:
            x, y = room
            new_room = {
                "name": f"room {i}",
                "description": f"room {i} description",
                "coordinates": {
                    "x": x,
                    "y": y,
                },
                "adjacent": {},
                "players": {},
                "inventory": {},
            }

            for _ in range(randint(1, 7)):
                new_item = ItemFactory.build()
                new_room["inventory"][new_item.pop("name")] = new_item

            for _ in range(randint(0, 2)):
                new_player = PlayerFactory.build(i, new_room)
                new_room["players"][new_player["name"]] = new_player

            RoomFactory.worldmap[room] = new_room
            i += 1

        return RoomFactory._get_adj()

    @staticmethod
    def _get_adj():
        for coord, room in RoomFactory.worldmap.items():
            for direction in RoomFactory.moves:
                searching = True
                position = coord
                while searching:
                    position = tuple(
                        map(
                            add, position, RoomFactory.moves[direction]
                        )
                    )
                    if RoomFactory.maze[position] == MazeFactory.wall_color:
                        room["adjacent"][direction] = None
                        searching = False
                    elif RoomFactory.maze[position] in \
                            [MazeFactory.room_color, MazeFactory.player_color]:
                        room["adjacent"][direction] = \
                            RoomFactory.worldmap[position]["name"]
                        searching = False

        for coord, room in deepcopy(RoomFactory.worldmap).items():
            new_room = RoomFactory.worldmap.pop(coord)
            RoomFactory.worldmap[new_room.pop("name")] = new_room

        return RoomFactory.worldmap


class MazeFactory:
    """Generate a maze with rooms on intersections, corners, and dead-ends"""

    wall_color, path_color, room_color, player_color = (-2, 2, 1, 0)
    moves = factory_data.MOVES
    rules = factory_data.rules(wall_color, path_color)

    @staticmethod
    def draw(maze):
        """display the maze"""

        plt.figure(figsize=(len(maze[0])//2, len(maze)//2))
        plt.pcolormesh(maze, cmap=plt.cm.get_cmap("tab20b"))
        plt.axis("equal")
        plt.axis("off")
        plt.ion()
        plt.show()

    @staticmethod
    def update(maze):
        """update the maze display"""

        plt.pcolormesh(maze, cmap=plt.cm.get_cmap("tab20b"))
        plt.axis("equal")
        plt.axis("off")
        plt.draw()

    # pylint: disable=R0914
    @staticmethod
    def build():
        """generate a maze"""

        x = choice([10, 12, 14, 18])
        y = 148//x

        maze = npf((x+1, y+1), MazeFactory.wall_color)
        grid = [(i, j) for i in range(1, x+1, 2) for j in range(1, y+1, 2)]
        path = [choice(grid)]
        rooms = []
        position = path[0]
        grid.remove(position)

        while grid:
            n = len(path)
            nsew = []
            for move in MazeFactory.moves:
                nsew.append([
                    tuple(map(add, move[0], position)),
                    tuple(map(add, move[1], position))
                ])
            shuffle(nsew)
            for probe in nsew:
                if probe[0] in grid:
                    maze[probe[0]] = MazeFactory.path_color
                    maze[probe[1]] = MazeFactory.path_color
                    grid.remove(probe[0])
                    path.extend(probe)
                    break
            if n == len(path):
                position = path[max(path.index(position)-1, 1)]
            else:
                position = path[-1]

        for coord in path:
            i, j = coord
            neighbors = [
                maze[i-1, j],
                maze[i+1, j],
                maze[i, j-1],
                maze[i, j+1]
            ]
            if neighbors in MazeFactory.rules:
                rooms.append(coord)
                maze[coord] = MazeFactory.room_color
            maze[rooms[0]] = MazeFactory.player_color

        return {
            "maze": maze.tolist(),
            "rooms": RoomFactory.build(maze, rooms)
        }
