"""Base types for the Dork game"""
# -*- coding: utf-8 -*-
import os
from copy import deepcopy
from abc import ABC, abstractmethod
import yaml
from dork.game_utils.world_builder import MazeFactory
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

    def _take_item(self, item="all"):
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


class Gamebuilder:
    """Build an instance of Game"""

    @staticmethod
    def build(player_name):
        """Instantiate a game of Dork from dictionary"""

        data = Gamebuilder.load_game(player_name)

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

        game = Gamebuilder._instantiate(Game, **data)
        setattr(game, "maze", data["maze"])
        setattr(
            game, "rooms", Gamebuilder._make_rooms(
                deepcopy(data["rooms"])
            )
        )

        Gamebuilder._place_players(game)
        Gamebuilder._make_paths(game)

        for player in Player.instances:
            if player.name == player_name:
                hero = player

        game.hero = hero
        game.maze[hero.location.x][hero.location.y] = MazeFactory.player_color
        return game

    @staticmethod
    def _make_rooms(rooms):

        factories = {
            "adjacent": Gamebuilder._make_adjacent,
            "inventory": Gamebuilder._make_item,
            "players": Gamebuilder._make_player,
            "stats": Gamebuilder._make_stats,
        }

        for name, room in rooms.items():
            new_room = Gamebuilder._instantiate(Room, **room)
            for field, data in room.items():
                if field == "adjacent":
                    Gamebuilder._make_adjacent(new_room, data)
                elif field == "coordinates":
                    Gamebuilder._make_coord(new_room, data)
                elif isinstance(data, dict):
                    room_field = getattr(new_room, field)
                    for sub in data:
                        room_field[sub] = factories[field](data[sub])
                else:
                    setattr(new_room, field, data)
            rooms[name] = new_room
            new_room._new_instance()

        return rooms

    @staticmethod
    def _make_player(player):
        new_player = Gamebuilder._instantiate(Player, **player)
        for field, data in player.items():
            if isinstance(data, dict):
                inventory = getattr(new_player, field)
                for sub in data:
                    inventory[sub] = Gamebuilder._make_item(data)
            else:
                setattr(new_player, field, data)
        new_player._new_instance()
        return new_player

    @staticmethod
    def _make_item(item):
        new_item = Gamebuilder._instantiate(Item, **item)
        for field, data in item.items():
            if field == "stats":
                Gamebuilder._make_stats(new_item, data)
            else:
                setattr(new_item, field, data)
        return new_item

    @staticmethod
    def _make_adjacent(room, adjacent):
        for key, val in adjacent.items():
            setattr(room, key, val)

    @staticmethod
    def _make_coord(room, coord):
        setattr(room, "x", coord[0])
        setattr(room, "y", coord[1])

    @staticmethod
    def _make_stats(item, stats):
        for key, val in stats.items():
            setattr(item, key, val)

    @staticmethod
    def _place_players(game):
        for _, room in game.rooms.items():
            for _, player in room.players.items():
                player.location = room

    @staticmethod
    def _make_paths(game):
        adj = ["north", "south", "east", "west"]
        for _, room in game.rooms.items():
            for direction, room_name in vars(room).items():
                if room_name and direction in adj:
                    setattr(room, direction, game.rooms[room_name])

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