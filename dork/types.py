"""Base types for the Dork game"""

import os
from copy import deepcopy
from random import choices, choice, randint
from operator import add
import yaml
import matplotlib.pyplot as plt
from numpy import full as npf
import dork.game_utils.factory_data as factory_data
# pylint: disable=protected-access


class Holder():
    """A holder/container of items"""

    def __init__(self):
        self.inventory = dict

    def get_items(self, caller, verbose):
        """Print all inventory items"""

        if self.inventory:
            out = f"\n    inventory:"
        else:
            out = f"There's nothing here."

        def _verbose_print(data, calls=2):
            out = ""
            spc = "    "
            for key, val in data.items():
                if isinstance(val, dict):
                    out += "\n" + spc*calls + \
                        f"{key}:{_verbose_print(val, calls+1)}"
                elif val not in (0, ''):
                    out += "\n" + spc*calls + f"{key}: {val}"
            return out

        def _brief_print(data, calls=2):
            out = ""
            col = ""
            spc = "    "
            for key, val in data.items():
                if isinstance(val, dict) and calls < 3:
                    if calls < 2:
                        col = ":"
                    out += "\n" + spc*calls + \
                        f"{key}{col}{_brief_print(val, calls+1)}"
                # elif val not in (0, '') and calls < 2:
                #     out += spc*calls + f"\n{key}: {val}"
            return out

        if verbose:
            return out + _verbose_print(caller.data["inventory"])
        return out + _brief_print(caller.data["inventory"])


class Stats:
    """stats for items"""

    def __init__(self):
        self.data = dict
        self.attack = int
        self.strength = int
        self.weight = int
        self.luck = int
        self.equipable = bool

    def __str__(self):
        return str(self.data)


class Item(Stats):
    """An obtainable/usable item"""

    def __init__(self):
        super().__init__()
        self.data = dict
        self.name = str
        self.description = str
        self.type = str

    def __str__(self):
        return str(self.data)


class Player(Holder):
    """A player or npc in the game"""

    instances = []

    def __init__(self):
        super().__init__()
        self.data = dict
        self.name = str
        self.description = str
        self.location = Room
        self.equipped = list

    def _new_instance(self):
        self.instances.append(self)

    def __str__(self):
        return str(self.data)

    def move(self, cardinal, maze):
        """walk this way"""

        adjacent_room = getattr(self.location, cardinal)

        if not adjacent_room:
            out = f"You cannot go {cardinal} from here."
        else:
            maze[self.location.x][self.location.y] = MazeFactory.room_color

            self.location = adjacent_room
            maze[self.location.x][self.location.y] = MazeFactory.player_color

            out = self.location.description
            MazeFactory.update(maze)
        return out


class Room(Holder):
    """A room on the worldmap"""

    instances = []

    def __init__(self):
        super().__init__()
        self.data = dict
        self.description = str
        self.players = dict
        self.x = int
        self.y = int
        self.north = None
        self.south = None
        self.east = None
        self.west = None

    def _new_instance(self):
        self.instances.append(self)

    def __str__(self):
        return str(self.data)


