"""Base types for the Dork game"""
# -*- coding: utf-8 -*-
# from pprint import pprint
from abc import ABC, abstractmethod
import os
from copy import deepcopy
from random import choices, choice, randint, shuffle, randrange
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
        self.inventory = dict

    def get_items(self, caller, verbose):
        """Print all inventory items"""

        if self.inventory:
            out = f"\n    inventory:"
        else:
            out = f"There's nothing here."

        if verbose:
            return out + Game._verbose_print(caller.data["inventory"])
        return out + Game._brief_print(caller.data["inventory"])


class Stats:
    """stats for items"""

    def __init__(self):
        self.data = dict
        self.attack = int
        self.strength = int
        self.weight = int
        self.luck = int
        self.equipable = bool


class Item(Stats):
    """An obtainable/usable item"""

    def __init__(self):
        super().__init__()
        self.data = dict
        self.name = str
        self.description = str
        self.type = str
        self.usable = NotUsable

    def make(self, item):
        """Make an item
        """
        self.name = item["name"]
        self.description = item["description"]
        self.type = item["type"]
        if not isinstance(self.type, str) or self.type is None:
            self.usable = NotUsable
        elif len(self.type) > 1:
            self.set_usable(self.type)
        else:
            self.usable = NotUsable

    def set_usable(self, new_use):
        """This method changes the use behavior,
        provide usable class as argument"""
        uses = {"filler": NotUsable,
                "weapon": Attackable,
                "key": Openable,
                "gold": Payable,
                "magic items": Statable,
                "jewelry": Statable,
                "armor": Statable,
                "magic consumables": Statable}
        if new_use is None or new_use not in uses:
            self.usable = NotUsable
        else:
            self.usable = uses[new_use]

    def use(self, target, name):
        """Strategy pattern call"""
        self.usable.use(target, name)


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


class Statable(Usable):
    """Any object that can change stats"""

    @staticmethod
    def use(target, name):
        """Stat change use method"""
        print("The " + name + " takes effect on " + target)


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

    def move(self, cardinal, maze):
        """walk this way"""

        adjacent_room = getattr(self.location, cardinal)

        if not adjacent_room:
            out = f"You cannot go {cardinal} from here."
        else:
            maze[self.location.x][self.location.y] = MazeFactory.room_color

            adjacent_room.data["players"][self.name] = \
                self.location.data["players"].pop(self.name)
            self.location = adjacent_room
            maze[self.location.x][self.location.y] = MazeFactory.player_color

            outt = self.location.description
            # outtt = self.location.name
            out = "You have entered "+outt
            MazeFactory.update(maze)
        return out


class Room(Adjacent, Coord, Holder):
    """A room on the worldmap"""
    # pylint: disable=too-many-instance-attributes

    instances = []

    def __init__(self):
        super().__init__()
        self.name = "yeah"
        self.data = dict
        self.description = str
        self.players = dict

    def _new_instance(self):
        self.instances.append(self)


