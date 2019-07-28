"""Base types for the Dork game"""
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import os
from copy import deepcopy
from random import choices, choice, randint, shuffle, randrange
from operator import add
from inspect import getfullargspec as argspec
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
        """Print all inventory items

        Displays all items held by self<player instance> or not. Verbose
        print displays more information about inventory.

        Args:
            out (str): Inventory
            verbose (str): Displays detailed inventory

        returns:
            verbose (str): Returns a formated/detailed inventory of player.

        """

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

        Extended Description

        Args:
            arg1 (str): description

        returns:
            arg1 (str): description

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
        provide usable class as argument

        Extended Description

        Args:
            arg1 (str): description

        returns:
            arg1 (str): description

        """
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
        """Strategy pattern call

        Extended Description

        Args:
            arg1 (str): description

        returns:
            arg1 (str): description

        """
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
        """walk this way

        Extended Description

        Args:
            arg1 (str): description

        returns:
            arg1 (str): description

        """
        adjacent_room = getattr(self.location, cardinal)

        if not adjacent_room:
            out = f"You cannot go {cardinal} from here."
        else:
            adjacent_room.data["players"][self.name] = \
                self.location.data["players"].pop(self.name)

            adjacent_room.players[self.name] = \
                self.location.players.pop(self.name)

            maze[self.location.x][self.location.y] = MazeFactory.room_color
            self.location = adjacent_room
            maze[self.location.x][self.location.y] = MazeFactory.player_color

            out = "You have entered " + self.location.description
            MazeFactory.update(maze)
        return out


class Room(Adjacent, Coord, Holder):
    """A room on the worldmap"""
    # pylint: disable=too-many-instance-attributes

    instances = []

    def __init__(self):
        super().__init__()
        self.name = str
        self.data = dict
        self.description = str
        self.players = dict

    def _new_instance(self):
        self.instances.append(self)


class Gamebuilder:
    """Build an instance of Game"""

    @classmethod
    def build(cls, player_name):
        """Instantiate a game of Dork from dictionary

        Extended Description

        Args:
            arg1 (str): description

        returns:
            arg1 (str): description

        """
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

        cls._get_adj_description(game)
        cls._get_room_inv_description(game)

        cls._place_players(game)
        cls._make_paths(game)

        for player in Player.instances:
            if player.name == player_name:
                hero = player

        game.hero = hero
        game.maze[hero.location.x][hero.location.y] = MazeFactory.player_color
        return game

    @classmethod
    def _get_room_inv_description(cls, worldmapp):
        worldmap = worldmapp.rooms
        worldmap_length = len(worldmap)
        iterator = 0
        for rooms in worldmap:
            if iterator != worldmap_length - 1:
                inv_list = worldmap[rooms].inventory
                num = len(inv_list)
                if num >= 2:
                    rand_ind = randrange(4)
                    first_desc = worldmap[rooms].description + "\n"
                    desc = factory_data.ROOM_INV_DESCRIPTIONS["1"][rand_ind]
                    worldmap[rooms].description = first_desc+desc
                elif num == 1:
                    first_desc = worldmap[rooms].description + "\n"
                    desc = factory_data.ROOM_INV_DESCRIPTIONS["2"]
                    worldmap[rooms].description = first_desc+desc
                elif num == 0:
                    first_desc = worldmap[rooms].description + "\n"
                    desc = factory_data.ROOM_INV_DESCRIPTIONS["3"]
                    worldmap[rooms].description = first_desc+desc
            iterator += 1
        return 0

    @classmethod
    def _get_adj_description(cls, worldmapp):

        worldmap = worldmapp.rooms

        for rooms in worldmap:
            desc = ""
            adj_list = list()
            adj_possibilities = {"north", "east", "south", "west"}
            for pos in adj_possibilities:
                if worldmap[rooms].data["adjacent"][pos] is not None:
                    adj_list.append(pos)

            adj_string = ""
            for adj in adj_list:
                if adj_list[0] == adj:
                    adj_string += " "+adj
                else:
                    adj_string += ", "+adj
            adj_string += "..."

            if((len(adj_list) == 1)
               and rooms != "room 0" and rooms != "room "+str(len(worldmap))):
                desc = factory_data.ADJ_ROOM_DESCRIPTIONS["1"]
            elif len(adj_list) == 2:
                rand_ind = randrange(8)
                desc = factory_data.ADJ_ROOM_DESCRIPTIONS["2"][rand_ind] \
                    + adj_string
            elif len(adj_list) == 3:
                rand_ind = randrange(5)
                desc = factory_data.ADJ_ROOM_DESCRIPTIONS["3"][rand_ind] \
                    + adj_string
            first_desc = worldmap[rooms].description + "\n"
            worldmap[rooms].description = first_desc+desc

        return 0

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
        """Load the save file associated with player

        Extended Description

        Args:
            arg1 (str): description

        returns:
            arg1 (str): description

        """
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
        """Save a game instance to a yaml file if it exists, else create one

        Extended Description

        Args:
            arg1 (str): description

        returns:
            arg1 (str): description

        """
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
        self.points = 10

    def __call__(self, cmd, arg):
        do_func = getattr(self, cmd)
        func_args = argspec(do_func).args
        if arg:
            if not func_args or ("self" in func_args and len(func_args) == 1):
                out = self._repl_error("This command takes no arguments")
            else:
                out = do_func(arg)
        else:
            out = do_func()
        return out

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

    def _points(self, user_input):
        if '_repl_error' in user_input:
            self.points = 0
        elif '_get_points' in user_input:
            pass
        else:
            self.points += 1
        return self.points

    def _get_points(self):
        point = self.points
        if point == 0:
            return f"Booooooo! you suck.\nYou have {point} points.", False
        return f"you have: {point}", False

    def _examine(self):
        out = ""
        location = self.hero.location
        if self.verbose:
            out += f"    players:" + Game._verbose_print(
                location.data["players"]
            )
            out += f"\n\n    inventory:" + Game._verbose_print(
                location.data["inventory"]
            )
        else:
            out += f"    players:" + Game._brief_print(
                location.data["players"]
            )
            out += f"\n\n    inventory:" + Game._brief_print(
                location.data["inventory"]
            )
        return out, False

    def _inventory(self):
        return self.hero.get_items(self.hero, self.verbose), False

    def _look(self):
        return self.hero.location.description, False

    def _save_game(self):
        self._get_state()
        Gamebuilder.save_game(self.hero.name, self.data)
        return "game saved successfully!", False

    # item_name defaults to None, so we take all items in room
    def _take_item(self, item_name=None):
        out = ""
        hero = self.hero
        room = hero.location
        if not item_name:
            room_copy = deepcopy(room.inventory)
            for item in room_copy:
                this_item = room.inventory.pop(item)
                this_data = room.data["inventory"].pop(item)
                hero.inventory[item] = this_item
                hero.data["inventory"][item] = this_data
                out += f"You took {item}\n"
        elif item_name in room.inventory:
            this_item = room.inventory.pop(item_name)
            this_data = room.data["inventory"].pop(item_name)
            hero.inventory[item_name] = this_item
            hero.data["inventory"][item_name] = this_data
            out += f"You took {item_name}. You took it well."
        else:
            out = f"There is no {item_name} here."

        self._update_room_inv_description(room)

        return out, False

    def _drop_item(self, item_name=None):
        out = ""
        hero = self.hero
        room = hero.location
        if not item_name:
            player_copy = deepcopy(hero.inventory)
            for item in player_copy:
                this_item = hero.inventory.pop(item)
                this_data = hero.data["inventory"].pop(item)
                room.inventory[item] = this_item
                room.data["inventory"][item] = this_data
                out += f"You dropped {item}\n"
        elif item_name in hero.inventory:
            this_item = hero.inventory.pop(item_name)
            this_data = hero.data["inventory"].pop(item_name)
            room.inventory[item_name] = this_item
            room.data["inventory"][item_name] = this_data
            out += f"You dropped {item_name}. How clumsy."
        else:
            out = f"There is no {item_name} in your inventory."

        self._update_room_inv_description(room)

        return out, False

    def _use_item(self, item="Nothing"):
        if item in self.hero.inventory.keys():
            target = input("What do you want to use it on? ")
            self.hero.inventory[item].use(target, item)
            return "You used the thing! It's super effective!", False
        return "You don't have that item...", False

    def _start_over(self):
        if self._confirm():
            out = "new game"
        else:
            out = "Guess you changed your mind!"
        return out, False

    def _get_state(self):
        for name, room in self.rooms.items():
            self.data["rooms"][name] = room.data

    @staticmethod
    def _update_room_inv_description(location):
        inv_list = location.inventory
        num = len(inv_list)
        description = location.description.splitlines()
        des = location.description
        if num > 1:
            rand_ind = randrange(4)
            des = description[0] + "\n" + description[1] + "\n" \
                + factory_data.ROOM_INV_DESCRIPTIONS["1"][rand_ind]
        if num == 1:
            des = description[0] + "\n" + description[1] \
                + "\n" + factory_data.ROOM_INV_DESCRIPTIONS["2"]
        elif num == 0:
            des = description[0] + "\n" + description[1] \
                + "\n" + factory_data.ROOM_INV_DESCRIPTIONS["3"]
        location.description = des
        return 0

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
        spc = "    "
        for key, val in data.items():
            if isinstance(val, dict) and calls < 3:
                out += "\n" + spc*calls + \
                    f"{key}{Game._brief_print(val, calls+1)}"
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
        """generate a random item

        Extended Description

        Args:
            arg1 (str): description

        returns:
            arg1 (str): description

        """
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
        """Make a player, give them items

        Extended Description

        Args:
            arg1 (str): description

        returns:
            arg1 (str): description

        """
        firsts = factory_data.FIRST_NAMES
        rand_first = choice(firsts)
        lasts = factory_data.LAST_NAMES
        rand_last = choice(lasts)
        new_player = {
            "name": rand_first + " " + rand_last,
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
        """build a room

        Extended Description

        Args:
            arg1 (str): description

        returns:
            arg1 (str): description

        """
        cls.maze = maze
        cls.rooms = rooms
        cls.worldmap = {}
        return cls._make_rooms()

    @classmethod
    def _make_rooms(cls):

        list_of_keys = factory_data.ROOMS
        shuffle(list_of_keys)
        list_of_adjtvs = factory_data.NAMES["adjectives"]
        shuffle(list_of_adjtvs)
        list_of_abstract = factory_data.NAMES["abstract"]
        shuffle(list_of_abstract)

        i = 0

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

        return cls.worldmap


class MazeFactory:
    """Generate a maze with rooms on intersections, corners, and dead-ends"""

    wall_color, path_color, room_color, player_color = (-2, 2, 1, 0)
    moves = factory_data.MOVES
    rules = factory_data.rules(wall_color, path_color)

    @staticmethod
    def draw(maze):
        """display the maze

        Extended Description

        Args:
            arg1 (str): description

        returns:
            arg1 (str): description

        """

        x_dim, y_dim = len(maze[0])//2, len(maze)//2
        plt.figure(figsize=(x_dim, y_dim))
        plt.pcolormesh(maze, cmap=plt.cm.get_cmap("tab20b"))
        plt.axis("equal")
        plt.axis("off")
        plt.ion()
        plt.show()

    @staticmethod
    def update(maze):
        """update the maze display

        Extended Description

        Args:
            arg1 (str): description

        returns:
            arg1 (str): description

        """
        plt.pcolormesh(maze, cmap=plt.cm.get_cmap("tab20b"))
        plt.axis("equal")
        plt.axis("off")
        plt.draw()

    # pylint: disable=R0914
    @staticmethod
    def build():
        """generate a maze

        Extended Description

        Args:
            arg1 (str): description

        returns:
            arg1 (str): description

        """
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