class Gamebuilder:
    """Build an instance of Game"""

    @classmethod
    def build(cls, player_name=None):
        """Instantiate a game of Dork from dictionary"""

        if not player_name:
            player_name = input("What's your name, stranger? ")

        data = cls.load_game(player_name)

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

        game = cls._instantiate(Game, **data)
        setattr(game, "maze", data["maze"])
        setattr(game, "rooms", cls._make_rooms(deepcopy(data["rooms"])))

        cls._place_players(game)
        cls._make_paths(game)

        for player in Player.instances:
            if player.name == player_name:
                hero = player

        game.hero = hero
        game.maze[hero.location.x][hero.location.y] = MazeFactory.player_color
        return game

    @classmethod
    def _place_players(cls, game):
        for _, room in game.rooms.items():
            for _, player in room.players.items():
                player.location = room

    @classmethod
    def _make_paths(cls, game):
        adj = ["north", "south", "east", "west"]
        for _, room in game.rooms.items():
            for direction, room_name in vars(room).items():
                if room_name and direction in adj:
                    setattr(room, direction, game.rooms[room_name])

    @classmethod
    def _make_rooms(cls, rooms):

        factories = {
            "adjacent": cls._make_adjacent,
            "inventory": cls._make_item,
            "players": cls._make_player,
            "stats": cls._make_stats,
        }

        for name, room in rooms.items():
            new_room = cls._instantiate(Room, **room)
            for field, data in room.items():
                if field == "adjacent":
                    cls._make_adjacent(new_room, data)
                elif isinstance(data, dict):
                    room_field = getattr(new_room, field)
                    for sub in data:
                        room_field[sub] = factories[field](data[sub])
                else:
                    setattr(new_room, field, data)
            rooms[name] = new_room
            new_room._new_instance()
        return rooms

    @classmethod
    def _make_player(cls, player):
        new_player = cls._instantiate(Player, **player)
        for field, data in player.items():
            if isinstance(data, dict):
                inventory = getattr(new_player, field)
                for sub in data:
                    inventory[sub] = cls._make_item(data)
            else:
                setattr(new_player, field, data)
        new_player._new_instance()
        return new_player

    @classmethod
    def _make_item(cls, item):
        new_item = cls._instantiate(Item, **item)
        for field, data in item.items():
            if isinstance(data, dict):
                setattr(new_item, field, cls._make_stats(data))
            else:
                setattr(new_item, field, data)
        return new_item

    @classmethod
    def _make_adjacent(cls, room, adjacent):
        for key, val in adjacent.items():
            setattr(room, key, val)

    @classmethod
    def _make_stats(cls, stats):
        return cls._instantiate(Stats, **stats)

    @staticmethod
    def _instantiate(clz, **data):
        """return an object of type clz with attributes given by data"""

        new_obj = clz()
        setattr(new_obj, "data", data)
        for key, val in deepcopy(data).items():
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
        self.data = {}
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

    def _get_rooms(self):
        return str(self.rooms), False

    def _gtfo(self):
        return f"Thanks for playing DORK, {self.hero.name}!", True

    def _draw_maze(self):
        MazeFactory.draw(self.maze)
        return "", False

    def _move(self, cardinal):
        return self.hero.move(cardinal, self.maze), False

    def _examine(self):
        return self.hero.location.get_items(
            self.hero.location, self.verbose
        ), False

    def _inventory(self):
        return self.hero.get_items(self.hero, self.verbose), False

    def _look(self):
        return self.hero.location.description, False

    def _save_game(self):
        Gamebuilder.save_game(self.hero.name, self.data)
        return "game saved successfully!", False

    def _start_over(self):
        if self._confirm():
            Gamebuilder.build()
            out = ""
        else:
            out = "Guess you changed your mind!"
        return out, False

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

    @classmethod
    def build(cls, weights=None):
        """generate a random item"""

        weights = {
            "player": [8, 0, 0, 7, 5, 10]
        }.get(weights, [8, 35, 3, 7, 5, 10])

        item_type = choice(choices(
            population=list(cls.types.keys()),
            weights=weights,
            k=len(list(cls.types.keys()))
        ))

        item_name = choice(choices(
            population=cls.types[item_type],
            k=len(cls.types[item_type])
        ))

        return cls._forge(item_name, item_type)

    @classmethod
    def _generate(cls, unique_type, stats, item_name, item_type):
        return {
            "name": item_name,
            "type": " ".join([item_type, unique_type]),
            "description": "",
            "stats": stats
        }

    @classmethod
    def _stats(cls, unique_type, item_name, item_type):
        stats = factory_data.stats(item_type.split()[0])
        return cls._generate(unique_type, stats, item_name, item_type)

    @classmethod
    def _forge(cls, item_name, item_type):
        new_name = []
        unique_type = ""
        build = cls.sequence[item_type]

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
                if this_word in cls.suffixes:
                    new_name[-1] += this_word
                    unique_type = item_name
                    item_type = "legendary"
                else:
                    new_name.append(this_word)
            else:
                new_name.append(item_name)

        item_name = " ".join(new_name)
        return cls._stats(unique_type, item_name, item_type)


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

    moves = {
        "north": (1, 0), "south": (-1, 0),
        "east": (0, 1), "west": (0, -1),
    }

    # moves = {
    #     "north": (0, 1), "south": (0, -1),
    #     "east": (1, 0), "west": (-1, 0),
    # }

    @classmethod
    def build(cls, maze, rooms):
        """build a room"""

        cls.maze = maze
        cls.rooms = rooms
        cls.worldmap = {}
        return cls._make_rooms()

    @classmethod
    def _make_rooms(cls):
        i = 0
        for room in cls.rooms:
            x, y = room
            new_room = {
                "name": f"room {i}",
                "description": f"room {i} description",
                "x": x,
                "y": y,
                "adjacent": {},
                "players": {},
                "inventory": {},
            }

            for _ in range(randint(1, 7)):
                new_item = ItemFactory.build()
                new_room["inventory"][new_item.pop("name")] = new_item

            for _ in range(randint(0, 2)):
                new_player = PlayerFactory.build(i, new_room)
                new_room["players"][new_player.pop("name")] = new_player

            cls.worldmap[room] = new_room
            i += 1

        return cls._get_adj()

    @classmethod
    def _get_adj(cls):
        for coord, room in cls.worldmap.items():
            for direction in cls.moves:
                searching = True
                position = coord
                while searching:
                    position = tuple(map(add, position, cls.moves[direction]))
                    if cls.maze[position] == MazeFactory.wall_color:
                        room["adjacent"][direction] = None
                        searching = False
                    elif cls.maze[position] == MazeFactory.room_color:
                        room["adjacent"][direction] = \
                            cls.worldmap[position]["name"]
                        searching = False

        for coord, room in deepcopy(cls.worldmap).items():
            new_room = cls.worldmap.pop(coord)
            cls.worldmap[new_room.pop("name")] = new_room

        return cls.worldmap