class Gamebuilder:
    """Build an instance of Game"""

    @classmethod
    def build(cls, player_name):
        """Instantiate a game of Dork from dictionary"""

        data = cls.load_game(player_name)

        if not data:
            data = MazeFactory.build()

            hero_data = {
                "name": player_name,
                "description": "the hero of dork!",
                "location": "Entrance",
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
                elif field == "coordinates":
                    cls._make_coord(new_room, data)
                elif isinstance(data, dict):
                    room_field = getattr(new_room, field)
                    for sub in data:
                        room_field[sub] = factories[field](data[sub])
                else:
                    setattr(new_room, field, data)
            rooms[name] = new_room
            new_room._new_instance()

        # print(rooms["room 1"].data)
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
            if field == "stats":
                cls._make_stats(new_item, data)
            else:
                setattr(new_item, field, data)
        return new_item

    @classmethod
    def _make_adjacent(cls, room, adjacent):
        for key, val in adjacent.items():
            setattr(room, key, val)

    @classmethod
    def _make_coord(cls, room, coord):
        setattr(room, "x", coord[0])
        setattr(room, "y", coord[1])

    @classmethod
    def _make_stats(cls, item, stats):
        for key, val in stats.items():
            setattr(item, key, val)

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
    dataaa = {}

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

    def _set_location(self):
        """Set location based on
        """

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

    def _look(self, x="n"):
        if x == "around":
            items = self.hero.location.inventory
            print("\nItems:")
            for item in items:
                print(item)
            print()
        return self.hero.location.description, False

    def _save_game(self):
        self._get_state()
        Gamebuilder.save_game(self.hero.name, self.data)
        return "game saved successfully!", False

    def _take(self, item="all"):
        # Item defaults to "all", and adds all items in room to inventory
        room_items = self.hero.location.inventory
        room_items2 = room_items.copy()
        player = self.hero.inventory
        if item == "all":
            for item_n in room_items2:
                player[item_n] = room_items.pop(item_n)
            return f"You took {item} item. You took them well.", False
        player[item] = room_items.pop(item)
        return f"You took the {item}. You took it well.", False

    def _drop_item(self, item="all"):
        """drops specific item from player to room"""
        player = self.hero.inventory
        player2 = player.copy()
        room_items = self.hero.location.inventory
        if item == "all":
            for item_n in player2:
                room_items[item_n] = player.pop(item_n)
            return "Oops, you can't hold all these items", False
        room_items = self.hero.location.inventory
        room_items[item] = player.pop(item)
        return "Oops, you dropped something!", False

    def _use_item(self, item="Nothing"):
        if item in self.hero.inventory.keys():
            target = input("What do you want to use it on? ")
            self.hero.inventory[item].use(target, item)
            return "You used the thing! It's super effective!", False
        return "You don't have that item...", False

    def _start_over(self):
        if self._confirm():
            out = ""
        else:
            out = "Guess you changed your mind!"
        return out, False

    def _get_state(self):
        for name, room in self.rooms.items():
            self.data["rooms"][name] = room.data

    @staticmethod
    def _verbose_print(data, calls=2):
        out = ""
        spc = "    "
        for key, val in data.items():
            if isinstance(val, dict):
                out += "\n" + spc*calls + \
                    f"{key}:{Game._verbose_print(val, calls+1)}"
            elif val not in (0, ''):
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
    def _generate(cls, stats, item_name, item_type):
        return {
            "name": item_name,
            "type": item_type,
            "description": "",
            "stats": stats
        }

    @classmethod
    def _stats(cls, item_name, item_type):
        stats = factory_data.stats(item_type.split()[0])
        return cls._generate(stats, item_name, item_type)

    @classmethod
    def _forge(cls, item_name, item_type):
        new_name = []
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
                    item_type = f"legendary {item_name}"
                else:
                    new_name.append(this_word)
            else:
                new_name.append(item_name)

        item_name = " ".join(new_name)
        return cls._stats(item_name, item_type)


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

        list_of_keys = factory_data.ROOMS
        shuffle(list_of_keys)
        list_of_adjtvs = factory_data.NAMES["adjectives"]
        shuffle(list_of_adjtvs)
        list_of_abstract = factory_data.NAMES["abstract"]
        shuffle(list_of_abstract)

        for room in cls.rooms:
            if i == 0:
                x, y = room
                new_room = {
                    "number": f"room 0",
                    "name": f"Entrance",
                    "description": factory_data.DEFAULT_ROOMS["Entrance"],
                    "coordinates": [x, y],
                    "adjacent": {},
                    "players": {},
                    "inventory": {},
                }
            elif i < len(cls.rooms) - 1:
                rand = list_of_keys[i]
                x, y = room
                new_room = {
                    "number": f"room {i}",
                    "name": rand,
                    "description": "The " + list_of_adjtvs[i] + rand +
                                   list_of_abstract[i],
                    "coordinates": [x, y],
                    "adjacent": {},
                    "players": {},
                    "inventory": {},
                }
            else:
                x, y = room
                new_room = {
                    "number": f"room "+str(len(cls.rooms)),
                    "name": f"End",
                    "description": factory_data.DEFAULT_ROOMS["End"],
                    "coordinates": [x, y],
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
                    elif cls.maze[position] in \
                            [MazeFactory.room_color, MazeFactory.player_color]:
                        room["adjacent"][direction] = \
                            cls.worldmap[position]["number"]
                        searching = False

        for coord, room in deepcopy(cls.worldmap).items():
            new_room = cls.worldmap.pop(coord)
            cls.worldmap[new_room.pop("number")] = new_room

        cls._get_adj_description(cls.worldmap)
        cls._get_room_inv_description(cls.worldmap)

        return cls.worldmap

    @classmethod
    def _get_room_inv_description(cls, worldmap):
        for rooms in worldmap:
            inv_list = worldmap[rooms]["inventory"]
            num = len(inv_list)
            if num > 2:
                first_desc = worldmap[rooms]["description"] + "\n"
                desc = factory_data.ROOM_INV_DESCRIPTIONS["1"]
                worldmap[rooms]["description"] = first_desc+desc
            elif num == 1:
                first_desc = worldmap[rooms]["description"] + "\n"
                desc = factory_data.ROOM_INV_DESCRIPTIONS["2"]
                worldmap[rooms]["description"] = first_desc+desc
        return 0

    @classmethod
    def _get_adj_description(cls, worldmap):
        for rooms in worldmap:
            desc = ""
            adj_list = list()
            adj_possibilities = {"north", "east", "south", "west"}
            for pos in adj_possibilities:
                if worldmap[rooms]["adjacent"][pos] is not None:
                    adj_list.append(pos)

            # if worldmap[rooms]["adjacent"]["north"] is not None:
            #    adj_list.append("North")
            # if worldmap[rooms]["adjacent"]["east"] is not None:
            #    adj_list.append("East")
            # if worldmap[rooms]["adjacent"]["south"] is not None:
            #    adj_list.append("South")
            # if worldmap[rooms]["adjacent"]["west"] is not None:
            #    adj_list.append("West")

            adj_string = ""
            for adj in adj_list:
                if adj_list[0] == adj:
                    adj_string += " "+adj
                else:
                    adj_string += ", "+adj
            adj_string += "..."

            if((len(adj_list) == 1)
               and rooms != "room 0" and rooms != "room "+str(len(cls.rooms))):
                desc = factory_data.ADJ_ROOM_DESCRIPTIONS["1"]
            elif len(adj_list) == 2:
                rand_ind = randrange(7)
                desc = factory_data.ADJ_ROOM_DESCRIPTIONS["2"][rand_ind] \
                    + adj_string
            elif len(adj_list) == 3:
                rand_ind = randrange(5)
                desc = factory_data.ADJ_ROOM_DESCRIPTIONS["3"][rand_ind] \
                    + adj_string
            first_desc = worldmap[rooms]["description"] + "\n"
            worldmap[rooms]["description"] = first_desc+desc

        return 0


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
        # plt.show()

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