class MazeFactory:
    """Generate a maze with rooms on intersections, corners, and dead-ends"""

    moves = factory_data.MOVES
    wall_color, path_color, room_color, player_color = (-2, 0, 1, 2)
    rules = factory_data.rules(wall_color, path_color)

    @staticmethod
    def draw(maze):
        """display the map"""

        plt.figure(figsize=(len(maze[0])//2, len(maze)//2))
        plt.pcolormesh(maze, cmap=plt.cm.get_cmap("tab20b"))
        plt.axis("equal")
        plt.axis("off")
        plt.ion()
        plt.show()

    @staticmethod
    def update(maze):
        """update the map display"""

        plt.pcolormesh(maze, cmap=plt.cm.get_cmap("tab20b"))
        plt.axis("equal")
        plt.axis("off")
        plt.draw()

    @classmethod
    def build(cls):
        """build a maze"""

        x = choice([10, 12, 14, 18])
        y = 148//x

        cls.rng_x = range(1, x+1, 2)
        cls.rng_y = range(1, y+1, 2)

        cls.maze = npf((x+1, y+1), fill_value=cls.wall_color)
        cls.grid = [(i, j) for i in cls.rng_x for j in cls.rng_y]
        cls.path = [choice(cls.grid)]
        cls.rooms = []

        return cls._generate()

    @classmethod
    def _generate(cls):
        k = cls.path[0]
        cls.grid.remove(k)
        while cls.grid:
            n = len(cls.path)
            nsew = cls._prb_lnk(k)
            for prb_lnk in nsew:
                probe, _ = prb_lnk
                if probe in cls.grid:
                    cls._walk(prb_lnk)
                    cls.grid.remove(probe)
                    cls.path.extend(prb_lnk)
                    break
            if n == len(cls.path):
                k = cls.path[max(cls.path.index(k)-1, 1)]
            else:
                k = cls.path[-1]
        return cls._get_rooms()

    @classmethod
    def _get_rooms(cls):
        for coord in cls.path:
            neighbors = cls._neighbors(coord)
            if neighbors in cls.rules:
                cls.rooms.append(coord)
                cls.maze[coord] = cls.room_color
        cls.maze[cls.path[0]] = cls.room_color
        cls.maze[cls.path[-2]] = cls.room_color

        return {
            "maze": cls.maze.tolist(),
            "rooms": RoomFactory.build(cls.maze, cls.rooms),
        }

    @classmethod
    def _prb_lnk(cls, coord):
        nsew = []
        for move in cls.moves:
            prb = tuple(map(add, move[0], coord))
            lnk = tuple(map(add, move[1], coord))
            nsew.append([prb, lnk])
        return choices(nsew, k=len(nsew))

    @classmethod
    def _neighbors(cls, coord):
        i, j = coord
        return [
            cls.maze[(i-1, j)],
            cls.maze[(i+1, j)],
            cls.maze[(i, j-1)],
            cls.maze[(i, j+1)],
        ]

    @classmethod
    def _walk(cls, coord):
        prb, lnk = coord
        cls.maze[prb] = cls.path_color
        cls.maze[lnk] = cls.path_color
